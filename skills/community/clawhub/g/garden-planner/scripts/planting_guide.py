#!/usr/bin/env python3
"""
planting_guide.py - Recommend what to plant this week based on zone and current date.
Usage: planting_guide.py --zone 7
       planting_guide.py --zone 6 --date 2025-04-15
       planting_guide.py --zone 7 --json
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALENDAR_PATH = os.path.join(SKILL_DIR, "references", "planting-calendar.md")
ZONES_PATH = os.path.join(SKILL_DIR, "references", "zones.md")

VALID_ZONES = [str(z) for z in range(1, 12)]


def load_json_block(filepath, label=""):
    """Extract and parse the JSON code block from a markdown file."""
    try:
        with open(filepath) as f:
            content = f.read()
        match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise ValueError(f"No JSON block found in {filepath}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Reference file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error in {filepath}: {e}")


def load_references():
    plants = load_json_block(CALENDAR_PATH, "planting calendar")
    zones = load_json_block(ZONES_PATH, "zones")
    return plants, zones


def parse_month_day(mm_dd_str):
    """Parse MM-DD string into a (month, day) tuple. Returns None if null."""
    if mm_dd_str is None:
        return None
    try:
        parts = mm_dd_str.split("-")
        return int(parts[0]), int(parts[1])
    except Exception:
        return None


def days_until_future(target_md, ref_date):
    """Return days from ref_date until (month, day) in current or next year.
    Only returns positive values (future dates). Returns None if target_md is None."""
    if target_md is None:
        return None
    m, d = target_md
    target = date(ref_date.year, m, d)
    if target < ref_date:
        target = date(ref_date.year + 1, m, d)
    return (target - ref_date).days


def days_until_this_year(target_md, ref_date):
    """Return days from ref_date until (month, day) this year.
    Returns negative if the date has already passed."""
    if target_md is None:
        return None
    m, d = target_md
    target = date(ref_date.year, m, d)
    return (target - ref_date).days


def days_since(target_md, ref_date):
    """Return days since (month, day) this year, or None."""
    if target_md is None:
        return None
    m, d = target_md
    target = date(ref_date.year, m, d)
    if target > ref_date:
        target = date(ref_date.year - 1, m, d)
    return (ref_date - target).days


def classify_plant(plant_name, plant_data, zone_str, today, last_frost_md, first_frost_md):
    """
    Returns: ("plant_now" | "start_indoors" | "coming_soon" | "too_late" | "not_in_zone", reason)
    """
    zone = int(zone_str) if zone_str.isdigit() else 7
    zones_min = plant_data.get("zones_min", 1)
    zones_max = plant_data.get("zones_max", 11)

    if not (zones_min <= zone <= zones_max):
        return "not_in_zone", f"Zone {zone} outside range {zones_min}–{zones_max}"

    frost_sensitive = plant_data.get("frost_sensitive", True)
    cool_season = plant_data.get("cool_season", False)

    days_min = plant_data.get("days_min", 60)
    days_max = plant_data.get("days_max", 90)

    # last_frost_days_this_year: negative means it already passed this year
    last_frost_days_this_year = days_until_this_year(last_frost_md, today) if last_frost_md else None
    # first_frost_days: days until first fall frost (always future)
    first_frost_days = days_until_future(first_frost_md, today) if first_frost_md else None
    days_since_last_frost_val = days_since(last_frost_md, today) if last_frost_md else None

    # Determine if we're before or after last spring frost
    last_frost_in_future = last_frost_days_this_year is not None and last_frost_days_this_year > 0

    # Check if growing season is long enough (only relevant if we're past last frost)
    if not last_frost_in_future and first_frost_days is not None and days_min > first_frost_days:
        return "too_late", f"Only {first_frost_days}d until first frost; needs {days_min}+ days"

    if frost_sensitive:
        if last_frost_md is None:
            # Zone 10/11 — no frost
            return "plant_now", "Frost-free zone; plant anytime"

        if last_frost_in_future:
            days_left = last_frost_days_this_year
            if days_left > 14:
                return "start_indoors", f"Start indoors now; transplant outdoors in {days_left}d (after last frost)"
            else:
                return "coming_soon", f"Transplant outdoors in {days_left}d (after last frost)"
        else:
            # Past last frost — safe to plant
            if days_since_last_frost_val is not None and days_since_last_frost_val > 90:
                return "too_late", f"Season getting late ({days_since_last_frost_val}d past last frost)"
            return "plant_now", f"Past last frost; safe to plant outdoors now"
    else:
        # Cool-season crop
        if last_frost_in_future:
            days_left = last_frost_days_this_year
            # Before last frost — spring planting window for cool-season
            if days_left <= 42:
                return "plant_now", f"Cool-season crop; plant now ({days_left}d before last frost)"
            else:
                start_in = days_left - 42
                return "coming_soon", f"Cool-season crop; start in {start_in}d ({days_left}d before last frost)"
        else:
            # After last frost
            # Cool-season crops can still be planted in spring if not too hot yet
            # Allow spring planting up to ~30 days after last frost
            days_past_last_frost = days_since_last_frost_val or 0
            if days_past_last_frost <= 30:
                return "plant_now", f"Cool-season crop; still within spring planting window ({days_past_last_frost}d past last frost)"

            # Otherwise check fall planting window
            if first_frost_days is not None:
                fall_window_open = first_frost_days - days_max
                if fall_window_open >= 14:
                    return "plant_now", f"Fall planting window open; harvest before first frost ({first_frost_days}d away)"
                elif fall_window_open >= 0:
                    return "coming_soon", f"Fall planting window opens in {fall_window_open}d"
                else:
                    return "too_late", f"Too late for spring; too early for fall (first frost in {first_frost_days}d)"
            return "too_late", "Spring window closed; check back for fall planting"


def format_guide(results, zone, today):
    plant_now = [(n, r, cat) for n, r, cat in results if cat == "plant_now"]
    start_indoors = [(n, r, cat) for n, r, cat in results if cat == "start_indoors"]
    coming_soon = [(n, r, cat) for n, r, cat in results if cat == "coming_soon"]
    too_late = [(n, r, cat) for n, r, cat in results if cat == "too_late"]

    print(f"\n{'='*60}")
    print(f"🌿  Planting Guide — Zone {zone} — {today.strftime('%B %d, %Y')}")
    print(f"{'='*60}")

    if plant_now:
        print(f"\n  ✅  PLANT NOW ({len(plant_now)} options)")
        print(f"  {'─'*50}")
        for name, reason, _ in sorted(plant_now, key=lambda x: x[0]):
            print(f"  • {name.title():<22} — {reason}")

    if start_indoors:
        print(f"\n  🏠  START INDOORS ({len(start_indoors)} options)")
        print(f"  {'─'*50}")
        for name, reason, _ in sorted(start_indoors, key=lambda x: x[0]):
            print(f"  • {name.title():<22} — {reason}")

    if coming_soon:
        print(f"\n  ⏰  COMING SOON ({len(coming_soon)} options)")
        print(f"  {'─'*50}")
        for name, reason, _ in sorted(coming_soon, key=lambda x: x[0]):
            print(f"  • {name.title():<22} — {reason}")

    if too_late:
        print(f"\n  ❌  TOO LATE THIS SEASON ({len(too_late)} plants)")
        print(f"  {'─'*50}")
        for name, reason, _ in sorted(too_late, key=lambda x: x[0]):
            print(f"  • {name.title():<22} — {reason}")

    print(f"\n{'='*60}")
    print(f"Tip: Results based on average zone frost dates. Check local forecasts!\n")


def main():
    parser = argparse.ArgumentParser(description="Get planting recommendations for your zone and date.")
    parser.add_argument("--zone", required=True, help="USDA hardiness zone (e.g. 7)")
    parser.add_argument("--date", default=None,
                        help="Date to use for recommendations (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--type", choices=["vegetable", "herb", "flower", "fruit", "all"],
                        default="all", help="Filter by plant type")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output JSON instead of human-readable")
    parser.add_argument("--data-dir", default=os.path.expanduser("~/.openclaw/workspace/garden"),
                        help="Garden data dir (for reading config zone)")
    args = parser.parse_args()

    zone_str = args.zone.strip()
    if zone_str not in VALID_ZONES:
        print(f"Error: zone must be 1–11 (got '{zone_str}')", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    if args.date:
        try:
            today = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: invalid date '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)

    try:
        plants_db, zones_db = load_references()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading references: {e}", file=sys.stderr)
        sys.exit(1)

    zone_data = zones_db.get(zone_str, {})
    last_frost_md = parse_month_day(zone_data.get("last_frost"))
    first_frost_md = parse_month_day(zone_data.get("first_frost"))

    if not zone_data:
        print(f"Warning: Zone {zone_str} not found in zones reference. Using defaults.", file=sys.stderr)

    results = []
    for plant_name, plant_data in plants_db.items():
        if args.type != "all" and plant_data.get("type") != args.type:
            continue
        cat, reason = classify_plant(plant_name, plant_data, zone_str, today, last_frost_md, first_frost_md)
        if cat != "not_in_zone":
            results.append((plant_name, reason, cat))

    if args.json_output:
        output = {
            "zone": zone_str,
            "date": today.isoformat(),
            "last_frost": zone_data.get("last_frost"),
            "first_frost": zone_data.get("first_frost"),
            "recommendations": [
                {"plant": n, "category": cat, "reason": r}
                for n, r, cat in sorted(results, key=lambda x: x[0])
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        format_guide(results, zone_str, today)


if __name__ == "__main__":
    main()
