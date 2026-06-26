# Script 29: Export Prompts

import csv

prompts = ["calculate power", "design circuit", "analyze fault"]

with open("prompts.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Prompt"])

    for p in prompts:
        writer.writerow([p])

print("Exported to prompts.csv")
