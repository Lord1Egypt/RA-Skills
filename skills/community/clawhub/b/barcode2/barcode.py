#!/usr/bin/env python3
"""
Jisu Barcode generate & read skill for OpenClaw.
基于极速数据条码生成识别 API：
https://www.jisuapi.com/api/barcode/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/barcode"


def _call_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update({k: v for k, v in params.items() if v not in (None, "")})

    url = f"{BASE_URL}/{path}"
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

    return data.get("result")


def cmd_generate(appkey: str, req: dict):
    """
    条码生成 /barcode/generate

    请求 JSON 示例：
    {
        "type": "ean13",
        "barcode": "6901236341056",
        "fontsize": 12,
        "dpi": 72,
        "scale": 2,
        "height": 40
    }
    """
    btype = req.get("type")
    code = req.get("barcode")
    if not btype:
        return {"error": "missing_param", "message": "type is required"}
    if not code:
        return {"error": "missing_param", "message": "barcode is required"}

    params = {
        "type": btype,
        "barcode": code,
        "fontsize": req.get("fontsize"),
        "dpi": req.get("dpi"),
        "scale": req.get("scale"),
        "height": req.get("height"),
    }
    return _call_api("generate", appkey, params)


def cmd_read(appkey: str, req: dict):
    """
    条码识别 /barcode/read

    请求 JSON 示例：
    {
        "barcode": "https://api.jisuapi.com/barcode/barcode/1471602033673149.png"
    }
    或 barcode 为 base64 条码图片内容。
    """
    barcode_val = req.get("barcode")
    if not barcode_val:
        return {"error": "missing_param", "message": "barcode is required (URL or base64 string)"}

    params = {"barcode": barcode_val}
    return _call_api("read", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  barcode.py generate '{\"type\":\"ean13\",\"barcode\":\"6901236341056\",\"fontsize\":12,\"dpi\":72,\"scale\":2,\"height\":40}'\n"
            "  barcode.py read '{\"barcode\":\"https://api.jisuapi.com/barcode/barcode/1471602033673149.png\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()

    req: dict = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        raw = sys.argv[2]
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(obj, dict):
            print("Error: JSON body must be an object.", file=sys.stderr)
            sys.exit(1)
        req = obj

    if cmd == "generate":
        result = cmd_generate(appkey, req)
    elif cmd == "read":
        result = cmd_read(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

