#!/usr/bin/env python3
"""Add a new filament spool to the inventory."""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/filament-vault")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

VALID_MATERIALS = {"PLA", "PETG", "ABS", "TPU", "Nylon", "ASA", "other"}


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def save_inventory(spools):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as f:
        json.dump(spools, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Add a new filament spool to inventory.")
    parser.add_argument("--brand", required=True, help="Brand name (e.g. Bambu, Hatchbox)")
    parser.add_argument(
        "--material",
        required=True,
        choices=sorted(VALID_MATERIALS),
        help="Filament material type",
    )
    parser.add_argument("--color", required=True, help="Color name (e.g. Matte Black)")
    parser.add_argument(
        "--weight",
        type=float,
        default=1000.0,
        help="Initial weight in grams (default: 1000)",
    )
    parser.add_argument("--cost", type=float, default=None, help="Purchase cost in USD")
    parser.add_argument("--location", default=None, help="Storage location (e.g. Shelf A)")
    parser.add_argument("--notes", default=None, help="Optional notes")

    args = parser.parse_args()

    if args.weight <= 0:
        print("Error: --weight must be greater than 0.", file=sys.stderr)
        sys.exit(1)

    if args.cost is not None and args.cost < 0:
        print("Error: --cost must be non-negative.", file=sys.stderr)
        sys.exit(1)

    spool = {
        "id": str(uuid.uuid4()),
        "brand": args.brand,
        "material": args.material,
        "color": args.color,
        "weight_initial_g": args.weight,
        "weight_remaining_g": args.weight,
        "cost_usd": args.cost,
        "location": args.location,
        "notes": args.notes,
        "status": "active",
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "finished_date": None,
    }

    spools = load_inventory()
    spools.append(spool)
    save_inventory(spools)

    print(f"✓ Added spool: {args.brand} {args.material} — {args.color}")
    print(f"  ID       : {spool['id']}")
    print(f"  Weight   : {args.weight:.0f}g")
    if args.cost is not None:
        print(f"  Cost     : ${args.cost:.2f}")
    if args.location:
        print(f"  Location : {args.location}")
    if args.notes:
        print(f"  Notes    : {args.notes}")


if __name__ == "__main__":
    main()
