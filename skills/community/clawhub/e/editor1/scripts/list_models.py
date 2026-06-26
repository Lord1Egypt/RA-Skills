#!/usr/bin/env python3
"""
功能3：查看指定 Agent 可用的大模型列表
用法：python list_models.py [agent_id]
  agent_id: 可选，不传则使用当前对话的 agent_id
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, parse_current_agent_id, api_post


def main():
    agent_id = sys.argv[1] if len(sys.argv) > 1 else None

    jwt_token, username = get_env()

    if not agent_id:
        agent_id = parse_current_agent_id(jwt_token)

    headers = get_auth_headers(jwt_token, username)

    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/list_available_llm_model",
        headers,
        {"agent_id": agent_id},
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
