#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_cases

def main():
    parser = argparse.ArgumentParser(description="Show score for one case")
    parser.add_argument("--id", required=True, help="Case ID")
    args = parser.parse_args()

    data = load_cases()
    case = data["cases"].get(args.id)
    if not case:
        print(f"Case not found: {args.id}")
        sys.exit(1)

    print(json.dumps({
        "id": case["id"],
        "title": case["title"],
        "score": case.get("score", {})
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
