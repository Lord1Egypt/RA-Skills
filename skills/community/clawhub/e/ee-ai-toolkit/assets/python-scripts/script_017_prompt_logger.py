# Script 17: Prompt Logger

prompt = input("Enter prompt: ")

with open("prompts.txt", "a") as f:
    f.write(prompt + "\n")

print("Prompt saved.")
