# Script 65: Prompt Search

prompts = [
    "calculate power",
    "design circuit",
    "analyze load flow",
    "write report"
]

keyword = input("Enter search keyword: ")

results = [p for p in prompts if keyword in p]

print("Matching Prompts:")
for r in results:
    print("-", r)
