#!/usr/bin/env python3
"""
Cell base station query skill for OpenClaw.
基于极速数据基站查询 API：
https://www.jisuapi.com/api/cell/
"""

import sys
import json
import os
import requests


CELL_QUERY_URL = "https://api.jisuapi.com/cell/query"


def query_cell(appkey: str, req: dict):
    """
    基站查询 /cell/query

    请求 JSON 示例（移动/联通）：
    {
        "mnc": "0",
        "lac": "22709",
        "cellid": "39205",
        "sid": "",
        "nid": ""
    }
    """
    mnc = req.get("mnc")
    lac = req.get("lac")
    cellid = req.get("cellid")

    if not mnc:
        return {"error": "missing_param", "message": "mnc is required"}
    if not lac:
        return {"error": "missing_param", "message": "lac is required"}
    if not cellid:
        return {"error": "missing_param", "message": "cellid is required"}

    params = {
        "appkey": appkey,
        "mnc": mnc,
        "lac": lac,
        "cellid": cellid,
    }

    sid = req.get("sid")
    nid = req.get("nid")
    if sid is not None:
        params["sid"] = sid
    if nid is not None:
        params["nid"] = nid

    try:
        resp = requests.get(CELL_QUERY_URL, params=params, timeout=10)
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
            "  cell.py '{\"mnc\":\"0\",\"lac\":\"22709\",\"cellid\":\"39205\",\"sid\":\"\",\"nid\":\"\"}'  # 基站查询",
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

    # 基本必填校验
    for field in ("mnc", "lac", "cellid"):
        if field not in req or req[field] in (None, ""):
            print(f"Error: '{field}' is required in request JSON.", file=sys.stderr)
            sys.exit(1)

    result = query_cell(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

