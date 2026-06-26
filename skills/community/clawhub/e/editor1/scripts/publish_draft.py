#!/usr/bin/env python3
"""
功能6：将 Agent 草稿发布为正式版本
用法：python publish_draft.py [agent_id]
  agent_id: 可选，不传则使用当前对话的 agent_id

⚠️ 高危操作：发布后所有用户的正式对话立即使用新版本。
             若草稿 is_stale=true，发布将覆盖 agent 最新版本的改动。
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, parse_current_agent_id, api_post


def check_draft_stale(agent_id: str, headers: dict) -> bool:
    """检查草稿是否过期，返回 is_stale 状态"""
    try:
        result = api_post(
            f"{BASE_URL}/openapi/v1/agents/get_draft",
            headers,
            {"agent_id": agent_id},
        )
        draft = result.get("data") or {}
        return bool(draft.get("is_stale"))
    except SystemExit:
        return False


def main():
    agent_id = sys.argv[1] if len(sys.argv) > 1 else None

    jwt_token, username = get_env()

    if not agent_id:
        agent_id = parse_current_agent_id(jwt_token)
        print(f"使用当前对话 Agent ID: {agent_id}")

    headers = get_auth_headers(jwt_token, username)

    # 检查草稿是否过期
    is_stale = check_draft_stale(agent_id, headers)

    print("\n" + "=" * 60)
    print("⚠️  高危操作确认")
    print("=" * 60)
    print(f"Agent ID : {agent_id}")
    print("操作说明 : 将当前草稿发布为正式版本")
    print("影响范围 : 发布后，所有用户的正式对话立即使用新版本")

    if is_stale:
        print("\n🔴 警告：当前草稿已过期！")
        print("   草稿基于的版本低于 Agent 最新发布版本。")
        print("   发布此草稿将覆盖 Agent 最新版本的改动，可能导致数据丢失！")
        print("   建议先运行 new_draft.py 基于最新版本重新生成草稿。")

    print("\n请输入 yes 确认发布，其他任意键取消：", end="")
    confirm = input().strip().lower()
    if confirm != "yes":
        print("已取消发布操作。")
        sys.exit(0)

    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/publish_draft",
        headers,
        {"agent_id": agent_id},
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
