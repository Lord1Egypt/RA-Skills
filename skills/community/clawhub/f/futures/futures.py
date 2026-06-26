#!/usr/bin/env python3
"""
Futures price skill for OpenClaw.
基于极速数据期货查询 API：
https://www.jisuapi.com/api/futures/
"""

import sys
import json
import os
from typing import Optional

import requests


BASE_URL = "https://api.jisuapi.com/futures"

EXCHANGES = ("shfutures", "dlfutures", "zzfutures", "zgjrfutures", "gzfutures")


def _call_futures(path: str, appkey: str, params: Optional[dict] = None):
    url = f"{BASE_URL}/{path}"
    all_params = {"appkey": appkey}
    if params:
        all_params.update({k: v for k, v in params.items() if v not in (None, "")})

    try:
        resp = requests.get(url, params=all_params, timeout=10)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
        }

    return data.get("result", {})


def exchange_futures(appkey: str, exchange: str, req: Optional[dict] = None):
    """
    各交易所实时行情：shfutures / dlfutures / zzfutures / zgjrfutures / gzfutures
    可选 params: type（期货类型代码，如 FU2309、TA0）
    """
    params = {}
    if req and req.get("type"):
        params["type"] = req["type"]
    return _call_futures(exchange, appkey, params)


def futures_history(appkey: str, req: dict):
    """
    期货历史查询 /futures/history

    请求 JSON 示例：
    {
        "market": "shfutures",
        "type": "SC2703",
        "startdate": "2026-06-01",
        "enddate": "2026-06-10"
    }

    market: shfutures | dlfutures | zzfutures | zgjrfutures | gzfutures
    """
    for field in ("market", "type", "startdate", "enddate"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "market": req["market"],
        "type": req["type"],
        "startdate": req["startdate"],
        "enddate": req["enddate"],
    }
    return _call_futures("history", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  futures.py shfutures                              # 上海期货交易所\n"
            "  futures.py shfutures '{\"type\":\"FU2309\"}'         # 指定品种\n"
            "  futures.py dlfutures                              # 大连商品交易所\n"
            "  futures.py zzfutures                              # 郑州商品交易所\n"
            "  futures.py zgjrfutures                            # 中国金融期货交易所\n"
            "  futures.py gzfutures                              # 广州期货交易所\n"
            "  futures.py history '{\"market\":\"shfutures\",\"type\":\"SC2703\",\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-10\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    req = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(req, dict):
            req = {}

    if cmd == "history":
        result = futures_history(appkey, req)
    elif cmd in EXCHANGES:
        result = exchange_futures(appkey, cmd, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
