#!/usr/bin/env python3
"""esim-travel-setup: international connectivity + 2FA-preservation planner.

Pure-stdlib. Four tools:
  plan    -- destination + days + data appetite -> which eSIM type fits
             (local / regional / global), rough data sizing from behavior,
             dual-SIM strategy, and a pre-departure checklist.
  twofa   -- audit your accounts for travel-authentication risk: which
             methods survive SIM swap / roam loss / new-device login walls,
             generate the export/backup plan BEFORE leaving.
  costs   -- compare roaming bundle vs eSIM vs local SIM for your trip with
             break-even days.
  checklist -- printable T-48h/T-24h/T-0 connectivity checklist.

Usage:
  python3 esim_planner.py plan --destination Japan --days 12 --maps-heavy
  python3 esim_planner.py twofa --bank --email-google --work-slack --crypto
  python3 esim_planner.py costs --destination "Mexico" --days 10 \
      --data-gb 5 --roaming-bundle 10 --roaming-gb 2
  python3 esim_planner.py checklist
"""
from __future__ import annotations

import argparse
import sys

# Data sizing: GB/day by behavior profile
DATA_PROFILES = {
    "light":      (0.15, "messaging, email, maps occasionally, light browsing"),
    "maps-heavy": (0.40, "navigation all day + lookups + social + music"),
    "heavy":      (0.80, "video calls, hotspot for laptop, streaming"),
    "work":       (1.20, "full workday on LTE: meetings, cloud IDE, large files"),
}

# Regional eSIM coverage groups (typical multi-country products)
REGIONS = {
    "Europe":     ["EU members", "UK", "Switzerland", "Norway", "Iceland", "Turkey (some)"],
    "Asia":       ["Japan", "South Korea", "Singapore", "Thailand", "Vietnam", "Malaysia", "Indonesia", "Hong Kong", "Taiwan"],
    "SEA":        ["Thailand", "Vietnam", "Singapore", "Malaysia", "Indonesia", "Philippines", "Cambodia", "Laos"],
    "North America": ["USA", "Canada", "Mexico"],
    "Latin America": ["Mexico", "Brazil", "Argentina", "Chile", "Colombia", "Peru"],
    "Africa":     ["South Africa", "Kenya", "Egypt", "Morocco", "Nigeria", "Tanzania"],
    "Global":     ["120-190 countries at lower per-GB value; for multi-region trips"],
}

COUNTRIES_2FA_RECOVERY = {
    # destination -> gotchas
    "China":       "Great Firewall: Google/WhatsApp/Instagram blocked without VPN; install VPN BEFORE arrival (app stores remove them inside China)",
    "Japan":       "clean Internet; note public wifi is sparse, eSIM strongly advised",
    "Russia":      "SMS delivery to foreign numbers unreliable; banking apps of sanctioned banks may fail abroad",
    "Iran":        "heavy filtering + SMS interconnect issues; connectivity itself is the risk",
    "USA":         "fine; foreign numbers receiving SMS sometimes pay per-message on prepaid",
    "Brazil":      "IMEI registration required for foreign phones (ANATEL) — do at airport or 3G/4G stops working after ~15 days",
    "Turkey":      "phone registration rules for long stays (>120 days tourist SIM rules); short trips fine",
    "India":       "eSIM works on main carriers; foreign SIM registration paper trail at kiosks takes 1-2h",
    "UAE":         "VoIP calls (WhatsApp/Meet) blocked without local plans; SMS fine",
    "Thailand":    "easy tourist SIMs at airport; eSIM also available from dtac/AIS",
}

ACCOUNTS = {
    # name -> (risk_if_no_access, auth_methods, pre-trip action)
    "bank": (10, "SMS OTP + app push",
             "ENABLE hardware-token/app-based 2FA (bank app key or TOTP); ask bank for a travel notice; get offline backup codes; if bank only does SMS OTP: keep home SIM ACTIVE with global roaming enabled for SMS (receive-only is usually free)"),
    "email-google": (10, "password + TOTP/prompt",
             "Enroll a BACKUP phone + print offline codes; add a travel phone number; check 'trusted devices' — a new-device login abroad can trigger ID-verification walls that need a phone you can't receive on"),
    "work-slack": (6, "SSO + MFA app",
             "Enroll 2 MFA methods; register the travel device as trusted BEFORE leaving"),
    "crypto": (10, "app + seed",
             "HARDWARE WALLET stays home in a safe; seed phrase NEVER travels in luggage photos/cloud; test that your exchange 2FA works on the travel device"),
    "social": (3, "TOTP mostly",
             "Offline codes; low stakes, quick to fix"),
    "icloud": (8, "device-bound + SMS fallback",
             "Add travel number as trusted; print recovery key — an iCloud lockout bricks Find-My and Apple Pay abroad"),
    "whatsapp": (5, "phone-number bound",
             "WhatsApp binds to your NUMBER: swapping eSIMs doesn't break it over wifi, but re-verification needs SMS — keep home SIM reachable via roaming"),
    "airline-hotel": (4, "email magic links",
             "Ensure email works (see email above); screenshot bookings offline"),
}


def cmd_plan(args):
    gb_day, desc = DATA_PROFILES[args.profile]
    total = gb_day * args.days
    print("=" * 62)
    print(f"CONNECTIVITY PLAN — {args.destination}, {args.days} days")
    print("=" * 62)
    print(f"Profile '{args.profile}': {desc}")
    print(f"Estimated data: {total:.1f} GB total ({gb_day} GB/day)")

    reg = None
    for r, members in REGIONS.items():
        if any(args.destination.lower() in m.lower() for m in members):
            reg = r
            break

    print("\neSIM choice:")
    if reg and reg != "Global":
        print(f"  Destination is in the '{reg}' regional group — a regional eSIM")
        print(f"  ({', '.join(members[:5])}...) usually beats per-country if you cross borders.")
        if args.days >= 10:
            print(f"  For {args.days} days, compare: local carrier eSIM (best $/GB, one-time)")
            print(f"  vs regional multi-country (convenience) vs global (multi-leg trips).")
    else:
        print("  Single-country trip: a LOCAL eSIM (Airalo/Saily/nomad or the carrier")
        print("  directly, e.g. Japan→Ubigi/KDDI) gives the best price and speeds.")
    print("  Rule of thumb: local > regional > global on $/GB; global wins only for")
    print("  3+ region hops.")

    gotcha = None
    for c, note in COUNTRIES_2FA_RECOVERY.items():
        if c.lower() in args.destination.lower():
            gotcha = note
            break
    if gotcha:
        print(f"\n!! {args.destination} gotcha: {gotcha}")

    print("\nDual-SIM strategy (keep home number ACTIVE):")
    print("  Slot/eSIM 1: home SIM — roaming RECEIVE-ONLY (free on most carriers;")
    print("              exists so bank OTPs and WhatsApp verification arrive)")
    print("  Slot/eSIM 2: travel eSIM — data + calls over IP")
    print("  Phone settings: default data = travel eSIM; 'allow cellular data")
    print("  switching' OFF; iMessage/RCS tied to home number as usual.")
    return 0


def cmd_twofa(args):
    ns = vars(args)
    selected = [(name, ACCOUNTS[name]) for name in ACCOUNTS if ns.get(name)]
    if not selected:
        selected = list(ACCOUNTS.items())

    print("=" * 62)
    print("2FA / ACCOUNT-ACCESS TRAVEL AUDIT")
    print("=" * 62)
    total_risk = 0
    for name, (risk, methods, action) in selected:
        total_risk += risk
        print(f"\n[{risk}/10 risk] {name} — auth: {methods}")
        print(f"   BEFORE DEPARTURE: {action}")
    print("\n" + "-" * 62)
    print(f"Aggregate exposure: {total_risk} risk-points across {len(selected)} accounts")
    print("\nUNIVERSAL RULES:")
    print("  1. Print offline backup codes — paper in two physical locations")
    print("     (wallet + luggage). Not photos. Not cloud notes.")
    print("  2. Test every MFA method on the DEVICE YOU TRAVEL WITH before leaving.")
    print("  3. Keep home SIM enabled for SMS receive via roaming — most banks still")
    print("     send OTP as SMS; receiving texts abroad is free on major carriers.")
    print("  4. Password manager available OFFLINE (cached vault on device).")
    print("  5. If a new-device login wall can hit (email/iCloud), pre-trust the")
    print("     travel device now — recovery abroad without your number is brutal.")
    return 0


def cmd_costs(args):
    print("=" * 62)
    print(f"COST COMPARISON — {args.destination}, {args.days} days, {args.data_gb} GB")
    print("=" * 62)
    esim_gb_price = 4.5  # typical blended $/GB for destination eSIMs
    esim_cost = max(args.data_gb * esim_gb_price, 5.0)
    daily_roam = args.roaming_bundle
    roam_cost = daily_roam * args.days
    roam_total_gb = args.roaming_gb * args.days
    local_sim_cost = 8.0 + args.data_gb * 2.5  # SIM + local data pricing

    rows = [
        ("Travel eSIM (pre-purchased)", esim_cost, args.data_gb,
         "install before flight, instant on landing"),
        ("Roaming bundle ($%.0f/day)" % daily_roam, roam_cost, roam_total_gb,
         "zero setup; watch the daily-charge auto-renew"),
        ("Local physical SIM on arrival", local_sim_cost, args.data_gb,
         "cheapest per GB; airport kiosk time + registration hassle"),
    ]
    rows.sort(key=lambda r: r[1])
    print(f"{'OPTION':38} {'COST':>7} {'DATA':>8}")
    for name, cost, gb, note in rows:
        print(f"{name:38} ${cost:>6.0f} {gb:>5.0f} GB   {note}")
    best = rows[0]
    print(f"\nCheapest: {best[0]} at ~${best[1]:.0f} for {args.days} days.")
    if roam_cost > esim_cost * 1.5:
        print(f"Roaming is {roam_cost / esim_cost:.1f}x the eSIM price — the daily")
        print(f"bundle is a convenience tax; fine for 1-3 day trips, not for {args.days}.")
    print("\nHidden factors: eSIM = airplane-mode-to-connected in 2 minutes;")
    print("physical SIM = queue + passport registration + eSIM-to-SIM swap risk")
    print("(loses your home number's SMS receive if your phone is single-SIM).")
    return 0


def cmd_checklist(_args):
    items = {
        "T-48h": [
            "buy + INSTALL the eSIM (activation on first connect at destination)",
            "run `twofa` audit; print backup codes (paper x2)",
            "add travel number to iCloud/Google trusted numbers",
            "enable SMS roaming RECEIVE on home carrier (usually free; verify)",
            "screenshot/queue offline maps for first hours (Google/organic maps)",
            "download airline/hotel/banking apps' data for offline use",
        ],
        "T-24h": [
            "verify eSIM appears in phone settings with a QR installed",
            "test one MFA login on the travel device (bank + email minimum)",
            "check destination gotchas: VPN needed? app-store restrictions?",
            "notify bank + card issuers of travel dates (fraud blocks otherwise)",
            "charge + pack: universal adapter, spare cable, power bank",
        ],
        "T-0 (airport)": [
            "BEFORE takeoff: enable eSIM line (it connects on landing)",
            "set travel eSIM as DEFAULT DATA; disable data on home SIM",
            "keep home SIM ON with roaming for SMS (receive-only)",
            "on landing: airplane mode OFF → data should attach in <2 min",
            "if no attach in 5 min: toggle airplane mode; check eSIM is 'on';",
            "  then manually select carrier network",
            "send the arrival message on your usual apps to confirm number alive",
        ],
    }
    print("=" * 62)
    print("CONNECTIVITY CHECKLIST")
    print("=" * 62)
    for phase, items_list in items.items():
        print(f"\n{phase}")
        for it in items_list:
            print(f"  [ ] {it}")
    print("\nFailure protocol: no data after 10 min → join airport wifi, open")
    print("eSIM provider app (needs internet ONCE), check activation status,")
    print("run their diagnostics; still dead → switch to roaming day-pass and")
    print("dispute the eSIM later. Never let connectivity block banking SMS.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Travel eSIM + 2FA planner")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("--destination", required=True)
    pl.add_argument("--days", type=int, required=True)
    pl.add_argument("--profile", default="maps-heavy", choices=list(DATA_PROFILES))

    tw = sub.add_parser("twofa")
    for flag in ACCOUNTS:
        tw.add_argument(f"--{flag}", dest=flag, action="store_true")

    co = sub.add_parser("costs")
    co.add_argument("--destination", required=True)
    co.add_argument("--days", type=int, required=True)
    co.add_argument("--data-gb", type=float, required=True)
    co.add_argument("--roaming-bundle", type=float, default=10.0,
                    help="$ per day for carrier travel pass")
    co.add_argument("--roaming-gb", type=float, default=2.0,
                    help="GB per day the pass allows")

    sub.add_parser("checklist")

    args = p.parse_args(argv)
    return {"plan": cmd_plan, "twofa": cmd_twofa,
            "costs": cmd_costs, "checklist": cmd_checklist}[args.cmd](args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
