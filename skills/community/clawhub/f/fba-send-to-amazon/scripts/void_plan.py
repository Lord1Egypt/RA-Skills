#!/usr/bin/env python3
"""Void ONE inbound plan, guarded by an exact shipment fingerprint.

    python3 void_plan.py <planId> --expect FBA1... FBA2... FBA3...
    python3 void_plan.py <planId> --expect FBA1... FBA2... FBA3... --yes

    python3 void_plan.py --find FBA1... FBA2...     # locate a plan by its shipments

Dry run by default. `--yes` is required to actually cancel.

Safety design, learned the hard way
-----------------------------------
Cancelling the wrong inbound plan destroys real shipments, and plans created
minutes apart look nearly identical. So:

  * The plan id is passed explicitly — never discovered-and-cancelled in one go.
  * --expect lists every FBA shipment id the plan must contain. The set must
    match EXACTLY. A subset match is not enough: a superset means you are about
    to cancel shipments you did not list.
  * Dry run is the default and prints exactly what would happen.
  * There is deliberately no "cancel everything matching X" mode, and no
    polling/retry loop. Never leave an unattended background process cancelling
    production shipments; a human should confirm each destructive run.

Cancellation is PUT /inboundPlans/{id}/cancellation — not DELETE, not POST /void.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spapi import ENDPOINT, request  # noqa: E402

BASE = ENDPOINT + "/inbound/fba/2024-03-20"


def _req(method, path, body=None, params=None):
    return request(method, BASE + path, body=body, params=params)


def fba_ids_of(plan_id):
    plan = _req("GET", f"/inboundPlans/{plan_id}")
    ids = set()
    for s in plan.get("shipments", []):
        d = _req("GET", f"/inboundPlans/{plan_id}/shipments/{s['shipmentId']}")
        if d.get("shipmentConfirmationId"):
            ids.add(d["shipmentConfirmationId"])
    return plan, ids


def find(expected: set[str]):
    """Scan ACTIVE plans for one whose shipments exactly match `expected`.

    Note: listInboundPlans is heavily indexed-lagged — a freshly created ACTIVE
    plan can be missing for many hours (voided ones show up sooner). If nothing
    is found here, query Seller Central's internal shipment endpoint from a
    logged-in browser instead; it resolves an FBA id to its plan immediately:

        GET /fba/shippingqueue/api/v1/shipment/queryShipment?shipmentId=<FBA id>
        -> { workflowId: <this is the inboundPlanId>, shipmentStatus, destinationFC, ... }
    """
    token = None
    while True:
        params = {"status": "ACTIVE", "sortBy": "CREATION_TIME",
                  "sortOrder": "DESC", "pageSize": 30}
        if token:
            params["paginationToken"] = token
        page = _req("GET", "/inboundPlans", params=params)
        for p in page.get("inboundPlans", []):
            pid = p["inboundPlanId"]
            _, ids = fba_ids_of(pid)
            mark = "MATCH" if ids == expected else "     "
            print(f"  {mark} {pid}  created={p.get('createdAt', '?')[:19]}  {sorted(ids)}")
            if ids == expected:
                print(f"\nTo cancel it:\n  python3 {Path(sys.argv[0]).name} {pid} "
                      f"--expect {' '.join(sorted(expected))} --yes")
                return pid
        token = page.get("pagination", {}).get("nextToken")
        if not token:
            break
    print("\nNo match. listInboundPlans lags by hours for new plans — see the "
          "Seller Central fallback in this script's docstring.")
    return None


def void(plan_id: str, expected: set[str], apply: bool):
    plan, ids = fba_ids_of(plan_id)
    print(f"plan      : {plan_id}")
    print(f"status    : {plan.get('status')}")
    print(f"shipments : {sorted(ids)}")

    if ids != expected:
        sys.exit("REFUSING: fingerprint mismatch.\n"
                 f"  --expect {sorted(expected)}\n"
                 f"  actual   {sorted(ids)}\n"
                 "  The sets must be exactly equal. Verify before retrying.")
    print(f"fingerprint: exact match on {len(ids)} shipments")

    if not apply:
        print("\nDRY RUN — nothing changed. Re-run with --yes to void.")
        return
    if plan.get("status") == "VOIDED":
        print("already VOIDED, nothing to do.")
        return

    r = _req("PUT", f"/inboundPlans/{plan_id}/cancellation", {})
    if "operationId" in r:
        for _ in range(60):
            op = _req("GET", f"/operations/{r['operationId']}")
            status = op.get("operationStatus")
            if status in ("SUCCESS", "SUCCEEDED"):
                break
            if status in ("FAILED", "FAILURE"):
                sys.exit(f"cancel FAILED: {op.get('operationProblems')}")
            time.sleep(3)
    print(f"VOIDED -> {_req('GET', f'/inboundPlans/{plan_id}').get('status')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan_id", nargs="?")
    ap.add_argument("--expect", nargs="+", metavar="FBA_ID",
                    help="every FBA shipment id the plan must contain (exact set)")
    ap.add_argument("--find", nargs="+", metavar="FBA_ID",
                    help="locate the ACTIVE plan containing exactly these shipments")
    ap.add_argument("--yes", action="store_true", help="actually cancel")
    args = ap.parse_args()

    if args.find:
        find(set(args.find))
        return
    if not args.plan_id or not args.expect:
        ap.error("need <planId> and --expect, or --find")
    void(args.plan_id, set(args.expect), args.yes)


if __name__ == "__main__":
    main()
