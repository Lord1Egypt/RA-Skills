#!/usr/bin/env python3
"""
mcporter 公共工具函数。

提供 DingTalk 表格 Skill 共享的 mcporter 调用、响应解析、路径安全校验
以及常用表格辅助函数。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

NODE_URL_PATTERN = re.compile(
    r"^https://alidocs\.dingtalk\.com/i/nodes/([a-zA-Z0-9]+)$",
    re.IGNORECASE,
)


def qualify_tool(tool: str) -> str:
    """把简短工具名补全为 `namespace.tool` 形式。"""
    return tool if "." in tool else f"dingtalk-sheets.{tool}"


def run_mcporter(tool: str, args: dict = None, timeout: int = 60) -> Tuple[bool, str]:
    """
    执行 mcporter 命令（使用 `--args` JSON 传参）。

    Args:
        tool: 工具名，可传 `create_workspace_sheet` 或完整名
        args: 参数字典
        timeout: 超时秒数

    Returns:
        (success, output)
    """
    command = ["mcporter", "call", qualify_tool(tool), "--output", "json"]
    if args:
        command.extend(["--args", json.dumps(args, ensure_ascii=False)])

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"命令执行超时（{timeout}秒）"
    except Exception as error:  # pragma: no cover - 保底异常处理
        return False, str(error)


def parse_response(output: str) -> Optional[Any]:
    """解析 mcporter 响应，自动处理嵌套的 `result` 字段。"""
    try:
        data = json.loads(output)
        if isinstance(data, dict) and "result" in data:
            return data["result"]
        return data
    except json.JSONDecodeError:
        return None


def resolve_safe_path(path: str) -> Path:
    """把路径限制在工作区内，防止目录遍历。"""
    allowed_root = Path(os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())).resolve()
    raw_path = Path(path)
    target_path = raw_path.resolve() if raw_path.is_absolute() else (Path.cwd() / raw_path).resolve()

    try:
        target_path.relative_to(allowed_root)
        return target_path
    except ValueError as exc:
        raise ValueError(
            f"路径超出允许范围：{path}\n"
            f"允许根目录：{allowed_root}\n"
            "提示：可通过 OPENCLAW_WORKSPACE 调整允许目录"
        ) from exc


def extract_node_id_from_url(value: str) -> Optional[str]:
    """从钉钉文档 URL 提取 nodeId / dentryUuid。"""
    match = NODE_URL_PATTERN.match(value.strip())
    return match.group(1) if match else None


def extract_node_id(payload: Any) -> Optional[str]:
    """从常见返回结构中提取表格 nodeId。"""
    if isinstance(payload, str):
        return extract_node_id_from_url(payload) or payload

    if not isinstance(payload, dict):
        return None

    for key in ("nodeId", "dentryUuid", "id"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    for key in ("pcUrl", "url", "docUrl", "nodeUrl"):
        value = payload.get(key)
        if isinstance(value, str):
            node_id = extract_node_id_from_url(value)
            if node_id:
                return node_id

    return None


def build_node_url(node_id: str) -> str:
    """把 nodeId 拼成标准文档 URL。"""
    return f"https://alidocs.dingtalk.com/i/nodes/{node_id}"


def find_first_list(payload: Any, candidate_keys: Iterable[str]) -> list:
    """从返回结构中抓取第一个匹配的列表字段。"""
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    for key in candidate_keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value

    for value in payload.values():
        if isinstance(value, list):
            return value

    return []


def extract_sheet_records(payload: Any) -> list:
    """兼容不同返回结构提取工作表列表。"""
    return find_first_list(payload, ("sheets", "sheetList", "items", "data", "rows"))


def sheet_identity(record: Any) -> Tuple[Optional[str], Optional[str]]:
    """提取工作表记录中的 (sheet_id, name)。"""
    if not isinstance(record, dict):
        return None, None

    sheet_id = None
    for key in ("sheetId", "id"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            sheet_id = value.strip()
            break

    name = None
    for key in ("name", "title", "sheetName"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            name = value.strip()
            break

    return sheet_id, name


def find_sheet_record(payload: Any, token: str) -> Optional[dict]:
    """按工作表 ID 或名称查找记录。"""
    token = token.strip()
    for record in extract_sheet_records(payload):
        sheet_id, name = sheet_identity(record)
        if token in {sheet_id, name}:
            return record
    return None


def column_number_to_name(index: int) -> str:
    """把 1-based 列号转成 A1 表示法列名。"""
    if index < 1:
        raise ValueError("列号必须 >= 1")

    result = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result.append(chr(ord("A") + remainder))
    return "".join(reversed(result))


def matrix_range_address(row_count: int, column_count: int, start_row: int = 1, start_column: int = 1) -> str:
    """根据矩阵尺寸生成 A1 表示法地址。"""
    if row_count < 1 or column_count < 1:
        raise ValueError("行数和列数都必须 >= 1")

    start_col = column_number_to_name(start_column)
    end_col = column_number_to_name(start_column + column_count - 1)
    end_row = start_row + row_count - 1
    return f"{start_col}{start_row}:{end_col}{end_row}"


def normalize_table(rows: list[list[str]]) -> list[list[str]]:
    """把不等长二维数组补齐成矩形。"""
    if not rows:
        return rows

    width = max(len(row) for row in rows)
    return [row + [""] * (width - len(row)) for row in rows]


def extract_range_payload(payload: Any) -> dict:
    """从 get_range 返回中提取核心数据块。"""
    if not isinstance(payload, dict):
        return {}

    if any(key in payload for key in ("values", "displayValues", "formulas")):
        return payload

    for key in ("data", "range", "result"):
        value = payload.get(key)
        if isinstance(value, dict) and any(inner in value for inner in ("values", "displayValues", "formulas")):
            return value

    return payload


def _coerce_non_negative_int(value: Any) -> int:
    """把工作表返回中的行列值规范成非负整数。"""
    if isinstance(value, int):
        return max(value, 0)

    if isinstance(value, str):
        try:
            return max(int(value.strip()), 0)
        except ValueError:
            return 0

    return 0


def extract_sheet_position(payload: Any) -> Tuple[int, int]:
    """提取最后非空行列位置；缺失时回退为 0。"""
    if not isinstance(payload, dict):
        return 0, 0

    last_row = _coerce_non_negative_int(payload.get("lastNonEmptyRow"))
    last_column = _coerce_non_negative_int(payload.get("lastNonEmptyColumn"))
    return last_row, last_column


def append_rows_with_update_range(
    node_id: str,
    sheet_id: str,
    values: list[list[str]],
    timeout: int = 60,
) -> Tuple[bool, dict]:
    """
    用 `get_sheet + update_range` 模拟末尾追加。

    当前 skill 默认不直接调用 `append_rows`，以规避上游服务不稳定。
    未来若要恢复原生 `append_rows`，可把 `writeMode`
    设为 `native`，并在调用侧恢复直接透传。
    """
    normalized_values = normalize_table(values)
    if not normalized_values:
        return False, {"error": "没有可追加的数据"}

    sheet_success, sheet_output = run_mcporter(
        "get_sheet",
        {"nodeId": node_id, "sheetId": sheet_id},
        timeout=timeout,
    )
    if not sheet_success:
        return False, {"error": sheet_output}

    sheet_payload = parse_response(sheet_output)
    if not isinstance(sheet_payload, dict):
        return False, {"error": f"解析工作表详情失败：{sheet_output}"}

    last_row, _ = extract_sheet_position(sheet_payload)
    start_row = last_row + 1 if last_row > 0 else 1
    range_address = matrix_range_address(
        len(normalized_values),
        len(normalized_values[0]),
        start_row=start_row,
    )

    update_success, update_output = run_mcporter(
        "update_range",
        {
            "nodeId": node_id,
            "sheetId": sheet_id,
            "rangeAddress": range_address,
            "values": normalized_values,
        },
        timeout=timeout,
    )
    if not update_success:
        return False, {"error": update_output, "rangeAddress": range_address}

    update_payload = parse_response(update_output)
    if update_payload is None:
        return False, {"error": f"解析写入响应失败：{update_output}", "rangeAddress": range_address}

    return True, {
        "rangeAddress": range_address,
        "result": update_payload,
        "writeMode": "update_range",
    }
