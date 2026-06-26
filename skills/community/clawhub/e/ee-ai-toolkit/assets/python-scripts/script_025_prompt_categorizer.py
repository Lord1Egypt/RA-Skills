# Script 25: Prompt Categorizer

def categorize(prompt):
    if "load" in prompt:
        return "Power Systems"
    elif "circuit" in prompt:
        return "Circuit Design"
    elif "report" in prompt:
        return "Documentation"
    else:
        return "General"

p = input("Enter prompt: ")
print("Category:", categorize(p.lower()))
