#!/usr/bin/env python3
"""
Exchange rate skill for OpenClaw.
基于极速数据汇率查询 API：
https://www.jisuapi.com/api/exchange/
"""

import sys
import json
import os
import requests


EXCHANGE_CONVERT_URL = "https://api.jisuapi.com/exchange/convert"
EXCHANGE_SINGLE_URL = "https://api.jisuapi.com/exchange/single"
EXCHANGE_CURRENCY_URL = "https://api.jisuapi.com/exchange/currency"
EXCHANGE_BANK_URL = "https://api.jisuapi.com/exchange/bank"
EXCHANGE_REALTIME_URL = "https://api.jisuapi.com/exchange/realtime"
EXCHANGE_BANKHISTORY_URL = "https://api.jisuapi.com/exchange/bankhistory"
EXCHANGE_HISTORY_URL = "https://api.jisuapi.com/exchange/history"
EXCHANGE_HISTORY2_URL = "https://api.jisuapi.com/exchange/history2"


def convert_exchange(appkey: str, req: dict):
    """
    调用 /exchange/convert 接口，进行货币间汇率换算。

    请求 JSON 示例：
    {
        "from": "CNY",
        "to": "USD",
        "amount": 10
    }
    """
    params = {"appkey": appkey}

    from_currency = req.get("from")
    to_currency = req.get("to")
    amount = req.get("amount", 1)

    if not from_currency:
        return {"error": "missing_param", "message": "from is required"}
    if not to_currency:
        return {"error": "missing_param", "message": "to is required"}

    params["from"] = from_currency
    params["to"] = to_currency
    params["amount"] = amount

    try:
        resp = requests.get(EXCHANGE_CONVERT_URL, params=params, timeout=10)
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


def single_currency(appkey: str, currency: str):
    """
    调用 /exchange/single 接口，查询单个货币相对热门货币的汇率列表。
    """
    params = {
        "appkey": appkey,
        "currency": currency,
    }

    try:
        resp = requests.get(EXCHANGE_SINGLE_URL, params=params, timeout=10)
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


def list_currencies(appkey: str):
    """
    调用 /exchange/currency 接口，查询所有支持的货币列表。
    """
    params = {"appkey": appkey}

    try:
        resp = requests.get(EXCHANGE_CURRENCY_URL, params=params, timeout=10)
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

    return data.get("result", [])


def bank_rates(appkey: str, bank: str = None):
    """
    调用 /exchange/bank 接口，查询指定银行的外汇牌价（十大银行）。

    bank 编码（可选，不传则默认为 BOC）：
      - ICBC: 工商银行
      - BOC: 中国银行
      - ABCHINA: 农业银行
      - BANKCOMM: 交通银行
      - CCB: 建设银行
      - CMBCHINA: 招商银行
      - CEBBANK: 光大银行
      - SPDB: 浦发银行
      - CIB: 兴业银行
      - ECITIC: 中信银行
    """
    params = {"appkey": appkey}
    if bank:
        params["bank"] = bank

    try:
        resp = requests.get(EXCHANGE_BANK_URL, params=params, timeout=10)
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


def _call_exchange_api(url: str, appkey: str, params: dict = None):
    if params is None:
        params = {}
    all_params = {"appkey": appkey}
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


def realtime_rates(appkey: str, rate_type: str = "basic"):
    """
    调用 /exchange/realtime 接口，查询基本汇率或交叉盘实时行情。
    type: basic（基本汇率）| cross（交叉盘）
    """
    return _call_exchange_api(EXCHANGE_REALTIME_URL, appkey, {"type": rate_type or "basic"})


def bank_history(appkey: str, req: dict):
    """
    调用 /exchange/bankhistory 接口，查询银行历史外汇牌价。

    请求 JSON 示例：
    {
        "startdate": "2026-06-01",
        "enddate": "2026-06-11",
        "bank": "BOC",
        "code": "USD"
    }
    """
    for field in ("startdate", "enddate", "bank"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "startdate": req["startdate"],
        "enddate": req["enddate"],
        "bank": req["bank"],
        "code": req.get("code", ""),
    }
    return _call_exchange_api(EXCHANGE_BANKHISTORY_URL, appkey, params)


def exchange_history(appkey: str, req: dict):
    """
    调用 /exchange/history 接口，查询两种货币之间的历史汇率。

    请求 JSON 示例：
    {
        "from": "USD",
        "to": "CNY",
        "startdate": "2026-06-01",
        "enddate": "2026-06-10"
    }
    """
    for field in ("from", "to", "startdate", "enddate"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "from": req["from"],
        "to": req["to"],
        "startdate": req["startdate"],
        "enddate": req["enddate"],
    }
    return _call_exchange_api(EXCHANGE_HISTORY_URL, appkey, params)


def exchange_history2(appkey: str, req: dict):
    """
    调用 /exchange/history2 接口，按 6 位货币代码查询历史行情（含开高低收）。

    请求 JSON 示例：
    {
        "code": "USDCNY",
        "startdate": "2026-06-01",
        "enddate": "2026-06-10"
    }
    """
    for field in ("code", "startdate", "enddate"):
        if not req.get(field):
            return {"error": "missing_param", "message": f"{field} is required"}
    params = {
        "code": req["code"],
        "startdate": req["startdate"],
        "enddate": req["enddate"],
    }
    return _call_exchange_api(EXCHANGE_HISTORY2_URL, appkey, params)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  exchange.py '{\"from\":\"CNY\",\"to\":\"USD\",\"amount\":10}'   # 汇率换算\n"
            "  exchange.py single CNY                                          # 单个货币相对热门货币汇率\n"
            "  exchange.py currency                                            # 所有货币列表\n"
            "  exchange.py bank BOC                                            # 银行外汇牌价（默认 BOC）\n"
            "  exchange.py realtime basic                                        # 基本汇率实时行情\n"
            "  exchange.py realtime cross                                        # 交叉盘实时行情\n"
            "  exchange.py bankhistory '{\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-11\",\"bank\":\"BOC\",\"code\":\"USD\"}'\n"
            "  exchange.py history '{\"from\":\"USD\",\"to\":\"CNY\",\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-10\"}'\n"
            "  exchange.py history2 '{\"code\":\"USDCNY\",\"startdate\":\"2026-06-01\",\"enddate\":\"2026-06-10\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")

    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    # 单个货币
    if cmd == "single":
        if len(sys.argv) < 3:
            print("Error: currency code is required for 'single'.", file=sys.stderr)
            sys.exit(1)
        currency = sys.argv[2]
        result = single_currency(appkey, currency)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 所有货币
    if cmd in ("currency", "currencies", "list"):
        result = list_currencies(appkey)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 银行外汇牌价
    if cmd == "bank":
        bank_code = sys.argv[2] if len(sys.argv) >= 3 else None
        result = bank_rates(appkey, bank_code)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 基本/交叉盘实时行情
    if cmd == "realtime":
        rate_type = sys.argv[2] if len(sys.argv) >= 3 else "basic"
        result = realtime_rates(appkey, rate_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 银行历史牌价 / 历史汇率 / 历史行情
    if cmd in ("bankhistory", "history", "history2"):
        if len(sys.argv) < 3:
            print(f"Error: JSON request body is required for '{cmd}'.", file=sys.stderr)
            sys.exit(1)
        try:
            req = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if cmd == "bankhistory":
            result = bank_history(appkey, req)
        elif cmd == "history":
            result = exchange_history(appkey, req)
        else:
            result = exchange_history2(appkey, req)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 默认：汇率换算，参数为 JSON
    raw = sys.argv[1]
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    if "from" not in req or "to" not in req:
        print("Error: 'from' and 'to' are required in request JSON.", file=sys.stderr)
        sys.exit(1)

    result = convert_exchange(appkey, req)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

