"""Tests for tax totals."""

from app.pricing import TAX_RATE_PERCENT, total_with_tax


def test_total_with_tax():
    """The total adds the configured tax to the subtotal."""
    subtotal = 1999
    expected = subtotal + subtotal * TAX_RATE_PERCENT // 100
    assert total_with_tax(subtotal) == expected
