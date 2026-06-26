#!/usr/bin/env python3
"""
获取工作流的节点信息
用法: python3 get_workflow_info.py <HOST> <API_KEY> <WEBAPP_ID>
"""

import sys
import json
import urllib.request
import urllib.error


def get_workflow_info(host: str, api_key: str, webapp_id: str) -> dict:
    """获取工作流的节点信息"""
    url = f"https://{host}/api/webapp/apiCallDemo"

    headers = {
        "Host": host,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = f"?apiKey={api_key}&webappId={webapp_id}"

    req = urllib.request.Request(
        url + params,
        headers=headers,
        method="GET"
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
    if len(sys.argv) < 4:
        print("Usage: python3 get_workflow_info.py <HOST> <API_KEY> <WEBAPP_ID>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    api_key = sys.argv[2]
    webapp_id = sys.argv[3]

    try:
        result = get_workflow_info(host, api_key, webapp_id)
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
