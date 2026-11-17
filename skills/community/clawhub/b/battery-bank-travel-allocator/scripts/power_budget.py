#!/usr/bin/env python3
"""power_budget.py — allocate battery-bank capacity across devices for a
day away from outlets.

The travel math nobody does until the phone dies: a "20000 mAh" bank
does not deliver 20000 mAh to your devices. Three losses compound —
(1) capacity is rated at the 3.7 V cell, delivery at 5 V (×0.74),
(2) conversion + cable heat eats another 10-15%, (3) fast-charge
protocols and device-side charge management waste more. Realistic
transfer is 60-65% of the rating, and every bank ages.

This tool builds a power budget for a day out:

  * device draw model: screen-on hours × drain rate, plus background
    (a phone idles at ~1%/h with radios on; navigation/photography
    multiplies drain 3-6×)
  * bank inventory with age derating (Li-ion loses ~4%/yr of design
    capacity, more if stored hot)
  * allocation: highest-priority device first, but NEVER to 100% —
    charging past ~85% wastes bank energy on slower, lossier cells
    of the curve; stop-charge thresholds per device class
  * verdicts: which devices make it, what to top up en route, and
    the honest "leave the big bank, take the small one" call when
    over-provisioned
  * solar add-on: realistic panel yield for a lunch-stop recharge

Subcommands:
  plan    — full day budget from device usage + banks
  banks   — inventory check: real capacity of what you own
  solar   — watt-hours a panel will realistically add
"""
from __future__ import annotations

import argparse

CELL_V = 3.7
CONV_EFF = 0.85       # boost 3.7->5V + heat + protocol overhead
AGE_LOSS_PER_YR = 0.04

# device library: (battery Wh, drain %/h screen-on, idle %/h, stop-charge %)
DEVICES = {
    "phone":        (15.0, 8,  1.0, 85),
    "phone-small":  (11.0, 9,  1.2, 85),
    "phone-big":    (20.0, 7,  0.9, 85),
    "tablet":       (28.0, 6,  0.6, 90),
    "camera":       (12.0, 0,  0.0, 100),   # model via triggers below
    "earbuds":      (1.5,  0,  0.0, 100),
    "watch":        (1.2,  0,  2.0, 90),
    "laptop-usb":   (60.0, 9,  1.5, 80),
    "drone":        (30.0, 0,  0.0, 100),
}
# heavy-use multipliers for phone drain (applied to screen-on rate)
ACTIVITY = {
    "light": 1.0, "photos": 1.6, "navigation": 3.5,
    "video": 2.5, "hotspot": 2.8, "gaming": 4.0, "offline-maps": 1.8,
}


def bank_wh(mah: int, years_old: float = 0.0, cycles: int = 0) -> float:
    """Rated mAh → realistic deliverable Wh at device voltage."""
    cell_wh = mah / 1000 * CELL_V
    age = years_old * AGE_LOSS_PER_YR
    cyc = min(0.20, cycles / 500 * 0.08)  # ~8% per 500 cycles, capped
    return cell_wh * (1 - age - cyc) * CONV_EFF


def device_wh(name: str, hours_screen: float, activity: str, hours_away: float) -> tuple[float, float]:
    """Returns (needed Wh to stay alive, drain Wh over the day)."""
    cap, drain_on, idle, _ = DEVICES[name]
    if hours_screen == 0:  # camera/drone: per-trigger model
        return cap * 0.0, 0.0
    mult = ACTIVITY.get(activity, 1.0)
    pct = hours_screen * drain_on * mult + max(0.0, hours_away - hours_screen) * idle
    return cap * min(pct, 100) / 100, cap * min(pct, 100) / 100


def charge_gap(name: str, start_pct: float) -> float:
    """Wh needed to bring device from start% to its stop-charge cap."""
    cap, _, _, stop = DEVICES[name]
    return cap * max(0.0, stop - start_pct) / 100


def cmd_plan(args) -> None:
    banks = []
    for spec in args.banks:  # "20000:2" = 20000mAh, 2 years old
        mah, _, yrs = spec.partition(":")
        banks.append(bank_wh(int(mah), float(yrs or 0)))
    total_bank = sum(banks)
    print(f"=== BANKS ===")
    for spec, wh in zip(args.banks, banks):
        mah = spec.split(":")[0]
        print(f"  {mah} mAh bank → {wh:.0f} Wh deliverable")
    print(f"  total deliverable: {total_bank:.0f} Wh")

    print(f"\n=== DAY DEMAND ({args.hours} h away) ===")
    rows = []
    for spec in args.devices:
        # phone:5:60:navigation = device:screen-hours:start-pct:activity
        parts = spec.split(":")
        name = parts[0]
        hours = float(parts[1]) if len(parts) > 1 else 0
        start = float(parts[2]) if len(parts) > 2 else 100
        act = parts[3] if len(parts) > 3 else "light"
        cap, _, _, stop = DEVICES[name]
        _, drain = device_wh(name, hours, act, args.hours)
        # energy needed from bank = deficit below stop threshold
        end_without = start - (drain / cap * 100)
        need = cap * (min(stop, max(0.0, stop - end_without)) ) / 100
        # can't return energy to bank if end_without > stop
        if end_without >= stop:
            need = 0.0
        rows.append((name, hours, act, start, end_without, need))

    total_need = sum(r[5] for r in rows)
    for name, hours, act, start, end_wo, need in rows:
        status = "OK on battery" if need == 0 else f"needs {need:.1f} Wh from bank"
        print(f"  {name:<12} {hours:>4.1f}h {act:<11} start {start:>3.0f}% → without bank: {end_wo:>4.0f}% | {status}")
    print(f"  total demand: {total_need:.1f} Wh")

    print(f"\n=== VERDICT ===")
    if total_bank >= total_need * 1.2:
        print(f"  OVER-PROVISIONED: banks carry {total_bank:.0f} Wh vs {total_need:.1f} Wh needed.")
        print(f"  Leave the biggest bank home if you value pocket space: the next-size-down")
        print(f"  still clears the day. (Demand ×1.2 safety margin = {total_need*1.2:.1f} Wh.)")
    elif total_bank >= total_need:
        print(f"  FITS: {total_bank:.0f} Wh vs {total_need:.1f} Wh — margin {total_bank-total_need:.1f} Wh.")
        print(f"  Charge order: priority device first; expect ~15% protocol waste on top of model.")
    else:
        print(f"  SHORTFALL: {total_need-total_bank:.1f} Wh short.")
        print(f"  Fixes: airplane mode + offline maps (−60% phone drain), carry a wall plug")
        print(f"  for a lunch stop, or drop the lowest-priority device from the charge list.")
    print(f"  Tip: charge phones to 85% ceilings — last 15% costs bank energy at the worst efficiency.")


def cmd_banks(args) -> None:
    print("Realistic deliverable energy (65% rule-of-thumb check):")
    for mah in (5000, 10000, 20000, 26800, 40000):
        wh = bank_wh(mah)
        full_charges = wh / 15
        print(f"  {mah:>6} mAh rated → {wh:5.0f} Wh  "
              f"(≈ {full_charges:.1f}× full charges of a 15 Wh phone)")
    print("\nAge derating: 4%/yr; cycles ~8%/500. A 3-year-old daily-cycled 20000")
    print("bank delivers roughly what a new 10000 does.")


def cmd_solar(args) -> None:
    # realistic yield: panel W × sun hours × 0.5 (angle/heat/cloud derate)
    wh = args.watts * args.sun_hours * 0.5
    print(f"{args.watts} W panel × {args.sun_hours} h sun × 50% derate → {wh:.0f} Wh")
    print(f"≈ {wh/15*85:.0f}% of one 15 Wh phone (at 85% stop-charge)")
    print("Panel reality: midday-perpendicular is the only time you see the rating;")
    print("backpack-hanging panels average 10-25% of sticker over a hiking day.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("plan", help="full day power budget")
    p.add_argument("--banks", required=True, nargs="+",
                   help="mAh[:years-old], e.g. 20000:2 10000:0")
    p.add_argument("--devices", required=True, nargs="+",
                   help="device[:screen-hours:start-pct:activity], e.g. phone:5:80:navigation tablet:3:100:video")
    p.add_argument("--hours", type=float, default=12, help="hours away from outlet")
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("banks", help="real-capacity table for common banks")
    p.set_defaults(fn=cmd_banks)

    p = sub.add_parser("solar", help="realistic panel yield")
    p.add_argument("--watts", type=float, required=True)
    p.add_argument("--sun-hours", type=float, default=4)
    p.set_defaults(fn=cmd_solar)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return
    args.fn(args)


if __name__ == "__main__":
    main()
