#!/usr/bin/env python3
"""database-specialist - Order Creation Script (Phase 1)

Creates a local order file and outputs ORDER_NO, AMOUNT, INDICATOR.
Uses CLAWTIP_PAY_TO and CLAWTIP_SM4_KEY from environment.
"""
import argparse
import hashlib
import json
import os
import random
import sys
import time

from file_utils import save_order
from sm4_utils import sm4_encrypt_hex, sm4_encrypt_base64

SLUG = "database-specialist"
AMOUNT = 390  # 3.9 yuan = 390 fen
DESCRIPTION = "Database architecture design, SQL optimization, schema review"
RESOURCE_URL = os.environ.get("CLAWTIP_RESOURCE_URL", f"https://clawhub.ai/skill/{SLUG}")
ENCODED_INFO_DATA = "database-specialist-order-info"


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def generate_order_no() -> str:
    ts = int(time.time() * 1000)
    rand = random.randint(100000, 999999)
    return f"{ts}{rand}"


def create_order_file(question: str, indicator: str) -> dict:
    pay_to = os.environ.get("CLAWTIP_PAY_TO", "")
    sm4_key = os.environ.get("CLAWTIP_SM4_KEY", "")

    if not pay_to:
        print("WARNING: CLAWTIP_PAY_TO environment variable not set")
    if not sm4_key:
        print("WARNING: CLAWTIP_SM4_KEY environment variable not set")

    order_no = generate_order_no()

    encrypt_payload = json.dumps({
        "orderNo": order_no,
        "amount": str(AMOUNT),
        "payTo": pay_to,
    }, ensure_ascii=False)

    encrypted_data = encrypt_payload
    if sm4_key:
        try:
            # Support both hex (32 chars) and base64 keys
            if len(sm4_key) == 32 and all(c in "0123456789abcdefABCDEF" for c in sm4_key):
                encrypted_data = sm4_encrypt_hex(sm4_key, encrypt_payload)
            else:
                encrypted_data = sm4_encrypt_base64(sm4_key, encrypt_payload)
        except Exception as e:
            print(f"WARNING: SM4 encryption failed: {e}")

    order_data = {
        "payTo": pay_to,
        "amount": AMOUNT,
        "order_no": order_no,
        "encrypted_data": encrypted_data,
        "slug": SLUG,
        "question": question,
        "description": DESCRIPTION,
        "resource_url": RESOURCE_URL,
        "encodedInfoData": ENCODED_INFO_DATA,
    }

    save_order(indicator, order_no, order_data)
    return order_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create database-specialist order"
    )
    parser.add_argument("question", help="User question / consultation content")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    print("=" * 60)
    print("NOTICE: This step creates a local order file for clawtip payment.")
    print("        No data is transmitted to external servers at this stage.")
    print("=" * 60)

    try:
        order_data = create_order_file(args.question, indicator)
    except Exception as e:
        print(f"\u8ba2\u5355\u521b\u5efa\u5931\u8d25: {e}")
        sys.exit(1)

    print(f"ORDER_NO={order_data['order_no']}")
    print(f"AMOUNT={order_data['amount']}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")

    summary = {
        "order_no": order_data["order_no"],
        "amount": order_data["amount"],
        "indicator": indicator,
        "slug": SLUG,
    }
    print(f"JSON_RESULT={json.dumps(summary, ensure_ascii=False)}")
