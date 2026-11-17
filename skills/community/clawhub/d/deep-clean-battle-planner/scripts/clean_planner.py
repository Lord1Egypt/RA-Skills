#!/usr/bin/env python3
"""deep-clean-battle-planner: whole-house deep clean as a schedulable project.

Pure-stdlib. Four tools:
  plan    -- rooms + hours -> wave plan (dusty-first ordering, top-down,
           task lists per room with durations, dependency notes).
  schedule-- spread waves across available time blocks; realistic cycling
           (kitchen/bathrooms recur at high frequency, deep zones rotate).
  products-- surface x soil -> chemistry-safe cleaner table (never mixes
           bleach+acid, bleach+ammonia), DIY alternatives.
  zone    -- one-room playbook: ordered task sequence with tools and time.

Usage:
  python3 clean_planner.py plan --rooms kitchen,bathroom-main,livingroom --hours 6
  python3 clean_planner.py schedule --blocks "Sat 3h,Sun 2h,Mon 1h" \
      --rooms-list kitchen,bathroom-main,livingroom,bedroom,hallway
  python3 clean_planner.py products --surface tile-grout --soil mold
  python3 clean_planner.py zone --room kitchen
"""
from __future__ import annotations

import argparse
import sys

# room -> (base_minutes, tasks[(name, minutes)], recurrence_days, dust_priority)
ROOMS = {
    "kitchen": (90, [
        ("declutter counters + soak dishes", 10),
        ("cabinets fronts + handles (top-down)", 12),
        ("stove: grates, drip pans, hood filter degrease", 20),
        ("countertops + backsplash descale", 12),
        ("sink: descale faucet, sanitize basin + drain", 10),
        ("appliance exteriors; interior microwave", 8),
        ("floor: vacuum then mop, baseboards last", 15),
        ("trash + recycling bins wash", 5),
    ], 7, 2),
    "bathroom-main": (60, [
        ("spray tub/shower cleaner, dwell 10m while you do toilet+sink", 2),
        ("toilet: bowl under-rim, seat, base, behind", 12),
        ("sink + faucet descale + mirror", 10),
        ("tub/shower scrub after dwell", 12),
        ("grout check + targeted treatment", 8),
        ("floor + behind-toilet sweep-mop", 10),
        ("towels swap + bin + switch plates", 6),
    ], 5, 3),
    "livingroom": (55, [
        ("declutter 2-bag (keep/donate)", 10),
        ("dust ceiling->shelves->furniture top-down", 12),
        ("upholstery vacuum + cushion flip/rotate", 10),
        ("electronics/screens microfiber", 8),
        ("windows interior + sills + tracks", 10),
        ("floor: vacuum edges first, then mop if hard", 5),
    ], 14, 4),
    "bedroom": (40, [
        ("strip bed; wash linens (start machine FIRST)", 5),
        ("dust top-down: headboard, nightstands, lamps", 10),
        ("under-bed vacuum + rotate mattress (quarterly)", 10),
        ("closet floor + visible surface reset", 8),
        ("floor + baseboards", 7),
    ], 14, 5),
    "hallway": (20, [
        ("walls scuff-mark pass (magic eraser)", 8),
        ("light switches, door handles sanitize", 4),
        ("floor + baseboards + corners", 8),
    ], 30, 6),
    "entry": (25, [
        ("shoe zone reset + mat wash", 8),
        ("coat rack + hooks dust", 5),
        ("door inside+outside + knob sanitize", 6),
        ("floor: vacuum + mop, corners", 6),
    ], 14, 1),
}

# surface x soil -> (cleaner, dwell, warning)
PRODUCTS = {
    ("tile-grout", "mold"):        ("chlorine bleach gel (cling gel preferred)", "15m rinse",
                                    "ventilate; NEVER mix with ammonia or acids (chloramine/chlorine gas)"),
    ("tile-grout", "soap-scum"):   ("alkaline degreaser or 1:1 vinegar+dish soap", "10m scrub",
                                    "vinegar on stone tiles etches — use pH-neutral on natural stone"),
    ("glass", "hard-water"):       ("white vinegar 1:1 or citric acid 10%", "5m wipe",
                                    "acid; rinse thoroughly; keep off marble/limestone"),
    ("hardwood", "general"):       ("pH-neutral hardwood cleaner, damp not wet", "none",
                                    "no vinegar (long-term finish damage), no steam mops"),
    ("laminate", "general"):       ("barely-damp microfiber + mild detergent", "none",
                                    "water seams swell laminate; wring mop hard"),
    ("stone-natural", "general"):  ("pH-neutral stone soap", "none",
                                    "NO vinegar/bleach/acid — etches marble/granite seal"),
    ("stainless", "fingerprints"): ("dish soap + water, dry; grain-direction rub", "none",
                                    "no bleach; no steel wool (scratches grain)"),
    ("oven", "grease-carbon"):     ("oven cleaner (sodium hydroxide)", "overnight",
                                    "caustic: gloves+goggles; ventilate; keep off self-clean ovens' elements"),
    ("carpet", "stains"):          ("extract with water first; enzyme cleaner for organic", "blot never rub", None),
    ("fabric-upholstery", "general"): ("upholstery-spec cleaner or mild detergent foam", "patch test", None),
    ("mattress", "sweat-odor"):    ("baking soda sift, vacuum after 1h; enzyme for stains", "1h", None),
    ("electronics", "dust"):       ("dry microfiber; 70% isopropyl on stubborn", "none",
                                    "device OFF; no drips into vents"),
}

DANGER_MIXES = [
    ("bleach + vinegar/acid", "chlorine gas — coughing, eye burns, hospital visits"),
    ("bleach + ammonia", "chloramine gas — toxic at kitchen concentrations"),
    ("bleach + rubbing alcohol", "chloroform-like compounds"),
    ("hydrogen peroxide + vinegar", "peracetic acid — corrosive to skin/lungs"),
    ("drain cleaner (caustic) + anything", "exothermic eruption; sequential use only with full flush between"),
]


def cmd_plan(args):
    rooms = [r.strip().lower() for r in args.rooms.split(",") if r.strip()]
    unknown = [r for r in rooms if r not in ROOMS]
    if unknown:
        print(f"Unknown rooms: {', '.join(unknown)}. Known: {', '.join(ROOMS)}")
        return 1

    print("=" * 62)
    print(f"DEEP-CLEAN BATTLE PLAN — {args.hours}h available")
    print("=" * 62)
    total = sum(ROOMS[r][0] for r in rooms)
    print(f"Full effort for {len(rooms)} rooms: {total} min ({total / 60:.1f}h)")

    # priority: dust-generating and high-traffic first (entry, kitchen, bath)
    order = sorted(rooms, key=lambda r: ROOMS[r][3])
    fitting = []
    used = 0
    for r in order:
        if used + ROOMS[r][0] <= args.hours * 60 * 0.85:  # 15% overhead buffer
            fitting.append(r)
            used += ROOMS[r][0]
    deferred = [r for r in order if r not in fitting]

    wave = 1
    for r in fitting:
        base, tasks, recur, _ = ROOMS[r]
        print(f"\n--- WAVE {wave}: {r} ({base} min) ---")
        print(f"    recurrence: every {recur} days for upkeep")
        for name, mins in tasks:
            print(f"    [{mins:2d}m] {name}")
        wave += 1
    if deferred:
        print(f"\nDEFERRED (didn't fit): {', '.join(deferred)}")
        print("Schedule separately — a rushed room is worse than a planned one.")

    print("\nORDERING RULES:")
    print("  - dustiest work FIRST (dust falls onto later work otherwise)")
    print("  - top-down inside every room: fans->shelves->surfaces->floors")
    print("  - start washer/dishwasher/oven-cleaner at T-0: machines clean")
    print("    while you do; your hands are the bottleneck, not them")
    print("  - 15% buffer is real: supplies hunt, phone distractions, dwell times")
    return 0


def cmd_schedule(args):
    blocks = []
    for b in args.blocks.split(","):
        label, hours = b.strip().rsplit(" ", 1)
        blocks.append((label, float(hours.rstrip("h"))))
    rooms = [r.strip().lower() for r in args.rooms_list.split(",") if r.strip()]
    unknown = [r for r in rooms if r not in ROOMS]
    if unknown:
        print(f"Unknown rooms: {', '.join(unknown)}. Known: {', '.join(ROOMS)}")
        return 1

    print("=" * 62)
    print("SCHEDULE — waves mapped to time blocks")
    print("=" * 62)
    order = sorted(rooms, key=lambda r: ROOMS[r][3])
    remaining = list(order)
    for label, hours in blocks:
        cap = hours * 60 * 0.85
        used, picked = 0, []
        i = 0
        while i < len(remaining):
            r = remaining[i]
            if used + ROOMS[r][0] <= cap:
                picked.append(r); used += ROOMS[r][0]; remaining.pop(i)
            else:
                i += 1
        print(f"\n{label} ({hours}h usable {cap:.0f}m):")
        if picked:
            for r in picked:
                print(f"   - {r} ({ROOMS[r][0]}m, recurs every {ROOMS[r][2]}d)")
        else:
            print("   - (no full room fits — use as catch-up/finish block)")
    if remaining:
        print(f"\nLEFT OVER (need another block): {', '.join(remaining)}")
    print("\nUPKEEP CADENCE after the deep clean:")
    for r in order:
        print(f"   {r:14} every {ROOMS[r][2]:2d} days")
    return 0


def cmd_products(args):
    key = (args.surface.lower(), args.soil.lower())
    if key not in PRODUCTS:
        print(f"No exact entry for {key}. Known surfaces: "
              f"{sorted(set(s for s, _ in PRODUCTS))}")
        print(f"Known soils: {sorted(set(s for _, s in PRODUCTS))}")
        return 1
    cleaner, dwell, warning = PRODUCTS[key]
    print("=" * 62)
    print(f"PRODUCT MATCH — {args.surface} x {args.soil}")
    print("=" * 62)
    print(f"Use: {cleaner}")
    print(f"Method/dwell: {dwell}")
    if warning:
        print(f"WARNING: {warning}")
    print("\nNEVER MIX:")
    for combo, effect in DANGER_MIXES:
        print(f"  ✗ {combo} → {effect}")
    return 0


def cmd_zone(args):
    r = args.room.lower()
    if r not in ROOMS:
        print(f"Unknown room '{r}'. Known: {', '.join(ROOMS)}")
        return 1
    base, tasks, recur, _ = ROOMS[r]
    print("=" * 62)
    print(f"ZONE PLAYBOOK — {r} ({base} min, upkeep every {recur}d)")
    print("=" * 62)
    t = 0
    for name, mins in tasks:
        t += mins
        print(f"  {t:3d}m mark ─ {name}")
    print(f"\nTools: microfiber set, scrub brush, degreaser, pH-neutral floor")
    print(f"cleaner, vacuum, mop. Dwell-spray first, scrub last.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Deep-clean battle planner")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("--rooms", required=True, help="comma-separated")
    pl.add_argument("--hours", type=float, required=True)

    sc = sub.add_parser("schedule")
    sc.add_argument("--blocks", required=True, help='e.g. "Sat 3h,Sun 2h,Mon 1h"')
    sc.add_argument("--rooms-list", required=True)

    pr = sub.add_parser("products")
    pr.add_argument("--surface", required=True)
    pr.add_argument("--soil", required=True)

    zo = sub.add_parser("zone")
    zo.add_argument("--room", required=True)

    args = p.parse_args(argv)
    return {"plan": cmd_plan, "schedule": cmd_schedule,
            "products": cmd_products, "zone": cmd_zone}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
