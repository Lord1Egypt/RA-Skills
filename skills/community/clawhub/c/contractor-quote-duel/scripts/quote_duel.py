#!/usr/bin/env python3
"""
quote_duel.py — compare contractor quotes for the same home project.

Normalizes bids into a work-scope matrix, exposes what each quote omits,
runs unit-price sanity checks against ballpark bands, models deposit-risk
and payment-schedule exposure, and drafts a scope-gap clarification
letter per bidder.

Stdlib only. Offline. Decision support, not a guarantee of prices.
"""
import argparse
import json

# Ballpark unit-price bands (USD, US national-ish 2024-26; regional spread
# is wide — treat as order-of-magnitude sanity checks, not quotes).
UNIT_BANDS = {
    # scope item key: (low, high, unit label)
    "interior_paint": (2.5, 6.0, "per sq ft wall"),
    "interior_paint_room": (300, 800, "per room, 2 coats"),
    "hardwood_floor": (9, 22, "per sq ft installed"),
    "laminate_floor": (5, 12, "per sq ft installed"),
    "tile_floor": (10, 28, "per sq ft installed"),
    "roof_asphalt_shingle": (4.5, 9.0, "per sq ft roof"),
    "roof_metal": (9, 20, "per sq ft roof"),
    "kitchen_full_reno": (26000, 80000, "mid-range full, 10x10"),
    "bathroom_full_reno": (9000, 30000, "mid-range full gut"),
    "bathroom_resurface": (3500, 9000, "tub+surround+fixtures"),
    "drywall_patch": (75, 250, "per hole <=12in"),
    "drywall_hang_finish": (2.0, 4.5, "per sq ft"),
    "window_replacement": (500, 1300, "per window installed"),
    "fence_wood_privacy": (18, 45, "per linear ft"),
    "deck_build": (35, 85, "per sq ft pressure-treated"),
    "concrete_driveway": (6, 12, "per sq ft 4in"),
    "hvac_replace_furnace": (3500, 7500, "unit installed"),
    "hvac_replace_ac": (3500, 8000, "unit installed"),
    "hvac_minisplit": (3000, 6000, "per zone"),
    "water_heater": (1400, 3200, "tank installed"),
    "panel_upgrade_200a": (2200, 5000, "service panel"),
    "ev_charger_install": (500, 1800, "hardwired L2"),
    "gutter_replace": (6, 14, "per linear ft aluminum"),
    "siding_vinyl": (7, 14, "per sq ft"),
    "foundation_crack_inject": (500, 1500, "per crack epoxy"),
    "asphalt_driveway_seal": (0.3, 0.7, "per sq ft"),
}

SCOPE_HINTS = {
    "paint": "interior_paint_room", "floor": "laminate_floor",
    "hardwood": "hardwood_floor", "tile": "tile_floor",
    "roof": "roof_asphalt_shingle", "metal roof": "roof_metal",
    "kitchen": "kitchen_full_reno", "bath": "bathroom_full_reno",
    "window": "window_replacement", "fence": "fence_wood_privacy",
    "deck": "deck_build", "driveway": "concrete_driveway",
    "furnace": "hvac_replace_furnace", "ac": "hvac_replace_ac",
    "mini": "hvac_minisplit", "water heater": "water_heater",
    "panel": "panel_upgrade_200a", "ev": "ev_charger_install",
    "gutter": "gutter_replace", "siding": "siding_vinyl",
    "foundation": "foundation_crack_inject", "sealcoat": "asphalt_driveway_seal",
    "drywall": "drywall_hang_finish",
}

# What a serious quote for each job family MUST contain. Missing = flag.
REQUIRED_DOCS = {
    "default": ["itemized labor/material split or unit prices",
                "start date + estimated duration",
                "payment schedule (never 100% up front)"],
    "roof": ["tear-off layers and disposal included",
             "underlayment + ice/water shield spec",
             "flashing/vent work itemized", "warranty terms (labor)"],
    "kitchen": ["cabinet/counter allowance or spec", "permit responsibility",
                "electric/plumbing relocation scope", "dumpster/disposal"],
    "bath": ["waterproofing method (esp. tile showers)",
             "vent fan ducting scope", "permit responsibility"],
    "hvac": ["load calc (Manual J) or sizing rationale",
             "duct modification scope", "old equipment haul-away"],
    "electrical": ["permit + inspection included", "circuit/panel spec"],
    "structural": ["engineered drawing/stamp if structural",
                   "permit responsibility"],
}


def norm_key(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch == " ")


def match_band(item):
    k = " " + norm_key(item) + " "
    for hint, key in SCOPE_HINTS.items():
        if len(hint) <= 3:  # short hints must match whole words ("ac", "ev")
            if f" {hint} " in k:
                return key
        elif hint in k:
            return key
    return None


def job_family(items):
    fam = "default"
    k = " ".join(norm_key(i) for i in items)
    for f in ("roof", "kitchen", "bath", "hvac", "structural", "electrical"):
        if f in k:
            fam = f
    return fam


def cmd_matrix(a):
    quotes = load_quotes(a)
    # Union of scope items
    items = []
    for q in quotes:
        for it in q["items"]:
            n = it["item"]
            if n not in items:
                items.append(n)
    fam = job_family(items)
    req = REQUIRED_DOCS.get(fam, REQUIRED_DOCS["default"])
    print(f"SCOPE MATRIX — {len(quotes)} quotes, {len(items)} distinct line items "
          f"(family: {fam})\n")
    header = f"{'line item':<38}" + "".join(f"{q['bidder'][:14]:>16}" for q in quotes)
    print(header)
    print("-" * len(header))
    for it in items:
        row = f"{it[:36]:<38}"
        for q in quotes:
            val = next((x for x in q["items"] if x["item"] == it), None)
            if val is None:
                row += f"{'— MISSING':>16}"
            else:
                row += f"{val['price']:>16,.0f}"
        print(row)
    tot = f"{'TOTAL':<38}"
    for q in quotes:
        tot += f"{q['total']:>16,.0f}"
    print(tot)
    print()
    for q in quotes:
        missing = [i for i in req if i not in [d.lower() for d in q.get("docs", [])]]
        if missing:
            print(f"{q['bidder']}: missing documentation — {', '.join(missing)}")
    if a.json:
        print(json.dumps({"items": items, "quotes": quotes}, indent=2, default=str))


def cmd_pricecheck(a):
    quotes = load_quotes(a)
    flags = 0
    for q in quotes:
        for it in q["items"]:
            key = match_band(it["item"])
            if not key or key not in UNIT_BANDS:
                continue
            lo, hi, unit = UNIT_BANDS[key]
            qty = it.get("qty", 1) or 1
            unit_price = it["price"] / qty
            if unit_price > hi * 1.6:
                verdict = f"HIGH {unit_price:,.0f} vs band {lo:,.0f}-{hi:,.0f} {unit}"
                flags += 1
            elif unit_price < lo * 0.5:
                verdict = f"LOW {unit_price:,.0f} vs band {lo:,.0f}-{hi:,.0f} {unit} — expect change orders or corner-cutting"
                flags += 1
            else:
                verdict = "ok"
            print(f"[{q['bidder']}] {it['item']}: {verdict}")
    if flags == 0:
        print("No unit-price outliers vs ballpark bands.")
    print("\nBands are order-of-magnitude US averages; regional spread is wide.")


def cmd_risk(a):
    quotes = load_quotes(a)
    print("DEPOSIT & PAYMENT RISK\n")
    for q in quotes:
        dep = q.get("deposit_pct", 0)
        sched = q.get("schedule", [])
        upfront = dep
        risk = []
        if dep > 30:
            risk.append(f"deposit {dep}% > 30% norm (many states cap 10-30%)")
        if not sched:
            risk.append("no payment schedule written")
        cum = dep
        milestones_before_completion = sum(s.get("pct", 0) for s in sched
                                           if not s.get("at_completion", False))
        if milestones_before_completion + dep > 60:
            risk.append(f"{dep + milestones_before_completion}% due before completion — walk risk")
        if not q.get("insured", False):
            risk.append("liability insurance not verified")
        if not q.get("licensed", True):
            risk.append("not licensed")
        verdict = "LOW" if len(risk) <= 1 and dep <= 30 else (
            "MEDIUM" if len(risk) <= 3 else "HIGH")
        print(f"{q['bidder']}: deposit {dep}%  ->  {verdict}")
        for r in risk:
            print(f"   - {r}")
    print()
    print("Norms: deposit <=30% (materials), final payment only after "
          "inspection/punch list, never pay cash without receipt.")


def cmd_letter(a):
    quotes = load_quotes(a)
    q = next((x for x in quotes if x["bidder"].lower() == a.bidder.lower()), quotes[0])
    others = [x for x in quotes if x is not q]
    items = []
    for x in others:
        for it in x["items"]:
            if it["item"] not in [i["item"] for i in q["items"]] and it["item"] not in items:
                items.append(it["item"])
    print(f"Subject: Question about your quote for {a.project or 'the project'}\n")
    print(f"Hi {q['bidder']},\n")
    if items:
        print("Thanks for the quote. Comparing bids, a few scope items appear "
              "in other proposals but not yours:")
        for i in items:
            print(f"  - {i}")
        print("\nCould you confirm whether these are included, excluded, or "
              "not applicable? If excluded, a unit price to add them would "
              "help me compare like-for-like.")
    else:
        print("Thanks for the quote. To compare bids like-for-like, could you "
              "confirm: what exactly is excluded from this scope, and which "
              "items would be handled as allowance/allowance-plus?")
    print("\nAlso please confirm:")
    print("  1. Payment schedule (I keep deposits under 30% and hold final "
          "payment until punch-list completion).")
    print("  2. Start date and realistic duration.")
    print("  3. Who pulls permits.")
    print("  4. Warranty on labor.\n")
    print("Thanks — a reply by DATE works best for my decision timeline.")
    if a.json:
        print(json.dumps({"bidder": q["bidder"], "scope_gaps": items}, indent=2))


def load_quotes(a):
    data = json.loads(a.quotes_json)
    return data if isinstance(data, list) else data.get("quotes", [])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quotes-json", required=True,
                    help='JSON: [{"bidder":"A","total":9500,"deposit_pct":10,'
                         '"items":[{"item":"roof","price":9500,"qty":2000}],'
                         '"docs":[...],"insured":true}]')
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("matrix", help="scope x bidder matrix + missing items")
    sub.add_parser("pricecheck", help="unit-price sanity vs ballpark bands")
    sub.add_parser("risk", help="deposit + payment-schedule risk")
    d = sub.add_parser("letter", help="scope-gap clarification letter")
    d.add_argument("--bidder", default="")
    d.add_argument("--project", default="")
    a = ap.parse_args()
    {"matrix": cmd_matrix, "pricecheck": cmd_pricecheck,
     "risk": cmd_risk, "letter": cmd_letter}[a.cmd](a)


if __name__ == "__main__":
    main()
