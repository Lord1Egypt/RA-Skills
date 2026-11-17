#!/usr/bin/env python3
"""ev-charge-planner: home EV charging math — time, cost, TOU arbitrage, gas delta.

Pure-stdlib. Three tools:
  session -- battery kWh needed + charger power + rate plan -> hours:minutes
            to target, energy split across TOU windows, cost, breaker-load
            sanity, and miles added.
  compare -- monthly fuel cost EV vs gas car at your prices and mileage, with
            public-charging mix and efficiency adjustments.
  tou     -- plan overnight charging inside an off-peak window: computes
            latest-safe-finish (departure time minus buffer), suggests amperage
            reduction to fit the window comfortably, prices alternatives.

Usage:
  python3 ev_planner.py session --kwh-needed 32 --kw 7.4 --rate 0.23 \
      --battery 60 --departure "07:00"
  python3 ev_planner.py compare --kwh100mi 28 --miles-month 900 --gas-price 4.10 \
      --gas-mpg 30 --home-rate 0.14 --public-pct 20 --public-rate 0.48
  python3 ev_planner.py tou --kwh-needed 44 --kw 11 --offpeak "23:00-07:00" \
      --rate 0.11 --regular-rate 0.34 --departure "06:30" --buffer-min 30
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta

EVSE_EFFICIENCY = 0.90  # wall-to-battery losses (~10%: inverter + cable + heat)
KW_AT_240 = {16: 3.8, 24: 5.8, 32: 7.7, 40: 9.6, 48: 11.5}  # amps -> kW @ L2
MILES_PER_KWH_TYPICAL = 3.4


def parse_hhmm(s: str) -> int:
    h, m = s.strip().split(":")
    return int(h) * 60 + int(m)


def fmt_min(m: float) -> str:
    return f"{int(m // 60)}h{int(m % 60):02d}m"


def parse_window(s: str):
    a, b = s.split("-")
    start, end = parse_hhmm(a), parse_hhmm(b)
    length = (end - start) % (24 * 60)
    return start, end, length


def cmd_session(args):
    hours = args.kwh_needed / (args.kw * EVSE_EFFICIENCY)
    minutes = hours * 60
    cost = args.kwh_needed / EVSE_EFFICIENCY * args.rate
    wall_kwh = args.kwh_needed / EVSE_EFFICIENCY
    miles = args.kwh_needed * MILES_PER_KWH_TYPICAL * (args.ev_mi_per_kwh / MILES_PER_KWH_TYPICAL)

    print("=" * 62)
    print(f"CHARGE SESSION — need {args.kwh_needed:.1f} kWh into battery")
    print("=" * 62)
    print(f"Charger: {args.kw} kW   (wall-to-battery efficiency ~{EVSE_EFFICIENCY:.0%})")
    print(f"Wall energy drawn: {wall_kwh:.1f} kWh")
    print(f"Time to target: {fmt_min(minutes)}  ({hours:.2f} h)")
    print(f"Cost @ ${args.rate:.3f}/kWh: ${cost:.2f}")
    if args.battery:
        pct = args.kwh_needed / args.battery * 100
        print(f"Battery: {args.kwh_needed:.0f}/{args.battery} kWh = {pct:.0f}% added")
    print(f"Miles added @ {args.ev_mi_per_kwh} mi/kWh: ~{miles:.0f} mi")

    if args.house_amps and args.panel_amps:
        evse_amps = args.kw / 0.24
        load_pct = (args.house_amps + evse_amps) / args.panel_amps * 100
        print(f"\nPanel load check: house {args.house_amps}A + EVSE ~{evse_amps:.0f}A "
              f"on {args.panel_amps}A panel = {load_pct:.0f}%")
        if load_pct > 80:
            headroom = (args.panel_amps * 0.80 - args.house_amps) * 0.24
            print(f"  !! ABOVE 80% continuous-load guidance. Drop charger to "
                  f"~{headroom:.1f} kW or enable load management.")
        else:
            print(f"  OK (under 80% continuous guidance).")

    if args.departure:
        done = parse_hhmm(args.departure) - minutes
        start = int(done) % (24 * 60)
        print(f"\nTo finish by {args.departure} (100% target): start at "
              f"{start // 60:02d}:{start % 60:02d}")
    return 0


def cmd_compare(args):
    home_miles = args.miles_month * (1 - args.public_pct / 100)
    public_miles = args.miles_month * args.public_pct / 100

    home_kwh = home_miles / args.ev_mi_per_kwh / EVSE_EFFICIENCY
    public_kwh = public_miles / args.ev_mi_per_kwh / EVSE_EFFICIENCY
    ev_cost = home_kwh * args.home_rate + public_kwh * args.public_rate

    gas_gal = args.miles_month / args.gas_mpg
    gas_cost = gas_gal * args.gas_price

    print("=" * 62)
    print(f"MONTHLY FUEL COST — {args.miles_month:,} mi/month")
    print("=" * 62)
    print(f"EV:  {home_kwh:.0f} kWh home @ ${args.home_rate:.3f} = ${home_kwh * args.home_rate:.0f}")
    print(f"     {public_kwh:.0f} kWh public @ ${args.public_rate:.2f} = ${public_kwh * args.public_rate:.0f}"
          f"  ({args.public_pct}% of miles)")
    print(f"     total EV: ${ev_cost:.0f}/mo  ({ev_cost / args.miles_month * 100:.2f} $/100mi)")
    print(f"GAS: {gas_gal:.0f} gal @ ${args.gas_price:.2f} = ${gas_cost:.0f}/mo "
          f"({gas_cost / args.miles_month * 100:.2f} $/100mi)")
    delta = gas_cost - ev_cost
    print(f"\nEV saves ${delta:.0f}/month  →  ${delta * 12:.0f}/year"
          f"  ({delta / gas_cost * 100:.0f}% cheaper)" if delta > 0 else
          f"\nEV COSTS ${-delta:.0f}/mo MORE (heavy public charging?)" )
    if args.public_pct > 50:
        print("\nNote: >50% public charging at DC rates erases most home-charging")
        print("savings — the economics of EV ownership live at home.")
    eff_gas = 33.7 * args.gas_mpg  # MPGe equivalent for context
    print(f"\nContext: your gas car = {eff_gas:.0f} MPGe-equivalent efficiency.")
    return 0


def cmd_tou(args):
    start, end, length = parse_window(args.offpeak)
    hours = args.kwh_needed / (args.kw * EVSE_EFFICIENCY)
    fit_min = hours * 60

    print("=" * 62)
    print(f"TOU OVERNIGHT PLAN — off-peak {args.offpeak} ({fmt_min(length)} window)")
    print("=" * 62)
    print(f"Need {args.kwh_needed:.1f} kWh at {args.kw} kW = {fmt_min(fit_min)}")
    offpeak_cost = args.kwh_needed / EVSE_EFFICIENCY * args.rate
    regular_cost = args.kwh_needed / EVSE_EFFICIENCY * args.regular_rate
    print(f"Off-peak cost: ${offpeak_cost:.2f}   at regular rate: ${regular_cost:.2f}   "
          f"save ${regular_cost - offpeak_cost:.2f}/session")

    dep = parse_hhmm(args.departure)
    buf = args.buffer_min
    latest_finish = (dep - buf) % (24 * 60)
    avail = (latest_finish - start) % (24 * 60)

    print(f"\nDeparture {args.departure} with {buf}min buffer → must finish by "
          f"{latest_finish // 60:02d}:{latest_finish % 60:02d}")
    if avail >= fit_min:
        slack = avail - fit_min
        latest_start = int(latest_finish - fit_min) % (24 * 60)
        print(f"FITS: {fmt_min(avail)} available, {fmt_min(slack)} slack.")
        print(f"  Latest safe start: {latest_start // 60:02d}:{latest_start % 60:02d}")
        if slack < 30:
            print("  Tight — a charging fault eats the whole slack. Start at window open.")
    else:
        deficit = fit_min - avail
        # amperage reduction is wrong direction; need HIGHER power or trim energy
        kw_fit = args.kwh_needed / EVSE_EFFICIENCY / (avail / 60)
        print(f"DOES NOT FIT: short by {fmt_min(deficit)}.")
        print(f"  Options:")
        print(f"  a) raise charger to {kw_fit:.1f} kW (if EVSE + breaker allow)")
        part = avail / 60 * EVSE_EFFICIENCY * args.kw
        extra = (args.kwh_needed - part) / EVSE_EFFICIENCY * (args.regular_rate - args.rate)
        print(f"  b) accept {part:.1f} kWh tonight ({part * args.ev_mi_per_kwh:.0f} mi) "
              f"and top up tomorrow")
        print(f"  c) use regular-rate tail: charge {fmt_min(avail)} off-peak, "
              f"remaining {args.kwh_needed - part:.1f} kWh at "
              f"${args.regular_rate:.3f} (≈ ${extra:.2f} extra vs all off-peak)")
    print("\nRule: finish charging well before departure — cars do battery")
    print("conditioning/balancing after charge completes; departing mid-charge")
    print("on cold days costs range.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Home EV charging planner")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("session")
    s.add_argument("--kwh-needed", type=float, required=True)
    s.add_argument("--kw", type=float, required=True, help="charger power kW (e.g. 7.4, 11)")
    s.add_argument("--rate", type=float, required=True, help="$ per kWh")
    s.add_argument("--battery", type=float, default=0)
    s.add_argument("--ev-mi-per-kwh", type=float, default=MILES_PER_KWH_TYPICAL)
    s.add_argument("--house-amps", type=float, default=0, help="baseline house load A")
    s.add_argument("--panel-amps", type=float, default=0, help="panel size A")
    s.add_argument("--departure", default="", help="HH:MM target finish time")

    c = sub.add_parser("compare")
    c.add_argument("--kwh100mi", type=float, default=28, help="ignored; use --ev-mi-per-kwh")
    c.add_argument("--ev-mi-per-kwh", type=float, default=3.4)
    c.add_argument("--miles-month", type=float, required=True)
    c.add_argument("--home-rate", type=float, required=True)
    c.add_argument("--public-pct", type=float, default=10)
    c.add_argument("--public-rate", type=float, default=0.48)
    c.add_argument("--gas-price", type=float, required=True)
    c.add_argument("--gas-mpg", type=float, required=True)

    t = sub.add_parser("tou")
    t.add_argument("--kwh-needed", type=float, required=True)
    t.add_argument("--kw", type=float, required=True)
    t.add_argument("--offpeak", required=True, help="HH:MM-HH:MM")
    t.add_argument("--rate", type=float, required=True)
    t.add_argument("--regular-rate", type=float, required=True)
    t.add_argument("--departure", required=True)
    t.add_argument("--buffer-min", type=int, default=30)
    t.add_argument("--ev-mi-per-kwh", type=float, default=MILES_PER_KWH_TYPICAL)

    args = p.parse_args(argv)
    return {"session": cmd_session, "compare": cmd_compare, "tou": cmd_tou}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
