#!/usr/bin/env python3
"""
功能4：基于最新版本重新生成 Agent 草稿
用法：python new_draft.py [agent_id]
  agent_id: 可选，不传则使用当前对话的 agent_id

⚠️ 警告：此操作会覆盖当前未发布的草稿内容，请确认后再执行。
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
        print(f"使用当前对话 Agent ID: {agent_id}")

    # 二次确认
    print(f"\n⚠️  即将基于最新版本重新生成 Agent [{agent_id}] 的草稿。")
    print("    此操作将覆盖当前未发布的草稿内容！")
    confirm = input("请输入 yes 确认，其他任意键取消：").strip().lower()
    if confirm != "yes":
        print("已取消操作。")
        sys.exit(0)

    headers = get_auth_headers(jwt_token, username)

    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/new_draft_from_latest_version",
        headers,
        {"agent_id": agent_id},
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
