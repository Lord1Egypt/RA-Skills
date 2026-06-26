#!/usr/bin/env python3
"""Odoo sales operations: eBay products, inventory, sale orders, tracking.

Usage:
    python3 scripts/sales.py <action>   # JSON args on stdin (where noted)

Actions:
    list-products     List products in the Odoo 'eBay' category. No input.
    inventory         Stock levels for SKUs. Input: {"skus": ["A-1", ...]}
    create-order      Push an eBay order to Odoo. Input: the order object
                      (see mock-order for the shape). Honors ODOO_DRY_RUN.
    tracking          Tracking for a shipped order. Input: {"odoo_order_id": 123}
    mock-order        Generate a realistic test order (does NOT call Odoo).
                      Input (all optional): {"sku": "...", "buyer_index": 0,
                      "num_line_items": 2}. Pipe its output into create-order.
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone
from typing import Any

from _cli import run
from odoo_client import OdooClient


# ── Live actions ────────────────────────────────────────────────────────────


def _list_products(client: OdooClient, _args: dict[str, Any]) -> Any:
    return {"products": client.fetch_ebay_products()}


def _inventory(client: OdooClient, args: dict[str, Any]) -> Any:
    skus = args.get("skus") or []
    if not isinstance(skus, list):
        raise ValueError("`skus` must be a list of SKU strings.")
    return {"levels": client.get_inventory_levels([str(s) for s in skus])}


def _create_order(client: OdooClient, args: dict[str, Any]) -> Any:
    if not args:
        raise ValueError("create-order requires an order object on stdin.")
    return client.create_sale_order(args)


def _tracking(client: OdooClient, args: dict[str, Any]) -> Any:
    order_id = args.get("odoo_order_id")
    if order_id is None:
        raise ValueError("`odoo_order_id` is required.")
    info = client.get_tracking_info(order_id)
    return {"shipped": info is not None, "tracking": info}


# ── Mock order generator (ported from app/odoo/mock_orders.py) ──────────────

_SAMPLE_BUYERS = [
    ("mike_collector_42", "John Doe", "mike.test@example.com"),
    ("vintage_hunter_99", "Sarah Smith", "sarah.test@example.com"),
    ("deals_finder_7", "Mark Johnson", "mark.test@example.com"),
    ("gadget_guru_21", "Lisa Brown", "lisa.test@example.com"),
]

_SAMPLE_SHIPPING_ADDRESSES = [
    {
        "name": "John Doe",
        "address_line_1": "123 Main Street",
        "address_line_2": "Apt 4",
        "city": "Austin",
        "state": "TX",
        "postal_code": "78701",
        "country": "US",
        "phone": "512-555-0101",
        "email": "john.doe.test@example.com",
    },
    {
        "name": "Sarah Smith",
        "address_line_1": "456 Oak Avenue",
        "address_line_2": "",
        "city": "Portland",
        "state": "OR",
        "postal_code": "97201",
        "country": "US",
        "phone": "503-555-0202",
        "email": "sarah.smith.test@example.com",
    },
    {
        "name": "Mark Johnson",
        "address_line_1": "789 Pine Road",
        "address_line_2": "Suite 100",
        "city": "Nashville",
        "state": "TN",
        "postal_code": "37203",
        "country": "US",
        "phone": "615-555-0303",
        "email": "mark.j.test@example.com",
    },
    {
        "name": "Lisa Brown",
        "address_line_1": "321 Cedar Lane",
        "address_line_2": "",
        "city": "Denver",
        "state": "CO",
        "postal_code": "80202",
        "country": "US",
        "phone": "303-555-0404",
        "email": "lisa.brown.test@example.com",
    },
]

_SAMPLE_PRODUCTS = [
    ("TEST-SKU-001", "Vintage Brass Desk Lamp", 49.99),
    ("TEST-SKU-002", "Leather Bound Notebook Set of 3", 24.99),
    ("TEST-SKU-003", "Handmade Ceramic Coffee Mug", 18.50),
    ("TEST-SKU-004", "Stainless Steel Water Bottle 32oz", 29.99),
    ("TEST-SKU-005", "Wooden Cutting Board Large", 42.00),
    ("TEST-SKU-006", "Canvas Backpack Olive Green", 65.00),
    ("TEST-SKU-007", "Bluetooth Speaker Portable", 39.99),
    ("TEST-SKU-008", "Wool Blanket Twin Size", 89.99),
]


def _mock_order(_client: OdooClient, args: dict[str, Any]) -> Any:
    sku = args.get("sku")
    buyer_index = args.get("buyer_index")
    num_line_items = args.get("num_line_items")

    if buyer_index is not None:
        idx = int(buyer_index) % len(_SAMPLE_BUYERS)
    else:
        idx = random.randint(0, len(_SAMPLE_BUYERS) - 1)
    username, full_name, email = _SAMPLE_BUYERS[idx]
    addr = dict(_SAMPLE_SHIPPING_ADDRESSES[idx % len(_SAMPLE_SHIPPING_ADDRESSES)])

    if sku:
        line_items = [
            {
                "line_item_id": f"line_{uuid.uuid4().hex[:8]}",
                "sku": sku,
                "title": f"Test product {sku}",
                "quantity": 1,
                "unit_price": 25.00,
                "line_total": 25.00,
                "tax": 2.06,
            }
        ]
    else:
        count = int(num_line_items) if num_line_items else random.randint(1, 3)
        products = random.sample(_SAMPLE_PRODUCTS, min(count, len(_SAMPLE_PRODUCTS)))
        line_items = []
        for i, (psku, ptitle, pprice) in enumerate(products):
            qty = random.randint(1, 2)
            line_total = round(pprice * qty, 2)
            tax = round(line_total * 0.0825, 2)  # 8.25% tax
            line_items.append(
                {
                    "line_item_id": f"line_{i + 1}_{uuid.uuid4().hex[:6]}",
                    "sku": psku,
                    "title": ptitle,
                    "quantity": qty,
                    "unit_price": pprice,
                    "line_total": line_total,
                    "tax": tax,
                }
            )

    subtotal = round(sum(li["line_total"] for li in line_items), 2)
    tax_total = round(sum(li["tax"] for li in line_items), 2)
    shipping = round(random.uniform(5.99, 14.99), 2)
    total = round(subtotal + tax_total + shipping, 2)

    now = datetime.now(timezone.utc)
    legacy_id = str(random.randint(100_000_000_000, 999_999_999_999))
    order_id = f"{random.randint(10, 99)}-{legacy_id[:5]}-{legacy_id[5:]}"

    addr["name"] = full_name
    addr["email"] = email

    return {
        "order_id": order_id,
        "legacy_order_id": legacy_id,
        "creation_date": now.isoformat(),
        "order_fulfillment_status": "NOT_STARTED",
        "order_payment_status": "PAID",
        "buyer_username": username,
        "buyer_email": email,
        "line_items": line_items,
        "subtotal": subtotal,
        "tax": tax_total,
        "shipping": shipping,
        "total": total,
        "currency": "USD",
        "shipping_address": addr,
        "billing_address": addr,
    }


ACTIONS = {
    "list-products": _list_products,
    "inventory": _inventory,
    "create-order": _create_order,
    "tracking": _tracking,
    "mock-order": _mock_order,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage="sales.py <list-products|inventory|create-order|tracking|mock-order>",
        offline_actions={"mock-order"},
    )
