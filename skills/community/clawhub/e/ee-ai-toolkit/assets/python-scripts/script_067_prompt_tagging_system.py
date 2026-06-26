# Script 67: Prompt Tagging

def tag_prompt(prompt):
    tags = []

    if "power" in prompt:
        tags.append("Power Systems")
    if "circuit" in prompt:
        tags.append("Circuit Design")
    if "fault" in prompt:
        tags.append("Protection")

    return tags

p = input("Enter prompt: ")

print("Tags:", tag_prompt(p.lower()))
