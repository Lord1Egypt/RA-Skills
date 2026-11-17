#!/usr/bin/env python3
"""
commute_carbon.py — log trips, compute commute CO2, compare modes, track trajectory.

Factors: g CO2 per PASSENGER-km, planning-grade averages (DEFRA/EEA/EPA synthesis).
Storage: local JSON (default ~/.commute-carbon.json). Pure stdlib.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys

DEFAULT_FILE = os.path.join(os.path.expanduser("~"), ".commute-carbon.json")
DEFAULT_BUDGET_KG = 1000.0  # personal transport CO2 budget per year

# g CO2 per passenger-km (see references/emission-factors.md)
FACTORS = {
    "car": 192.0,        # average ICE car, solo
    "carpool": 192.0,    # /passengers at log time
    "ev": 53.0,
    "motorcycle": 103.0,
    "bus": 97.0,
    "coach": 27.0,
    "metro": 35.0,
    "tram": 30.0,
    "train": 41.0,
    "bike": 0.0,
    "e-bike": 5.0,
    "walk": 0.0,
    "scooter": 8.0,
    "plane": 255.0,
}
MODE_ALIASES = {
    "driving": "car", "drive": "car", "auto": "car",
    "carpool": "carpool", "car-pool": "carpool", "rideshare": "carpool",
    "electric": "ev", "electric-car": "ev",
    "motorbike": "motorcycle", "moto": "motorcycle",
    "subway": "metro", "underground": "metro", "tube": "metro",
    "light-rail": "tram", "streetcar": "tram",
    "rail": "train", "regional": "train",
    "bicycle": "bike", "cycling": "bike", "cycle": "bike",
    "ebike": "e-bike", "ebike": "e-bike",
    "walking": "walk", "foot": "walk",
    "e-scooter": "scooter", "escooter": "scooter",
    "flight": "plane", "flying": "plane", "air": "plane",
}

def canon_mode(name: str) -> str:
    m = (name or "").lower().strip()
    if m in FACTORS:
        return m
    if m in MODE_ALIASES:
        return MODE_ALIASES[m]
    raise SystemExit(f"ERROR: unknown mode '{name}'. Valid: {', '.join(sorted(FACTORS))}")

def load(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {"trips": []}

def save(db, path):
    json.dump(db, open(path, "w"), indent=2)

def trip_co2_kg(mode, km, passengers=1):
    f = FACTORS[mode]
    if mode == "carpool":
        f = f / max(1, passengers)
    return f * km / 1000.0

def iso(d: dt.date):
    return d.isoformat()

# ---------------------------------------------------------------- commands

def cmd_log(a):
    db = load(a.file)
    mode = canon_mode(a.mode)
    km = a.km if a.oneway else a.km * 2
    date = a.date or iso(dt.date.today())
    t = {
        "date": date, "mode": mode, "km": km,
        "passengers": a.passengers, "note": a.note,
        "co2_kg": round(trip_co2_kg(mode, km, a.passengers), 3),
    }
    db["trips"].append(t)
    db["trips"].sort(key=lambda x: x["date"])
    save(db, a.file)
    extra = f" ({a.passengers} pax)" if mode == "carpool" else ""
    print(f"logged {date} {mode}{extra} {km:g} km → {t['co2_kg']:.2f} kg CO2")

def window(db, days=None, month=None):
    trips = db["trips"]
    if month:  # YYYY-MM
        trips = [t for t in trips if t["date"].startswith(month)]
        label = month
    elif days:
        cutoff = iso(dt.date.today() - dt.timedelta(days=days - 1))
        trips = [t for t in trips if t["date"] >= cutoff]
        label = (f"{cutoff} → {iso(dt.date.today())}" if trips else "no trips")
    return trips, label

def report(trips, label, budget=None):
    if not trips:
        print(f"{label}: no trips logged")
        return
    total_km = sum(t["km"] for t in trips)
    total_co2 = sum(t["co2_kg"] for t in trips)
    baseline = trip_co2_kg("car", total_km)
    saved = baseline - total_co2
    pct = (saved / baseline * 100) if baseline > 0 else 0.0
    days_span = (dt.date.fromisoformat(max(t["date"] for t in trips)) -
                 dt.date.fromisoformat(min(t["date"] for t in trips))).days + 1
    print(f"{label}   {len(trips)} trips, {total_km:g} km over {days_span} day(s)")
    print(f"  CO2: {total_co2:.1f} kg   (baseline all-car: {baseline:.1f} kg  →  {pct:.0f}% saved)")
    # per-mode
    agg = {}
    for t in trips:
        m = agg.setdefault(t["mode"], {"kg": 0.0, "n": 0, "km": 0.0})
        m["kg"] += t["co2_kg"]; m["n"] += 1; m["km"] += t["km"]
    print("  by mode:")
    for mode, m in sorted(agg.items(), key=lambda kv: -kv[1]["kg"]):
        bar = "█" * max(1, int(round(m["kg"] / max(total_co2, 0.001) * 15))) if m["kg"] > 0 else ""
        print(f"    {mode:<10} {bar} {m['kg']:.1f} kg  ({m['n']} trips, {m['km']:g} km)")
    # top trips
    print("  top trips:")
    for t in sorted(trips, key=lambda x: -x["co2_kg"])[:3]:
        if t["co2_kg"] <= 0:
            continue
        note = f"   {t['note']}" if t.get("note") else ""
        print(f"    {t['date']} {t['mode']} {t['km']:g} km → {t['co2_kg']:.1f} kg{note}")
    if budget:
        annual = total_co2 / days_span * 365
        status = "✅ under" if annual <= budget else "⚠️ over"
        print(f"  trajectory: {annual/1000:.2f} t/yr — {status} {budget/1000:.2f} t budget")

def cmd_week(a):
    trips, label = window(load(a.file), days=7)
    report(trips, f"Week {label}", budget=a.budget)

def cmd_month(a):
    if a.month:
        trips, label = window(load(a.file), month=a.month)
    else:
        trips, label = window(load(a.file), days=30)
    report(trips, f"Month {label}", budget=a.budget)

def cmd_year(a):
    db = load(a.file)
    budget = a.budget or DEFAULT_BUDGET_KG
    trips, label = window(db, days=365)
    if not trips:
        print("no trips in the last year")
        return
    total = sum(t["co2_kg"] for t in trips)
    total_km = sum(t["km"] for t in trips)
    days_span = (dt.date.today() - dt.date.fromisoformat(min(t["date"] for t in trips))).days + 1
    annualized = total / days_span * 365
    print(f"Logged: {total:.1f} kg over {days_span} days ({total_km:g} km)")
    print(f"Annualized trajectory: {annualized/1000:.2f} t CO2/yr   budget: {budget/1000:.2f} t")
    if annualized <= budget:
        print("✅ on track — headroom " + f"{(budget-annualized)/1000:.2f} t")
    else:
        print(f"⚠️ over budget by {(annualized-budget)/1000:.2f} t/yr "
              f"(≈ {(annualized-budget)*1000/FACTORS['car']:.0f} car-km to cut)")
    trees = annualized / 21.0  # ~21 kg CO2 per urban tree per year (nowadays commonly cited 20-25)
    print(f"equivalence: {trees:.0f} mature urban trees sequester this per year")

def cmd_compare(a):
    print(f"One-way {a.km} km (round trip {a.km*2:g} km), solo unless noted:\n")
    print(f"{'mode':<12} {'g/pkm':>6} {'round-trip kg':>14}")
    for mode in ["walk", "bike", "e-bike", "scooter", "tram", "metro", "coach",
                 "train", "motorcycle", "bus", "ev", "car", "plane"]:
        kg = trip_co2_kg(mode, a.km * 2)
        print(f"{mode:<12} {FACTORS[mode]:>6.0f} {kg:>14.2f}")
    print(f"\ncarpool-3: {trip_co2_kg('carpool', a.km*2, 3):.2f} kg round trip (64 g/pkm)")

def cmd_factors(a):
    print("g CO2 per passenger-km (planning-grade averages):")
    for mode, f in sorted(FACTORS.items(), key=lambda kv: kv[1]):
        extra = "  ÷ passengers (log --passengers N)" if mode == "carpool" else ""
        print(f"  {mode:<12} {f:>6.1f}{extra}")
    print("\nSources synthesized: UK DEFRA/BEIS GHG conversion factors, EEA rail/bus")
    print("averages, EPA auto trends. See references/emission-factors.md.")

def cmd_log_list(a):
    trips = load(a.file)["trips"]
    for t in trips[-a.limit:]:
        note = f"  {t['note']}" if t.get("note") else ""
        print(f"{t['date']} {t['mode']:<10} {t['km']:>6g} km  {t['co2_kg']:>7.2f} kg{note}")
    print(f"({len(trips)} trips total)")

def cmd_export(a):
    trips = load(a.file)["trips"]
    if not trips:
        print("(nothing to export)")
        return
    with open(a.csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "mode", "km", "passengers", "co2_kg", "note"])
        w.writeheader()
        for t in trips:
            w.writerow({k: t.get(k, "") for k in w.fieldnames})
    print(f"exported {len(trips)} trips → {a.csv}")

# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", default=DEFAULT_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("log", help="log a trip (distance doubled unless --oneway)")
    sp.add_argument("--mode", required=True)
    sp.add_argument("--km", type=float, required=True, help="one-way km")
    sp.add_argument("--oneway", action="store_true")
    sp.add_argument("--passengers", type=int, default=1, help="for carpool")
    sp.add_argument("--date", help="YYYY-MM-DD")
    sp.add_argument("--note")
    sp.set_defaults(func=cmd_log)

    sp = sub.add_parser("compare", help="one-off mode comparison, no logging")
    sp.add_argument("--km", type=float, required=True, help="one-way km")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("week", help="last 7 days")
    sp.add_argument("--budget", type=float)
    sp.set_defaults(func=cmd_week)

    sp = sub.add_parser("month", help="last 30 days or --month YYYY-MM")
    sp.add_argument("--month")
    sp.add_argument("--budget", type=float)
    sp.set_defaults(func=cmd_month)

    sp = sub.add_parser("year", help="annualized trajectory vs budget")
    sp.add_argument("--budget", type=float, default=DEFAULT_BUDGET_KG)
    sp.set_defaults(func=cmd_year)

    sp = sub.add_parser("factors", help="emission factors table")
    sp.set_defaults(func=cmd_factors)

    sp = sub.add_parser("log-list", help="recent trips")
    sp.add_argument("--limit", type=int, default=20)
    sp.set_defaults(func=cmd_log_list)

    sp = sub.add_parser("export", help="CSV export")
    sp.add_argument("--csv", default="trips.csv")
    sp.set_defaults(func=cmd_export)

    a = p.parse_args()
    a.func(a)

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # downstream (head/less) closed the pipe — exit quietly
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
