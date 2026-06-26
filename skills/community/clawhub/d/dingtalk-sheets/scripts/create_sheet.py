#!/usr/bin/env python3
"""
创建钉钉在线表格，并可选新增一个工作表。

用法:
    python create_sheet.py <name> [--sheet-name <sheet_name>] [--folder-id <folderId>] [--workspace-id <workspaceId>]
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from mcporter_utils import build_node_url, extract_node_id, parse_response, run_mcporter


def create_workspace_sheet(name: str, folder_id: Optional[str] = None, workspace_id: Optional[str] = None) -> Optional[dict]:
    """创建一个新的钉钉在线表格。"""
    args = {"name": name}
    if folder_id:
        args["folderId"] = folder_id
    if workspace_id:
        args["workspaceId"] = workspace_id

    success, output = run_mcporter("create_workspace_sheet", args)
    if not success:
        print(f"错误：创建表格失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"错误：解析响应失败：{output}")
        return None
    return result


def create_sheet_tab(node_id: str, sheet_name: str) -> Optional[dict]:
    """在已有表格里创建一个新的工作表。"""
    success, output = run_mcporter("create_sheet", {"nodeId": node_id, "name": sheet_name})
    if not success:
        print(f"错误：创建工作表失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"错误：解析响应失败：{output}")
        return None
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="创建钉钉在线表格")
    parser.add_argument("name", help="表格标题")
    parser.add_argument("--sheet-name", help="创建表格后追加创建的工作表名称")
    parser.add_argument("--folder-id", help="目标文件夹 ID 或链接 URL")
    parser.add_argument("--workspace-id", help="目标知识库 ID")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    print(f"开始创建表格：{args.name}")
    print("-" * 50)

    print("步骤 1: 创建表格文件...")
    result = create_workspace_sheet(args.name, folder_id=args.folder_id, workspace_id=args.workspace_id)
    if result is None:
        sys.exit(1)

    node_id = extract_node_id(result)
    if not node_id:
        print("错误：无法从返回结果提取表格 nodeId")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(f"创建成功：{args.name}")
    print(f"   表格 ID: {node_id}")
    print(f"   访问链接：{result.get('pcUrl') or result.get('url') or build_node_url(node_id)}")

    if args.sheet_name:
        print("\n步骤 2: 创建附加工作表...")
        sheet_result = create_sheet_tab(node_id, args.sheet_name)
        if sheet_result is None:
            sys.exit(1)
        print(f"工作表创建成功：{args.sheet_name}")
        if isinstance(sheet_result, dict):
            sheet_id = sheet_result.get("sheetId") or sheet_result.get("id")
            if sheet_id:
                print(f"   工作表 ID: {sheet_id}")

    print("-" * 50)
    print("完成。")
    print(f"\n表格链接：{build_node_url(node_id)}")


if __name__ == "__main__":
    main()
