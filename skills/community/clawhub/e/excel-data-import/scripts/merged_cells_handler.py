#!/usr/bin/env python3
from typing import Any
# -*- coding: utf-8 -*-
"""
合并单元格处理器

功能：处理 Excel 中的合并单元格
"""


def get_merged_ranges(ws) -> Any:
    """获取工作表中所有合并单元格区域

    Args:
        ws: openpyxl Worksheet 对象

    Returns:
        list: 合并单元格区域列表
    """
    return list(ws.merged_cells.ranges)


def handle_merged_cells(ws, merged_ranges) -> Any:
    """处理合并单元格（保持合并结构）

    Args:
        ws: openpyxl Worksheet 对象
        merged_ranges: 合并单元格区域列表

    Returns:
        list: 合并单元格区域列表（已处理）
    """
    # openpyxl 会自动保持合并单元格结构
    # 这里我们只需要确保不破坏它们

    # 记录合并单元格信息（用于调试）
    merged_info = []
    for merged_range in merged_ranges:
        merged_info.append(
            {
                "range": str(merged_range),
                "min_row": merged_range.min_row,
                "max_row": merged_range.max_row,
                "min_col": merged_range.min_col,
                "max_col": merged_range.max_col,
            }
        )

    return merged_info


def is_cell_merged(cell, merged_ranges) -> Any:
    """检查单元格是否在合并区域内

    Args:
        cell: openpyxl Cell 对象
        merged_ranges: 合并单元格区域列表

    Returns:
        bool: 是否在合并区域内
    """
    for merged_range in merged_ranges:
        if (
            merged_range.min_row <= cell.row <= merged_range.max_row
            and merged_range.min_col <= cell.column <= merged_range.max_col
        ):
            return True

    return False
