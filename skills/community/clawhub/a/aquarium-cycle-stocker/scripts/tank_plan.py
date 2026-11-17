#!/usr/bin/env python3
"""Aquarium cycle planner, stocking calculator, water-change scheduler (freshwater).

Subcommands:
  cycle  — dated fishless-cycle calendar (optionally bacteria-seeded), clearance gate
  stock  — adult-size bioload + compatibility + schooling screen, wave plan
  wc     — water-change size/frequency to hold nitrate at target given tap nitrate

Species database embedded (common community species, adult cm + shape class + params).
stdlib only.
"""
import argparse
import datetime as dt
import json
import sys

# name: (adult_cm, shape_factor, temp_C band, pH band, schooling_min, temperament, level)
SPECIES = {
    "neon tetra":        (3.5, 1.0, (20, 26), (5.5, 7.0), 6, "peaceful", "mid"),
    "ember tetra":       (2.5, 1.0, (22, 28), (5.0, 7.0), 6, "peaceful", "mid"),
    "harlequin rasbora": (4.5, 1.0, (22, 27), (5.5, 7.0), 6, "peaceful", "mid"),
    "chili rasbora":     (2.0, 1.0, (23, 28), (5.0, 6.5), 8, "peaceful", "mid"),
    "cardinal tetra":    (4.0, 1.0, (22, 27), (5.0, 6.5), 6, "peaceful", "mid"),
    "zebra danio":       (5.0, 1.0, (18, 26), (6.5, 7.5), 6, "lively", "top"),
    "tiger barb":        (7.0, 1.3, (22, 27), (6.0, 7.5), 6, "semi-aggressive", "mid"),
    "cherry barb":       (5.0, 1.0, (22, 27), (6.0, 7.0), 6, "peaceful", "mid"),
    "honey gourami":     (5.0, 1.3, (22, 28), (6.0, 7.5), 2, "peaceful", "top"),
    "dwarf gourami":     (8.0, 1.3, (24, 28), (6.0, 7.5), 1, "semi-aggressive", "top"),
    "betta":             (6.0, 1.3, (24, 28), (6.5, 7.5), 1, "aggressive-fins", "all"),
    "corydoras":         (5.5, 1.3, (22, 26), (6.0, 7.5), 6, "peaceful", "bottom"),
    "bronze cory":       (7.0, 1.3, (22, 26), (6.0, 7.5), 6, "peaceful", "bottom"),
    "otocinclus":        (4.0, 1.0, (22, 27), (6.0, 7.5), 6, "peaceful", "glass"),
    "bristlenose pleco": (12.0, 2.0, (21, 27), (6.0, 7.5), 1, "peaceful", "bottom"),
    "common pleco":      (35.0, 3.0, (22, 28), (6.5, 7.5), 1, "peaceful", "bottom"),
    "fancy goldfish":    (20.0, 2.0, (18, 22), (7.0, 7.5), 1, "messy", "all"),
    "angelfish":         (15.0, 2.0, (24, 28), (6.0, 7.0), 4, "semi-aggressive", "mid"),
    "discus":            (16.0, 2.0, (28, 30), (5.5, 6.5), 4, "shy", "mid"),
    "guppy":             (4.0, 1.0, (22, 27), (7.0, 8.0), 3, "peaceful", "top"),
    "killifish":         (6.0, 1.0, (22, 26), (6.0, 7.0), 2, "semi-aggressive", "top"),
    "kuhli loach":       (10.0, 1.0, (24, 30), (5.5, 6.5), 5, "peaceful", "bottom"),
    "white cloud":       (4.0, 1.0, (16, 22), (6.0, 7.5), 6, "peaceful", "mid"),
}

FILTER_CLASS = {"hob": 1.0, "canister": 1.15, "sponge": 0.95, "internal": 1.0, "undergravel": 0.9}

CONFLICTS = [
    ("betta", "neon tetra", "RISKY", "neons can nip betta fins; prefer ember/chili rasbora"),
    ("betta", "guppy", "NO", "guppy coloration/flowing fins trigger betta aggression"),
    ("betta", "tiger barb", "NO", "barbs shred betta fins"),
    ("tiger barb", "guppy", "NO", "barbs nip guppy fins relentlessly"),
    ("tiger barb", "betta", "NO", "barbs shred betta fins"),
    ("angelfish", "neon tetra", "RISKY", "adult angels eat neons; cardinals slightly safer"),
    ("discus", "tiger barb", "NO", "barbs too boisterous for discus"),
    ("fancy goldfish", "neon tetra", "NO", "temp bands don't overlap (18-22 vs 20-26 edge) + goldfish eat small fish"),
    ("common pleco", "fancy goldfish", "RISKY", "plecos can latch onto goldfish slime coat at night"),
]


def cmd_cycle(args):
    print(f"FISHLESS CYCLE PLAN — {args.volume} L @ {args.temp}°C"
          + (" (bacteria-seeded)" if args.bacteria else ""))
    if not 20 <= args.temp <= 28:
        print("  ⚠ temp outside 20-28: bacteria colonize much slower/fish stress at extremes")
    start = dt.date.today()
    rate = 1.0 if not args.bacteria else 0.5  # seeded timeline fraction (~2 wk vs ~4)
    phases = [
        (1, f"Dose surfactant-free ammonia to {args.target:.0f} ppm. Test NH₃ & NO₂ (baseline)."),
        (3, "NH₃ falling, NO₂ appearing: Nitrosomonas at work. Re-dose NH₃ to target when <1 ppm."),
        (7, "NO₂ spike phase (can go off-scale >5 ppm). TOXIC — no fish, ever. Keep feeding the cycle."),
        (12, "NO₂ falling, NO₃ climbing: Nitrospira colonizing. Keep NH₃ at 2-3 ppm."),
        (17, "CLEARANCE TEST: dose 2 ppm ammonia. If NH₃=0 AND NO₂=0 within 24 h → cycled."),
        (19, "Confirm gate a 2nd time. Big (80%) water change + full dechlor to reset NO₃, then stock wave 1."),
    ]
    for day, msg in phases:
        d = start + dt.timedelta(days=round((day - 1) * rate))
        print(f"  Day {day:>3} ({d}): {msg}")
    total = round(21 * rate) if args.bacteria else 28
    print(f"\n  Expected duration: ~{total} days at {args.temp}°C "
          + ("(seeded accelerates; verify with tests, not calendar)" if args.bacteria
             else "(4-6 wk typical; verify with tests, not calendar)"))
    print("  GATE (both required twice): 2 ppm ammonia → 0 NH₃ & 0 NO₂ in 24 h.")
    print("  Speed levers: seeded media from a cycled tank = days; 27-28°C; strong aeration; pH>7.")
    print("  Emergency (fish already in): daily 25-50% changes + Prime, feed every other day, test daily.")


def load_factor(sp):
    return sp[1]


def cmd_stock(args):
    picks = []
    for spec in args.fish or []:
        try:
            count_s, _, name = spec.partition(" ")
            count = int(count_s)
            name = name.strip().lower()
        except ValueError:
            sys.exit(f"Bad --fish '{spec}' (use: '6 neon tetra')")
        if name not in SPECIES:
            close = [k for k in SPECIES if name.split()[0] in k]
            sys.exit(f"Unknown species '{name}'. Close matches: {close}. DB: {sorted(SPECIES)}")
        picks.append((count, name, SPECIES[name]))

    capacity = args.volume * FILTER_CLASS[args.filter]
    load = sum(c * sp[0] * sp[1] for c, _, sp in picks)
    pct = 100 * load / capacity
    verdict = "OK" if pct <= 75 else ("MAX" if pct <= 115 else "OVERSTOCKED")

    print(f"STOCKING — {args.volume} L, {args.filter} filter (capacity {capacity:.0f} cm-fish)")
    for c, name, sp in picks:
        print(f"  {c}× {name:<18} adult {sp[0]:>4.1f} cm × {sp[1]} shape = {c*sp[0]*sp[1]:>5.1f} load "
              f"| {sp[6]:<6} | {sp[5]}")
    print(f"  ADULT bioload: {load:.1f} / {capacity:.0f} = {pct:.0f}% → {verdict}")
    if pct > 115:
        print("  ↳ cut counts or upgrade filtration; sustained >115% kills by ammonia, slowly.")
    elif pct > 75:
        print("  ↳ heavy but manageable: strict water-change schedule + watch NH₃ weekly.")
    print("  NOTE: pet stores sell juveniles — you are signing an adult-size IOU at the register.")

    # schooling
    for c, name, sp in picks:
        if sp[4] and c < sp[4]:
            print(f"  SCHOOLING VIOLATION: {name} needs ≥{sp[4]} (have {c}) — stress/pine/short life.")

    # compatibility
    names = [n for _, n, _ in picks]
    probs = 0
    for a in names:
        for b in names:
            if a == b:
                continue
            for x, y, sev, why in CONFLICTS:
                if a == x and b == y:
                    print(f"  CONFLICT [{sev}] {x} + {y}: {why}")
                    probs += 1
    # parameter overlap
    if picks:
        t_lo = max(sp[2][0] for _, _, sp in picks)
        t_hi = min(sp[2][1] for _, _, sp in picks)
        p_lo = max(sp[3][0] for _, _, sp in picks)
        p_hi = min(sp[3][1] for _, _, sp in picks)
        print(f"  PARAMS: temp overlap {t_lo}-{t_hi}°C " + ("✓" if t_lo <= t_hi else "✗ NO OVERLAP"))
        print(f"          pH overlap {p_lo}-{p_hi} " + ("✓" if p_lo <= p_hi else "✗ NO OVERLAP"))

    waves = min(3, len(picks))
    order = sorted(picks, key=lambda p: (-p[0], p[1]))
    print(f"  STOCK IN WAVES (14 days apart, bacteria must catch up):")
    for i, (c, name, _) in enumerate(order[:waves], 1):
        print(f"    wave {i}: {c}× {name}   (+14d before next)")
    if len(picks) > waves:
        print(f"    wave {waves+1}: {' + '.join(f'{c}× {n}' for c, n, _ in order[waves:])}")
    if probs == 0 and pct <= 75:
        print("\n  VERDICT: sound community plan. Quarantine new fish 4-6 weeks before display.")


def cmd_wc(args):
    if args.tap >= args.target:
        print(f"  IMPOSSIBLE: tap nitrate ({args.tap}) ≥ target ({args.target}).")
        print("  Water changes alone can never reach target. Options: pothos/fast plants,")
        print("  NO₃ resin, RO/DI blend to cut tap nitrate, or accept a higher target.")
        return
    if args.nitrate <= args.target:
        print(f"  Already at/below target ({args.nitrate} ≤ {args.target}). Test weekly, change 25%/2wk.")
        return
    frac = 1 - (args.target - args.tap) / (args.nitrate - args.tap)
    l = args.volume * frac
    print(f"  ONE-SHOT to target: change {100*frac:.0f}% ({l:.0f} L) now.")
    if args.production:
        f = args.production / (args.target - args.tap)
        l2 = args.volume * f
        print(f"  HOLD at target with production {args.production} ppm/wk: {100*f:.0f}% weekly ({l2:.0f} L)")
        print("  (or split: " + f"{100*(1-(1-f)**0.5):.0f}% twice weekly)")
    else:
        print("  To compute a steady schedule, re-run with --production (measured ppm NO₃/week rise).")
    print("  Match temp ±1°C, dechlorinate before it touches the tank, never vacuum deep into substrate.")
    print("  Nitrate test: shake reagent #2 hard 30 s and tube 1 min — false lows are common.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("cycle")
    c.add_argument("--volume", type=float, required=True)
    c.add_argument("--temp", type=float, default=25.0)
    c.add_argument("--target", type=float, default=3.0, help="ammonia ppm to dose")
    c.add_argument("--bacteria", action="store_true", help="bottled bacteria seeded")
    c.set_defaults(fn=cmd_cycle)

    s = sub.add_parser("stock")
    s.add_argument("--volume", type=float, required=True)
    s.add_argument("--filter", default="hob", choices=sorted(FILTER_CLASS))
    s.add_argument("--fish", action="append", help="e.g. --fish '6 neon tetra' (repeatable)")
    s.set_defaults(fn=cmd_stock)

    w = sub.add_parser("wc")
    w.add_argument("--volume", type=float, required=True)
    w.add_argument("--nitrate", type=float, required=True)
    w.add_argument("--target", type=float, default=20.0)
    w.add_argument("--tap", type=float, default=0.0)
    w.add_argument("--production", type=float, default=0.0, help="ppm NO₃ per week")
    w.set_defaults(fn=cmd_wc)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
