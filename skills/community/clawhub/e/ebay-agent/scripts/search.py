"""
eBay Browse API wrapper for item search.

Provides search_items() to query eBay's item_summary/search endpoint with
filtering by price, condition, and other criteria. Returns structured
result dicts suitable for scoring and display.
"""

import os
from typing import Optional
import httpx

SANDBOX_BASE_URL = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
PRODUCTION_BASE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

# Condition ID mapping (eBay codes)
CONDITION_IDS = {
    "new": "1000",
    "new_other": "1500",
    "certified_refurbished": "2000",
    "seller_refurbished": "2500",
    "used": "3000",
    "very_good": "4000",
    "good": "5000",
    "acceptable": "6000",
    "for_parts": "7000",
}


def _get_search_url() -> str:
    """
    Return the Browse API search endpoint based on EBAY_ENVIRONMENT.

    Returns:
        Search URL string (sandbox or production)
    """
    env = os.getenv("EBAY_ENVIRONMENT", "production").lower()
    return SANDBOX_BASE_URL if env == "sandbox" else PRODUCTION_BASE_URL


def _build_filter(max_price: Optional[float], condition: Optional[str]) -> Optional[str]:
    """
    Build the eBay filter query string for price and condition.

    Args:
        max_price: Maximum price in USD, or None for no price filter.
        condition: Condition key from CONDITION_IDS, or None for no condition filter.

    Returns:
        Filter string suitable for the eBay API ?filter= parameter, or None.
    """
    parts = []

    if max_price is not None:
        parts.append(f"price:[0..{max_price}],priceCurrency:USD")

    if condition is not None:
        condition_id = CONDITION_IDS.get(condition.lower())
        if condition_id:
            parts.append(f"conditionIds:{{{condition_id}}}")

    return ",".join(parts) if parts else None


def _parse_item(raw: dict) -> dict:
    """
    Extract relevant fields from a raw eBay item_summary response entry.

    Args:
        raw: Raw dict from the eBay API items array.

    Returns:
        Cleaned dict with normalized fields.
    """
    price_info = raw.get("price", {})
    shipping_options = raw.get("shippingOptions", [{}])
    shipping_cost = shipping_options[0].get("shippingCost", {}).get("value", "0.00") if shipping_options else "0.00"
    seller = raw.get("seller", {})

    return {
        "item_id": raw.get("itemId"),
        "title": raw.get("title"),
        "price": float(price_info.get("value", 0)),
        "currency": price_info.get("currency", "USD"),
        "shipping_cost": float(shipping_cost),
        "total_price": float(price_info.get("value", 0)) + float(shipping_cost),
        "condition": raw.get("condition"),
        "seller_feedback_pct": seller.get("feedbackPercentage"),
        "seller_feedback_score": seller.get("feedbackScore"),
        "item_url": raw.get("itemWebUrl"),
        "image_url": raw.get("image", {}).get("imageUrl"),
        "location": raw.get("itemLocation", {}).get("country"),
    }


def search_items(
    query: str,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    limit: int = 10,
    access_token: Optional[str] = None,
) -> list[dict]:
    """
    Search eBay listings via the Browse API item_summary/search endpoint.

    Args:
        query: Search query string (e.g. "Sony 85mm f/1.8 lens").
        max_price: Maximum total price filter in USD. Pass None for no limit.
        condition: Condition filter key. One of: new, new_other,
                   certified_refurbished, seller_refurbished, used,
                   very_good, good, acceptable, for_parts. Pass None for any.
        limit: Maximum number of results to return (default 10, max 200).
        access_token: Bearer token for auth. If None, will attempt to fetch
                      one via get_app_access_token() (requires credentials).

    Returns:
        List of item dicts with normalized fields (title, price, condition,
        seller info, URL). Empty list if no results or on API error.

    Raises:
        EnvironmentError: If credentials are missing and no token is provided.
        httpx.HTTPStatusError: If the API returns an error status.
    """
    if access_token is None:
        from .auth import get_app_access_token
        access_token = get_app_access_token()

    search_url = _get_search_url()
    params: dict = {
        "q": query,
        "limit": limit,
    }

    filter_str = _build_filter(max_price, condition)
    if filter_str:
        params["filter"] = filter_str

    response = httpx.get(
        search_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        },
        params=params,
    )
    response.raise_for_status()

    data = response.json()
    raw_items = data.get("itemSummaries", [])
    return [_parse_item(item) for item in raw_items]
