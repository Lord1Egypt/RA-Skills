# Script 8: Prompt Validator

def validate_prompt(prompt):
    keywords = ["calculate", "explain", "design"]
    score = sum(1 for word in keywords if word in prompt.lower())
    return score

prompt = input("Enter your prompt: ")
score = validate_prompt(prompt)

print(f"Prompt Quality Score: {score}/3")
