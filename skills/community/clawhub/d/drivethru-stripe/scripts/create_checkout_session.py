#!/usr/bin/env python3
"""Create a Stripe Checkout Session from a JSON payload on stdin.

Reads STRIPE_SECRET_KEY from the environment. Prints a JSON object with the
hosted checkout `url`, session `id`, and `expires_at` on success, or
`{"error": {...}}` on failure (with a non-zero exit code).
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


ALLOWED_MODES = {"payment", "subscription", "setup"}


def _fail(error_type: str, message: str, **extra: Any) -> None:
    payload = {"error": {"type": error_type, "message": message, **extra}}
    print(json.dumps(payload))
    sys.exit(1)


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        _fail("validation_error", "Input must be a JSON object.")

    mode = payload.get("mode", "payment")
    if mode not in ALLOWED_MODES:
        _fail(
            "validation_error",
            f"`mode` must be one of {sorted(ALLOWED_MODES)}, got {mode!r}.",
        )

    line_items = payload.get("line_items")
    if mode != "setup":
        if not isinstance(line_items, list) or not line_items:
            _fail("validation_error", "`line_items` must be a non-empty array.")
        for i, item in enumerate(line_items):
            if not isinstance(item, dict):
                _fail("validation_error", f"line_items[{i}] must be an object.")
            if "price" not in item and "price_data" not in item:
                _fail(
                    "validation_error",
                    f"line_items[{i}] must include either `price` or `price_data`.",
                )
            if "quantity" not in item and mode != "subscription":
                item["quantity"] = 1

    success_url = payload.get("success_url") or os.environ.get(
        "STRIPE_DEFAULT_SUCCESS_URL"
    )
    cancel_url = payload.get("cancel_url") or os.environ.get(
        "STRIPE_DEFAULT_CANCEL_URL"
    )
    if not success_url:
        _fail(
            "validation_error",
            "`success_url` is required (or set STRIPE_DEFAULT_SUCCESS_URL).",
        )

    args: dict[str, Any] = {"mode": mode, "success_url": success_url}
    if cancel_url:
        args["cancel_url"] = cancel_url
    if line_items is not None:
        args["line_items"] = line_items

    for optional in (
        "customer",
        "customer_email",
        "client_reference_id",
        "metadata",
        "allow_promotion_codes",
        "automatic_tax",
        "shipping_address_collection",
        "billing_address_collection",
        "payment_method_types",
        "locale",
        "subscription_data",
        "payment_intent_data",
        "expires_at",
    ):
        if optional in payload:
            args[optional] = payload[optional]

    return args


def main() -> None:
    api_key = os.environ.get("STRIPE_SECRET_KEY")
    if not api_key:
        _fail(
            "auth_error",
            "STRIPE_SECRET_KEY is not set. Export it before invoking the skill.",
        )
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

    raw = sys.stdin.read()
    if not raw.strip():
        _fail("validation_error", "No JSON payload received on stdin.")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        _fail("validation_error", f"Invalid JSON on stdin: {e}")

    args = _validate(payload)

    try:
        session = stripe.checkout.Session.create(**args)
    except stripe.error.AuthenticationError as e:
        _fail("auth_error", str(e))
    except stripe.error.InvalidRequestError as e:
        _fail("invalid_request", str(e), param=getattr(e, "param", None))
    except stripe.error.StripeError as e:
        _fail("stripe_error", str(e))

    print(
        json.dumps(
            {
                "url": session.url,
                "id": session.id,
                "expires_at": session.expires_at,
                "mode": session.mode,
                "livemode": session.livemode,
            }
        )
    )


if __name__ == "__main__":
    main()
