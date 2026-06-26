import logging
import os
from typing import Dict

import requests


logger = logging.getLogger(__name__)


BILLING_API_URL = "https://skillpay.me"
BILLING_API_KEY = os.getenv("SKILLPAY_API_KEY")
SKILL_ID = "d81a694a-f0bd-4119-a07a-926927d75631"
DEV_MODE = os.getenv("SKILLPAY_DEV_MODE", "false").lower() in {"1", "true", "yes"}

REQUEST_TIMEOUT_SECONDS = 15
DEFAULT_PRICE_USD = 0.02


def _headers() -> Dict[str, str]:
    if not BILLING_API_KEY and not DEV_MODE:
        raise RuntimeError("SKILLPAY_API_KEY not configured")
    return {
        "X-API-Key": BILLING_API_KEY or "",
        "Content-Type": "application/json",
    }


def check_balance(user_id: str) -> Dict:
    if DEV_MODE:
        return {"ok": True, "balance": 999}

    url = f"{BILLING_API_URL}/api/v1/billing/balance"
    try:
        response = requests.get(
            url,
            params={"user_id": user_id},
            headers=_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        balance = data.get("balance", 0)
        return {"ok": True, "balance": balance, "raw": data}
    except requests.RequestException as exc:
        logger.exception("Balance request failed for user_id=%s", user_id)
        return {"ok": False, "error": "billing_api_error", "message": str(exc)}
    except ValueError as exc:
        logger.exception("Invalid balance response for user_id=%s", user_id)
        return {"ok": False, "error": "invalid_response", "message": str(exc)}


def charge_user(user_id: str, amount: float = DEFAULT_PRICE_USD) -> Dict:
    if DEV_MODE:
        return {"ok": True, "charged": amount}

    url = f"{BILLING_API_URL}/api/v1/billing/charge"
    payload = {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": amount,
        "currency": "USD",
    }
    try:
        response = requests.post(
            url,
            json=payload,
            headers=_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        data = response.json() if response.text else {}
        if response.status_code in (401, 402, 403):
            return {
                "ok": False,
                "error": "insufficient_balance",
                "balance": data.get("balance"),
                "raw": data,
            }
        response.raise_for_status()
        return {"ok": True, "data": data}
    except requests.RequestException as exc:
        logger.exception("Charge request failed for user_id=%s", user_id)
        return {"ok": False, "error": "billing_api_error", "message": str(exc)}
    except ValueError as exc:
        logger.exception("Invalid charge response for user_id=%s", user_id)
        return {"ok": False, "error": "invalid_response", "message": str(exc)}


def get_payment_link(user_id: str, amount: float = DEFAULT_PRICE_USD) -> Dict:
    if DEV_MODE:
        return {"ok": True, "payment_url": "https://skillpay.me/dev-checkout", "amount": amount}

    url = f"{BILLING_API_URL}/api/v1/billing/payment-link"
    payload = {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": amount,
        "currency": "USD",
    }
    try:
        response = requests.post(
            url,
            json=payload,
            headers=_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "ok": True,
            "payment_url": data.get("payment_url") or data.get("url"),
            "raw": data,
        }
    except requests.RequestException as exc:
        logger.exception("Payment-link request failed for user_id=%s", user_id)
        return {"ok": False, "error": "billing_api_error", "message": str(exc)}
    except ValueError as exc:
        logger.exception("Invalid payment-link response for user_id=%s", user_id)
        return {"ok": False, "error": "invalid_response", "message": str(exc)}
