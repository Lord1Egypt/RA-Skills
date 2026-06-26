#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, PAGES_DIR

def slugify(text: str) -> str:
    safe = "".join(c.lower() if c.isalnum() else "-" for c in text)
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe.strip("-") or "output"

def main():
    parser = argparse.ArgumentParser(description="Save cleaned output with a custom title")
    parser.add_argument("--url", required=True, help="URL to find in job history")
    parser.add_argument("--title", required=True, help="Output title")
    args = parser.parse_args()

    jobs = load_jobs().get("jobs", {})
    matches = [j for j in jobs.values() if j.get("url") == args.url]
    if not matches:
        print("No fetched job found for this URL.")
        sys.exit(1)

    latest = sorted(matches, key=lambda x: x["created_at"], reverse=True)[0]
    clean_path = latest["clean_path"]

    with open(clean_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = f"{slugify(args.title)}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    out_path = os.path.join(PAGES_DIR, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ Saved cleaned output")
    print(f"  {out_path}")

if __name__ == "__main__":
    main()
