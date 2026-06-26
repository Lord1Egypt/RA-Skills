#!/usr/bin/env python3
import json
import os
from datetime import datetime

CHART_DIR = os.path.expanduser("~/.openclaw/workspace/memory/chart")
OUTPUT_DIR = os.path.join(CHART_DIR, "output")
CHARTS_FILE = os.path.join(CHART_DIR, "charts.json")

def write_json_if_missing(path, payload):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(CHART_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    write_json_if_missing(CHARTS_FILE, {
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        },
        "charts": {}
    })

    print("✓ Chart storage initialized")
    print(f"  {CHARTS_FILE}")
    print(f"  {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
