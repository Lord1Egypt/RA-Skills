#!/usr/bin/env python3
"""pd_compatibility_checker.py - USB-C Power Delivery compatibility gate.

Modes:
  check  - verdict for a device <-> charger <-> cable triple
  table  - print the PD rules ladder used for verdicts
  watt   - what a device needs to hit full speed (wattage decoder)

Verdict ladder: OK / CAPPED / SLOW / NO-CHARGE / DANGER.

Knows: PD revision caps (2.0 fixed-only, 3.0 PPS, 3.1 EPR 140/240W),
voltage/current steps, cable resistor logic (e-marked 5A vs 3A),
proprietary protocols (VOOC/SuperVOOC, SCP, QC, PPVS/PPS),
dummy-trap detection (charge-only cables, non-compliant ports).

Zero dependencies (Python 3.8+ stdlib). Educational reference; when
in doubt, trust the label on the hardware, not this script.
"""
import argparse
import json
import sys

# ------------------------------------------------- PD fixed steps (PD 2.0/3.0 SPR)
PD_FIXED_PDO = [
    # (volts, max amps at that step)
    (5, 3.0), (9, 3.0), (15, 3.0), (20, 5.0),
]
# PD 3.1 EPR adds:
PD_EPR_PDO = [(28, 5.0), (36, 5.0), (48, 5.0)]

# ------------------------------------------------- device archetype library
# full_speed_w: watts needed for max charge rate
# min_w: below this many phones throttle charge or refuse
# protocols: what it can negotiate beyond standard PD
DEVICES = {
    "phone-basic": {"full_speed_w": 18, "min_w": 10,
                    "protocols": ["pd2", "pd3"], "note": "typical midrange phone"},
    "phone-flagship": {"full_speed_w": 30, "min_w": 15,
                       "protocols": ["pd2", "pd3", "pps"],
                       "note": "Pixel/Galaxy/base iPhone tier"},
    "phone-proprietary": {"full_speed_w": 65, "min_w": 15,
                          "protocols": ["pd2", "pd3", "pps", "vooc"],
                          "note": "full rate only on proprietary (VOOC/SCP) chargers"},
    "iphone-plus": {"full_speed_w": 27, "min_w": 15,
                    "protocols": ["pd2", "pd3"],
                    "note": "Plus/Pro Max iPhones (~27W PD)"},
    "laptop-ultrabook": {"full_speed_w": 65, "min_w": 45,
                         "protocols": ["pd2", "pd3"],
                         "note": "13-14in ultrabook"},
    "laptop-performance": {"full_speed_w": 100, "min_w": 65,
                           "protocols": ["pd2", "pd3"],
                           "note": "15-16in performance laptop"},
    "laptop-gaming": {"full_speed_w": 240, "min_w": 100,
                      "protocols": ["pd2", "pd3", "epr"],
                      "note": "gaming laptop, 16in+; full rate often proprietary"},
    "tablet": {"full_speed_w": 35, "min_w": 18,
               "protocols": ["pd2", "pd3", "pps"],
               "note": "large tablet"},
    "steam-deck": {"full_speed_w": 45, "min_w": 30,
                   "protocols": ["pd2", "pd3"],
                   "note": "handheld console"},
    "camera": {"full_speed_w": 15, "min_w": 9,
               "protocols": ["pd2", "pd3"],
               "note": "mirrorless camera USB-C PD"},
    "earbuds": {"full_speed_w": 5, "min_w": 2.5,
                "protocols": ["pd2"],
                "note": "tiny-battery devices; prefer low-power ports"},
    "power-bank": {"full_speed_w": 65, "min_w": 20,
                   "protocols": ["pd2", "pd3", "pps"],
                   "note": "PD power bank input"},
}

CHARGERS = {
    "5w-brick": {"max_w": 5, "protocols": ["dumb"], "note": "legacy 5V/1A brick"},
    "10w-brick": {"max_w": 10, "protocols": ["dumb"], "note": "legacy 5V/2A"},
    "18w-pd": {"max_w": 18, "protocols": ["pd2", "pd3"], "note": "QC/PD18 travel brick"},
    "20w-pd": {"max_w": 20, "protocols": ["pd2", "pd3"], "note": "Apple 20W tier"},
    "30w-pd": {"max_w": 30, "protocols": ["pd2", "pd3", "pps"], "note": "phone-fast tier"},
    "45w-pd": {"max_w": 45, "protocols": ["pd2", "pd3", "pps"], "note": "deck/laptop tier"},
    "65w-pd": {"max_w": 65, "protocols": ["pd2", "pd3", "pps"], "note": "1-port laptop brick"},
    "100w-pd": {"max_w": 100, "protocols": ["pd2", "pd3", "pps"], "note": "multi-port flagship"},
    "140w-pd": {"max_w": 140, "protocols": ["pd2", "pd3", "pps", "epr"], "note": "EPR 28V tier"},
    "240w-pd": {"max_w": 240, "protocols": ["pd2", "pd3", "pps", "epr"], "note": "EPR 48V max"},
    "vooc-65": {"max_w": 65, "protocols": ["pd2", "pd3", "vooc"], "note": "proprietary 65W"},
}

CABLES = {
    "2a-cheap": {"max_a": 2.0, "emarked": False, "data": True,
                 "note": "unmarked bargain cable (assume 3A? no - assume worse)"},
    "3a-standard": {"max_a": 3.0, "emarked": False, "data": True,
                    "note": "standard USB-C, 60W cap at 20V"},
    "3a-charge-only": {"max_a": 3.0, "emarked": False, "data": False,
                       "note": "charge-only (no data lines) - traps, KVMs, docks"},
    "5a-emarked": {"max_a": 5.0, "emarked": True, "data": True,
                   "note": "e-marked 100W cable"},
    "5a-epr240": {"max_a": 5.0, "emarked": True, "data": True, "epr": True,
                  "note": "EPR-rated 240W (50V/5A) cable"},
}


def negotiated_watts(charger, device, cable):
    """Best common PD operating point given cable current cap."""
    shared = set(charger["protocols"]) & set(device["protocols"]) & {"pd2", "pd3"}
    if not shared:
        return 0.0, "no common PD revision"
    best = 0.0
    steps = PD_FIXED_PDO[:]
    if "epr" in charger["protocols"] and "epr" in device["protocols"] \
            and cable.get("epr"):
        steps += PD_EPR_PDO
    for v, a in steps:
        a_eff = min(a, cable["max_a"])
        w = v * a_eff
        if w <= charger["max_w"] and w > best:
            best = w
    # cable amps may cap below the charger's headline
    return best, None


def cmd_check(args):
    dev = DEVICES.get(args.device)
    chg = CHARGERS.get(args.charger)
    cab = CABLES.get(args.cable)
    if not (dev and chg and cab):
        sys.exit("unknown archetype; see `table` for the catalog")
    print("Device  : %s (%s)" % (args.device, dev["note"]))
    print("Charger : %s (%s)" % (args.charger, chg["note"]))
    print("Cable   : %s (%s)" % (args.cable, cab["note"]))
    print()

    warnings = []
    # proprietary fast-charge check
    proprietary_miss = None
    if "vooc" in dev["protocols"] and "vooc" not in chg["protocols"]:
        proprietary_miss = (
            "device's %dW full rate needs its proprietary protocol; on "
            "standard PD expect ~%dW" % (dev["full_speed_w"],
                                         min(chg["max_w"], 30)))
    if not cab["data"]:
        warnings.append("charge-only cable: no data lines -> PD negotiation "
                        "IMPOSSIBLE over most such cables -> 5V/dumb mode")

    w, why = negotiated_watts(chg, dev, cab)
    if why:
        verdict = "NO-CHARGE"
    elif not cab["data"]:
        # charge-only usually kills negotiation
        verdict = "NO-CHARGE"
        w = 0.0
    else:
        eff = min(w, chg["max_w"])
        if eff >= dev["full_speed_w"]:
            verdict = "OK"
        elif eff >= dev["min_w"]:
            verdict = "CAPPED"
        elif eff > 0:
            verdict = "SLOW"
        else:
            verdict = "NO-CHARGE"
        w = eff

    print("Negotiated power : %.0f W" % w)
    print("Device needs     : %.0f W full / %.0f W min" %
          (dev["full_speed_w"], dev["min_w"]))
    print("VERDICT          : %s" % verdict)
    if verdict == "OK":
        print("  Charges at full designed rate.")
    elif verdict == "CAPPED":
        print("  Charges, but below max rate (%.0fW of %.0fW). Fine overnight."
              % (w, dev["full_speed_w"]))
    elif verdict == "SLOW":
        print("  Device will throttle charging or refuse; use a bigger brick.")
    elif verdict == "NO-CHARGE":
        print("  This combination will not fast-charge at all (5V fallback "
              "at best).")
    if proprietary_miss:
        print("NOTE: %s" % proprietary_miss)
    for warn in warnings:
        print("WARNING: %s" % warn)
    if cab["max_a"] < 5.0 and chg["max_w"] > 60:
        print("WARNING: %.0fW charger on a %dA cable caps at %.0fW — "
              "get an e-marked 5A cable."
              % (chg["max_w"], cab["max_a"], 20 * cab["max_a"]))
    return 0


def cmd_table(args):
    print("PD fixed voltage steps (SPR):")
    for v, a in PD_FIXED_PDO:
        print("  %2dV @ up to %.1fA = %.0fW" % (v, a, v * a))
    print("PD 3.1 EPR steps (need e-marked EPR cable):")
    for v, a in PD_EPR_PDO:
        print("  %2dV @ up to %.1fA = %.0fW" % (v, a, v * a))
    print()
    print("Cable rules:")
    print("  no e-marker + no 5A claim -> 3A cap -> 60W max (20V x 3A)")
    print("  e-marked 5A               -> 100W max (20V x 5A)")
    print("  EPR-rated (50V)           -> 140/240W capable")
    print()
    print("Device archetypes:")
    for k, v in sorted(DEVICES.items()):
        print("  %-20s full %3dW  min %3dW  [%s]" %
              (k, v["full_speed_w"], v["min_w"], ",".join(v["protocols"])))
    print()
    print("Charger archetypes:")
    for k, v in sorted(CHARGERS.items()):
        print("  %-12s %3dW  [%s]" % (k, v["max_w"], ",".join(v["protocols"])))
    return 0


def cmd_watt(args):
    print("What %.0fW means:" % args.watts)
    for v in (5, 9, 15, 20, 28, 36, 48):
        a = args.watts / v
        if a <= 5.0:
            print("  = %.0fW is %dV @ %.2fA" % (args.watts, v, a))
    tiers = [
        (7.5, "trickle (earbuds/case)"),
        (15, "slow phone charge (overnight fine)"),
        (20, "standard phone fast charge"),
        (30, "flagship phone full rate / PPS sweet spot"),
        (45, "handheld console / small laptop entry"),
        (65, "ultrabook single-port standard"),
        (100, "performance laptop"),
        (140, "EPR tier (needs EPR cable)"),
        (240, "EPR max - gaming laptops, tiny minority"),
    ]
    label = None
    for t, desc in tiers:
        if args.watts <= t:
            label = desc
            break
    if label:
        print("  class: %s" % label)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("check", help="device x charger x cable verdict")
    sp.add_argument("--device", required=True)
    sp.add_argument("--charger", required=True)
    sp.add_argument("--cable", required=True)
    sp.set_defaults(func=cmd_check)

    sp = sub.add_parser("table", help="print rule tables")
    sp.set_defaults(func=cmd_table)

    sp = sub.add_parser("watt", help="decode a wattage")
    sp.add_argument("--watts", type=float, required=True)
    sp.set_defaults(func=cmd_watt)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
