#!/usr/bin/env python3
"""database-specialist - Service execution script (Phase 3)

Reads payCredential from local order file. If present and valid,
delivers the database specialist service authorization.
"""
import argparse
import hashlib
import json
import sys
import time

from file_utils import load_order

SLUG = "database-specialist"
CREDENTIAL_TTL = 86400  # 24 hours


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def is_credential_valid(order_data: dict) -> bool:
    credential = order_data.get("payCredential")
    if not credential:
        return False
    credential_ts = order_data.get("credentialTimestamp")
    if credential_ts:
        age = time.time() - credential_ts
        if age > CREDENTIAL_TTL:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify payment and authorize database-specialist service"
    )
    parser.add_argument("order_no", help="Order number from Phase 1")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_data = load_order(indicator, args.order_no)
    except Exception as e:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: \u8ba2\u5355\u6587\u4ef6\u8bfb\u53d6\u5931\u8d25: {e}")
        sys.exit(1)

    if not is_credential_valid(order_data):
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: \u672a\u627e\u5230\u6709\u6548\u7684\u652f\u4ed8\u51ed\u8bc1\u3002\u8bf7\u5148\u901a\u8fc7 clawtip \u5b8c\u6210\u652f\u4ed8\u3002")
        sys.exit(1)

    pay_status = order_data.get("payStatus", "SUCCESS")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status != "SUCCESS":
        print(f"ERROR_INFO: \u652f\u4ed8\u72b6\u6001\u4e3a {pay_status}\uff0c\u65e0\u6cd5\u7eed\u8fdb")
        sys.exit(1)

    print("AUTHORIZATION_RESULT=verified")
    _jr = json.dumps({
        "pay_status": pay_status,
        "authorization": "verified",
        "order_no": args.order_no,
    })
    print(f"JSON_RESULT={_jr}")
    print("\n" + "=" * 50)
    print("  database-specialist - Service Authorized")
    print("=" * 50)
    print("Payment verified. The AI model can now deliver")
    print("database architecture and SQL optimization services.")
