#!/usr/bin/env python3
"""Update a filament spool: log usage, mark finished, or add notes."""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/filament-vault")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def save_inventory(spools):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as f:
        json.dump(spools, f, indent=2)


def find_by_id(spools, spool_id):
    for i, s in enumerate(spools):
        if s["id"] == spool_id:
            return i, s
    return None, None


def find_by_search(spools, query):
    query_lower = query.lower()
    matches = []
    for i, s in enumerate(spools):
        fields = [
            s.get("brand", ""),
            s.get("color", ""),
            s.get("material", ""),
            s.get("location", "") or "",
            s.get("notes", "") or "",
            s["id"],
        ]
        if any(query_lower in f.lower() for f in fields):
            matches.append((i, s))
    return matches


def main():
    parser = argparse.ArgumentParser(description="Update a filament spool in inventory.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="Spool UUID to update")
    group.add_argument("--search", help="Partial match search (brand, color, material, etc.)")

    parser.add_argument("--used", type=float, help="Grams consumed in this session")
    parser.add_argument(
        "--finished", action="store_true", help="Mark spool as finished/empty"
    )
    parser.add_argument("--notes", help="Append a note to the spool")

    args = parser.parse_args()

    if not any([args.used, args.finished, args.notes]):
        print(
            "Error: specify at least one of --used, --finished, or --notes.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.used is not None and args.used <= 0:
        print("Error: --used must be greater than 0.", file=sys.stderr)
        sys.exit(1)

    spools = load_inventory()

    if not spools:
        print("Inventory is empty. Add spools with add_spool.py.", file=sys.stderr)
        sys.exit(1)

    if args.id:
        idx, spool = find_by_id(spools, args.id)
        if spool is None:
            print(f"Error: no spool found with ID '{args.id}'.", file=sys.stderr)
            sys.exit(1)
        selected = [(idx, spool)]
    else:
        selected = find_by_search(spools, args.search)
        if not selected:
            print(
                f"Error: no spools matched '{args.search}'.", file=sys.stderr
            )
            sys.exit(1)
        if len(selected) > 1:
            print(
                f"Multiple spools matched '{args.search}'. Narrow your search or use --id:"
            )
            for _, s in selected:
                print(
                    f"  [{s['id'][:8]}…] {s['brand']} {s['material']} — {s['color']} "
                    f"({s['weight_remaining_g']:.0f}g remaining)"
                )
            sys.exit(1)

    idx, spool = selected[0]

    if spool["status"] == "finished" and not args.notes:
        print(
            f"Warning: spool [{spool['id'][:8]}…] is already finished. "
            "Use --notes to add a note.",
            file=sys.stderr,
        )
        sys.exit(1)

    changes = []

    if args.used is not None:
        before = spool["weight_remaining_g"]
        spool["weight_remaining_g"] = max(0.0, before - args.used)
        changes.append(
            f"Used {args.used:.0f}g → {before:.0f}g ➜ {spool['weight_remaining_g']:.0f}g remaining"
        )
        if spool["weight_remaining_g"] == 0:
            spool["status"] = "finished"
            spool["finished_date"] = datetime.now().strftime("%Y-%m-%d")
            changes.append("Auto-marked as finished (0g remaining)")

    if args.finished:
        spool["weight_remaining_g"] = 0.0
        spool["status"] = "finished"
        spool["finished_date"] = datetime.now().strftime("%Y-%m-%d")
        changes.append("Marked as finished")

    if args.notes:
        existing = spool.get("notes") or ""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_note = f"[{timestamp}] {args.notes}"
        spool["notes"] = f"{existing}\n{new_note}".strip()
        changes.append(f"Added note: {args.notes}")

    spools[idx] = spool
    save_inventory(spools)

    print(f"✓ Updated: {spool['brand']} {spool['material']} — {spool['color']}")
    print(f"  ID: {spool['id']}")
    for change in changes:
        print(f"  → {change}")

    # Low-stock warning
    if spool["status"] == "active" and spool["weight_remaining_g"] < 100:
        print(
            f"  ⚠ Low stock: only {spool['weight_remaining_g']:.0f}g remaining!"
        )


if __name__ == "__main__":
    main()
