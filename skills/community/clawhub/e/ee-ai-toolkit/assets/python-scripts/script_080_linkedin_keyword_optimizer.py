# Script 80: LinkedIn Optimizer

keywords = ["AI", "Electrical Engineer", "Python", "Power Systems"]

profile = input("Paste LinkedIn summary:\n").lower()

missing = [k for k in keywords if k.lower() not in profile]

print("Suggested Keywords to Add:")
for m in missing:
    print("-", m)
