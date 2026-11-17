#!/usr/bin/env python3
"""
fuel_coach.py — price driving habits in $/yr for YOUR car, mileage, and gas price.

Subcommands:
  audit      ranked $/yr price of each habit (the main tool)
  floor      physics floor: idealized min gallons/100mi for your car
  trip       speed trade-off in $ AND minutes
  diagnose   route a sustained MPG drop

Stdlib only. Figures are engineering bands, not gospel; see SKILL.md sources.
"""
import argparse
import math
import sys

# Habit -> (label, consumption penalty range as fraction, applies-to note)
HABITS = {
    "aggressive":   ("Aggressive driving (jack-rabbit + hard braking)", (0.10, 0.40), "city-weighted; DOE range"),
    "speed":        ("Highway 75 instead of 65 mph",                   (0.08, 0.15), "aero v^3"),
    "roofbox":      ("Roof box/cargo box mounted (unused)",            (0.10, 0.25), "highway-weighted"),
    "rorack":       ("Bike/trike rack on hitch (unused)",              (0.05, 0.12), "highway"),
    "idle":         ("Idling 10 min/day (warm-ups, drive-throughs)",   (0.03, 0.06), "~0.3-0.6 gal/h x 61 h/yr"),
    "tires":        ("Tires 8 psi under placard",                      (0.03, 0.04), "+0.4%/psi"),
    "coldstarts":   ("3 cold errand runs instead of 1 warm loop",      (0.04, 0.08), "short-trip drivers"),
    "trunk":        ("100 lb of trunk junk",                           (0.01, 0.02), "rolling resistance"),
    "ac":           ("AC always-on vs windows <45 mph",                (0.02, 0.06), "climate-dependent"),
    "windows":      ("Windows open at 70+ mph instead of AC",          (0.02, 0.05), "aero"),
    "premium":      ("Premium fuel in a regular-rated car",            (0.00, 0.00), "$0.20-0.60/gal pure waste"),
    "lowrollback":  ("Aging/low-rolling-resistance-lost tires (worn tread is fine)", (0.01, 0.03), "tire class"),
}

DIAGNOSE = [
    ("Tires 5+ psi low", "free", "Seasonal temp drop alone = 2-4 psi. Check cold, at the pump, monthly."),
    ("Season/route change", "free", "Winter blend + warm-up = 8-12% lower is NORMAL. Log 3 tanks."),
    ("Dragging brake / stuck caliper", "$250-450", "Wheel hub hot after a gentle drive = smoking gun."),
    ("Air filter severely clogged", "$20-40", "Mostly hurts acceleration; MPG effect on old cars."),
    ("Oxygen sensor aging", "$150-350", "Lazy sensor skews mixture: classic gradual 10-15% loss."),
    ("Thermostat stuck open", "$80-200", "Engine never fully warms, runs rich forever."),
    ("Misfire / plug / coil", "$100-400", "Rough idle; check-engine usually on by now."),
    ("Fuel leak or theft", "varies", "Do math per tank with notes, not per mood."),
]


def cmd_audit(args):
    gallons_yr = args.miles / args.mpg
    base_cost = gallons_yr * args.price
    print(f"\n  YOUR BASELINE: {args.miles:.0f} mi/yr @ {args.mpg} MPG, ${args.price}/gal")
    print(f"  = {gallons_yr:.0f} gal = ${base_cost:.0f}/yr on fuel\n")
    chosen = args.habits.split(",") if args.habits else list(HABITS)
    rows = []
    for key in chosen:
        key = key.strip().lower()
        if key not in HABITS:
            close = [k for k in HABITS if k.startswith(key[:4])]
            if not close:
                print(f"  !! unknown habit '{key}' (see keys in output below)"); continue
            key = close[0]
        label, (lo, hi), note = HABITS[key]
        if key == "premium":
            waste = gallons_yr * 0.40  # midband $0.40/gal premium delta
            rows.append((waste, f"{label:<52} ${waste:>6.0f}/yr   ({note}; priced as $0.40/gal delta)"))
            continue
        # highway-weighted habits only burn on a highway share of miles
        hw = args.hw_share if key in ("speed", "roofbox", "rorack", "windows") else 1.0
        lo_cost = base_cost * lo * hw
        hi_cost = base_cost * hi * hw
        rows.append(((lo_cost+hi_cost)/2,
                     f"{label:<52} ${lo_cost:>6.0f}-${hi_cost:.0f}/yr  ({note})"))
    rows.sort(key=lambda r: -r[0])
    print(f"  {'HABIT (what it costs you, per year)':<70}")
    print("  " + "-" * 78)
    for _, line in rows:
        print("  " + line)
    total_lo = sum(r[0] for r in rows) * 0  # don't double count; show top-3 potential
    top3 = rows[:3]
    print("  " + "-" * 78)
    print(f"  Top-3 realistic capture: ${sum(r[0] for r in top3):.0f}/yr (midband, not additive gospel)")
    print("  Fix leaks before spigots: tire pressure is free; additives do nothing.")
    return 0


def cmd_floor(args):
    # Highway-cycle idealized floor: aero + rolling at 65 mph, 22% tank-to-wheel
    m_kg = args.weight_lb * 0.4536
    cd_a = args.cd * args.frontal          # frontal area in m^2 (~2.2 sedan, ~3.0 SUV)
    rho = 1.2
    v = 65 * 0.44704
    aero_w = 0.5 * rho * cd_a * v ** 3
    crr = 0.010
    roll_w = crr * m_kg * 9.81 * v
    wheel_w = aero_w + roll_w
    fuel_w = wheel_w / 0.22
    # energy per 100 mi at steady 65 mph: (kW) * (hours per 100 mi) / (33.7 kWh per gal)
    hours_per_100mi = 100 / 65
    gal_100mi = (fuel_w / 1000 / 33.7) * hours_per_100mi
    mpg_floor = 100 / gal_100mi
    print(f"\n  PHYSICS FLOOR @ 65 mph steady (22% tank-to-wheel)")
    print(f"  Aero power:   {aero_w/1000:.1f} kW   Rolling: {roll_w/1000:.1f} kW")
    print(f"  Idealized min consumption: {gal_100mi:.2f} gal/100 mi = {mpg_floor:.0f} MPG")
    print(f"  Your actual:  {args.mpg} MPG -> {100/args.mpg:.2f} gal/100 mi")
    print("  (compare against your STEADY-HIGHWAY MPG, not combined, for apples-to-apples)")
    ratio = (100/args.mpg) / gal_100mi
    print(f"  You run {ratio:.1f}x above the steady-65 floor.")
    print("  Steady 65 mph driving sits near the floor by definition — that's why highway")
    print("  has little habit headroom. City stops, cold starts and speed are the levers.")
    print("  >1.5-2x on HIGHWAY numbers points at maintenance (tires, brakes, sensors).")
    return 0


def cmd_trip(args):
    # fuel multiplier = (1 + aero_share*((v2/v1)^3 - 1)) / eff_gain
    # aero ~60% of power at 65; higher load = slightly better engine efficiency
    a, b = args.speed_a, args.speed_b
    aero_share, eff_gain = 0.60, 1.08
    mult = (1 + aero_share * ((b / a) ** 3 - 1)) / eff_gain
    t_a = args.miles / a * 60
    t_b = args.miles / b * 60
    g_a = args.miles / args.mpg_high
    g_b = args.miles / (args.mpg_high / mult)
    print(f"\n  TRIP: {args.miles:.0f} mi, highway {args.mpg_high} MPG @ {a} mph")
    print(f"  {a} mph: {t_a:.0f} min, {g_a:.1f} gal (${g_a*args.price:.2f})")
    print(f"  {b} mph: {t_b:.0f} min, {g_b:.1f} gal (${g_b*args.price:.2f})")
    print(f"\n  Driving {b} costs ${g_b*args.price - g_a*args.price:.2f} and saves {t_a-t_b:.0f} minutes")
    per_hr = (g_b*args.price - g_a*args.price) / max((t_a-t_b)/60, 1e-9)
    print(f"  = paying ${per_hr:.2f}/hour to go faster on this trip")
    if args.per_year:
        print(f"  x {args.per_year} trips/yr = ${(g_b-g_a)*args.price*args.per_year:.0f}/yr")
    return 0


def cmd_diagnose(args):
    drop = (args.was - args.now) / args.was * 100
    print(f"\n  DROP: {args.was} -> {args.now} MPG = -{drop:.1f}%")
    if drop < 10:
        print("  Under 10%: within noise/season band. Log 3 tanks before parts.")
    band = "moderate" if drop < 15 else "large"
    print(f"  A sustained {band} drop routes to (likelihood x cheapness order):\n")
    for i, (cause, cost, note) in enumerate(DIAGNOSE, 1):
        print(f"  [{i}] {cause:<28} (~{cost})")
        print(f"      {note}")
    print("\n  Free checks first: tire psi cold, 3-tank log, wheel-hub heat after gentle drive.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Fuel habit pricing")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("audit")
    p.add_argument("--mpg", type=float, default=30)
    p.add_argument("--price", type=float, default=3.50)
    p.add_argument("--miles", type=float, default=15000)
    p.add_argument("--hw-share", type=float, default=0.5, help="highway share 0-1")
    p.add_argument("--habits", help="comma list to price (default all)")
    p.set_defaults(fn=cmd_audit)
    p = sub.add_parser("floor")
    p.add_argument("--weight-lb", type=float, default=3400)
    p.add_argument("--cd", type=float, default=0.30)
    p.add_argument("--frontal", type=float, default=2.2, help="frontal area m^2 (sedan ~2.2, SUV ~3.0)")
    p.add_argument("--mpg", type=float, default=30)
    p.set_defaults(fn=cmd_floor)
    p = sub.add_parser("trip")
    p.add_argument("--miles", type=float, default=400)
    p.add_argument("--mpg-high", type=float, default=34)
    p.add_argument("--speed-a", type=float, default=65)
    p.add_argument("--speed-b", type=float, default=75)
    p.add_argument("--price", type=float, default=3.50)
    p.add_argument("--per-year", type=float)
    p.set_defaults(fn=cmd_trip)
    p = sub.add_parser("diagnose")
    p.add_argument("--was", type=float, required=True)
    p.add_argument("--now", type=float, required=True)
    p.set_defaults(fn=cmd_diagnose)
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); sys.exit(1)
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
