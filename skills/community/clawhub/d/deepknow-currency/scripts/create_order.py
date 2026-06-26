#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from urllib.request import Request, urlopen

from file_utils import save_order
from runtime_config import resolve_base_url


SLUG = "deepknow-currency"
INDICATOR = hashlib.md5(SLUG.encode("utf-8")).hexdigest()


def request_json(url: str, payload: dict) -> dict:
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_question(raw_question: str) -> str:
    question = raw_question.strip()
    if not question:
        raise ValueError("missing question")
    try:
        return json.dumps(
            json.loads(question),
            ensure_ascii=False,
            separators=(",", ":"),
        )
    except json.JSONDecodeError:
        return question


def main() -> int:
    if len(sys.argv) < 2:
        print("订单创建失败: missing question")
        return 1

    try:
        question = normalize_question(sys.argv[1])
    except ValueError as exc:
        print(f"订单创建失败: {exc}")
        return 1

    try:
        body = request_json(f"{resolve_base_url()}/api/skill/create-order", {"question": question})
        order_no = body["order_no"]
        save_order(
            INDICATOR,
            order_no,
            {
                "skill-id": SLUG,
                "skill_id": SLUG,
                "order_no": order_no,
                "amount": body["amount_fen"],
                "question": question,
                "encrypted_data": body["encrypted_data"],
                "pay_to": body["pay_to"],
                "description": body["description"],
                "slug": SLUG,
                "resource_url": body["resource_url"],
            },
        )
    except Exception as exc:
        print(f"订单创建失败: {exc}")
        return 1

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={body['amount_fen']}")
    print(f"QUESTION={question}")
    print(f"INDICATOR={INDICATOR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
