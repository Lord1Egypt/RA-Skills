#!/usr/bin/env python3
"""List filament inventory with optional filters."""

import argparse
import json
import os
import sys

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/filament-vault")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

LOW_STOCK_DEFAULT = 100  # grams


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def apply_filters(spools, material=None, color=None, brand=None, low_stock=False, threshold=LOW_STOCK_DEFAULT, include_finished=False):
    filtered = []
    for s in spools:
        if not include_finished and s.get("status") == "finished":
            continue
        if material and s.get("material", "").lower() != material.lower():
            continue
        if color and color.lower() not in s.get("color", "").lower():
            continue
        if brand and brand.lower() not in s.get("brand", "").lower():
            continue
        if low_stock and s.get("weight_remaining_g", 0) >= threshold:
            continue
        filtered.append(s)
    return filtered


def print_table(spools):
    if not spools:
        print("No spools match your filters.")
        return

    col_id = 10
    col_brand = max(len("Brand"), max(len(s.get("brand", "")) for s in spools))
    col_mat = max(len("Material"), max(len(s.get("material", "")) for s in spools))
    col_color = max(len("Color"), max(len(s.get("color", "")) for s in spools))
    col_rem = 10
    col_init = 10
    col_cost = 8
    col_loc = max(len("Location"), max(len(s.get("location") or "") for s in spools))
    col_status = 8

    def row(*cols_vals):
        parts = []
        widths = [col_id, col_brand, col_mat, col_color, col_rem, col_init, col_cost, col_loc, col_status]
        for val, w in zip(cols_vals, widths):
            parts.append(str(val).ljust(w))
        return "  ".join(parts)

    header = row("ID", "Brand", "Material", "Color", "Remaining", "Initial", "Cost", "Location", "Status")
    sep = "-" * len(header)
    print(header)
    print(sep)

    for s in spools:
        short_id = s["id"][:8] + "…"
        remaining = f"{s.get('weight_remaining_g', 0):.0f}g"
        initial = f"{s.get('weight_initial_g', 0):.0f}g"
        cost = f"${s['cost_usd']:.2f}" if s.get("cost_usd") is not None else "—"
        location = s.get("location") or "—"
        status = s.get("status", "active")

        # Add low-stock flag
        if status == "active" and s.get("weight_remaining_g", 0) < LOW_STOCK_DEFAULT:
            status = "⚠ low"

        print(row(short_id, s.get("brand", ""), s.get("material", ""), s.get("color", ""),
                  remaining, initial, cost, location, status))

    print(sep)
    active = [s for s in spools if s.get("status") not in ("finished",)]
    total_g = sum(s.get("weight_remaining_g", 0) for s in active)
    print(f"  {len(spools)} spool(s) shown  |  {total_g:.0f}g total remaining")


def main():
    parser = argparse.ArgumentParser(description="List filament inventory.")
    parser.add_argument("--material", help="Filter by material (e.g. PLA, PETG)")
    parser.add_argument("--color", help="Filter by color (partial match)")
    parser.add_argument("--brand", help="Filter by brand (partial match)")
    parser.add_argument(
        "--low-stock",
        action="store_true",
        help=f"Show only spools below threshold (default {LOW_STOCK_DEFAULT}g)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=LOW_STOCK_DEFAULT,
        help=f"Low-stock threshold in grams (default {LOW_STOCK_DEFAULT})",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include finished spools",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    spools = load_inventory()

    if not spools:
        if args.json:
            print("[]")
        else:
            print("Inventory is empty. Add spools with add_spool.py.")
        return

    filtered = apply_filters(
        spools,
        material=args.material,
        color=args.color,
        brand=args.brand,
        low_stock=args.low_stock,
        threshold=args.threshold,
        include_finished=args.all,
    )

    if args.json:
        print(json.dumps(filtered, indent=2))
    else:
        print_table(filtered)


if __name__ == "__main__":
    main()
