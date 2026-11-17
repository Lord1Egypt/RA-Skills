#!/usr/bin/env python3
"""Clean Air Room Planner — HEPA CADR sizing, adequacy checks, DIY
Corsi-Rosenthal box math, PM2.5 diary analysis, filter-life tracking.

Stdlib-only.
"""
import argparse
import json
import math
import os
import sys
from datetime import date, datetime, timedelta

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "air_data.json")

M3_PER_FT3 = 0.0283168
CFM_PER_M3H = 0.589  # 1 m³/h = 0.589 cfm (approx, exact: /3.6 * 1.699)

ACH = {
    "smoke": ("Wildfire smoke event", 5),
    "allergy": ("Allergy season", 4.5),
    "general": ("General air quality", 2.5),
}

PM_BANDS = [
    (12, "Good"),
    (35, "Moderate"),
    (55, "Unhealthy for sensitive groups"),
    (150, "Unhealthy"),
    (250, "Very unhealthy"),
    (float("inf"), "Hazardous"),
]


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def pm_band(v):
    for limit, name in PM_BANDS:
        if v <= limit:
            return name
    return "Hazardous"


def load_data():
    if os.path.exists(DATA):
        with open(DATA) as f:
            return json.load(f)
    return {"readings": [], "filters": {}}


def save_data(d):
    with open(DATA, "w") as f:
        json.dump(d, f, indent=2)


# ---------------------------------------------------------------- size
def cmd_size(args):
    ceil = args.ceiling or (2.7 if args.unit == "m" else 8.0)
    if args.unit == "m":
        vol = args.area * ceil
        print(f"Room: {vol:.1f} m³ ({args.area:.0f} m² × {ceil:.1f} m)")
    else:
        vol_ft3 = args.area * ceil
        vol = vol_ft3 * M3_PER_FT3
        print(f"Room: {args.area:.0f} sq ft × {ceil:.0f} ft "
              f"= {vol_ft3:.0f} ft³ = {vol:.1f} m³")

    label, ach = ACH[args.use]
    cadr = vol * ach
    cfm = cadr * 0.5886  # 1 m³/h = 0.5886 CFM
    print(f"Target: {ach} ACH ({label})")
    print(f"Required CADR: {cadr:.0f} m³/h  (~{cfm:.0f} CFM)")
    print(f"  buy margin: {cadr*1.5:.0f} m³/h to allow quiet-speed operation")
    print()
    print("Shopping rule: multiply floor area by ceiling height, then by the")
    print("ACH above. Ignore 'for rooms up to X' claims (they assume 2 ACH).")


# ---------------------------------------------------------------- check
def cmd_check(args):
    vol = args.area * (args.ceiling or 2.7)
    label, ach_target = ACH[args.use]
    ach = args.cadr / vol
    verdict = ("ADEQUATE" if ach >= ach_target else
               "UNDERSIZED" if ach >= ach_target * 0.6 else "INADEQUATE")
    mins = 60 / ach if ach > 0 else float("inf")
    print(f"Room: {vol:.1f} m³ | Purifier CADR: {args.cadr:g} m³/h")
    print(f"Achieved: {ach:.1f} ACH vs {ach_target} target ({label})")
    print(f"Full air change every ~{mins:.0f} minutes")
    print(f"Verdict: {verdict} for {args.use}")
    if verdict != "ADEQUATE":
        need = vol * ach_target
        print(f"Needed CADR: {need:.0f} m³/h — you are "
              f"{need-args.cadr:.0f} short")
        print("Options: smaller room (close the door), second unit, or run")
        print("at max speed during peaks.")
    else:
        print("Run on HIGH during event peaks; low speed is fine overnight")
        print("only if the room is sealed.")
    print()
    print(f"Steady-state estimate: indoor ≈ "
          f"{0.15 if ach >= 4 else 0.3:.0%}–"
          f"{0.25 if ach >= 4 else 0.5:.0%} of outdoor PM2.5 (sealed room).")


# ---------------------------------------------------------------- crbox
def cmd_crbox(args):
    eff = args.fan_cfm * (0.40 if args.filters >= 4 else 0.33)
    m3h = eff / 0.5886
    print(f"DIY Corsi-Rosenthal box: {args.fan_cfm:g} CFM box fan "
          f"+ {args.filters} MERV-13 filter(s)")
    print(f"Effective clean airflow ≈ {eff:.0f} CFM ≈ {m3h:.0f} m³/h")
    print()
    if args.filters < 4:
        print("Use 4-5 filters: more surface = less pressure drop = more")
        print("flow. A 4-filter cube is the standard build.")
    print("Equivalent commercial purifier class: "
          f"{'large-room' if m3h > 600 else 'mid-room'} "
          f"(${60} of parts vs $300-500).")
    print("Noise: high but tolerable; seal edges with tape; replace")
    print("filters when visibly gray or after ~3-6 months of events.")


# ---------------------------------------------------------------- log
def cmd_log(args):
    d = load_data()
    if args.log_cmd == "add":
        entry = {"ts": datetime.now().isoformat(timespec="minutes"),
                 "indoor": args.indoor, "outdoor": args.outdoor,
                 "purifier": args.purifier or "",
                 "note": args.note or ""}
        d["readings"].append(entry)
        save_data(d)
        print(f"Logged: indoor {args.indoor} / outdoor {args.outdoor} µg/m³ "
              f"({pm_band(args.indoor)} indoors)")
    elif args.log_cmd == "analyze":
        rs = d["readings"]
        if len(rs) < 3:
            die("need at least 3 readings; log more first")
        print(f"{len(rs)} readings")
        ratios = [r["indoor"] / r["outdoor"] for r in rs
                  if r["outdoor"] > 0]
        avg_ratio = sum(ratios) / len(ratios)
        on = [r for r in rs if (r.get("purifier") or "").lower() in ("on", "yes", "true", "1")]
        off = [r for r in rs if r not in on]
        print(f"Average indoor/outdoor ratio: {avg_ratio:.2f}")
        if on and off:
            r_on = sum(x["indoor"]/x["outdoor"] for x in on if x["outdoor"]>0)/len([x for x in on if x["outdoor"]>0] or [1])
            r_off = sum(x["indoor"]/x["outdoor"] for x in off if x["outdoor"]>0)/len([x for x in off if x["outdoor"]>0] or [1])
            print(f"  with purifier ON: {r_on:.2f} | OFF: {r_off:.2f} "
                  f"→ {'filtration is working' if r_on < r_off*0.75 else 'weak effect — check seals/speed'}")
        peak = max(rs, key=lambda r: r["indoor"])
        print(f"Peak indoor: {peak['indoor']} µg/m³ ({pm_band(peak['indoor'])}) "
              f"at {peak['ts']}")
        good = sum(1 for r in rs if r["indoor"] <= 12)
        print(f"Time in 'Good' band: {good}/{len(rs)} readings "
              f"({good/len(rs)*100:.0f}%)")
        print()
        print("Target: keep the clean-air room under 35 (and ideally under")
        print("12) during events. If ratio > 0.5 with the purifier on:")
        print("seal drafts, close the door, run at max speed, check filter.")


# ---------------------------------------------------------------- filter
def cmd_filter(args):
    d = load_data()
    if args.filter_cmd == "new":
        d["filters"][args.name] = {"rated_hours": args.rated_hours,
                                   "used_hours": 0.0,
                                   "smoke_weeks": 0,
                                   "installed": date.today().isoformat()}
        save_data(d)
        print(f"Registered filter {args.name!r} rated {args.rated_hours} h")
    elif args.filter_cmd == "tick":
        f = d["filters"].get(args.name) or die(f"unknown filter {args.name!r}")
        f["used_hours"] += args.hours
        if args.smoke_week:
            f["smoke_weeks"] += 1
        save_data(d)
        print(f"{args.name}: +{args.hours:g} h "
              f"(total {f['used_hours']:g} h)")
    elif args.filter_cmd == "status":
        if not d["filters"]:
            print("No filters registered (filter new --name ... --rated-hours ...)")
            return
        print(f"{'Filter':<18}{'Used':<10}{'Effective':<12}Change by")
        print("-" * 52)
        today = date.today()
        for name, f in d["filters"].items():
            # each heavy smoke week loads media ~3x a normal week (~60h)
            eff = f["used_hours"] + f["smoke_weeks"] * 120
            pct = eff / f["rated_hours"]
            installed = date.fromisoformat(f["installed"])
            if eff > 0 and pct < 1:
                hours_left = f["rated_hours"] - eff
                days_in = max((today - installed).days, 1)
                burn_per_day = eff / days_in
                days_left = int(hours_left / max(burn_per_day, 0.1))
                due = today + timedelta(days=days_left)
                due_s = due.isoformat()
            else:
                due_s = "OVERDUE"
            print(f"{name:<18}{f['used_hours']:g} h   "
                  f"{pct*100:.0f}% used    {due_s}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("size", help="required CADR for a room")
    p.add_argument("--area", type=float, required=True,
                   help="floor area (m² or sq ft)")
    p.add_argument("--ceiling", type=float, default=None,
                   help="ceiling height (default 2.7 m / 8 ft)")
    p.add_argument("--unit", choices=["m", "ft"], default="m")
    p.add_argument("--use", choices=list(ACH), default="smoke")
    p.set_defaults(fn=cmd_size)

    p = sub.add_parser("check", help="is your purifier adequate?")
    p.add_argument("--area", type=float, required=True, help="m²")
    p.add_argument("--ceiling", type=float, default=2.7)
    p.add_argument("--use", choices=list(ACH), default="smoke")
    p.add_argument("--cadr", type=float, required=True, help="m³/h (smoke CADR)")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("crbox", help="DIY box-fan filter estimate")
    p.add_argument("--fan-cfm", type=float, required=True)
    p.add_argument("--filters", type=int, default=4)
    p.set_defaults(fn=cmd_crbox)

    p = sub.add_parser("log", help="PM2.5 diary")
    p.add_argument("log_cmd", choices=["add", "analyze"])
    p.add_argument("--indoor", type=float)
    p.add_argument("--outdoor", type=float)
    p.add_argument("--purifier", default="",
                   help="'on' or 'off' at time of reading")
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("filter", help="filter-life tracking")
    p.add_argument("filter_cmd", choices=["new", "tick", "status"])
    p.add_argument("--name", default=None)
    p.add_argument("--rated-hours", type=float, default=2000)
    p.add_argument("--hours", type=float, default=0)
    p.add_argument("--smoke-week", action="store_true",
                   help="mark this week as a heavy-smoke week (3x loading)")
    p.set_defaults(fn=cmd_filter)

    args = ap.parse_args()
    if args.cmd == "log" and args.log_cmd == "add":
        if args.indoor is None or args.outdoor is None:
            die("log add needs --indoor and --outdoor")
    args.fn(args)


if __name__ == "__main__":
    main()
