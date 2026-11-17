#!/usr/bin/env python3
"""camping-loadout-planner — condition-driven gear list, sleep-system math, weight audit.

Modes:
  --demo            full demo: 34F shoulder-season 2-nighter with a tight sleep stack
  --trip trip.json  your trip (see trip.example.json)
  --sleep LOW_F BAG_COMFORT_F PAD_R [LINER_F]
                    sleep-system verdict for a forecast low
  --budget BASE_LB CLASS   check base weight vs class budget + cut suggestions from demo list

Stdlib only.
"""
from __future__ import annotations

import argparse
import json

# ------------------------------------------------------------ sleep system
def required_bag_comfort(forecast_low_f: float, clear_sky: bool = False,
                         altitude_ft: int = 0) -> float:
    """bag comfort needed = low - 5F base margin - radiative - lapse corrections."""
    req = forecast_low_f - 5
    if clear_sky:
        req -= 3  # radiative cooling under clear calm skies
    if altitude_ft > 0:
        req -= 3.5 * (altitude_ft / 1000) * 0.35  # valley forecasts under-read summits
    return round(req, 1)


def pad_verdict(pad_r: float, night_low_f: float) -> dict:
    if night_low_f <= 25 and pad_r < 5:
        return {"verdict": "PAD TOO COLD", "why": f"R {pad_r} under {night_low_f:.0f}F — need R 5+ "
                "(stack a cheap foam pad under it: R adds)"}
    if night_low_f <= 32 and pad_r < 4:
        return {"verdict": "PAD MARGINAL", "why": f"R {pad_r} at freezing — add foam (R adds) "
                "or accept a cold night"}
    if night_low_f <= 45 and pad_r < 2:
        return {"verdict": "PAD MARGINAL", "why": f"R {pad_r} below 45F — summer pad at 3-season temps"}
    return {"verdict": "PAD OK", "why": f"R {pad_r} adequate for {night_low_f:.0f}F nights"}


def sleep_verdict(forecast_low_f, bag_comfort_f, pad_r, liner_add_f=0,
                  clear_sky=False, altitude_ft=0):
    req = required_bag_comfort(forecast_low_f, clear_sky, altitude_ft)
    stack = bag_comfort_f - (10 if pad_r < 2 else 0) + liner_add_f  # pad deficit penalty
    margin = round(stack - req, 1)
    return {
        "required_comfort_f": req,
        "stack_effective_f": stack,
        "margin_f": margin,
        "verdict": "SLEEP OK" if margin >= 2 else ("SLEEP TIGHT — OK" if margin >= 0 else "SLEEP RISK"),
        "pad": pad_verdict(pad_r, forecast_low_f),
        "advice": ("Comfortable margin." if margin >= 5 else
                   "Tight — wear your puffy to bed (+5-10F) or add a liner (+8-10F)." if margin >= 0 else
                   "You will be cold. Add liner + sleepwear layers, or a warmer bag/pad."),
    }


# ------------------------------------------------------------ weight audit
BUDGETS = {"traditional": (30, 45), "lightweight": (20, 30),
           "ultralight": (10, 20), "super-ul": (0, 10)}


def weight_audit(items: list, trek_class: str, body_weight_lb: float,
                 consumables_lb: float = 0.0):
    base = sum(i["oz"] for i in items) / 16
    lo, hi = BUDGETS[trek_class]
    total = base + consumables_lb
    over = base - hi
    cuts = []
    if over > 0:
        # rank by oz per "just-in-case" probability — heuristic: cut duplicates & low-use first
        ranked = sorted(items, key=lambda i: (i.get("dup", 0), -i["oz"]))
        for i in ranked:
            if over <= 0:
                break
            if i.get("essential"):
                continue
            cuts.append(i["name"])
            over -= i["oz"] / 16
    return {
        "base_weight_lb": round(base, 1),
        "class_budget": f"{lo}-{hi} lb",
        "verdict": "WITHIN BUDGET" if base <= hi else f"OVER by {base - hi:.1f} lb",
        "cut_list": cuts,
        "total_pack_lb": round(total, 1),
        "body_check": ("OK" if total <= 0.20 * body_weight_lb else
                       f"OVER 20% body weight ({0.20 * body_weight_lb:.0f} lb ceiling)"),
    }


# --------------------------------------------------------- trip pipeline
def derive_gear(trip: dict) -> list:
    """condition flags -> gear categories with reasons."""
    gear = []
    low = trip["forecast_low_f"]
    def add(cat, item, why):
        gear.append({"category": cat, "item": item, "why": why})
    # shelter
    if trip.get("precip_pct", 30) >= 30:
        add("shelter", "rainfly + pack liner + rain jacket", f"precip {trip['precip_pct']}%")
    if trip.get("bug_season"):
        add("shelter", "headnet + full-mesh tent intact", "bug season")
    # sleep
    add("sleep", f"bag/pad/liner stack for {required_bag_comfort(low, trip.get('clear_sky', False), trip.get('altitude_ft', 0)):.0f}F",
        "derived from forecast low - 5F margin")
    if low <= 40:
        add("sleep", "beanie + dry sleep socks", "sub-40F nights")
    # insulation
    if low <= 35: add("clothing", "mid puffy + gloves", "static camp hours at 35F-")
    elif low <= 45: add("clothing", "light puffy or heavy fleece", "static camp at 45F-")
    if trip.get("precip_pct", 0) >= 40:
        add("clothing", "NO cotton — synthetic/wool base layers", "wet cooling risk")
    # water
    gap = trip.get("water_gap_mi", 3)
    if gap >= 6:
        add("water", "4-6 L capacity + electrolytes", f"sources {gap} mi apart")
    else:
        add("water", "2 L capacity + filter + backup tabs", f"sources every {gap} mi")
    # kitchen
    ppl = trip.get("people", 2)
    nights = trip.get("nights", 2)
    fuel_g = 11 * ppl * nights
    add("kitchen", f"canister {fuel_g:.0f} g fuel (110g canister fits: {fuel_g <= 110})",
        "11 g/person-day, 2 boils + coffee")
    add("kitchen", f"food {1.8 * ppl * nights:.1f} lb total", "1.8 lb/person-day default")
    # bear
    if trip.get("bear_country") == "sierra":
        add("food-storage", "canister MANDATORY (Garcia/Bearikade)", "Sierra rule")
    elif trip.get("bear_country") == "grizzly":
        add("food-storage", "IGBC canister", "grizzly country")
    elif trip.get("bear_country"):
        add("food-storage", "ursack or 12ft/6ft hang kit", "black bear country")
    # fire
    if trip.get("fire_ban"):
        add("kitchen", "stove-only meal plan", "fire ban active")
    return gear


DEMO_TRIP = {
    "name": "Shoulder-season 2-nighter",
    "nights": 2, "people": 2,
    "forecast_low_f": 34, "precip_pct": 30, "bug_season": False,
    "water_gap_mi": 4, "altitude_ft": 0, "clear_sky": True,
    "bear_country": "black", "fire_ban": False,
    "trek_class": "lightweight", "body_weight_lb": 170,
    "gear": [
        {"name": "20F-limit bag (~29F comfort)", "oz": 38, "essential": True},
        {"name": "R-2 air pad", "oz": 14, "essential": True},
        {"name": "silk liner", "oz": 5, "essential": False},
        {"name": "2P tent", "oz": 56, "essential": True},
        {"name": "canister stove", "oz": 3, "essential": True},
        {"name": "second knife", "oz": 6.4, "dup": 1},
        {"name": "steel mug (dup of titanium)", "oz": 4.8, "dup": 1},
        {"name": "first-aid kit", "oz": 6, "essential": True},
        {"name": "headlamp + spare batteries", "oz": 4, "essential": True},
        {"name": "water filter + tabs", "oz": 3.5, "essential": True},
        {"name": "power bank 10Ah", "oz": 6.9, "essential": False},
        {"name": "rain jacket", "oz": 7, "essential": True},
        {"name": "puffy", "oz": 11, "essential": True},
        {"name": "tp + trowel + soap", "oz": 3, "essential": True},
    ],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--trip", help="trip JSON")
    p.add_argument("--sleep", nargs=3, metavar=("LOW_F", "BAG_COMFORT_F", "PAD_R"))
    p.add_argument("--sleep-liner", type=float, default=0, help="liner boost F (with --sleep)")
    p.add_argument("--budget", nargs=2, metavar=("BASE_LB", "CLASS"))
    args = p.parse_args()

    if args.demo or args.trip:
        trip = DEMO_TRIP
        if args.trip:
            with open(args.trip) as f:
                trip = json.load(f)
        print(f"TRIP: {trip.get('name', '?')} — {trip['nights']} nights, {trip['people']} people, "
              f"low {trip['forecast_low_f']}F, precip {trip.get('precip_pct', '?')}%\n")
        print("DERIVED GEAR LIST")
        cat = None
        for g in derive_gear(trip):
            if g["category"] != cat:
                cat = g["category"]
                print(f"  [{cat}]")
            print(f"    - {g['item']:<46} ({g['why']})")
        # sleep verdict from gear if present
        bag = next((i for i in trip.get("gear", []) if "bag" in i["name"]), None)
        pad = next((i for i in trip.get("gear", []) if "pad" in i["name"]), None)
        liner = next((i for i in trip.get("gear", []) if "liner" in i["name"]), None)
        print("\nSLEEP SYSTEM")
        if bag and pad:
            import re as _re
            # prefer the explicit comfort rating ("~29F comfort") over a limit ("20F-limit")
            bag_m = (_re.search(r"(\d+(?:\.\d+)?)F\s*comfort", bag["name"])
                     or _re.search(r"comfort[^\d]*(\d+(?:\.\d+)?)", bag["name"])
                     or _re.search(r"(\d+)F", bag["name"]))
            pad_m = _re.search(r"R-?(\d+(?:\.\d+)?)", pad["name"])
            if bag_m and pad_m:
                bag_c = float(bag_m.group(1))
                pad_r = float(pad_m.group(1))
                sv = sleep_verdict(trip["forecast_low_f"], bag_c, pad_r,
                                   9 if liner else 0, trip.get("clear_sky", False),
                                   trip.get("altitude_ft", 0))
                print(f"  stack {sv['stack_effective_f']}F vs required {sv['required_comfort_f']}F "
                      f"-> {sv['verdict']} (margin {sv['margin_f']}F)")
                print(f"  pad: {sv['pad']['verdict']}")
                print(f"  {sv['advice']}")
            else:
                print("  (could not parse bag rating or pad R from gear names)")
        if trip.get("gear"):
            print("\nWEIGHT AUDIT")
            food_lb = 1.8 * trip["people"] * trip["nights"]
            water_lb = 2 * 2.2  # 2L day-1
            wa = weight_audit(trip["gear"], trip["trek_class"], trip["body_weight_lb"],
                              food_lb + water_lb)
            print(f"  base {wa['base_weight_lb']} lb vs {wa['class_budget']} -> {wa['verdict']}")
            if wa["cut_list"]:
                print(f"  cut list: {', '.join(wa['cut_list'])}")
            print(f"  total day-1 pack {wa['total_pack_lb']} lb -> {wa['body_check']}")
        return

    if args.sleep:
        low, comfort, r = map(float, args.sleep)
        import json as j
        print(j.dumps(sleep_verdict(low, comfort, r, args.sleep_liner), indent=2))
        return

    if args.budget:
        base, cls = float(args.budget[0]), args.budget[1]
        lo, hi = BUDGETS.get(cls, BUDGETS["lightweight"])
        verdict = "WITHIN BUDGET" if base <= hi else f"OVER by {base - hi:.1f} lb"
        print(f"base {base} lb vs {cls} ({lo}-{hi}): {verdict}")
        return

    p.print_help()


if __name__ == "__main__":
    main()
