#!/usr/bin/env python3
"""
功能2：查询名下有管理权限的 Agent 列表
用法：python list_agents.py [--agent_id <id>] [--keyword <关键字>]
  --agent_id: 可选，按 agent_id 精确查询
  --keyword : 可选，按名称/描述关键字过滤

示例：
  python list_agents.py
  python list_agents.py --keyword 客服
  python list_agents.py --agent_id agent_xxx
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, api_post


def parse_args():
    parser = argparse.ArgumentParser(description="查询名下有管理权限的 Agent 列表")
    parser.add_argument("--agent_id", default=None, help="按 agent_id 精确查询")
    parser.add_argument("--keyword", default=None, help="按名称/描述关键字过滤")
    return parser.parse_args()


def main():
    args = parse_args()

    jwt_token, username = get_env()
    headers = get_auth_headers(jwt_token, username)

    payload = {}
    if args.agent_id:
        payload["agent_id"] = args.agent_id
    if args.keyword:
        payload["keyword"] = args.keyword

    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/list",
        headers,
        payload,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
