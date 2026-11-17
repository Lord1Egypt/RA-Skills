#!/usr/bin/env python3
"""List the transportation options Amazon actually offers for a plan.

    python3 list_carriers.py <planId> [--config plan.json]

Run this after placement is confirmed but before you pin a carrier in your
config. `carrier.name` must match the returned string EXACTLY — these are
account- and lane-specific, so guessing from a carrier's marketing name (or
from another seller's config) will fail with "carrier not offered".

The output also shows each option's `preconditions`. An empty list means no
delivery window is required; ['CONFIRMED_DELIVERY_WINDOW'] means one must be
booked before confirmation.

Amazon SEND is the exception that needs no window. Own-carrier SPD/LTL, FIST
carriers and most others do need one. Read this field per option — never
hardcode either answer.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spapi import ENDPOINT, request  # noqa: E402

BASE = ENDPOINT + "/inbound/fba/2024-03-20"


def _req(method, path, body=None, params=None):
    return request(method, BASE + path, body=body, params=params)


def _paged(path, params, key):
    out, page_params = [], dict(params)
    while True:
        page = _req("GET", path, params=page_params)
        out.extend(page.get(key, []))
        token = page.get("pagination", {}).get("nextToken")
        if not token:
            return out
        page_params = dict(params, paginationToken=token)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan_id")
    ap.add_argument("--config", help="plan config JSON, used to generate options if absent")
    args = ap.parse_args()

    plan = _req("GET", f"/inboundPlans/{args.plan_id}")
    print(f"plan {args.plan_id}  ({plan.get('status')})\n")

    seen = {}
    for s in plan.get("shipments", []):
        sid = s["shipmentId"]
        options = _paged(f"/inboundPlans/{args.plan_id}/transportationOptions",
                         {"shipmentId": sid}, "transportationOptions")
        if not options:
            print(f"  {sid[:14]}: no options yet — run generateTransportationOptions first\n"
                  f"     (create_inbound_plan.py --resume {args.plan_id} does this)")
            continue
        print(f"  shipment {sid[:14]}  ({len(options)} options)")
        for o in options:
            name = o.get("carrier", {}).get("name", "?")
            cost = o.get("quote", {}).get("cost", {}).get("amount", "?")
            pre = o.get("preconditions") or []
            print(f"     {o.get('shippingSolution','?'):<26} {o.get('shippingMode','?'):<12} "
                  f"${cost:<8} preconditions={pre or 'NONE'}")
            print(f"       carrier.name = {name!r}")
            seen.setdefault(name, (o.get("shippingMode"), o.get("shippingSolution")))
        print()

    if seen:
        print("Paste one of these into your config's `carrier` block:\n")
        for name, (mode, solution) in sorted(seen.items()):
            print(json.dumps({"shipping_mode": mode, "shipping_solution": solution,
                              "name": name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
