#!/usr/bin/env python3
import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases

def main():
    data = load_cases()
    rows = []
    for cid, case in sorted(data.get("cases", {}).items()):
        rows.append({
            "id": cid,
            "title": case.get("title"),
            "overall_score": case.get("score", {}).get("overall"),
            "created_at": case.get("created_at")
        })
    print(json.dumps(rows, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
