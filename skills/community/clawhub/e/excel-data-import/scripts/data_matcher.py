#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据匹配引擎

功能：基于关键字段匹配数据行
"""

from typing import Any


def find_matching_row(key_value, target_ws, target_headers, key_field, start_row, end_row) -> Any:
    """在目标表中查找匹配的行

    Args:
        key_value: 关键字段的值
        target_ws: 目标工作表
        target_headers: 目标表头字典 {列名: 列号}
        key_field: 关键字段名称
        start_row: 起始行号
        end_row: 结束行号

    Returns:
        int: 匹配的行号，如果未找到返回 None
    """
    if key_value is None:
        return None

    # 从表头字典中查找关键字段的列号
    key_col = target_headers.get(key_field)

    if not key_col:
        # 如果未找到关键字段，返回 None
        return None

    for row in range(start_row, end_row + 1):
        cell_value = target_ws.cell(row=row, column=key_col).value

        # 精确匹配（去除空格）
        if cell_value and str(cell_value).strip() == str(key_value).strip():
            return row

    # 未找到匹配
    return None
