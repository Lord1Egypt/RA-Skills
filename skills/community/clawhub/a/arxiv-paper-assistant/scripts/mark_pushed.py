#!/usr/bin/env python3
"""
Mark a paper as pushed by adding its ID to data/pushed.json.
Usage: python3 mark_pushed.py <paper_id>
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
PUSHED_FILE = os.path.join(DATA_DIR, "pushed.json")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 mark_pushed.py <paper_id>", file=sys.stderr)
        sys.exit(1)

    paper_id = sys.argv[1]

    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(PUSHED_FILE):
        with open(PUSHED_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"pushed": []}

    if paper_id not in data["pushed"]:
        data["pushed"].append(paper_id)
        with open(PUSHED_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Marked as pushed: {paper_id}")
    else:
        print(f"Already marked: {paper_id}")


if __name__ == "__main__":
    main()