#!/usr/bin/env python3
"""Phase 1：创建发明专利撰写订单，输出供 openclaw 解析的 ORDER_NO / AMOUNT / ENCRYPTED_DATA / PAY_TO。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE = os.environ.get("SKILL_SERVER_BASE_URL", "http://api.clawtip.top").rstrip("/")
CREATE_ORDER_URL = f"{DEFAULT_BASE}/api/clawtip/createOrder"


def create_order(question: str) -> tuple[str, int | str, str, str]:
    payload = json.dumps(
        {"question": question, "clientIp": ""},
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        CREATE_ORDER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常，请确认服务地址 {CREATE_ORDER_URL} 可达: {e}") from e

    if body.get("responseCode") != "200":
        raise RuntimeError(body.get("responseMessage") or "createOrder 失败")

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("响应缺少 orderNo")

    amount = body.get("amount")
    encrypted_data = body.get("encryptedData")
    pay_to = body.get("payTo")

    if encrypted_data is None or pay_to is None:
        raise RuntimeError("响应缺少 encryptedData 或 payTo")

    return str(order_no), amount, str(encrypted_data), str(pay_to)


def main() -> None:
    parser = argparse.ArgumentParser(description="创建发明专利撰写订单")
    parser.add_argument(
        "question",
        help="用户技术主题/发明要点简述（将写入订单，用于后续撰写对齐）",
    )
    args = parser.parse_args()

    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"ENCRYPTED_DATA={encrypted_data}")
    print(f"PAY_TO={pay_to}")


if __name__ == "__main__":
    main()
