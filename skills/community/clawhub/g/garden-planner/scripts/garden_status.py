#!/usr/bin/env python3
"""
garden_status.py - Show current garden status.
Displays all active plants with growth stage, days since planting, harvest estimate, and next action.
Usage: garden_status.py [--all] [--json] [--data-dir PATH]
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


def growth_stage(days_since_planting, days_to_harvest):
    """Determine growth stage based on progress through growing cycle."""
    if days_to_harvest is None or days_to_harvest == 0:
        return "unknown"
    progress = days_since_planting / days_to_harvest

    if progress < 0.15:
        return "seedling"
    elif progress < 0.45:
        return "vegetative"
    elif progress < 0.70:
        return "flowering"
    elif progress < 0.90:
        return "fruiting"
    else:
        return "ready"


STAGE_ICONS = {
    "seedling":   "🌱",
    "vegetative": "🌿",
    "flowering":  "🌸",
    "fruiting":   "🍅",
    "ready":      "✅",
    "unknown":    "❓",
}

STAGE_ACTIONS = {
    "seedling":   "Water gently; keep moist; protect from strong wind",
    "vegetative": "Regular watering; fertilize if needed; watch for pests",
    "flowering":  "Consistent watering; avoid disturbing flowers; stake if tall",
    "fruiting":   "Deep watering; check for pests; support heavy fruit",
    "ready":      "HARVEST NOW — don't wait or quality declines",
    "unknown":    "Monitor plant health; check planting calendar for guidance",
}


def format_plant(plant, today):
    planted_date = datetime.strptime(plant["planted_date"], "%Y-%m-%d").date()
    days_since = (today - planted_date).days

    days_to_harvest = None
    if plant.get("days_to_harvest_min") and plant.get("days_to_harvest_max"):
        days_to_harvest = (plant["days_to_harvest_min"] + plant["days_to_harvest_max"]) // 2

    stage = growth_stage(days_since, days_to_harvest)
    icon = STAGE_ICONS[stage]
    action = STAGE_ACTIONS[stage]

    days_until_harvest = None
    if plant.get("expected_harvest"):
        harvest_date = datetime.strptime(plant["expected_harvest"], "%Y-%m-%d").date()
        days_until_harvest = (harvest_date - today).days

    return {
        "id": plant["id"],
        "name": plant["name"],
        "type": plant["type"],
        "location": plant["location"],
        "planted_date": plant["planted_date"],
        "days_since_planting": days_since,
        "growth_stage": stage,
        "stage_icon": icon,
        "expected_harvest": plant.get("expected_harvest"),
        "days_until_harvest": days_until_harvest,
        "next_action": action,
        "notes": plant.get("notes", ""),
    }


def print_status(plants_info, config, today):
    zone = config.get("zone", "unknown")
    location = config.get("location_name", "Your Garden")

    print(f"\n{'='*60}")
    print(f"🌻  Garden Status — {today.strftime('%B %d, %Y')}")
    print(f"    {location} | Zone {zone}")
    print(f"{'='*60}")

    if not plants_info:
        print("\nNo active plants. Add some with: add_plant.py --name ... --type ...")
        return

    # Group by stage
    ready = [p for p in plants_info if p["growth_stage"] == "ready"]
    active = [p for p in plants_info if p["growth_stage"] != "ready"]

    if ready:
        print(f"\n{'─'*60}")
        print(f"  🚨  READY TO HARVEST ({len(ready)} plant{'s' if len(ready) > 1 else ''})")
        print(f"{'─'*60}")
        for p in ready:
            print(f"\n  {p['stage_icon']} {p['name']} [{p['type']}]")
            print(f"     Location: {p['location']}")
            print(f"     Planted:  {p['planted_date']} ({p['days_since_planting']} days ago)")
            print(f"     ⚡ {p['next_action']}")

    print(f"\n{'─'*60}")
    print(f"  🌱  Active Plants ({len(active)})")
    print(f"{'─'*60}")

    for p in active:
        stage_label = p["growth_stage"].upper()
        print(f"\n  {p['stage_icon']} {p['name']} [{p['type']}]  — {stage_label}")
        print(f"     Location: {p['location']}")
        print(f"     Planted:  {p['planted_date']} ({p['days_since_planting']} days ago)")

        if p["expected_harvest"]:
            if p["days_until_harvest"] is not None:
                if p["days_until_harvest"] > 0:
                    print(f"     Harvest:  ~{p['expected_harvest']} (in {p['days_until_harvest']} days)")
                elif p["days_until_harvest"] == 0:
                    print(f"     Harvest:  TODAY is harvest day!")
                else:
                    print(f"     Harvest:  {p['expected_harvest']} ({abs(p['days_until_harvest'])} days overdue)")
            else:
                print(f"     Harvest:  {p['expected_harvest']}")
        else:
            print(f"     Harvest:  Unknown")

        print(f"     → {p['next_action']}")
        if p["notes"]:
            print(f"     Notes:    {p['notes']}")

    print(f"\n{'='*60}")
    print(f"Total active: {len(plants_info)} plants\n")


def main():
    parser = argparse.ArgumentParser(description="Show garden status for all active plants.")
    parser.add_argument("--all", action="store_true", help="Include inactive/harvested plants")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output as JSON instead of human-readable")
    parser.add_argument("--data-dir", default=DATA_DIR,
                        help=f"Garden data directory (default: {DATA_DIR})")
    args = parser.parse_args()

    data_dir = os.path.expanduser(args.data_dir)
    garden_file = os.path.join(data_dir, "garden.json")

    garden = load_garden(garden_file)
    if garden is None:
        print("No garden data found. Start with: add_plant.py --name ... --type ...")
        print(f"Expected location: {garden_file}")
        sys.exit(0)

    today = date.today()
    all_plants = garden.get("plants", [])

    if args.all:
        plants_to_show = all_plants
    else:
        plants_to_show = [p for p in all_plants if p.get("active", True)]

    plants_info = [format_plant(p, today) for p in plants_to_show]

    if args.json_output:
        print(json.dumps({"date": today.isoformat(), "plants": plants_info}, indent=2))
    else:
        config = garden.get("config", {})
        print_status(plants_info, config, today)


if __name__ == "__main__":
    main()
