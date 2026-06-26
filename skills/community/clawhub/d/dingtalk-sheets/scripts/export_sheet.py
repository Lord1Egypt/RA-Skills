#!/usr/bin/env python3
"""
导出钉钉表格数据到本地 CSV / TSV 文件。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Optional

from mcporter_utils import (
    extract_node_id_from_url,
    extract_range_payload,
    parse_response,
    resolve_safe_path,
    run_mcporter,
)


MAX_EXPORT_ROWS = 10000
MAX_EXPORT_COLUMNS = 500
ALLOWED_EXTENSIONS = [".csv", ".tsv"]


def extract_node_uuid(value: str) -> Optional[str]:
    """兼容测试命名，实际提取的是表格 nodeId / dentryUuid。"""
    return extract_node_id_from_url(value)


def validate_output_extension(filename: str) -> bool:
    """校验输出文件类型。"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def detect_delimiter(path: Path) -> str:
    """按目标文件扩展名推断分隔符。"""
    return "\t" if path.suffix.lower() == ".tsv" else ","


def get_range(node_id: str, sheet_id: Optional[str] = None, range_value: Optional[str] = None) -> Optional[dict]:
    args = {"nodeId": node_id}
    if sheet_id:
        args["sheetId"] = sheet_id
    if range_value:
        args["range"] = range_value

    success, output = run_mcporter("get_range", args)
    if not success:
        print(f"错误：获取表格数据失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"错误：解析响应失败：{output}")
        return None
    return extract_range_payload(result)


def select_table(payload: dict) -> list[list[str]]:
    """优先导出 displayValues，其次导出 values。"""
    table = payload.get("displayValues") or payload.get("values") or []
    if not isinstance(table, list):
        return []

    normalized: list[list[str]] = []
    for row in table:
        if isinstance(row, list):
            normalized.append(["" if cell is None else str(cell) for cell in row])
    return normalized


def validate_table_shape(rows: list[list[str]]) -> bool:
    """限制导出矩阵大小，避免一次性落盘超大文件。"""
    if len(rows) > MAX_EXPORT_ROWS:
        print(f"错误：导出行数过多：{len(rows)}（最大 {MAX_EXPORT_ROWS}）")
        return False

    if rows and max(len(row) for row in rows) > MAX_EXPORT_COLUMNS:
        print(f"错误：导出列数过多：{max(len(row) for row in rows)}（最大 {MAX_EXPORT_COLUMNS}）")
        return False

    return True


def save_table(rows: list[list[str]], output_path: Path) -> bool:
    """保存为 CSV / TSV 文件。"""
    try:
        with open(output_path, "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle, delimiter=detect_delimiter(output_path))
            writer.writerows(rows)
        return True
    except Exception as error:  # pragma: no cover - 文件系统异常
        print(f"错误：保存文件失败：{error}")
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="导出钉钉表格数据")
    parser.add_argument("node_id", help="表格 nodeId 或 https://alidocs.dingtalk.com/i/nodes/{dentryUuid} URL")
    parser.add_argument("output", nargs="?", help="输出路径，默认 `<nodeId>.csv`")
    parser.add_argument("--sheet-id", help="工作表 ID 或名称")
    parser.add_argument("--range", dest="range_value", help="要导出的 A1 范围")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    raw_node_id = args.node_id.strip()
    node_id = extract_node_uuid(raw_node_id) or raw_node_id

    output_path = args.output or f"{node_id}.csv"
    if not validate_output_extension(output_path):
        print(f"错误：不支持的输出类型：{Path(output_path).suffix}")
        print(f"支持的类型：{', '.join(ALLOWED_EXTENSIONS)}")
        sys.exit(1)

    try:
        safe_output = resolve_safe_path(output_path)
    except ValueError as error:
        print(f"错误：{error}")
        sys.exit(1)

    print("开始导出表格数据")
    print(f"   表格：{raw_node_id}")
    print(f"   输出：{safe_output}")
    print("-" * 50)

    print("步骤 1: 读取表格数据...")
    payload = get_range(node_id, sheet_id=args.sheet_id, range_value=args.range_value)
    if payload is None:
        sys.exit(1)

    rows = select_table(payload)
    if not validate_table_shape(rows):
        sys.exit(1)

    print(f"   行数：{len(rows)}")
    print(f"   列数：{max((len(row) for row in rows), default=0)}")

    print("\n步骤 2: 保存到本地文件...")
    if not save_table(rows, safe_output):
        sys.exit(1)

    print("-" * 50)
    print("导出完成。")
    print(f"\n文件路径：{safe_output}")


if __name__ == "__main__":
    main()
