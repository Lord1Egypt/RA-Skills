#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backlog", help="Backlog JSON from build_backlog.py")
    ap.add_argument("--top", type=int, default=10, help="Show top N items")
    args = ap.parse_args()

    data = load_json(Path(args.backlog))
    items = data.get("items", [])[: args.top]
    print(f"backlog_count: {data.get('count', 0)}")
    print(f"showing_top: {len(items)}")
    print()
    for i, item in enumerate(items, start=1):
        print(f"[{i}] {item.get('id')} | score={item.get('priority_score')}")
        print(f"    type={item.get('type')} reuse={item.get('reuse_value')} confidence={item.get('confidence')} scope={item.get('impact_scope')} worth={item.get('promotion_worthiness')}")
        print(f"    targets={', '.join(item.get('targets') or ['daily-memory'])}")
        print(f"    summary={item.get('summary')}")


if __name__ == "__main__":
    main()
