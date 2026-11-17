"""Order endpoints; responses follow docs/api.md."""

RETRY_AFTER_SECONDS = 30


def get_order(order_id: str, store: dict) -> dict:
    """Serialize one order for GET /orders/{id}."""
    order = store[order_id]
    return {"id": order_id, "total_cents": order["total_cents"]}


def sync_rejected() -> tuple[int, dict]:
    """Answer a rate-limited sync request with the documented retry delay."""
    return 429, {"retry_after": RETRY_AFTER_SECONDS}
