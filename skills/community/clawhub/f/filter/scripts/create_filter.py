#!/usr/bin/env python3
"""Create and store reusable filter rules."""

import json
import os
import uuid
import argparse
from datetime import datetime

FILTER_DIR = os.path.expanduser("~/.openclaw/workspace/memory/filter")
RULES_FILE = os.path.join(FILTER_DIR, "rules.json")


def ensure_dir():
    os.makedirs(FILTER_DIR, exist_ok=True)


def load_rules():
    if not os.path.exists(RULES_FILE):
        return {"rules": []}

    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"rules": []}


def save_rules(data):
    ensure_dir()
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Create filter rule")
    parser.add_argument("--type", required=True, help="Content type (email, news, search, tasks, etc)")
    parser.add_argument("--criteria", required=True, help="Filter criteria")
    parser.add_argument("--priority", default="medium", choices=["low", "medium", "high"])
    args = parser.parse_args()

    filter_id = f"FILTER-{str(uuid.uuid4())[:6].upper()}"

    filter_rule = {
        "id": filter_id,
        "type": args.type,
        "criteria": args.criteria,
        "priority": args.priority,
        "created_at": datetime.now().isoformat(),
        "active": True
    }

    data = load_rules()
    data["rules"].append(filter_rule)
    save_rules(data)

    print(f"✓ Filter rule created: {filter_id}")
    print(f"  Type: {args.type}")
    print(f"  Criteria: {args.criteria}")
    print(f"  Priority: {args.priority}")
    print(f"  Saved to: {RULES_FILE}")


if __name__ == "__main__":
    main()
