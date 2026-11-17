#!/usr/bin/env python3
"""
create_key.py — 验证短信验证码并获取 API Key

用法:
    python create_key.py <phone> <verify_code>

成功输出:
    {"error": 0, "key": "sk-xxx", "query_id": "2348523643"}

失败输出:
    {"error": <code>, "msg": "<描述>"}
"""

import sys
import json
import urllib.request
import urllib.error

API_URL = "https://youjia.baidu.com/bff-third-api/openapi/v1/key/register"


def create_key(phone: str, verify_code: str) -> dict:
    payload = json.dumps({
        "phone": phone,
        "code": verify_code,
        "app_id": "baidu-youjia-car",
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"error": -1, "msg": f"网络连接异常: {e.reason}"}
    except Exception as e:
        return {"error": -1, "msg": f"请求异常: {e}"}

    result_code = body.get("ResultCode", "-1")
    if result_code == "0":
        result_data = body.get("Result", {})
        return {
            "error": 0,
            "key": result_data.get("key_id", ""),
            "query_id": body.get("QueryID", ""),
        }
    else:
        return {
            "error": int(result_code) if result_code.lstrip("-").isdigit() else -1,
            "msg": body.get("ResultMsg", "未知错误"),
        }


def main():
    if len(sys.argv) != 3:
        print(json.dumps(
            {"error": -1, "msg": "用法: create_key.py <phone> <verify_code>"},
            ensure_ascii=False
        ))
        sys.exit(1)

    result = create_key(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)


if __name__ == "__main__":
    main()
