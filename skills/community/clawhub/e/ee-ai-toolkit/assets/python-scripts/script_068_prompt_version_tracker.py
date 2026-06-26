# Script 68: Prompt Version Tracker

history = []

while True:
    p = input("Enter prompt (or 'exit'): ")

    if p == "exit":
        break

    history.append(p)

print("\nPrompt Versions:")
for i, h in enumerate(history):
    print(f"Version {i+1}: {h}")
