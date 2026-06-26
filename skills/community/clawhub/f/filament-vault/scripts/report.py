#!/usr/bin/env python3
"""Generate a filament inventory spending report and low-stock alerts."""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/filament-vault")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

LOW_STOCK_DEFAULT = 100  # grams


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


def bar(fraction, width=20):
    """Simple ASCII progress bar."""
    filled = int(round(fraction * width))
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled)


def main():
    parser = argparse.ArgumentParser(description="Generate filament inventory report.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=LOW_STOCK_DEFAULT,
        help=f"Low-stock threshold in grams (default {LOW_STOCK_DEFAULT})",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")
    args = parser.parse_args()

    spools = load_inventory()

    if not spools:
        print("Inventory is empty. Add spools with add_spool.py.")
        return

    active = [s for s in spools if s.get("status") == "active"]
    finished = [s for s in spools if s.get("status") == "finished"]
    all_spools = spools

    # Totals
    total_weight_remaining = sum(s.get("weight_remaining_g", 0) for s in active)
    total_weight_initial = sum(s.get("weight_initial_g", 0) for s in all_spools)
    total_weight_used = sum(
        s.get("weight_initial_g", 0) - s.get("weight_remaining_g", 0) for s in all_spools
    )
    total_value_active = sum(
        s["cost_usd"] for s in active if s.get("cost_usd") is not None
    )
    total_spend_all = sum(
        s["cost_usd"] for s in all_spools if s.get("cost_usd") is not None
    )

    # By-material breakdown
    by_material = defaultdict(lambda: {"count": 0, "remaining_g": 0.0, "value": 0.0, "spools": []})
    for s in active:
        m = s.get("material", "unknown")
        by_material[m]["count"] += 1
        by_material[m]["remaining_g"] += s.get("weight_remaining_g", 0)
        by_material[m]["value"] += s.get("cost_usd") or 0
        by_material[m]["spools"].append(s)

    # Low-stock alerts
    low_stock = [
        s for s in active if s.get("weight_remaining_g", 0) < args.threshold
    ]

    # Monthly spending (requires added_date)
    monthly = defaultdict(float)
    for s in all_spools:
        if s.get("cost_usd") and s.get("added_date"):
            try:
                month = s["added_date"][:7]  # YYYY-MM
                monthly[month] += s["cost_usd"]
            except Exception:
                pass

    if args.json:
        report = {
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "summary": {
                "total_spools": len(all_spools),
                "active_spools": len(active),
                "finished_spools": len(finished),
                "total_weight_remaining_g": total_weight_remaining,
                "total_weight_initial_g": total_weight_initial,
                "total_weight_used_g": total_weight_used,
                "total_value_active_usd": total_value_active,
                "total_spend_all_usd": total_spend_all,
            },
            "by_material": {
                m: {
                    "count": v["count"],
                    "remaining_g": v["remaining_g"],
                    "value_usd": v["value"],
                }
                for m, v in by_material.items()
            },
            "low_stock": [
                {
                    "id": s["id"],
                    "brand": s["brand"],
                    "material": s["material"],
                    "color": s["color"],
                    "remaining_g": s["weight_remaining_g"],
                }
                for s in low_stock
            ],
            "monthly_spending": dict(sorted(monthly.items())),
        }
        print(json.dumps(report, indent=2))
        return

    # Human-readable report
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'═' * 52}")
    print(f"  🧵  Filament Vault Report  —  {now}")
    print(f"{'═' * 52}\n")

    print("SUMMARY")
    print(f"  Active spools   : {len(active)}")
    print(f"  Finished spools : {len(finished)}")
    print(f"  Weight remaining: {total_weight_remaining:.0f}g  ({total_weight_remaining/1000:.2f}kg)")
    print(f"  Weight used     : {total_weight_used:.0f}g")
    if total_value_active > 0:
        print(f"  Active inventory value: ${total_value_active:.2f}")
    if total_spend_all > 0:
        print(f"  Total all-time spend  : ${total_spend_all:.2f}")

    print("\nBY MATERIAL")
    if by_material:
        for mat in sorted(by_material.keys()):
            v = by_material[mat]
            pct = v["remaining_g"] / total_weight_remaining if total_weight_remaining > 0 else 0
            cost_str = f"  ${v['value']:.2f}" if v["value"] > 0 else ""
            print(
                f"  {mat:<8} {v['count']} spool(s)  {v['remaining_g']:.0f}g  "
                f"[{bar(pct)}]{cost_str}"
            )
    else:
        print("  No active spools.")

    if low_stock:
        print(f"\n⚠  LOW STOCK ALERTS (< {args.threshold:.0f}g)")
        for s in sorted(low_stock, key=lambda x: x.get("weight_remaining_g", 0)):
            print(
                f"  {s['brand']} {s['material']} — {s['color']}"
                f"  [{s['id'][:8]}…]  {s['weight_remaining_g']:.0f}g remaining"
            )
    else:
        print(f"\n✓ No low-stock spools (threshold: {args.threshold:.0f}g)")

    if monthly:
        print("\nMONTHLY SPENDING")
        for month in sorted(monthly.keys()):
            print(f"  {month}  ${monthly[month]:.2f}")

    print(f"\n{'═' * 52}\n")


if __name__ == "__main__":
    main()
