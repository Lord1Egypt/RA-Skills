# Script 61: Power System Prompt Pack

def generate_prompts(system_type):
    prompts = [
    f"Perform load flow analysis for a {system_type} system.",
    f"Calculate fault current in a {system_type} network.",
    f"Analyze voltage stability of a {system_type} system."
    ]
    return prompts

system = input("Enter system type: ")

for p in generate_prompts(system):
    print("-", p)
