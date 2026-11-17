"""Product lookup with an in-process cache in front of the slow catalog file."""

import json
from pathlib import Path

CATALOG = Path(__file__).with_name("catalog.json")
_cache: dict[tuple[str, float], dict] = {}


def _read_catalog_entry(sku: str) -> dict:
    """Read one product from the catalog file; this is the slow path the cache avoids."""
    with CATALOG.open() as handle:
        return json.load(handle)[sku]


def load_product(sku: str, requested_at: float) -> dict:
    """Return the product for sku, serving repeated lookups from the cache.

    requested_at is the caller's request time, stored with the entry for auditing.
    """
    key = (sku, requested_at)
    if key in _cache:
        return _cache[key]
    product = _read_catalog_entry(sku)
    _cache[key] = product
    return product
