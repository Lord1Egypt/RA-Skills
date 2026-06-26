"""
User preferences for eBay search scoring and filtering.

Returns default preferences. Future versions may support persistent
preferences via environment variables or skill configuration.
"""

from dataclasses import dataclass


@dataclass
class UserPreferences:
    min_condition: str = "good"  # acceptable minimum: new, like_new, very_good, good, acceptable
    min_seller_score: float = 95.0  # percent positive feedback
    max_shipping_days: int = 7
    require_free_returns: bool = False
    budget_default: float = 500.0
    price_vs_speed: str = "balanced"  # price, speed, balanced


def load_preferences() -> UserPreferences:
    """Return default preferences."""
    return UserPreferences()
