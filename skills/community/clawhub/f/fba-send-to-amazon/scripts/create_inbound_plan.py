#!/usr/bin/env python3
"""Create an FBA inbound plan via SP-API Fulfillment Inbound v2024-03-20.

    python3 create_inbound_plan.py plan.json              # run the full flow
    python3 create_inbound_plan.py plan.json --resume ID  # continue a plan that
                                                          # already confirmed placement
    python3 create_inbound_plan.py --void PLAN_ID [...]   # cancel plan(s)

`plan.json` drives everything — see plan.example.json. Nothing about your
products or addresses is hardcoded here.

Operation order matters. Getting it wrong fails silently or with a misleading
error. setPackingInformation must run AFTER confirmPackingOption and BEFORE
confirmPlacementOption:

    createInboundPlan
      -> generatePackingOptions -> listPackingOptions
      -> confirmPackingOption
      -> setPackingInformation            (packingGroupId, not packingOptionId)
      -> generatePlacementOptions -> confirmPlacementOption   (pick the $0 one)
      -> generateTransportationOptions
      -> [book a delivery window ONLY if preconditions demand it]
      -> confirmTransportationOptions     (contactInformation goes HERE)

Every POST/PUT returns an operationId that must be polled to
operationStatus == "SUCCESS" (not "SUCCEEDED").
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spapi import ENDPOINT, MARKETPLACE, request  # noqa: E402

BASE = ENDPOINT + "/inbound/fba/2024-03-20"


# ── HTTP wrappers ────────────────────────────────────────────────────────────
def _req(method, path, body=None, params=None):
    return request(method, BASE + path, body=body, params=params)


def _poll(op_id, label, max_wait=300):
    for _ in range(max_wait // 3):
        r = _req("GET", f"/operations/{op_id}")
        status = r.get("operationStatus")
        if status in ("SUCCESS", "SUCCEEDED"):
            print(f"  [{label}] SUCCESS")
            return r
        if status in ("FAILED", "FAILURE"):
            problems = json.dumps(r.get("operationProblems", []), indent=2, ensure_ascii=False)
            raise RuntimeError(f"[{label}] FAILED:\n{problems}")
        time.sleep(3)
    raise TimeoutError(f"[{label}] timed out after {max_wait}s")


def _op(method, path, body=None, label=""):
    """Call an async endpoint and wait for the operation to finish."""
    r = _req(method, path, body)
    if "operationId" in r:
        _poll(r["operationId"], label or path)
    return r


def _paged(path, params, key):
    out, page_params = [], dict(params)
    while True:
        page = _req("GET", path, params=page_params)
        out.extend(page.get(key, []))
        token = page.get("pagination", {}).get("nextToken")
        if not token:
            return out
        page_params = dict(params, paginationToken=token)


# ── workflow steps ───────────────────────────────────────────────────────────
def create_plan(cfg):
    body = {
        "destinationMarketplaces": [cfg.get("marketplace_id", MARKETPLACE)],
        "name": cfg["plan_name"],
        "sourceAddress": cfg["source_address"],
        "items": [{"msku": s["msku"], "quantity": s["total_qty"],
                   "prepOwner": "SELLER", "labelOwner": "SELLER"} for s in cfg["skus"]],
    }
    print("1. createInboundPlan")
    r = _req("POST", "/inboundPlans", body)
    plan_id = r["inboundPlanId"]
    _poll(r["operationId"], "createInboundPlan")
    print(f"   plan: {plan_id}")
    return plan_id


def packing(plan_id):
    print("2. generatePackingOptions")
    _op("POST", f"/inboundPlans/{plan_id}/packingOptions", {}, "generatePackingOptions")
    options = _req("GET", f"/inboundPlans/{plan_id}/packingOptions")["packingOptions"]
    option = options[0]
    print(f"   option {option['packingOptionId']}  groups={option['packingGroups']}")

    print("3. confirmPackingOption")
    _op("POST",
        f"/inboundPlans/{plan_id}/packingOptions/{option['packingOptionId']}/confirmation",
        {}, "confirmPackingOption")
    return option["packingGroups"]


def set_packing(plan_id, group_id, cfg):
    """Declare N IDENTICAL boxes as ONE box object with quantity=N.

    This is the whole trick behind an even multi-warehouse split. BoxInput.quantity
    means "number of containers with identical weight/dimensions/contents", so
    Amazon treats the box as an indivisible atom and placement can only hand out
    whole boxes. Send N separate box objects (or skip packing info entirely) and
    Amazon re-splits by SKU into wildly uneven shipments.

    Required fields people commonly miss (each one returns a misleading 403):
      - contentInformationSource
      - labelOwner + prepOwner on every item
      - packingGroupId, NOT packingOptionId
      - never send boxId; it is an output-only field
    """
    box_cfg = cfg["box"]
    box = {
        "contentInformationSource": "BOX_CONTENT_PROVIDED",
        "dimensions": {
            "length": box_cfg["length"], "width": box_cfg["width"],
            "height": box_cfg["height"],
            "unitOfMeasurement": box_cfg.get("dimension_unit", "CM"),
        },
        "weight": {"unit": box_cfg.get("weight_unit", "KG"), "value": box_cfg["weight"]},
        "quantity": cfg["num_boxes"],
        "items": [{"msku": s["msku"], "quantity": s["per_box"],
                   "labelOwner": "SELLER", "prepOwner": "SELLER"} for s in cfg["skus"]],
    }
    per_box = sum(s["per_box"] for s in cfg["skus"])
    print(f"4. setPackingInformation — {cfg['num_boxes']} identical boxes "
          f"x {per_box}u = {per_box * cfg['num_boxes']}u")
    _op("POST", f"/inboundPlans/{plan_id}/packingInformation",
        {"packageGroupings": [{"packingGroupId": group_id, "boxes": [box]}]},
        "setPackingInformation")


def placement(plan_id):
    print("5. generatePlacementOptions")
    _op("POST", f"/inboundPlans/{plan_id}/placementOptions", {}, "generatePlacementOptions")
    options = _req("GET", f"/inboundPlans/{plan_id}/placementOptions")["placementOptions"]

    def fee(o):
        return sum(f.get("value", {}).get("amount", 0) for f in o.get("fees", []))

    for o in sorted(options, key=fee):
        print(f"   ${fee(o):>7.2f}  shipments={len(o['shipmentIds'])}  {o['placementOptionId']}")

    best = min(options, key=fee)
    print(f"6. confirmPlacementOption  ${fee(best):.2f}, {len(best['shipmentIds'])} shipments")
    _op("POST",
        f"/inboundPlans/{plan_id}/placementOptions/{best['placementOptionId']}/confirmation",
        {}, "confirmPlacementOption")
    return best["placementOptionId"], best["shipmentIds"]


def confirm_delivery_window(plan_id, sid, earliest=None):
    _op("POST", f"/inboundPlans/{plan_id}/shipments/{sid}/deliveryWindowOptions",
        {}, f"genDeliveryWindow {sid[:10]}")
    windows = _req("GET", f"/inboundPlans/{plan_id}/shipments/{sid}/deliveryWindowOptions")
    available = [w for w in windows["deliveryWindowOptions"]
                 if w.get("availabilityType") == "AVAILABLE"
                 and (not earliest or w["startDate"] >= earliest)]
    pick = min(available or windows["deliveryWindowOptions"], key=lambda w: w["startDate"])
    _op("POST", f"/inboundPlans/{plan_id}/shipments/{sid}/deliveryWindowOptions/"
                f"{pick['deliveryWindowOptionId']}/confirmation", {}, f"confDW {sid[:10]}")
    print(f"     window {pick['startDate'][:10]} ~ {pick['endDate'][:10]}")


def transportation(plan_id, placement_id, shipment_ids, cfg):
    carrier = cfg["carrier"]
    ready = {"start": cfg["ready_to_ship"]}     # WindowInput has ONLY `start`
    configs = [{"shipmentId": sid, "readyToShipWindow": ready} for sid in shipment_ids]

    for attempt in range(cfg.get("max_carrier_retries", 12)):
        suffix = f"  (attempt {attempt + 1})" if attempt else ""
        print(f"7. generateTransportationOptions  {carrier['shipping_mode']} / "
              f"{carrier['shipping_solution']}{suffix}")
        _op("POST", f"/inboundPlans/{plan_id}/transportationOptions",
            {"placementOptionId": placement_id,
             "shipmentTransportationConfigurations": configs},
            "generateTransportationOptions")

        print("8. select option per shipment")
        selections, total = [], 0.0
        for sid in shipment_ids:
            options = _paged(f"/inboundPlans/{plan_id}/transportationOptions",
                             {"shipmentId": sid}, "transportationOptions")
            wanted = [o for o in options
                      if o.get("shippingMode") == carrier["shipping_mode"]
                      and o.get("shippingSolution") == carrier["shipping_solution"]
                      and o.get("carrier", {}).get("name") == carrier["name"]]
            if not wanted:
                offered = sorted({(o.get("shippingMode"), o.get("carrier", {}).get("name"))
                                  for o in options})
                raise RuntimeError(
                    f"{sid}: carrier '{carrier['name']}' not offered. Available:\n"
                    + "\n".join(f"    {m} | {c}" for m, c in offered))

            pick = wanted[0]
            preconditions = pick.get("preconditions") or []
            total += pick.get("quote", {}).get("cost", {}).get("amount", 0)
            print(f"   {sid[:12]}  {pick['carrier']['name']}  "
                  f"${pick.get('quote', {}).get('cost', {}).get('amount', '?')}  "
                  f"preconditions={preconditions or 'NONE'}")

            # Book a delivery window only when Amazon demands one for this option.
            # Amazon SEND is the exception that needs none (empty preconditions);
            # own-carrier SPD/LTL, FIST carriers and most others return
            # CONFIRMED_DELIVERY_WINDOW. Read the field — never hardcode either way.
            if "CONFIRMED_DELIVERY_WINDOW" in preconditions:
                confirm_delivery_window(plan_id, sid, cfg.get("ready_to_ship", "")[:10])

            # contactInformation belongs in the CONFIRM request, per the official
            # ConfirmTransportationOptionsRequest example. Omitting it fails with
            # FBA_INB_0117 "partnered carrier is unavailable at the moment",
            # which reads like an Amazon outage but is a parameter error.
            selections.append({"shipmentId": sid,
                               "transportationOptionId": pick["transportationOptionId"],
                               "contactInformation": cfg["contact"]})
        print(f"   freight total: ${total:.2f}")

        print("9. confirmTransportationOptions")
        try:
            _op("POST", f"/inboundPlans/{plan_id}/transportationOptions/confirmation",
                {"transportationSelections": selections}, "confirmTransportationOptions")
            return
        except RuntimeError as e:
            # Transportation option IDs are single-use — a failed confirm burns
            # them, and reusing one returns FBA_INB_0348 "not AVAILABLE". So each
            # retry must regenerate and reselect, never re-post the same payload.
            if not any(code in str(e) for code in
                       ("FBA_INB_0117", "FBA_INB_0348", "InternalServerError")):
                raise
            wait = min(90, 15 * (attempt + 1))
            print(f"   carrier busy — regenerating and retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("carrier still unavailable after all retries")


def report(plan_id, shipment_ids, cfg, out_path: Path):
    print("\n" + "=" * 72)
    rows = []
    for sid in shipment_ids:
        s = _req("GET", f"/inboundPlans/{plan_id}/shipments/{sid}")
        items = _paged(f"/inboundPlans/{plan_id}/shipments/{sid}/items", {}, "items")
        boxes = _paged(f"/inboundPlans/{plan_id}/shipments/{sid}/boxes", {}, "boxes")
        rows.append({
            "fba_shipment_id": s.get("shipmentConfirmationId"),
            "shipment_api_id": sid,
            "amazon_reference_id": s.get("amazonReferenceId"),
            "warehouse_code": s.get("destination", {}).get("warehouseId"),
            # Real box ids, format FBA<id>U000001 (U + SIX digits). Downstream
            # customs paperwork must use these, never a guessed U{n:05d}.
            "box_codes": [b["boxId"] for b in boxes if b.get("boxId")],
            "boxes": sum(b.get("quantity", 1) for b in boxes),
            "units": sum(i["quantity"] for i in items),
            "items": [{"msku": i["msku"], "qty": i["quantity"]} for i in items],
        })
        r = rows[-1]
        print(f"  {r['fba_shipment_id']}  {r['warehouse_code']:5}  "
              f"{r['boxes']} box  {r['units']:>4} units")
    print(f"  TOTAL: {sum(r['boxes'] for r in rows)} boxes, "
          f"{sum(r['units'] for r in rows)} units")
    print("=" * 72)

    out_path.write_text(json.dumps({
        "inbound_plan_id": plan_id,
        "channel": cfg.get("channel", ""),
        "box_spec": cfg["box"],
        "shipments": rows,
    }, indent=2, ensure_ascii=False))
    print(f"saved -> {out_path}")


# ── entry points ─────────────────────────────────────────────────────────────
def run(cfg, out_path):
    plan_id = create_plan(cfg)
    groups = packing(plan_id)
    if len(groups) != 1:
        print(f"!! {len(groups)} packing groups — these SKUs cannot share one box type.")
        print("   Amazon requires separate boxes per group; an identical-box split")
        print("   is impossible as configured. Split the plan or adjust the SKU set.")
    for group in groups:
        set_packing(plan_id, group, cfg)
    placement_id, shipment_ids = placement(plan_id)
    transportation(plan_id, placement_id, shipment_ids, cfg)
    report(plan_id, shipment_ids, cfg, out_path)


def resume(plan_id, cfg, out_path):
    """Continue a plan whose placement option is already confirmed."""
    options = _req("GET", f"/inboundPlans/{plan_id}/placementOptions")["placementOptions"]
    accepted = [o for o in options if o.get("status") == "ACCEPTED"]
    if not accepted:
        raise RuntimeError(f"{plan_id}: no ACCEPTED placement option — start fresh instead")
    pid, sids = accepted[0]["placementOptionId"], accepted[0]["shipmentIds"]
    print(f"resume {plan_id}  placement={pid}  {len(sids)} shipments")
    transportation(plan_id, pid, sids, cfg)
    report(plan_id, sids, cfg, out_path)


def void(plan_id):
    # Cancellation is PUT /cancellation — not DELETE, not POST /void.
    _op("PUT", f"/inboundPlans/{plan_id}/cancellation", {}, f"cancel {plan_id[:12]}")
    print(f"{plan_id} -> {_req('GET', f'/inboundPlans/{plan_id}').get('status')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", nargs="?", help="plan config JSON")
    ap.add_argument("--resume", metavar="PLAN_ID")
    ap.add_argument("--void", nargs="+", metavar="PLAN_ID")
    ap.add_argument("--out", help="where to write the result JSON")
    args = ap.parse_args()

    if args.void:
        for pid in args.void:
            void(pid)
        return

    if not args.config:
        ap.error("config JSON is required (see plan.example.json)")
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out_path = Path(args.out) if args.out else \
        Path(args.config).with_name(Path(args.config).stem + "-result.json")

    if args.resume:
        resume(args.resume, cfg, out_path)
    else:
        run(cfg, out_path)


if __name__ == "__main__":
    main()
