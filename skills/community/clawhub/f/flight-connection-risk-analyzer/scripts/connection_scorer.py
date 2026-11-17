#!/usr/bin/env python3
"""Flight Connection Risk Analyzer — plan layovers above the legal floor.

Scores a connecting itinerary on four factors: buffer above Minimum Connect
Time, terminal-transfer reality at the hub, time-of-day delay stacking (US DOT
bands), and consequence asymmetry (last flight, winter hub, self-transfer).
Prints risk 0-100, a verdict, and a situation-specific protocol.

stdlib only. No network.
"""
import argparse
import json
import sys

# ---------------------------------------------------------------------------
# Hub knowledge base. MCTs are planning defaults (conservative mid-bands of
# airline filings); verify the airline's exact MCT when it matters.
# transfer_min: typical transfer between the terminals this connection type
# implies (includes re-security where unavoidable).
# ---------------------------------------------------------------------------
HUBS = {
    # code: {name, dom_dom_mct, dom_intl_mct, intl_dom_mct, intl_intl_mct,
    #        transfer: {type: minutes}, notes}
    "ATL": {"name": "Atlanta", "dom_dom_mct": 40, "dom_intl": 70, "intl_dom": 90, "intl_intl": 80,
            "transfer": {"dom-dom": 12, "dom-intl": 15, "intl-dom": 75, "intl-intl": 20},
            "notes": "Plane Train; intl arrivals = customs+recheck+TSA"},
    "DFW": {"name": "Dallas-Fort Worth", "dom_dom_mct": 45, "dom_intl": 70, "intl_dom": 85, "intl_intl": 75,
            "transfer": {"dom-dom": 8, "dom-intl": 10, "intl-dom": 70, "intl-intl": 15},
            "notes": "Skylink airside; among the easiest hubs"},
    "ORD": {"name": "Chicago O'Hare", "dom_dom_mct": 45, "dom_intl": 90, "intl_dom": 120, "intl_intl": 90,
            "transfer": {"dom-dom": 15, "dom-intl": 25, "intl-dom": 90, "intl-intl": 30},
            "notes": "T5 intl <-> T1-3 via ATS + re-security; winter pain"},
    "DEN": {"name": "Denver", "dom_dom_mct": 45, "dom_intl": 70, "intl_dom": 85, "intl_intl": 75,
            "transfer": {"dom-dom": 12, "dom-intl": 15, "intl-dom": 70, "intl-intl": 18},
            "notes": "Concourse train; winter de-ice stacks"},
    "IAH": {"name": "Houston Intercontinental", "dom_dom_mct": 45, "dom_intl": 70, "intl_dom": 85, "intl_intl": 75,
            "transfer": {"dom-dom": 12, "dom-intl": 15, "intl-dom": 70, "intl-intl": 18},
            "notes": "Skyway train; intl recheck in D/E"},
    "JFK": {"name": "New York JFK", "dom_dom_mct": 55, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 30, "dom-intl": 25, "intl-dom": 80, "intl-intl": 25},
            "notes": "AirTrain; most terminal pairs = exit + re-TSA"},
    "EWR": {"name": "Newark", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 15, "dom-intl": 20, "intl-dom": 75, "intl-intl": 20},
            "notes": "A-B connector exists; summer thunder season brutal"},
    "LGA": {"name": "New York LaGuardia", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 25, "dom-intl": 30, "intl-dom": 30, "intl-intl": 30},
            "notes": "Terminal changes = bus, leave security"},
    "SFO": {"name": "San Francisco", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 95, "intl_intl": 75,
            "transfer": {"dom-dom": 15, "dom-intl": 20, "intl-dom": 80, "intl-intl": 20},
            "notes": "Intl G re-security; morning fog delays"},
    "LAX": {"name": "Los Angeles", "dom_dom_mct": 55, "dom_intl": 90, "intl_dom": 110, "intl_intl": 90,
            "transfer": {"dom-dom": 25, "dom-intl": 30, "intl-dom": 90, "intl-intl": 30},
            "notes": "Bus between terminals; many pairs exit + re-TSA"},
    "SEA": {"name": "Seattle", "dom_dom_mct": 50, "dom_intl": 70, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 15, "dom-intl": 18, "intl-dom": 75, "intl-intl": 20},
            "notes": "Satellite train; intl recheck"},
    "CLT": {"name": "Charlotte", "dom_dom_mct": 42, "dom_intl": 65, "intl_dom": 85, "intl_intl": 70,
            "transfer": {"dom-dom": 10, "dom-intl": 12, "intl-dom": 70, "intl-intl": 15},
            "notes": "Compact; walks usually < 15 min"},
    "MSP": {"name": "Minneapolis", "dom_dom_mct": 45, "dom_intl": 70, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 12, "dom-intl": 15, "intl-dom": 75, "intl-intl": 18},
            "notes": "Winter hub; compact inside"},
    "DTW": {"name": "Detroit", "dom_dom_mct": 42, "dom_intl": 65, "intl_dom": 85, "intl_intl": 70,
            "transfer": {"dom-dom": 10, "dom-intl": 12, "intl-dom": 70, "intl-intl": 15},
            "notes": "ExpressTram; forgiving layout"},
    "PHX": {"name": "Phoenix", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 20, "dom-intl": 22, "intl-dom": 75, "intl-intl": 22},
            "notes": "T3-T4 walk = exit + re-security"},
    "LAS": {"name": "Las Vegas", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 18, "dom-intl": 20, "intl-dom": 75, "intl-intl": 20},
            "notes": "D-gate trams; terminal change = bus"},
    "BOS": {"name": "Boston", "dom_dom_mct": 50, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 22, "dom-intl": 25, "intl-dom": 78, "intl-intl": 25},
            "notes": "Terminal changes = outside security"},
    "MCO": {"name": "Orlando", "dom_dom_mct": 45, "dom_intl": 70, "intl_dom": 85, "intl_intl": 70,
            "transfer": {"dom-dom": 15, "dom-intl": 18, "intl-dom": 72, "intl-intl": 18},
            "notes": "Shuttles to airsides"},
    "AMS": {"name": "Amsterdam Schiphol", "dom_dom_mct": 50, "dom_intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "World-class; passport control at Schengen exit"},
    "CDG": {"name": "Paris Charles de Gaulle", "dom_dom_mct": 55, "dom_intl": 75, "intl_dom": 75, "intl_intl": 75,
            "transfer": {"dom-dom": 20, "dom-intl": 25, "intl-dom": 25, "intl-intl": 30},
            "notes": "2E-2G shuttle; distances kill beginners"},
    "FRA": {"name": "Frankfurt", "dom_dom_mct": 45, "dom_intl": 45, "intl_dom": 45, "intl_intl": 45,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Compact and efficient"},
    "MUC": {"name": "Munich", "dom_dom_mct": 40, "dom_intl": 40, "intl_dom": 40, "intl_intl": 40,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Excellent transfer machine"},
    "LHR": {"name": "London Heathrow", "dom_dom_mct": 60, "dom_intl": 75, "intl_dom": 75, "intl_intl": 75,
            "transfer": {"dom-dom": 30, "dom-intl": 30, "intl-dom": 30, "intl-intl": 35},
            "notes": "T4/T5 not walkable; bus-gate drives add minutes"},
    "IST": {"name": "Istanbul", "dom_dom_mct": 55, "dom_intl": 60, "intl_dom": 60, "intl_intl": 60,
            "transfer": {"dom-dom": 20, "dom-intl": 25, "intl-dom": 25, "intl-intl": 30},
            "notes": "Huge but walkable; security at some gate areas"},
    "YYZ": {"name": "Toronto Pearson", "dom_dom_mct": 55, "dom_intl": 75, "intl_dom": 90, "intl_intl": 75,
            "transfer": {"dom-dom": 20, "dom-intl": 25, "intl-dom": 80, "intl-intl": 25},
            "notes": "T1-T3 = exit security; US preclearance flips direction"},
    "HKG": {"name": "Hong Kong", "dom_dom_mct": 50, "dom_intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Automated people mover; efficient"},
    "SIN": {"name": "Singapore Changi", "dom_dom_mct": 50, "dom_intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Best-in-class transfers"},
    "ICN": {"name": "Seoul Incheon", "dom_dom_mct": 50, "dom_intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Efficient; occasional gate-change marches"},
    "NRT": {"name": "Tokyo Narita", "dom_dom_mct": 50, "dom_intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Compact terminals"},
    "HND": {"name": "Tokyo Haneda", "dom_dom_mct": 50, "dom-intl": 50, "intl_dom": 50, "intl_intl": 50,
            "transfer": {"dom-dom": 15, "dom-intl": 15, "intl-dom": 15, "intl-intl": 20},
            "notes": "Efficient; intl-dom adds immigration"},
}

# Departure-block delay stack (approx US DOT BTS late-departure rates).
DEP_BLOCKS = {
    "05-08": {"late_pct": 10, "label": "early morning — fresh aircraft"},
    "08-12": {"late_pct": 14, "label": "mid-morning"},
    "12-16": {"late_pct": 20, "label": "afternoon — congestion begins"},
    "16-20": {"late_pct": 30, "label": "evening push — cascading delays"},
    "20-24": {"late_pct": 36, "label": "late evening — worst stack + overnight risk"},
}
WINTER_HUBS = {"ORD", "DTW", "MSP", "DEN", "JFK", "EWR", "YYZ", "FRA"}


def base_risk(buffer_min: int) -> int:
    if buffer_min >= 60:
        return 5
    if buffer_min >= 40:
        return 20
    if buffer_min >= 25:
        return 40
    if buffer_min >= 10:
        return 60
    return 85


def score_connection(airport: str, layover_min: int, ctype: str,
                     dep_block: str = "12-16", season: str = "summer",
                     last_flight: bool = False, self_transfer: bool = False,
                     checked_bag: bool = False) -> dict:
    hub = HUBS.get(airport.upper())
    if not hub:
        return {"error": f"unknown hub '{airport}' — see --list-hubs; use generic bands + manual transfer estimate"}

    mct_field = {"dom-dom": "dom_dom_mct", "dom-intl": "dom_intl",
                 "intl-dom": "intl_dom", "intl-intl": "intl_intl"}[ctype]
    mct = hub[mct_field]
    transfer = hub["transfer"].get(ctype, 20)

    # Effective buffer: minutes above MCT, penalized when the physical
    # transfer itself eats into a sub-MCT-style budget.
    buffer = layover_min - mct
    effective = layover_min - max(mct, transfer + 25)  # 25 = deplane + door-close
    working_buffer = min(buffer, effective)

    risk = base_risk(working_buffer)

    blk = DEP_BLOCKS.get(dep_block, DEP_BLOCKS["12-16"])
    if blk["late_pct"] >= 30:
        risk += 12
    elif blk["late_pct"] >= 20:
        risk += 6
    else:
        risk += 0

    if last_flight:
        risk += 15
    if season == "winter" and airport.upper() in WINTER_HUBS:
        risk += 10
    if self_transfer:
        risk += 25
        if layover_min < 180:
            risk += 20  # doctrine: unprotected transfers need >= 3h
    if checked_bag and working_buffer < 35:
        risk += 8
    if layover_min >= 240:
        risk -= 10  # generous layovers absorb almost anything

    risk = max(0, min(100, risk))
    if risk <= 24:
        verdict = "SAFE"
    elif risk <= 49:
        verdict = "TIGHT"
    elif risk <= 74:
        verdict = "HIGH RISK"
    else:
        verdict = "RUSSIAN ROULETTE"

    protocol = []
    if verdict in ("TIGHT", "HIGH RISK", "RUSSIAN ROULETTE"):
        protocol.append("Seat within first 10 rows of the inbound aircraft.")
        protocol.append("Carry-on only — do not check a bag on this itinerary.")
    protocol.append(f"Transfer at {airport}: {hub['notes']}")
    if "intl-dom" in ctype and airport not in ("AMS", "CDG", "FRA", "MUC", "LHR", "IST", "HKG", "SIN", "ICN", "NRT", "HND"):
        protocol.append("US-style intl arrival: customs + bag recheck + re-enter TSA — keep moving, lines are the killer.")
    if self_transfer:
        protocol.append("SELF-TRANSFER: no airline protection — know the next fare and the refund rule before booking.")
    if last_flight:
        protocol.append("LAST FLIGHT: identify the morning-after flight now; ask about hotel-voucher policy at rebooking.")
    if season == "winter" and airport.upper() in WINTER_HUBS:
        protocol.append("Winter northern hub: assume de-ice queues; anything under 60 min buffer is a coin flip.")
    if risk <= 24:
        protocol.append("Plenty of slack — normal ops you'll have time to eat.")

    return {
        "airport": f"{airport.upper()} ({hub['name']})",
        "connection_type": ctype,
        "layover_min": layover_min,
        "mct_min": mct,
        "transfer_min_est": transfer,
        "buffer_over_mct": buffer,
        "working_buffer_min": working_buffer,
        "dep_block": f"{dep_block} ({blk['label']}, ~{blk['late_pct']}% late)",
        "self_transfer": self_transfer,
        "last_flight": last_flight,
        "risk": risk,
        "verdict": verdict,
        "protocol": protocol,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--airport", help="connection hub IATA code")
    ap.add_argument("--layover", type=int, help="scheduled layover in minutes")
    ap.add_argument("--type", dest="ctype", default="dom-dom",
                    choices=["dom-dom", "dom-intl", "intl-dom", "intl-intl"])
    ap.add_argument("--dep-block", default="12-16",
                    choices=list(DEP_BLOCKS.keys()),
                    help="departure block of the INBOUND leg")
    ap.add_argument("--season", default="summer", choices=["summer", "winter"])
    ap.add_argument("--last-flight", action="store_true")
    ap.add_argument("--self-transfer", action="store_true")
    ap.add_argument("--checked-bag", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-hubs", action="store_true")
    args = ap.parse_args()

    if args.list_hubs:
        for code, h in sorted(HUBS.items()):
            print(f"{code:4} {h['name']:28} dom-dom MCT {h['dom_dom_mct']:3}  intl-dom MCT {h['intl_dom']:3}  | {h['notes']}")
        return 0

    if not args.airport or not args.layover:
        ap.error("--airport and --layover are required (or --list-hubs)")

    r = score_connection(args.airport, args.layover, args.ctype, args.dep_block,
                         args.season, args.last_flight, args.self_transfer,
                         args.checked_bag)
    if "error" in r:
        print(r["error"], file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(r, indent=2))
        return 0

    print(f"\n=== Connection Risk: {r['airport']} ===")
    print(f"  Type:                {r['connection_type']}")
    print(f"  Scheduled layover:   {r['layover_min']} min")
    print(f"  MCT (planning):      {r['mct_min']} min")
    print(f"  Transfer est.:       {r['transfer_min_est']} min")
    print(f"  Buffer over MCT:     {r['buffer_over_mct']} min")
    print(f"  Working buffer:      {r['working_buffer_min']} min (after deplane + door-close + transfer)")
    print(f"  Inbound dep block:   {r['dep_block']}")
    print(f"  RISK SCORE:          {r['risk']}/100")
    print(f"  VERDICT:             {r['verdict']}")
    print("\n  Protocol:")
    for p in r["protocol"]:
        print(f"   - {p}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
