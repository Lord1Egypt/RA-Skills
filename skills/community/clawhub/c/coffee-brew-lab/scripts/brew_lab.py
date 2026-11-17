#!/usr/bin/env python3
"""Coffee Brew Lab — recipe math, taste diagnosis, brew-log analysis.

Engines:
  recipe   SCA golden-ratio water/coffee math per method, grind/temp/dwell
           profiles, pour schedules, altitude-corrected temperatures.
  diagnose defect -> single-variable parameter move (one change per cup).
  log      brew journal with per-variable correlation of score vs settings.

Stdlib only. Brew log: brew_log.json next to script (--store overrides).
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import date
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "brew_log.json"

CUP_ML = 240  # a "cup" of filter coffee, SCA-style (not the 5oz mug)

METHODS = {
    "v60": {
        "name": "Pour-over (V60/Chemex)", "ratio": 16.0, "grind": "medium-fine (table salt, fine side)",
        "temp_c": [92, 96], "dwell": "2:30-3:30 total drawdown",
        "steps": ["rinse filter, preheat vessel, discard water",
                  "bloom: pour 2-3x coffee weight, swirl, wait 45s",
                  "pour to 60% of water by 1:15 in 1-2 pours",
                  "finish pouring by 2:00; flat bed at end"]},
    "french-press": {
        "name": "French press", "ratio": 15.0, "grind": "coarse (~1000-1400 µm)",
        "temp_c": [93, 96], "dwell": "4:00 steep + 2:00 settle",
        "steps": ["add coffee, pour all water off-boil-ish in 30s",
                  "at 4:00 break crust, skim foam",
                  "wait 2:00, press slowly, decant ALL coffee immediately"]},
    "aeropress": {
        "name": "AeroPress", "ratio": 13.0, "grind": "medium-fine",
        "temp_c": [85, 92], "dwell": "1:30-2:00 incl. 20-30s press",
        "steps": ["(optional paper+metal combo for clarity)",
                  "pour to line, stir 3x at 10s",
                  "press gently 20-30s, stop at the hiss"]},
    "cold-brew": {
        "name": "Cold brew (concentrate)", "ratio": 8.0, "grind": "extra-coarse",
        "temp_c": [18, 22], "dwell": "12-18h room temp",
        "steps": ["combine, stir, cover",
                  "steep 12-18h (16h sweet spot)",
                  "strain, dilute 1:1 with water or milk to serve"]},
    "moka": {
        "name": "Moka pot", "ratio": 10.0, "grind": "fine, NOT espresso-fine",
        "temp_c": [0, 0], "dwell": "slow stream, off heat at gurgle",
        "steps": ["fill base to valve, water just off cold",
                  "basket full, level, NO tamping",
                  "low-medium heat; slow lazy stream is the goal",
                  "cool base under tap at first gurgle, serve now"]},
    "espresso": {
        "name": "Espresso", "ratio": 2.0, "grind": "fine",
        "temp_c": [90, 94], "dwell": "25-32s",
        "steps": ["dose 18g, distribute (WDT), level tamp",
                  "target 36g out (1:2)",
                  "adjust grind first; dose is last resort"]},
}

DIAGNOSES = {
    "bitter": ("over-extraction",
               ["grind 1-2 clicks COARSER (first choice)",
                "water 3-5°C COOLER",
                "shorten dwell / faster drawdown",
                "reduce agitation (fewer pours/stirs)"]),
    "sour": ("under-extraction",
             ["grind 1-2 clicks FINER (first choice)",
              "water 3-5°C HOTTER",
              "longer dwell",
              "more agitation (extra pour/stir)"]),
    "weak": ("under-strength (ratio, not extraction)",
             ["more coffee: ratio 1:16 -> 1:15 (e.g. 15g -> 16g per 240g)",
              "do NOT change grind — that's the other axis"]),
    "harsh": ("over-strength (ratio, not extraction)",
              ["less coffee: ratio 1:15 -> 1:16",
               "or dilute the cup 10% and re-taste before changing anything"]),
    "sour-and-bitter": ("uneven extraction / channeling",
                        ["fix distribution: WDT, level tamp, even pours",
                         "check grinder for bimodal output (fines+boulders)",
                         "do NOT touch temperature yet — it masks, not fixes"]),
    "hollow": ("staleness or under-dose",
               ["check roast date: ideal window 7-45 days off roast",
                "dose +10%",
                "if papery: rinse filters; if still hollow with fresh beans: water chemistry"]),
    "astringent": ("late over-extraction / dirty equipment",
                   ["shorten dwell",
                    "deep-clean the brewer (rancid oils read as bitter)",
                    "coarser grind if the stream ran slow"]),
}

DEFECT_ALIASES = {
    "dry": "bitter", "harsh-bitter": "bitter", "grassy": "sour", "salty": "sour",
    "thin": "weak", "watery": "weak", "intense": "harsh", "papery": "hollow",
    "boring": "hollow", "drying": "astringent", "both": "sour-and-bitter",
}


def boil_point(altitude_m: int) -> float:
    return 100.0 - altitude_m / 300.0


def fmt_mmss(sec: int) -> str:
    return f"{sec // 60}:{sec % 60:02d}"


# ------------------------------------------------------------------ recipe
def cmd_recipe(args) -> None:
    m = METHODS[args.method]
    ratio = args.ratio or m["ratio"]
    if args.grams:
        coffee = args.grams
        water = round(coffee * ratio)
    elif args.cups:
        water = args.cups * CUP_ML
        coffee = round(water / ratio, 1)
    elif args.liters:
        water = args.liters * 1000
        coffee = round(water / ratio, 1)
    else:
        sys.exit("Give --cups, --grams, or --liters")

    print(f"┌─ {m['name']} ─ ratio 1:{ratio:g}")
    print(f"│  coffee {coffee}g   water {water}g"
          + (f"  (≈{water / CUP_ML:.0f} cups)" if water >= CUP_ML else ""))
    print(f"│  grind: {m['grind']}")
    if m["temp_c"][1] > 0:
        lo, hi = m["temp_c"]
        note = ""
        if args.altitude:
            boil = boil_point(args.altitude)
            hi = min(hi, round(boil - 2))
            lo = min(lo, hi)
            note = f"  (altitude-capped: boil ≈ {boil:.0f}°C at {args.altitude}m)"
        print(f"│  water: {lo}-{hi}°C{note}")
    print(f"│  time: {m['dwell']}")
    if args.method == "v60":
        bloom = round(coffee * 2.5)
        p60 = round(water * 0.6)
        print(f"│  bloom: {bloom}g water, 45s swirl")
        print(f"│  pour:  0:45→{p60}g (60%), by 2:00→{water}g total")
    if args.method == "espresso":
        out = round(coffee * 2)
        print(f"│  target: {coffee}g in -> {out}g out in 25-32s")
    if args.method == "cold-brew":
        print(f"│  serve: dilute concentrate 1:1 (makes ≈{2 * water / CUP_ML:.0f} cups)")
    print("└─ method:")
    for s in m["steps"]:
        print(f"   • {s}")
    print("\nChange ONE variable per cup. Log every brew (log add).")


# ------------------------------------------------------------------ diagnose
def cmd_diagnose(args) -> None:
    key = args.defect.lower().strip().replace("_", "-")
    key = DEFECT_ALIASES.get(key, key)
    if key not in DIAGNOSES:
        sys.exit(f"Unknown defect '{args.defect}'. Known: " + ", ".join(DIAGNOSES))
    axis, moves = DIAGNOSES[key]
    print(f"“{key}” reads as: {axis}\n")
    print("Moves, in order of usual effectiveness (pick ONE this cup):")
    for i, mv in enumerate(moves, 1):
        print(f"  {i}. {mv}")
    print("\nRe-brew, re-taste, log both cups. Change one variable at a time.")


# ------------------------------------------------------------------ log
def load_log(store: Path) -> list:
    if store.exists():
        return json.loads(store.read_text())
    return []


def cmd_log(args) -> None:
    store = args.store
    entries = load_log(store)
    if args.sub == "add":
        e = {"date": date.today().isoformat(), "method": args.method,
             "bean": args.bean, "grams": args.grams, "water": args.water,
             "ratio": round(args.water / args.grams, 1) if args.grams and args.water else None,
             "grind": args.grind, "temp": args.temp, "dwell_s": args.dwell,
             "score": args.score, "tags": [t.strip() for t in args.tags.split(",") if t.strip()]}
        entries.append(e)
        store.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n")
        print(f"Logged brew #{len(entries)}: {args.method} "
              f"1:{e['ratio']} grind {args.grind} {args.temp}°C "
              f"{fmt_mmss(args.dwell)} — {args.score}/10"
              + (f" [{args.tags}]" if args.tags else ""))
    elif args.sub == "best":
        if not entries:
            sys.exit("Log empty.")
        top = sorted(entries, key=lambda e: -e["score"])[:5]
        print("Top cups:")
        for e in top:
            print(f"  {e['score']}/10  {e['date']} {e['method']:12} "
                  f"1:{e['ratio']} grind {e['grind']} {e['temp']}°C "
                  f"{fmt_mmss(e['dwell_s'])} {e.get('bean') or ''}")
    elif args.sub == "analyze":
        if len(entries) < 4:
            sys.exit(f"Only {len(entries)} brews logged — need ≥4 for analysis.")
        scores = [e["score"] for e in entries]
        print(f"{len(entries)} brews, mean score {statistics.mean(scores):.1f}\n")
        for var, get in (("grind", lambda e: e["grind"]), ("temp", lambda e: e["temp"]),
                         ("dwell", lambda e: e["dwell_s"]), ("ratio", lambda e: e["ratio"])):
            pairs = [(get(e), e["score"]) for e in entries if get(e) is not None]
            if len(pairs) < 4:
                continue
            xs, ys = zip(*pairs)
            if len(set(xs)) < 2:
                print(f"  {var:6}: constant ({xs[0]}) — change it to learn anything")
                continue
            r = pearson(xs, ys)
            direction = "higher score at HIGHER values" if r > 0 else "higher score at LOWER values"
            conf = "strong" if abs(r) >= 0.6 else "moderate" if abs(r) >= 0.35 else "weak"
            print(f"  {var:6}: r={r:+.2f} ({conf}) — {direction}")
        print("\nNote: correlations are per-bean. Re-analyze when beans change.")


def pearson(xs, ys) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


# ------------------------------------------------------------------ cli
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default=str(DEFAULT_STORE))
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("recipe", help="water/coffee math + method profile")
    sp.add_argument("--method", required=True, choices=METHODS.keys())
    sp.add_argument("--cups", type=int, help="240ml cups (filter methods)")
    sp.add_argument("--grams", type=float, help="coffee grams (drives water)")
    sp.add_argument("--liters", type=float, help="water liters (cold brew)")
    sp.add_argument("--ratio", type=float, help="override (e.g. 16 for 1:16)")
    sp.add_argument("--altitude", type=int, help="meters above sea level")
    sp.set_defaults(fn=cmd_recipe)

    sp = sub.add_parser("diagnose", help="defect -> single-variable move")
    sp.add_argument("defect", help="bitter|sour|weak|harsh|sour-and-bitter|hollow|astringent")
    sp.set_defaults(fn=cmd_diagnose)

    sp = sub.add_parser("log")
    log_sub = sp.add_subparsers(dest="sub", required=True)
    add = log_sub.add_parser("add")
    add.add_argument("--method", required=True)
    add.add_argument("--bean", default="")
    add.add_argument("--grams", type=float, required=True)
    add.add_argument("--water", type=float, required=True)
    add.add_argument("--grind", type=float, required=True, help="YOUR grinder's setting")
    add.add_argument("--temp", type=float, required=True)
    add.add_argument("--dwell", type=int, required=True, help="seconds")
    add.add_argument("--score", type=int, required=True, help="1-10")
    add.add_argument("--tags", default="", help="comma defects e.g. bitter,sour")
    best = log_sub.add_parser("best")
    ana = log_sub.add_parser("analyze")
    sp.set_defaults(fn=cmd_log)

    args = p.parse_args()
    args.store = Path(args.store)
    args.fn(args)


if __name__ == "__main__":
    main()
