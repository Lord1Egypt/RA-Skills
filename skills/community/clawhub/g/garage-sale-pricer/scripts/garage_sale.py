#!/usr/bin/env python3
"""garage_sale.py — garage/yard sale pricing & operations engine.

Subcommands:
  price        price one item: category band x condition multiplier -> tag + floor + day ladder
  add / list   build an inventory JSON (tag sheet + leftover routing)
  plan         sale-day logistics: expected gross, change float, signs, timing
  leftovers    route unsold inventory to donate / consign / curb / keep
Categories are GARAGE-SALE bands (30-50% below online marketplace). Stdlib only.
"""
import argparse
import json
import math
from pathlib import Path

INVENTORY_DEFAULT = Path.home() / ".garage_sale_inventory.json"

# category -> (low, high) garage-sale price band in USD; pct = % of retail when retail known
CATEGORIES = {
    "furniture_upholstered": ((15, 135), 0.125),   # sofas, armchairs: 10-15% retail
    "furniture_wood":        ((20, 150), 0.25),    # dressers, tables: 20-30%
    "furniture_assembled":   ((5, 40), 0.20),      # IKEA-class: flat-pack depreciates hard
    "clothing_adult":        ((1, 10), None),
    "clothing_kids":         ((0.5, 3), None),
    "shoes":                 ((2, 15), None),
    "books_media":           ((0.5, 3), None),
    "electronics":           ((5, 120), 0.25),     # 20-30% retail
    "kitchen_appliance":     ((5, 20), 0.25),
    "kitchenware":           ((1, 10), None),
    "tools_power":           ((15, 150), 0.40),    # 30-50% retail
    "tools_hand":            ((1, 25), None),
    "lawn_garden":           ((5, 80), 0.30),
    "bike_adult":            ((20, 60), None),
    "bike_kids":             ((10, 30), None),
    "toys":                  ((1, 10), None),
    "toys_complete_sets":    ((10, 40), None),
    "baby_gear":             ((5, 60), 0.30),      # strollers, high chairs (NOT expired car seats)
    "sports":                ((5, 60), 0.25),
    "crafts_hobby":          ((2, 30), None),
    "decor_art":             ((2, 30), None),
    "linens":                ((1, 8), None),
    "games_puzzles":         ((2, 15), None),
    "exercise":              ((10, 120), 0.25),
    "office":                ((2, 40), 0.20),
    "misc":                  ((1, 15), None),
}

CONDITION = {"A": 1.3, "B": 1.0, "C": 0.7, "D": 0.4}  # like-new / good / fair / rough

NEVER_SELL = [
    "drop-side cribs (banned)", "car seats older than ~6-10 years or after ANY crash",
    "crashed bike/ski helmets", "recalled items (check recalls.gov)",
    "expired car seats / expired children's medicine",
]


def price_item(category: str, condition: str, retail: float = None):
    if category not in CATEGORIES:
        sys_exit_valid = ", ".join(sorted(CATEGORIES))
        raise SystemExit(f"unknown category '{category}'. valid: {sys_exit_valid}")
    (lo, hi), pct = CATEGORIES[category]
    mult = CONDITION.get(condition.upper())
    if mult is None:
        raise SystemExit("condition must be A (like-new), B (good), C (fair), D (rough)")
    band_lo, band_hi = lo * mult, hi * mult
    if retail and pct:
        retail_price = retail * pct * mult
        tag = round(max(min(retail_price, band_hi), band_lo))
        src = f"{int(pct*100)}% of retail ${retail:.0f} x {mult}, clamped to band"
    else:
        tag = round((band_lo + band_hi) / 2)
        src = f"band midpoint x condition {mult}"
    floor_ = round(tag * 0.6)
    return {"tag": tag, "floor": floor_, "day2": round(tag * 0.5),
            "band": (round(band_lo), round(band_hi)), "src": src}


def load_inv(p: Path):
    return json.loads(p.read_text()) if p.exists() else {"items": []}


def save_inv(p: Path, inv):
    p.write_text(json.dumps(inv, indent=2))


def cmd_price(args):
    r = price_item(args.category, args.condition, args.retail)
    print(f"{args.category} (condition {args.condition.upper()})"
          + (f", retail ${args.retail:.0f}" if args.retail else "") + ":")
    print(f"  TAG  ${r['tag']}   ({r['src']}; band ${r['band'][0]}-${r['band'][1]})")
    print(f"  negotiation floor ${r['floor']} · day-2 ${r['day2']} · last hour: fill-a-bag or donate")


def cmd_add(args):
    p = Path(args.inventory)
    inv = load_inv(p)
    r = price_item(args.category, args.condition, args.retail)
    inv["items"].append({"name": args.name, "category": args.category,
                         "condition": args.condition.upper(),
                         "tag": r["tag"], "floor": r["floor"], "day2": r["day2"]})
    save_inv(p, inv)
    print(f"{args.name}: tag ${r['tag']} (floor ${r['floor']}) -> {p}")


def cmd_list(args):
    inv = load_inv(Path(args.inventory))
    if not inv["items"]:
        print("(inventory empty — use `add`)")
        return
    total = 0
    print(f"{'ITEM':<28}{'CAT':<22}{'COND':<5}{'TAG':>5}{'DAY2':>6}")
    for it in inv["items"]:
        total += it["tag"]
        print(f"{it['name']:<28}{it['category']:<22}{it['condition']:<5}{it['tag']:>5}{it['day2']:>6}")
    print(f"\n{len(inv['items'])} items · day-1 gross potential ${total} · "
          f"realistic 50-70%: ${round(total*0.6)}")
    print("\nPRINTABLE TAGS (cut along lines):")
    for it in inv["items"]:
        bar = "-" * 26
        print(f"+{bar}+{bar}+")
        print(f"| {it['name'][:24]:<24} | ${it['tag']:<3} after noon ${it['day2']:<3} |")


def cmd_plan(args):
    gross = args.items * args.avg_price
    lo, hi = round(gross * 0.5), round(gross * 0.7)
    ones = max(30, round(gross * 0.09))
    fives = max(20, round(gross * 0.045))
    tens = max(20, round(gross * 0.07))
    float_total = ones + fives + tens + 10 + 20  # + quarter roll + $20 buffer
    print(f"SCALE: ~{args.items} items @ avg ${args.avg_price} tag")
    print(f"EXPECTED GROSS: ${lo}-${hi} (50-70% of tag total; best 90 min = ~40% of it)")
    print(f"CHANGE FLOAT (get FRIDAY at the bank): ${float_total}")
    print(f"  ${ones} in $1s · ${fives} in $5s · ${tens} in $10s · 1 quarter roll ($10) · 1x $20 buffer")
    print("\nSIGNAGE: 3-4 signs at major intersections + 1-2 per turn into your street;")
    print("  balloon or flag on each; ADDRESS + STREET + 'SAT 7-2' in 8-inch letters;")
    print("  CHECK CITY ORDINANCE first (some ban utility-pole signs entirely; HOA notice windows).")
    print("\nTIMING: Sat 7:00 AM start (pro buyers 7-8:30 = 40% of revenue); close 1-2 PM;")
    print("  multi-family or community sale weekends multiply traffic 2-3x.")
    print("\nDISPLAY: everything visible at waist height, nothing in boxes to dig;")
    print("  clothes on a rack (not a pile) = 2x price power; power strip out to demo electronics;")
    print("  free pile at the curb as bait; Venmo/Zelle QR taped to every table.")
    print("\nNEVER SELL: " + "; ".join(NEVER_SELL) + ".")


def cmd_leftovers(args):
    inv = load_inv(Path(args.inventory))
    if not inv["items"]:
        raise SystemExit("inventory empty")
    routes = {"donate": [], "consign": [], "curb": [], "keep": []}
    for it in inv["items"]:
        cat = it["category"]
        if it["tag"] >= 50 and cat in ("furniture_wood", "furniture_upholstered", "tools_power",
                                       "exercise", "electronics", "baby_gear", "sports"):
            routes["consign"].append(f"{it['name']} (${it['tag']})")
        elif it["tag"] <= 3 or cat in ("clothing_adult", "clothing_kids", "books_media",
                                       "linens", "kitchenware", "toys"):
            routes["donate"].append(f"{it['name']} (${it['tag']})")
        elif it["tag"] <= 10:
            routes["curb"].append(f"{it['name']} (${it['tag']}) — curb-alert 'free at 4 PM'")
        else:
            routes["keep"].append(f"{it['name']} (${it['tag']}) -> re-list marketplace")
    for r, items in routes.items():
        if items:
            print(f"{r.upper()} ({len(items)}):")
            for i in items[:12]:
                print(f"   {i}")
            if len(items) > 12:
                print(f"   ... +{len(items)-12} more")
    print("\nDonate pickup should be SCHEDULED before the sale (Saturday 4-6 PM window) —")
    print("leftovers in the garage next month is how sales become storage.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", default=str(INVENTORY_DEFAULT))
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("price")
    pr.add_argument("--category", required=True)
    pr.add_argument("--condition", required=True, choices=list(CONDITION))
    pr.add_argument("--retail", type=float)
    pr.set_defaults(fn=cmd_price)
    ad = sub.add_parser("add")
    ad.add_argument("--name", required=True)
    ad.add_argument("--category", required=True)
    ad.add_argument("--condition", required=True, choices=list(CONDITION))
    ad.add_argument("--retail", type=float)
    ad.set_defaults(fn=cmd_add)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    pl = sub.add_parser("plan")
    pl.add_argument("--items", type=int, required=True)
    pl.add_argument("--avg-price", type=float, required=True)
    pl.set_defaults(fn=cmd_plan)
    sub.add_parser("leftovers").set_defaults(fn=cmd_leftovers)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
