#!/usr/bin/env python3
"""
send_code.py — 发送短信验证码

用法:
    python send_code.py <phone>

成功输出:
    {"error": 0, "query_id": "2348523641"}

失败输出:
    {"error": <code>, "msg": "<描述>"}
"""

import sys
import json
import urllib.request
import urllib.error

API_URL = "https://youjia.baidu.com/bff-smartapp-api/clue/sendverifycode"


def send_code(phone: str) -> dict:
    url = f"{API_URL}?channel=youjia&phone={phone}"
    payload = json.dumps({"phone": phone, "channel": "youjia"}).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
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
        return {"error": 0, "query_id": body.get("QueryID", "")}
    else:
        return {"error": int(result_code) if result_code.lstrip("-").isdigit() else -1,
                "msg": body.get("ResultMsg", "未知错误")}


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": -1, "msg": "用法: send_code.py <phone>"}, ensure_ascii=False))
        sys.exit(1)

    result = send_code(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)


if __name__ == "__main__":
    main()
