#!/usr/bin/env python3
"""
add_plant.py - Add a plant to the garden log.
Usage: add_plant.py --name "Tomato" --type vegetable [--planted-date 2025-05-10] [--location bed-A] [--notes "..."]
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALENDAR_PATH = os.path.join(SKILL_DIR, "references", "planting-calendar.md")
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/garden")
GARDEN_FILE = os.path.join(DATA_DIR, "garden.json")

VALID_TYPES = ("vegetable", "herb", "flower", "fruit")


def load_harvest_data():
    """Extract JSON data block from planting-calendar.md."""
    try:
        with open(CALENDAR_PATH) as f:
            content = f.read()
        match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print(f"Warning: could not load planting calendar: {e}", file=sys.stderr)
    return {}


def find_plant_data(name, harvest_db):
    """Fuzzy match plant name against the database."""
    name_lower = name.lower().strip()
    # Exact match first
    if name_lower in harvest_db:
        return harvest_db[name_lower], name_lower
    # Partial match
    for key in harvest_db:
        if key in name_lower or name_lower in key:
            return harvest_db[key], key
    return None, None


def calculate_harvest(planted_date_str, days_min, days_max):
    """Return expected harvest date string (midpoint of range)."""
    planted = datetime.strptime(planted_date_str, "%Y-%m-%d").date()
    mid_days = (days_min + days_max) // 2
    harvest = planted + timedelta(days=mid_days)
    return harvest.strftime("%Y-%m-%d")


def load_garden(garden_file):
    if os.path.exists(garden_file):
        with open(garden_file) as f:
            return json.load(f)
    return {"config": {}, "plants": [], "watering_schedules": []}


def save_garden(data, garden_file):
    os.makedirs(os.path.dirname(garden_file), exist_ok=True)
    with open(garden_file, "w") as f:
        json.dump(data, f, indent=2)


def next_plant_id(plants):
    if not plants:
        return "plant_001"
    existing = []
    for p in plants:
        m = re.match(r"plant_(\d+)", p.get("id", ""))
        if m:
            existing.append(int(m.group(1)))
    return f"plant_{(max(existing) + 1):03d}" if existing else "plant_001"


def main():
    parser = argparse.ArgumentParser(description="Add a plant to the garden log.")
    parser.add_argument("--name", required=True, help="Plant name (e.g. 'Cherokee Purple Tomato')")
    parser.add_argument("--type", required=True, choices=VALID_TYPES,
                        help="Plant type: vegetable, herb, flower, or fruit")
    parser.add_argument("--planted-date", default=None,
                        help="Date planted (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--location", default="unspecified",
                        help="Where it's planted (e.g. bed-A, container-1, row-2)")
    parser.add_argument("--notes", default="", help="Optional notes about this plant")
    parser.add_argument("--days-to-harvest", default=None, type=int,
                        help="Override days to harvest (overrides calendar lookup)")
    parser.add_argument("--data-dir", default=DATA_DIR,
                        help=f"Garden data directory (default: {DATA_DIR})")

    args = parser.parse_args()

    # Handle data dir override
    data_dir = os.path.expanduser(args.data_dir)
    garden_file = os.path.join(data_dir, "garden.json")

    # Validate and set planted date
    planted_date = args.planted_date or date.today().strftime("%Y-%m-%d")
    try:
        datetime.strptime(planted_date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: invalid date format '{planted_date}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    # Look up harvest data
    harvest_db = load_harvest_data()
    plant_data, matched_key = find_plant_data(args.name, harvest_db)

    days_min = days_max = None
    expected_harvest = None

    if args.days_to_harvest:
        days_min = days_max = args.days_to_harvest
        expected_harvest = calculate_harvest(planted_date, days_min, days_max)
        print(f"Using manual days-to-harvest: {args.days_to_harvest} days")
    elif plant_data:
        days_min = plant_data["days_min"]
        days_max = plant_data["days_max"]
        expected_harvest = calculate_harvest(planted_date, days_min, days_max)
        print(f"Matched '{matched_key}' in planting calendar: {days_min}–{days_max} days to harvest")
    else:
        print(f"Warning: '{args.name}' not found in planting calendar. "
              f"Harvest date unknown. Use --days-to-harvest to set manually.", file=sys.stderr)

    # Load existing garden
    garden = load_garden(garden_file)

    # Build plant entry
    plant_id = next_plant_id(garden.get("plants", []))
    entry = {
        "id": plant_id,
        "name": args.name,
        "type": args.type,
        "planted_date": planted_date,
        "location": args.location,
        "notes": args.notes,
        "days_to_harvest_min": days_min,
        "days_to_harvest_max": days_max,
        "expected_harvest": expected_harvest,
        "active": True,
    }

    garden.setdefault("plants", []).append(entry)
    save_garden(garden, garden_file)

    print(f"\n✓ Added: {args.name} [{args.type}]")
    print(f"  ID:        {plant_id}")
    print(f"  Location:  {args.location}")
    print(f"  Planted:   {planted_date}")
    if expected_harvest:
        print(f"  Expected harvest: {expected_harvest} ({days_min}–{days_max} days)")
    else:
        print(f"  Expected harvest: Unknown")
    if args.notes:
        print(f"  Notes:     {args.notes}")
    print(f"\nSaved to: {garden_file}")


if __name__ == "__main__":
    main()
