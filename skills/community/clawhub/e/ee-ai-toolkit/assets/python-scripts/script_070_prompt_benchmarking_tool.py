# Script 70: Prompt Benchmark

prompts = {
    "calculate power": 4.5,
    "design circuit": 4.8,
    "fault analysis": 4.2
}

best = max(prompts, key=prompts.get)

print("Best Prompt:", best)
print("Score:", prompts[best])
