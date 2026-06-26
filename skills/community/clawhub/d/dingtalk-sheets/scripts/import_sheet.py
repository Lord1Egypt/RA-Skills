#!/usr/bin/env python3
"""
从本地 CSV / TSV 文件导入到钉钉表格。

默认行为：创建一个新表格并把数据写入第一个工作表。
也可以通过 `--node-id` 把数据写入已有表格。
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Optional

from mcporter_utils import (
    APPEND_ROWS_MODE,
    append_rows_with_update_range,
    build_node_url,
    extract_node_id,
    extract_sheet_records,
    find_sheet_record,
    matrix_range_address,
    normalize_table,
    parse_response,
    resolve_safe_path,
    run_mcporter,
    sheet_identity,
)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_ROWS = 5000
MAX_COLUMNS = 200
ALLOWED_EXTENSIONS = [".csv", ".tsv"]


def validate_file_extension(filename: str) -> bool:
    """校验导入文件后缀。"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def validate_file_size(path: Path) -> bool:
    """校验导入文件大小。"""
    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        print(f"错误：文件过大：{size / 1024 / 1024:.2f}MB（最大 {MAX_FILE_SIZE / 1024 / 1024:.0f}MB）")
        return False
    return True


def detect_delimiter(path: Path) -> str:
    """按扩展名推断分隔符。"""
    return "\t" if path.suffix.lower() == ".tsv" else ","


def read_table(path: Path) -> list[list[str]]:
    """读取 CSV / TSV 内容。"""
    if not validate_file_size(path):
        sys.exit(1)

    delimiter = detect_delimiter(path)
    encodings = ("utf-8-sig", "utf-8", "gbk")
    last_error = None

    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding, newline="") as handle:
                rows = [[cell for cell in row] for row in csv.reader(handle, delimiter=delimiter)]
            return rows
        except UnicodeDecodeError as error:
            last_error = error

    print(f"错误：读取文件失败：{last_error}")
    sys.exit(1)


def ensure_table_shape(rows: list[list[str]]) -> list[list[str]]:
    """限制最大行列数并补齐矩阵。"""
    if not rows:
        print("错误：导入文件为空，没有可写入的数据")
        sys.exit(1)

    if len(rows) > MAX_ROWS:
        print(f"错误：行数过多：{len(rows)}（最大 {MAX_ROWS}）")
        sys.exit(1)

    width = max(len(row) for row in rows)
    if width < 1:
        print("错误：导入文件为空，没有可写入的数据")
        sys.exit(1)

    if width > MAX_COLUMNS:
        print(f"错误：列数过多：{width}（最大 {MAX_COLUMNS}）")
        sys.exit(1)

    return normalize_table(rows)


def create_workspace_sheet(name: str, folder_id: Optional[str], workspace_id: Optional[str]) -> Optional[dict]:
    args = {"name": name}
    if folder_id:
        args["folderId"] = folder_id
    if workspace_id:
        args["workspaceId"] = workspace_id

    success, output = run_mcporter("create_workspace_sheet", args)
    if not success:
        print(f"错误：创建表格失败：{output}")
        return None

    return parse_response(output)


def get_all_sheets(node_id: str) -> Optional[object]:
    success, output = run_mcporter("get_all_sheets", {"nodeId": node_id})
    if not success:
        print(f"错误：获取工作表列表失败：{output}")
        return None
    return parse_response(output)


def create_sheet_tab(node_id: str, name: str) -> Optional[dict]:
    success, output = run_mcporter("create_sheet", {"nodeId": node_id, "name": name})
    if not success:
        print(f"错误：创建工作表失败：{output}")
        return None
    return parse_response(output)


def resolve_target_sheet(node_id: str, sheet_id: Optional[str], sheet_name: Optional[str]) -> Optional[str]:
    """解析目标工作表；必要时自动创建。"""
    if sheet_id:
        return sheet_id

    sheets_payload = get_all_sheets(node_id)
    if sheets_payload is None:
        return None

    if sheet_name:
        matched = find_sheet_record(sheets_payload, sheet_name)
        if matched:
            matched_id, _ = sheet_identity(matched)
            return matched_id or sheet_name

        created = create_sheet_tab(node_id, sheet_name)
        if created is None:
            return None

        created_id = None
        if isinstance(created, dict):
            created_id = created.get("sheetId") or created.get("id")
        if created_id:
            return created_id

        sheets_payload = get_all_sheets(node_id)
        if sheets_payload is None:
            return None
        matched = find_sheet_record(sheets_payload, sheet_name)
        if matched:
            matched_id, _ = sheet_identity(matched)
            return matched_id or sheet_name

        return sheet_name

    records = extract_sheet_records(sheets_payload)
    if not records:
        print("错误：当前表格没有可用的工作表")
        return None

    first_id, first_name = sheet_identity(records[0])
    return first_id or first_name


def update_range(node_id: str, sheet_id: str, values: list[list[str]]) -> Optional[dict]:
    range_address = matrix_range_address(len(values), len(values[0]))
    args = {
        "nodeId": node_id,
        "sheetId": sheet_id,
        "rangeAddress": range_address,
        "values": values,
    }

    success, output = run_mcporter("update_range", args)
    if not success:
        print(f"错误：写入表格失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"错误：解析响应失败：{output}")
        return None
    return {"rangeAddress": range_address, "result": result}


def append_rows(node_id: str, sheet_id: str, values: list[list[str]]) -> Optional[dict]:
    success, result = append_rows_with_update_range(node_id, sheet_id, values)
    if not success:
        print(f"错误：追加数据失败：{result.get('error')}")
        return None

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="导入本地 CSV / TSV 文件到钉钉表格")
    parser.add_argument("source", help="本地 CSV / TSV 文件路径")
    parser.add_argument("title", nargs="?", help="新表格标题；不传时默认使用文件名")
    parser.add_argument("--node-id", help="已有表格的 nodeId 或 URL；传入后不再新建表格")
    parser.add_argument("--sheet-id", help="目标工作表 ID")
    parser.add_argument("--sheet-name", help="目标工作表名称；不存在时会自动新建")
    parser.add_argument("--folder-id", help="创建新表格时的目标文件夹 ID 或链接 URL")
    parser.add_argument("--workspace-id", help="创建新表格时的目标知识库 ID")
    parser.add_argument(
        "--append",
        action="store_true",
        help="按追加模式写入；当前会使用 get_sheet + update_range 模拟末尾追加",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not validate_file_extension(args.source):
        print(f"错误：不支持的文件类型：{Path(args.source).suffix}")
        print(f"支持的类型：{', '.join(ALLOWED_EXTENSIONS)}")
        sys.exit(1)

    try:
        source_path = resolve_safe_path(args.source)
    except ValueError as error:
        print(f"错误：{error}")
        sys.exit(1)

    if not source_path.exists():
        print(f"错误：文件不存在：{source_path}")
        sys.exit(1)

    title = args.title or source_path.stem

    print(f"开始导入表格数据：{source_path.name}")
    print("-" * 50)

    print("步骤 1: 读取本地数据...")
    rows = ensure_table_shape(read_table(source_path))
    print(f"   行数：{len(rows)}")
    print(f"   列数：{len(rows[0])}")

    node_id = args.node_id
    if not node_id:
        print("\n步骤 2: 创建目标表格...")
        create_result = create_workspace_sheet(title, args.folder_id, args.workspace_id)
        if create_result is None:
            sys.exit(1)

        node_id = extract_node_id(create_result)
        if not node_id:
            print("错误：无法从创建结果里提取 nodeId")
            print(json.dumps(create_result, ensure_ascii=False, indent=2))
            sys.exit(1)
        print(f"创建成功：{build_node_url(node_id)}")
    else:
        print("\n步骤 2: 使用已有表格...")
        print(f"目标表格：{node_id}")

    print("\n步骤 3: 解析目标工作表...")
    sheet_id = resolve_target_sheet(node_id, args.sheet_id, args.sheet_name)
    if not sheet_id:
        sys.exit(1)
    print(f"目标工作表：{sheet_id}")

    print("\n步骤 4: 写入数据...")
    if args.append:
        print(f"   追加策略：{APPEND_ROWS_MODE}（暂不直连 append_rows）")
        write_result = append_rows(node_id, sheet_id, rows)
        if write_result is None:
            sys.exit(1)
        print("数据追加成功")
        appended_range = write_result.get("rangeAddress")
        if appended_range:
            print(f"   追加范围：{appended_range}")
    else:
        write_result = update_range(node_id, sheet_id, rows)
        if write_result is None:
            sys.exit(1)
        print("数据写入成功")
        print(f"   写入范围：{write_result['rangeAddress']}")

    print("-" * 50)
    print("导入完成。")
    print(f"\n表格链接：{build_node_url(node_id)}")


if __name__ == "__main__":
    main()
