#!/usr/bin/env python3
"""
Auto parts EPC query skill for OpenClaw.
基于极速数据汽车配件 EPC 查询 API：
https://www.jisuapi.com/api/epc/
"""

import sys
import json
import os
import requests


BASE_URL = "https://api.jisuapi.com/epc"


def _call_epc_api(path: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
    all_params.update({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{BASE_URL}/{path}"

    try:
        resp = requests.get(url, params=all_params, timeout=15)
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


def car(appkey: str, req: dict):
    """
    车型查询 /epc/car

    请求 JSON 示例：
    { "parentid": 0 }
    """
    parentid = req.get("parentid")
    if parentid in (None, ""):
        return {"error": "missing_param", "message": "parentid is required"}
    return _call_epc_api("car", appkey, {"parentid": parentid})


def cardetail(appkey: str, req: dict):
    """
    车型详情 /epc/cardetail

    请求 JSON 示例：
    { "carid": 629 }
    """
    carid = req.get("carid")
    if carid in (None, ""):
        return {"error": "missing_param", "message": "carid is required"}
    return _call_epc_api("cardetail", appkey, {"carid": carid})


def vin(appkey: str, req: dict):
    """
    VIN 查询 /epc/vin

    请求 JSON 示例：
    { "vin": "LE4HG5EB3AL999908" }
    """
    vin_code = req.get("vin")
    if not vin_code:
        return {"error": "missing_param", "message": "vin is required"}
    return _call_epc_api("vin", appkey, {"vin": vin_code})


def group(appkey: str, req: dict):
    """
    车型组查询 /epc/group

    请求 JSON 示例：
    { "carid": 630, "parentid": 0, "vin": "" }
    carid 与 vin 任选其一；parentid 为当前组上级 ID。
    """
    carid = req.get("carid")
    vin_code = req.get("vin")
    parentid = req.get("parentid")

    if parentid in (None, ""):
        return {"error": "missing_param", "message": "parentid is required"}
    if not carid and not vin_code:
        return {"error": "missing_param", "message": "carid or vin is required"}

    params = {"parentid": parentid}
    if carid not in (None, ""):
        params["carid"] = carid
    if vin_code:
        params["vin"] = vin_code
    return _call_epc_api("group", appkey, params)


def groupparts(appkey: str, req: dict):
    """
    组和配件查询 /epc/groupparts

    请求 JSON 示例：
    { "carid": 630, "parentid": 3 }
    """
    carid = req.get("carid")
    parentid = req.get("parentid")
    missing = []
    if parentid in (None, ""):
        missing.append("parentid")
    if carid in (None, ""):
        missing.append("carid")
    if missing:
        return {
            "error": "missing_param",
            "message": f"Missing required fields: {', '.join(missing)}",
        }
    params = {"carid": carid, "parentid": parentid}
    return _call_epc_api("groupparts", appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  epc.py car '{\"parentid\":0}'\n"
            "  epc.py cardetail '{\"carid\":629}'\n"
            "  epc.py vin '{\"vin\":\"LE4HG5EB3AL999908\"}'\n"
            "  epc.py group '{\"carid\":630,\"parentid\":0}'\n"
            "  epc.py groupparts '{\"carid\":630,\"parentid\":3}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd not in ("car", "cardetail", "vin", "group", "groupparts"):
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

    if cmd == "car":
        result = car(appkey, req)
    elif cmd == "cardetail":
        result = cardetail(appkey, req)
    elif cmd == "vin":
        result = vin(appkey, req)
    elif cmd == "group":
        result = group(appkey, req)
    elif cmd == "groupparts":
        result = groupparts(appkey, req)
    else:
        print(f"Error: unhandled command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

