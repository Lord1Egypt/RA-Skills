#!/usr/bin/env python3
"""
Aaron — Dental Receptionist & Orchestrator
Persistent agent managing all IRL dental appointments for the CFO.
Named after Aaron who held Moses' arms when he couldn't hold them himself.
"""

import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
AARON_DIR = WORKSPACE / "aaron"
RECORDS_FILE = AARON_DIR / "dental-records.json"
LOG_FILE = AARON_DIR / "aaron-log.jsonl"

AARON_DIR.mkdir(exist_ok=True)

DEFAULT_RECORDS = {
    "cfo": "Allowed Feminism — NYC commuter, A line, Eastern time",
    "dentist": {
        "name": None,
        "address": None,
        "phone": None,
        "in_network": None,
        "specialty": "General / Cosmetic"
    },
    "insurance": {
        "provider": None,
        "plan": None,
        "group_number": None,
        "member_id": None
    },
    "appointments": [],
    "pending_treatments": [],
    "last_cleaning": None,
    "notes": []
}

def load_records():
    if RECORDS_FILE.exists():
        return json.loads(RECORDS_FILE.read_text())
    records = DEFAULT_RECORDS.copy()
    save_records(records)
    return records

def save_records(records):
    RECORDS_FILE.write_text(json.dumps(records, indent=2))

def log(entry):
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    mode = "a" if LOG_FILE.exists() else "w"
    with open(LOG_FILE, mode) as f:
        f.write(json.dumps(entry) + "\n")

def days_since(date_str):
    if not date_str:
        return None
    try:
        d = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - d).days
    except:
        return None

def upcoming_appointments(records, within_hours=48):
    upcoming = []
    now = datetime.now(timezone.utc)
    for appt in records.get("appointments", []):
        if appt.get("status") == "completed":
            continue
        try:
            appt_dt = datetime.fromisoformat(appt["datetime"].replace("Z", "+00:00"))
            delta = appt_dt - now
            if 0 <= delta.total_seconds() <= within_hours * 3600:
                upcoming.append((appt, delta))
        except:
            continue
    return upcoming

def status(records):
    print("\n🦷 AARON — Dental Status Report")
    print("=" * 45)

    # Dentist
    d = records.get("dentist", {})
    if d.get("name"):
        print(f"Dentist:     {d['name']}")
        print(f"Address:     {d.get('address', 'not recorded')}")
        print(f"In-network:  {d.get('in_network', 'unknown')}")
    else:
        print("Dentist:     ⚠️  Not recorded yet")

    # Insurance
    ins = records.get("insurance", {})
    if ins.get("provider"):
        print(f"Insurance:   {ins['provider']} / {ins.get('plan', '?')}")
    else:
        print("Insurance:   ⚠️  Not recorded yet")

    # Last cleaning
    lc = records.get("last_cleaning")
    age = days_since(lc)
    if age is not None:
        flag = "⚠️ OVERDUE" if age > 180 else "✅"
        print(f"Last cleaning: {lc[:10]} ({age} days ago) {flag}")
    else:
        print("Last cleaning: ⚠️  Not recorded")

    # Upcoming appointments
    upcoming = upcoming_appointments(records, within_hours=72)
    if upcoming:
        print(f"\n📅 Upcoming (next 72h):")
        for appt, delta in upcoming:
            h = int(delta.total_seconds() // 3600)
            print(f"  • {appt['datetime'][:16]} — {appt.get('type', 'appointment')} ({h}h from now)")
            if appt.get("dentist"):
                print(f"    {appt['dentist']}")
            if appt.get("address"):
                print(f"    {appt['address']}")
    else:
        print("\n📅 No appointments in next 72h")

    # Pending treatments
    pending = [t for t in records.get("pending_treatments", []) if not t.get("completed")]
    if pending:
        print(f"\n⚕️  Pending treatments ({len(pending)}):")
        for t in pending:
            age_str = ""
            if t.get("recommended_date"):
                d_age = days_since(t["recommended_date"])
                if d_age:
                    age_str = f" (recommended {d_age}d ago)"
            print(f"  • {t['treatment']}{age_str}")
    else:
        print("\n⚕️  No pending treatments")

    # All appointments history
    all_appts = records.get("appointments", [])
    completed = [a for a in all_appts if a.get("status") == "completed"]
    print(f"\n📋 Appointment history: {len(completed)} completed, {len(all_appts) - len(completed)} upcoming")

def remind(records):
    """Check for upcoming reminders and print them."""
    upcoming_48 = upcoming_appointments(records, within_hours=48)
    upcoming_2 = upcoming_appointments(records, within_hours=2)

    if upcoming_2:
        for appt, delta in upcoming_2:
            h = int(delta.total_seconds() // 3600)
            print(f"⏰ 2-HOUR REMINDER")
            print(f"Your {appt.get('type', 'dental appointment')} is in {h} hour(s).")
            if appt.get("address"):
                print(f"Location: {appt['address']}")
            print(f"NYC commuter note: Check A line service, allow 45-60min from Howard Beach.")
            print(f"Bring: insurance card, photo ID, any X-rays if new patient.")
    elif upcoming_48:
        for appt, delta in upcoming_48:
            h = int(delta.total_seconds() // 3600)
            print(f"📅 48-HOUR REMINDER")
            print(f"Your {appt.get('type', 'dental appointment')} is in ~{h} hours.")
            if appt.get("datetime"):
                print(f"When: {appt['datetime'][:16]}")
            if appt.get("address"):
                print(f"Where: {appt['address']}")
            print(f"Prep: nothing to eat/drink 1h before cleaning. Brush before you go.")
            print(f"Bring: insurance card + photo ID.")
    else:
        # Check overdue cleaning
        lc = records.get("last_cleaning")
        age = days_since(lc)
        if age is not None and age > 180:
            print(f"🦷 It's been {age} days since your last cleaning (recommended every 180).")
            print(f"Want me to find available slots? Just say the word.")
        else:
            print("✅ No upcoming dental reminders. You're all set.")

def add_appointment_interactive(records):
    print("\nAdding new appointment. (Press Enter to skip optional fields)")
    appt = {}
    appt["type"] = input("Type (cleaning/checkup/filling/crown/etc): ").strip() or "checkup"
    appt["datetime"] = input("Date/time (YYYY-MM-DD HH:MM): ").strip()
    appt["dentist"] = input("Dentist name (optional): ").strip() or None
    appt["address"] = input("Address (optional): ").strip() or None
    appt["notes"] = input("Notes (optional): ").strip() or None
    appt["status"] = "scheduled"
    appt["created"] = datetime.now(timezone.utc).isoformat()

    records.setdefault("appointments", []).append(appt)
    save_records(records)
    log({"action": "add_appointment", "appointment": appt})
    print(f"✅ Added: {appt['type']} on {appt['datetime']}")

def add_treatment(records, treatment_str):
    treatment = {
        "treatment": treatment_str,
        "recommended_date": datetime.now(timezone.utc).isoformat(),
        "completed": False,
        "completed_date": None
    }
    records.setdefault("pending_treatments", []).append(treatment)
    save_records(records)
    log({"action": "add_treatment", "treatment": treatment_str})
    print(f"✅ Treatment logged: {treatment_str}")
    print(f"Aaron will track this until it's completed.")

def main():
    parser = argparse.ArgumentParser(description="Aaron — Dental Receptionist")
    parser.add_argument("--status", action="store_true", help="Show full dental status")
    parser.add_argument("--remind", action="store_true", help="Check for upcoming reminders")
    parser.add_argument("--add-appointment", action="store_true", help="Add a new appointment")
    parser.add_argument("--add-treatment", type=str, help="Log a pending treatment recommendation")
    parser.add_argument("--last-cleaning", type=str, help="Set last cleaning date (YYYY-MM-DD)")
    args = parser.parse_args()

    records = load_records()

    if args.last_cleaning:
        records["last_cleaning"] = args.last_cleaning + "T00:00:00Z"
        save_records(records)
        print(f"✅ Last cleaning set to {args.last_cleaning}")
        return

    if args.add_treatment:
        add_treatment(records, args.add_treatment)
        return

    if args.add_appointment:
        add_appointment_interactive(records)
        return

    if args.remind:
        remind(records)
        return

    # Default: status
    status(records)

if __name__ == "__main__":
    main()
