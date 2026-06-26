# Script 71: Resume Keyword Analyzer

keywords = ["AI", "Python", "Power Systems", "MATLAB", "Machine Learning"]

resume = input("Paste your resume text:\n").lower()

score = sum(1 for k in keywords if k.lower() in resume)

print(f"Keyword Match Score: {score}/{len(keywords)}")
