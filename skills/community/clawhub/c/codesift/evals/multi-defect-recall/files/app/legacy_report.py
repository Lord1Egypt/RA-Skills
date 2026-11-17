"""Revenue report for the retired CSV billing export."""

from app.pricing import total_with_tax


def legacy_revenue(rows: list[tuple[str, int]]) -> int:
    """Sum (order_id, subtotal_cents) rows with tax."""
    return sum(total_with_tax(subtotal) for _, subtotal in rows)
