import time

from .constants import EXPIRED_PLACEHOLDER, STALE_THRESHOLD_SECONDS


def mark_stale_market_data(data: dict, now: float | None = None) -> dict:
    now = now if now is not None else time.time()
    is_stale = (now - data.get("timestamp", 0)) > STALE_THRESHOLD_SECONDS
    return {**data, "is_stale": is_stale}


def expire_intelligence(data: dict, now: float | None = None) -> dict:
    now = now if now is not None else time.time()
    ttl = data.get("ttl_seconds", 1800)
    created_at = data.get("created_at", 0)
    if (now - created_at) > ttl:
        return {**data, "content": EXPIRED_PLACEHOLDER}
    return {**data}
