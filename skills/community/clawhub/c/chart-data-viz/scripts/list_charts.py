#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_charts

def main():
    data = load_charts()
    charts = data.get("charts", {})

    if not charts:
        print("No charts found.")
        return

    for chart_id, chart in charts.items():
        print(f"{chart_id} | {chart['type']} | {chart['title']}")
        print(f"  {chart['output_path']}")

if __name__ == "__main__":
    main()
