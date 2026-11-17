#!/usr/bin/env python3
"""canning-safety-ranger — recipe screening, altitude corrections, jar triage.

Modes:
  --demo                     run the full demo battery
  --screen --food F --method M [--altitude FT] [--tested]
                             screen a plan: verdict + violated rules + corrections
  --time JARS METHOD BASE_MIN ALT_FT
                             altitude-corrected water-bath time
  --pressure JARS PSI ALT_FT [dial|weighted]
                             altitude-corrected pressure-can settings
  --jar SIGN [low-acid|high-acid]
                             suspect-jar triage verdict

Stdlib only.
"""
from __future__ import annotations

import argparse
import re

# ------------------------------------------------------------- food classes
# class: acid (<4.6), borderline (tomatoes), low-acid (>=4.6)
FOOD_DB = {
    "jam": ("acid", "water-bath"), "jelly": ("acid", "water-bath"),
    "strawberries": ("acid", "water-bath"), "applesauce": ("acid", "water-bath"),
    "apples": ("acid", "water-bath"), "peaches": ("acid", "water-bath"),
    "pears": ("acid", "water-bath"), "cherries": ("acid", "water-bath"),
    "pickles": ("acid-if-brine", "water-bath"),
    "tomatoes": ("borderline", "water-bath+acid"),
    "tomato sauce": ("borderline", "water-bath+acid or pressure"),
    "tomato juice": ("borderline", "water-bath+acid"),
    "salsa": ("mixed", "tested-recipe-only"),
    "green beans": ("low-acid", "pressure"), "beans": ("low-acid", "pressure"),
    "corn": ("low-acid", "pressure"), "potatoes": ("low-acid", "pressure"),
    "carrots": ("low-acid", "pressure"), "peas": ("low-acid", "pressure"),
    "beets": ("low-acid", "pressure (pickled beets = acid path w/ tested brine)"),
    "chicken": ("low-acid", "pressure"), "beef": ("low-acid", "pressure"),
    "meat": ("low-acid", "pressure"), "stock": ("low-acid", "pressure"),
    "broth": ("low-acid", "pressure"), "soup": ("low-acid/mixed", "pressure (tested recipes only)"),
    "fish": ("low-acid", "pressure"), "salmon": ("low-acid", "pressure"),
    "pumpkin butter": ("NEVER", "no safe home process (density)"),
    "pureed squash": ("NEVER", "no safe home process (density)"),
    "pesto": ("NEVER", "oil + low acid = botulism risk, no process"),
    "butter": ("NEVER", "fat + dairy: not home-cannable"),
    "cream soup": ("NEVER", "dairy: not home-cannable"),
    "cake in a jar": ("NEVER", "internet trend, refuse"),
    "nut meats": ("NEVER", "oil + low acid"),
}

NEVER_KEYWORDS = ("pumpkin butter", "pureed squash", "squash puree", "pesto", "butter",
                  "cream soup", "cake in a jar", "cake-in-a-jar", "nut meats", "avocado",
                  "banana puree", "eggs")
LOW_ACID_KEYWORDS = ("green bean", "beans", "corn", "potato", "carrot", "pea", "beet",
                     "chicken", "beef", "meat", "stock", "broth", "soup", "fish",
                     "salmon", "venison", "pork", "turkey", "duck", "clam", "oyster")
THICKENER_KEYWORDS = ("flour", "rice", "pasta", "noodles", "roux", "cornstarch",
                      "tapioca", "breadcrumb")


def classify_food(food: str) -> tuple[str, str, str]:
    """returns (class, required method, matched key)"""
    f = food.lower().strip()
    def has(kw):  # whole-word match with optional plural, so 'pea' never matches 'peaches'
        return re.search(r"\b" + re.escape(kw) + r"(s|es)?\b", f) is not None
    for kw in NEVER_KEYWORDS:
        if has(kw):
            return "NEVER", "none", kw
    if "tomato" in f and any(k in f for k in ("salsa", "sauce", "juice", "crushed", "whole")):
        if "salsa" in f:
            return "mixed", "tested-recipe-only", "salsa"
        return "borderline", "water-bath+acid", "tomato"
    if "salsa" in f or "picante" in f or "relish" in f or "chutney" in f:
        return "mixed", "tested-recipe-only", "mixed-condiment"
    if "pickle" in f or "brine" in f:
        return "acid-if-brine", "water-bath (tested brine)", "pickle"
    for kw in LOW_ACID_KEYWORDS:
        if has(kw):
            return "low-acid", "pressure", kw
    for name, (cls, method) in FOOD_DB.items():
        if name in f:
            return cls, method, name
    for kw in THICKENER_KEYWORDS:
        if has(kw):
            return "NEVER", f"thickener ({kw}) breaks heat penetration — add when reheating", kw
    return "unknown", "look up a tested process (NCHFP) before proceeding", "?"


# --------------------------------------------------------- altitude engine
def wb_altitude_time(base_min: int, alt_ft: int) -> int:
    """USDA ladder: +5 min per 1,000 ft above 1,000 ft."""
    if alt_ft <= 1000:
        return base_min
    extra = 5 * ((alt_ft - 1) // 1000)  # 1001-3000 -> +5 ... matches ladder bands
    return base_min + extra


def pressure_at_altitude(alt_ft: int, gauge: str = "dial") -> int:
    """psi target. dial: 11 + 1 per 2,000 over sea; weighted: 10 -> 15 above 2,000."""
    if gauge == "weighted":
        return 15 if alt_ft > 2000 else 10
    return 11 + (alt_ft // 2000) if alt_ft % 2000 == 0 and alt_ft > 0 else 11 + (alt_ft // 2000)


# pressure ladder per references: 0-2000:11, 2001-4000:12, 4001-6000:13 ...
def pressure_dial(alt_ft: int) -> int:
    if alt_ft <= 2000:
        return 11
    return 11 + (alt_ft - 1) // 2000


# ---------------------------------------------------------------- screening
def screen(food: str, method: str, altitude: int = 0, tested: bool = False,
           thickeners: bool = False) -> dict:
    cls, req, key = classify_food(food)
    method = (method or "").lower()
    violations, corrections = [], []
    # auto-detect thickeners named in the food description itself
    fl = food.lower()
    if not thickeners and any(re.search(r"\b" + re.escape(kw), fl)
                              for kw in THICKENER_KEYWORDS):
        thickeners = True

    if cls == "NEVER":
        return {"food": food, "verdict": "NEVER-CAN", "class": cls,
                "why": req,
                "action": "No safe home process exists. Freeze or refrigerate instead."}

    if cls == "low-acid" and "pressure" not in method and method:
        violations.append("RULE 1: low-acid food + water-bath/steam = botulism risk")
        corrections.append(f"Pressure-can only (dial {pressure_dial(altitude)} psi at "
                           f"{altitude:,} ft, or weighted gauge per ladder)")
    if cls == "borderline" and method in ("water-bath", "water bath", "water-bath-canner"):
        if not tested:
            violations.append("RULE 2: tomatoes are pH 4.3-4.9 — acidify every jar")
        corrections.append("Add 2 Tbsp bottled lemon juice or 1/4 tsp citric acid per QUART "
                           "(1 Tbsp / 1/8 tsp per pint) directly in the jar")
    if cls == "mixed" and not tested:
        violations.append("RULE 3: mixed-acid condiment without a tested recipe — veg ratios shift pH")
        corrections.append("Use an NCHFP/Ball tested recipe verbatim; no ingredient substitutions")
    if cls == "unknown":
        corrections.append("No classification — find the exact tested process before canning")
    if thickeners:
        violations.append("RULE 6: thickener (flour/rice/pasta/cornstarch) in the jar")
        corrections.append("Can without it; thicken at reheat time")

    alt_note = ""
    if altitude > 1000:
        if "pressure" in (req + method) or cls == "low-acid":
            corrections.append(f"Altitude {altitude:,} ft: use dial {pressure_dial(altitude)} psi "
                               f"or weighted {'15 lb' if altitude > 2000 else '10 lb'}")
        else:
            alt_note = (f"Water-bath time at {altitude:,} ft = base + "
                        f"{wb_altitude_time(0, altitude)} min (USDA ladder)")

    verdict = "SAFE" if not violations else "UNSAFE-AS-PLANNED"
    return {"food": food, "class": cls, "required": req,
            "verdict": verdict,
            "violations": violations or ["none"],
            "corrections": corrections or ["proceed with a tested process"],
            "altitude_note": alt_note or f"altitude correction at {altitude:,} ft applied"}


# ------------------------------------------------------------- jar triage
TRIAGE = {
    "bulging-lid": ("DISCARD", "gas from microbial growth inside — toxin-risk spoilage"),
    "domed-lid": ("DISCARD", "same as bulging: gas production means process failure"),
    "unsealed": ("REFRIGERATE-OR-REPROCESS",
                 "if <24h since canning: reprocess with new lid (full time); else refrigerate & eat within days"),
    "mold": ("DISCARD", "mold roots penetrate soft products beyond the visible spot"),
    "fizz": ("DISCARD", "in-jar fermentation = brine/acid failure"),
    "smell": ("DISCARD", "odor means OTHER spoilage; on low-acid jars assume process failure"),
    "cloudy": ("DISCARD if also fizz/smell; otherwise discard for pickles, OK for some",
               "cloudy pickles brine = fermentation continued"),
    "good-seal": ("EAT", "concave lid, clean contents — within 12-18 months for quality"),
}


def triage(sign: str, food_class: str) -> dict:
    key = sign.lower().strip()
    verdict, why = TRIAGE.get(key, ("DISCARD", "unknown sign — when in doubt, out it goes"))
    if verdict == "DISCARD" and food_class == "low-acid":
        why += " — botulism toxin is odorless; never taste-test a suspect low-acid jar"
    return {"sign": sign, "verdict": verdict, "why": why,
            "discard_protocol": "Open under water in a bucket, bleach surfaces, do not taste."}


# ------------------------------------------------------------------- demo
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--screen", action="store_true")
    p.add_argument("--food")
    p.add_argument("--method")
    p.add_argument("--altitude", type=int, default=0)
    p.add_argument("--tested", action="store_true")
    p.add_argument("--thickeners", action="store_true")
    p.add_argument("--time", nargs=4, metavar=("JARS", "METHOD", "BASE_MIN", "ALT_FT"))
    p.add_argument("--pressure", nargs=4, metavar=("JARS", "PSI", "ALT_FT", "GAUGE"))
    p.add_argument("--jar", nargs=2, metavar=("SIGN", "FOOD_CLASS"))
    args = p.parse_args()

    if args.demo:
        cases = [
            ("green beans", "water-bath", 5000, False),
            ("tomato sauce", "water-bath", 0, False),
            ("salsa", "water-bath", 3000, False),
            ("peaches", "water-bath", 5000, True),
            ("pumpkin butter", "water-bath", 0, False),
            ("chicken stock", "pressure", 6500, True),
        ]
        for food, method, alt, tested in cases:
            r = screen(food, method, alt, tested)
            print(f"{food.upper():<18} -> {r['verdict']}")
            for v in r.get("violations", [])[:2]:
                print(f"   ! {v}")
            for c in r.get("corrections", [])[:2]:
                print(f"   fix: {c}")
            print()
        print("JAR TRIAGE 'bulging-lid' on low-acid:",
              triage("bulging-lid", "low-acid")["verdict"])
        print("JAR TRIAGE 'unsealed':", triage("unsealed", "acid")["verdict"])
        print(f"\nWATER BATH 35 min base @ 5,000 ft -> {wb_altitude_time(35, 5000)} min")
        print(f"PRESSURE dial @ 5,000 ft -> {pressure_dial(5000)} psi")
        return

    if args.screen:
        if not args.food:
            p.error("--screen requires --food")
        import json
        print(json.dumps(screen(args.food, args.method, args.altitude, args.tested,
                                args.thickeners), indent=2))
        return

    if args.time:
        jars, method, base, alt = args.time
        print(f"{jars}, {method}: {base} min @ sea level -> "
              f"{wb_altitude_time(int(base), int(alt))} min @ {int(alt):,} ft")
        return

    if args.pressure:
        jars, psi, alt, gauge = args.pressure
        if gauge == "weighted":
            w = 15 if int(alt) > 2000 else 10
            print(f"{jars} @ {int(alt):,} ft, weighted gauge: use {w} lb weight "
                  f"(base {psi} psi ignored — weighted uses the ladder)")
        else:
            print(f"{jars} @ {int(alt):,} ft, dial gauge: {pressure_dial(int(alt))} psi "
                  f"(base {psi})")
        return

    if args.jar:
        import json
        print(json.dumps(triage(*args.jar), indent=2))
        return

    p.print_help()


if __name__ == "__main__":
    main()
