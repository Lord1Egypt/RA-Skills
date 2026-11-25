#!/usr/bin/env python3
"""Accessibility Ramp Builder — safe ramp geometry from your real rise.

A family member starts using a walker or wheelchair and the porch steps
become a wall. This tool engineers the ramp: required run length at the
right slope (1:12 self-propelled / 1:10 assisted / 1:8 walker), rest
landings every 30 in of rise, 60x60 in top/turn landings, handrails when
rise > 6 in, door-clearance checks, switchback layouts when the yard is
too short, threshold wedges under 1.5 in, a rough lumber takeoff, and
cost bands for wood / modular aluminum / concrete.

It refuses the dangerous shortcut: a steep ramp a self-propelled
wheelchair user cannot climb or safely descend.

Usage:
  ramp_builder.py --rise 22 --use self-propelled
  ramp_builder.py --rise 30 --use walker --space-ft 14 --door-width 30
  ramp_builder.py --existing-slope 1:8 --use self-propelled

stdlib only. Residential guidance built on ADA/ANSI geometry; verify
local permit rules.
"""
import argparse
import math
import sys

CONFIG = {
    # maximum rise:run ratios (run inches per 1 inch rise)
    "ratio": {"self-propelled": 12, "assisted": 10, "walker": 8},
    "max_rise_per_run_in": 30,     # rest platform required above this
    "landing_in": 60,              # top/bottom/turn landing (length & width)
    "min_clear_width_in": 36,
    "rail_rise_trigger_in": 6,     # handrails both sides above this rise
    "rail_height": (34, 38),
    "rail_extension_in": 12,
    "threshold_wedge_max_in": 1.5,
    "portable_max_in": 3,
    "door_clear_min_in": 32,
    "door_clear_ideal_in": 36,
    "max_cross_slope_pct": 2.08,   # 1:48
    # installed cost bands $/linear ft of ramp structure
    "cost_per_lf": {"wood": (100, 250), "modular-alum": (150, 300),
                    "concrete": (200, 400)},
}


def money(x):
    return f"${x:,.0f}"


def hr(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


def parse_slope(s):
    if ":" not in s:
        raise SystemExit("slope must look like 1:12")
    a, b = s.split(":")
    return float(b) / float(a)   # run per rise


def main():
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    p.add_argument("--rise", type=float, default=None,
                   help="total vertical rise to overcome, inches")
    p.add_argument("--use", choices=list(CONFIG["ratio"]),
                   default="self-propelled")
    p.add_argument("--space-ft", type=float, default=None,
                   help="straight run available outside the door, feet")
    p.add_argument("--door-width", type=float, default=None,
                   help="CLEAR width of the door (door minus frame/threshold)")
    p.add_argument("--existing-slope", default=None,
                   help="audit an existing ramp, e.g. 1:8")
    a = p.parse_args()

    # ---------------- existing-ramp audit ----------------
    if a.existing_slope:
        ratio = parse_slope(a.existing_slope)
        ok = {u: r for u, r in CONFIG["ratio"].items()}
        hr("EXISTING RAMP AUDIT")
        print(f"Stated slope: 1:{ratio:.0f} "
              f"({100 / ratio:.1f}% grade)")
        for u, r in ok.items():
            safe = ratio >= r
            print(f"  {u:15s} need 1:{r:<3d} → "
                  f"{'OK' if safe else 'TOO STEEP / UNSAFE'}")
        worst = ok[a.use]
        if ratio < worst:
            print(f"\nVERDICT: DANGEROUS for {a.use}.")
            print("  Descending a too-steep ramp is the real hazard —")
            print("  front casters lift, the chair runs away, and a fall")
            print("  backward is a head strike. Replace or re-build.")
        else:
            print(f"\nVERDICT: SAFE for {a.use} (and "
                  f"{', '.join(u for u, r in ok.items() if u != a.use and ratio >= r)}).")
        print("\nCross-slope: keep under 2% (1:48) — sideways tilt tips")
        print("occupied chairs off-balance on turns.")
        return 0

    if not a.rise:
        raise SystemExit("--rise (inches) or --existing-slope is required")

    ratio = CONFIG["ratio"][a.use]
    run_in = a.rise * ratio
    run_ft = run_in / 12
    runs = max(1, math.ceil(a.rise / CONFIG["max_rise_per_run_in"]))
    mid_landings = runs - 1
    total_struct_ft = run_ft + (mid_landings + 1) * (CONFIG["landing_in"] / 12)

    hr(f"RAMP ENGINE — {a.rise:.0f} in rise, {a.use} user")
    print(f"Slope standard .............. 1:{ratio} "
          f"({100 / ratio:.1f}% grade)")
    print(f"Required straight run ....... {run_ft:.1f} ft")
    if mid_landings:
        print(f"Rest platforms .............. {mid_landings} "
              f"(one per extra 30 in of rise)")
    print(f"Top + bottom landings ....... {CONFIG['landing_in']} in long × "
          f"{CONFIG['landing_in']} in wide each")
    print(f"Total structure length ...... {total_struct_ft:.1f} ft "
          "(incl. landings)")
    print(f"Clear width ................. {CONFIG['min_clear_width_in']} in "
          f"min ({CONFIG['min_clear_width_in'] + 4} in comfortable)")
    if a.rise > CONFIG["rail_rise_trigger_in"]:
        rail_len = 2 * (run_ft + (mid_landings + 1) * 5)
        print(f"Handrails ................... BOTH sides "
              f"(rise > {CONFIG['rail_rise_trigger_in']} in), "
              f"{CONFIG['rail_height'][0]}-{CONFIG['rail_height'][1]} in high,")
        print(f"                            12 in horizontal extensions; "
              f"≈ {rail_len:.0f} lf total railing")

    if a.rise <= CONFIG["threshold_wedge_max_in"]:
        hr("VERDICT: NO RAMP NEEDED")
        print(f"Rise {a.rise} in ≤ 1.5 in: a threshold wedge/bevel solves it.")
        print("Rubber or aluminum threshold ramp, $15-60. Done.")
        return 0
    if a.rise <= CONFIG["portable_max_in"]:
        hr("VERDICT: PORTABLE RAMP OK")
        print(f"Rise {a.rise} in ≤ 3 in: a portable suitcase ramp can work,")
        print("but check its rated slope at full extension and add edge")
        print("guards. For a walker user a short fixed ramp is still safer.")

    # ---------------- fit analysis ----------------
    if a.space_ft is not None:
        hr("FIT ANALYSIS")
        space_in = a.space_ft * 12
        if space_in >= run_in:
            print(f"Straight run fits: {a.space_ft:.1f} ft available vs "
                  f"{run_ft:.1f} ft needed. Build straight.")
        else:
            seg = run_in / 2
            # 180° switchback: two parallel runs + one 5x5 turn platform.
            # Wall-side footprint length = run + 5 ft turn platform,
            # depth = two runs side by side (~7-8 ft).
            sb_len = seg / 12 + CONFIG["landing_in"] / 12
            sb_depth = 2 * (CONFIG["min_clear_width_in"] + 4) / 12
            print(f"Space problem: {a.space_ft:.1f} ft available vs "
                  f"{run_ft:.1f} ft straight run required.")
            if a.use == "walker":
                steeper = a.rise * CONFIG["ratio"]["walker"] / 12
                print(f"  Option A: walker-grade 1:8 needs {steeper:.1f} ft — "
                      f"{'fits' if steeper <= a.space_ft else 'still too long'}.")
            print(f"  Option B: 180° switchback — two {seg / 12:.1f} ft parallel"
                  f" runs + a 5×5 ft turn platform:")
            print(f"           footprint ≈ {sb_len:.0f} ft along the wall × "
                  f"≈{sb_depth:.0f} ft out from it.")
            if sb_len <= a.space_ft:
                print(f"\nVERDICT: FITS AS SWITCHBACK ({sb_len:.0f} ft wall run).")
                print("  Keep the door landing level, and mind the turn")
                print("  platform rail placement so it doesn't eat the")
                print("  turning circle of the chair.")
            else:
                print("\nVERDICT: DOES NOT FIT as a ramp.")
                print("  Options left: re-grade the entry, move the door")
                print("  path, or a vertical platform lift (VPL) —")
                print("  lifts start around $3-5k installed and solve")
                print("  short-yard geometry a ramp cannot.")

    # ---------------- door check ----------------
    if a.door_width is not None:
        hr("DOOR CHECK")
        if a.door_width >= CONFIG["door_clear_ideal_in"]:
            print(f"{a.door_width} in clear — comfortable for wheelchairs.")
        elif a.door_width >= CONFIG["door_clear_min_in"]:
            print(f"{a.door_width} in clear — legal minimum 32 in; tight but")
            print("  workable. Swing-clear (offset) hinges can add ~2 in.")
        else:
            print(f"⚠ {a.door_width} in clear is BELOW the 32 in wheelchair")
            print("  minimum — the ramp leads to a door the chair can't enter.")
            print("  Fixes: swing-clear hinges (+2 in), a wider door, or")
            print("  removing the door entirely where privacy allows.")

    # ---------------- takeoff & cost ----------------
    hr("MATERIAL TAKEOFF (wood, rough)")
    deck_boards = math.ceil(run_in / 5.5) * runs        # 2x6 decking, 5.5 in
    stringers = math.ceil(CONFIG["min_clear_width_in"] / 16) + 1
    posts = (mid_landings + 1) * 2 + 4
    print(f"2×6 decking boards .......... {deck_boards} "
          f"({run_ft:.0f} lf of ramp surface)")
    print(f"Stringers (2×12) ............ {stringers} per run × {runs} runs")
    print(f"4×4 posts ................... {posts} (landings + rail posts)")
    print(f"Hardware + footing tubes .... galvanized, concrete footings below"
          "\n                             frost line where required")
    hr("COST BANDS (installed, per linear foot)")
    total = total_struct_ft
    for mat, (lo, hi) in CONFIG["cost_per_lf"].items():
        print(f"  {mat:14s} {money(lo * total)} – {money(hi * total)}")
    print("DIY wood material alone typically lands near the low band.")

    hr("BUILD RULES THAT KEEP PEOPLE SAFE")
    print("1. 1:12 for self-propelled is not bureaucratic polish —")
    print("   steeper ramps are descending runaways for hand-propelled chairs.")
    print(f"2. Rest platform at every {CONFIG['max_rise_per_run_in']} in of rise;")
    print(f"   landings {CONFIG['landing_in']}×{CONFIG['landing_in']} in, level.")
    print("3. Nosing edges + 2 in curbs or rail-edges so castors can't")
    print("   drop off the side; slip-resistant decking (or grip strips).")
    print(f"4. Cross-slope under 2% — measure with a level app both ways.")
    print("5. Drainage: ramp pitches shed water; never let ice form a")
    print("   film — position away from gutter downspouts.")
    print("6. PERMIT: ramps attached to the house commonly need one;")
    print("   setbacks/egress rules vary by town. ADA applies to public")
    print("   spaces — these residential numbers are the safety standard.")
    print("7. Landing at the door must be level — you cannot open a door")
    print("   while sitting on a slope.")
    print("\nVerify local code and utility lines before digging footings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
