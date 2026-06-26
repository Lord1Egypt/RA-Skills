# Script 98: Multi-Criteria Decision

options = {
    "Option A": [0.8, 0.7, 0.9],
    "Option B": [0.9, 0.6, 0.8]
}

weights = [0.4, 0.3, 0.3]

scores = {}

for k, v in options.items():
    scores[k] = sum(w*x for w, x in zip(weights, v))

best = max(scores, key=scores.get)

print("Best Option:", best)
print("Score:", scores[best])
