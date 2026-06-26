"""
server/currency.py — Currency formatting helpers for Friday Budgeting Pro.

Provides a unified format_amount() function that displays amounts with the
correct currency prefix (C$, US$, £, €, or ISO code prefix for others).

FX rate conversion (amount_home) and FX rate fetching are deferred to a
follow-up PR; this module covers only display formatting.
"""

from __future__ import annotations

# Map ISO 4217 codes to display symbols/prefixes.
_CURRENCY_SYMBOLS: dict[str, str] = {
    "CAD": "C$",
    "USD": "US$",
    "GBP": "£",
    "EUR": "€",
}


def format_amount(amount: float | None, currency: str = "CAD") -> str:
    """Format *amount* with a currency prefix.

    Examples
    --------
    >>> format_amount(1234.56, "CAD")
    'C$1,234.56'
    >>> format_amount(500, "USD")
    'US$500.00'
    >>> format_amount(1234.56, "EUR")
    '€1,234.56'
    >>> format_amount(None, "CAD")
    '—'
    """
    if amount is None:
        return "\u2014"  # em dash
    symbol = _CURRENCY_SYMBOLS.get(currency, f"{currency} ")
    return f"{symbol}{abs(amount):,.2f}"
