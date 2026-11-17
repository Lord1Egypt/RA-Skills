#!/usr/bin/env python3
"""dampdoctor.py — basement moisture diagnosis, source ranking, dehumidifier sizing.

Subcommands:
  analyze       dew point vs wall temp physics → condensation/liquid verdict
  dehumidifier  AHAM pints/day sizing + energy pricing + existing-unit check
  sources       10-source ranked audit with fix prices
  log           humidity CSV analyzer (date,RH[,Temp]) vs target band

Offline, stdlib only.
"""
import argparse
import csv
import math
import re

# ------------------------------------------------------------------ physics

def dew_point(t, rh):
    """Magnus formula, °C."""
    a, b = 17.62, 243.12
    g = math.log(max(rh, 1) / 100.0) + (a * t) / (b + t)
    return b * g / (a - g)


def soil_temp_estimate(month):
    """Northern-temperate deep-soil band by month (°C)."""
    bands = {12: (8, 10), 1: (8, 10), 2: (8, 10),
             3: (9, 12), 4: (10, 13), 5: (11, 14), 6: (12, 15),
             7: (13, 16), 8: (14, 17), 9: (14, 17),
             10: (13, 16), 11: (10, 13)}
    lo, hi = bands.get(month, (12, 15))
    return (lo + hi) / 2, lo, hi


MONTH_BY_NAME = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"])}


def analyze(air_t, rh, wall_t, soil_t, area_m2, ceiling, season, month=None):
    td = dew_point(air_t, rh)
    est, lo, hi = soil_temp_estimate(month or MONTH_BY_NAME.get((season or "")[:3].lower(), 7))
    wall = wall_t if wall_t is not None else soil_t if soil_t is not None else est
    wall_src = "measured" if wall_t is not None else (
        "given soil" if soil_t is not None else f"seasonal estimate ({lo}–{hi}°C band)")
    print("BASEMENT MOISTURE ANALYSIS")
    print("═" * 62)
    print(f"Air: {air_t:.1f}°C @ {rh:.0f}% RH → dew point {td:.1f}°C")
    print(f"Wall temperature ({wall_src}): {wall:.1f}°C")
    print(f"{'Wall' if wall < td else 'Wall'} vs dew point: wall is "
          f"{'BELOW' if wall < td else 'ABOVE'} dew point by {abs(td - wall):.1f}°C")
    print("─" * 62)
    if wall < td - 1.0:
        v = ("CONDENSATION LIKELY — surfaces colder than the dew point WILL collect "
             "moisture film; expect mold on organic items, damp film on cold walls, "
             "sweating cold-water tank/pipes.")
    elif wall < td:
        v = ("MARGINAL — wall sits at the dew point: condensation comes and goes with "
             "RH swings. A 5% RH drop or +1°C wall temperature resolves it.")
    else:
        v = (f"CONDENSATION UNLIKELY (wall {wall:.1f}°C > dew {td:.1f}°C by "
             f"{wall - td:.1f}°C). Damp marks/mold now point to LIQUID water — "
             "read the wall signs (efflorescence/tide marks) and run `sources`.")
    print("VERDICT:", v)
    target_rh = 55
    max_td = dew_point(air_t, target_rh)
    print(f"Dehumidifier target: ≤{target_rh}% RH (dew point {max_td:.1f}°C at "
          f"{air_t:.0f}°C) keeps typical wall temps above the dew point.")
    if area_m2:
        cls = "damp" if rh < 80 else "wet"
        pints, liters = size_dehumidifier(area_m2, cls)
        print(f"Sizing for {area_m2:.0f} m² at {rh:.0f}% RH ('{cls}' class): "
              f"~{pints} pt / {liters} L per day (see `dehumidifier` for details).")
    print("Next: `sources --wall-signs ...` to rank fixes, or `dehumidifier` to size.")
    print("NOT A STRUCTURAL ASSESSMENT — horizontal cracks/bowing walls = contractor now.")


# --------------------------------------------------------- dehumidifier sizing

# area m² -> liters/day for moderately damp / very damp / wet (≈Energy Star table)
SIZE_TABLE = [
    (50, 10, 12, 14), (100, 14, 17, 20), (150, 18, 21, 25),
    (250, 25, 30, 34), (350, 32, 38, 44),
]


def size_dehumidifier(area_m2, damp_class):
    need = {"moderately damp": 1, "damp": 1, "very damp": 2, "wet": 3}[damp_class]
    prev = None
    for row in SIZE_TABLE:
        if area_m2 <= row[0]:
            liters = row[need]
            break
        prev = row
    else:
        liters = 44 + (area_m2 - 350) // 100 * 4  # extrapolate
        liters = min(liters, 60)
    pints = round(liters * 2.113)
    return pints, liters


def dehumidifier(area, cls, energy_rate, measured, open_factor, cold):
    print(f"DEHUMIDIFIER SIZING — {area:.0f} m² ({area * 10.764:.0f} ft²), class '{cls}'")
    print("═" * 62)
    pints, liters = size_dehumidifier(area, cls)
    factor = 1.0 + open_factor
    note = ""
    if cold:
        factor *= 1.2
        note = " ×1.2 cold-basement (units extract ~60% of nameplate at 18°C)"
    rec_l = liters * factor
    rec_p = pints * factor
    print(f"Table capacity: {pints} pt ({liters} L)/day × {factor:.2f} openness/cold factor"
          f"{note}")
    print(f"→ BUY CLASS: ≥{math.ceil(rec_p / 5) * 5} pt ({math.ceil(rec_l / 2) * 2} L)/day")
    if rec_l >= 12:
        print("→ Get the drain-hose / condensate-pump version. Buckets at this class overflow.")
    kwh_per_l = 1 / 1.6  # Energy Star integrated factor L/kWh
    duty = 0.5
    daily_kwh = rec_l * duty * kwh_per_l
    print(f"Energy: ≈{daily_kwh:.1f} kWh/day at 50% duty "
          f"(≈${daily_kwh * 30 * energy_rate:.0f}/mo at ${energy_rate:.2f}/kWh)")
    if measured is not None:
        print("─" * 62)
        print(f"EXISTING-UNIT CHECK: measured extraction {measured:.1f} L/day "
              f"vs required {rec_l:.0f} L/day")
        if measured >= rec_l * 0.9:
            print("VERDICT: KEEPING UP — if RH still >60%, the moisture SOURCE is the "
                  "problem (run `sources`), not the machine.")
        else:
            gap = rec_l - measured
            print(f"VERDICT: UNDERSIZED by ~{gap:.0f} L/day — either the unit is too small, "
                  "or a liquid/s interior source is feeding the room (dryer, sump, leak).")
    print("Circulation tip: a $30 fan moving air along cold walls raises surface temp "
          "and cuts condensation — cheaper than the next size up.")


# ----------------------------------------------------------------- source audit

SOURCES = [
    # key, label, fix, price
    ("downspouts", "Downspouts dumping at the foundation", 
     "Extend 2+ m / bury drain line away from walls", "$10–50/corner"),
    ("grading", "Negative grading toward the wall", 
     "Regrade to slope away over first 3 m", "$0 DIY – $500"),
    ("gutters", "Clogged or short gutters", "Clean + extend; guards", "$0–300"),
    ("window_wells", "Window wells without drains/covers", "Dome covers + gravel", "$20–60"),
    ("dryer_vent", "Dryer venting indoors", "Vent outside (through wall kit)", "$30–100"),
    ("sump", "Unsealed sump pit", "Sealed bolt-down lid", "$30–80"),
    ("penetrations", "Service penetration gaps (gas/water/hose bib)", 
     "Hydraulic cement / expanding foam", "$10"),
    ("interior_sources", "Interior moisture: laundry drying, firewood, leaks",
     "Vent dryer properly; move firewood out; fix leaks", "$0–150"),
    ("cracks", "Wall cracks / cold joints seeping", "Epoxy/poly injection", "$15 DIY – $500"),
    ("hydrostatic", "Hydrostatic pressure / high water table",
     "Interior drain tile + sump (last resort)", "$3k–10k pro"),
]

WALL_SIGNS = {
    "efflorescence": ("White salt crystals = water moving THROUGH the concrete and "
                      "evaporating → LIQUID path. Fix outside water management (top of list)."),
    "tide-marks": ("Dark band at the base = capillary rise / joint seepage → LIQUID. "
                   "Check downspouts + grading first."),
    "streaks": ("Streaks trailing from cracks = localized liquid leak → injection "
                "candidate AFTER outside fixes."),
    "mold-organic": ("Mold only on cardboard/wood/fabric (not concrete) = airborne "
                     "humidity/condensation → dehumidifier + sources 5–8."),
    "uniform-film": ("Uniform damp film, worst on cold walls/tank/pipes = CONDENSATION "
                     "→ dehumidifier + air sealing."),
}


def sources(args_ns):
    print("MOISTURE SOURCE AUDIT (ranked, cheapest fixes first)")
    print("═" * 62)
    flagged = []
    for key, label, fix, price in SOURCES:
        val = getattr(args_ns, key, None)
        if val is None:
            continue
        is_bad = val in (True, "yes", "bad", "clogged", "inside", "none", "negative")
        # numeric downspout distance in meters: <2 m from foundation = bad
        if key == "downspouts":
            try:
                is_bad = float(val) < 2.0
            except (TypeError, ValueError):
                pass
        if is_bad:
            flagged.append((label, fix, price))
    if not flagged:
        print("No problem sources flagged. If dampness persists: run `analyze` for "
              "condensation physics and `log` for RH stats.")
    for i, (label, fix, price) in enumerate(flagged, 1):
        print(f"[{i}] {label}\n    → {fix}  ({price})")
    signs = [s for s in WALL_SIGNS if getattr(args_ns, f"sign_{s.replace('-', '_')}", None)]
    # also accept --wall-signs "efflorescence,mold-organic"
    if args_ns.wall_signs:
        for s in [x.strip() for x in args_ns.wall_signs.split(",") if x.strip()]:
            norm = s.lower().replace(" ", "-")
            if norm in WALL_SIGNS:
                signs.append(norm)
    if signs:
        print("─" * 62)
        for s in dict.fromkeys(signs):
            print(f"SIGN — {s}: {WALL_SIGNS[s]}")
    if flagged:
        n_cheap = sum(1 for _, _, p in flagged if p.startswith(("$0", "$1", "$2", "$3"))
                      and "k" not in p and "500" not in p)
        print("─" * 62)
        print(f"DOCTRINE: {n_cheap} cheap fix(es) before any contractor talk. "
              "A $12k drain-tile quote before downspouts/grading are fixed = get "
              "a second opinion.")
    print("Structural red flags (horizontal cracks, bowing) = structural engineer, "
          "not a moisture project.")


# ------------------------------------------------------------------ log analyze

def log_analyze(path, target):
    rows = []
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if not row or not re.search(r"\d", row[0] or ""):
                continue
            try:
                date = row[0].strip()
                rh = float(row[1])
                t = float(row[2]) if len(row) > 2 and row[2].strip() else None
                rows.append((date, rh, t))
            except (ValueError, IndexError):
                continue
    if not rows:
        print("No parsable rows (expected CSV: date,RH[,Temp]).")
        return 1
    rhs = [r[1] for r in rows]
    over = [r for r in rows if r[1] > target + 5]
    under = [r for r in rows if r[1] < target - 15]
    avg = sum(rhs) / len(rhs)
    print(f"HUMIDITY LOG — {len(rows)} readings, avg {avg:.0f}% RH, "
          f"min {min(rhs):.0f}%, max {max(rhs):.0f}%")
    print("═" * 62)
    print(f"Target band: {target}% ±5 → {len(over)} reading(s) HIGH, "
          f"{len(under)} LOW.")
    if over:
        # cluster by month
        months = {}
        for d, rh_, _t in over:
            key = re.sub(r"\d+$", "", d)[:7]
            months.setdefault(key, 0)
            months[key] += 1
        top = sorted(months.items(), key=lambda kv: -kv[1])[:3]
        print(f"High-RH clusters: {', '.join(f'{k} ({v})' for k, v in top)}")
        print("→ Sustained >60% RH is the mold condition. If clustered in warm months: "
              "condensation season — dehumidifier earlier in the year.")
    temps = [r[2] for r in rows if r[2] is not None]
    if temps:
        tavg = sum(temps) / len(temps)
        # worst-case dew check on the most humid reading
        worst = max(rows, key=lambda r: r[1])
        if worst[2] is not None:
            td = dew_point(worst[2], worst[1])
            print(f"Worst reading: {worst[0]} — {worst[1]:.0f}% @ {worst[2]:.0f}°C "
                  f"→ dew point {td:.1f}°C (walls below this = wet).")
    print("Instrument note: cheap hygrometers drift ±5–10% — calibrate against the "
          "salt-test (saturated NaCl = 75%) before trusting absolute numbers.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("analyze")
    p.add_argument("--air-t", type=float, required=True)
    p.add_argument("--rh", type=float, required=True)
    p.add_argument("--wall-t", type=float, default=None,
                   help="measured wall surface temp (best input)")
    p.add_argument("--soil-t", type=float, default=None)
    p.add_argument("--season", default="summer")
    p.add_argument("--area", type=float, default=0, help="floor area, m² (or ft² if >2000)")
    p.add_argument("--ceiling", type=float, default=2.3)

    p = sub.add_parser("dehumidifier")
    p.add_argument("--area", type=float, required=True, help="m²")
    p.add_argument("--class", dest="cls", default="damp",
                   choices=["moderately damp", "damp", "very damp", "wet"])
    p.add_argument("--energy-rate", type=float, default=0.15, help="$/kWh")
    p.add_argument("--measured-liters-day", type=float, default=None)
    p.add_argument("--open-factor", type=float, default=0.2,
                   help="0.0 sealed..0.5 open stairwell")
    p.add_argument("--cold", action="store_true", help="basement stays <18°C")

    p = sub.add_parser("sources")
    for key, label, _f, _p in SOURCES:
        p.add_argument(f"--{key.replace('_', '-')}", default=None,
                       help=f"{label} (value: bad/none/negative/clogged/inside or yes)")
    p.add_argument("--wall-signs", default="",
                   help="comma list: efflorescence,tide-marks,streaks,mold-organic,uniform-film")

    p = sub.add_parser("log")
    p.add_argument("--csv", required=True)
    p.add_argument("--target", type=int, default=50)

    a = ap.parse_args()
    # normalize dashed args onto underscores
    for key in list(vars(a)):
        setattr(a, key.replace("-", "_"), getattr(a, key))
    if a.cmd == "analyze":
        area = a.area if a.area and a.area < 2000 else (a.area / 10.764 if a.area else 0)
        month = None
        m = re.search(r"\d{4}- (\d{1,2})|\d{4}-(\d{1,2})", getattr(a, "season", "") or "")
        analyze(a.air_t, a.rh, a.wall_t, a.soil_t, area, a.ceiling, a.season, month)
    elif a.cmd == "dehumidifier":
        dehumidifier(a.area, a.cls, a.energy_rate, a.measured_liters_day,
                     a.open_factor, a.cold)
    elif a.cmd == "sources":
        sources(a)
    elif a.cmd == "log":
        raise SystemExit(log_analyze(a.csv, a.target) or 0)


if __name__ == "__main__":
    main()
