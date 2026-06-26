#!/usr/bin/env python3
"""Query Stripe products and return name, description, price, image, metadata.

Reads STRIPE_SECRET_KEY from the environment. Accepts a JSON filter object
on stdin (all fields optional); prints `{"products": [...], "has_more": bool,
"next_starting_after": str|null}` on success or `{"error": {...}}` on failure.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

try:
    import stripe
except ImportError:
    print(
        json.dumps(
            {
                "error": {
                    "type": "dependency_error",
                    "message": "The 'stripe' Python package is not installed. Install it with: pip install 'stripe>=10.0.0'",
                }
            }
        )
    )
    sys.exit(2)


def _fail(error_type: str, message: str, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}))
    sys.exit(1)


def _price_to_dict(price: Any) -> dict[str, Any]:
    return {
        "id": price.id,
        "unit_amount": price.unit_amount,
        "currency": price.currency,
        "recurring": (
            {
                "interval": price.recurring.interval,
                "interval_count": price.recurring.interval_count,
            }
            if getattr(price, "recurring", None)
            else None
        ),
        "nickname": getattr(price, "nickname", None),
        "active": price.active,
    }


def _product_to_dict(product: Any, prices: list[Any]) -> dict[str, Any]:
    images = list(getattr(product, "images", []) or [])
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "image": images[0] if images else None,
        "images": images,
        "metadata": dict(product.metadata or {}),
        "active": product.active,
        "default_price": (
            product.default_price
            if isinstance(product.default_price, str)
            else (product.default_price.id if product.default_price else None)
        ),
        "prices": [_price_to_dict(p) for p in prices],
    }


def _fetch_prices(product_id: str, include_inactive: bool) -> list[Any]:
    kwargs: dict[str, Any] = {"product": product_id, "limit": 100}
    if not include_inactive:
        kwargs["active"] = True
    return list(stripe.Price.list(**kwargs).auto_paging_iter())


def main() -> None:
    api_key = os.environ.get("STRIPE_SECRET_KEY")
    if not api_key:
        _fail("auth_error", "STRIPE_SECRET_KEY is not set. Export it before invoking the skill.")
    if not api_key.startswith(("sk_test_", "sk_live_", "rk_")):
        _fail(
            "auth_error",
            "STRIPE_SECRET_KEY does not look like a Stripe secret key "
            "(expected prefix sk_test_, sk_live_, or rk_).",
        )

    stripe.api_key = api_key
    api_version = os.environ.get("STRIPE_API_VERSION")
    if api_version:
        stripe.api_version = api_version

    raw = sys.stdin.read().strip()
    payload: dict[str, Any] = {}
    if raw:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            _fail("validation_error", f"Invalid JSON on stdin: {e}")
        if not isinstance(payload, dict):
            _fail("validation_error", "Input must be a JSON object.")

    query = payload.get("query")
    ids = payload.get("ids")
    active = payload.get("active", True)
    include_inactive_prices = bool(payload.get("include_inactive_prices", False))
    limit = int(payload.get("limit", 10))
    if limit < 1 or limit > 100:
        _fail("validation_error", "`limit` must be between 1 and 100.")
    starting_after = payload.get("starting_after")

    has_more = False
    next_starting_after: str | None = None
    products_raw: list[Any] = []

    try:
        if ids:
            if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
                _fail("validation_error", "`ids` must be a list of Stripe product IDs.")
            for pid in ids:
                products_raw.append(stripe.Product.retrieve(pid))

        elif query:
            if not isinstance(query, str):
                _fail("validation_error", "`query` must be a string.")
            # Stripe search syntax: https://stripe.com/docs/search
            # Treat a bare term as a name substring search; pass through if it
            # already contains a `:` (assume the caller wrote a real query).
            if ":" not in query:
                escaped = query.replace('"', '\\"')
                q = f'name:"{escaped}"'
                if active is not None:
                    q = f'{q} AND active:"{str(bool(active)).lower()}"'
            else:
                q = query
            result = stripe.Product.search(query=q, limit=limit)
            products_raw = list(result.data)
            has_more = bool(getattr(result, "has_more", False))
            next_starting_after = getattr(result, "next_page", None)

        else:
            kwargs: dict[str, Any] = {"limit": limit}
            if active is not None:
                kwargs["active"] = bool(active)
            if starting_after:
                kwargs["starting_after"] = starting_after
            result = stripe.Product.list(**kwargs)
            products_raw = list(result.data)
            has_more = bool(getattr(result, "has_more", False))
            if has_more and products_raw:
                next_starting_after = products_raw[-1].id

    except stripe.error.AuthenticationError as e:
        _fail("auth_error", str(e))
    except stripe.error.InvalidRequestError as e:
        _fail("invalid_request", str(e), param=getattr(e, "param", None))
    except stripe.error.StripeError as e:
        _fail("stripe_error", str(e))

    products_out = [
        _product_to_dict(p, _fetch_prices(p.id, include_inactive_prices))
        for p in products_raw
    ]

    print(
        json.dumps(
            {
                "products": products_out,
                "has_more": has_more,
                "next_starting_after": next_starting_after,
            }
        )
    )


if __name__ == "__main__":
    main()
