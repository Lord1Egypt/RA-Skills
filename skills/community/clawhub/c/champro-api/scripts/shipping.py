"""Shipping-method catalog and the billing-type rule that goes with it.

CHAMPRO's method list is not free text — an unrecognised `ShippingMethod` is a
rejected order — and a third of the list is *coupled to a billing type*. Any
method ending in `COLLECT` or `THIRD PARTY` bills someone other than the
CHAMPRO account, so it requires `ShippingCustomerAccount` (the payer's carrier
account). Omitting it is a rejection the API reports only after the round trip.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

_ASSET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "shipping_methods.json",
)


@lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    with open(_ASSET, encoding="utf-8") as handle:
        return json.load(handle)


def methods() -> list[dict[str, Any]]:
    return list(_catalog()["methods"])


def warehouses() -> list[dict[str, Any]]:
    return list(_catalog()["warehouses"])


WAREHOUSE_CODES = frozenset({"IL", "CA", "DR"})


def _normalise(name: str) -> str:
    return " ".join(str(name or "").upper().replace("_", " ").split())


@lru_cache(maxsize=1)
def _by_normalised() -> dict[str, dict[str, Any]]:
    return {_normalise(m["name"]): m for m in _catalog()["methods"]}


def lookup(name: str) -> dict[str, Any] | None:
    """Resolve a method name tolerantly.

    The published list mixes two spellings — `UPS GROUND` and `FEDEX_2_DAY` —
    so underscores and spaces are treated alike. The value actually sent is
    always the catalog's canonical spelling, never the caller's.
    """

    return _by_normalised().get(_normalise(name))


def requires_shipping_account(name: str) -> bool:
    entry = lookup(name)
    return bool(entry and entry.get("billing_type"))


def suggest(name: str, limit: int = 5) -> list[str]:
    """Nearest catalog names for a method that did not resolve."""

    import difflib  # noqa: PLC0415

    return difflib.get_close_matches(_normalise(name), list(_by_normalised()), n=limit, cutoff=0.5)
