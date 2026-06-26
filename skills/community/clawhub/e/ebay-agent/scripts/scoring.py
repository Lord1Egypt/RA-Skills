"""
Trade-off scoring for eBay search results.

Ranks listings by a weighted combination of price savings, seller trust,
shipping speed, and item condition relative to user preferences.
"""

from .preferences import UserPreferences

# Maps condition strings (from eBay API) to a 0-1 quality scale
CONDITION_SCORES: dict[str, float] = {
    "New": 1.0,
    "New with box": 1.0,
    "New without box": 0.95,
    "New other (see details)": 0.9,
    "New without tags": 0.9,
    "Open box": 0.85,
    "Certified - Refurbished": 0.85,
    "Excellent - Refurbished": 0.8,
    "Seller refurbished": 0.75,
    "Very Good": 0.7,
    "Like New": 0.7,
    "Used": 0.6,
    "Pre-owned": 0.6,
    "Good": 0.55,
    "Acceptable": 0.35,
    "For parts or not working": 0.0,
}

# Maps condition filter keys to minimum acceptable condition scores
CONDITION_FLOOR: dict[str, float] = {
    "new": 0.9,
    "like_new": 0.85,
    "very_good": 0.7,
    "good": 0.55,
    "acceptable": 0.35,
}


def _get_weights(price_vs_speed: str) -> dict[str, float]:
    if price_vs_speed == "price":
        return {"price": 0.55, "trust": 0.25, "speed": 0.05, "condition": 0.15}
    elif price_vs_speed == "speed":
        return {"price": 0.20, "trust": 0.25, "speed": 0.40, "condition": 0.15}
    return {"price": 0.40, "trust": 0.30, "speed": 0.20, "condition": 0.10}


def score_listing(item: dict, prefs: UserPreferences) -> float:
    """
    Score a single listing from 0-1 based on user preferences.

    Args:
        item: Parsed item dict from search.py (must have total_price, condition,
              seller_feedback_pct, and optionally shipping_days).
        prefs: User preference settings.

    Returns:
        Float score between 0.0 and 1.0, higher is better.
    """
    budget = prefs.budget_default
    total = item.get("total_price", 0)
    price_score = max(0, (budget - total) / budget) if budget > 0 else 0

    feedback = item.get("seller_feedback_pct")
    trust_score = float(feedback) / 100 if feedback else 0.5

    shipping_days = item.get("shipping_days", 5)
    speed_score = max(0, 1 - (shipping_days / 14))

    condition_str = item.get("condition", "")
    condition_score = CONDITION_SCORES.get(condition_str, 0.4)

    weights = _get_weights(prefs.price_vs_speed)

    return (
        price_score * weights["price"]
        + trust_score * weights["trust"]
        + speed_score * weights["speed"]
        + condition_score * weights["condition"]
    )


def rank_results(items: list[dict], prefs: UserPreferences) -> list[dict]:
    """
    Score and sort search results by preference-weighted score.

    Also filters out items below the user's minimum condition threshold
    and minimum seller score. Adds a 'score' key to each item dict.

    Returns:
        Sorted list (best first), each item enriched with 'score' field.
    """
    min_condition = CONDITION_FLOOR.get(prefs.min_condition, 0.0)
    scored = []
    for item in items:
        condition_val = CONDITION_SCORES.get(item.get("condition", ""), 0.4)
        if condition_val < min_condition:
            continue

        feedback = item.get("seller_feedback_pct")
        if feedback and float(feedback) > 0 and float(feedback) < prefs.min_seller_score:
            continue

        item["score"] = round(score_listing(item, prefs), 3)
        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
