#!/usr/bin/env python3
"""
获取RunningHub账户信息
用法: python3 get_account_info.py <HOST> <API_KEY>
"""

import sys
import json
import urllib.request
import urllib.error


def get_account_info(host: str, api_key: str) -> dict:
    """获取账户信息"""
    url = f"https://{host}/uc/openapi/accountStatus"

    headers = {
        "Host": host,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {"apikey": api_key}

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
            return {
                "code": e.code,
                "msg": body.get("msg", str(e.reason)),
                "errorMessages": [str(e.reason)]
            }
        except:
            return {
                "code": e.code,
                "msg": str(e.reason),
                "errorMessages": [str(e.reason)]
            }
    except Exception as e:
        return {
            "code": -1,
            "msg": str(e),
            "errorMessages": [str(e)]
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 get_account_info.py <HOST> <API_KEY>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    api_key = sys.argv[2]

    try:
        result = get_account_info(host, api_key)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "code": -1,
            "msg": str(e),
            "errorMessages": [str(e)]
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
