#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="Path to patch JSON")
    args = ap.parse_args()

    data = load_json(Path(args.patches))
    patches = data.get("patch_candidates", [])

    print(f"new_candidates: {data.get('new_candidates', 0)}")
    print(f"high_priority: {data.get('high_priority', 0)}")
    print(f"needs_human_review: {str(data.get('needs_human_review', True)).lower()}")
    print()

    grouped = {}
    for patch in patches:
        grouped.setdefault(patch.get("target_file", "unknown"), []).append(patch)

    for target, group in grouped.items():
        print(f"## {target} ({len(group)})")
        for i, patch in enumerate(group, start=1):
            status = "approved" if patch.get("approved") else patch.get("review_status", "pending")
            print(f"- [{status}] {patch.get('id')}")
            print(f"  rationale: {patch.get('rationale')}")
            if patch.get("anchor"):
                print(f"  anchor: {patch.get('anchor')} ({patch.get('insert_mode')})")
            print(f"  entry: {patch.get('suggested_entry')}")
        print()


if __name__ == "__main__":
    main()
