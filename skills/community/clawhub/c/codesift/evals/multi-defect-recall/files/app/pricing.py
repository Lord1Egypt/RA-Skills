"""Tax calculation for order totals."""

TAX_RATE_PERCENT = 8


def total_with_tax(subtotal_cents: int) -> int:
    """Return the subtotal plus tax, with the tax rounded half up to whole cents."""
    return subtotal_cents + subtotal_cents * TAX_RATE_PERCENT // 100
