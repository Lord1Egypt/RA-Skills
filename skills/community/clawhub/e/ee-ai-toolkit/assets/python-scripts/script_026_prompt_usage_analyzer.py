# Script 26: Prompt Usage Analyzer

from collections import Counter

prompts = [
    "calculate power",
    "calculate power",
    "design circuit",
    "load flow analysis",
    "calculate power"
]

count = Counter(prompts)

print("Usage Frequency:")
for k, v in count.items():
    print(k, ":", v)
