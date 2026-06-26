# Script 23: Prompt Rewriter

def improve_prompt(prompt):
    return f"Act as an electrical engineer. {prompt}. Provide step-by-step solution with formulas."

p = input("Enter weak prompt: ")
print("Improved Prompt:")
print(improve_prompt(p))
