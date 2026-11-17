#!/usr/bin/env python3
"""Turn an inbound-plan result file into one shipment JSON per FBA shipment.

    python3 build_shipments.py plan-result.json --lines lines.json --out shipments/

`plan-result.json` is what Claw School's (claw-school.com) companion skill
**fba-send-to-amazon** writes
(`create_inbound_plan.py` → `<config>-result.json`). It already contains, per
shipment: the FBA id, the Amazon reference id, the warehouse code, the real box
ids, and the box/unit counts — so none of that has to be retyped or looked up
in the web UI.

If you did not use that skill, build the same structure from SP-API directly:

    d  = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}
    bx = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}/boxes

    d["shipmentConfirmationId"]   -> fba_shipment_id
    d["amazonReferenceId"]        -> reference_id
    d["destination"]["warehouseId"] -> warehouse_code
    bx[i]["boxId"]                -> box_code   (verbatim; never derive it)

`lines.json` is the declaration content of ONE box — the same for every box when
the boxes are identical:

    {
      "ticket": {"channel": "...", "dest_country": "US", "customs_type": "..."},
      "items":  [{"product_key": "<key into your product data>", "qty": 14}, ...]
    }

For non-identical boxes, write the shipment files by hand or extend this script;
`items` is per box, not per shipment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan_result")
    ap.add_argument("--lines", required=True, help="per-box declaration content")
    ap.add_argument("--out", default="shipments")
    args = ap.parse_args()

    plan = json.loads(Path(args.plan_result).read_text(encoding="utf-8"))
    lines = json.loads(Path(args.lines).read_text(encoding="utf-8"))
    ticket = dict(lines.get("ticket", {}))
    items = lines["items"]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for s in plan["shipments"]:
        fba, fc = s["fba_shipment_id"], s["warehouse_code"]
        box_codes = s.get("box_codes") or []
        n_boxes = s.get("boxes", len(box_codes) or 1)

        if len(box_codes) < n_boxes:
            print(f"!  {fba}: {len(box_codes)} box_codes for {n_boxes} boxes — "
                  "boxes with no code will be blank on the invoice")

        boxes = [{
            "box_seq": i + 1,
            "fba_shipment_id": fba,
            "reference_id": s.get("amazon_reference_id", ""),
            "box_code": box_codes[i] if i < len(box_codes) else "",
            "warehouse_code": fc,
            "items": items,
        } for i in range(n_boxes)]

        doc = {"ticket": {**ticket, "label": f"{fba}_{fc}"}, "boxes": boxes}
        path = out_dir / f"{fba}_{fc}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        units = sum(i["qty"] for i in items) * n_boxes
        print(f"  {path}  {n_boxes} box, {units} units")

    print(f"\n{len(plan['shipments'])} shipment file(s) in {out_dir}")


if __name__ == "__main__":
    main()
