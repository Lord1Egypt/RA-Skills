# Script 72: Skills Gap Analyzer

required = {"python", "ai", "power systems", "matlab"}
user = set(input("Enter your skills (space separated): ").lower().split())

missing = required - user

print("Missing Skills:", missing)
