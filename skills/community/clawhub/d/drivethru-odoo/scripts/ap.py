#!/usr/bin/env python3
"""Odoo Accounts Payable operations: purchase orders, vendor bills, vendors.

Usage:
    python3 scripts/ap.py <action>   # JSON args on stdin

Actions:
    search-pos       Search purchase orders.
                     Input (all optional): {"search": "...", "vendor": "...",
                     "state": "purchase", "limit": 20}
    get-po           Full PO detail. Input: {"po_id": 123}
    update-po-lines  Update line prices and/or freight/fees before billing.
                     Input: {"po_id": 123, "lines": [{"line_id": 1,
                     "price_unit": 9.5}], "freight_cost": 12.0, "fees_cost": 3.0}
    create-bill      Create a draft vendor bill from a PO. Honors ODOO_DRY_RUN.
                     Input: {"po_id": 123, "vendor_bill_number": "INV-1",
                     "invoice_date": "2026-06-01", "line_ids": [1,2],
                     "reviewer_user_id": 6, "review_note": "...",
                     "expected_total": 100.0, "tolerance": 0.05}
    get-bill         Full vendor-bill detail. Input: {"bill_id": 456}
    search-vendors   Search vendor partners.
                     Input (all optional): {"search": "...", "limit": 20}
"""

from __future__ import annotations

from typing import Any

from _cli import run
from odoo_client import OdooClient


def _require_int(args: dict[str, Any], key: str) -> int:
    if key not in args:
        raise ValueError(f"`{key}` is required.")
    return int(args[key])


def _search_pos(client: OdooClient, args: dict[str, Any]) -> Any:
    return {
        "purchase_orders": client.search_purchase_orders(
            search=args.get("search"),
            vendor=args.get("vendor"),
            state=args.get("state"),
            limit=int(args.get("limit", 20)),
        )
    }


def _get_po(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_purchase_order(_require_int(args, "po_id"))


def _update_po_lines(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.update_po_lines(
        _require_int(args, "po_id"),
        lines=args.get("lines"),
        freight_cost=args.get("freight_cost"),
        fees_cost=args.get("fees_cost"),
    )


def _create_bill(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.create_vendor_bill(
        po_id=_require_int(args, "po_id"),
        vendor_bill_number=args.get("vendor_bill_number", ""),
        invoice_date=args.get("invoice_date", ""),
        line_ids=args.get("line_ids"),
        reviewer_user_id=args.get("reviewer_user_id"),
        review_note=args.get("review_note", ""),
        expected_total=args.get("expected_total"),
        tolerance=float(args.get("tolerance", 0.05)),
    )


def _get_bill(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_vendor_bill(_require_int(args, "bill_id"))


def _search_vendors(client: OdooClient, args: dict[str, Any]) -> Any:
    return {
        "vendors": client.search_vendors(
            search=args.get("search"),
            limit=int(args.get("limit", 20)),
        )
    }


ACTIONS = {
    "search-pos": _search_pos,
    "get-po": _get_po,
    "update-po-lines": _update_po_lines,
    "create-bill": _create_bill,
    "get-bill": _get_bill,
    "search-vendors": _search_vendors,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage="ap.py <search-pos|get-po|update-po-lines|create-bill|get-bill|search-vendors>",
    )
