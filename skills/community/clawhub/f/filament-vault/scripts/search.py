#!/usr/bin/env python3
"""Fuzzy search filament inventory across all fields."""

import argparse
import json
import os
import re
import sys

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/filament-vault")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def tokenize(text):
    """Return lowercase words from text."""
    return re.findall(r"[a-z0-9]+", text.lower())


def score_spool(spool, query_tokens):
    """
    Score a spool against query tokens.
    Returns (score, matched_fields) where score > 0 means a match.
    Higher score = better match.
    """
    fields = {
        "brand": spool.get("brand", ""),
        "material": spool.get("material", ""),
        "color": spool.get("color", ""),
        "location": spool.get("location") or "",
        "notes": spool.get("notes") or "",
        "status": spool.get("status", ""),
        "id": spool.get("id", ""),
        "added_date": spool.get("added_date", ""),
    }

    score = 0
    matched_fields = []

    for field_name, value in fields.items():
        value_tokens = tokenize(value)
        value_lower = value.lower()

        for qt in query_tokens:
            # Exact substring match (higher weight)
            if qt in value_lower:
                score += 3 if field_name in ("brand", "material", "color") else 2
                if field_name not in matched_fields:
                    matched_fields.append(field_name)
            # Token-level partial match
            elif any(qt in vt for vt in value_tokens):
                score += 1
                if field_name not in matched_fields:
                    matched_fields.append(field_name)

    return score, matched_fields


def print_results(results, query):
    if not results:
        print(f"No spools matched '{query}'.")
        return

    print(f"Found {len(results)} result(s) for '{query}':\n")

    for spool, score, matched_fields in results:
        status = spool.get("status", "active")
        rem = spool.get("weight_remaining_g", 0)
        init = spool.get("weight_initial_g", 0)
        cost_str = f"  Cost: ${spool['cost_usd']:.2f}" if spool.get("cost_usd") is not None else ""
        loc_str = f"  Location: {spool['location']}" if spool.get("location") else ""
        notes_str = f"  Notes: {spool['notes']}" if spool.get("notes") else ""
        status_display = "⚠ low" if status == "active" and rem < 100 else status

        print(
            f"  [{spool['id'][:8]}…] {spool['brand']} {spool['material']} — {spool['color']}"
        )
        print(
            f"    Remaining: {rem:.0f}g / {init:.0f}g  |  Status: {status_display}"
            f"  |  Added: {spool.get('added_date', '—')}"
        )
        if cost_str:
            print(f"   {cost_str}")
        if loc_str:
            print(f"   {loc_str}")
        if notes_str:
            # Truncate long notes for display
            note_display = spool["notes"]
            if len(note_display) > 120:
                note_display = note_display[:117] + "…"
            print(f"    Notes: {note_display}")
        print(f"    Matched: {', '.join(matched_fields)}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Fuzzy search filament inventory across all fields."
    )
    parser.add_argument("query", help="Search query (e.g. 'black petg', 'bambu', 'shelf a')")
    parser.add_argument("--all", action="store_true", help="Include finished spools")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument(
        "--min-score",
        type=int,
        default=1,
        help="Minimum relevance score to include in results (default: 1)",
    )

    args = parser.parse_args()

    spools = load_inventory()

    if not spools:
        print("Inventory is empty. Add spools with add_spool.py.")
        return

    if not args.all:
        spools = [s for s in spools if s.get("status") != "finished"]

    query_tokens = tokenize(args.query)
    if not query_tokens:
        print("Error: empty query.", file=sys.stderr)
        sys.exit(1)

    scored = []
    for spool in spools:
        score, matched = score_spool(spool, query_tokens)
        if score >= args.min_score:
            scored.append((spool, score, matched))

    # Sort by score descending, then brand+color
    scored.sort(key=lambda x: (-x[1], x[0].get("brand", ""), x[0].get("color", "")))

    if args.json:
        output = [s for s, _, _ in scored]
        print(json.dumps(output, indent=2))
        return

    print_results(scored, args.query)


if __name__ == "__main__":
    main()
