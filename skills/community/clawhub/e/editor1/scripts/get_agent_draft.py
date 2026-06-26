#!/usr/bin/env python3
"""
功能：查看指定 agent_id 的草稿配置
用法：python get_agent_draft.py <agent_id>
示例：python get_agent_draft.py 877c45a6f2f542e0b3dadb089f6ef532
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, api_post


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("用法：python get_agent_draft.py <agent_id>")
        print("示例：python get_agent_draft.py 877c45a6f2f542e0b3dadb089f6ef532")
        sys.exit(0)

    agent_id = sys.argv[1].strip()
    if not agent_id:
        print("错误：agent_id 不能为空", file=sys.stderr)
        sys.exit(1)

    jwt_token, username = get_env()
    headers = get_auth_headers(jwt_token, username)

    # 调用 get_draft
    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/get_draft",
        headers,
        {"agent_id": agent_id},
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
