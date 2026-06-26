#!/usr/bin/env python3
"""
企业联系方式查询 skill for OpenClaw.
基于极速数据企业工商联系方式查询 API：
https://www.jisuapi.com/api/enterprisecontact/
"""

import sys
import json
import os
import requests


QUERY_URL = "https://api.jisuapi.com/enterprisecontact/query"


def cmd_query(appkey: str, req: dict):
    """
    企业联系方式查询 /enterprisecontact/query

    请求 JSON：company / creditno / regno / orgno 任填至少一个。
    """
    company = req.get("company")
    creditno = req.get("creditno")
    regno = req.get("regno")
    orgno = req.get("orgno")

    if not any(v not in (None, "") for v in (company, creditno, regno, orgno)):
        return {"error": "missing_param", "message": "至少提供 company、creditno、regno、orgno 之一"}

    params = {"appkey": appkey}
    if company not in (None, ""):
        params["company"] = company
    if creditno not in (None, ""):
        params["creditno"] = creditno
    if regno not in (None, ""):
        params["regno"] = regno
    if orgno not in (None, ""):
        params["orgno"] = orgno

    try:
        resp = requests.get(QUERY_URL, params=params, timeout=10)
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
            "  enterprisecontact.py query '{\"company\":\"北京抖音信息服务有限公司\"}'  # 按企业名\n"
            "  enterprisecontact.py query '{\"creditno\":\"91110000xxxx\"}'  # 按统一信用代码",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    if cmd != "query":
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    req = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(req, dict):
            req = {}

    result = cmd_query(appkey, req)
    if isinstance(result, dict) and result.get("error"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
