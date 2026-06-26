# Script 28: Relay Prompt Generator

def generate_prompt(system):
    return f"Analyze relay coordination for a {system} system and provide settings."

system = input("Enter system type: ")
print(generate_prompt(system))
