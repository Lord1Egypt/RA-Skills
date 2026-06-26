# Script 21: Prompt Quality Analyzer

def analyze_prompt(prompt):
    score = 0

    if "calculate" in prompt.lower():
        score += 1
    if "step-by-step" in prompt.lower():
        score += 1
    if "with equations" in prompt.lower():
        score += 1
    if "example" in prompt.lower():
        score += 1

    return score

prompt = input("Enter prompt: ")

score = analyze_prompt(prompt)
print(f"Prompt Quality Score: {score}/4")
