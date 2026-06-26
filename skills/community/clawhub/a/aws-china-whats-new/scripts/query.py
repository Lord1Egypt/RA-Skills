#!/usr/bin/env python3
"""Query AWS China What's New data."""

import argparse
import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(SKILL_DIR, "data", "whats_new.json")
FETCH_SCRIPT = os.path.join(SCRIPT_DIR, "fetch_data.py")

# TTL in seconds (24 hours)
DATA_TTL = 24 * 60 * 60

# Region detection keywords
BEIJING_KEYWORDS = ["Beijing", "cn-north-1", "Sinnet", "\u5317\u4eac"]
NINGXIA_KEYWORDS = ["Ningxia", "cn-northwest-1", "NWCD", "\u5b81\u590f"]
BOTH_KEYWORDS = ["China Regions", "\u4e2d\u56fd\u533a\u57df"]


def ensure_data():
    """Ensure data file exists and is fresh. Auto-fetch if needed."""
    need_full = False
    need_incremental = False

    if not os.path.exists(DATA_FILE):
        need_full = True
    else:
        age = time.time() - os.path.getmtime(DATA_FILE)
        if age > DATA_TTL:
            need_incremental = True

    if need_full:
        print("Data file not found, fetching all years...", file=sys.stderr)
        subprocess.run([sys.executable, FETCH_SCRIPT], check=True,
                       stdout=sys.stderr, stderr=sys.stderr)
    elif need_incremental:
        print("Data stale (>24h), running incremental update...", file=sys.stderr)
        subprocess.run([sys.executable, FETCH_SCRIPT, "--incremental"], check=True,
                       stdout=sys.stderr, stderr=sys.stderr)


def load_data():
    """Load the data file, auto-fetching if needed."""
    ensure_data()
    if not os.path.exists(DATA_FILE):
        print(json.dumps({"error": "Failed to fetch data."}))
        sys.exit(1)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_region(item):
    """Detect which AWS China region(s) an item relates to."""
    text = item.get("title", "") + " " + item.get("body", "")
    regions = set()

    for kw in BOTH_KEYWORDS:
        if kw.lower() in text.lower():
            regions.add("beijing")
            regions.add("ningxia")

    for kw in BEIJING_KEYWORDS:
        if kw.lower() in text.lower():
            regions.add("beijing")

    for kw in NINGXIA_KEYWORDS:
        if kw.lower() in text.lower():
            regions.add("ningxia")

    if not regions:
        return ["unknown"]
    return sorted(regions)


def matches_service(item, service):
    """Check if an item matches a service name (case-insensitive fuzzy match)."""
    text = (item.get("title", "") + " " + item.get("body", "")).lower()
    # Support multi-word service names and partial matches
    terms = service.lower().split()
    return all(term in text for term in terms)


def filter_items(items, args):
    """Apply filters to items."""
    results = items

    if args.service:
        results = [it for it in results if matches_service(it, args.service)]

    if args.year:
        results = [it for it in results if it.get("year") == args.year]

    if args.after:
        results = [it for it in results if it.get("date", "") >= args.after]

    if args.before:
        results = [it for it in results if it.get("date", "") <= args.before]

    if args.region and args.region != "all":
        region_map = {"beijing": "beijing", "ningxia": "ningxia"}
        target = region_map.get(args.region.lower())
        if target:
            results = [it for it in results if target in detect_region(it)]

    if args.latest:
        results = results[:1]
    elif args.limit:
        results = results[:args.limit]

    return results


def format_output(items):
    """Format items for output, adding detected regions and stripping HTML from body."""
    output = []
    for item in items:
        clean = {
            "title": item.get("title", ""),
            "date": item.get("date", ""),
            "link": item.get("link", ""),
            "regions": detect_region(item),
            "year": item.get("year"),
            "body_preview": strip_html(item.get("body", ""))[:300],
        }
        output.append(clean)
    return output


def strip_html(html_text):
    """Remove HTML tags from text."""
    return re.sub(r"<[^>]+>", "", html_text).strip()


def main():
    parser = argparse.ArgumentParser(description="Query AWS China What's New data")
    parser.add_argument("--service", type=str, help="Filter by service name (fuzzy match)")
    parser.add_argument(
        "--region",
        type=str,
        choices=["beijing", "ningxia", "all"],
        help="Filter by region",
    )
    parser.add_argument("--year", type=int, help="Filter by year")
    parser.add_argument("--after", type=str, help="Filter items after date (YYYY-MM-DD)")
    parser.add_argument("--before", type=str, help="Filter items before date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, help="Limit number of results")
    parser.add_argument("--latest", action="store_true", help="Show only the latest item")
    args = parser.parse_args()

    items = load_data()
    results = filter_items(items, args)
    output = format_output(results)

    print(json.dumps({"count": len(output), "items": output}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
