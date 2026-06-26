#!/usr/bin/env python3
import json
import os
from datetime import datetime

FETCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/fetch")
PAGES_DIR = os.path.join(FETCH_DIR, "pages")
JOBS_FILE = os.path.join(FETCH_DIR, "jobs.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(FETCH_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    write_json_if_missing(JOBS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "jobs": {}
    })

    print("✓ Fetch storage initialized")
    print(f"  {JOBS_FILE}")
    print(f"  {PAGES_DIR}")

if __name__ == "__main__":
    main()
