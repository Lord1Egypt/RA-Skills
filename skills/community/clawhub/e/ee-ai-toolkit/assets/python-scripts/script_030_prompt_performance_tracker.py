# Script 30: Prompt Performance Tracker

prompts = {
    "calculate power": 4,
    "design circuit": 5,
    "load flow": 3
}

sorted_prompts = sorted(prompts.items(), key=lambda x: x[1], reverse=True)

print("Top Prompts:")
for p, score in sorted_prompts:
    print(p, "->", score)
