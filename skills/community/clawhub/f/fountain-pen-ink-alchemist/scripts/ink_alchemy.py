#!/usr/bin/env python3
"""
ink_alchemy.py — fountain pen ink mixing, logging, and conversion math.

Commands:
  mix      Dilution math: starting volume + add-water % -> new volume,
           concentration shift, and a dry-time estimate (glycerin and
           humidity aware).
  batch    Record ink batches to ink_log.json (date, components,
           ratios, notes); list existing entries.
  compare  Side-by-side table of two recipes: dry time, flow, wash
           resistance, nib safety, upkeep.
  convert  Drops <-> ml, and pen-fill / page estimates by nib type.

Stdlib only. Offline. Estimates are heuristics for planning, not lab
measurements — always swab-test on the paper you'll actually use.

Exit codes: 0 success, 2 usage or validation error.
"""
import argparse
import json
import math
import os
import sys
from datetime import date

# ─── Dry-time model constants ───
# Base: a standard dye fountain-pen ink on copy paper at 50% RH.
BASE_DRY_S = 20.0
WATER_EXP = 0.85      # dry time scales ~ (new_vol/old_vol) ** 0.85
GLYC_PER_PCT = 1.18   # each +1% glycerin multiplies dry time by ~1.18
DROP_ML = 0.05        # ~20 drops per ml for water-based ink droppers

# ─── Nib profiles ───
# fill_ml: typical standard-converter fill; pages_per_ml: rough A4/lined
# pages of writing per ml for that nib width.
NIBS = {
    "ef":   {"label": "Extra-Fine (EF)", "fill_ml": 0.7, "pages_per_ml": 40},
    "f":    {"label": "Fine (F)",        "fill_ml": 0.8, "pages_per_ml": 33},
    "m":    {"label": "Medium (M)",      "fill_ml": 0.9, "pages_per_ml": 25},
    "b":    {"label": "Broad (B)",       "fill_ml": 1.0, "pages_per_ml": 20},
    "stub": {"label": "Stub 1.1mm",      "fill_ml": 1.1, "pages_per_ml": 14},
}

# ─── Recipe book (heuristic profiles at 50% RH, copy paper) ───
RECIPES = {
    "standard-dye": {
        "dry_s": "~18 s", "flow": "medium", "wash": "low — re-wets fully",
        "nibs": "all nibs incl. EF; the safe default class",
        "upkeep": "flush pen every 4-6 weeks",
        "notes": "dye is dissolved: no particles, no settling",
    },
    "diluted-dye": {
        "dry_s": "~24 s", "flow": "wet", "wash": "very low — feathering risk",
        "nibs": "all nibs; wetter flow helps dry EF/F pens",
        "upkeep": "flush every 4-6 weeks",
        "notes": "+15-25% distilled water: lighter color, more spread",
    },
    "iron-gall": {
        "dry_s": "~12 s", "flow": "medium-dry", "wash": "high after oxidation",
        "nibs": "steel OK short-term; gold safer. Flush after each use",
        "upkeep": "cap tightly, use weekly, flush monthly",
        "notes": "acidic (pH 2-4): eats steel if left to sit",
    },
    "shimmer": {
        "dry_s": "~20 s", "flow": "wet", "wash": "low (dye carrier)",
        "nibs": "BROAD/STUB only — mica particles clog EF/F",
        "upkeep": "swirl (don't shake) before every fill; flush weekly",
        "notes": "particles settle flat in the pen; store nib-up",
    },
    "pigment": {
        "dry_s": "~15 s", "flow": "medium", "wash": "waterproof when dry",
        "nibs": "F/M fine if flushed weekly; EF risky",
        "upkeep": "never let it dry in the pen; weekly flush",
        "notes": "suspended solids, not dissolved — bottle settles too",
    },
    "homemade-no-biocide": {
        "dry_s": "varies", "flow": "varies", "wash": "usually low",
        "nibs": "sacrificial pen ONLY",
        "upkeep": "expect mold in 1-3 weeks without preservative",
        "notes": "water + dye is microbial soup; add a biocide",
    },
    "high-glycerin": {
        "dry_s": "~45 s+", "flow": "very wet", "wash": "low",
        "nibs": "all nibs, but slow-drying on coated papers",
        "upkeep": "watch for smearing; reduce glycerin in summer",
        "notes": "glycerin is a humectant: holds water on the paper",
    },
}


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def rh_multiplier(rh):
    """Dry time roughly doubles from 50% to 90% RH, halves toward 10%."""
    return 2 ** ((rh - 50) / 40)


# ─── mix ───
def cmd_mix(a):
    if a.target_ml <= 0:
        die("--target-ml must be > 0")
    if not 0 < a.add_water_pct <= 100:
        die("--add-water-pct must be in (0, 100]")
    if a.glycerin_pct < 0 or a.glycerin_pct > 10:
        die("--glycerin-pct sensible range is 0-10 (it is % of final volume)")
    if not 5 <= a.rh <= 95:
        die("--rh must be 5-95 (% relative humidity)")

    ratio = 1 + a.add_water_pct / 100.0
    new_vol = a.target_ml * ratio
    water_add = a.target_ml * a.add_water_pct / 100.0
    conc = 100.0 / ratio  # % of original dye concentration

    dilution_mult = ratio ** WATER_EXP
    glyc_mult = GLYC_PER_PCT ** a.glycerin_pct
    hum_mult = rh_multiplier(a.rh)
    dry_s = a.base_dry_s * dilution_mult * glyc_mult * hum_mult

    print(f"Ink dilution — {a.target_ml:g} ml starting volume, "
          f"+{a.add_water_pct:g}% distilled water")
    print(f"  Distilled water to add : {water_add:.2f} ml")
    print(f"  New total volume       : {new_vol:.2f} ml")
    print(f"  Dye concentration      : {conc:.1f}% of original "
          f"({-100 + conc:+.1f}% shift)")
    print()
    print(f"Dry-time estimate (base {a.base_dry_s:g} s, {a.rh:g}% RH):")
    print(f"  Dilution factor  x{dilution_mult:.2f}")
    print(f"  Glycerin factor  x{glyc_mult:.2f} ({a.glycerin_pct:g}% of volume)")
    print(f"  Humidity factor  x{hum_mult:.2f}")
    print(f"  Estimated dry time     : ~{dry_s:.0f} s "
          f"(was ~{a.base_dry_s:g} s)")
    print()
    if a.add_water_pct >= 30:
        print("WARNING: >=30% added water -> washed-out color, feathering,")
        print("         bleedthrough on cheap paper. Stay in the 5-25% band.")
    else:
        print(f"  +{a.add_water_pct:g}% water -> slightly wetter flow; good for")
        print("  dry pens or papers that skip. Color ~1 shade lighter.")
    if a.glycerin_pct >= 5:
        print("WARNING: >=5% glycerin -> smear risk for hours on coated paper.")
    print("  Always use DISTILLED water — tap minerals crust the nib and")
    print("  feed microbes. Swab-test on the target paper before filling.")


# ─── batch ───
def load_log(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        die(f"cannot read log {path}: {exc}")
    if not isinstance(data, list):
        die(f"log {path} is not a JSON list — refusing to overwrite")
    return data


def save_log(path, entries):
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(entries, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError as exc:
        die(f"cannot write log {path}: {exc}")


def cmd_batch(a):
    if a.action == "add":
        if not a.components.strip():
            die("--components is required (e.g. 'ku-jaku 50ml, water 10ml')")
        entries = load_log(a.log)
        entry = {
            "id": max((e.get("id", 0) for e in entries), default=0) + 1,
            "date": date.today().isoformat(),
            "name": a.name.strip() or f"batch-{len(entries) + 1}",
            "components": a.components.strip(),
            "ratio": (a.ratio or "").strip(),
            "notes": (a.notes or "").strip(),
        }
        entries.append(entry)
        save_log(a.log, entries)
        print(f"Logged batch #{entry['id']} -> {a.log}")
        print(f"  date       : {entry['date']}")
        print(f"  name       : {entry['name']}")
        print(f"  components : {entry['components']}")
        if entry["ratio"]:
            print(f"  ratio      : {entry['ratio']}")
        if entry["notes"]:
            print(f"  notes      : {entry['notes']}")
        return
    # list
    entries = load_log(a.log)
    if not entries:
        print(f"No batches in {a.log} — add one with `batch add`.")
        return
    print(f"{len(entries)} batch(es) in {a.log}:")
    for e in entries:
        print(f"  #{e.get('id', '?'):>3} {e.get('date', '????-??-??')}  "
              f"{e.get('name', '(unnamed)')}")
        print(f"        components: {e.get('components', '-')}")
        if e.get("ratio"):
            print(f"        ratio     : {e['ratio']}")
        if e.get("notes"):
            print(f"        notes     : {e['notes']}")


# ─── compare ───
def cmd_compare(a):
    if a.list:
        print("Available recipes:")
        for key, rec in RECIPES.items():
            print(f"  {key:<20} {rec['notes']}")
        return
    for key in (a.recipe_a, a.recipe_b):
        if key not in RECIPES:
            die(f"unknown recipe '{key}' — use `compare --list` to see keys")
    ra, rb = RECIPES[a.recipe_a], RECIPES[a.recipe_b]
    rows = [
        ("Dry time (50% RH)", "dry_s"), ("Flow", "flow"),
        ("Wash resistance", "wash"), ("Nib safety", "nibs"),
        ("Upkeep", "upkeep"), ("Notes", "notes"),
    ]
    w0 = max(len(r[0]) for r in rows)
    w1 = max([len(a.recipe_a)] + [len(str(ra[k])) for _, k in rows])
    w2 = max([len(a.recipe_b)] + [len(str(rb[k])) for _, k in rows])
    prop = "Property"
    header = f"{prop:<{w0}} | {a.recipe_a:<{w1}} | {a.recipe_b:<{w2}}"
    print(header)
    print("-" * len(header))
    for label, key in rows:
        print(f"{label:<{w0}} | {str(ra[key]):<{w1}} | {str(rb[key]):<{w2}}")


# ─── convert ───
def cmd_convert(a):
    if a.nib_table:
        print(f"{'Nib':<18} {'Converter fill':>15} {'Pages per ml':>13}")
        for key in NIBS:
            n = NIBS[key]
            print(f"{key:<4} {n['label']:<13} {n['fill_ml']:>12g} ml "
                  f"{n['pages_per_ml']:>13g}")
        return
    if a.drop_ml <= 0:
        die("--drop-ml must be > 0")
    if a.nib and a.nib not in NIBS:
        die(f"unknown nib '{a.nib}' — choices: {', '.join(NIBS)}")
    if a.drops is None and a.ml is None:
        die("give --drops N or --ml N (or --nib-table)")

    if a.drops is not None:
        ml = a.drops * a.drop_ml
        print(f"{a.drops:g} drops x {a.drop_ml:g} ml/drop = {ml:.2f} ml")
    else:
        ml = a.ml
        drops = ml / a.drop_ml
        print(f"{ml:g} ml / {a.drop_ml:g} ml per drop = {drops:.0f} drops")

    if ml <= 0:
        die("volume must be > 0")
    if a.nib:
        n = NIBS[a.nib]
        fills = ml / n["fill_ml"]
        pages = ml * n["pages_per_ml"]
        print(f"{n['label']}: typical converter fill {n['fill_ml']:g} ml ->")
        print(f"  {fills:.0f} fills from {ml:g} ml")
        print(f"  ~{pages:,.0f} pages of writing (~{n['pages_per_ml']:g} pages/ml)")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("mix", help="dilution + dry-time math")
    m.add_argument("--target-ml", type=float, required=True,
                   help="starting volume of ink (ml)")
    m.add_argument("--add-water-pct", type=float, required=True,
                   help="distilled water to add, %% of starting volume")
    m.add_argument("--glycerin-pct", type=float, default=0.0,
                   help="glycerin as %% of FINAL volume (flow/anti-dry aid)")
    m.add_argument("--rh", type=float, default=50.0,
                   help="room relative humidity %% (default 50)")
    m.add_argument("--base-dry-s", type=float, default=BASE_DRY_S,
                   dest="base_dry_s", help="dry time of the base ink (s)")

    b = sub.add_parser("batch", help="record/list ink batches in ink_log.json")
    b.add_argument("action", choices=["add", "list"])
    b.add_argument("--name", default="", help="batch name")
    b.add_argument("--components", default="",
                   help="e.g. 'ku-jaku 50ml, distilled water 10ml'")
    b.add_argument("--ratio", default="", help="e.g. '5:1'")
    b.add_argument("--notes", default="", help="free text")
    b.add_argument("--log", default="ink_log.json", help="log file path")

    c = sub.add_parser("compare", help="two recipes side by side")
    c.add_argument("recipe_a", nargs="?", help="recipe key")
    c.add_argument("recipe_b", nargs="?", help="recipe key")
    c.add_argument("--list", action="store_true", dest="list",
                   help="list available recipes")

    v = sub.add_parser("convert", help="drops<->ml, fills & pages by nib")
    v.add_argument("--drops", type=float, help="drop count -> ml")
    v.add_argument("--ml", type=float, help="millilitres -> drops")
    v.add_argument("--drop-ml", type=float, default=DROP_ML, dest="drop_ml",
                   help=f"ml per drop (default {DROP_ML})")
    v.add_argument("--nib", choices=list(NIBS),
                   help="estimate fills/pages for this nib")
    v.add_argument("--nib-table", action="store_true", dest="nib_table",
                   help="print the nib reference table")

    a = ap.parse_args()
    {"mix": cmd_mix, "batch": cmd_batch,
     "compare": cmd_compare, "convert": cmd_convert}[a.cmd](a)


if __name__ == "__main__":
    main()
