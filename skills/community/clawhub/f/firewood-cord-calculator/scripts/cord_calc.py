#!/usr/bin/env python3
"""Firewood cord calculator: honest cord volume, species/moisture-corrected
BTU, cost-per-MMBtu vs competing fuels, seasoning back-planning, and
annual consumption sizing. Pure stdlib.

Examples:
  python3 cord_calc.py --volume --length-ft 8 --height-ft 4 --depth-in 16
  python3 cord_calc.py --evaluate --species red-oak --cords 1.0 --price 300 --moisture 22 --efficiency 0.70
  python3 cord_calc.py --compare --price 300 --species red-oak --propane 2.60 --gas 1.40 --electricity 0.14 --heatpump-cop 3.0
  python3 cord_calc.py --season --species white-oak --split-in 5 --ready 2027-11-01
  python3 cord_calc.py --annual --sqft 2000 --hdd 5000 --species red-oak
"""
import argparse
from datetime import date, timedelta

CORD_FT3 = 128.0
# species: MMBtu per cord @20% MC (higher/lower bound baked into midpoint), seasoning months to <20%
SPECIES = {
    "osage-orange": (30.0, 12, "hedge; hottest common firewood, sparks"),
    "honey-locust": (27.0, 12, "dense, long coals"),
    "black-locust": (27.0, 12, "rot-resistant, excellent coals"),
    "red-oak":      (24.0, 12, "the standard hardwood heat"),
    "white-oak":    (26.0, 18, "dries slower than red; worth the wait"),
    "sugar-maple":  (24.0, 9,  "burns clean, even"),
    "red-maple":    (21.0, 9,  ""),
    "beech":        (25.0, 12, ""),
    "birch":        (21.0, 9,  "bark makes great kindling"),
    "ash":          (23.0, 9,  "seasons fast, splits easy; emerald-ash areas have supply"),
    "cherry":       (20.0, 9,  "pleasant aroma, moderate heat"),
    "walnut":       (20.0, 9,  ""),
    "elm":          (20.0, 12, "fibrous to split, holds water"),
    "sycamore":     (19.0, 12, "hard to split when green"),
    "aspen":        (14.0, 6,  "low heat; better than nothing"),
    "poplar":       (14.0, 6,  ""),
    "pine":         (16.0, 6,  "hot and fast; creosote risk damped-down; great kindling"),
    "spruce":       (15.0, 6,  ""),
    "fir":          (15.0, 6,  ""),
    "mixed":        (20.0, 9,  "unknown mix: assume moderate hardwood"),
}

PACKING = {"tight": 0.95, "hand": 0.90, "loose": 0.68}

# moisture correction: fraction of dry-wood heat available, from MC (wet basis)
def moisture_factor(mc_pct):
    if mc_pct <= 20:
        return 1.0
    # each % over 20 costs ~1.5% of energy up to 50% MC floor of 0.55
    return max(0.55, 1.0 - (mc_pct - 20) * 0.015)


def cmd_volume(a):
    depth_ft = a.depth_in / 12.0
    gross = a.length_ft * a.height_ft * depth_ft
    pack = PACKING[a.packing]
    net = gross * pack
    cords = net / CORD_FT3
    print("=" * 62)
    print("CORD VOLUME CHECK")
    print("=" * 62)
    print(f"  stack {a.length_ft:g} ft x {a.height_ft:g} ft x {a.depth_in:g} in"
          f"  = {gross:.1f} ft3 gross")
    print(f"  packing '{a.packing}' factor {pack:.2f} -> {net:.1f} ft3 net")
    print(f"  TRUE VOLUME: {cords:.2f} cord  ({cords * CORD_FT3:.0f} ft3)")
    if a.face_cords:
        fc = a.face_cords
        print(f"  as face cords (16in depth): this stack = {cords * 3:.2f} face-cord units")
    print(f"\n  reference: 1 cord = 128 ft3 stacked = 4x4x8 ft")
    print(f"  a 'face cord' (8x4x16in) = {8 * 4 * 16 / 12 / CORD_FT3:.2f} cord")
    if cords < 0.9:
        print("  >> SHORT of a full cord - price accordingly.")
    elif cords > 1.1:
        print("  >> More than a cord - generous measure.")
    else:
        print("  >> Honest cord measure.")


def cmd_evaluate(a):
    btu, months, note = SPECIES[a.species]
    mf = moisture_factor(a.moisture)
    eff = a.efficiency
    delivered = btu * mf * eff
    cost_per_mmbtu = a.price / delivered
    print("=" * 62)
    print(f"EVALUATE: {a.cords:g} cord {a.species} @ ${a.price:g}/cord")
    print("=" * 62)
    print(f"  energy content @20% MC:      {btu:.1f} MMBtu/cord")
    if note:
        print(f"  ({note})")
    print(f"  moisture correction ({a.moisture:g}%):  x{mf:.2f}")
    print(f"  stove efficiency:            x{eff:.2f}")
    print(f"  DELIVERED HEAT:              {delivered:.1f} MMBtu/cord")
    print(f"  cost per delivered MMBtu:    ${cost_per_mmbtu:.2f}")
    print(f"  total heat purchased:        {delivered * a.cords:.1f} MMBtu for ${a.price * a.cords:.0f}")
    if a.moisture > 25:
        print("\n  !! >25% MC: this is green wood - it will steam, creosote the")
        print("     chimney, and deliver well under nameplate heat. Meter it")
        print("     on a fresh split face before paying 'seasoned' prices.")
    return cost_per_mmbtu


def cmd_compare(a):
    wood_cost = cmd_evaluate(a)
    print()
    print("=" * 62)
    print("FUEL COMPARISON (per delivered MMBtu)")
    print("=" * 62)
    rows = [("wood (this offer)", wood_cost)]
    if a.propane:
        rows.append(("propane", a.propane / 0.0916 / 0.90))  # 91,600 BTU/gal, 90% furnace eff
    if a.gas:
        rows.append(("natural gas (furnace)", a.gas / 0.1 / 0.95))
    if a.electricity:
        rows.append(("resistance electric", a.electricity / 0.003412 / 1.0))
    if a.electricity and a.heatpump_cop:
        rows.append((f"heat pump (COP {a.heatpump_cop:g})",
                     a.electricity / 0.003412 / a.heatpump_cop))
    for name, cost in sorted(rows, key=lambda r: r[1]):
        bar = "#" * int(cost * 4)
        print(f"  {name:24s} ${cost:6.2f}/MMBtu  {bar}")
    cheapest = min(rows, key=lambda r: r[1])
    print(f"\n  >> Cheapest: {cheapest[0]} at ${cheapest[1]:.2f}/MMBtu")
    if cheapest[0].startswith("wood"):
        other = sorted(rows, key=lambda r: r[1])[1]
        print(f"     vs next-best {other[0]} ${other[1]:.2f} - wood saves "
              f"${(other[1] - cheapest[1]) * 60:.0f}/yr at ~60 MMBtu/yr typical house")
    else:
        fair = cheapest[1] * SPECIES[a.species][0] * moisture_factor(a.moisture) * a.efficiency
        print(f"     Fair price for this wood: <= ${fair:.0f}/cord")


def cmd_season(a):
    btu, months, note = SPECIES[a.species]
    # split thickness adjusts: <4in = -2 mo, >6in = +3 mo
    adj = months + (-2 if a.split_in <= 4 else 3 if a.split_in >= 6 else 0)
    ready = date.fromisoformat(a.ready)
    split_by = ready - timedelta(days=30.44 * adj)
    print("=" * 62)
    print(f"SEASONING PLAN: {a.species} -> ready {ready}")
    print("=" * 62)
    print(f"  baseline drying time:  {months} months")
    print(f"  split thickness {a.split_in}in adjustment: {adj - months:+d} months")
    print(f"  TOTAL: {adj} months")
    print(f"  split & stack by:      {split_by:%B %d, %Y}")
    print(f"""
  drying conditions that actually move the number:
  - single row, ends to prevailing wind, sun exposure
  - off the ground (pallets/rails), bark-side down on hardwoods
  - top cover only (tarp/tin roof), sides open - airflow is the dryer
  - no 'seasoning' against a closed shed wall or in deep shade
  - check with a meter: <20% MC on a fresh-split face = ready""")


def cmd_annual(a):
    btu, months, note = SPECIES[a.species]
    # rough house demand: BTU/ft2 per HDD ~ 8-15 for decent homes, use 10
    demand_mmbtu = a.sqft * a.hdd * 10 / 1_000_000
    if a.fraction is not None:
        demand_mmbtu *= a.fraction
    delivered = btu * 1.0 * 0.70  # assume seasoned, 70% stove
    cords_honest = demand_mmbtu / delivered
    print("=" * 62)
    print(f"ANNUAL FIREWOOD DEMAND: {a.sqft:g} ft2, {a.hdd:g} HDD65 climate")
    print("=" * 62)
    print(f"  estimated seasonal heat demand: {demand_mmbtu:.0f} MMBtu")
    print(f"  (rule-of-thumb 10 BTU/ft2/HDD - adjust with your fuel bills)")
    if a.fraction is not None:
        print(f"  wood covers {a.fraction * 100:.0f}% of that demand")
    print(f"  {a.species} delivered ~{delivered:.1f} MMBtu/cord (seasoned, 70% stove)")
    print(f"  THEORETICAL: {cords_honest:.1f} cords/season")
    print(f"  REALISTIC FIRST YEAR: {cords_honest * 1.4:.1f} cords (the 1.4x ambiance factor)")
    print(f"  STACKING SPACE: ~{cords_honest * 1.4 * 85:.0f} ft of 4-ft-tall single-row wall")


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("volume", help="measure a stack -> true cords")
    v.add_argument("--length-ft", type=float, required=True)
    v.add_argument("--height-ft", type=float, required=True)
    v.add_argument("--depth-in", type=float, default=16)
    v.add_argument("--packing", choices=PACKING, default="hand")
    v.add_argument("--face-cords", type=int, default=0)

    e = sub.add_parser("evaluate", help="energy + cost per MMBtu of an offer")
    e.add_argument("--species", choices=SPECIES, default="mixed")
    e.add_argument("--cords", type=float, default=1.0)
    e.add_argument("--price", type=float, required=True)
    e.add_argument("--moisture", type=float, default=20)
    e.add_argument("--efficiency", type=float, default=0.70)

    c = sub.add_parser("compare", help="wood vs propane/gas/electric/heat pump")
    c.add_argument("--species", choices=SPECIES, default="mixed")
    c.add_argument("--cords", type=float, default=1.0)
    c.add_argument("--price", type=float, required=True)
    c.add_argument("--moisture", type=float, default=20)
    c.add_argument("--efficiency", type=float, default=0.70)
    c.add_argument("--propane", type=float)
    c.add_argument("--gas", type=float)
    c.add_argument("--electricity", type=float)
    c.add_argument("--heatpump-cop", type=float)

    s = sub.add_parser("season", help="back-plan split-by date")
    s.add_argument("--species", choices=SPECIES, required=True)
    s.add_argument("--split-in", type=float, default=5)
    s.add_argument("--ready", default=date.today().isoformat())

    n = sub.add_parser("annual", help="cords per year for a house")
    n.add_argument("--sqft", type=float, required=True)
    n.add_argument("--hdd", type=float, required=True)
    n.add_argument("--species", choices=SPECIES, default="mixed")
    n.add_argument("--fraction", type=float,
                   help="share of heat from wood, 0-1 (default 1.0)")

    a = ap.parse_args()
    {"volume": cmd_volume, "evaluate": cmd_evaluate, "compare": cmd_compare,
     "season": cmd_season, "annual": cmd_annual}[a.cmd](a)


if __name__ == "__main__":
    main()
