#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from file_utils import load_order
from runtime_config import resolve_base_url


SLUG = "deepknow-currency"
INDICATOR = hashlib.md5(SLUG.encode("utf-8")).hexdigest()
SUPPORTED_PAY_STATUSES = {"SUCCESS", "PROCESSING", "FAIL", "ERROR"}


def request_json(url: str, payload: dict) -> dict:
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {exc.code}: {body or exc.reason}") from exc


def main() -> int:
    if len(sys.argv) < 2:
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: missing order_no")
        return 1

    order_no = sys.argv[1]
    try:
        order = load_order(INDICATOR, order_no)
        credential = order.get("payCredential") or order.get("credential")
        if not credential:
            raise RuntimeError("payment credential not found in order file")

        payload = request_json(
            f"{resolve_base_url()}/api/skill/fulfill",
            {
                "order_no": order_no,
                "credential": credential,
                "question": order.get("question", ""),
            },
        )
        raw_pay_status = payload.get("PAY_STATUS")
        if raw_pay_status is None:
            print("PAY_STATUS: ERROR")
            print("ERROR_INFO: missing PAY_STATUS")
            return 1

        pay_status = str(raw_pay_status).upper()
        if pay_status not in SUPPORTED_PAY_STATUSES:
            print("PAY_STATUS: ERROR")
            print(f"ERROR_INFO: unsupported PAY_STATUS: {pay_status}")
            return 1

        print(f"PAY_STATUS: {pay_status}")
        if pay_status == "ERROR":
            print(f"ERROR_INFO: {payload.get('ERROR_INFO', 'unknown error')}")
            return 1
        if payload.get("ERROR_INFO"):
            print(f"ERROR_INFO: {payload['ERROR_INFO']}")
        if payload.get("result") is not None:
            print(json.dumps(payload["result"], ensure_ascii=False))
        return 0
    except Exception as exc:
        print("PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
