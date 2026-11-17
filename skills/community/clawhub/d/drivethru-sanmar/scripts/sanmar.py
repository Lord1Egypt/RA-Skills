#!/usr/bin/env python3
"""SanMar API toolkit — single CLI entrypoint for all sanmar tools.

Usage:
    python3 scripts/sanmar.py <action>   # JSON args on stdin

Each action maps to a deterministic SanMar tool. Arguments are a JSON object
on stdin whose keys match the tool's parameters; the result is a single JSON
object on stdout (or `{"error": {...}}` with a non-zero exit code on failure).

Credentials come from the `SANMAR_*` environment variables by default, or can
be passed inline in the stdin JSON (`customer_number`, `username`, `password`,
`environment`, and `ftp_password` for the SFTP-backed tools).

Actions (grouped by pillar):

  Products & pricing
    search-products         Catalog discovery for a style.
                            {"style": "PC55", "color"?, "size"?}
    get-pricing             myPrice + tier pricing for lines.
                            {"lines": [{"style","color","size"}, ...]}
    lookup-mainframe-color  Resolve a marketing color to its mainframe code (SFTP).
                            {"style", "color", "size"?, "force_refresh"?}

  Inventory
    check-inventory         Live warehouse inventory for one SKU (legacy port).
                            {"style", "color", "size", "auto_resolve_color"?}
    get-inventory-levels    Named per-warehouse availability (PromoStandards v2).
                            {"style", "part_ids"?}
    get-inventory-feed      Bulk inventory-by-warehouse from the FTP dip feed.
                            {"style"?, "path"?|"text"?|"remote_path"?}

  Purchase orders
    validate-cart           Pre-submit validation of a draft PO (no commit).
                            {"purchase_order": {...}}
    create-purchase-order   Submit a PO. EXTERNAL WRITE — needs "confirm": true,
                            otherwise returns a dry-run SOAP preview.
                            {"purchase_order": {...}, "confirm": false}
    parse-po-pdf            Extract a draft PO from a PDF (show user for approval).
                            {"pdf_path": "/path/to/po.pdf"}
    cancel-order            Reserved stub — SanMar exposes no cancel endpoint.
                            {"po_number": "...", "reason"?, "confirm"?}

  Tracking
    check-order-status      SanMar order number + shipment progress for a PO.
                            {"po_number": "..."}
    get-tracking            Package-level tracking (OSN): carrier, method, ship
                            date, items. Query by PO / sales order / ship date.
                            {"po_number" | "sales_order_number" | "shipment_date"}
    get-shipment-status     Parse the FTP Daily Shipment Status (ASN) file:
                            tracking + per-line costs. {"path"?|"text"?|"remote_path"?, "po_number"?}

  Invoicing
    get-invoices            Retrieve invoices (InvoicePort). Query by PO / invoice
                            number / order date / date range / unpaid. Each carries
                            a normalized "common" shape for payables.
                            {"po_number"|"invoice_number"|"order_date"|"start_date"+"end_date"|"unpaid"}
    parse-invoice-file      Parse an FTP Daily Invoice file (fixed-width or EDI-810)
                            into the same shape. {"path"?|"text"?|"remote_path"?, "edi"?}

  Returns
    process-return          Browser-driven portal return (Playwright). WRITE —
                            confirm:true gates the (not-yet-implemented) submit;
                            otherwise fills + returns a dry-run preview.
                            {"order_number" | "po_number", "lines": [...], "confirm"?}
"""

from __future__ import annotations

import os
import sys

# Ensure sibling modules import by bare name regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import run  # noqa: E402
from sanmar_tools import (  # noqa: E402
    sanmar_cancel_order,
    sanmar_check_inventory,
    sanmar_check_order_status,
    sanmar_create_purchase_order,
    sanmar_get_inventory_feed,
    sanmar_get_inventory_levels,
    sanmar_get_invoices,
    sanmar_get_pricing,
    sanmar_get_shipment_status,
    sanmar_get_tracking,
    sanmar_lookup_mainframe_color,
    sanmar_parse_invoice_file,
    sanmar_parse_po_pdf,
    sanmar_process_return,
    sanmar_search_products,
    sanmar_validate_cart,
)

ACTIONS = {
    "search-products": sanmar_search_products,
    "check-inventory": sanmar_check_inventory,
    "get-inventory-levels": sanmar_get_inventory_levels,
    "get-inventory-feed": sanmar_get_inventory_feed,
    "get-pricing": sanmar_get_pricing,
    "validate-cart": sanmar_validate_cart,
    "create-purchase-order": sanmar_create_purchase_order,
    "check-order-status": sanmar_check_order_status,
    "get-tracking": sanmar_get_tracking,
    "get-shipment-status": sanmar_get_shipment_status,
    "get-invoices": sanmar_get_invoices,
    "parse-invoice-file": sanmar_parse_invoice_file,
    "cancel-order": sanmar_cancel_order,
    "process-return": sanmar_process_return,
    "parse-po-pdf": sanmar_parse_po_pdf,
    "lookup-mainframe-color": sanmar_lookup_mainframe_color,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage="sanmar.py <" + "|".join(ACTIONS) + ">",
    )
