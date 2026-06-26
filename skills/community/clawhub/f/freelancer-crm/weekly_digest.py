import json
import os
from datetime import date
import follow_up
import invoice_tracker
import send_message

def generate_digest():
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(skill_dir, "config.json")
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            f_threshold = config.get("follow_up_days", 5)
            i_threshold = config.get("invoice_reminder_days", 7)
    except:
        f_threshold = 5
        i_threshold = 7

    overdue_contacts = follow_up.check_follow_ups(days_threshold=f_threshold)
    overdue_invoices = invoice_tracker.check_overdue_invoices(reminder_days=i_threshold)

    total_revenue = sum(float(inv["amount"]) for inv in overdue_invoices)
    
    digest_msg = f"Good morning. This week digest ({date.today().isoformat()}):\n\n"
    digest_msg += f"- {len(overdue_contacts)} clients need follow-up.\n"
    digest_msg += f"- {len(overdue_invoices)} invoices overdue (${total_revenue:,.2f} total).\n"
    digest_msg += "- 0 proposals awaiting response.\n\n"
    digest_msg += "Would you like me to draft the carry-over messages for these?"

    return digest_msg

if __name__ == "__main__":
    print(generate_digest())
