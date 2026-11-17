"""表格数据整形：把载荷里的表变成矩阵、表头跨列、强调行与列宽。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这些函数只吃
表格载荷、吐数据结构，不创建任何 Flowable——所以能单独测试，
也能被别的渲染路径复用。
"""

from __future__ import annotations

import re
from typing import Any


class TableDataError(RuntimeError):
    """表格载荷不合法。

    以前抛的是 scripts 层的 SkillError；包不该依赖 scripts，所以这里
    自己定义。调用侧把它翻译回 SkillError，对外行为不变。
    """


def _cell_text(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(
            cell.get("translation")
            or cell.get("target")
            or cell.get("text")
            or cell.get("value")
            or ""
        )
    return str(cell or "")


def _table_matrix(table: dict[str, Any]) -> tuple[list[list[str]], list[tuple]]:
    spans: list[tuple] = []
    rows_value = table.get("rows")
    if isinstance(rows_value, list) and rows_value:
        matrix = [
            [_cell_text(cell) for cell in row]
            for row in rows_value
            if isinstance(row, list)
        ]
        if matrix:
            width = max(len(row) for row in matrix)
            matrix = [row + [""] * (width - len(row)) for row in matrix]
            spans.extend(_table_header_spans(table, matrix))
            return matrix, spans

    row_count = int(table.get("row_count") or 0)
    column_count = int(table.get("column_count") or 0)
    cells = table.get("cells")
    if row_count < 1 or column_count < 1 or not isinstance(cells, list):
        raise TableDataError("结构化表格缺少有效行列和单元格")
    matrix = [["" for _ in range(column_count)] for _ in range(row_count)]
    sequential = not any(
        isinstance(cell, dict)
        and any(key in cell for key in ("row", "column", "col"))
        for cell in cells
    )
    for index, cell in enumerate(cells):
        if sequential:
            row = index // column_count
            column = index % column_count
        elif isinstance(cell, dict):
            row = int(cell.get("row") or 0)
            column = int(cell.get("column", cell.get("col", 0)) or 0)
            if row >= row_count or column >= column_count:
                row -= 1
                column -= 1
        else:
            continue
        if not 0 <= row < row_count or not 0 <= column < column_count:
            continue
        matrix[row][column] = _cell_text(cell)
        if isinstance(cell, dict):
            row_span = int(cell.get("row_span") or 1)
            col_span = int(cell.get("col_span") or 1)
            if row_span > 1 or col_span > 1:
                spans.append(
                    (
                        "SPAN",
                        (column, row),
                        (
                            min(column_count - 1, column + col_span - 1),
                            min(row_count - 1, row + row_span - 1),
                        ),
                    )
                )
    spans.extend(_table_header_spans(table, matrix))
    return matrix, spans


def _table_header_spans(
    table: dict[str, Any],
    matrix: list[list[str]],
) -> list[tuple]:
    structure = table.get("header_structure")
    if not isinstance(structure, dict) or not matrix:
        return []
    merged_cells = structure.get("merged_cells")
    if not isinstance(merged_cells, list):
        return []
    row_count = len(matrix)
    column_count = len(matrix[0])
    spans: list[tuple] = []
    for cell in merged_cells:
        if not isinstance(cell, dict):
            continue
        try:
            row = int(cell.get("row", 0))
            column = int(cell.get("column", cell.get("col", 0)))
            row_span = max(1, int(cell.get("row_span", 1)))
            col_span = max(1, int(cell.get("col_span", 1)))
        except (TypeError, ValueError):
            continue
        if not 0 <= row < row_count or not 0 <= column < column_count:
            continue
        if row_span == 1 and col_span == 1:
            continue
        spans.append(
            (
                "SPAN",
                (column, row),
                (
                    min(column_count - 1, column + col_span - 1),
                    min(row_count - 1, row + row_span - 1),
                ),
            )
        )
    return spans


def _table_emphasis_rows(
    table: dict[str, Any],
    *,
    row_count: int,
    header_rows: int,
) -> set[int]:
    result: set[int] = set()
    for value in table.get("bold_rows", []):
        if isinstance(value, int) and 0 <= value < row_count:
            result.add(value)
    semantics = table.get("style_semantics")
    if not isinstance(semantics, dict):
        return result
    data_rows = (
        semantics.get("bold_data_rows")
        or semantics.get("excluded_data_rows")
        or []
    )
    for value in data_rows:
        if not isinstance(value, int):
            continue
        row_index = header_rows + value - 1
        if 0 <= row_index < row_count:
            result.add(row_index)
    return result


def _table_note_text(raw_note: Any) -> str:
    if not isinstance(raw_note, dict):
        return str(raw_note).strip()
    note = str(
        raw_note.get("translation")
        or raw_note.get("text")
        or raw_note.get("note")
        or ""
    ).strip()
    marker = str(raw_note.get("marker") or "").strip()
    if marker and note and not note.startswith(marker):
        return f"{marker}　{note}"
    return note


def _column_widths(
    matrix: list[list[str]],
    total_width: float,
    configured_weights: Any = None,
) -> list[float]:
    columns = len(matrix[0])
    if (
        isinstance(configured_weights, list)
        and len(configured_weights) == columns
        and all(
            isinstance(weight, (int, float)) and float(weight) > 0
            for weight in configured_weights
        )
    ):
        total_weight = sum(map(float, configured_weights))
        return [
            total_width * float(weight) / total_weight
            for weight in configured_weights
        ]
    minimum_weight = 12.0 if columns <= 4 else 4.0
    weights = []
    for column in range(columns):
        longest = max(
            len(re.sub(r"\s+", "", row[column]))
            for row in matrix
        )
        weights.append(max(minimum_weight, min(float(longest), 34.0)))
    minimum = max(34.0, total_width / max(columns * 2.8, 1))
    raw_total = sum(weights)
    widths = [
        max(minimum, total_width * weight / raw_total)
        for weight in weights
    ]
    scale = total_width / sum(widths)
    return [width * scale for width in widths]

