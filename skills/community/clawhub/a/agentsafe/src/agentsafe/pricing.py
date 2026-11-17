"""Tiered audit pricing (advertised at request time, per TERMS_OF_SERVICE.md).

Prices are USD strings (x402 format) picked from the contract's verified
source size BEFORE payment verification, so the advertised payment
requirement always matches the real audit cost. The line count is derived
server-side from Etherscan's verified source; the client can never
influence the quoted tier.

Table (AgentLISA pricing):
    up to   100 source lines -> $0.50
    101 -   500 source lines -> $2.50
    501 - 1,000 source lines -> $5.00
    1,001 - 5,000 source lines -> $25.00
    over 5,000 -> custom pricing (request refused, contact link returned)
"""

from __future__ import annotations

from typing import Final

from agentsafe.explorer import SourceBundle

CUSTOM_PRICING_CONTACT_URL: Final[str] = "https://tally.so/r/laby7B"

# (max_source_lines_inclusive, price) - ascending order
AUDIT_PRICING_TIERS: Final[tuple[tuple[int, str], ...]] = (
    (100, "$0.50"),
    (500, "$2.50"),
    (1000, "$5.00"),
    (5000, "$25.00"),
)

MAX_AUDIT_SOURCE_LINES: Final[int] = AUDIT_PRICING_TIERS[-1][0]


class PricingError(ValueError):
    """Raised when no tiered price can be quoted for a contract."""


class ContractTooLargeError(PricingError):
    """Source exceeds the largest advertised tier; custom pricing required."""


def count_source_lines(bundle: SourceBundle) -> int:
    """Non-blank source lines across all verified files (the audited code)."""
    total = 0
    for f in bundle.files:
        if not f.path.endswith(".sol"):
            continue
        total += sum(1 for line in f.content.splitlines() if line.strip())
    return total


def audit_price_for_lines(lines: int) -> str:
    """Price string for the tier covering `lines`.

    Raises ContractTooLargeError above the largest tier.
    """
    if lines < 0:
        raise PricingError(f"invalid source line count: {lines}")
    for max_lines, price in AUDIT_PRICING_TIERS:
        if lines <= max_lines:
            return price
    raise ContractTooLargeError(
        f"contract has {lines} source lines, exceeding the largest advertised "
        f"tier ({MAX_AUDIT_SOURCE_LINES}); custom pricing required"
    )


def pricing_summary() -> list[dict[str, object]]:
    """Machine-readable tier table for the health tool / discovery."""
    tiers: list[dict[str, object]] = [
        {"up_to_lines": max_lines, "price": price} for max_lines, price in AUDIT_PRICING_TIERS
    ]
    tiers.append(
        {
            "over_lines": MAX_AUDIT_SOURCE_LINES,
            "price": "custom",
            "contact": CUSTOM_PRICING_CONTACT_URL,
        }
    )
    return tiers
