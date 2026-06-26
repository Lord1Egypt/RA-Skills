#!/usr/bin/env python3
"""
功能5：修改 Agent 草稿的指定字段
用法：python modify_draft.py [agent_id] --name <名称> --desc <描述> --welcome_msg <欢迎语>
                              --system_prompt <提示词> --model <模型名>

参数说明：
  agent_id      : 可选，不传则使用当前对话的 agent_id
  --name        : 修改智能体名称
  --desc        : 修改描述
  --welcome_msg : 修改欢迎语
  --system_prompt : 修改系统提示词（支持从文件读取，前缀 @，如 @prompt.txt）
  --model       : 修改默认模型（使用 model_name，可通过 list_models.py 查询）

示例：
  python modify_draft.py --name "新名称" --desc "新描述"
  python modify_draft.py agent_xxx --system_prompt @my_prompt.txt
  python modify_draft.py --model claude-3-5-sonnet
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from common import BASE_URL, get_env, get_auth_headers, parse_current_agent_id, api_post


def parse_args():
    parser = argparse.ArgumentParser(description="修改 Knot Agent 草稿字段")
    parser.add_argument("agent_id", nargs="?", default=None, help="Agent ID（可选，默认使用当前对话 agent）")
    parser.add_argument("--name", default=None, help="修改智能体名称")
    parser.add_argument("--desc", default=None, help="修改描述")
    parser.add_argument("--welcome_msg", default=None, help="修改欢迎语")
    parser.add_argument("--system_prompt", default=None,
                        help="修改系统提示词（支持 @文件路径 从文件读取）")
    parser.add_argument("--model", default=None, help="修改默认模型（使用 model_name）")
    return parser.parse_args()


def resolve_value(value: str) -> str:
    """若 value 以 @ 开头，则从文件读取内容"""
    if value and value.startswith("@"):
        file_path = value[1:]
        if not os.path.exists(file_path):
            print(f"错误：文件不存在：{file_path}", file=sys.stderr)
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return value


def main():
    args = parse_args()

    # 构建修改 payload（只包含非空字段）
    payload = {}
    if args.name is not None:
        payload["name"] = resolve_value(args.name)
    if args.desc is not None:
        payload["desc"] = resolve_value(args.desc)
    if args.welcome_msg is not None:
        payload["welcome_msg"] = resolve_value(args.welcome_msg)
    if args.system_prompt is not None:
        payload["system_prompt"] = resolve_value(args.system_prompt)
    if args.model is not None:
        payload["default_llm_model"] = args.model

    if not payload:
        print("错误：未指定任何要修改的字段。请使用 --name / --desc / --welcome_msg / --system_prompt / --model 参数。")
        sys.exit(1)

    jwt_token, username = get_env()

    agent_id = args.agent_id
    if not agent_id:
        agent_id = parse_current_agent_id(jwt_token)

    payload["agent_id"] = agent_id

    headers = get_auth_headers(jwt_token, username)

    result = api_post(
        f"{BASE_URL}/openapi/v1/agents/modify_draft",
        headers,
        payload,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
