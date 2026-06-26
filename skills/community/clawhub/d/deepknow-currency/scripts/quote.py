#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from urllib.request import Request, urlopen

from runtime_config import SUPPORTED_QUOTE_CURRENCIES, resolve_base_url


def request_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) < 2:
        print("查询失败: missing quote_currency")
        return 1

    quote_currency = sys.argv[1].strip().upper()
    if quote_currency not in SUPPORTED_QUOTE_CURRENCIES:
        print(f"查询失败: unsupported quote_currency: {quote_currency}")
        print(f"SUPPORTED={','.join(SUPPORTED_QUOTE_CURRENCIES)}")
        return 1

    try:
        payload = request_json(f"{resolve_base_url()}/api/quotes/latest")
        item = next((value for value in payload.get("items", []) if value.get("quote_currency") == quote_currency), None)
        if item is None:
            raise RuntimeError(f"quote not found for {quote_currency}")
        print(f"BASE_CURRENCY={payload.get('base_currency', 'CNY')}")
        print(f"QUOTE_CURRENCY={quote_currency}")
        print(f"RATE={item['rate']}")
        print(f"OBSERVATION_DATE={item.get('observation_date', '')}")
        return 0
    except Exception as exc:
        print(f"查询失败: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
