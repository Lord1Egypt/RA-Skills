#!/usr/bin/env python3
"""CHAMPRO API toolkit — single CLI entrypoint.

Usage:
    python3 scripts/champro.py <action>    # JSON args on stdin

Every action reads a JSON object on stdin and prints one JSON object on stdout,
or `{"error": {...}}` with a non-zero exit code. Credentials come from the
environment (CHAMPRO_API_CUSTOMER_KEY, CHAMPRO_CB_CUSTOMER_KEY) or inline as
`api_customer_key` / `cb_customer_key`.

Actions:

  Setup
    check-access        Credentials + egress IP readiness. Orders nothing.
                        {}

  Catalog  (fills PromoStandards PPC's MOQ / lead-time gap)
    get-product-info    SKU grid, MOQ, MOQCustom, lead times for a master.
                        {"product_master": "JSBJ8"} | {"product_masters": [...]}
    find-skus           Filter a master's grid by size/configuration/fabric/color.
                        {"product_master": "JSBJ8", "size": "L", "fabric": "ACTIVE CLOTH"}
    get-lead-times      Lead-time names a CUSTOM order may use, with surcharges.
                        {"product_master": "JSBJ8"}

  Inventory  (CHAMPRO publishes NO PromoStandards INV service)
    check-inventory     Per-warehouse stock (IL/CA/DR) + restock date.
                        {"skus": ["BBS44ABS", "HJ2ABM"]}
    plan-warehouses     Assign each line a warehouse that can cover it.
                        {"lines": [{"sku": "...", "quantity": 3}], "prefer": ["IL","CA","DR"]}

  Orders  (CHAMPRO registers NO PromoStandards PO test endpoint)
    validate-order      Run every local rule. Sends nothing.
                        {"order": {...}, "product_masters": ["JSBJ8"]}
    preview-order       The exact JSON that would be POSTed + the report.
                        {"order": {...}}
    split-mixed-cart    Split a mixed cart into STOCK + CUSTOM orders (error 07).
                        {"items": [...], "base": {...}}
    place-order         Submit. EXTERNAL WRITE. Sandbox unless production:true;
                        sends nothing unless confirm:true.
                        {"order": {...}, "confirm": true, "production": false}

  Tracking  (CHAMPRO publishes NO ODRSTAT and NO OSN service)
    get-order-status    Status + tracking for SubOrderID(s) from place-order.
                        {"order_numbers": [1212121, 1212133]}
    track-order         Follow every suborder of a place-order result.
                        {"place_order_result": {...}}

  Custom Builder  (no PromoStandards equivalent exists)
    cb-categories       Embeddable categories and downloadable file types.
                        {}
    cb-embed-url        iframe src for a category, with the embed key.
                        {"category": "FOOTBALL"}
    cb-get-design       Roster/config for a saved Design Session ID.
                        {"session_id": "..."}
    cb-get-file         Download ProofPdf / Front / Back / Left / RightImage.
                        {"session_id": "...", "file_type": "ProofPdf"}
    cb-place-order      Order a saved design. EXTERNAL WRITE, same gates.
                        {"session_id": "...", "ship_to": {...}, "confirm": true}

  Reference
    list-shipping-methods  Methods + which need a ShippingCustomerAccount.
                        {}
    explain-error       What a CHAMPRO error code means and what to do.
                        {"code": "25"} | {"message": "E2.8.3: X - Not enough Inventory."}
"""

from __future__ import annotations

import os
import sys

# Sibling modules import by bare name regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import run  # noqa: E402
from catalog import find_skus, get_lead_times, get_product_info  # noqa: E402
from custom_builder import (  # noqa: E402
    embed_url,
    get_design,
    get_design_file,
    list_categories,
    place_design_order,
)
from diagnostics import check_access  # noqa: E402
from inventory import check_inventory, plan_warehouses  # noqa: E402
from order_status import get_order_status, track_placed_order  # noqa: E402
from orders import place_order, preview_order, split_by_type, validate_orders  # noqa: E402
from reference import explain_error, list_shipping_methods  # noqa: E402

ACTIONS = {
    # setup
    "check-access": check_access,
    # catalog
    "get-product-info": get_product_info,
    "find-skus": find_skus,
    "get-lead-times": get_lead_times,
    # inventory
    "check-inventory": check_inventory,
    "plan-warehouses": plan_warehouses,
    # orders
    "validate-order": validate_orders,
    "preview-order": preview_order,
    "split-mixed-cart": split_by_type,
    "place-order": place_order,
    # tracking
    "get-order-status": get_order_status,
    "track-order": track_placed_order,
    # custom builder
    "cb-categories": list_categories,
    "cb-embed-url": embed_url,
    "cb-get-design": get_design,
    "cb-get-file": get_design_file,
    "cb-place-order": place_design_order,
    # reference
    "list-shipping-methods": list_shipping_methods,
    "explain-error": explain_error,
}

if __name__ == "__main__":
    run(ACTIONS, usage=__doc__ or "")
