#!/usr/bin/env python3
"""
Barcode2 skill for OpenClaw.
基于极速数据商品条码查询 API：
https://www.jisuapi.com/api/barcode2/
"""

import sys
import json
import os
import requests


BARCODE2_URL = "https://api.jisuapi.com/barcode2/query"


def query_barcode(appkey: str, req: dict):
    """
    调用 /barcode2/query 接口，按条形码查询商品信息。

    请求 JSON 示例：
    {
        "barcode": "06917878036526"
    }
    """
    params = {"appkey": appkey}

    barcode = req.get("barcode")
    if not barcode:
        return {
            "error": "missing_param",
            "message": "barcode is required",
        }
    params["barcode"] = barcode

    try:
        resp = requests.get(BARCODE2_URL, params=params, timeout=10)
    except Exception as e:
        return {
            "error": "request_failed",
            "message": str(e),
        }

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {
            "error": "invalid_json",
            "body": resp.text,
        }

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", {})


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  barcode.py '{\"barcode\":\"06917878036526\"}'  # 按条形码查询商品",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if "barcode" not in req or not req["barcode"]:
        print("Error: 'barcode' is required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = query_barcode(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

