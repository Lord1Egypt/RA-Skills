#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作表分析器

功能：分析 Excel 工作表结构，识别合并单元格、表头位置、数据区域
支持多层合并表头的自动检测和展开
"""

from typing import Any, Dict, List, Optional


# 常见表头关键词（中文）
HEADER_KEYWORDS = [
    '姓名', '名字', '学号', '学籍号', '编号', 'ID',
    '身份证', '证件', '手机', '电话', '联系方式',
    '部门', '科室', '班级', '年级',
    '日期', '时间', '年份', '月份',
    '地址', '位置', '备注', '说明',
    '语文', '数学', '英语', '物理', '化学', '生物',
    '政治', '历史', '地理', '思品', '道德',
    '工号', '出勤', '合计', '总分',
]


def detect_header_row(ws, max_check_rows=15, min_fields=3) -> Dict[str, Any]:
    """自动检测表头行（支持多层合并表头）

    策略：
    1. 检查前N行，排除完全空白行
    2. 对每行计算得分（唯一字段数 + 关键词匹配 + 合并单元格惩罚 + 数据特征判断）
    3. 选择得分最高的行作为表头

    对于多层表头，会返回**最后一行**表头的行号（因为用户在配置中
    通常需要指向包含具体列名的行），同时 header_depth 会标明表头层数。

    Returns:
        {
            'header_row': 最后一行表头的行号,
            'header_depth': 表头层数（如2表示2行表头）,
            'data_start_row': 数据起始行号,
            'confidence': 置信度（0-1）,
            'reason': 检测原因
        }
    """
    if not ws or ws.max_row < 1:
        return {
            'header_row': 1, 'header_depth': 1,
            'data_start_row': 2, 'confidence': 0.0,
            'reason': '工作表为空'
        }

    check_range = min(max_check_rows, ws.max_row)
    merged_ranges = list(ws.merged_cells.ranges)

    # 获取每个合并区域覆盖的行集合
    merged_row_spans = []
    for mr in merged_ranges:
        merged_row_spans.append((mr.min_row, mr.max_row, mr.min_col, mr.max_col))

    # 为每行打分
    row_scores = []
    for row_idx in range(1, check_range + 1):
        row = ws[row_idx]

        unique_fields = set()
        keyword_matches = 0
        merged_cells = 0
        non_empty_count = 0

        for col_idx, cell in enumerate(row, start=1):
            if cell.value is not None:
                value_str = str(cell.value).strip()
                if value_str:
                    non_empty_count += 1
                    unique_fields.add(value_str)

                    for keyword in HEADER_KEYWORDS:
                        if keyword in value_str:
                            keyword_matches += 1
                            break

                    for mr in merged_ranges:
                        if cell.coordinate in mr:
                            merged_cells += 1
                            break

        if non_empty_count == 0:
            continue
        if len(unique_fields) < min_fields:
            continue

        # 计算得分
        score = 0
        score += len(unique_fields) * 40
        score += keyword_matches * 30
        score -= merged_cells * 20

        # 数据特征判断：纯数字行大幅降权
        is_likely_data = all(
            f.replace('.', '').replace('-', '').replace(',', '').isdigit()
            for f in unique_fields
        )
        # ID/编号格式的字段密度检测
        id_like_count = sum(1 for f in unique_fields
                          if f.replace('.','').replace('-','').replace(',','').isdigit()
                          or (f.startswith('E') and len(f) <= 10 and f[1:].replace('.','').isdigit()))
        # 超过一半字段像ID/数字，则视为数据行
        if len(unique_fields) > 0 and id_like_count / len(unique_fields) > 0.5:
            is_likely_data = True

        if is_likely_data:
            score -= 80  # 大幅降权
        else:
            score += 10

        # 关键词匹配加分增强（含关键词的行更可能是表头）
        if keyword_matches >= 2:
            score += keyword_matches * 20  # 额外加分

        row_scores.append({
            'row_num': row_idx,
            'score': score,
            'field_count': len(unique_fields),
            'keyword_count': keyword_matches,
            'merged_count': merged_cells,
            'is_data': is_likely_data,
            'non_empty_count': non_empty_count,
        })

    if not row_scores:
        return {
            'header_row': 1, 'header_depth': 1,
            'data_start_row': 2, 'confidence': 0.0,
            'reason': '未检测到有效表头'
        }

    # 找到得分最高的行
    best = max(row_scores, key=lambda r: r['score'])

    # 检查是否有合并单元格从 best 行延伸到下一行
    # 如果有，说明下一行是二级表头，应该选择下一行
    for mr in merged_ranges:
        if mr.min_row == best['row_num'] and mr.max_row > best['row_num']:
            # 找到下一行的得分
            next_row_score = next((r for r in row_scores if r['row_num'] == mr.max_row), None)
            if next_row_score:
                # 如果下一行也有较多字段，选择它作为主表头行
                if next_row_score['non_empty_count'] >= 2:
                    best = next_row_score
            break

    # 检测表头层数：向上查找连续的表头行
    header_depth = 1
    best_row = best['row_num']
    for rs in row_scores:
        if rs['row_num'] == best_row - header_depth:
            # 上一行如果是表头特征（合并单元格覆盖了当前行，或也是关键词行）
            spans_down = False
            for mr in merged_ranges:
                if mr.min_row <= rs['row_num'] and mr.max_row >= best_row:
                    spans_down = True
                    break
            # 如果上一行合并到了当前行，或者是纯文本行（非纯数据），也算表头
            if spans_down or (not rs['is_data'] and rs['non_empty_count'] >= 2):
                header_depth += 1
            else:
                break

    first_header_row = best_row - header_depth + 1
    data_start = best_row + 1

    # 置信度
    if best['is_data']:
        confidence = min(best['score'] / 100, 0.4)
    else:
        confidence = min(best['score'] / 100, 1.0)

    reasons = []
    if best['keyword_count'] > 0:
        reasons.append(f"包含{best['keyword_count']}个关键词")
    if best['field_count'] >= 5:
        reasons.append(f"{best['field_count']}个字段")
    reasons.append(f"表头{header_depth}层")

    return {
        'header_row': best_row,
        'header_depth': header_depth,
        'first_header_row': first_header_row,
        'data_start_row': data_start,
        'confidence': confidence,
        'reason': ' | '.join(reasons) if reasons else "默认选择"
    }


def read_headers_with_merged(ws, header_row: int, max_col: int,
                              first_header_row: Optional[int] = None) -> Dict[str, int]:
    """读取表头，支持合并单元格展开

    对于多层表头，从 first_header_row 到 header_row 逐行读取，
    合并单元格的值会被分配到其覆盖的所有列。
    最终以 header_row（最详细的列名行）为主，上层合并值作为分组前缀。

    Args:
        ws: 工作表
        header_row: 主表头行号（包含具体列名的最后一行）
        max_col: 最大列数
        first_header_row: 第一行表头（默认等于 header_row）

    Returns:
        dict: {列名: 列号}
    """
    if first_header_row is None:
        first_header_row = header_row

    merged_ranges = list(ws.merged_cells.ranges)

    # 构建合并单元格映射: (row, col) -> 实际值
    merged_value_map = {}
    for mr in merged_ranges:
        # 只处理在表头范围内的合并
        if mr.min_row > header_row or mr.max_row < first_header_row:
            continue
        # 读取合并区域左上角的值
        top_left_value = ws.cell(row=mr.min_row, column=mr.min_col).value
        if top_left_value is not None:
            top_left_value = str(top_left_value).strip()
        else:
            top_left_value = ""
        # 记录合并区域覆盖的所有单元格
        for r in range(mr.min_row, mr.max_row + 1):
            for c in range(mr.min_col, mr.max_col + 1):
                if (r, c) not in merged_value_map:
                    merged_value_map[(r, c)] = top_left_value

    # 读取主表头行的列名
    headers = {}
    for col in range(1, max_col + 1):
        # 优先读取主表头行的值
        value = None
        cell = ws.cell(row=header_row, column=col)
        if cell.value is not None:
            value = str(cell.value).strip()
        elif (header_row, col) in merged_value_map:
            value = merged_value_map[(header_row, col)]

        if value:
            headers[value] = col

    return headers


def analyze_worksheet(ws, header_row: int, first_header_row: Optional[int] = None) -> Dict[str, Any]:
    """分析工作表结构

    Args:
        ws: openpyxl Worksheet 对象
        header_row: 表头行号（最后一行表头）
        first_header_row: 第一行表头（多层表头时的第一行）

    Returns:
        dict: 工作表结构信息
    """
    if first_header_row is None:
        first_header_row = header_row

    data_range = find_data_range(ws, header_row)
    headers = read_headers_with_merged(ws, header_row, data_range["max_col"], first_header_row)
    merged_count = len(ws.merged_cells.ranges)

    return {
        "total_rows": data_range["max_row"],
        "max_col": data_range["max_col"],
        "header_row": header_row,
        "first_header_row": first_header_row,
        "data_start_row": header_row + 1,
        "headers": headers,
        "merged_cells_count": merged_count,
        "data_range": data_range,
    }


def find_data_range(ws, header_row: int) -> Dict[str, Any]:
    """查找数据范围

    Args:
        ws: openpyxl Worksheet 对象
        header_row: 表头行号

    Returns:
        dict: {max_row: 实际最后一行, max_col: 最大列数}
    """
    # 先从表头行确定列数
    max_col = 1
    for col in range(1, ws.max_column + 1):
        cell = ws.cell(row=header_row, column=col)
        if cell.value is not None and str(cell.value).strip() != "":
            max_col = col

    # 也检查合并单元格延伸到的列
    for mr in ws.merged_cells.ranges:
        if mr.min_row <= header_row <= mr.max_row:
            max_col = max(max_col, mr.max_col)

    # 扫描数据行，找到实际最后一行
    actual_max_row = header_row
    data_start = header_row + 1
    for row in range(data_start, ws.max_row + 1):
        row_has_data = False
        for col in range(1, max_col + 1):
            cell = ws.cell(row=row, column=col)
            if cell.value is not None and str(cell.value).strip() != "":
                row_has_data = True
        if row_has_data:
            actual_max_row = row

    return {"max_row": actual_max_row, "max_col": max_col}
