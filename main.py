from fastapi import FastAPI
import pandas as pd
import pickle
from iteration_utilities import unique_everseen
from iteration_utilities import duplicates

job_list = pickle.load(open('job1_dict.pkl', 'rb'))
job1 = pd.DataFrame(job_list)
similarity = pickle.load(open('similarity1.pkl', 'rb'))


def recommend(job_name):
    job_index = job1[job1['KEY_SKILL'] == job_name].index[0]
    distances = similarity[job_index]
    job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_job = []
    for i in job_list:
        recommended_job.append(job1.iloc[i[0]].JOB_TYPE)
    recommended_job1 = set(recommended_job)
    return recommended_job1


def recommend_ug(job_name):
    job_index = job1[job1['UG'] == job_name].index[0]
    distances = similarity[job_index]
    job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_job = []
    for i in job_list:
        recommended_job.append(job1.iloc[i[0]].JOB_TYPE)
    recommended_job1 = set(recommended_job)
    return recommended_job1


def recommend_spe(job_name):
    job_index = job1[job1['SPECIALIZATION'] == job_name].index[0]
    distances = similarity[job_index]
    job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_job = []
    for i in job_list:
        recommended_job.append(job1.iloc[i[0]].JOB_TYPE)
    recommended_job1 = set(recommended_job)
    return recommended_job1


def recommend_inti(job_name):
    job_index = job1[job1['INTERESTS'] == job_name].index[0]
    distances = similarity[job_index]
    job_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_job = []
    for i in job_list:
        recommended_job.append(job1.iloc[i[0]].JOB_TYPE)
    recommended_job1 = set(recommended_job)
    return recommended_job1



app = FastAPI()

@app.get("/")
async def root():
  return {"message": "This is a Career Recommendation API Designed for VNR Hackathon Nov 2022"}


UG1 = set(job1['UG'].values)
SPEC1 = set(job1['SPECIALIZATION'].values)
SKILLS = set(job1['KEY_SKILL'].values)
INTERESTS = set(job1['INTERESTS'].values)

@app.get("/getUGOptions")
async def getUGOptions():
  return {"options": UG1}

@app.get("/getSpecOptions")
async def getSpecOptions():
  return {"options": SPEC1}

@app.get("/getSkillsOptions")
async def getSkillsOptions():
  return {"options": SKILLS}

@app.get("/getInterestsOptions")
async def getInterestsOptions():
  return {"options": INTERESTS}

@app.get("/getRecommendations")
async def getRecommendations(selected_ug: str, selected_Specialization: str, skills_array: str, interests_array: str):
  skills_array = skills_array.split(',')
  interests_array = interests_array.split(',')

  pandas_skills_array = pd.Series(skills_array)
  final_skills_array = pandas_skills_array.values
  pandas_interests_array = pd.Series(interests_array)
  final_interests_array = pandas_interests_array.values
  final_interests_array = [] if final_interests_array == [''] else final_interests_array
  final_skills_array = [] if final_skills_array == [''] else final_skills_array
  recommendation = []

  for i in final_skills_array:
      recommendation.extend(recommend(i))

  for i in final_interests_array:
      recommendation.extend(recommend_inti(i))
  recommendation.extend(recommend_ug(selected_ug))
  recommendation.extend(recommend_spe(selected_Specialization))
  result = pd.DataFrame(unique_everseen(duplicates(recommendation)))
  return {"recommendations": result}