#!/usr/bin/env python3
"""cargo_packer.py — truck/pickup/trailer load planning: fit math, load map,
tie-down counts. Stdlib only. Exit 0 ok, 2 usage/data error."""

import argparse
import math
import re
import sys

# ---------------------------------------------------------------------------
# Parsing


def parse_dims(token):
    """'L120xW80xH60' -> (120, 80, 60) in cm."""
    m = re.fullmatch(
        r"\s*[Ll]\s*(\d+(?:\.\d+)?)\s*[Xx]\s*[Ww]\s*(\d+(?:\.\d+)?)\s*[Xx]\s*[Hh]\s*(\d+(?:\.\d+)?)\s*",
        token,
    )
    if not m:
        raise ValueError(f"bad dims {token!r} — use L120xW80xH60")
    return tuple(float(x) for x in m.groups())


def parse_cargo(spec):
    """'L120xW80xH60:2,L60xW40xH40:5' -> [((L,W,H), n), ...]"""
    items = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError(f"bad cargo item {part!r} — need LxWxH:count")
        dims_s, _, cnt_s = part.partition(":")
        n = int(cnt_s)
        if n <= 0:
            raise ValueError(f"count must be >=1 in {part!r}")
        items.append((parse_dims(dims_s), n))
    if not items:
        raise ValueError("no cargo items parsed")
    return items


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Density heuristics


def density_class(dims):
    """Crude density class from longest side + volume: big light things
    shouldn't be under small heavy things. Returns A (heaviest/densest
    suggestion) .. C."""
    L, W, H = max(dims), sorted(dims)[1], min(dims)
    vol_l = (dims[0] * dims[1] * dims[2]) / 1000.0  # liters
    longest = max(dims)
    if longest >= 180:  # furniture-scale
        return "F"
    if vol_l <= 40:  # small boxes -> books/tools class
        return "A"
    if vol_l <= 120:
        return "B"
    if vol_l >= 300:  # sofa/mattress-scale light volume
        return "F"
    return "C"


# ---------------------------------------------------------------------------
# Commands


def cmd_fit(args):
    try:
        cargo = parse_cargo(args.cargo)
        space = parse_dims(args.space)
    except ValueError as e:
        die(str(e))

    SL, SW, SH = space
    space_m3 = SL * SW * SH / 1_000_000
    print("=" * 62)
    print(f"  FIT CHECK — space {SL:.0f} x {SW:.0f} x {SH:.0f} cm "
          f"({space_m3:.2f} m3)")
    print("=" * 62)

    total_m3 = 0.0
    rows = []
    for dims, n in cargo:
        vol = dims[0] * dims[1] * dims[2] / 1_000_000
        total_m3 += vol * n
        fits_alone = (dims[0] <= SL and dims[1] <= SW and dims[2] <= SH) or (
            dims[1] <= SL and dims[0] <= SW and dims[2] <= SH) or (
            dims[2] <= SL and dims[1] <= SW and dims[0] <= SH)
        longest = max(dims)
        rows.append((dims, n, vol, fits_alone, longest))

    practical = space_m3 * 0.80
    print(f"  Cargo cube total : {total_m3:.2f} m3 "
          f"({len(cargo)} item types, {sum(n for _, n in cargo)} pieces)")
    print(f"  Space cube       : {space_m3:.2f} m3")
    print(f"  Practical (80%)  : {practical:.2f} m3")
    print()

    oversize = [r for r in rows if not r[3]]
    if oversize:
        print("  DIMENSION FAIL (no rotation fits in the space):")
        for dims, n, _, _, longest in oversize:
            print(f"    {dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f} cm x{n} "
                  f"(longest side {longest:.0f} cm)")
        print()

    pct = total_m3 / space_m3 * 100
    pct_practical = total_m3 / practical * 100 if practical else 0
    print(f"  Cube usage: {pct:.0f}% of raw space, "
          f"{pct_practical:.0f}% of practical (80%) capacity")
    if oversize:
        verdict = "CANNOT FIT — oversized item(s); load on-end/angle or bigger truck"
    elif total_m3 > practical:
        verdict = ("TIGHT — over the 80% practical ceiling; expect a "
                   "hard pack or leave the tail 10% behind")
    else:
        verdict = "FITS — with margin for blankets, straps, and a walk gap"
    print(f"  VERDICT: {verdict}")

    # per-piece stacking advice
    print()
    print("  Density guidance:")
    for dims, n, vol, fits, _ in rows:
        cls = density_class(dims)
        where = {"A": "floor, forward (heavy class)",
                 "B": "mid-height, mid-load",
                 "C": "top / rear (light class)",
                 "F": "floor furniture — strap, drawers out; on-end if mattress/sofa"}[cls]
        print(f"    {dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f} x{n}: class {cls} -> {where}")
    return 0


def cmd_loadmap(args):
    try:
        cargo = parse_cargo(args.cargo)
        space = parse_dims(args.space)
    except ValueError as e:
        die(str(e))
    SL, SW, SH = space

    # Order: class A first (forward), then B, then F, then C
    def sort_key(entry):
        dims, n = entry
        return {"A": 0, "B": 1, "F": 2, "C": 3}[density_class(dims)]

    ordered = sorted(cargo, key=sort_key)

    # Place along L axis greedily, rows across W
    grid_W = 4  # top-down map cells across width
    print("=" * 62)
    print(f"  LOAD MAP — {SL:.0f}x{SW:.0f} cm floor, {SH:.0f} cm walls "
          f"(not to scale)")
    print("=" * 62)
    print("  TOP-DOWN (front/cab at TOP; heavy items forward):")
    print()

    cell = max(SL, SW) / 24.0
    cols = max(6, min(78, int(SW / cell))) if cell else 20
    rows_n = max(4, min(30, int(SL / cell))) if cell else 10
    lab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    canvas = [["." for _ in range(cols)] for _ in range(rows_n)]
    labels = []
    idx = 0
    cursor_x = 0  # along L (rows)
    row_w = 0     # used width in current row band
    for dims, n in ordered:
        # orient longest horizontal
        d = sorted(dims, reverse=True)
        w_cells = max(1, int(d[1] / cell))
        l_cells = max(1, int(d[0] / cell))
        ch = lab[idx % len(lab)]
        idx += 1
        labels.append((ch, dims, n, density_class(dims)))
        for _ in range(n):
            placed = False
            for attempt in range(rows_n):
                r = cursor_x + attempt
                if r >= rows_n:
                    break
                if row_w + w_cells <= cols:
                    c0 = row_w
                else:
                    continue
                for rr in range(r, min(r + l_cells, rows_n)):
                    for cc in range(c0, min(c0 + w_cells, cols)):
                        canvas[rr][cc] = ch
                row_w += w_cells
                cursor_x = r
                placed = True
                break
            if not placed:
                # stack marker: reuse letter at cursor
                r = min(cursor_x, rows_n - 1)
                c0 = 0
                canvas[r][c0] = ch
    for r in range(rows_n):
        print("     |" + "".join(canvas[r]) + "|")
    print("     +" + "-" * cols + "+")
    print(f"      front wall at top; tailgate at bottom; "
          f"1 cell ≈ {cell:.0f} cm")
    print()
    print("  LEGEND:")
    for ch, dims, n, cls in labels:
        print(f"    {ch}: {dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f} cm x{n} "
              f"[class {cls}]")
    print()
    print("  SIDE VIEW (height profile — keep center of gravity low):")
    profile = min(rows_n, 8)
    heights = [0] * cols
    # crude: stack heights per column from the map
    for r in range(rows_n):
        for c in range(cols):
            if canvas[r][c] != ".":
                # each item ~ its height in cells
                pass
    hcell = max(SH / 6.0, 1)
    for level in range(6, 0, -1):
        line = "".join("#" if (c / cols) * SH < level * hcell and any(
            canvas[r][c] != "." for r in range(rows_n)) else " " for c in range(cols))
        print(f"  {level*hcell:4.0f}cm |{line}|")
    print("        +" + "-" * cols + "+")
    print("        (rough height profile; A-class low, C-class high)")
    return 0


def cmd_checklist(args):
    w = args.weight_lb
    surface = args.surface
    print("=" * 62)
    print(f"  SECURING CHECKLIST — {w:.0f} lb on {surface}")
    print("=" * 62)
    # WSTDA-ish: aggregate WLL >= 2x weight
    strap_wll = {"light": 333, "standard": 500, "heavy": 1000, "chain": 5400}
    wll = strap_wll["standard"]
    need_wll = 2 * w
    n_straps = max(2, math.ceil(need_wll / wll))
    print(f"  Aggregate WLL needed (2x cargo): {need_wll:.0f} lb")
    std = strap_wll["standard"]
    n_std = max(2, math.ceil(need_wll / std))
    print(f"  Standard 2in ratchet straps (WLL {std} lb): {n_std} straps minimum")
    hv = strap_wll["heavy"]
    n_hv = max(2, math.ceil(need_wll / hv))
    print(f"  ... or heavy straps (WLL {hv} lb): {n_hv}")
    print()
    if surface == "pickup":
        print("  PICKUP BED doctrine:")
        print("   - Load heavy items forward of the rear axle (front-bias)")
        print("   - Use bed rail pockets / bolted eyes; never plastic hooks")
        howto = ("   - 2 straps over the top through bed anchors, crossed;\n"
                 "     1 forward ratchet to the front anchor per side")
    elif surface == "trailer":
        print("  TRAILER doctrine:")
        print("   - 60/40 weight bias toward the tongue (see your tongue "
              "weight spec, typically 10-15% of GTW)")
        print("   - Anchor to D-rings / stake pockets; strap at 45 deg max "
              "from horizontal where possible")
        howto = ("   - 2+ straps over the load to D-rings EACH side +\n"
                 "     1 direct forward + 1 direct rearward strap per big item")
    else:  # box truck
        print("  BOX TRUCK doctrine:")
        print("   - Load heavy against the cab bulkhead; use E-track/L-track "
              "walls + load bars")
        print("   - Fill voids — load bars or void fillers every 0.8-1.2 m")
        howto = ("   - E-track straps (WLL 1000 lb) at 45 deg, 4-point on "
                 "tall furniture;\n     load bar behind the last stack")
    print(howto)
    print()
    blankets = max(4, int(w / 150))
    print(f"  Moving blankets: {blankets} (1 per furniture face-pair + 2 spare)")
    print(f"  Shrink wrap / stretch plastic: {max(1, int(w/500))} rolls")
    print(f"  Corner protectors under every strap touching cargo: {n_std * 2}")
    print()
    print("  PRE-DEPARTURE:")
    print("   [ ] Straps tight, no slack, re-check after 10 km")
    print("   [ ] No cargo above the rail / box opening line")
    print("   [ ] Doors/ramp secured and locked")
    print("   [ ] Lights and plate visible, strap ends tied off")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="cargo_packer.py",
        description="Load planning: fit math, load map, tie-down counts")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("fit", help="cube fit with 80% ceiling")
    sp.add_argument("--cargo", required=True,
                    help="'L120xW80xH60:2,L60xW40xH40:5' (cm)")
    sp.add_argument("--space", required=True, help="'L400xW200xH200' (cm)")
    sp.set_defaults(fn=cmd_fit)

    sp = sub.add_parser("loadmap", help="ASCII load map + tie-down plan")
    sp.add_argument("--cargo", required=True)
    sp.add_argument("--space", required=True)
    sp.set_defaults(fn=cmd_loadmap)

    sp = sub.add_parser("checklist", help="securing checklist by weight")
    sp.add_argument("--weight-lb", type=float, required=True)
    sp.add_argument("--surface", default="pickup",
                    choices=["pickup", "trailer", "box-truck"])
    sp.set_defaults(fn=cmd_checklist)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
