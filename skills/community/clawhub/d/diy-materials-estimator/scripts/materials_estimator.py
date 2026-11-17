#!/usr/bin/env python3
"""DIY Materials Estimator — exact quantities from dimensions, buy-unit rounding.

Seven project calculators (paint, mulch, concrete, drywall, flooring, tile,
fence) plus a consolidated shopping list. All math is coverage physics from
manufacturer/norm mid-bands; output is rounded UP to real purchase units.

stdlib only. No network. State (saved projects) lives in materials_jobs.json
next to this script.
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "materials_jobs.json")

# ----------------------------- constants ----------------------------------
PAINT_COVERAGE = {          # ft2/gal, one coat
    "smooth": 375, "textured": 275, "exterior": 300, "primer": 350,
}
DOOR_FT2, WINDOW_FT2 = 21.0, 12.0
CONCRETE_BAG_YIELD = {80: 0.60, 60: 0.45, 40: 0.30}   # ft3 per bag
MULCH_BAG_FT3 = {"2": 2.0, "3": 3.0}
FLOOR_WASTE = {"straight": 0.05, "diagonal": 0.10, "herringbone": 0.13}
DRYWALL_SHEETS = {"4x8": 32.0, "4x10": 40.0, "4x12": 48.0}
GRAVITY_LB_PER_FT3_CONCRETE = 150.0


def ceil_to(x, unit):
    return int(math.ceil(round(x / unit, 6))) if unit > 0 else x


def parse_dims(s):
    """'12x14' / '12x14x4' -> tuple of floats."""
    parts = [float(p) for p in s.lower().split("x")]
    if any(p <= 0 for p in parts):
        raise ValueError(f"bad dimensions: {s}")
    return tuple(parts)


def save_job(name, lines, items):
    jobs = {}
    if os.path.exists(STATE):
        try:
            jobs = json.loads(open(STATE).read())
        except Exception:
            jobs = {}
    jobs[name] = {"summary": lines, "items": items}
    with open(STATE, "w") as f:
        json.dump(jobs, f, indent=2)


# ----------------------------- calculators --------------------------------
def calc_paint(a):
    dims = parse_dims(a.room)
    if len(dims) != 2:
        sys.exit("--room must be LxW")
    L, W = dims
    h = a.height
    perimeter = 2 * (L + W)
    gross = perimeter * h
    openings = a.doors * DOOR_FT2 + a.windows * WINDOW_FT2
    walls = max(0.0, gross - openings)
    ceiling = L * W if a.ceiling else 0.0
    area = walls + ceiling
    cov = PAINT_COVERAGE[a.surface]
    coats = a.coats
    gallons = (area / cov) * coats / 0.95
    buy_gal = ceil_to(gallons, 1)
    cheaper_5 = buy_gal >= 4
    items = [{"item": f"paint ({a.surface})",
              "qty": f"{buy_gal} gal" + ("  [or 1 x 5-gal bucket — usually cheaper]" if cheaper_5 else ""),
              "calc": f"{area:.0f} ft2 / {cov} ft2/gal x {coats} coats / 0.95 = {gallons:.2f} gal"}]
    lines = [
        f"Paint: room {L}x{W}, {h} ft walls, {a.doors} door(s), {a.windows} window(s)",
        f"  wall area {walls:.0f} ft2" + (f" + ceiling {ceiling:.0f} ft2" if ceiling else ""),
        f"  gallons needed {gallons:.2f} -> BUY {buy_gal} gal",
    ]
    if a.primer:
        pgal = ceil_to(area / PAINT_COVERAGE['primer'] / 0.95, 1)
        items.append({"item": "primer", "qty": f"{pgal} gal",
                      "calc": f"{area:.0f} / 350 x 1 coat"})
        lines.append(f"  primer: BUY {pgal} gal")
    if a.trim:
        trim_gal = ceil_to(a.trim / 350 / 0.95, 1)
        items.append({"item": "trim paint", "qty": f"{trim_gal} gal",
                      "calc": f"{a.trim} ft2 trim"})
        lines.append(f"  trim/doors {a.trim} ft2: BUY {trim_gal} gal (semi-gloss)")
    return lines, items


def calc_mulch(a):
    dims = parse_dims(a.area)
    area = math.prod(dims)
    depth_ft = (a.depth_in / 12.0) if a.depth_in else (a.depth_cm / 30.48)
    ft3 = area * depth_ft
    yd3 = ft3 / 27.0
    bag2 = ceil_to(ft3 / 2.0, 1)
    bag3 = ceil_to(ft3 / 3.0, 1)
    lines = [
        f"Mulch: area {area:.0f} ft2 at {depth_ft*12:.1f} in",
        f"  volume {ft3:.1f} ft3 = {yd3:.2f} yd3",
        f"  bags: {bag2} x 2-ft3  |  {bag3} x 3-ft3",
        f"  bulk: {'ORDER BULK DELIVERY (>=4 yd3, cheaper per yd3)' if yd3 >= 4 else 'bag territory (<4 yd3)'}",
        "  reminder: keep mulch 8 cm off tree trunks (no volcanos)",
    ]
    items = [{"item": "mulch", "qty": f"{bag2} x 2-ft3 bags (or {yd3:.2f} yd3 bulk)",
              "calc": f"{area:.0f} ft2 x {depth_ft:.3f} ft = {ft3:.1f} ft3"}]
    return lines, items


def calc_concrete(a):
    if a.slab:
        dims = parse_dims(a.slab)
        if len(dims) != 3:
            sys.exit("--slab must be LxWxD(inches)")
        L, W, D_in = dims
        vol = L * W * (D_in / 12.0)
        desc = f"slab {L}x{W} ft at {D_in} in"
    elif a.holes:
        # holes: count x diameter_in x depth_in
        try:
            n, dia, depth = (float(p) for p in a.holes.split(","))
        except ValueError:
            sys.exit("--holes must be count,diameter_in,depth_in (e.g. 26,10,30)")
        r = dia / 24.0
        vol = n * math.pi * r * r * (depth / 12.0)
        vol *= 1.10  # flare/waste
        desc = f"{n:g} holes x {dia:g} in dia x {depth:g} in deep"
    else:
        sys.exit("need --slab LxWxD(in) or --holes count,dia_in,depth_in")
    bag_yield = CONCRETE_BAG_YIELD[a.bag_lb]
    bags = ceil_to(vol / bag_yield, 1)
    weight_tons = vol * GRAVITY_LB_PER_FT3_CONCRETE / 2000.0
    crossover = "READY-MIX/TRAILER IS BETTER (past ~20 bags: cheaper per ft3, uniform mix)" if bags > 20 else "bag-mix territory"
    lines = [
        f"Concrete: {desc}",
        f"  volume {vol:.2f} ft3 (~{weight_tons:.2f} tons at 150 lb/ft3)",
        f"  {a.bag_lb}-lb bags: {bags}  [{crossover}]",
        f"  water: ~{bags * (3 if a.bag_lb == 80 else 2)} qt total (start dry, add slowly)",
        "  cure: keep damp 3-7 days for full strength (sprinkle + plastic)",
    ]
    items = [{"item": f"concrete {a.bag_lb}-lb bags", "qty": str(bags),
              "calc": f"{vol:.2f} ft3 / {bag_yield} ft3 per bag"}]
    return lines, items


def calc_drywall(a):
    dims = parse_dims(a.room)
    if len(dims) != 2:
        sys.exit("--room must be LxW")
    L, W = dims
    wall_area = 2 * (L + W) * a.height - (a.doors * DOOR_FT2 + a.windows * WINDOW_FT2)
    ceiling = L * W if a.ceiling else 0.0
    area = wall_area + ceiling
    sheet_ft2 = DRYWALL_SHEETS[a.sheet]
    waste = 0.10 if not a.diagonal else 0.15
    sheets = ceil_to(area * (1 + waste) / sheet_ft2, 1)
    screws_lb = ceil_to(area / 300.0, 1)
    tape_ft = area * 1.1
    mud_gal = ceil_to(area / 120.0 * 1.25, 1)
    lines = [
        f"Drywall: {L}x{W} x {a.height} ft, walls{'+ceiling' if ceiling else ''} = {area:.0f} ft2",
        f"  sheets {a.sheet}: {sheets} (incl. {int(waste*100)}% waste)",
        f"  screws 1.25in: ~{screws_lb} lb (~300/lb)",
        f"  tape: ~{tape_ft:.0f} ft  |  joint compound: ~{mud_gal} gal (fill+skim, +25%)",
    ]
    items = [
        {"item": f"drywall sheets {a.sheet}", "qty": str(sheets), "calc": f"{area:.0f} ft2 x{1+waste} / {sheet_ft2}"},
        {"item": "screws 1-1/4in (lb)", "qty": str(screws_lb), "calc": "~1 screw per ft2"},
        {"item": "joint compound (gal)", "qty": str(mud_gal), "calc": "1 gal/120 ft2 +25%"},
        {"item": "paper tape (ft)", "qty": f"{tape_ft:.0f}", "calc": "1.1 ft per ft2"},
    ]
    return lines, items


def calc_flooring(a):
    area = a.area
    waste = FLOOR_WASTE[a.pattern]
    need = area * (1 + waste)
    boxes = ceil_to(need / a.box_sqft, 1) if a.box_sqft else None
    lines = [
        f"Flooring: {area:.0f} ft2, pattern {a.pattern} (waste {int(waste*100)}%)",
        f"  buy {need:.0f} ft2" + (f"  -> {boxes} boxes @ {a.box_sqft} ft2/box" if boxes else ""),
        f"  underlayment: {ceil_to(area*1.05, 1):.0f} ft2 | transitions: count doorways",
        "  acclimate LVP/engineered 48h in-room before install",
    ]
    items = [{"item": f"flooring ({a.pattern})", "qty": f"{need:.0f} ft2" + (f" / {boxes} boxes" if boxes else ""),
              "calc": f"{area} x (1+{waste})"}]
    return lines, items


def calc_tile(a):
    dims = parse_dims(a.tile)
    if len(dims) != 2:
        sys.exit("--tile must be WxL in inches")
    tw, tl = dims
    tile_ft2 = (tw / 12.0) * (tl / 12.0)
    area = a.area
    waste = 0.15 if a.pattern in ("herringbone", "diagonal") else 0.10
    n_tiles = ceil_to(area / tile_ft2 * (1 + waste), 1)
    boxes = ceil_to(n_tiles / a.per_box, 1) if a.per_box else None
    # grout: industry chart (sanded), lbs per 100 ft2 by tile+joint
    chart = {(12, 12): (2, 9), (12, 24): (3, 11), (6, 6): (2, 14), (4, 4): (1, 16), (3, 6): (2, 18), (24, 24): (3, 10)}
    key = (int(tw), int(tl)) if (int(tw), int(tl)) in chart else None
    if key:
        j, lbs = chart[key]
        grout_lbs = ceil_to(area / 100.0 * lbs, 1)
        grout_note = f"~{grout_lbs} lb sanded ({j}/16in joint)"
    else:
        grout_lbs = ceil_to(area * a.joint * 0.09, 1)
        grout_note = f"~{grout_lbs} lb (joint {a.joint}/16 in, estimate)"
    thinset = ceil_to(area / 100.0, 1)
    lines = [
        f"Tile: {area:.0f} ft2, {tw}x{tl} in ({tile_ft2:.3f} ft2/tile), pattern {a.pattern}",
        f"  tiles {n_tiles}" + (f" -> {boxes} boxes @ {a.per_box}/box" if boxes else ""),
        f"  grout: {grout_note}",
        f"  thinset: ~{thinset} x 50-lb bags (3/16 v-notch; 1/4 for large format)",
        "  seal cement grout after 72h; use unsanded for <1/8 joints",
    ]
    items = [
        {"item": f"tile {tw}x{tl}in", "qty": f"{n_tiles} tiles" + (f" ({boxes} boxes)" if boxes else ""),
         "calc": f"{area}/{tile_ft2:.3f} x {1+waste}"},
        {"item": "grout (lb)", "qty": str(grout_lbs), "calc": grout_note},
        {"item": "thinset 50-lb bags", "qty": str(thinset), "calc": "~1 per 100 ft2"},
    ]
    return lines, items


def calc_fence(a):
    ft = a.length
    spacing = a.post_spacing
    posts = ceil_to(ft / spacing, 1) + 1
    bays = posts - 1
    rail_rows = 3 if a.style == "privacy" and a.height >= 6 else 2
    rails_16ft = ceil_to(bays * rail_rows * 8.0 / 16.0, 1)  # rails come in 16ft 2x4
    if a.style == "privacy":
        picket_w, gap = 5.5, 0.0
    elif a.style == "shadowbox":
        picket_w, gap = 5.5, 1.5
    else:  # paddock
        picket_w, gap = 5.5, 3.0
    pickets = ceil_to(ft * 12.0 / (picket_w + gap), 1)
    pickets_waste = ceil_to(pickets * 1.05, 1)
    bags = posts * (1 if a.bag_lb == 80 else 2)
    lines = [
        f"Fence: {ft} ft, {a.style}, {a.height} ft height, posts every {spacing} ft",
        f"  posts (4x4 treated, {math.ceil(a.height + 2)} ft long — bury {min(2.0, a.height/3):.0f} ft): {posts}",
        f"  rails: {bays} bays x {rail_rows} rows -> {rails_16ft} x 16-ft 2x4",
        f"  pickets {picket_w}in {a.style} (gap {gap}in): {pickets} -> BUY {pickets_waste} (+5%)",
        f"  concrete: {bags} x {a.bag_lb}-lb bags ({'1x80lb' if a.bag_lb == 80 else '2x50lb'} per post)",
        f"  fasteners: ~{pickets_waste * 2 + rails_16ft * 4} exterior screws/nails (ring-shank for pickets)",
    ]
    items = [
        {"item": "4x4 posts 8-ft treated", "qty": str(posts), "calc": f"{ft}/{spacing}+1"},
        {"item": "2x4x16 rails", "qty": str(rails_16ft), "calc": f"{bays} bays x {rail_rows} rows"},
        {"item": f"pickets {picket_w}in x {a.height}ft", "qty": str(pickets_waste), "calc": f"{ft}ft/( {(picket_w+gap)/12:.2f}ft ) +5%"},
        {"item": f"concrete {a.bag_lb}-lb", "qty": str(bags), "calc": "per-post table"},
        {"item": "exterior fasteners", "qty": f"~{pickets_waste * 2 + rails_16ft * 4}", "calc": "2/picket + rail screws"},
    ]
    return lines, items


# ----------------------------- shopping list ------------------------------
def shopping_list(_=None):
    if not os.path.exists(STATE):
        print("No saved projects yet — run a calculator first (state: materials_jobs.json)")
        return [], []
    jobs = json.loads(open(STATE).read())
    print(f"\n===== CONSOLIDATED SHOPPING LIST ({len(jobs)} project(s)) =====\n")
    total_items = []
    for name, j in jobs.items():
        print(f"[{name}]")
        for it in j["items"]:
            print(f"  - {it['item']}: {it['qty']}   ({it['calc']})")
            total_items.append(f"{name}: {it['item']}: {it['qty']}")
        print()
    print(f"TOTAL: {len(total_items)} line items. Round UP was applied everywhere.")
    return [], total_items


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("paint")
    p.add_argument("--room", required=True, help="LxW ft")
    p.add_argument("--height", type=float, default=8.0)
    p.add_argument("--doors", type=int, default=1)
    p.add_argument("--windows", type=int, default=1)
    p.add_argument("--coats", type=int, default=2)
    p.add_argument("--surface", default="smooth", choices=list(PAINT_COVERAGE))
    p.add_argument("--primer", action="store_true")
    p.add_argument("--trim", type=float, default=0.0, help="trim/door area ft2")
    p.add_argument("--ceiling", action="store_true")
    p.set_defaults(fn=calc_paint, name="paint")

    m = sub.add_parser("mulch")
    m.add_argument("--area", required=True, help="LxW ft (or '600' for single number = ft2)")
    m.add_argument("--depth-in", type=float, default=3.0)
    m.add_argument("--depth-cm", type=float, default=0.0)
    m.set_defaults(fn=calc_mulch, name="mulch")

    c = sub.add_parser("concrete")
    c.add_argument("--slab", help="LxWxD_in")
    c.add_argument("--holes", help="count,diameter_in,depth_in")
    c.add_argument("--bag-lb", type=int, default=80, choices=[40, 60, 80])
    c.set_defaults(fn=calc_concrete, name="concrete")

    d = sub.add_parser("drywall")
    d.add_argument("--room", required=True)
    d.add_argument("--height", type=float, default=8.0)
    d.add_argument("--doors", type=int, default=1)
    d.add_argument("--windows", type=int, default=1)
    d.add_argument("--ceiling", action="store_true")
    d.add_argument("--sheet", default="4x8", choices=list(DRYWALL_SHEETS))
    d.add_argument("--diagonal", action="store_true")
    d.set_defaults(fn=calc_drywall, name="drywall")

    f = sub.add_parser("flooring")
    f.add_argument("--area", type=float, required=True, help="ft2")
    f.add_argument("--pattern", default="straight", choices=list(FLOOR_WASTE))
    f.add_argument("--box-sqft", type=float, default=0.0, help="ft2 per box (0 = don't round to boxes)")
    f.set_defaults(fn=calc_flooring, name="flooring")

    t = sub.add_parser("tile")
    t.add_argument("--area", type=float, required=True)
    t.add_argument("--tile", required=True, help="WxL inches, e.g. 12x24")
    t.add_argument("--per-box", type=int, default=0)
    t.add_argument("--joint", type=int, default=3, help="joint width in 1/16in units (3 = 3/16)")
    t.add_argument("--pattern", default="straight", choices=["straight", "diagonal", "herringbone"])
    t.set_defaults(fn=calc_tile, name="tile")

    g = sub.add_parser("fence")
    g.add_argument("--length", type=float, required=True)
    g.add_argument("--style", default="privacy", choices=["privacy", "shadowbox", "paddock"])
    g.add_argument("--height", type=float, default=6.0)
    g.add_argument("--post-spacing", type=float, default=8.0)
    g.add_argument("--bag-lb", type=int, default=80, choices=[50, 80])
    g.set_defaults(fn=calc_fence, name="fence")

    sub.add_parser("shopping-list").set_defaults(fn=shopping_list, name="list")

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 1

    lines, items = args.fn(args)
    if lines:
        print("\n".join(lines))
        if args.cmd != "shopping-list":
            save_job(args.name, lines, items)
            print(f"\n[saved to shopping list: '{args.name}']")
    return 0


if __name__ == "__main__":
    sys.exit(main())
