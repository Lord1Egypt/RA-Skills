#!/usr/bin/env python3
"""
circuit_doctor.py — residential circuit load triage + dead-outlet diagnosis.

Subcommands:
  load        Sum appliance draw vs breaker capacity (80% continuous rule)
  dead-outlet Ranked dead-outlet diagnosis tree
  trip        Trip-pattern decoder
  db          Show the appliance database
  map         Interactive circuit-mapping session logger

Stdlib only. No warranties; safety gates live in SKILL.md — read them first.
"""
import argparse
import difflib
import json
import os
import sys
from datetime import datetime

# Input watts (what the circuit actually sees)
APPLIANCES = {
    # kitchen
    "microwave (small, 700w out)": 1000, "microwave (1000w out)": 1400,
    "microwave (1250w out)": 1600, "toaster": 1000, "toaster oven": 1400,
    "kettle": 1500, "air fryer": 1500, "instant pot (heat phase)": 1100,
    "coffee maker": 1100, "drip coffee maker": 900, "espresso machine": 1300,
    "blender (peak)": 700, "dishwasher (heat phase)": 1500, "disposal": 600,
    "slow cooker": 250, "rice cooker": 700, "electric griddle": 1200,
    "waffle iron": 1100, "electric can opener": 150,
    # heating / personal
    "space heater": 1500, "oil-filled radiator": 1500, "ceramic heater": 1500,
    "hair dryer": 1600, "hair dryer (pro 1875w)": 1875, "iron": 1400,
    "electric blanket": 250, "heated mattress pad": 100,
    "towel warmer": 150, "heat gun": 1400,
    # laundry / mechanical
    "washer (spin)": 500, "washer (heat)": 1200, "electric dryer (240v)": 4500,
    "gas dryer (motor)": 400, "furnace blower": 600, "electric water heater (240v)": 4500,
    "gas water heater (pilot/vent)": 150, "sump pump (running)": 1000,
    "well pump (240v)": 1100, "dehumidifier": 450, "humidifier": 200,
    "garage door opener (running)": 500, "central ac (240v, per ton)": 3500,
    "window ac (large)": 1200, "window ac (small)": 600, "space fan": 60,
    "ceiling fan": 70, "bathroom exhaust fan": 40, "whole-house fan": 1200,
    # refrigeration (running draw; surge 3x on compressor start)
    "refrigerator": 200, "fridge (older)": 350, "chest freezer": 200,
    "mini fridge": 100, "wine cooler": 150,
    # electronics / lighting
    "led bulb": 10, "incandescent bulb": 75, "cfl bulb": 20,
    "tv (55in led)": 120, "tv (65in)": 150, "desktop pc + monitors": 350,
    "gaming pc (load)": 500, "laptop": 80, "router + modem": 30,
    "game console": 150, "phone charger": 20, "printer": 400,
    # workshop
    "corded drill": 600, "circular saw (cutting)": 1400, "table saw (cutting)": 1800,
    "shop vac": 1200, "air compressor (2hp)": 1500, "bench grinder": 500,
    "work lights": 300,
    # misc household
    "aquarium heater": 200, "aquarium filter": 25, "heat lamp": 250,
    "vacuum (upright)": 900, "robot vacuum dock": 30, "sewing machine": 100,
    "christmas lights (led, 300)": 40, "christmas lights (incandescent, 300)": 1000,
}

MOTOR_LOADS = {"refrigerator", "fridge (older)", "chest freezer", "mini fridge", "wine cooler",
               "sump pump (running)", "well pump (240v)", "garage door opener (running)",
               "washer (spin)", "washer (heat)", "air compressor (2hp)", "disposal"}

STATE_FILE = os.path.join(os.path.expanduser("~"), ".circuit_map.json")


def cmd_load(args):
    items = []
    for chunk in args.items.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            name, w = chunk.rsplit(":", 1)
            try:
                watts = float(w)
            except ValueError:
                print(f"  !! can't parse watts in '{chunk}' (use name:watts)"); sys.exit(1)
            items.append((name.strip().lower(), watts))
        else:
            name = chunk.lower()
            match = find_appliance(name)
            if match:
                items.append((match, APPLIANCES[match]))
            else:
                print(f"  !! unknown appliance '{chunk}' — try `db` or give watts as name:watts")
                sys.exit(1)
    if not items:
        print("  no items given"); sys.exit(1)

    volts, amps = args.volts, args.amps
    total_w = sum(w for _, w in items)
    draw_a = total_w / volts
    rated_a = volts * amps
    continuous_cap = amps * 0.80
    draw_w_80 = volts * continuous_cap

    print(f"\n  Circuit: {volts} V, {amps} A breaker (rated {rated_cap_str(rated_a)})")
    print(f"  {'item':<38} {'watts':>6}   {'amps':>6}")
    print("  " + "-" * 56)
    for n, w in items:
        print(f"  {n:<38} {w:>6.0f}   {w/volts:>6.2f}")
    motor_note = [n for n, _ in items if any(m in n for m in MOTOR_LOADS)]
    print("  " + "-" * 56)
    print(f"  {'TOTAL':<38} {total_w:>6.0f}   {draw_a:>6.2f}")
    print(f"\n  Breaker ceiling: {rated_cap_str(rated_a)}")
    print(f"  80% continuous:  {draw_w_80:.0f} W ({continuous_cap:.1f} A) — the honest all-day limit")

    if draw_a > amps:
        verdict = "OVERLOAD"
    elif total_w > draw_w_80:
        verdict = "TIGHT"
    else:
        verdict = "OK"
    print(f"\n  VERDICT: {verdict}")
    if verdict == "OVERLOAD":
        over_a = draw_a - amps
        print(f"  Over by {over_a:.1f} A ({over_a*volts:.0f} W). This WILL trip.")
        worst = max(items, key=lambda x: x[1])
        print(f"  Move '{worst[0]}' ({worst[1]:.0f} W) to another circuit, or drop something.")
    elif verdict == "TIGHT":
        slack = draw_w_80 - total_w
        if slack >= 0:
            print(f"  Under 80% by {slack:.0f} W.")
        else:
            print(f"  Over the 80% line by {-slack:.0f} W.")
        print("  Fine for short use; trips if it runs 3+ hours")
        print(f"  or on a hot day. Space heater + this = breaker trip.")
    else:
        print(f"  Fits with {draw_w_80 - total_w:.0f} W headroom under the continuous limit.")
    if motor_note:
        print(f"\n  Note: {', '.join(motor_note)} — compressor start draws 2-3x for ~1s.")
        print("  If trips coincide with motor START, suspect the appliance, not the load sum.")
    if args.continuous:
        print("  (--continuous set: everything must fit under the 80% line, not just the sum)")
    return 0


def rated_cap_str(watts):
    return f"{watts:.0f} W"


def find_appliance(query):
    keys = list(APPLIANCES)
    if query in APPLIANCES:
        return query
    # substring / headword match
    for k in keys:
        if query in k or k.split("(")[0].strip() in query:
            return k
    close = difflib.get_close_matches(query, keys, n=1, cutoff=0.5)
    return close[0] if close else None


def cmd_dead_outlet(args):
    print("\n  DEAD OUTLET — ranked diagnosis (breaker looks fine)")
    print("  " + "=" * 52)
    steps = [
        ("Tripped GFCI elsewhere (~60% of cases)",
         "GFCIs protect DOWNSTREAM outlets, often in other rooms.\n"
         "     Find every GFCI (TEST/RESET buttons): garage, basement, bathrooms,\n"
         "     kitchen, exterior, laundry. Press RESET on each.\n"
         "     Outdoor/garage units are the classic hidden killers."),
        ("Switched half-outlet",
         "Plug a lamp into BOTH halves, flip every nearby wall switch.\n"
         "     Builders commonly switch one half for lamps."),
        ("Half-tripped breaker",
         "Flip the suspect breaker fully OFF, wait 3 s, firmly ON.\n"
         "     A breaker can look ON while internally tripped."),
        ("Failed backstab connection (1970s-90s builds)",
         "Push-in back connectors fail and kill downstream outlets.\n"
         "     Signature: several outlets dead in a line, breaker fine.\n"
         "     The fault is in the LAST WORKING outlet before the dead ones.\n"
         "     Fix: breaker OFF, verify dead with NCVT, re-terminate on side screws."),
        ("Wire-nut failure in a junction box",
         "Thermal cycling loosens splices; downstream dies the same way.\n"
         "     Check boxes between last-working and first-dead outlet."),
        ("Dead outlet itself (springs worn)",
         "If plug falls out or feels loose — replace receptacle.\n"
         "     WARM/scorch/buzz = electrician, stop."),
    ]
    for i, (title, body) in enumerate(steps, 1):
        print(f"\n  [{i}] {title}\n      {body}")
    print("\n  SAFETY: warm outlet, scorch, smell, or tingle -> breaker OFF + electrician.")
    print("  Aluminum wiring (1965-73) -> specialist only. Panel stays closed.")
    return 0


def cmd_trip(args):
    patterns = {
        "instant": ("Short circuit / ground fault in a device or cord",
                    "Unplug everything, reset. Stays on = replug one by one to find culprit.\n"
                    "     Trips with nothing plugged = wiring fault -> electrician."),
        "minutes": ("Classic overload",
                    "Run `load` with everything on that circuit. Two 'invisible 1500s'\n"
                    "     (heater/kettle/microwave) on one circuit is the usual answer."),
        "together": ("Marginal overload — only when two loads coincide",
                     "Move one big load to another circuit; relabel the panel."),
        "gfci": ("Ground fault at plug level",
                 "Unplug all loads on that GFCI, reset, replug one by one.\n"
                 "     Wet-location trips (bathroom/outdoor/sump) = it's doing its job."),
        "motor": ("Failing motor / locked rotor, or marginal overload",
                  "If the appliance trips the circuit ALONE, the appliance is the fault.\n"
                  "     Fridge/sump/AC compressor failing = appliance repair, not wiring."),
        "random": ("Water ingress, rodent chew, failing breaker, or AFCI nuisance",
                   "Inspect attic/garage runs for chew marks and damp.\n"
                   "     Random trips that persist after load isolation -> electrician."),
        "won't reset": ("Hard fault present (or failed breaker)",
                        "Everything unplugged + lights off and still won't latch:\n"
                        "     stop resetting, call an electrician."),
    }
    p = (args.pattern or "").lower()
    key = None
    for k in patterns:
        if k in p or p in k:
            key = k; break
    if not key:
        key = difflib.get_close_matches(p, patterns.keys(), n=1, cutoff=0.3)
        key = key[0] if key else None
    if not key:
        print("\n  Patterns I know: " + ", ".join(patterns))
        print("  e.g. --pattern instant | minutes | together | gfci | motor | random | \"won't reset\"")
        return 1
    title, body = patterns[key]
    print(f"\n  PATTERN: {key}\n  MEANING: {title}\n  ACTION:\n{body}")
    return 0


def cmd_db(args):
    print(f"\n  {len(APPLIANCES)} appliances (INPUT watts — what the circuit sees):\n")
    cur = None
    for k in sorted(APPLIANCES):
        grp = "kitchen" if any(w in k for w in ("microwave", "toaster", "kettle", "fryer", "pot",
                "coffee", "blender", "dish", "disposal", "cooker", "rice", "griddle", "waffle", "can")) \
            else "heating/personal" if any(w in k for w in ("heater", "dryer", "iron", "blanket",
                "mattress", "towel", "gun")) \
            else "mechanical" if any(w in k for w in ("washer", "dryer (", "furnace", "water heater",
                "pump", "humid", "opener", "ac", "fan")) \
            else "cold" if any(w in k for w in ("fridge", "freezer", "cooler", "refrigerator")) \
            else "electronics" if any(w in k for w in ("bulb", "tv", "pc", "laptop", "router",
                "console", "charger", "printer")) \
            else "workshop" if any(w in k for w in ("drill", "saw", "vac", "compressor",
                "grinder", "work lights")) \
            else "household"
        if grp != cur:
            print(f"  --- {grp.upper()} ---")
            cur = grp
        print(f"    {k:<42} {APPLIANCES[k]:>5} W")
    return 0


def cmd_map(args):
    print("\n  CIRCUIT MAPPING SESSION (Ctrl-C exits; state saved to ~/.circuit_map.json)")
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            state = json.load(open(STATE_FILE))
        except Exception:
            pass
    label = args.label or f"breaker-{len(state)+1}"
    entry = {"mapped": datetime.now().strftime("%Y-%m-%d %H:%M")}
    print(f"  Recording: {label}")
    entry["amps"] = input("  Breaker size (A, e.g. 15): ").strip() or "?"
    entry["rooms"] = input("  Rooms/outlets covered: ").strip() or "?"
    entry["loads"] = input("  Big loads found (fridge, microwave...): ").strip() or "?"
    entry["notes"] = input("  Notes (GFCI? shared? half-switched?): ").strip() or ""
    state[label] = entry
    json.dump(state, open(STATE_FILE, "w"), indent=2)
    print(f"  Saved {len(state)} circuits. GO WRITE IT ON THE PANEL DOOR.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Residential circuit triage")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("load", help="sum appliance draw vs breaker")
    p.add_argument("--volts", type=float, default=120)
    p.add_argument("--amps", type=float, default=15)
    p.add_argument("--items", required=True, help="comma list: name[:watts]")
    p.add_argument("--continuous", action="store_true", help="everything runs 3+ hours")
    p.set_defaults(fn=cmd_load)

    p = sub.add_parser("dead-outlet", help="ranked dead-outlet tree")
    p.set_defaults(fn=cmd_load if False else cmd_dead_outlet)

    p = sub.add_parser("trip", help="decode trip pattern")
    p.add_argument("--pattern", required=True)
    p.set_defaults(fn=cmd_trip)

    p = sub.add_parser("db", help="appliance database")
    p.set_defaults(fn=cmd_db)

    p = sub.add_parser("map", help="log a circuit-mapping session")
    p.add_argument("--label", help="breaker label")
    p.set_defaults(fn=cmd_map)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        sys.exit(1)
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
