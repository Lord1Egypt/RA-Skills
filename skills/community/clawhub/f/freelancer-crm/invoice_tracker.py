import json
import os
from datetime import datetime, date

def check_overdue_invoices(reminder_days=7):
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
        if client.get("invoice_status") != "sent":
            continue
        
        sent_date_str = client.get("invoice_sent_date")
        if not sent_date_str:
            continue
            
        try:
            sent_date = datetime.strptime(sent_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue
            
        days_since_sent = (today - sent_date).days

        if days_since_sent >= reminder_days:
            overdue.append({
                "name": client.get("name"),
                "phone": client.get("phone"),
                "amount": client.get("invoice_amount"),
                "days_overdue": days_since_sent,
                "project": client.get("project")
            })

    return overdue

if __name__ == "__main__":
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(skill_dir, "config.json")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            reminder_days = config.get("invoice_reminder_days", 7)
    except:
        reminder_days = 7

    results = check_overdue_invoices(reminder_days=reminder_days)
    if not results:
        print("No overdue invoices today.")
    else:
        for c in results:
            print(f"{c['name']} — ${c['amount']} — {c['days_overdue']} days overdue — {c['project']}")
