#!/usr/bin/env python3
"""Fetch AWS China What's New data from amazonaws.cn and save to JSON."""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from html.parser import HTMLParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(SKILL_DIR, "data", "whats_new.json")

BASE_URL = "https://www.amazonaws.cn/en/new/{year}/"
YEARS = range(2016, 2027)

USER_AGENT = "Mozilla/5.0 (compatible; AWSChinaWhatsNew/1.0)"


def fetch_page(url):
    """Fetch a URL and return the HTML content."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return None


def extract_items_from_html(html):
    """Extract What's New items from embedded JSON in the HTML page.

    The page contains multiple <script type="application/json"> blocks.
    The one with the items has entries containing 'itemBody' and 'itemTitle' fields.
    """
    pattern = r'<script\s+type="application/json"[^>]*>(.*?)</script>'
    scripts = re.findall(pattern, html, re.DOTALL)

    for script_content in scripts:
        try:
            data = json.loads(script_content)
        except (json.JSONDecodeError, ValueError):
            continue

        items = data.get("data", {}).get("items", [])
        if not items:
            continue

        # The right block has items with 'itemTitle' and 'itemBody' in fields
        first_fields = items[0].get("fields", {})
        if "itemTitle" in first_fields and "itemBody" in first_fields:
            return items

    return []


def parse_items(raw_items, year):
    """Parse raw JSON items into clean dicts."""
    parsed = []
    for item in raw_items:
        fields = item.get("fields", {})
        title = fields.get("itemTitle")
        if not title:
            continue  # skip metadata entries without a title

        body = fields.get("itemBody", "")
        date_str = fields.get("itemMetadataDate", "")
        link = fields.get("itemLink", "")

        # Normalize date to YYYY-MM-DD
        date_normalized = ""
        if date_str:
            try:
                # Format: 2026-01-16T00:00:00.000+08:00
                date_normalized = date_str[:10]
            except Exception:
                date_normalized = date_str

        parsed.append({
            "title": title.strip(),
            "body": body.strip(),
            "date": date_normalized,
            "link": link.strip(),
            "year": year,
        })

    return parsed


def load_existing_data():
    """Load existing data file if it exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(items):
    """Save items to the data file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(items)} items to {DATA_FILE}")


def fetch_year(year):
    """Fetch and parse items for a single year."""
    url = BASE_URL.format(year=year)
    print(f"Fetching {url} ...")
    html = fetch_page(url)
    if not html:
        return []

    raw_items = extract_items_from_html(html)
    if not raw_items:
        print(f"  No items found for {year}", file=sys.stderr)
        return []

    items = parse_items(raw_items, year)
    print(f"  Found {len(items)} items for {year}")
    return items


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch AWS China What's New data")
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only fetch current year and merge with existing data",
    )
    parser.add_argument(
        "--year",
        type=int,
        nargs="+",
        help="Fetch specific year(s) only",
    )
    args = parser.parse_args()

    if args.incremental:
        current_year = datetime.now().year
        years_to_fetch = [current_year]
        existing = load_existing_data()
        # Remove old entries for the current year
        existing = [item for item in existing if item.get("year") != current_year]
    elif args.year:
        years_to_fetch = args.year
        existing = load_existing_data()
        # Remove old entries for the specified years
        existing = [item for item in existing if item.get("year") not in years_to_fetch]
    else:
        years_to_fetch = list(YEARS)
        existing = []

    all_items = list(existing)

    for year in years_to_fetch:
        items = fetch_year(year)
        all_items.extend(items)

    # Sort by date descending
    all_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    save_data(all_items)
    print(f"Total: {len(all_items)} items")


if __name__ == "__main__":
    main()
