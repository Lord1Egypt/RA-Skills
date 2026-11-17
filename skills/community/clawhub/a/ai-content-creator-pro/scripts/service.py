#!/usr/bin/env python3
"""ai-content-creator-pro - Service execution script (Phase 3)

Buyout model: pay 楼9.90 once. On first payment, writes a buyout
credential locally. Subsequent calls skip payment and go straight
to content creation.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import sys
import time

SLUG = "ai-content-creator-pro"
CREDENTIAL_TTL = 86400

_BUYOUT_DIR = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "credentials", SLUG)
_BUYOUT_FILE = os.path.join(_BUYOUT_DIR, "buyout.json")

_INDICATOR_RE = re.compile(r"^[a-fA-F0-9]{32}$")
_ORDER_NO_RE = re.compile(r"^[0-9]{14,32}$")

def _validate_indicator(indicator):
    if not _INDICATOR_RE.fullmatch(indicator):
        raise ValueError("Invalid indicator format")
def _validate_order_no(order_no):
    if not _ORDER_NO_RE.fullmatch(order_no):
        raise ValueError("Invalid order_no format")
def _get_orders_dir(indicator):
    _validate_indicator(indicator)
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home, "openclaw", "skills", "orders", indicator)
    else:
        return os.path.join(home, ".openclaw", "skills", "orders", indicator)
def _load_order(indicator, order_no):
    _validate_order_no(order_no)
    path = os.path.join(_get_orders_dir(indicator), f"{order_no}.json")
    if not os.path.isfile(path):
        raise RuntimeError(f"Order file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()

def has_buyout() -> bool:
    """Check if user has already bought out this skill."""
    return os.path.isfile(_BUYOUT_FILE)

def write_buyout(order_no: str, credential: str):\n    """Record buyout credential after first successful payment."""\n    print(f"[BUYOUT] Writing credential to {_BUYOUT_FILE}")\n    os.makedirs(_BUYOUT_DIR, exist_ok=True)
    data = {"slug": SLUG, "order_no": order_no, "credential": credential, "timestamp": int(time.time())}
    with open(_BUYOUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_credential_valid(order_data: dict) -> bool:
    credential = order_data.get("payCredential")
    if not credential:
        return False
    credential_ts = order_data.get("credentialTimestamp")
    if credential_ts and time.time() - credential_ts > CREDENTIAL_TTL:
        return False
    return True


if __name__ == "__main__":
    # Check buyout first
    if has_buyout():
        print("=" * 60)
        print("  ai-content-creator-pro - Buyout Active")
        print("=" * 60)
        print("Buyout credential found. Skipping payment.\n")
        print("The AI model will now deliver multi-platform content creation.")
        print("=" * 60)
        print("PAY_STATUS: SUCCESS")
        print("BUYOUT: true")
        sys.exit(0)

    # First-time use: need payment
    parser = argparse.ArgumentParser(description="Verify buyout payment for ai-content-creator-pro")
    parser.add_argument("order_no", help="Order number from Phase 1")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_data = _load_order(indicator, args.order_no)
    except Exception as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: Order file read failed: {e}")
        sys.exit(1)

    if not is_credential_valid(order_data):
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: No valid payment credential found. Complete payment via clawtip first.")
        sys.exit(1)

    pay_status = order_data.get("payStatus", "SUCCESS")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status != "SUCCESS":
        print(f"ERROR_INFO: Payment status is '{pay_status}', cannot proceed")
        sys.exit(1)

    # First payment successful - write buyout credential
    credential = order_data.get("payCredential", "")
    write_buyout(args.order_no, credential)
    print("BUYOUT: registered")
    print("=" * 60)
    print("  ai-content-creator-pro - Buyout Complete!")
    print("=" * 60)
    print("Thank you! You now have unlimited access.")
    print("Future uses will skip payment automatically.\n")
    print("The AI model will now deliver multi-platform content creation.")
    print("=" * 60)

