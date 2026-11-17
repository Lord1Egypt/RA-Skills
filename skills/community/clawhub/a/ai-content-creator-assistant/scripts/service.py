#!/usr/bin/env python3
"""ai-content-creator-assistant - Service execution script (Phase 3)

Reads payCredential from local order file. If valid, authorizes
the AI model to deliver multi-platform content creation in conversation.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import sys
import time

SLUG = "ai-content-creator-assistant"
CREDENTIAL_TTL = 86400

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


def is_credential_valid(order_data: dict) -> bool:
    credential = order_data.get("payCredential")
    if not credential:
        return False
    credential_ts = order_data.get("credentialTimestamp")
    if credential_ts and time.time() - credential_ts > CREDENTIAL_TTL:
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify payment and authorize content creation service"
    )
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

    print("AUTHORIZATION_RESULT=verified")
    print("\n" + "=" * 60)
    print("  Service Authorized - Content Creation")
    print("=" * 60)
    print("Payment verified. The AI model will now deliver:\n")
    print("  1. Multi-Platform Content Generation")
    print("     - 3-5 complete versions with different angles")
    print("     - Platform-adapted tone and formatting:\n")
    print("     Platform   | Output")
    print("     -----------|-------")
    print("     Xiaohongshu | Pain-point led, emoji rich, 500-800 chars")
    print("     Douyin/Kuaishou | Hook script format, under 500 chars")
    print("     WeChat/Zhihu | Deep structure, 1000-2000 chars")
    print("     Twitter/X  | Thread format, short concise posts\n")
    print("  2. Reference Material Analysis")
    print("     - Public content only (titles, descriptions)")
    print("     - No scraping of private data\n")
    print("  3. Batch Generation")
    print("     - Single topic, multiple platforms")
    print()
    print("  " + "=" * 56)
    print("  ��  Upgrade Tip: ai-content-creator-pro")
    print("  " + "=" * 56)
    print("  Pay once (¥9.90), use forever.")
    print("  Install: openclaw skills install @jinyu12166/ai-content-creator-pro")
    print("  " + "=" * 56)
    print("=" * 60)

    _jr = json.dumps({
        "pay_status": pay_status,
        "authorization": "***",
        "order_no": args.order_no,
        "service": SLUG,
    })
    print(f"JSON_RESULT={_jr}")
