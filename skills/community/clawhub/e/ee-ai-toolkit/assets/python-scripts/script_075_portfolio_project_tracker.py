# Script 75: Portfolio Tracker

projects = []

while True:
    name = input("Enter project name (or 'exit'): ")

    if name == "exit":
        break

    status = input("Status (ongoing/completed): ")
    projects.append((name, status))

print("\nProjects:")
for p in projects:
    print(p[0], "-", p[1])
