#!/usr/bin/env python3
"""
Driver exam question bank skill for OpenClaw.
基于极速数据驾考题库 API：
https://www.jisuapi.com/api/driverexam/
"""

import sys
import json
import os
import requests


DRIVEREXAM_QUERY_URL = "https://api.jisuapi.com/driverexam/query"


def query_driverexam(appkey: str, req: dict):
    """
    获取考题 /driverexam/query

    请求 JSON 示例：
    {
        "type": "C1",
        "subject": "1",
        "pagesize": "10",
        "pagenum": "1",
        "sort": "normal",
        "chapter": "1"
    }
    """
    type_ = req.get("type")
    if not type_:
        return {"error": "missing_param", "message": "type is required"}

    params: dict = {
        "appkey": appkey,
        "type": type_,
    }

    # 可选参数，按文档直接透传
    for key in ("subject", "pagesize", "pagenum", "sort", "chapter"):
        value = req.get(key)
        if value not in (None, ""):
            params[key] = value

    try:
        resp = requests.get(DRIVEREXAM_QUERY_URL, params=params, timeout=10)
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


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  driverexam.py '{\"type\":\"C1\",\"subject\":\"1\",\"pagesize\":\"10\",\"pagenum\":\"1\",\"sort\":\"normal\"}'  # 获取考题",
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

    if "type" not in req or not req["type"]:
        print("Error: 'type' is required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = query_driverexam(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

