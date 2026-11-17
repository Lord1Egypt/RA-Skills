#!/usr/bin/env python3
"""bikeshield.py — bike theft hardening, registry, and 72-hour recovery playbook.

Subcommands:
  audit        grade a lock setup against bike value + area risk
  register add add a bike to the local registry (bikes.json)
  register photos  photo evidence checklist (by brand class serial guidance)
  register list    show registry
  stolen       print the first-72-hours recovery playbook for a registered bike
  check        used-bike purchase serial check (registry + what to look up)

Offline, stdlib only.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "bikes.json")

# ------------------------------------------------------------- lock knowledge

# name regex -> (sold-secure class, art approx, notes)
LOCK_DB = [
    (r"kryptonite\s+(new-york|fahgettaboudit|standard|evolution.*99)", "diamond",
     "Top-tier hardened shackle; resists grinders ~1 min, defeats croppers."),
    (r"hiplock\s+(d1000|pragmasis|protector)", "diamond",
     "Angle-grinder-rated class (D1000 published anti-grind laminate)."),
    (r"litelok\s+x[13]|\bx1\b", "diamond", "Anti-grind core class."),
    (r"kryptonite\s+evolution|abus\s+granit|onguard\s+(brute|pitbull)", "gold",
     "Defeats bolt croppers and hand attacks; cordless grinder cuts in 40–90 s."),
    (r"abus\s+(futura|x-plus|citychain\s*1[01])|krypto\s*new-u", "gold",
     "Gold-class chain/U."),
    (r"onguard\s+(beast|copycat)|kryptonite\s+(keeper|kryptolok)|abus\s+(buster|bordo\s*6\d)", "silver",
     "Resists opportunistic hand attacks and small croppers; not grinder-proof."),
    (r"folding\s*lock|bordo\s*6\d|compact\s*folding", "silver",
     "Folding class: mid resistance, watch the rivets vs grinders."),
    (r"\bcable\b|combination\s*lock|coil\s*lock|\bchain\s*(lock)?\b.*(8|10)\s?mm", "bronze",
     "Cables and thin chains are opportunistic-tug class ONLY."),
]

RISK_LABELS = {
    1: "rural / in-sight stops only",
    2: "residential street, low-theft suburb",
    3: "inner suburb, campus daytime parking",
    4: "dense city, transit hubs, all-day commuter parking",
    5: "major-city core / known theft district (NYC, SF, London core...)",
}

MIN_CLASS_BY_RISK_DAY = {1: "bronze", 2: "silver", 3: "silver", 4: "gold", 5: "diamond"}
MIN_CLASS_BY_RISK_NIGHT = {1: "silver", 2: "silver", 3: "gold", 4: "diamond", 5: "inside-only"}

CLASS_ORDER = ["bronze", "silver", "gold", "diamond"]

PHOTO_CHECKLIST = [
    "Drive side full bike (whole frame in frame)",
    "Non-drive side full bike",
    "Serial close-up (readable digits, note location)",
    "Drivetrain close-up (rear derailleur + cassette)",
    "Front of cockpit (stem, saddle, distinctive parts)",
    "Any distinctive scratches/stickers/dents + component swaps",
]

SERIAL_BY_BRAND = [
    (r"trek", "Bottom of the bottom bracket shell; often starts 'WTU'."),
    (r"specialized", "Front of seat tube or rear dropout; often 'WSBC' prefix."),
    (r"giant", "Under the bottom bracket shell or on the seat tube."),
    (r"cannondale", "Left rear dropout or BB shell; 'GM' prefix common."),
    (r"santa\s*cruz", "Under the BB shell or rear dropout (carbon: etched plate)."),
    (r"brompton", "Frame plate near the hinge + BB shell."),
    (r"cube|merida|scott|canyon", "BB shell underside or seat tube; Canyon under BB."),
    (r"e-?bike|bosch|shimano\s*ep", "Frame BB shell + MOTOR housing number — record BOTH."),
]
GENERIC_SERIAL = "Bottom bracket shell (flip the bike) — the generic default spot."


def classify_lock(name: str):
    low = name.lower()
    for rx, cls, note in LOCK_DB:
        if re.search(rx, low):
            return cls, note
    return "unknown", "No match — assume bronze until verified (check Sold Secure rating)."


def audit(value, risk, locks, hours_parked):
    print(f"LOCK AUDIT — bike ${value}, area risk {risk}/5 ({RISK_LABELS.get(risk, '?')})")
    if hours_parked and hours_parked >= 10:
        print(f"Parking duration: {hours_parked} h → OVERNIGHT/ALL-DAY rules apply.")
        min_cls = MIN_CLASS_BY_RISK_NIGHT.get(risk, "diamond")
    else:
        min_cls = MIN_CLASS_BY_RISK_DAY.get(risk, "gold")
    print("═" * 64)
    classes = []
    weakest = None
    for lk in locks:
        cls, note = classify_lock(lk)
        classes.append(cls)
        rank = CLASS_ORDER.index(cls) if cls in CLASS_ORDER else -1
        need = CLASS_ORDER.index(min_cls) if min_cls in CLASS_ORDER else 3
        verdict = ("OK for this spot" if rank >= need else
                   ("BORDERLINE — daylight + in-sight only" if rank == need - 1 else
                    "INSUFFICIENT for this spot"))
        print(f"[{len(classes)}] {lk} → {cls.upper()}")
        print(f"    {note}")
        print(f"    Need ≥ {min_cls.upper()} here → {verdict}")
        if cls in ("bronze", "unknown") and weakest is None:
            weakest = lk
    print("─" * 64)
    best = max((CLASS_ORDER.index(c) for c in classes if c in CLASS_ORDER), default=-1)
    need = CLASS_ORDER.index(min_cls) if min_cls in CLASS_ORDER else 3
    if not locks:
        print("VERDICT: NO LOCK LISTED — unlocked bike in risk", risk)
    elif min_cls == "inside-only":
        print("VERDICT: INSIDE-ONLY — no portable lock survives a night grinder run at risk 5.")
        print("FIX: take the bike inside; if impossible, floor-anchored chain at home + \
Diamond U everywhere else.")
    elif best >= need:
        print(f"VERDICT: {'PASS' if best == need else 'STRONG'} — primary meets the {min_cls} bar.")
        if len(locks) == 1:
            print("FIX: single lock = quick-release wheel/seatpost are the cheap wins: add \
locking skewers or a secondary mini-U.")
    else:
        print(f"VERDICT: FAIL — best lock is {CLASS_ORDER[best] if best >= 0 else 'unknown'}, \
spot needs {min_cls}.")
        print("FIX: upgrade the primary; demote the current one to wheel duty.")
    budget = value * 0.10, value * 0.15
    print(f"LOCK BUDGET doctrine: ${budget[0]:.0f}–${budget[1]:.0f}/yr-class spend \
(10–15% of value) at risk {risk}.")
    print("\nLOCKING PROTOCOL:")
    for i, step in enumerate([
        "Object test: NO to unbolt-able sign posts, scaffolding, chain-link, trees; \
YES to ground-anchored racks/hoops.",
        "Sheldon method: U through rear wheel + seat tube inside the triangle; fill the shackle.",
        "Lock high off the ground, keyway down; replace quick releases with locking skewers.",
        f"{'Overnight outside = NO. Bike goes inside.' if (hours_parked or 0) >= 10 or risk >= 4 else 'Day discipline: never leave overnight outside.'}",
    ], 1):
        print(f"  {i}. {step}")


# ------------------------------------------------------------------- registry

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_registry(reg):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)


def register(args):
    reg = load_registry()
    if args.reg_cmd == "add":
        entry = {
            "id": re.sub(r"[^a-z0-9]+", "-",
                         f"{args.make}-{args.model}".lower()).strip("-"),
            "make": args.make, "model": args.model, "year": args.year,
            "color": args.color, "value": args.value, "serial": args.serial,
            "distinctive": args.distinctive or "",
            "registered": [],
            "photos_done": False,
            "added": datetime.now().isoformat(timespec="seconds"),
        }
        reg = [b for b in reg if b["id"] != entry["id"]] + [entry]
        save_registry(reg)
        print(f"REGISTERED: {entry['id']} → {os.path.abspath(REGISTRY_PATH)}")
        print("Next: register photos | sign up on BikeIndex.org + Project 529 \
(same serial + photos).")
    elif args.reg_cmd == "photos":
        low = (args.bike or "").lower()
        brand_note = GENERIC_SERIAL
        for rx, note in SERIAL_BY_BRAND:
            if re.search(rx, low):
                brand_note = note
                break
        print(f"PHOTO EVIDENCE CHECKLIST — {args.bike or 'your bike'}")
        print(f"Serial location: {brand_note}")
        print("═" * 64)
        for i, ph in enumerate(PHOTO_CHECKLIST, 1):
            print(f"  [{i}] {ph}")
        print("Store copies: phone + cloud + this registry folder. Receipt photo too.")
    elif args.reg_cmd == "list":
        reg = load_registry()
        if not reg:
            print(f"Registry empty ({REGISTRY_PATH}). Add with `register add`.")
        for b in reg:
            print(f"  {b['id']}: serial {b['serial']} | ${b['value']} | {b['color']}"
                  f" | registered: {', '.join(b['registered']) or 'NONE — do BikeIndex + 529'}")


def stolen(bike_id, hours_ago, location):
    reg = load_registry()
    bike = next((b for b in reg if b["id"] == bike_id), None)
    if not bike:
        print(f"No registry entry '{bike_id}'. Known: {[b['id'] for b in reg] or 'none'}")
        return 1
    when = datetime.now() - timedelta(hours=hours_ago)
    print(f"STOLEN-BIKE PLAYBOOK — {bike['make']} {bike['model']} "
          f"({bike['color']}, ${bike['value']})")
    print(f"Serial: {bike['serial']}   Stolen ~{when:%Y-%m-%d %H:%M} "
          f"({hours_ago} h ago)   {location or ''}")
    print("═" * 64)
    phase = max(0, hours_ago)
    steps = [
        ("NOW — hour 0–1", [
            f"File the police report: serial {bike['serial']}, make/model/color/value. "
            "GET THE CASE NUMBER — it unlocks insurance, registry flags, takedowns.",
            "Flag STOLEN on BikeIndex + Project 529 (they push alerts to shops/police scans).",
            "Write down exact theft details: location, lock type, what was cut/left behind, "
            "CCTV doorbells facing the spot (Ring owners share clips if asked within 24 h).",
        ]),
        ("HOUR 1–24", [
            "Saved searches (40 km radius, newest-first): "
            f"'{bike['make']} {bike['model']}', '{bike['make']} bike', "
            "and bike-parts category for your wheelset/groupset.",
            f"Flyer with photo + serial + case number → bike shops, co-ops, pawn shops "
            "within 5 km. Shops check registries before buying used.",
            "Post in local cycling groups (FB/Reddit/WhatsApp) with the BikeIndex link — "
            "these groups recover more bikes than any other channel.",
        ]),
        ("DAY 1–3", [
            "Check listings DAILY: thieves repost under new accounts; stripped parts "
            "appear with generic titles.",
            "Insurance: file the claim (policy sublimit vs scheduled rider); attach case "
            "number, photos, receipt. Note the deadline in your policy (often 24–72 h).",
            "Transit lost&found + city auction lists (unclaimed 'found' bikes surface there "
            "in some cities).",
        ]),
        ("RECOVERY MEETING (if found)", [
            "Never open with 'stolen' — pose as a buyer, arrange to inspect.",
            f"Verify serial {bike['serial']} in person, photograph it, then call the "
            "non-emergency line with the case number instead of confronting.",
            "Bring a friend; meet public; don't hand over money for your own bike.",
        ]),
    ]
    for title, items in steps:
        print(f"▸ {title}")
        for it in items:
            print(f"   • {it}")
    print("─" * 64)
    if phase > 72:
        print("NOTE: theft reported >72 h old — marketplace window closing; prioritize "
              "registry scans + pawn/shop flyering + insurance.")
    print("Evidence pack for insurance: photos from registry, receipt, police case #, "
          "remaining lock parts (keep the cut lock!).")


def check(serial):
    print(f"USED-BIKE PURCHASE CHECK — serial '{serial}'")
    print("═" * 64)
    reg = load_registry()
    hit = [b for b in reg if b["serial"].lower() == serial.lower()]
    if hit:
        print("✖ MATCHES YOUR OWN REGISTRY (double-check who's selling).")
    print("Look the serial up on:")
    for name, url in [
        ("BikeIndex", "https://bikeindex.org/bikes?serial=" + serial),
        ("Project 529", "app search (529 Garage)"),
        ("Local police stolen-property / national registry where applicable", ""),
    ]:
        print(f"  • {name}" + (f" → {url}" if url else ""))
    print("Red flags in the seller: no original photos (stock/low-res only), serial "
          "photo refused, 'found it', price way under market, meetup resistance.")
    print("Also verify: frame cracks at welds/head tube, BB play, wheel true — a too-cheap "
          "bike with a sanded BB shell is a sandblasted serial. Walk away.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("audit")
    p.add_argument("--bike-value", type=float, required=True)
    p.add_argument("--area-risk", type=int, required=True, choices=range(1, 6))
    p.add_argument("--locks", required=True, help="semicolon-separated lock descriptions")
    p.add_argument("--hours-parked", type=float, default=None)

    p = sub.add_parser("register")
    rsub = p.add_subparsers(dest="reg_cmd", required=True)
    a = rsub.add_parser("add")
    a.add_argument("--make", required=True); a.add_argument("--model", required=True)
    a.add_argument("--year", type=int, default=0); a.add_argument("--color", default="")
    a.add_argument("--value", type=float, required=True)
    a.add_argument("--serial", required=True)
    a.add_argument("--distinctive", default="")
    rsub.add_parser("list")
    ph = rsub.add_parser("photos")
    ph.add_argument("--bike", default="")

    p = sub.add_parser("stolen")
    p.add_argument("--bike-id", required=True)
    p.add_argument("--hours-ago", type=float, default=1)
    p.add_argument("--location", default="")

    p = sub.add_parser("check")
    p.add_argument("--serial", required=True)

    args = ap.parse_args()
    if args.cmd == "audit":
        locks = [l.strip() for l in args.locks.split(";") if l.strip()]
        audit(args.bike_value, args.area_risk, locks, args.hours_parked)
    elif args.cmd == "register":
        register(args)
    elif args.cmd == "stolen":
        sys.exit(stolen(args.bike_id, args.hours_ago, args.location) or 0)
    elif args.cmd == "check":
        check(args.serial)


if __name__ == "__main__":
    main()
