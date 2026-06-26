#!/usr/bin/env python3
"""AI Product Monitor — One-click full pipeline.

Stages:
  1. RSS Monitor        → data/raw_launches.json
  2. Product Search     → data/enriched_launches.json
  3. Screenshot Capture → data/screenshots/*.png
  4. Trend Analysis     → data/trend_report.md
"""

import argparse
import json
import os
import re
import sys
import hashlib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
FEEDS_PATH = SKILL_DIR / "references" / "feeds.yaml"
RAW_PATH = DATA_DIR / "raw_launches.json"
ENRICHED_PATH = DATA_DIR / "enriched_launches.json"
SCREENSHOT_DIR = DATA_DIR / "screenshots"
REPORT_PATH = DATA_DIR / "trend_report.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_feeds_config():
    """Minimal YAML parser (no dependency required)."""
    import yaml  # try stdlib-style
    with open(FEEDS_PATH) as f:
        return yaml.safe_load(f)


def _try_import_yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def load_feeds_config_fallback():
    """Fallback YAML parser if pyyaml is not installed."""
    yaml = _try_import_yaml()
    if yaml:
        return yaml.safe_load(open(FEEDS_PATH))
    # Minimal parse for our specific format
    config = {"feeds": [], "launch_keywords": [], "lookback_days": 7}
    current_list = None
    with open(FEEDS_PATH) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue
            if stripped.startswith("feeds:"):
                current_list = "feeds"
            elif stripped.startswith("launch_keywords:"):
                current_list = "keywords"
            elif stripped.startswith("lookback_days:"):
                config["lookback_days"] = int(stripped.split(":")[1].strip())
            elif stripped.startswith("- name:"):
                if current_list == "feeds":
                    config["feeds"].append({"name": stripped.split(":", 1)[1].strip()})
                    current_field = "feed"
            elif stripped.startswith("url:"):
                if config["feeds"]:
                    config["feeds"][-1]["url"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("category:"):
                if config["feeds"]:
                    config["feeds"][-1]["category"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("- ") and current_list == "keywords":
                config["launch_keywords"].append(stripped[2:].strip().strip('"').strip("'").lower())
    return config


def ensure_data_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def item_id(title: str, url: str) -> str:
    return hashlib.md5(f"{title}|{url}".encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Stage 1: RSS Monitor
# ---------------------------------------------------------------------------

def stage_rss():
    print("📡 Stage 1: RSS Monitor")
    config = load_feeds_config_fallback()
    keywords = [k.lower() for k in config.get("launch_keywords", [])]
    lookback = config.get("lookback_days", 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback)

    launches = []
    existing_ids = set()
    if RAW_PATH.exists():
        for item in json.loads(RAW_PATH.read_text()):
            existing_ids.add(item["id"])
            launches.append(item)

    for feed_cfg in config.get("feeds", []):
        name = feed_cfg.get("name", "Unknown")
        url = feed_cfg.get("url")
        category = feed_cfg.get("category", "unknown")
        if not url:
            continue
        print(f"  Fetching {name} ...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AI-Product-Monitor/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                xml_data = resp.read()
        except Exception as e:
            print(f"  ⚠ Failed to fetch {name}: {e}")
            continue

        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            print(f"  ⚠ Parse error for {name}: {e}")
            continue

        # Atom or RSS
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall(".//atom:entry", ns) or root.findall(".//item")

        for entry in entries:
            title_el = entry.find("atom:title", ns) or entry.find("title")
            link_el = entry.find("atom:link", ns) or entry.find("link")
            date_el = entry.find("atom:published", ns) or entry.find("pubDate")
            desc_el = entry.find("atom:summary", ns) or entry.find("description")

            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link = ""
            if link_el is not None:
                link = link_el.attrib.get("href", "") or (link_el.text or "").strip()
            pub_date = date_el.text.strip() if date_el is not None and date_el.text else ""
            desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""

            if not title or not link:
                continue

            # Check if launch-related
            text_blob = f"{title} {desc}".lower()
            if not any(kw in text_blob for kw in keywords):
                continue

            iid = item_id(title, link)
            if iid in existing_ids:
                continue

            launches.append({
                "id": iid,
                "title": title,
                "url": link,
                "date": pub_date,
                "description": desc[:500],
                "source": name,
                "category": category,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            })
            existing_ids.add(iid)
            print(f"    ✅ {title}")

    RAW_PATH.write_text(json.dumps(launches, indent=2, ensure_ascii=False))
    print(f"  Total launches: {len(launches)}")
    return launches


# ---------------------------------------------------------------------------
# Stage 2: Product Search (web search enrichment)
# ---------------------------------------------------------------------------

def stage_search():
    print("🔍 Stage 2: Product Info Search")
    if not RAW_PATH.exists():
        print("  ⚠ No raw_launches.json — run stage 1 first")
        return []

    launches = json.loads(RAW_PATH.read_text())
    enriched = []
    if ENRICHED_PATH.exists():
        enriched = json.loads(ENRICHED_PATH.read_text())
    enriched_ids = {e["id"] for e in enriched}

    # Use Brave search via web_fetch on the OpenClaw tools API if available,
    # otherwise fall back to a simple web request.
    # Since this script runs inside OpenClaw context, we invoke the CLI.
    import subprocess

    for item in launches:
        if item["id"] in enriched_ids:
            continue

        query = f'{item["title"]} AI product launch'
        print(f"  Searching: {query}")

        search_snippet = ""
        try:
            # Use openclaw's web search if available
            result = subprocess.run(
                ["openclaw", "web-search", query, "--count", "3", "--format", "json"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                search_snippet = result.stdout.strip()[:2000]
            else:
                # Fallback: just mark as searched
                search_snippet = "(search unavailable)"
        except Exception:
            search_snippet = "(search unavailable)"

        entry = {**item, "search_context": search_snippet}
        enriched.append(entry)
        enriched_ids.add(entry["id"])

    ENRICHED_PATH.write_text(json.dumps(enriched, indent=2, ensure_ascii=False))
    print(f"  Enriched items: {len(enriched)}")
    return enriched


# ---------------------------------------------------------------------------
# Stage 3: Screenshot Capture
# ---------------------------------------------------------------------------

def stage_screenshot():
    print("📸 Stage 3: Screenshot Capture")
    if not ENRICHED_PATH.exists():
        print("  ⚠ No enriched_launches.json — run stage 2 first")
        return

    items = json.loads(ENRICHED_PATH.read_text())
    import subprocess

    captured = {f.stem for f in SCREENSHOT_DIR.glob("*.png")}

    for item in items:
        slug = slugify(item["title"])
        out_file = SCREENSHOT_DIR / f"{slug}.png"
        if slug in captured:
            continue

        url = item.get("url", "")
        if not url:
            continue

        print(f"  Capturing: {item['title'][:60]}")
        try:
            # Use OpenClaw browser tool if available
            result = subprocess.run(
                ["openclaw", "browser", "screenshot", "--url", url, "--out", str(out_file)],
                capture_output=True, text=True, timeout=45,
            )
            if result.returncode != 0:
                print(f"    ⚠ Screenshot failed: {result.stderr[:100]}")
        except Exception as e:
            print(f"    ⚠ Screenshot error: {e}")

    total = len(list(SCREENSHOT_DIR.glob("*.png")))
    print(f"  Screenshots: {total}")


# ---------------------------------------------------------------------------
# Stage 4: Trend Analysis
# ---------------------------------------------------------------------------

def stage_trends():
    print("📊 Stage 4: Trend Analysis")

    items = []
    for path in [ENRICHED_PATH, RAW_PATH]:
        if path.exists():
            items = json.loads(path.read_text())
            break

    if not items:
        print("  ⚠ No data to analyze")
        return

    # Aggregate stats
    sources = {}
    categories = {}
    dates = []
    for item in items:
        src = item.get("source", "Unknown")
        sources[src] = sources.get(src, 0) + 1
        cat = item.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        dates.append(item.get("date", "")[:10])

    # Build report
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# AI Product Launch Trend Report",
        f"",
        f"_Generated: {now}_",
        f"",
        f"## Overview",
        f"",
        f"- **Total launches tracked:** {len(items)}",
        f"- **Sources monitored:** {len(sources)}",
        f"",
        f"## By Source",
        f"",
    ]
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        lines.append(f"- **{src}**: {count}")

    lines += [
        "",
        "## By Category",
        "",
    ]
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        lines.append(f"- **{cat}**: {count}")

    # Timeline
    date_counts = {}
    for d in sorted(dates):
        if d:
            date_counts[d] = date_counts.get(d, 0) + 1

    lines += [
        "",
        "## Launch Timeline",
        "",
    ]
    for d, count in sorted(date_counts.items()):
        bar = "█" * count
        lines.append(f"- **{d}**: {bar} ({count})")

    # Recent items
    lines += [
        "",
        "## Recent Launches",
        "",
    ]
    for item in items[-10:]:
        lines.append(f"- [{item.get('title', 'Untitled')}]({item.get('url', '#')}) — _{item.get('source', '')}_")

    # Key insights
    top_source = max(sources, key=sources.get) if sources else "N/A"
    lines += [
        "",
        "## Key Insights",
        "",
        f"- Most active source: **{top_source}** ({sources.get(top_source, 0)} launches)",
        f"- Average launches per day: {len(items) / max(len(date_counts), 1):.1f}",
        f"- Screenshots captured: {len(list(SCREENSHOT_DIR.glob('*.png')))}",
    ]

    REPORT_PATH.write_text("\n".join(lines))
    print(f"  Report written to {REPORT_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

STAGES = {
    "rss": stage_rss,
    "search": stage_search,
    "screenshot": stage_screenshot,
    "trends": stage_trends,
}

def main():
    parser = argparse.ArgumentParser(description="AI Product Monitor Pipeline")
    parser.add_argument("--stage", choices=list(STAGES.keys()), help="Run a single stage (default: all)")
    parser.add_argument("--from-stage", choices=list(STAGES.keys()), help="Run from this stage onward")
    args = parser.parse_args()

    ensure_data_dirs()

    stage_order = ["rss", "search", "screenshot", "trends"]

    if args.stage:
        STAGES[args.stage]()
    elif args.from_stage:
        idx = stage_order.index(args.from_stage)
        for s in stage_order[idx:]:
            STAGES[s]()
            print()
    else:
        for s in stage_order:
            STAGES[s]()
            print()

    print("✅ Pipeline complete.")

if __name__ == "__main__":
    main()