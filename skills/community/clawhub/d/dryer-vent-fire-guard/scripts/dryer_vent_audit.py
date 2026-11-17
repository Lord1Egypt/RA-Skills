#!/usr/bin/env python3
"""Dryer vent fire-risk audit.

Turns dry-time creep + vent run geometry into code-based verdicts (IRC M1502
35-ft equivalent-length allowance) and a concrete action ladder.

Data sources for the model:
- IRC M1502.4 / manufacturer install manuals: 35 ft max developed length for
  4" duct, minus 5 ft per 90-degree elbow.
- USFA/CPSC: ~13k-15.5k dryer fires/yr, ~1/3 from failure to clean the vent.
- Dry-time bands from healthy appliance service baselines (towel load).

Stdlib only. No network.
"""
import argparse
import json
import sys

# 90-degree elbow equivalent cost, ft (IRC M1502.4 table convention)
ELBOW_FT = 5.0
# Max developed length for a 4" rigid run, ft
MAX_EQ_FT_4IN = 35.0
# Small-diameter penalty: 3" runs are a hard flag
DIAM_PENALTY = {2.5: 10.0, 3.0: 12.0, 4.0: 0.0}
# Friction factor vs actual length for flex materials
MATERIAL = {
    "rigid":      {"factor": 1.0,  "violation": False, "note": "code-compliant smooth-wall aluminum/galvanized steel"},
    "semirigid":  {"factor": 1.35, "violation": False, "note": "acceptable transition, mildly lossy"},
    "foil":       {"factor": 2.0,  "violation": True,  "note": "CODE VIOLATION on dryers - replace immediately"},
    "vinyl":      {"factor": 2.0,  "violation": True,  "note": "CODE VIOLATION - combustible, melts, ignites"},
    "unknown":    {"factor": 1.5,  "violation": False, "note": "inspect: foil/vinyl must be replaced"},
}


def dry_time_verdict(minutes: float):
    """Standard towel-load dry-time bands."""
    if minutes <= 50:
        return "HEALTHY", 0
    if minutes <= 60:
        return "WATCH", 1
    if minutes <= 90:
        return "RESTRICTED", 2
    return "SEVERE", 3


def equivalent_length(material: str, length_ft: float, elbows: int, diameter_in: float):
    mat = MATERIAL[material]
    eq = length_ft * mat["factor"] + elbows * ELBOW_FT + DIAM_PENALTY.get(diameter_in, 0.0)
    return eq, mat


def audit(material: str, length_ft: float, elbows: int, diameter_in: float,
          dry_minutes: float = None, loads_per_week: float = None,
          vertical_rise_ft: float = 0.0, screen_on_hood: bool = False,
          vents_indoors: bool = False, animal_problem: bool = False,
          years_since_clean: float = 0.0):
    # --- dry-time evidence ---
    tv, score_dt = dry_time_verdict(dry_minutes) if dry_minutes else ("UNTESTED", 0)

    # --- geometry vs code ---
    eq, mat = equivalent_length(material, length_ft, elbows, diameter_in)
    geometry_pct = eq / MAX_EQ_FT_4IN
    score_geo = 3 if geometry_pct > 1.0 else (2 if geometry_pct > 0.85 else (1 if geometry_pct > 0.7 else 0))

    # --- risk stacking ---
    flags = []
    score = max(score_dt, score_geo)
    if mat["violation"]:
        score = max(score, 3)
        flags.append(("MATERIAL", mat["note"]))
    if dry_minutes and dry_minutes > 60:
        flags.append(("DRY-TIME", f"{dry_minutes:.0f} min for a towel load = restricted airflow; "
                                 "each extra cycle bakes lint at higher temperature"))
    if vertical_rise_ft > 6:
        score = max(score, 1)
        flags.append(("VERTICAL", f"{vertical_rise_ft:.0f} ft vertical rise: lint must be blown uphill; "
                                  "slows self-clearing, expect faster accumulation"))
    if screen_on_hood:
        score = max(score, 2)
        flags.append(("SCREEN HOOD", "screen on exterior hood plugs with lint then damper jams - replace with damper-only hood"))
    if vents_indoors:
        score = max(score, 3)
        flags.append(("INDOOR VENT", "venting indoors/attic/crawl is a code violation: moisture + lint inside the building"))
    if diameter_in < 4.0:
        flags.append(("DIAMETER", f"{diameter_in}\" duct: undersized; modern dryers need 4\""))
    if animal_problem:
        flags.append(("PESTS", "nest in termination/hood - remove, fit damper hood"))
    if years_since_clean >= 2:
        score = max(score, score_dt and max(1, score_dt))
        flags.append(("OVERDUE", f"{years_since_clean:.0f} yrs since last clean (1x/yr minimum; 2x/yr for large households/pets)"))
    if geometry_pct > 1.0:
        flags.append(("OUT OF CODE", f"{eq:.0f} ft equivalent vs 35 ft allowance - lint will re-accumulate regardless of cleaning; "
                                     "reroute/shorten/remove elbows or upsize"))

    band = ["SAFE", "WATCH", "RESTRICTED", "SEVERE"][min(score, 3)]

    # --- action ladder ---
    ladder = []
    if score >= 2 or mat["violation"]:
        ladder.append("1. CLEAN NOW: unplug (gas: shut valve), pull dryer, vacuum wall collar + internal duct "
                      "with shop vac + vent brush from BOTH ends")
    elif score == 1:
        ladder.append("1. INSPECT + CLEAN: pull dryer, check transition for kinks/lint, brush the run; "
                      "restriction is early but real")
    if mat["violation"]:
        ladder.append("2. REPLACE DUCT: foil/vinyl -> semi-rigid or rigid aluminum today ($10-25)")
    if geometry_pct > 1.0:
        ladder.append("3. REROUTE: every 90° elbow removed buys back 5 ft of allowance; straightest path wins")
    if screen_on_hood or animal_problem:
        ladder.append("4. FIX TERMINATION: damper-only hood, no screen, confirm flap swings free")
    if vents_indoors:
        ladder.append("5. RE-VENT OUTDOORS before next use: interior venting is a moisture + fire hazard")
    if score == 0:
        ladder = ["No action beyond routine: clean 1x/yr (2x/yr large household/pets), keep hood flap clear"]

    # --- recurrence + cost framing ---
    cadence = "every 12 months" if (loads_per_week or 0) <= 8 else "every 6 months"
    extra_cost = 0.0
    if dry_minutes:
        healthy = 50.0
        if dry_minutes > healthy:
            loads = loads_per_week or 5
            extra_kwh = (dry_minutes - healthy) / 60.0 * 3.0 * loads * 52  # ~3 kW element
            extra_cost = extra_kwh * 0.17
            ladder.append(f"Wasted energy: ~{extra_kwh:.0f} kWh/yr (~${extra_cost:.0f} @ $0.17/kWh) from extended cycles alone")

    return {
        "verdict": band,
        "dry_time_verdict": tv,
        "equivalent_length_ft": round(eq, 1),
        "code_allowance_ft": MAX_EQ_FT_4IN,
        "geometry_used_pct": round(geometry_pct * 100),
        "flags": [{"what": w, "why": why} for w, why in flags],
        "action_ladder": ladder,
        "cleaning_cadence": cadence,
    }


def main():
    p = argparse.ArgumentParser(description="Dryer vent fire-risk audit (IRC M1502 model)")
    p.add_argument("--demo", action="store_true", help="run built-in demo case")
    p.add_argument("--material", choices=sorted(MATERIAL), help="duct material behind the dryer")
    p.add_argument("--length-ft", type=float, help="actual duct length along the full path")
    p.add_argument("--elbows", type=int, default=0, help="count of 90-degree elbows")
    p.add_argument("--diameter-in", type=float, default=4.0, help="duct diameter, inches")
    p.add_argument("--dry-minutes", type=float, help="minutes to dry a standard towel load")
    p.add_argument("--loads-per-week", type=float)
    p.add_argument("--vertical-rise-ft", type=float, default=0.0)
    p.add_argument("--screen-on-hood", action="store_true")
    p.add_argument("--vents-indoors", action="store_true")
    p.add_argument("--pests", action="store_true", help="bird/rodent nest at termination")
    p.add_argument("--years-since-clean", type=float, default=0.0)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.demo:
        r = audit("foil", 12, 4, 4.0, dry_minutes=75, loads_per_week=8,
                  years_since_clean=3, screen_on_hood=True)
    else:
        if not a.material or not a.length_ft:
            p.error("--material and --length-ft are required (or use --demo)")
        r = audit(a.material, a.length_ft, a.elbows, a.diameter_in, a.dry_minutes,
                  a.loads_per_week, a.vertical_rise_ft, a.screen_on_hood,
                  a.vents_indoors, a.pests, a.years_since_clean)

    if a.json:
        print(json.dumps(r, indent=2))
        return

    print(f"VERDICT: {r['verdict']}  (dry-time: {r['dry_time_verdict']})")
    print(f"Vent: {r['equivalent_length_ft']} ft equivalent vs {r['code_allowance_ft']} ft allowance "
          f"({r['geometry_used_pct']}% of code used)")
    for f in r["flags"]:
        print(f"  ! {f['what']}: {f['why']}")
    print("Actions:")
    for s in r["action_ladder"]:
        print(f"  {s}")
    print(f"Cleaning cadence: {r['cleaning_cadence']}")


if __name__ == "__main__":
    main()
