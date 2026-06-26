"""
eBay item valuation using Browse API and Marketplace Insights API.

Provides get_valuation() to estimate item market value based on
current/recent eBay listings, with condition-based price adjustment,
outlier trimming, fair range, and confidence scoring.
"""

import os
import statistics
from typing import Optional

import httpx


# Condition adjustment factors for valuation
# Maps user-facing condition keys to multipliers applied to avg price
CONDITION_ADJUSTMENTS: dict[str, float] = {
    "new": 1.0,
    "like_new": 0.95,
    "very_good": 0.85,
    "good": 0.75,
    "acceptable": 0.6,
    "used": 0.8,
    "for_parts": 0.3,
}

SANDBOX_INSIGHTS_URL = "https://api.sandbox.ebay.com/buy/marketplace_insights/v1/item_sales/search"
PRODUCTION_INSIGHTS_URL = "https://api.ebay.com/buy/marketplace_insights/v1/item_sales/search"


def _get_insights_url() -> str:
    env = os.getenv("EBAY_ENVIRONMENT", "production").lower()
    return SANDBOX_INSIGHTS_URL if env == "sandbox" else PRODUCTION_INSIGHTS_URL


def _try_marketplace_insights(
    query: str, limit: int, access_token: str
) -> tuple[list[float], str]:
    """
    Try Marketplace Insights API for sold item prices.

    Returns (list of prices, source_label). Falls back to empty list
    on 403/404 or any error.
    """
    url = _get_insights_url()
    try:
        response = httpx.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
            },
            params={"q": query, "limit": limit, "sort": "price"},
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("itemSales", [])
        prices = []
        for item in items:
            price_val = item.get("lastSoldPrice", {}).get("value")
            if price_val:
                prices.append(float(price_val))
        if prices:
            return prices, "marketplace_insights"
    except (httpx.HTTPStatusError, httpx.RequestError):
        pass
    return [], ""


def _browse_api_prices(
    query: str, limit: int, access_token: str
) -> list[float]:
    """Get current listing prices from Browse API search."""
    from .search import search_items

    items = search_items(
        query, limit=limit, access_token=access_token
    )
    return [item["price"] for item in items if item.get("price")]


def _browse_api_items(
    query: str, limit: int, access_token: str
) -> list[dict]:
    """Get current listing items (full dicts) from Browse API search."""
    from .search import search_items
    return search_items(query, limit=limit, access_token=access_token)


def _trim_outliers(prices: list[float]) -> list[float]:
    """
    Remove outliers using IQR-based filtering.

    With fewer than 5 prices, returns all prices unchanged.
    """
    if len(prices) < 5:
        return prices
    sorted_p = sorted(prices)
    q1 = sorted_p[len(sorted_p) // 4]
    q3 = sorted_p[3 * len(sorted_p) // 4]
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    trimmed = [p for p in sorted_p if lower <= p <= upper]
    return trimmed if trimmed else sorted_p


def compute_fair_range(prices: list[float]) -> dict:
    """
    Compute fair value range from a list of prices.

    Returns dict with: fair_low, fair_high, median, trimmed_mean,
    trimmed_count, raw_count.
    """
    raw_count = len(prices)
    if not prices:
        return {
            "fair_low": 0, "fair_high": 0, "median": 0,
            "trimmed_mean": 0, "trimmed_count": 0, "raw_count": 0,
        }

    trimmed = _trim_outliers(prices)
    med = statistics.median(trimmed)
    tmean = statistics.mean(trimmed)

    if len(trimmed) >= 4:
        q1 = trimmed[len(trimmed) // 4]
        q3 = trimmed[3 * len(trimmed) // 4]
        fair_low = round(q1, 2)
        fair_high = round(q3, 2)
    else:
        fair_low = round(min(trimmed), 2)
        fair_high = round(max(trimmed), 2)

    return {
        "fair_low": fair_low,
        "fair_high": fair_high,
        "median": round(med, 2),
        "trimmed_mean": round(tmean, 2),
        "trimmed_count": len(trimmed),
        "raw_count": raw_count,
    }


def compute_confidence(
    trimmed_count: int,
    raw_count: int,
    fair_low: float,
    fair_high: float,
    median: float,
) -> str:
    """
    Return confidence level: 'high', 'medium', or 'low'.

    Based on comp count, how many survived trimming, and price spread.
    """
    if trimmed_count < 3:
        return "low"

    spread = (fair_high - fair_low) / median if median > 0 else 1.0
    survival_rate = trimmed_count / raw_count if raw_count > 0 else 0

    score = 0
    if trimmed_count >= 8:
        score += 2
    elif trimmed_count >= 5:
        score += 1

    if spread < 0.25:
        score += 2
    elif spread < 0.50:
        score += 1

    if survival_rate > 0.7:
        score += 1

    if score >= 4:
        return "high"
    elif score >= 2:
        return "medium"
    return "low"


def get_valuation(
    item_name: str,
    condition: str = "used",
    token: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """
    Estimate market value for an item based on eBay data.

    Tries Marketplace Insights API first (sold data), falls back to
    Browse API (current listings). Computes price statistics with
    outlier trimming, fair range, and confidence.

    Args:
        item_name: Search query for the item.
        condition: Item condition key (new, like_new, very_good, good,
                   acceptable, used, for_parts).
        token: Bearer access token. If None, fetches one automatically.
        limit: Max number of listings to analyze.

    Returns:
        Dict with keys: avg, median, min, max, count, adjusted_avg,
        condition, source, recommended_price, fair_low, fair_high,
        confidence, trimmed_count.

    Raises:
        EnvironmentError: If credentials are missing and no token provided.
    """
    if token is None:
        from .auth import get_app_access_token
        token = get_app_access_token()

    # Try Marketplace Insights first
    prices, source = _try_marketplace_insights(item_name, limit, token)

    # Fall back to Browse API with relevance filtering
    items_for_filtering = []
    if not prices:
        items_for_filtering = _browse_api_items(item_name, limit, token)
        from .relevance import filter_relevant
        filtered = filter_relevant(items_for_filtering, item_name)
        prices = [item["total_price"] for item in filtered if item.get("total_price")]
        source = "browse_api"

    if not prices:
        return {
            "avg": 0, "median": 0, "min": 0, "max": 0,
            "count": 0, "adjusted_avg": 0, "condition": condition,
            "source": source, "recommended_price": 0,
            "fair_low": 0, "fair_high": 0, "confidence": "low",
            "trimmed_count": 0,
        }

    # Compute stats
    avg = statistics.mean(prices)
    median = statistics.median(prices)
    price_min = min(prices)
    price_max = max(prices)

    adjustment = CONDITION_ADJUSTMENTS.get(condition.lower(), 0.8)
    adjusted_avg = avg * adjustment
    recommended = adjusted_avg * 0.95  # 5% below adjusted avg

    # Fair range with outlier trimming
    fr = compute_fair_range(prices)
    confidence = compute_confidence(
        fr["trimmed_count"], fr["raw_count"],
        fr["fair_low"], fr["fair_high"], fr["median"],
    )

    return {
        "avg": round(avg, 2),
        "median": round(median, 2),
        "min": round(price_min, 2),
        "max": round(price_max, 2),
        "count": len(prices),
        "adjusted_avg": round(adjusted_avg, 2),
        "condition": condition,
        "source": source,
        "recommended_price": round(recommended, 2),
        "fair_low": fr["fair_low"],
        "fair_high": fr["fair_high"],
        "confidence": confidence,
        "trimmed_count": fr["trimmed_count"],
    }
