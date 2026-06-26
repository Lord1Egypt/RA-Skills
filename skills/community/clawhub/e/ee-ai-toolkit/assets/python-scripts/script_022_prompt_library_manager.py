# Script 22: Prompt Library Manager

import json

prompts = {}

while True:
    choice = input("Add/View/Exit: ").lower()

    if choice == "add":
        key = input("Enter category: ")
        value = input("Enter prompt: ")
        prompts.setdefault(key, []).append(value)

    elif choice == "view":
        print(json.dumps(prompts, indent=2))

    elif choice == "exit":
        break
