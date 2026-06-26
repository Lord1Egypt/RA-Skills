#!/usr/bin/env python3
"""Competitor Monitor - Track competitor websites, pricing, and activity."""

import argparse
import hashlib
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from difflib import unified_diff

CONFIG_PATH = Path.home() / ".openclaw" / "competitor-monitor.json"
DATA_DIR = Path.home() / ".openclaw" / "competitor-data"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    default = {"competitors": [], "alertChannel": "telegram", "diffThreshold": 0.05}
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(default, indent=2))
    return default


def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


def fetch_page(url, timeout=15):
    """Fetch a URL and return text content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def extract_text(html):
    """Simple HTML to text extraction."""
    import re
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def get_snapshot_path(name, track_type):
    safe_name = name.lower().replace(" ", "-")
    return DATA_DIR / safe_name / f"{track_type}_latest.txt"


def get_history_path(name):
    safe_name = name.lower().replace(" ", "-")
    return DATA_DIR / safe_name / "history.json"


def save_snapshot(name, track_type, content):
    path = get_snapshot_path(name, track_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def load_snapshot(name, track_type):
    path = get_snapshot_path(name, track_type)
    if path.exists():
        return path.read_text()
    return None


def log_change(name, track_type, summary, old_hash, new_hash):
    path = get_history_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    history = []
    if path.exists():
        try:
            history = json.loads(path.read_text())
        except json.JSONDecodeError:
            history = []
    history.append({
        "timestamp": datetime.now().isoformat(),
        "type": track_type,
        "summary": summary,
        "old_hash": old_hash,
        "new_hash": new_hash,
    })
    path.write_text(json.dumps(history, indent=2))


def check_page_changes(name, url, track_type):
    """Check a page for changes since last snapshot."""
    html = fetch_page(url)
    if not html:
        return None

    text = extract_text(html)
    new_hash = content_hash(text)
    old_text = load_snapshot(name, track_type)

    if old_text is None:
        save_snapshot(name, track_type, text)
        print(f"  [{track_type}] Initial snapshot saved for {name}")
        return None

    old_hash = content_hash(old_text)
    if old_hash == new_hash:
        return None

    # Calculate diff
    old_lines = old_text.split(". ")
    new_lines = text.split(". ")
    diff = list(unified_diff(old_lines, new_lines, n=1))

    # Check if change exceeds threshold
    change_ratio = len(diff) / max(len(old_lines), 1)

    save_snapshot(name, track_type, text)

    changes = {
        "name": name,
        "type": track_type,
        "url": url,
        "change_ratio": change_ratio,
        "diff_lines": len(diff),
        "timestamp": datetime.now().isoformat(),
        "summary": f"{len(diff)} changes detected ({change_ratio:.1%} of content)",
    }

    log_change(name, track_type, changes["summary"], old_hash, new_hash)
    return changes


def check_competitor(competitor):
    """Run all checks for a single competitor."""
    name = competitor["name"]
    changes = []
    print(f"\nChecking: {name}")

    tracks = competitor.get("trackingTypes", ["pricing", "blog"])

    if "pricing" in tracks and competitor.get("pricingUrl"):
        result = check_page_changes(name, competitor["pricingUrl"], "pricing")
        if result:
            changes.append(result)

    if "blog" in tracks:
        blog_url = competitor.get("blogUrl", competitor["url"] + "/blog")
        result = check_page_changes(name, blog_url, "blog")
        if result:
            changes.append(result)

    if "changelog" in tracks:
        changelog_url = competitor.get("changelogUrl", competitor["url"] + "/changelog")
        result = check_page_changes(name, changelog_url, "changelog")
        if result:
            changes.append(result)

    # Main page check
    result = check_page_changes(name, competitor["url"], "main")
    if result:
        changes.append(result)

    if not changes:
        print(f"  No changes detected.")

    return changes


def add_competitor(args):
    config = load_config()
    entry = {
        "name": args.name,
        "url": args.url,
        "trackingTypes": args.track.split(",") if args.track else ["pricing", "blog"],
        "checkInterval": args.check_interval or "6h",
    }
    if args.social_twitter:
        entry["twitter"] = args.social_twitter

    # Auto-derive URLs
    base = args.url.rstrip("/")
    entry["pricingUrl"] = f"{base}/pricing"
    entry["blogUrl"] = f"{base}/blog"
    entry["changelogUrl"] = f"{base}/changelog"

    config["competitors"].append(entry)
    save_config(config)
    print(f"Added competitor: {args.name}")
    print(f"Tracking: {', '.join(entry['trackingTypes'])}")


def check_all(args):
    config = load_config()
    all_changes = []

    if args.name:
        competitors = [c for c in config["competitors"] if c["name"] == args.name]
    else:
        competitors = config["competitors"]

    if not competitors:
        print("No competitors configured. Use 'add' to add one.")
        return

    for comp in competitors:
        changes = check_competitor(comp)
        all_changes.extend(changes)

    if all_changes and args.alert_changes:
        print(f"\n=== {len(all_changes)} CHANGES DETECTED ===")
        for c in all_changes:
            print(f"\nCOMPETITOR ALERT: {c['name']}")
            print(f"Change type: {c['type']}")
            print(f"Detected: {c['timestamp']}")
            print(f"Summary: {c['summary']}")

    return all_changes


def show_history(args):
    path = get_history_path(args.name)
    if not path.exists():
        print(f"No history for {args.name}")
        return

    history = json.loads(path.read_text())
    days = args.days or 30
    cutoff = datetime.now() - timedelta(days=days)

    print(f"\nChange history for {args.name} (last {days} days):")
    print(f"{'Date':<22} | {'Type':<12} | {'Summary'}")
    print("-" * 70)
    for entry in history:
        ts = datetime.fromisoformat(entry["timestamp"])
        if ts >= cutoff:
            print(f"{entry['timestamp'][:19]:<22} | {entry['type']:<12} | {entry['summary']}")


def generate_report(args):
    config = load_config()
    period = args.period or "week"
    days = 7 if period == "week" else 30

    print(f"# Competitive Intelligence Report")
    print(f"Period: Last {days} days | Generated: {datetime.now().strftime('%Y-%m-%d')}\n")

    for comp in config["competitors"]:
        path = get_history_path(comp["name"])
        if not path.exists():
            continue

        history = json.loads(path.read_text())
        cutoff = datetime.now() - timedelta(days=days)
        recent = [h for h in history if datetime.fromisoformat(h["timestamp"]) >= cutoff]

        print(f"## {comp['name']}")
        print(f"URL: {comp['url']}")
        print(f"Changes detected: {len(recent)}\n")
        for entry in recent:
            print(f"- **{entry['type']}** ({entry['timestamp'][:10]}): {entry['summary']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Competitor Monitor")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add")
    add_p.add_argument("--name", required=True)
    add_p.add_argument("--url", required=True)
    add_p.add_argument("--track", default="pricing,blog,changelog")
    add_p.add_argument("--social-twitter")
    add_p.add_argument("--check-interval", default="6h")

    check_p = sub.add_parser("check")
    check_p.add_argument("--all", action="store_true")
    check_p.add_argument("--name")
    check_p.add_argument("--quiet", action="store_true")
    check_p.add_argument("--alert-changes", action="store_true")

    hist_p = sub.add_parser("history")
    hist_p.add_argument("--name", required=True)
    hist_p.add_argument("--days", type=int, default=30)

    report_p = sub.add_parser("report")
    report_p.add_argument("--format", default="markdown")
    report_p.add_argument("--period", default="week")

    args = parser.parse_args()

    if args.command == "add":
        add_competitor(args)
    elif args.command == "check":
        check_all(args)
    elif args.command == "history":
        show_history(args)
    elif args.command == "report":
        generate_report(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
