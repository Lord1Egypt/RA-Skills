#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_list(data):
    patches = data.get("patch_candidates", [])
    for i, patch in enumerate(patches, start=1):
        status = "approved" if patch.get("approved") else patch.get("review_status", "pending")
        print(f"[{i}] {patch.get('id')} -> {patch.get('target_file')} | {status}")
        print(f"    rationale: {patch.get('rationale')}")
        if patch.get("anchor"):
            print(f"    anchor: {patch.get('anchor')} ({patch.get('insert_mode')})")
        print(f"    entry: {patch.get('suggested_entry')}")


def update_patch(patch, action, note=None):
    if action == "approve":
        patch["approved"] = True
        patch["review_status"] = "approved"
    elif action == "reject":
        patch["approved"] = False
        patch["review_status"] = "rejected"
    elif action == "skip":
        patch.setdefault("approved", False)
        patch["review_status"] = "skipped"
    if note:
        patch["review_note"] = note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="Path to patch JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list")

    act = sub.add_parser("act")
    act.add_argument("--index", type=int, required=True, help="1-based patch index")
    act.add_argument("--action", choices=["approve", "reject", "skip"], required=True)
    act.add_argument("--note", default="")

    args = ap.parse_args()
    path = Path(args.patches)
    data = load_json(path)
    patches = data.get("patch_candidates", [])

    if args.cmd == "list":
        print_list(data)
        return

    idx = args.index - 1
    if idx < 0 or idx >= len(patches):
        raise SystemExit("index out of range")
    update_patch(patches[idx], args.action, args.note)
    save_json(path, data)
    print(json.dumps(patches[idx], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
