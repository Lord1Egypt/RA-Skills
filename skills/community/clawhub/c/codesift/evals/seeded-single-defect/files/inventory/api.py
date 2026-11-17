"""Handlers for product pages."""

import time

from inventory.store import load_product


def product_page(sku: str) -> dict:
    """Build the product page payload; called on every page view."""
    product = load_product(sku, time.time())
    return {"sku": sku, "name": product["name"], "price_cents": product["price_cents"]}
