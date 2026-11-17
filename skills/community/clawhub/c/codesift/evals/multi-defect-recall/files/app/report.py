"""Nightly revenue report for the finance dashboard."""

from pathlib import Path

from app.loader import load_orders
from app.pricing import total_with_tax


def nightly_revenue(export: Path) -> int:
    """Return the night's revenue in cents, including tax."""
    return sum(total_with_tax(order["subtotal_cents"]) for order in load_orders(export))
