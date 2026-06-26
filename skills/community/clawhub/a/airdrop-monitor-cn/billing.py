import os
import requests
from typing import Dict, Any

BILLING_URL = "https://skillpay.me/api/v1/billing"
API_KEY = os.environ.get("SKILL_BILLING_API_KEY", "")
SKILL_ID = os.environ.get("SKILL_ID", "")
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


class BillingConfigError(RuntimeError):
    pass


def _ensure_config() -> None:
    if not API_KEY or not SKILL_ID:
        raise BillingConfigError("Missing SKILL_BILLING_API_KEY or SKILL_ID")


def charge_user(user_id: str, amount: float | None = None) -> Dict[str, Any]:
    """Charge 1 call before executing paid logic."""
    _ensure_config()
    payload = {"user_id": user_id, "skill_id": SKILL_ID}
    if amount is not None:
        payload["amount"] = amount
    resp = requests.post(
        f"{BILLING_URL}/charge",
        headers=HEADERS,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("success"):
        return {"ok": True, "balance": data.get("balance", 0)}
    return {
        "ok": False,
        "balance": data.get("balance", 0),
        "payment_url": data.get("payment_url"),
        "message": data.get("message", "insufficient balance"),
    }


def get_balance(user_id: str) -> float:
    _ensure_config()
    resp = requests.get(
        f"{BILLING_URL}/balance",
        params={"user_id": user_id},
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    return float(resp.json().get("balance", 0))


def get_payment_link(user_id: str, amount: float = 8) -> str:
    _ensure_config()
    resp = requests.post(
        f"{BILLING_URL}/payment-link",
        headers=HEADERS,
        json={"user_id": user_id, "amount": amount},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("payment_url") or data.get("full_url") or ""
