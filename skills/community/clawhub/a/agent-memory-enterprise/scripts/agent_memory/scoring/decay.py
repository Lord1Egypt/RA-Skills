"""Time decay functions for memory scoring."""

from __future__ import annotations

import math
from datetime import datetime, timezone


def exponential_decay(
    hours_since: float,
    half_life_hours: float = 24.0,
) -> float:
    """Compute exponential time decay.

    Returns a value in [0, 1] where 1 means "just now" and 0 means "infinitely old".
    Uses formula: exp(-ln(2) * hours_since / half_life)
    """
    if hours_since < 0:
        return 1.0
    return math.exp(-math.log(2) * hours_since / half_life_hours)


def time_decay_score(
    timestamp: datetime,
    reference_time: datetime | None = None,
    half_life_hours: float = 24.0,
) -> float:
    """Compute a time-decay score for a given timestamp.

    Args:
        timestamp: The timestamp of the memory item.
        reference_time: The current time (defaults to now).
        half_life_hours: Hours for the score to drop to 0.5.

    Returns:
        Float in [0, 1].
    """
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)

    # Ensure both datetimes are timezone-aware
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)

    delta = reference_time - timestamp
    hours_since = delta.total_seconds() / 3600.0

    return exponential_decay(hours_since, half_life_hours)
