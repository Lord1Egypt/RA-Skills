#!/usr/bin/env python3
"""bike_cadence.py — bike maintenance scheduler, wear-budget calculator,
and symptom diagnostician (stdlib only).

Subcommands:
  schedule  dated per-component service calendar from YOUR km + conditions
  budget    annual wear-parts cost from lifetime table x your riding
  diagnose  symptom -> ordered check sequence (diagnose before buying)
"""
import argparse
import sys
from datetime import date, timedelta

# component: (lifetime_km good conditions, interval_floor_days, mid_price_usd, task)
PARTS = {
    "chain":          dict(km=4000, price=35,  task="measure wear (0.75% = replace); lube is weekly, not here"),
    "cassette":       dict(km=10000, price=60, task="inspect teeth hooks; replace with 2nd+ worn chain"),
    "chainrings":     dict(km=14000, price=60, task="shark-fin tooth check"),
    "pads-rim":       dict(km=3000, price=12,  task="wear-line visual"),
    "pads-disc":      dict(km=3500, price=20,  task="pad material >=0.5mm above backing; rotors at min stamp"),
    "cables":         dict(km=None, price=20,  task="replace cables+housing as a pair", days=365),
    "tires":          dict(km=5000, price=40,  task="tread squaring, cuts, casing threads"),
    "bb":             dict(km=8000, price=35,  task="creak under load / side-play test"),
    "bearings-wheels":dict(km=8000, price=25,  task="spin + rock test; regrease/replace"),
    "headset":        dict(km=None, price=25,  task="index creak / notchy steer; regrease", days=540),
    "tubeless-sealant":dict(km=None, price=10, task="top up sealant (it dries in 2-4 months)", days=90),
}
COND = {"dry": 1.0, "mixed": 0.8, "wet": 0.6, "winter-salted": 0.5}
STORAGE = {"inside": 1.1, "shed": 0.95, "outside": 0.8}
SUSP_HR = 50  # hrs lower-leg service

SYMPTOMS = {
    "skip-under-load": [
        "1. chain wear gauge: >=0.75% -> replace chain, then re-test",
        "2. skip persists same 2-3 cogs with NEW chain -> cassette is worn to old chain",
        "3. backpedal slowly: DER cage jump = stiff link -> flex it by hand",
        "4. skips only at cassette extremes -> B-gap / limit screws",
    ],
    "creak": [
        "1. chainring bolts cross-pattern tight (most common, free)",
        "2. swap pedals and ride -> gone = pedal bearings",
        "3. creak under SEATED load only -> BB cups torque / cartridge",
        "4. seatpost: remove, grease (alu) or carbon paste, re-torque",
        "5. creak when steering -> headset bearings",
        "6. der hanger, bottle cage, rack bolts — seriously, check these",
    ],
    "disc-rub": [
        "1. center caliper: loosen bolts, squeeze lever HARD, retighten while held",
        "2. rotor runout >0.3mm -> true it (careful, adjustable wrench)",
        "3. stuck piston: push both back with plastic lever, pump evenly",
        "4. rotor bent in transport -> often replace rather than true",
    ],
    "spongy-lever": [
        "1. bleed (brand kit; dark old fluid = plan yearly bleeds)",
        "2. glazed pads: flat-sand lightly, isopropyl clean — NO oils near rotors",
        "3. lever reach/contacts adjust after bleed, not to mask sponginess",
    ],
    "ghost-shift": [
        "1. cassette lockring tight?",
        "2. DER hanger alignment (the sacrificial $15 part) — gauge or shop",
        "3. re-index: barrel adjuster 1/4 turns under load, all cogs",
        "4. cable fray at shifter/DER bend points",
    ],
    "thump-per-revolution": [
        "1. tire bead seated evenly? valve not cockeyed",
        "2. spoke tension ping test; loose nipple at the thump sector",
        "3. hub bearing play -> cone adjust or cartridge replace",
    ],
}

def cmd_schedule(a):
    mult = COND[a.conditions] * STORAGE[a.storage]
    km_year = a.km_week * 52
    print(f"Riding {a.km_week} km/wk ({km_year:.0f} km/yr) | conditions {a.conditions} "
          f"(x{COND[a.conditions]:.2f}) | storage {a.storage} (x{STORAGE[a.storage]:.2f})")
    print(f"Effective lifetimes below assume discipline (wipe-lube weekly, no pressure washer)\n")
    base = date.fromisoformat(a.last_service) if a.last_service else date.today()
    rows = []
    for name, p in PARTS.items():
        eff_km = p["km"] * mult if p["km"] else None
        days = p.get("days")
        if eff_km:
            due_km = eff_km
            due_days = max(7, int(due_km / max(a.km_week, 1)))
        elif days:
            due_days = int(days * (0.8 if a.conditions in ("wet", "winter-salted") else 1.0))
        else:
            continue
        due = base + timedelta(days=due_days)
        rows.append((due, name, p))
    rows.sort()
    print(f"{'due':12} {'component':16} {'every':>10}  task")
    for due, name, p in rows:
        eff_km = p["km"] * mult if p["km"] else None
        every = f"{eff_km:.0f} km" if eff_km else f"{p.get('days')} d"
        print(f"{due.isoformat():12} {name:16} {every:>10}  {p['task']}")
    print("\nWeekly regardless: chain wipe+ lube, rotor/rim wipe, tire cut scan, pad glance, lights.")
    if a.suspension:
        hrs = a.km_week / 20.0 * 1.0  # ~20 km/h moving avg
        days50 = int(SUSP_HR / max(hrs, 0.1) * 7)
        print(f"Suspension: ~{hrs:.1f} hr/wk riding -> lower-leg service every ~{days50} days")
    print("\nSafety-critical first ride checks: brakes, tire pressure/bead, headset play, wheel QR/TA torque.")
    return 0

def cmd_budget(a):
    mult = COND[a.conditions] * STORAGE[a.storage]
    km_year = a.km_week * 52
    disc = "pads-disc" if a.disc else "pads-rim"
    print(f"Wear-parts budget @ {km_year:.0f} km/yr, conditions x{mult:.2f}\n")
    total = 0.0
    items = []
    for name, p in PARTS.items():
        if name in ("pads-disc", "pads-rim") and name != disc:
            continue
        if p["km"]:
            life = p["km"] * mult
            per_year = km_year / life
            cost = per_year * p["price"]
            if cost > 0.5:
                items.append((cost, name, life, per_year))
                total += cost
        else:
            per_year = 365.0 / p.get("days", 365)
            cost = per_year * p["price"]
            items.append((cost, name, None, per_year))
            total += cost
    items.sort(reverse=True)
    print(f"{'part':16} {'life':>10} {'x/yr':>6} {'$/yr':>7}")
    for cost, name, life, per_year in items:
        print(f"{name:16} {f'{life:.0f} km' if life else '-':>10} {per_year:>6.2f} {cost:>7.0f}")
    print(f"{'TOTAL':16} {'':>10} {'':>6} {total:>7.0f}")
    print("\n+ consumables: lube ~$25/yr, tubes/patches ~$15-40, degreaser $10")
    print("Chain discipline note: catching the chain at 0.75% (vs riding to 1.0%+)")
    print("typically keeps cassette+ring costs OUT of 2 of every 3 drivetrain bills.")
    return 0

def cmd_diagnose(a):
    steps = SYMPTOMS.get(a.symptom)
    if not steps:
        print(f"unknown symptom '{a.symptom}'. Known: {', '.join(SYMPTOMS)}")
        return 1
    print(f"CHECK ORDER for {a.symptom} (do these in order — stop when fixed):")
    for s in steps:
        print("  " + s)
    print("\nDoctrine: measure before buying; the cheap/free checks catch most cases.")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("schedule")
    s.add_argument("--km-week", type=float, required=True)
    s.add_argument("--conditions", choices=list(COND), default="mixed")
    s.add_argument("--storage", choices=list(STORAGE), default="inside")
    s.add_argument("--last-service", help="ISO date of last full service")
    s.add_argument("--suspension", action="store_true")
    s.set_defaults(fn=cmd_schedule)
    b = sub.add_parser("budget")
    b.add_argument("--km-week", type=float, required=True)
    b.add_argument("--conditions", choices=list(COND), default="mixed")
    b.add_argument("--storage", choices=list(STORAGE), default="inside")
    b.add_argument("--disc", action="store_true")
    b.set_defaults(fn=cmd_budget)
    d = sub.add_parser("diagnose")
    d.add_argument("--symptom", required=True)
    d.set_defaults(fn=cmd_diagnose)
    a = ap.parse_args()
    sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
