# Script 100: Decision Support

options = {
    "Design A": {"cost": 100, "efficiency": 90},
    "Design B": {"cost": 120, "efficiency": 95}
}

score = {}

for k, v in options.items():
    score[k] = v["efficiency"] / v["cost"]

best = max(score, key=score.get)

print("Best Design:", best)
print("Score:", score[best])
