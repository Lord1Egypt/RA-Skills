#!/usr/bin/env python3
"""
query_coin_truck.py — Query the Hong Kong Coin Cart (收銀車) schedule and location database.

Usage:
    python query_coin_truck.py --date today
    python query_coin_truck.py --date 2026-03-20
    python query_coin_truck.py --district 沙田區
    python query_coin_truck.py --truck 收銀車1號
    python query_coin_truck.py --date today --district 元朗區
    python query_coin_truck.py --list-districts
    python query_coin_truck.py --upcoming --days 7
"""

import json
import argparse
import sys
import os
from datetime import date, datetime, timedelta

# Resolve the JSON data file path relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "references", "coin_collection_truck_hk.json")

YEAR = 2026  # The schedule year; update if data is refreshed for a new year


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date_field(date_str: str, year: int = YEAR) -> date | None:
    """Parse a date string like '1月5日', '2026-01-05', '1/5/2026', etc."""
    if not date_str or not date_str.strip():
        return None
    date_str = date_str.strip()

    # ISO format: 2026-01-05
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass

    # US slash format: 1/5/2026 or 1/05/2026
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").date()
    except ValueError:
        pass

    # Chinese format: 1月5日
    try:
        import re
        m = re.match(r"(\d+)月(\d+)日", date_str)
        if m:
            month, day = int(m.group(1)), int(m.group(2))
            return date(year, month, day)
    except Exception:
        pass

    return None


def parse_suspended_dates(suspended_str: str, year: int = YEAR) -> list[date]:
    """Parse the 暫停日期 field which may contain multiple comma-separated dates."""
    if not suspended_str or not suspended_str.strip():
        return []
    parts = [p.strip() for p in suspended_str.split(",")]
    result = []
    for p in parts:
        d = parse_date_field(p, year)
        if d:
            result.append(d)
    return result


def is_active_on(record: dict, query_date: date) -> bool:
    """Return True if the coin truck is scheduled (and not suspended) on query_date."""
    start = parse_date_field(record.get("開始日期", ""))
    end = parse_date_field(record.get("結束日期", ""))
    if not start or not end:
        return False
    if not (start <= query_date <= end):
        return False
    suspended = parse_suspended_dates(record.get("暫停日期", ""))
    if query_date in suspended:
        return False
    return True


def format_record(record: dict, query_date: date | None = None) -> str:
    """Format a single record for human-readable output."""
    truck = record.get("收銀車", "")
    district = record.get("地區", "")
    address_zh = record.get("地址", "")
    address_en = record.get("English Address", "")
    start = record.get("開始日期", "")
    end = record.get("結束日期", "")
    note_zh = record.get("備注", "")
    note_en = record.get("備注(英文)", "")
    lat = record.get("latitude 緯度", "")
    lon = record.get("longitude 經度", "")

    lines = [
        f"  🚌 {truck} — {district}",
        f"     地址: {address_zh}",
        f"     Address: {address_en}",
        f"     Schedule: {start} ~ {end}",
    ]
    if note_zh:
        lines.append(f"     ⚠️  {note_zh}")
    if note_en:
        lines.append(f"     ⚠️  {note_en}")
    if lat and lon:
        lines.append(f"     📍 Coordinates: {lat}, {lon}")
        lines.append(f"     🗺️  Map: https://maps.google.com/?q={lat},{lon}")
    return "\n".join(lines)


def query_by_date(data: list, query_date: date) -> list[dict]:
    return [r for r in data if is_active_on(r, query_date)]


def query_by_district(data: list, district: str) -> list[dict]:
    district_lower = district.lower()
    return [
        r for r in data
        if district_lower in r.get("地區", "").lower()
        or district_lower in r.get("English Address", "").lower()
        or district_lower in r.get("地址", "").lower()
    ]


def query_by_truck(data: list, truck_name: str) -> list[dict]:
    return [r for r in data if truck_name in r.get("收銀車", "")]


def query_upcoming(data: list, from_date: date, days: int) -> list[dict]:
    """Return all records active within the next `days` days from from_date."""
    results = []
    seen = set()
    for offset in range(days + 1):
        d = from_date + timedelta(days=offset)
        for r in query_by_date(data, d):
            key = (r.get("收銀車"), r.get("開始日期"), r.get("地址"))
            if key not in seen:
                seen.add(key)
                results.append((d, r))
    return results


def list_districts(data: list) -> list[str]:
    return sorted(set(r.get("地區", "") for r in data if r.get("地區")))


def resolve_date(date_str: str) -> date:
    """Resolve a date string to a date object, supporting 'today', 'tomorrow', ISO, and Chinese formats."""
    if date_str.lower() == "today":
        return date.today()
    if date_str.lower() == "tomorrow":
        return date.today() + timedelta(days=1)
    # Try ISO
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass
    # Try Chinese format
    d = parse_date_field(date_str)
    if d:
        return d
    raise ValueError(f"Cannot parse date: '{date_str}'. Use 'today', 'tomorrow', or YYYY-MM-DD format.")


def main():
    parser = argparse.ArgumentParser(
        description="Query Hong Kong Coin Cart (收銀車) schedule and location."
    )
    parser.add_argument("--date", help="Query by date: 'today', 'tomorrow', or YYYY-MM-DD")
    parser.add_argument("--district", help="Filter by district name (Chinese or English partial match)")
    parser.add_argument("--truck", help="Filter by truck name, e.g. '收銀車1號' or '收銀車2號'")
    parser.add_argument("--upcoming", action="store_true", help="Show upcoming schedules")
    parser.add_argument("--days", type=int, default=7, help="Number of days ahead for --upcoming (default: 7)")
    parser.add_argument("--list-districts", action="store_true", help="List all districts in the database")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")

    args = parser.parse_args()
    data = load_data()

    # --list-districts
    if args.list_districts:
        districts = list_districts(data)
        print("Available districts (地區):")
        for d in districts:
            print(f"  - {d}")
        return

    # --upcoming
    if args.upcoming:
        from_date = resolve_date(args.date) if args.date else date.today()
        results = query_upcoming(data, from_date, args.days)
        if not results:
            print(f"No coin truck schedules found in the next {args.days} days from {from_date}.")
            return
        print(f"Upcoming Coin Cart (收銀車) schedules from {from_date} (+{args.days} days):\n")
        current_date = None
        for d, r in results:
            if d != current_date:
                current_date = d
                print(f"📅 {d.strftime('%Y-%m-%d (%A)')}")
            print(format_record(r))
            print()
        return

    # Start with full dataset, apply filters
    results = data

    if args.date:
        query_date = resolve_date(args.date)
        results = query_by_date(results, query_date)
        date_label = query_date.strftime("%Y-%m-%d (%A)")
    else:
        query_date = None
        date_label = None

    if args.district:
        results = query_by_district(results, args.district)

    if args.truck:
        results = query_by_truck(results, args.truck)

    if not results:
        filters = []
        if date_label:
            filters.append(f"date={date_label}")
        if args.district:
            filters.append(f"district={args.district}")
        if args.truck:
            filters.append(f"truck={args.truck}")
        print(f"No coin truck schedules found for: {', '.join(filters) if filters else 'given criteria'}.")
        return

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    # Formatted output
    if date_label:
        print(f"Coin Cart (收銀車) locations on {date_label}:\n")
    else:
        print(f"Coin Cart (收銀車) schedules matching your query:\n")

    for r in results:
        print(format_record(r))
        print()

    print(f"Total: {len(results)} result(s) found.")


if __name__ == "__main__":
    main()
