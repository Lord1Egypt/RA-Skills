import subprocess
import os

def get_changed_files():
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only"],
            text=True
        )
        return [f for f in output.splitlines() if f]
    except:
        return []

def analyze_file(file_path):
    total = 0
    ai = 0
    state = "ai"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "@human" in line:
                    state = "human"
                    continue
                if "@ai" in line:
                    state = "ai"
                    continue

                if line.strip():
                    total += 1
                    if state == "ai":
                        ai += 1
    except:
        pass

    return total, ai

def analyze_all():
    files = get_changed_files()

    total_sum = 0
    ai_sum = 0

    for file in files:
        if os.path.isfile(file):
            total, ai = analyze_file(file)
            total_sum += total
            ai_sum += ai

    percent = round((ai_sum / total_sum) * 100) if total_sum else 0

    return total_sum, ai_sum, percent