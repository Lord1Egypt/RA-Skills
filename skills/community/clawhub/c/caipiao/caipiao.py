#!/usr/bin/env python3
"""
Lottery (caipiao) skill for OpenClaw.
基于极速数据彩票开奖 API：
https://www.jisuapi.com/api/caipiao/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/caipiao"


def _call_caipiao_api(path: str, appkey: str, params: dict = None):
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

    return data.get("result", {})


def query(appkey: str, req: dict):
    """
    彩票开奖 /caipiao/query

    请求 JSON 示例：
    { "caipiaoid": 13, "issueno": "" }
    """
    caipiaoid = req.get("caipiaoid")
    if caipiaoid in (None, ""):
        return {"error": "missing_param", "message": "caipiaoid is required"}

    params = {
        "caipiaoid": caipiaoid,
        "issueno": req.get("issueno"),
    }
    return _call_caipiao_api("query", appkey, params)


def history(appkey: str, req: dict):
    """
    历史开奖信息 /caipiao/history

    请求 JSON 示例：
    {
        "caipiaoid": 13,
        "issueno": "",
        "start": 0,
        "num": 10
    }
    """
    caipiaoid = req.get("caipiaoid")
    if caipiaoid in (None, ""):
        return {"error": "missing_param", "message": "caipiaoid is required"}

    params = {
        "caipiaoid": caipiaoid,
        "issueno": req.get("issueno"),
        "start": req.get("start"),
        "num": req.get("num"),
    }
    return _call_caipiao_api("history", appkey, params)


def class_list(appkey: str):
    """
    彩票分类 /caipiao/class
    """
    return _call_caipiao_api("class", appkey, {})


def winning(appkey: str, req: dict):
    """
    查询是否中奖 /caipiao/winning

    请求 JSON 示例：
    {
        "caipiaoid": 11,
        "issueno": "",
        "number": "20 03 05 07 22",
        "refernumber": "12",
        "type": ""
    }
    """
    caipiaoid = req.get("caipiaoid")
    number = req.get("number")
    if caipiaoid in (None, ""):
        return {"error": "missing_param", "message": "caipiaoid is required"}
    if not number:
        return {"error": "missing_param", "message": "number is required"}

    params = {
        "caipiaoid": caipiaoid,
        "issueno": req.get("issueno"),
        "number": number,
        "refernumber": req.get("refernumber"),
        "type": req.get("type"),
    }
    return _call_caipiao_api("winning", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  caipiao.py class                                   # 彩票分类\n"
            "  caipiao.py query   '{\"caipiaoid\":13}'            # 最新开奖\n"
            "  caipiao.py history '{\"caipiaoid\":13,\"num\":10}' # 历史开奖\n"
            "  caipiao.py winning '{\"caipiaoid\":11,\"number\":\"02 06 15 25 30 32\",\"refernumber\":\"08\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "class":
        result = class_list(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if cmd not in ("query", "history", "winning"):
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"Error: JSON body is required for '{cmd}'.", file=sys.stderr)
        sys.exit(1)

    raw = sys.argv[2]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if cmd == "query":
        result = query(appkey, req)
    elif cmd == "history":
        result = history(appkey, req)
    elif cmd == "winning":
        result = winning(appkey, req)
    else:
        print(f"Error: unhandled command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

