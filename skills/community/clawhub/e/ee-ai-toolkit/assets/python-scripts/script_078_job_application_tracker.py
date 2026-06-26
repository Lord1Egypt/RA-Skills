# Script 78: Job Tracker

jobs = []

while True:
    company = input("Company (or 'exit'): ")

    if company == "exit":
        break

    status = input("Status (applied/interview/offer): ")
    jobs.append((company, status))

print("\nApplications:")
for j in jobs:
    print(j[0], "-", j[1])
