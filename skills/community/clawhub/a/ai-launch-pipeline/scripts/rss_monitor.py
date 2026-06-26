#!/usr/bin/env python3
"""RSS Monitor — fetch and parse AI product launch feeds."""

import json, os, sys, time, re, hashlib
from xml.etree import ElementTree as ET
from urllib.request import urlopen, Request
from urllib.error import URLError
import yaml

USER_AGENT = "Mozilla/5.0 (compatible; AILaunchMonitor/1.0)"
TIMEOUT = 15
DATA_DIR = os.environ.get("PIPELINE_DATA_DIR", "data")
SEEN_FILE = os.path.join(DATA_DIR, "seen_ids.json")


def load_feeds(config_path: str) -> list:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    return cfg.get("feeds", [])


def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen: set):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(seen), f)


def fetch_feed(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_rss(xml_text: str, source_name: str, category: str) -> list:
    items = []
    try:
        root = ET.fromstring(xml_text)
        # Handle RSS 2.0 and Atom
        entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        for entry in entries:
            title_el = entry.find("title") or entry.find("{http://www.w3.org/2005/Atom}title")
            link_el = entry.find("link") or entry.find("{http://www.w3.org/2005/Atom}link")
            pub_el = entry.find("pubDate") or entry.find("{http://www.w3.org/2005/Atom}published")
            desc_el = entry.find("description") or entry.find("{http://www.w3.org/2005/Atom}summary")

            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link = ""
            if link_el is not None:
                link = link_el.text.strip() if link_el.text else link_el.get("href", "")
            pub = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
            desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""

            if not title:
                continue
            uid = hashlib.md5(f"{source_name}:{title}".encode()).hexdigest()
            items.append({
                "id": uid,
                "title": title,
                "link": link,
                "published": pub,
                "description": desc[:500],
                "source": source_name,
                "category": category,
            })
    except ET.ParseError as e:
        print(f"  XML parse error for {source_name}: {e}", file=sys.stderr)
    return items


def run(config_path: str, max_items: int = 100) -> list:
    """Main entry: returns list of new launch items."""
    feeds = load_feeds(config_path)
    seen = load_seen()
    all_items = []

    for feed in feeds:
        print(f"  Fetching: {feed['name']} ({feed['url']})")
        try:
            xml = fetch_feed(feed["url"])
            items = parse_rss(xml, feed["name"], feed.get("category", "unknown"))
            new_items = [i for i in items if i["id"] not in seen]
            print(f"    → {len(items)} total, {len(new_items)} new")
            all_items.extend(new_items)
        except (URLError, Exception) as e:
            print(f"    ✗ Error: {e}", file=sys.stderr)

    # Deduplicate and cap
    seen_ids = set()
    unique = []
    for item in all_items:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            unique.append(item)
    unique = unique[:max_items]

    # Save seen
    seen.update(i["id"] for i in unique)
    save_seen(seen)

    # Write output
    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(DATA_DIR, "raw_launches.json")
    with open(out_path, "w") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)
    print(f"  Saved {len(unique)} new launches → {out_path}")
    return unique


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config/rss_feeds.yaml")
    p.add_argument("--max-items", type=int, default=100)
    args = p.parse_args()
    run(args.config, args.max_items)
