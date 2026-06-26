# Script 62: ETAP Prompt Manager

prompts = []

while True:
    cmd = input("Add/View/Exit: ").lower()

    if cmd == "add":
        p = input("Enter ETAP prompt: ")
        prompts.append(p)
    elif cmd == "view":
        for i, p in enumerate(prompts):
            print(f"{i+1}. {p}")
    elif cmd == "exit":
        break
