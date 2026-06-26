# Script 69: Metadata Extractor

def extract(prompt):
    return {
    "has_calculation": "calculate" in prompt,
    "has_steps": "step-by-step" in prompt,
    "has_equations": "equation" in prompt
    }

p = input("Enter prompt: ")

meta = extract(p.lower())

print("Metadata:")
for k, v in meta.items():
    print(k, ":", v)
