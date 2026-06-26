#!/usr/bin/env python3
"""模拟对话 CLI 入口 -- 测试接待助手回复能力"""

COMMAND_NAME = "test_chat"
COMMAND_DESC = "模拟对话试答（测试接待助手回复）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.test_chat.service import test_chat, format_chat_markdown


def main():
    parser = argparse.ArgumentParser(description="模拟对话试答", allow_abbrev=False)
    parser.add_argument("--query", "-q", required=True,
                        help="模拟买家提问内容")
    args = parser.parse_args()

    try:
        query = args.query.strip()
        if not query:
            print_output(False, "提问内容不能为空", {})
            return

        result = test_chat(query=query)
        markdown = format_chat_markdown(result)
        # 执行层兏底：剔除系统内部 ID（instanceId / requestId / agent_id / subaccount_id 等）后再下发给 LLM。
        # SKILL.md §严格禁止 §2 已以 prompt 软约束告知，这里加一道染色防御，避免模型被提示注入后透透内部 ID。
        safe_data = {k: v for k, v in result.items() if k not in ("instance_id",)}
        print_output(True, markdown, safe_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
