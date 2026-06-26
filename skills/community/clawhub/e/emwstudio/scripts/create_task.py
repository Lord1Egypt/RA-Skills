#!/usr/bin/env python3
"""
创建RunningHub工作流任务
用法: python3 create_task.py <HOST> <API_KEY> <WEBAPP_ID> <NODE_INFO_LIST>
"""

import sys
import json
import urllib.request
import urllib.error


def create_task(host: str, api_key: str, webapp_id: str, node_info_list: list) -> dict:
    """创建工作流任务"""
    url = f"https://{host}/task/openapi/ai-app/run"

    headers = {
        "Host": host,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "webappId": int(webapp_id),
        "apiKey": api_key,
        "nodeInfoList": node_info_list
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 create_task.py <HOST> <API_KEY> <WEBAPP_ID> <NODE_INFO_LIST>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    api_key = sys.argv[2]
    webapp_id = sys.argv[3]
    node_info_list = json.loads(sys.argv[4])

    try:
        result = create_task(host, api_key, webapp_id, node_info_list)
        print(json.dumps(result, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        error_response = {
            "code": e.code,
            "msg": str(e.reason),
            "data": None
        }
        try:
            body = json.loads(e.read().decode("utf-8"))
            error_response["msg"] = body.get("msg", str(e.reason))
        except:
            pass
        print(json.dumps(error_response, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"code": -1, "msg": str(e), "data": None}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
