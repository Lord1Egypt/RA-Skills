# Script 74: Interview Scoring

scores = []

n = int(input("Number of questions: "))

for i in range(n):
    s = float(input(f"Score for Q{i+1}: "))
    scores.append(s)

average = sum(scores) / len(scores)

print(f"Average Score = {average:.2f}")
