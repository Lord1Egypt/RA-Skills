"""
Deal evaluation for eBay items.

Given a search query, fetches comparable listings, filters for relevance,
computes a fair value range, and returns a deal rating with explanation.
"""

from typing import Optional

from .relevance import filter_relevant
from .valuation import (
    CONDITION_ADJUSTMENTS,
    compute_confidence,
    compute_fair_range,
    _try_marketplace_insights,
    _browse_api_items,
)


# Rating thresholds relative to median comp price
RATING_THRESHOLDS = {
    "great_deal": 0.85,
    "good_deal": 0.93,
    "fair_high": 1.10,
}


def _rate_price(price: float, fair_low: float, fair_high: float, median: float) -> str:
    """Assign a deal rating based on price vs comp stats."""
    if median <= 0:
        return "unknown"
    ratio = price / median
    if ratio <= RATING_THRESHOLDS["great_deal"]:
        return "great deal"
    elif ratio <= RATING_THRESHOLDS["good_deal"]:
        return "good deal"
    elif ratio <= RATING_THRESHOLDS["fair_high"]:
        return "fair"
    else:
        return "overpriced"


def _build_explanation(
    rating: str,
    comp_count: int,
    trimmed_count: int,
    confidence: str,
    fair_low: float,
    fair_high: float,
    median: float,
    source: str,
) -> str:
    """Build a human-readable explanation of the deal evaluation."""
    parts = []
    parts.append(f"{trimmed_count} relevant comps analyzed")
    if trimmed_count < comp_count:
        parts.append(f"{comp_count - trimmed_count} outliers removed")

    spread = fair_high - fair_low
    if spread > 0 and median > 0:
        spread_pct = spread / median * 100
        if spread_pct < 15:
            parts.append("tight price clustering")
        elif spread_pct < 30:
            parts.append("modest price spread")
        else:
            parts.append("wide price spread")

    if source == "marketplace_insights":
        parts.append("based on sold data")
    else:
        parts.append("based on active listings")

    return "; ".join(parts) + "."


def evaluate_deal(
    query: str,
    condition: str = "used",
    token: Optional[str] = None,
    limit: int = 25,
    target_price: Optional[float] = None,
) -> dict:
    """
    Evaluate whether an item is a good deal.

    Fetches comps, filters for relevance, computes fair range, and
    rates the deal.

    Args:
        query: Search query (e.g. "Sony FE 85mm f/1.8").
        condition: Condition filter key.
        token: Bearer access token. If None, fetches automatically.
        limit: Max comps to fetch.
        target_price: Optional specific price to evaluate. If None,
                      returns fair range and buy recommendation without
                      rating a specific price.

    Returns:
        Dict with: fair_low, fair_high, median, confidence, rating,
        buy_below, explanation, comps_used, source, comp_listings.
    """
    if token is None:
        from .auth import get_app_access_token
        token = get_app_access_token()

    # Try sold data first
    prices, source = _try_marketplace_insights(query, limit, token)
    comp_listings = []

    if prices:
        # Marketplace insights — no item-level filtering available
        fr = compute_fair_range(prices)
    else:
        # Browse API with relevance filtering
        items = _browse_api_items(query, limit, token)
        filtered = filter_relevant(items, query)
        comp_listings = filtered[:10]  # top comps for display
        prices = [item["total_price"] for item in filtered if item.get("total_price")]
        source = "browse_api"
        fr = compute_fair_range(prices)

    if not prices:
        return {
            "fair_low": 0, "fair_high": 0, "median": 0,
            "confidence": "low", "rating": "unknown",
            "buy_below": 0,
            "explanation": "No relevant listings found.",
            "comps_used": 0, "source": source,
            "comp_listings": [],
        }

    confidence = compute_confidence(
        fr["trimmed_count"], fr["raw_count"],
        fr["fair_low"], fr["fair_high"], fr["median"],
    )

    # Apply condition adjustment to range
    adj = CONDITION_ADJUSTMENTS.get(condition.lower(), 0.8)
    adj_low = round(fr["fair_low"] * adj, 2)
    adj_high = round(fr["fair_high"] * adj, 2)
    adj_median = round(fr["median"] * adj, 2)

    # Buy recommendation: 93% of median (good deal threshold)
    buy_below = round(adj_median * RATING_THRESHOLDS["good_deal"], 2)

    # Rate a specific price if provided
    if target_price is not None:
        rating = _rate_price(target_price, adj_low, adj_high, adj_median)
    else:
        rating = "n/a"

    explanation = _build_explanation(
        rating, fr["raw_count"], fr["trimmed_count"],
        confidence, adj_low, adj_high, adj_median, source,
    )

    return {
        "fair_low": adj_low,
        "fair_high": adj_high,
        "median": adj_median,
        "confidence": confidence,
        "rating": rating,
        "buy_below": buy_below,
        "explanation": explanation,
        "comps_used": fr["trimmed_count"],
        "source": source,
        "comp_listings": [
            {
                "title": c.get("title", "")[:50],
                "price": c.get("total_price", 0),
                "condition": c.get("condition", ""),
                "url": c.get("item_url", ""),
            }
            for c in comp_listings[:5]
        ],
    }
