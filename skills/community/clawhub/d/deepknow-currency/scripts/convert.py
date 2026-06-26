#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from runtime_config import SUPPORTED_QUOTE_CURRENCIES, resolve_base_url


def request_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) < 4:
        print("换算失败: usage: convert.py <from_currency> <to_currency> <amount>")
        return 1

    from_currency = sys.argv[1].strip().upper()
    to_currency = sys.argv[2].strip().upper()
    amount_raw = sys.argv[3].strip()

    try:
        amount = float(amount_raw)
    except ValueError:
        print(f"换算失败: invalid amount: {amount_raw}")
        return 1

    supported = {"CNY", *SUPPORTED_QUOTE_CURRENCIES}
    if from_currency not in supported:
        print(f"换算失败: unsupported source currency: {from_currency}")
        print(f"SUPPORTED=CNY,{','.join(SUPPORTED_QUOTE_CURRENCIES)}")
        return 1
    if to_currency not in supported:
        print(f"换算失败: unsupported target currency: {to_currency}")
        print(f"SUPPORTED=CNY,{','.join(SUPPORTED_QUOTE_CURRENCIES)}")
        return 1
    if from_currency != "CNY" and to_currency != "CNY":
        print("换算失败: conversion must involve CNY")
        return 1

    try:
        query = urlencode({"from": from_currency, "to": to_currency, "amount": amount_raw})
        payload = request_json(f"{resolve_base_url()}/api/convert?{query}")
        print(f"FROM_CURRENCY={payload['from_currency']}")
        print(f"TO_CURRENCY={payload['to_currency']}")
        print(f"AMOUNT={payload['amount']}")
        print(f"CONVERTED_AMOUNT={payload['converted_amount']}")
        print(f"BASE_CURRENCY={payload.get('base_currency', 'CNY')}")
        return 0
    except Exception as exc:
        print(f"换算失败: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
