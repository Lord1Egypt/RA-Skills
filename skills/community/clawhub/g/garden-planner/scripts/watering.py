#!/usr/bin/env python3
"""
watering.py - Track watering schedules and remind what needs water today.
Usage:
  watering.py status                      # Show what needs watering
  watering.py log --target bed-A          # Log a watering event now
  watering.py log --target bed-A --date 2025-06-10
  watering.py set --target bed-A --days 2 --notes "Deep water"
  watering.py list                        # Show all schedules
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/garden")
GARDEN_FILE = os.path.join(DATA_DIR, "garden.json")


def load_garden(garden_file):
    if not os.path.exists(garden_file):
        return None
    with open(garden_file) as f:
        return json.load(f)


def save_garden(garden, garden_file):
    os.makedirs(os.path.dirname(garden_file), exist_ok=True)
    with open(garden_file, "w") as f:
        json.dump(garden, f, indent=2)


def get_schedules(garden):
    return garden.setdefault("watering_schedules", [])


def find_schedule(schedules, target):
    for s in schedules:
        if s.get("target", "").lower() == target.lower():
            return s
    return None


def days_overdue(last_watered_str, frequency_days, today):
    """Return positive int if overdue, 0 if due today, negative if not yet due."""
    if not last_watered_str:
        return frequency_days  # never watered = overdue by full cycle
    try:
        last = datetime.strptime(last_watered_str, "%Y-%m-%d").date()
    except ValueError:
        return frequency_days
    next_water = last + timedelta(days=frequency_days)
    return (today - next_water).days


def status_cmd(garden, today):
    """Show watering status for all scheduled beds/plants."""
    schedules = get_schedules(garden)
    if not schedules:
        print("No watering schedules set. Use: watering.py set --target bed-A --days 2")
        return

    needs_water = []
    ok_soon = []
    on_track = []

    for s in schedules:
        target = s.get("target", "unknown")
        freq = s.get("frequency_days", 1)
        last = s.get("last_watered")
        notes = s.get("notes", "")
        overdue = days_overdue(last, freq, today)

        entry = {
            "target": target,
            "frequency_days": freq,
            "last_watered": last or "never",
            "notes": notes,
            "overdue_days": overdue,
        }

        if overdue >= 0:
            needs_water.append(entry)
        elif overdue == -1:
            ok_soon.append(entry)
        else:
            on_track.append(entry)

    print(f"\n{'='*56}")
    print(f"💧  Watering Status — {today.strftime('%B %d, %Y')}")
    print(f"{'='*56}")

    if needs_water:
        print(f"\n  🚿  NEEDS WATER NOW ({len(needs_water)})")
        print(f"  {'─'*48}")
        for e in sorted(needs_water, key=lambda x: -x["overdue_days"]):
            overdue_str = (
                f"OVERDUE by {e['overdue_days']}d" if e["overdue_days"] > 0
                else "DUE TODAY"
            )
            print(f"  • {e['target']:<20} [{overdue_str}]")
            print(f"    Last: {e['last_watered']}  |  Every {e['frequency_days']}d", end="")
            if e["notes"]:
                print(f"  |  {e['notes']}", end="")
            print()
    else:
        print(f"\n  ✅  Nothing needs water today.")

    if ok_soon:
        print(f"\n  ⏰  DUE TOMORROW")
        for e in ok_soon:
            print(f"  • {e['target']:<20}  (every {e['frequency_days']}d, last: {e['last_watered']})")

    if on_track:
        print(f"\n  ✓   On schedule (next water in 2+ days)")
        for e in on_track:
            days_left = abs(e["overdue_days"])
            next_date = (today + timedelta(days=days_left - 1)).strftime("%m/%d")
            print(f"  • {e['target']:<20}  next: {next_date} (in {days_left}d)")

    print(f"\n{'='*56}\n")


def log_cmd(garden, target, log_date, garden_file):
    """Log a watering event for a target."""
    schedules = get_schedules(garden)
    schedule = find_schedule(schedules, target)

    if not schedule:
        # Auto-create a minimal schedule
        schedule = {"target": target, "frequency_days": 2, "last_watered": None, "notes": ""}
        schedules.append(schedule)
        print(f"Created new schedule for '{target}' (default: every 2 days). "
              f"Use 'set' to configure frequency.")

    schedule["last_watered"] = log_date.strftime("%Y-%m-%d")
    save_garden(garden, garden_file)
    print(f"✓ Logged watering for '{target}' on {log_date.strftime('%Y-%m-%d')}")


def set_cmd(garden, target, frequency_days, notes, garden_file):
    """Set or update a watering schedule."""
    schedules = get_schedules(garden)
    schedule = find_schedule(schedules, target)

    if schedule:
        if frequency_days is not None:
            schedule["frequency_days"] = frequency_days
        if notes is not None:
            schedule["notes"] = notes
        print(f"✓ Updated schedule for '{target}'")
    else:
        schedule = {
            "target": target,
            "frequency_days": frequency_days if frequency_days is not None else 2,
            "last_watered": None,
            "notes": notes or "",
        }
        schedules.append(schedule)
        print(f"✓ Created schedule for '{target}'")

    save_garden(garden, garden_file)
    print(f"  Target:    {target}")
    print(f"  Frequency: every {schedule['frequency_days']} day(s)")
    if schedule.get("notes"):
        print(f"  Notes:     {schedule['notes']}")


def list_cmd(garden, today):
    """List all watering schedules."""
    schedules = get_schedules(garden)
    if not schedules:
        print("No watering schedules configured.")
        return

    print(f"\n{'─'*60}")
    print(f"  All Watering Schedules")
    print(f"{'─'*60}")
    for s in schedules:
        target = s.get("target", "unknown")
        freq = s.get("frequency_days", "?")
        last = s.get("last_watered", "never")
        notes = s.get("notes", "")
        overdue = days_overdue(last, int(freq) if str(freq).isdigit() else 2, today)

        if overdue >= 0:
            status = f"⚠️  {'DUE TODAY' if overdue == 0 else f'OVERDUE {overdue}d'}"
        else:
            next_d = (today + timedelta(days=-overdue - 1)).strftime("%m/%d")
            status = f"✓  next: {next_d}"

        print(f"\n  {target}")
        print(f"    Frequency: every {freq} day(s)  |  Last watered: {last}")
        print(f"    Status: {status}")
        if notes:
            print(f"    Notes: {notes}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Track and manage watering schedules.")
    # --data-dir as a global arg MUST be defined before subparsers to work correctly
    parser.add_argument("--data-dir", default=DATA_DIR,
                        help=f"Garden data directory (default: {DATA_DIR})")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Show what needs watering today")

    # list
    subparsers.add_parser("list", help="List all watering schedules")

    # log
    log_p = subparsers.add_parser("log", help="Log a watering event")
    log_p.add_argument("--target", required=True, help="Bed/container/row name (e.g. bed-A)")
    log_p.add_argument("--date", default=None,
                       help="Date watered (YYYY-MM-DD). Defaults to today.")

    # set
    set_p = subparsers.add_parser("set", help="Set or update a watering schedule")
    set_p.add_argument("--target", required=True, help="Bed/container/row name")
    set_p.add_argument("--days", type=int, help="Watering frequency in days")
    set_p.add_argument("--notes", help="Notes about watering this target")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Resolve paths
    data_dir = os.path.expanduser(args.data_dir)
    garden_file = os.path.join(data_dir, "garden.json")

    garden = load_garden(garden_file)
    if garden is None:
        if args.command in ("status", "list"):
            print("No garden data found. Initialize with add_plant.py or watering.py set.")
            sys.exit(0)
        # For log/set, create empty garden
        garden = {"config": {}, "plants": [], "watering_schedules": []}

    today = date.today()

    if args.command == "status":
        status_cmd(garden, today)

    elif args.command == "list":
        list_cmd(garden, today)

    elif args.command == "log":
        log_date = today
        if args.date:
            try:
                log_date = datetime.strptime(args.date, "%Y-%m-%d").date()
            except ValueError:
                print(f"Error: invalid date '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)
        log_cmd(garden, args.target, log_date, garden_file)

    elif args.command == "set":
        set_cmd(garden, args.target, args.days, args.notes, garden_file)


if __name__ == "__main__":
    main()
