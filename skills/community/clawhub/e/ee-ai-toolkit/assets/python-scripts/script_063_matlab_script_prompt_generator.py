# Script 63: MATLAB Prompt Generator

task = input("Enter engineering task: ")

prompt = f"""
Generate MATLAB code to:
{task}

Include:
- comments
- input/output variables
- plots if required
"""

print(prompt)
