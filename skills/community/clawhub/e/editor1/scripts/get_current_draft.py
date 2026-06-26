#!/usr/bin/env python3
"""
功能1：查看当前对话智能体的草稿配置
用法：python get_current_draft.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, parse_current_agent_id, api_post


def main():
    jwt_token, username = get_env()

    # 从 JWT 解析当前对话的 scene
    scene = parse_current_agent_id(jwt_token)

    # 获取认证头
    headers = get_auth_headers(jwt_token, username)

    # 通过 scene 查询真实 agent_id
    list_result = api_post(
        f"{BASE_URL}/openapi/v1/agents/list",
        headers,
        {"scene": scene},
    )
    agents = list_result.get("data") or []
    if not agents:
        print(f"错误：未找到 scene={scene} 对应的 Agent，请确认当前对话的智能体配置。")
        sys.exit(1)
    agent_id = agents[0].get("id")

    # 调用 get_draft
    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/get_draft",
        headers,
        {"agent_id": agent_id},
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
