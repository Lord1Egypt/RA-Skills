#!/usr/bin/env python3
"""Furniture Fit Checker — will it fit through the path and in the room?

Subcommands:
  path    — doorway pass check (diagonal tilt geometry)
  corner  — two-corridor L-corner turn check (numeric sweep)
  stairs  — staircase pass check (straight + 180 landing)
  room    — room layout fit with walkway standards + ASCII floorplan

Units: values may carry 'in', 'ft', 'cm', 'm' suffix; plain numbers = cm
if the value looks metric-large else inches... NO: plain = inches by
default; use suffixes for metric. (Explicit > implicit.)
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys

CM_PER_IN = 2.54
WALKWAY_MIN_CM = 75.0          # interior design standard path
DINING_CLEAR_CM = 91.0         # chair pull-out + walk


# ---------------------------------------------------------------------------
# Units

def to_cm(value: str) -> float:
    m = re.fullmatch(r"([0-9]*\.?[0-9]+)\s*(in|ft|cm|m|mm)?", value.strip().lower())
    if not m:
        raise ValueError(f"bad measurement {value!r} (e.g. 86, 32in, 14ft, 203cm, 1.2m)")
    n = float(m.group(1))
    unit = m.group(2) or "in"
    return {"in": n * CM_PER_IN, "ft": n * 30.48, "cm": n, "m": n * 100.0,
            "mm": n / 10.0}[unit]


def parse_list(s: str) -> list[float]:
    """Parse an 'AxB...' dimension list. A trailing unit on the LAST part
    applies to ALL parts (14x11ft), and a unit on every part also works
    (14ft x 11ft). Plain numbers = inches."""
    raw = [p for p in re.split(r"[x×*]", s) if p]
    if len(raw) not in (2, 3):
        raise ValueError(f"need WxD or WxDxH e.g. 86x37x35in / 14x11ft — got {s!r}")
    m = re.search(r"(in|ft|cm|mm|m)$", raw[-1].strip().lower())
    unit = m.group(1) if m else "in"
    values = []
    for part in raw:
        part = part.strip()
        m2 = re.fullmatch(r"([0-9]*\.?[0-9]+)\s*(in|ft|cm|mm|m)?", part.lower())
        if not m2:
            raise ValueError(f"bad dimension {part!r} in {s!r}")
        values.append(float(m2.group(1)) * {"in": 2.54, "ft": 30.48, "cm": 1.0,
                                            "mm": 0.1, "m": 100.0}[m2.group(2) or unit])
    return values


def parse_dims(s: str) -> tuple[float, float, float]:
    """Parse WxDxH (see parse_list for unit rules)."""
    values = parse_list(s)
    if len(values) != 3:
        raise ValueError(f"item needs WxDxH e.g. 86x37x35in or 218x94x89cm — got {s!r}")
    return tuple(values)  # type: ignore


def fmt(cm: float) -> str:
    return f"{cm/CM_PER_IN:.1f}in / {cm:.0f}cm"


# ---------------------------------------------------------------------------
# Path checks

def check_door(item: tuple[float, float, float], door_w: float, door_h: float) -> dict:
    """Rigid box through a rectangular opening in a (thin) wall.
    Choose each dimension in turn as the travel direction; the remaining
    two form the cross-section that must fit the opening — axis-aligned
    (a ≤ W and b ≤ H), or tilted in-plane (helps when the opening is much
    taller than wide). Tipping the item over is legitimate: that is just
    choosing a different travel direction."""
    results = []
    W, H = min(door_w, door_h), max(door_w, door_h)
    diag_open = math.hypot(W, H)
    for t_idx in range(3):
        t = item[t_idx]
        a, b = sorted([item[i] for i in range(3) if i != t_idx])
        axis = a <= W and b <= H
        tilt = (not axis) and a <= W and math.hypot(a, b) <= diag_open
        results.append({
            "travel_dim": fmt(t),
            "cross_section": f"{fmt(a)} × {fmt(b)}",
            "passes_axis": axis,
            "passes_tilted": tilt,
            "passes": axis or tilt,
        })
    best = next((r for r in results if r["passes"]), None)
    return {
        "fits": best is not None,
        "detail": results,
        "best": best,
        "verdict": "FITS" if best else "DOES NOT FIT",
    }


def check_corner(item: tuple[float, float, float], hall_a: float,
                 hall_b: float, ceiling_h: float | None = None) -> dict:
    """Item turning an L corner between corridors of widths A and B.

    Horizontal turn: with L = item length and T = second dimension in plan
    view, at angle θ the item needs L·sinθ+T·cosθ across corridor A and
    L·cosθ+T·sinθ across corridor B. Passes iff some θ satisfies both.

    Vertical-tilt mode (the movers' trick): if ceiling_h ≥ longest dim, the
    item can be stood on end, shrinking the plan footprint to the two
    smallest dims — usually makes the turn trivial. Checked automatically
    when ceiling_h is given.
    """
    L = max(item)
    T = sorted(item)[1]  # second-longest: the thickness in the turn plane
    tilt_mode = False
    if ceiling_h is not None and L <= ceiling_h:
        # stood on end: plan footprint = two smallest dims
        s = sorted(item)
        L, T = s[1], s[0]
        tilt_mode = True
    # For corridors of widths A and B meeting at right angle, item LxT:
    # blocking condition at angle θ (item touching inner corner):
    #   required: L·cosθ + T·sinθ ≤ B  and  L·sinθ + T·cosθ ≤ A
    # passes if ∃θ ∈ (0, π/2) satisfying both.
    ok_angles = []
    needed = []
    for i in range(0, 181):
        th = math.radians(i / 2)
        need_a = L * math.sin(th) + T * math.cos(th)
        need_b = L * math.cos(th) + T * math.sin(th)
        needed.append((need_a, need_b))
        if need_a <= hall_a and need_b <= hall_b:
            ok_angles.append(math.degrees(th))
    min_a = min(n[0] for n in needed)
    min_b = min(n[1] for n in needed)
    # best case for a square corner (A=B): minimize max(need_a, need_b)
    square_min = min(max(n[0], n[1]) for n in needed)
    return {
        "fits": bool(ok_angles),
        "tilt_mode": tilt_mode,
        "plan_footprint": f"{fmt(L)} x {fmt(T)}",
        "angle_range_deg": (min(ok_angles), max(ok_angles)) if ok_angles else None,
        "min_hall_a_needed_cm": min_a,
        "min_hall_b_needed_cm": min_b,
        "square_corner_min_cm": square_min,
        "verdict": ("FITS AROUND CORNER" + (" (stood on end)" if tilt_mode else ""))
                   if ok_angles else "DOES NOT MAKE THE TURN",
    }


def check_stairs(item, width_cm: float, headroom: float | None = None,
                 landing_depth_cm: float | None = None) -> dict:
    """Straight stairs: cross-section check (like a door turned sideways):
    two dims form the cross-section vs (width × headroom), third travels.
    180° landing: item must pivot — landing depth ≥ 0.75 × longest face
    diagonal (empirical)."""
    results = []
    W = width_cm
    H = headroom or 10_000  # unlimited if unknown
    for t_idx in range(3):
        a, b = sorted([item[i] for i in range(3) if i != t_idx])
        if a <= W and b <= H:
            results.append({"travel": fmt(item[t_idx]),
                            "cross": f"{fmt(a)} × {fmt(b)}", "ok": True})
    ok = bool(results)
    notes = []
    if not ok:
        needed_w = min(sorted(item)[0], sorted(item)[1])
        notes.append(f"no orientation fits: need width ≥ {fmt(needed_w)} "
                     f"(+ headroom for second dim)")
    if headroom is not None:
        tall = max(item)
        if tall > headroom and not any(
                r for r in results):
            notes.append(f"item height {fmt(tall)} vs headroom {fmt(headroom)}")
    if landing_depth_cm is not None:
        need = 0.75 * max(math.hypot(item[0], item[1]),
                          math.hypot(item[1], item[2]))
        if landing_depth_cm < need:
            ok = False
            notes.append(f"landing {fmt(landing_depth_cm)} < needed ~{fmt(need)} for pivot")
        else:
            notes.append(f"landing pivot OK ({fmt(landing_depth_cm)} ≥ {fmt(need)})")
    return {
        "fits": ok,
        "orientations": results,
        "notes": notes,
        "verdict": "FITS UP STAIRS" if ok else "DOES NOT FIT UP STAIRS",
    }


# ---------------------------------------------------------------------------
# Room check

def check_room(item_w: float, item_d: float, room_w: float, room_d: float,
               wall: str = "long", centered: bool = True,
               other: list[tuple[float, float]] | None = None) -> dict:
    """Fit against a wall; walkway = remaining depth on the facing side."""
    other = other or []
    # orient item: long side along the chosen wall
    if wall == "long":
        along, out = max(item_w, item_d), min(item_w, item_d)
        wall_len = room_w
    else:
        along, out = min(item_w, item_d), max(item_w, item_d)
        wall_len = room_d
    fits_wall = along <= wall_len
    walkway = room_d - out  # if placed against the 'long' wall (depth-wise)
    if wall == "short":
        walkway = room_w - out
    issues = []
    if not fits_wall:
        issues.append(f"item length {fmt(along)} > wall {fmt(wall_len)}")
    if walkway < WALKWAY_MIN_CM:
        issues.append(f"walkway {fmt(walkway)} < standard {fmt(WALKWAY_MIN_CM)}")
    for i, (ow, od) in enumerate(other, 1):
        # opposite-wall placement: remaining space between the two
        gap = room_d - out - od if wall == "long" else room_w - out - od
        if gap < WALKWAY_MIN_CM:
            issues.append(f"gap to furniture #{i}: {fmt(gap)} < {fmt(WALKWAY_MIN_CM)}")
    return {
        "fits": not issues,
        "item_along_wall_cm": along,
        "item_projection_cm": out,
        "walkway_cm": walkway,
        "walkway_ok": walkway >= WALKWAY_MIN_CM,
        "issues": issues,
        "verdict": "FITS WITH CLEARANCES" if not issues else "TIGHT / BLOCKED",
    }


def floorplan(room_w, room_d, item_w, item_d, wall="long",
              other=None) -> str:
    """ASCII floorplan; ~1 char = 10cm. '#' = the item, '=' = other furniture."""
    other = other or []
    W = max(int(round(room_w / 10)), 20)
    H = max(int(round(room_d / 10)), 10)
    grid = [[" "] * W for _ in range(H)]

    def put(cx_frac, y_top, w_cm, d_cm, ch):
        w = max(1, min(W, int(round(w_cm / 10))))
        d = max(1, min(H, int(round(d_cm / 10))))
        x0 = max(0, min(W - w, int(cx_frac * (W - w))))
        y0 = max(0, min(H - d, int(y_top)))
        for y in range(y0, y0 + d):
            for x in range(x0, x0 + w):
                grid[y][x] = ch

    # item against top wall, centered
    if wall == "long":
        iw, idp = max(item_w, item_d), min(item_w, item_d)
    else:
        iw, idp = min(item_w, item_d), max(item_w, item_d)
    put(0.5, 0, iw, idp, "#")
    # other furniture against bottom wall, centered
    for ow, od in other:
        put(0.5, H - max(1, int(round(od / 10))), ow, od, "=")

    border = "+" + "-" * W + "+"
    lines = [border]
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append(border)
    scale = f"scale ~1 char = 10cm | room {fmt(room_w)} x {fmt(room_d)} | # item | = other"
    return "\n".join(lines) + "\n" + scale


# ---------------------------------------------------------------------------
# CLI

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Furniture path & room fit checker")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("path", help="doorway pass check")
    sp.add_argument("--item", required=True, help="WxDxH e.g. 86x37x35in")
    sp.add_argument("--door", required=True, help="WxH e.g. 32x80in")
    sp.add_argument("--report", action="store_true")

    cp = sub.add_parser("corner", help="L-corner between corridors")
    cp.add_argument("--item", required=True)
    cp.add_argument("--hall-a", required=True)
    cp.add_argument("--hall-b", required=True)
    cp.add_argument("--ceiling", help="ceiling height (enables stand-on-end tilt)")

    tp = sub.add_parser("stairs", help="staircase check")
    tp.add_argument("--item", required=True)
    tp.add_argument("--width", required=True, help="clear stair width")
    tp.add_argument("--headroom", help="clearance above steps")
    tp.add_argument("--landing", help="landing depth (implies 180 turn)")

    rp = sub.add_parser("room", help="room fit + walkways")
    rp.add_argument("--item", required=True, help="WxD (2 dims) or WxDxH")
    rp.add_argument("--room", required=True, help="WxD e.g. 14x11ft")
    rp.add_argument("--wall", choices=["long", "short"], default="long")
    rp.add_argument("--other", action="append",
                    help="other furniture WxD, opposite wall, repeatable")
    rp.add_argument("--floorplan", action="store_true")
    rp.add_argument("--json", action="store_true")

    args = p.parse_args(argv)

    try:
        if args.cmd == "path":
            item = parse_dims(args.item)
            dw, dh = parse_list(args.door)[:2]
            r = check_door(item, dw, dh)
            print(f"ITEM {args.item} → DOOR {args.door}")
            for d in r["detail"]:
                mark = "✓" if d["passes"] else "✗"
                how = "flat" if d["passes_axis"] else ("tilted in-plane" if d["passes_tilted"] else "no")
                print(f"  {mark} travel {d['travel_dim']:>12} | cross-section {d['cross_section']} | {how}")
            print(f"\nVERDICT: {r['verdict']}")
            if not r["fits"]:
                print("  tips: remove legs/feet, pop hinge pins, angle-entry tilt,")
                print("        measure at the NARROWEST point of the actual route")
            if args.report:
                print(json.dumps(r, indent=2, default=str))
            return 0 if r["fits"] else 1

        if args.cmd == "corner":
            item = parse_dims(args.item)
            r = check_corner(item, to_cm(args.hall_a), to_cm(args.hall_b),
                             to_cm(args.ceiling) if args.ceiling else None)
            print(f"ITEM {args.item} → CORRIDOR {args.hall_a} → {args.hall_b}")
            if r["tilt_mode"]:
                print("  strategy: stood on end (movers' tilt) — plan footprint "
                      f"{r['plan_footprint']}")
            print(f"  min hall-A needed: {fmt(r['min_hall_a_needed_cm'])}")
            print(f"  min hall-B needed: {fmt(r['min_hall_b_needed_cm'])}")
            print(f"  square-corner min width needed: {fmt(r['square_corner_min_cm'])}")
            if r["angle_range_deg"]:
                lo, hi = r["angle_range_deg"]
                print(f"  workable angles: {lo:.0f}°–{hi:.0f}° (two people, slow pivot)")
            print(f"\nVERDICT: {r['verdict']}")
            return 0 if r["fits"] else 1

        if args.cmd == "stairs":
            item = parse_dims(args.item)
            r = check_stairs(item, to_cm(args.width),
                             to_cm(args.headroom) if args.headroom else None,
                             to_cm(args.landing) if args.landing else None)
            print(f"ITEM {args.item} → STAIRS width {args.width}")
            for o in r["orientations"]:
                print(f"  ✓ travel {o['travel']} | cross-section {o['cross']}")
            for n in r["notes"]:
                print(f"  · {n}")
            print(f"\nVERDICT: {r['verdict']}")
            return 0 if r["fits"] else 1

        if args.cmd == "room":
            dims = parse_list(args.item)
            iw, idp = dims[0], dims[1]
            rw, rd = parse_list(args.room)[:2]
            other = []
            if args.other:
                for o in args.other:
                    ow, od = parse_list(o)[:2]
                    other.append((ow, od))
            r = check_room(iw, idp, rw, rd, wall=args.wall, other=other)
            if args.json:
                print(json.dumps(r, indent=2, default=str))
                return 0
            print(f"ITEM {args.item} in ROOM {args.room} (against {args.wall} wall)")
            print(f"  along wall : {fmt(r['item_along_wall_cm'])}")
            print(f"  projection : {fmt(r['item_projection_cm'])}")
            print(f"  walkway    : {fmt(r['walkway_cm'])} (min {fmt(WALKWAY_MIN_CM)})")
            for i in r["issues"]:
                print(f"  ⚠ {i}")
            print(f"\nVERDICT: {r['verdict']}")
            if args.floorplan:
                print()
                print(floorplan(rw, rd, iw, idp, wall=args.wall, other=other))
            return 0 if r["fits"] else 1

    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
