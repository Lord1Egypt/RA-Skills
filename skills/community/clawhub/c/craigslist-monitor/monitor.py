#!/usr/bin/env python3
"""
Craigslist Monitor — Gracie AI Receptionist Lead Scraper
Scrapes Craigslist NY services for small businesses in Staten Island, Brooklyn, Bronx.

Usage:
  python3 monitor.py                    # scan all categories
  python3 monitor.py --save             # scan + save to MASTER_LEAD_LIST.md
  python3 monitor.py --type plumber     # single category
  python3 monitor.py --enrich           # also fetch individual ads for phones
"""

import sys
import re
import argparse
from datetime import datetime
from pathlib import Path

# ── Venv bootstrap ────────────────────────────────────────────────────────────
VENV_SITE = '/Users/wlc-studio/StudioBrain/00_SYSTEM/skills/scrapling/.venv/lib/python3.14/site-packages'
if VENV_SITE not in sys.path:
    sys.path.insert(0, VENV_SITE)

from scrapling.fetchers import Fetcher

# ── Config ────────────────────────────────────────────────────────────────────
MASTER_LEAD_LIST = Path.home() / "StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md"

SEARCH_QUERIES = {
    "plumber":     "https://newyork.craigslist.org/search/sss?query=plumber&nearby=1",
    "hvac":        "https://newyork.craigslist.org/search/sss?query=hvac&nearby=1",
    "auto repair": "https://newyork.craigslist.org/search/sss?query=auto+repair&nearby=1",
    "dental":      "https://newyork.craigslist.org/search/sss?query=dental&nearby=1",
    "contractor":  "https://newyork.craigslist.org/search/sss?query=contractor&nearby=1",
}

TARGET_AREAS = [
    "staten island", "brooklyn", "bronx",
    "crown heights", "bedford", "bushwick", "flatbush", "bensonhurst",
    "bay ridge", "red hook", "greenpoint", "williamsburg", "fort greene",
    "park slope", "sunset park", "canarsie", "coney island", "brighton beach",
    "morris park", "riverdale", "fordham", "tremont", "mott haven",
    # Zip codes — Staten Island
    "10301","10302","10303","10304","10305","10306","10307","10308","10309","10310",
    "10311","10312","10314",
    # Brooklyn zips
    "11201","11203","11204","11205","11206","11207","11208","11209","11210","11211",
    "11212","11213","11214","11215","11216","11217","11218","11219","11220","11221",
    "11222","11223","11224","11225","11226","11228","11229","11230","11231","11232",
    "11233","11234","11235","11236","11237","11238","11239",
    # Bronx zips
    "10451","10452","10453","10454","10455","10456","10457","10458","10459","10460",
    "10461","10462","10463","10464","10465","10466","10467","10468","10469","10470",
    "10471","10472","10473","10474","10475",
]

PHONE_RE = re.compile(r'(\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4})')

# ── Helpers ───────────────────────────────────────────────────────────────────

def in_target_area(text: str) -> bool:
    lower = text.lower()
    return any(area in lower for area in TARGET_AREAS)


def extract_phone(text: str) -> str:
    m = PHONE_RE.search(text)
    return m.group(1) if m else ""


def fetch_page(url: str):
    try:
        return Fetcher.get(url, stealthy_headers=True, impersonate='chrome', timeout=30)
    except Exception as e:
        print(f"  [fetch error] {e}", file=sys.stderr)
        return None


# ── Craigslist parser ─────────────────────────────────────────────────────────

def parse_listings(page, business_type: str) -> list[dict]:
    """
    Parse Craigslist search results using CSS selectors.
    Structure per result:
      <li class="cl-static-search-result">
        <a href="...url...">
          <div class="title">Ad Title</div>
          <div class="details">
            <div class="location">location text</div>
          </div>
        </a>
      </li>
    """
    leads = []
    results = page.css('.cl-static-search-result')

    for item in results:
        # Title
        title_el = item.css('.title')
        title = title_el[0].get_all_text().strip() if title_el else ""

        # Location
        loc_el = item.css('.location')
        location = loc_el[0].get_all_text().strip() if loc_el else ""

        # URL
        link_el = item.css('a')
        url = ""
        if link_el:
            url = link_el[0].attrib.get('href', '')

        # Filter: must be in target area
        if not in_target_area(location):
            continue

        phone = extract_phone(title)

        leads.append({
            "business_type": business_type,
            "title": title or "(no title)",
            "phone": phone,
            "location": location,
            "url": url,
        })

    # Deduplicate by URL
    seen = set()
    unique = []
    for lead in leads:
        key = lead["url"] or (lead["title"][:50] + lead["location"])
        if key not in seen:
            seen.add(key)
            unique.append(lead)

    return unique


def fetch_ad_phone(url: str) -> str:
    """Fetch individual ad page to find phone number."""
    if not url:
        return ""
    page = fetch_page(url)
    if not page:
        return ""
    body = page.css('body')
    text = body[0].get_all_text() if body else ""
    return extract_phone(text)


# ── Main scrape loop ──────────────────────────────────────────────────────────

def run_monitor(queries: dict, enrich_phone: bool = False) -> list[dict]:
    all_leads = []
    for biz_type, url in queries.items():
        print(f"\n🔍 Searching: {biz_type}...")
        page = fetch_page(url)
        if not page:
            print(f"  ⚠️  Could not fetch {url}")
            continue

        leads = parse_listings(page, biz_type)
        print(f"  ✅ Found {len(leads)} leads in target areas")

        if enrich_phone:
            for lead in leads:
                if not lead["phone"] and lead["url"]:
                    p = fetch_ad_phone(lead["url"])
                    if p:
                        lead["phone"] = p
                        print(f"     📞 {p} → {lead['title'][:40]}")

        all_leads.extend(leads)

    # Sort: phone-first, then by business type
    all_leads.sort(key=lambda x: (0 if x["phone"] else 1, x["business_type"]))
    return all_leads


# ── Output ────────────────────────────────────────────────────────────────────

def print_leads(leads: list[dict]):
    if not leads:
        print("\n❌ No leads found in target areas.")
        return

    print(f"\n{'='*60}")
    print(f"📋 CRAIGSLIST LEADS — {len(leads)} found")
    print(f"{'='*60}")
    for i, lead in enumerate(leads, 1):
        phone_str = f"📞 {lead['phone']}" if lead['phone'] else "📞 (no phone listed)"
        print(f"\n{i}. [{lead['business_type'].upper()}] {lead['title']}")
        print(f"   📍 {lead['location']}")
        print(f"   {phone_str}")
        if lead['url']:
            print(f"   🔗 {lead['url']}")


def save_leads(leads: list[dict]):
    MASTER_LEAD_LIST.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"\n## Craigslist Scan — {now}\n",
        f"**Source:** Craigslist NY Services | **Targets:** Staten Island, Brooklyn, Bronx\n",
        f"**Total:** {len(leads)} leads\n\n",
        "| # | Type | Business / Ad Title | Phone | Location | URL |\n",
        "|---|------|---------------------|-------|----------|-----|\n",
    ]
    for i, lead in enumerate(leads, 1):
        title = lead['title'].replace('|', '-')[:60]
        phone = lead['phone'] or "—"
        loc = lead['location'].replace('|', '-')[:30]
        url_cell = f"[link]({lead['url']})" if lead['url'] else "—"
        lines.append(f"| {i} | {lead['business_type']} | {title} | {phone} | {loc} | {url_cell} |\n")

    with open(MASTER_LEAD_LIST, "a") as f:
        f.writelines(lines)

    print(f"\n💾 Saved {len(leads)} leads → {MASTER_LEAD_LIST}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Craigslist Monitor — Gracie AI Receptionist lead scraper"
    )
    parser.add_argument("--save", action="store_true", help="Append results to MASTER_LEAD_LIST.md")
    parser.add_argument("--enrich", action="store_true", help="Fetch individual ads to find phone numbers")
    parser.add_argument("--type", dest="biz_type", metavar="TYPE",
                        help="Only search a specific type: " + ", ".join(SEARCH_QUERIES.keys()))
    args = parser.parse_args()

    queries = SEARCH_QUERIES
    if args.biz_type:
        key = args.biz_type.lower()
        if key not in SEARCH_QUERIES:
            print(f"Unknown type: '{key}'. Options: {list(SEARCH_QUERIES.keys())}")
            sys.exit(1)
        queries = {key: SEARCH_QUERIES[key]}

    leads = run_monitor(queries, enrich_phone=args.enrich)
    print_leads(leads)

    if args.save:
        save_leads(leads)


if __name__ == "__main__":
    main()
