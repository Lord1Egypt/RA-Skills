#!/usr/bin/env python3
"""RAG 接口语义检索 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.rag_query.service import rag_query_api_info

COMMAND_NAME = "rag_query"
COMMAND_DESC = "RAG 语义检索接口文档（输入自然语言，返回匹配的 API 信息）"


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置。\n\n请运行: `cli.py configure YOUR_AK`",
                     {"data": []})
        return

    parser = argparse.ArgumentParser(description="RAG 接口语义检索")
    parser.add_argument("--query", "-q", required=True, help="自然语言查询描述")
    args = parser.parse_args()

    try:
        result = rag_query_api_info(args.query)
        print_output(True, "RAG 检索完成", {"data": result})
    except Exception as e:
        print_error(e, {"data": []})


if __name__ == "__main__":
    main()
