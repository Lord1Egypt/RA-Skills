import json
import os
from datetime import datetime, date

def check_follow_ups(days_threshold=5):
    # Dynamic path resolution for ClawHub
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(skill_dir, "clients.json")
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    today = date.today()
    overdue = []

    for client in data.get("clients", []):
        if client.get("status") != "active":
            continue
        
        last_contact_str = client.get("last_contact")
        if not last_contact_str:
            continue
            
        try:
            last = datetime.strptime(last_contact_str, "%Y-%m-%d").date()
        except ValueError:
            continue
            
        days_silent = (today - last).days

        if days_silent >= days_threshold:
            overdue.append({
                "name": client.get("name"),
                "phone": client.get("phone"),
                "days_silent": days_silent,
                "project": client.get("project")
            })

    return overdue

if __name__ == "__main__":
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(skill_dir, "config.json")
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            threshold = config.get("follow_up_days", 5)
    except:
        threshold = 5

    results = check_follow_ups(days_threshold=threshold)
    if not results:
        print("No follow-ups needed today.")
    else:
        for c in results:
            print(f"{c['name']} — {c['days_silent']} days silent — {c['project']}")
