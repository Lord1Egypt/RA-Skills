#!/usr/bin/env python3
"""first-aid-kit-auditor: inventory, gap, and expiry engine for home first-aid kits.

Pure-stdlib. Maintains a kit registry (JSON), audits it against household profile
(people, kids, activities, conditions, pets), flags missing items and expired /
soon-expiring items, sizes a kit from headcount + adventure level, and prints a
shopping/action list.

Usage:
  python3 first_aid_auditor.py init --people 4 --kids 2 --pets 1 --adventure medium
  python3 first_aid_auditor.py add --item "adhesive bandages" --qty 50 --expires 2027-06-01
  python3 first_aid_auditor.py audit            # gaps + expiry + coverage verdict
  python3 first_aid_auditor.py shop             # prioritized shopping list
  python3 first_aid_auditor.py list             # current inventory
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

TODAY = dt.date.today()
DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit.json")

# ---------------------------------------------------------------- catalog
# category -> {item: (baseline_qty_for_4_person_household, shelf_years, tags)}
# tags drive household-specific requirements: kids, pets, adventure, car, meds

CATALOG = {
    "wound care": {
        "adhesive bandages (assorted)": (50, 4.0, []),
        "sterile gauze pads 4x4in":      (10, 4.0, []),
        "rolled gauze":                  (2, 4.0, []),
        "medical tape":                  (2, 4.0, []),
        "self-adherent wrap (co-flex)":  (2, 4.0, ["adventure"]),
        "triangle bandage/sling":        (2, 4.0, ["adventure"]),
        "antiseptic wipes":              (20, 3.0, []),
        "antibiotic ointment":           (2, 3.0, []),
        "hydrogel burn dressing":        (1, 4.0, []),
        "sterile saline rinse 15ml":     (4, 3.0, []),
        "tweezers (splinter)":           (1, 99.0, []),
        "finger splint":                 (2, 99.0, ["adventure"]),
        "SAM splint":                    (1, 99.0, ["adventure"]),
        "hemostatic gauze":              (1, 4.0, ["adventure"]),
        "nitrile gloves":                (6, 4.0, []),
        "cpr pocket mask":               (1, 5.0, ["adventure"]),
        "instant cold pack":             (2, 3.0, []),
        "eye wash cup / saline":         (1, 3.0, []),
    },
    "medications": {
        "acetaminophen (adult)":         (1, 3.0, []),
        "ibuprofen (adult)":             (1, 3.0, []),
        "children's acetaminophen":      (1, 2.0, ["kids"]),
        "children's ibuprofen":          (1, 2.0, ["kids"]),
        "children's antihistamine (diphenhydramine)": (1, 2.0, ["kids"]),
        "adult antihistamine":           (1, 3.0, []),
        "anti-diarrheal (loperamide)":   (1, 3.0, []),
        "oral rehydration salts":        (4, 3.0, []),
        "hydrocortisone 1% cream":       (1, 3.0, []),
        "burn gel":                      (1, 3.0, []),
        "aspirin 325mg (chest pain)":    (1, 3.0, []),
        "epinephrine auto-injector (Rx)": (1, 1.5, ["allergy"]),
        "inhaler (Rx, if asthmatic)":    (1, 1.5, ["asthma"]),
        "nasal decongestant":            (1, 3.0, []),
        "anti-nausea (dimenhydrinate)":  (1, 3.0, []),
    },
    "tools & info": {
        "scissors (trauma)":             (1, 99.0, []),
        "digital thermometer":           (1, 99.0, []),
        "instant-read temple thermometer": (0, 99.0, ["kids"]),
        "blanket (emergency mylar)":     (1, 99.0, ["adventure", "car"]),
        "penlight":                      (1, 99.0, []),
        "notepad + pencil":              (1, 99.0, []),
        "emergency contact card":        (1, 99.0, []),
        "first-aid handbook":            (1, 99.0, []),
        "glucose gel/tablets":           (1, 3.0, ["diabetes"]),
        "tourniquet (CAT-style)":        (1, 5.0, ["adventure"]),
        "backboard-free " + "space blanket": (1, 99.0, ["adventure"]),
    },
    "meds for pets (ask vet)": {
        "pet antihistamine (vet-dosed)": (1, 2.0, ["pets"]),
        "muzzle/soft cone":              (1, 99.0, ["pets"]),
        "vet wrap":                      (2, 4.0, ["pets"]),
        "styptic powder (nails)":        (1, 3.0, ["pets"]),
        "pet carrier strap":             (1, 99.0, ["pets"]),
    },
}

# Everything that should ALSO live in the car kit
CAR_EXTRA = ["emergency mylar blanket", "flashlight + batteries", "road flare/reflective triangle",
             "seat-belt cutter / window punch", "water bottles", "granola bars"]

EXPIRY_WARN_DAYS = 180  # flag items expiring within 6 months


def norm(s: str) -> str:
    return " ".join(s.lower().split())


def load_db(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"profile": {}, "inventory": []}


def save_db(db: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def catalog_index() -> dict[str, tuple[str, int, float, list]]:
    """item -> (category, baseline_qty, shelf_years, tags)"""
    idx = {}
    for cat, items in CATALOG.items():
        for item, (qty, yrs, tags) in items.items():
            idx[norm(item)] = (cat, qty, yrs, tags)
    return idx


def required_items(profile: dict) -> dict[str, tuple[int, str]]:
    """item -> (required_qty, reason) for this household."""
    people = profile.get("people", 4)
    kids = profile.get("kids", 0)
    scale = max(1.0, people / 4)          # scale baseline from 4-person household
    adv = profile.get("adventure", "low")
    tags = set()
    if kids:
        tags.add("kids")
    if profile.get("pets"):
        tags.add("pets")
    if adv in ("medium", "high"):
        tags.add("adventure")
    for cond in profile.get("conditions", []):
        tags.add(cond)                    # allergy, asthma, diabetes

    need = {}
    for item, (cat, qty, yrs, itags) in catalog_index().items():
        if qty == 0:
            continue                      # 0-baseline = tag-only item
        required = qty if not itags else qty
        reason = cat
        if itags and not (set(itags) & tags):
            continue                      # not applicable to this household
        if itags:
            reason = f"{cat} ({'/'.join(sorted(set(itags) & tags))} profile)"
        need[item] = (max(1, int(round(qty * (scale if not itags else 1)))),
                      reason)
    return need


# ---------------------------------------------------------------- commands

def cmd_init(args, db):
    db["profile"] = {
        "people": args.people, "kids": args.kids, "pets": args.pets,
        "adventure": args.adventure, "conditions": args.conditions or [],
    }
    save_db(db, args.db)
    p = db["profile"]
    print(f"Kit profile initialized: {p['people']} people ({p['kids']} kids), "
          f"{p['pets']} pets, adventure={p['adventure']}"
          + (f", conditions={p['conditions']}" if p["conditions"] else ""))
    print(f"Registry: {args.db}")
    print("Next: `add` what you already own (with expiry for meds), then `audit`.")


def cmd_add(args, db):
    entry = {"item": norm(args.item), "qty": args.qty, "expires": args.expires,
             "note": args.note or ""}
    db["inventory"].append(entry)
    save_db(db, args.db)
    exp = f", expires {entry['expires']}" if entry["expires"] else ""
    print(f"Added: {entry['item']} x{entry['qty']}{exp}")


def cmd_list(args, db):
    if not db["inventory"]:
        print("Inventory empty. Use `add` to register items.")
        return
    print(f"{'ITEM':44} {'QTY':>4}  EXPIRES        STATUS")
    idx = catalog_index()
    for e in sorted(db["inventory"], key=lambda x: x["item"]):
        item, qty, exp = e["item"], e["qty"], e["expires"]
        status = "ok"
        if exp:
            try:
                d = dt.date.fromisoformat(exp)
                if d < TODAY:
                    status = "EXPIRED"
                elif (d - TODAY).days <= EXPIRY_WARN_DAYS:
                    status = f"expiring in {(d - TODAY).days}d"
            except ValueError:
                status = "bad-date"
        known = "ok" if item in idx else "off-catalog"
        print(f"{item[:44]:44} {qty:>4}  {exp or '-':14} {status} {known if known != 'ok' else ''}")
    print(f"\nProfile: {json.dumps(db.get('profile', {}))}")


def cmd_audit(args, db):
    profile = db.get("profile") or {}
    if not profile:
        print("No profile. Run `init` first (e.g. init --people 4 --kids 2 --adventure medium).")
        return 1
    need = required_items(profile)
    have = {}
    for e in db["inventory"]:
        have[e["item"]] = have.get(e["item"], 0) + e["qty"]

    missing, short, expired, expiring = [], [], [], []
    for item, (rq, reason) in sorted(need.items()):
        hq = have.get(item, 0)
        if hq == 0:
            missing.append((item, rq, reason))
        elif hq < rq:
            short.append((item, hq, rq, reason))
    for e in db["inventory"]:
        exp = e.get("expires")
        if not exp:
            continue
        try:
            d = dt.date.fromisoformat(exp)
        except ValueError:
            continue
        if d < TODAY:
            expired.append((e["item"], exp))
        elif (d - TODAY).days <= EXPIRY_WARN_DAYS:
            expiring.append((e["item"], exp, (d - TODAY).days))

    total = len(need)
    cov = (total - len(missing) - len(short)) / total * 100 if total else 0

    print("=" * 64)
    print("FIRST-AID KIT AUDIT")
    print("=" * 64)
    print(f"Profile: {profile['people']} people ({profile['kids']} kids), "
          f"pets={profile['pets']}, adventure={profile['adventure']}"
          + (f", conditions={profile['conditions']}" if profile.get("conditions") else ""))
    print(f"Catalog requirements for this household: {total} items")
    print(f"Coverage: {cov:.0f}%  ({total - len(missing) - len(short)}/{total})")
    print()
    if expired:
        print("EXPIRED — replace now:")
        for item, exp in expired:
            print(f"  ! {item} (expired {exp})")
        print()
    if expiring:
        print(f"Expiring within {EXPIRY_WARN_DAYS // 30} months — buy on next shop:")
        for item, exp, days in expiring:
            print(f"  ~ {item} ({exp}, {days}d)")
        print()
    if missing:
        print("MISSING — core gaps:")
        for item, rq, reason in missing:
            print(f"  - {item}  (need {rq})  [{reason}]")
        print()
    if short:
        print("LOW STOCK:")
        for item, hq, rq, reason in short:
            print(f"  - {item}  have {hq}/{rq}  [{reason}]")
        print()
    if profile.get("car") is not None or args.car:
        print("CAR KIT EXTRAS (keep a duplicate kit in the car):")
        for c in CAR_EXTRA:
            print(f"  - {c}")
        print()

    # verdict
    if cov >= 90 and not expired:
        v = "READY — well-stocked for this household."
    elif cov >= 70:
        v = "ADEQUATE for minor injuries; close the gaps listed above."
    elif cov >= 40:
        v = "THIN — you are not equipped for anything beyond a scraped knee."
    else:
        v = "CRITICAL — this is not a first-aid kit yet."
    if expired and "CRITICAL" not in v and "THIN" not in v:
        v += f" But {len(expired)} item(s) EXPIRED — replace before relying on it."
    print(f"VERDICT: {v}")
    if profile.get("kids"):
        print("Kids in house: syrup medications MUST be children's formulations;")
        print("never adult pills split. Check doses by weight, not age alone.")
    print("\nEducation beats contents: a first-aid/CPR course is the best kit item.")
    return 0


def cmd_shop(args, db):
    """Priority shopping list from audit gaps."""
    profile = db.get("profile") or {}
    need = required_items(profile)
    have = {}
    for e in db["inventory"]:
        have[e["item"]] = have.get(e["item"], 0) + e["qty"]
    rows = []
    for item, (rq, reason) in sorted(need.items()):
        hq = have.get(item, 0)
        if hq < rq:
            rows.append((item, rq - hq, reason))
    for e in db["inventory"]:
        exp = e.get("expires")
        if exp:
            try:
                if dt.date.fromisoformat(exp) < TODAY:
                    rows.append((e["item"] + " [REPLACE-EXPIRED]", e["qty"], "expired"))
            except ValueError:
                pass
    if not rows:
        print("Nothing to buy — kit meets catalog for this household. Re-audit yearly.")
        return
    print("SHOPPING LIST (priority: expired > missing core > low stock):")
    for item, q, reason in rows:
        print(f"  [ ] {item} x{q}  ({reason})")
    print(f"\n{len(rows)} line items. Store everything in one sealed, labeled box;")
    print("keep it above child reach and below 25C (car kits degrade fast in heat).")


def main(argv=None):
    p = argparse.ArgumentParser(description="First-aid kit inventory/gap/expiry auditor")
    p.add_argument("--db", default=DEFAULT_DB, help=f"kit registry JSON (default {DEFAULT_DB})")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="set household profile")
    sp.add_argument("--people", type=int, default=4)
    s = sub.add_parser("audit", help="gaps + expiry + coverage verdict")
    s.add_argument("--car", action="store_true", help="include car-kit extras")
    sub.add_parser("shop", help="prioritized shopping list")
    sub.add_parser("list", help="show current inventory")

    sp.add_argument("--kids", type=int, default=0)
    sp.add_argument("--pets", type=int, default=0)
    sp.add_argument("--adventure", choices=["low", "medium", "high"], default="low")
    sp.add_argument("--conditions", nargs="*", default=[],
                    help="allergy asthma diabetes (drives Rx items)")

    sa = sub.add_parser("add", help="register an item you own")
    sa.add_argument("--item", required=True)
    sa.add_argument("--qty", type=int, default=1)
    sa.add_argument("--expires", help="YYYY-MM-DD (meds/steriles)")
    sa.add_argument("--note", default="")

    args = p.parse_args(argv)
    db = load_db(args.db)

    if args.cmd == "init":
        cmd_init(args, db)
    elif args.cmd == "init-extra":
        pass
    elif args.cmd == "add":
        cmd_add(args, db)
    elif args.cmd == "list":
        cmd_list(args, db)
    elif args.cmd == "audit":
        sys.exit(cmd_audit(args, db) or 0)
    elif args.cmd == "shop":
        cmd_shop(args, db)
    else:
        p.error(f"unknown command {args.cmd}")


if __name__ == "__main__":
    main(sys.argv[1:])
