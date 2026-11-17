#!/usr/bin/env python3
"""Generator Sizer — appliance load sheet, surge math, generator class,
fuel plan, and safety gates for backup power during outages.

Pure stdlib. Usage examples:
    python3 generator_sizer.py --appliances fridge sump-pump furnace-blower lights-10 router --storm-hours 48
    python3 generator_sizer.py --appliances fridge well-pump --generator-watts 3500 --check-only
"""
import argparse
import json
import math
import sys

# name: (running_w, surge_mult, tier, volts, label)
CATALOG = {
    "fridge":            (200, 3.0, 1, 120, "Refrigerator 18cuft"),
    "freezer":           (200, 3.0, 1, 120, "Chest freezer"),
    "mini-fridge":       (100, 2.0, 2, 120, "Mini fridge"),
    "sump-pump":         (900, 3.0, 1, 120, "Sump pump 1/2HP"),
    "well-pump":         (1000, 3.0, 1, 240, "Well pump 1/2HP"),
    "furnace-blower":    (600, 3.0, 1, 120, "Gas furnace blower 1/2HP"),
    "pellet-stove":      (400, 1.5, 1, 120, "Pellet stove"),
    "cpap":              (100, 1.0, 1, 120, "CPAP"),
    "oxygen-concentrator": (450, 1.5, 1, 120, "Oxygen concentrator"),
    "lights-10":         (100, 1.0, 1, 120, "10x LED lights"),
    "router":            (60, 1.1, 1, 120, "Router+modem+charging"),
    "microwave":         (1200, 1.0, 2, 120, "Microwave"),
    "coffee-maker":      (1000, 1.0, 2, 120, "Coffee maker"),
    "toaster":           (1100, 1.0, 2, 120, "Toaster"),
    "tv":                (120, 1.1, 2, 120, 'TV 55"'),
    "laptop":            (65, 1.0, 2, 120, "Laptop"),
    "window-ac":         (1100, 3.0, 2, 120, "Window AC 10k BTU"),
    "box-fan":           (100, 2.0, 2, 120, "Box fan"),
    "garage-opener":     (600, 2.5, 3, 120, "Garage door opener"),
    "washer":            (1200, 2.0, 3, 120, "Washing machine"),
    "gas-dryer":         (800, 2.5, 3, 120, "Gas dryer (motor)"),
    "electric-range":    (3000, 1.0, 3, 240, "Electric range (1 burner+oven mix)"),
    "electric-dryer":    (5000, 1.0, 3, 240, "Electric dryer"),
    "water-heater":      (4500, 1.0, 3, 240, "Electric water heater"),
    "dishwasher":        (1400, 2.0, 3, 120, "Dishwasher"),
    "hair-dryer":        (1500, 1.0, 3, 120, "Hair dryer"),
    "space-heater":      (1500, 1.0, 2, 120, "Space heater 1500W"),
    "air-compressor":    (1800, 3.0, 3, 120, "Air compressor 2HP"),
    "phone-charger":     (20, 1.0, 1, 120, "Phone chargers"),
    "fish-tank":         (150, 1.5, 1, 120, "Aquarium filter+heater"),
}

CLASSES = [
    (2000,  "2,000W inverter",  1700, "fridge + lights + router + CPAP; nothing else"),
    (3500,  "3,500W portable",  3000, "+ sump OR furnace blower (staggered, not both at once)"),
    (7500,  "7,500W portable",  6000, "+ well pump, microwave, window AC — real outage kit"),
    (13500, "10-13.5kW",        11000, "most of a house minus range/dryer/water heater"),
    (22000, "22kW standby+ATS", 22000, "whole home with load-shed controller"),
]


def parse_custom(specs):
    """specs like ['microwave:1100:1.5'] -> dict entries."""
    out = {}
    for s in specs or []:
        parts = s.split(":")
        if len(parts) < 2:
            raise SystemExit(f"--custom expects name:watts[:surge]: {s}")
        name = parts[0].strip().lower().replace(" ", "-")
        watts = float(parts[1])
        surge = float(parts[2]) if len(parts) > 2 else 1.0
        out[name] = (watts, surge, 2, 120, f"{name} (custom)")
    return out


def main():
    ap = argparse.ArgumentParser(description="Backup generator sizer")
    ap.add_argument("--appliances", nargs="+", default=[],
                    help="appliance keys from the catalog (see --list)")
    ap.add_argument("--custom", nargs="*", default=[],
                    help="custom loads name:running_watts[:surge_mult]")
    ap.add_argument("--generator-watts", type=float, default=None,
                    help="your existing generator's CONTINUOUS watts, for a fit check")
    ap.add_argument("--storm-hours", type=float, default=48,
                    help="storm duration for fuel planning (default 48)")
    ap.add_argument("--fuel", choices=["gasoline", "propane"], default="gasoline")
    ap.add_argument("--elevation-ft", type=float, default=0,
                    help="site elevation; gasoline loses ~3%/1000ft")
    ap.add_argument("--load-fraction", type=float, default=None,
                    help="assumed generator load fraction 0-1 (default: computed)")
    ap.add_argument("--check-only", action="store_true",
                    help="skip class/fuel sections; just the fit check")
    ap.add_argument("--list", action="store_true", help="list catalog keys")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    catalog = dict(CATALOG)
    catalog.update(parse_custom(a.custom))

    if a.list:
        for k, v in sorted(catalog.items()):
            print(f"{k:22s} {v[0]:6.0f}W run  x{v[1]:.1f} surge  T{v[2]}  {v[4]}")
        return

    unknown = [k for k in a.appliances if k not in catalog]
    if unknown:
        print(f"ERROR: unknown appliance keys: {unknown}\nUse --list.", file=sys.stderr)
        sys.exit(2)

    loads = [(k, catalog[k]) for k in a.appliances]
    run_total = sum(w for _, (w, *_ ) in loads)
    motors = [(k, w, m) for k, (w, m, *_ ) in loads if m > 1.0]
    nonmotor = run_total - sum(w for _, w, _ in motors)
    if motors:
        big_name, big_run, big_m = max(motors, key=lambda t: t[1] * t[2])
        others_running = sum(w for _, w, _ in motors) - big_run
        worst_surge = nonmotor + big_run * big_m + others_running
    else:
        big_name, worst_surge = None, run_total

    # required continuous with 15% headroom
    req_cont = run_total * 1.15
    alt_factor = max(0.0, 1 - 0.0003 * a.elevation_ft)  # ~3%/1000ft

    # fit check vs existing generator
    verdict_lines = []
    if a.generator_watts:
        cap = a.generator_watts * alt_factor
        fits = req_cont <= cap
        verdict_lines.append(f"Your generator: {a.generator_watts:.0f}W cont "
                             f"({cap:.0f}W after elevation derate)")
        verdict_lines.append(f"Required continuous (load + 15% headroom): {req_cont:.0f}W")
        verdict_lines.append(f"FIT: {'YES — with margin' if fits else 'NO'}")
        skipped = []
        kept = loads
        if not fits:
            # greedy keep by tier then watts
            kept = sorted(loads, key=lambda kv: (kv[1][2], -kv[1][0]))
            acc = 0.0
            kept2 = []
            for k, v in kept:
                if (acc + v[0]) * 1.15 <= cap:
                    kept2.append((k, v)); acc += v[0]
                else:
                    skipped.append(k)
            kept = kept2
            verdict_lines.append(f"  Keep ({sum(v[0] for _, v in kept):.0f}W): "
                                 + ", ".join(k for k, _ in kept))
            verdict_lines.append(f"  SKIPPED by priority: {', '.join(skipped)}")

    # generator class verdict
    class_line = None
    if not a.check_only:
        need = req_cont / alt_factor if alt_factor > 0 else req_cont
        for box, label, cont, runs in CLASSES:
            if need <= cont:
                class_line = (box, label, cont, runs)
                break
        if class_line is None:
            class_line = (22000, "22kW+ standby", 22000, "whole home")

    # fuel model
    fuel_lines = []
    if not a.check_only:
        if a.load_fraction is None:
            # assume sized-to-class load: delivered kW = run_total into a class unit
            if class_line:
                g_cont = class_line[2]
                lf = min(1.0, run_total / g_cont) if g_cont else 1.0
            else:
                lf = 0.5
        else:
            lf = a.load_fraction
        delivered_kw = (a.generator_watts or (class_line[2] if class_line else 7500)) * lf / 1000.0
        if a.fuel == "gasoline":
            gph = 0.05 + 0.095 * delivered_kw
            unit = "gal gasoline"
        else:
            gph = (0.05 + 0.095 * delivered_kw) * 2.0  # ~2x volume
            unit = "gal propane"
        total = gph * a.storm_hours * 1.25
        fuel_lines.append(f"Load fraction at this plan: {lf*100:.0f}% "
                          f"({delivered_kw:.1f} kW delivered)")
        fuel_lines.append(f"Burn: {gph:.2f} {unit}/h")
        fuel_lines.append(f"{a.storm_hours:.0f}h storm + 25% reserve: {total:.1f} {unit}"
                          + ("  (20lb tank = 4.7 gal)" if a.fuel == "propane" else ""))

    # safety gates
    has240 = any(v[3] == 240 for _, v in loads)
    safety = ["CO: outdoors 20+ft from openings; battery CO alarm indoors. Never garage/porch/crawl space."]
    if has240:
        safety.append("240V LOADS PRESENT → transfer switch or listed interlock REQUIRED. NEVER backfeed an outlet.")
    if any(k in a.appliances for k in ("cpap", "oxygen-concentrator")):
        safety.append("MEDICAL LOADS → inverter-class (low THD) power recommended; verify with device maker.")

    if a.json:
        out = {
            "run_total_w": run_total, "worst_surge_w": worst_surge,
            "required_continuous_w": req_cont,
            "largest_motor": big_name,
            "generator_class": class_line[1] if class_line else None,
            "fuel": fuel_lines, "safety": safety,
            "fit": (a.generator_watts and req_cont <= a.generator_watts * alt_factor),
        }
        print(json.dumps(out, indent=2))
        return

    print("=" * 64)
    print("GENERATOR LOAD SHEET")
    print("=" * 64)
    for k, (w, m, t, v, label) in loads:
        motor = "motor" if m > 1.0 else "      "
        print(f"  T{t} {k:20s} {w:6.0f}W run  x{m:.1f} surge  [{v}V {motor}] {label}")
    print("-" * 64)
    print(f"Total running:       {run_total:7.0f} W")
    print(f"Worst surge event:   {worst_surge:7.0f} W  "
          + (f"(start of {big_name} while others run)" if big_name else "(no motors)"))
    print(f"Required continuous: {req_cont:7.0f} W  (load + 15% headroom)")
    if a.elevation_ft:
        print(f"Elevation derate:    x{alt_factor:.2f} at {a.elevation_ft:.0f} ft")
    print()
    if verdict_lines:
        print("\n".join(verdict_lines)); print()
    if class_line and not a.check_only:
        print(f"GENERATOR CLASS VERDICT: {class_line[1]}")
        print(f"  honest continuous ~{class_line[2]:,}W; class box rating {class_line[0]:,}W")
        print(f"  this class runs: {class_line[3]}")
        print()
    if fuel_lines and not a.check_only:
        print("FUEL PLAN"); print("\n".join("  " + l for l in fuel_lines)); print()
    print("SAFETY GATES")
    print("\n".join("  ! " + s for s in safety))
    print("=" * 64)


if __name__ == "__main__":
    main()
