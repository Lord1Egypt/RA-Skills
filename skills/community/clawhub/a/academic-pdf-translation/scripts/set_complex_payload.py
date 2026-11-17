from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import SkillError, load_json, write_json


def _localized_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return ""
    return str(
        value.get("translation")
        or value.get("target")
        or value.get("localized")
        or value.get("label")
        or value.get("text")
        or ""
    ).strip()


def _validate_table_contract(table: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    label = f"tables[{index}]"
    rows = table.get("rows")
    row_count = table.get("row_count")
    column_count = table.get("column_count")
    inferred_rows = 0
    inferred_columns = 0
    if isinstance(rows, list):
        inferred_rows = len(rows)
        lengths: list[int] = []
        for row_index, row in enumerate(rows):
            if not isinstance(row, list):
                errors.append(f"{label}.rows[{row_index}] 必须是数组")
                continue
            lengths.append(len(row))
            if not any(_localized_text(cell) for cell in row):
                errors.append(f"{label}.rows[{row_index}] 不能整行为空")
        if lengths:
            inferred_columns = lengths[0]
            if any(length != inferred_columns for length in lengths):
                errors.append(f"{label}.rows 必须是规则矩阵")
        if inferred_rows < 2 or inferred_columns < 2:
            errors.append(f"{label}.rows 至少需要两行两列")
    if isinstance(row_count, int) and row_count > 0:
        if inferred_rows and row_count != inferred_rows:
            errors.append(f"{label}.row_count 与 rows 实际行数不一致")
    elif row_count is not None:
        errors.append(f"{label}.row_count 必须是正整数")
    if isinstance(column_count, int) and column_count > 0:
        if inferred_columns and column_count != inferred_columns:
            errors.append(f"{label}.column_count 与 rows 实际列数不一致")
    elif column_count is not None:
        errors.append(f"{label}.column_count 必须是正整数")

    effective_rows = (
        row_count if isinstance(row_count, int) and row_count > 0 else inferred_rows
    )
    effective_columns = (
        column_count
        if isinstance(column_count, int) and column_count > 0
        else inferred_columns
    )
    cells = table.get("cells")
    if isinstance(cells, list):
        coordinates: set[tuple[int, int]] = set()
        for cell_index, cell in enumerate(cells):
            if not isinstance(cell, dict):
                errors.append(f"{label}.cells[{cell_index}] 必须是对象")
                continue
            row = cell.get("row")
            column = cell.get("column")
            if (
                isinstance(row, bool)
                or not isinstance(row, int)
                or row < 0
                or isinstance(column, bool)
                or not isinstance(column, int)
                or column < 0
            ):
                errors.append(
                    f"{label}.cells[{cell_index}] 缺少有效 row/column"
                )
                continue
            coordinate = (row, column)
            if coordinate in coordinates:
                errors.append(f"{label}.cells 坐标重复: {coordinate}")
            coordinates.add(coordinate)
            if effective_rows and row >= effective_rows:
                errors.append(f"{label}.cells[{cell_index}] 行坐标越界")
            if effective_columns and column >= effective_columns:
                errors.append(f"{label}.cells[{cell_index}] 列坐标越界")
        if rows and effective_rows and effective_columns:
            expected = effective_rows * effective_columns
            if len(coordinates) not in {0, expected}:
                errors.append(
                    f"{label}.cells 必须为空或完整覆盖 {expected} 个坐标"
                )
    return errors


def _axis_text(axis: Any, key: str) -> str:
    return (
        str(axis.get(key) or "").strip()
        if isinstance(axis, dict)
        else ""
    )


def _validate_series(
    series: Any,
    *,
    label: str,
    expected_values: int | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(series, list) or not series:
        return [f"{label} 必须包含非空 series"]
    for index, item in enumerate(series):
        item_label = f"{label}.series[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_label} 必须是对象")
            continue
        if not _localized_text(item):
            errors.append(f"{item_label} 缺少目标语言名称")
        values = item.get("values")
        if not isinstance(values, list) or not values or not all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in values
        ):
            errors.append(f"{item_label}.values 必须是非空数值数组")
        elif expected_values is not None and len(values) != expected_values:
            errors.append(
                f"{item_label}.values 数量与横轴类别数量不一致"
            )
    return errors


def _validate_vector_contract(
    figure: dict[str, Any],
    index: int,
) -> list[str]:
    errors: list[str] = []
    label = f"figures[{index}]"
    figure_type = str(figure.get("type") or "").strip().lower()
    if not figure_type:
        errors.append(f"{label}.type 不能为空")

    nodes = figure.get("nodes")
    node_ids: set[str] = set()
    if isinstance(nodes, list):
        for node_index, node in enumerate(nodes):
            node_label = f"{label}.nodes[{node_index}]"
            if not isinstance(node, dict):
                errors.append(f"{node_label} 必须是对象")
                continue
            node_id = str(node.get("id") or "").strip()
            if not node_id:
                errors.append(f"{node_label}.id 不能为空")
            elif node_id in node_ids:
                errors.append(f"{label}.nodes ID 重复: {node_id}")
            else:
                node_ids.add(node_id)
            if not _localized_text(node):
                errors.append(f"{node_label} 缺少目标语言文字")

    edges = figure.get("edges")
    if isinstance(edges, list):
        for edge_index, edge in enumerate(edges):
            edge_label = f"{label}.edges[{edge_index}]"
            if not isinstance(edge, dict):
                errors.append(f"{edge_label} 必须是对象")
                continue
            source = str(edge.get("source") or edge.get("from") or "").strip()
            target = str(edge.get("target") or edge.get("to") or "").strip()
            if not source or not target:
                errors.append(f"{edge_label} 缺少 source/target")
                continue
            if node_ids and source not in node_ids:
                errors.append(f"{edge_label}.source 不存在: {source}")
            if node_ids and target not in node_ids:
                errors.append(f"{edge_label}.target 不存在: {target}")

    directed = (
        figure_type.startswith("directed-")
        or figure_type
        in {
            "confirmatory-factor-analysis-model",
            "moderated-directed-model",
            "moderated-mediation-model",
            "cycle",
        }
    )
    if directed:
        if not node_ids:
            errors.append(f"{label} 的定向模型必须包含 nodes")
        if not isinstance(edges, list) or not edges:
            errors.append(f"{label} 的定向模型必须包含 edges")

    panels = figure.get("panels")
    shapes: list[dict[str, Any]] = [
        shape
        for shape in figure.get("shapes", [])
        if isinstance(shape, dict)
    ] if isinstance(figure.get("shapes"), list) else []
    if isinstance(panels, list):
        for panel in panels:
            if not isinstance(panel, dict):
                continue
            panel_shapes = panel.get("shapes")
            if isinstance(panel_shapes, list):
                shapes.extend(
                    shape
                    for shape in panel_shapes
                    if isinstance(shape, dict)
                )
    if any(
        str(shape.get("type") or "").lower() == "quadrant"
        for shape in shapes
    ):
        axes = figure.get("axis_labels")
        if not isinstance(axes, dict):
            errors.append(f"{label} 的四象限图必须包含 axis_labels")
        else:
            for axis_name in ("horizontal", "vertical"):
                axis = axes.get(axis_name)
                for key in ("dimension", "negative", "positive", "direction"):
                    if not _axis_text(axis, key):
                        errors.append(
                            f"{label}.axis_labels.{axis_name}.{key} 不能为空"
                        )

    if figure_type == "line-chart":
        axes = figure.get("axis_labels")
        axis_names = {
            str(item.get("axis") or "").lower()
            for item in axes
            if isinstance(item, dict) and _localized_text(item)
        } if isinstance(axes, list) else set()
        if not any(name.startswith("horizontal") for name in axis_names):
            errors.append(f"{label} 缺少横轴名称")
        if not any(name.startswith("vertical") for name in axis_names):
            errors.append(f"{label} 缺少纵轴名称")
        errors.extend(_validate_series(figure.get("series"), label=label))

    if figure_type == "simple-slope-line-chart":
        x_axis = figure.get("x_axis")
        categories = (
            x_axis.get("categories")
            if isinstance(x_axis, dict)
            else None
        )
        if not isinstance(categories, list) or len(categories) < 2 or not all(
            str(value).strip() for value in categories
        ):
            errors.append(f"{label}.x_axis.categories 至少包含两个类别")
            category_count = None
        else:
            category_count = len(categories)
        y_axis = figure.get("y_axis")
        if not isinstance(y_axis, dict) or not _localized_text(y_axis):
            errors.append(f"{label}.y_axis 缺少目标语言名称")
        errors.extend(
            _validate_series(
                figure.get("series"),
                label=label,
                expected_values=category_count,
            )
        )

    for shape_index, shape in enumerate(shapes):
        if (
            str(shape.get("type") or "").lower()
            != "illustrative-time-series-bank"
        ):
            continue
        items = shape.get("items")
        expected_count = int(shape.get("series_count") or 0)
        if not isinstance(items, list) or not items:
            errors.append(
                f"{label}.shapes[{shape_index}] 必须显式提供 items，"
                "生成器不得补造项目名称"
            )
        elif expected_count and len(items) != expected_count:
            errors.append(
                f"{label}.shapes[{shape_index}].items 数量与 "
                "series_count 不一致"
            )
        elif not all(_localized_text(item) for item in items):
            errors.append(
                f"{label}.shapes[{shape_index}].items 含空白目标文字"
            )
    return errors


def validate_complex_payload_item(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    method = str(item.get("method") or "")
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return ["payload 必须是对象"]
    render_policy = payload.get("render_policy")
    if render_policy not in {
        None,
        "replace-page-units",
        "insert-before",
        "insert-after",
    }:
        errors.append(
            "payload.render_policy 仅支持 replace-page-units、"
            "insert-before 或 insert-after"
        )
    before_unit = payload.get("insert_before_unit_id")
    after_unit = payload.get("insert_after_unit_id")
    if before_unit is not None and not (
        isinstance(before_unit, str) and before_unit.strip()
    ):
        errors.append("payload.insert_before_unit_id 必须是非空单元 ID")
    if after_unit is not None and not (
        isinstance(after_unit, str) and after_unit.strip()
    ):
        errors.append("payload.insert_after_unit_id 必须是非空单元 ID")
    if before_unit and after_unit:
        errors.append("复杂内容只能选择一个译文单元插入锚点")
    if (before_unit or after_unit) and render_policy == "replace-page-units":
        errors.append("整页替换不能同时使用译文单元插入锚点")
    evidence = item.get("source_evidence")
    if not isinstance(evidence, list) or not any(
        isinstance(value, str) and value.strip() for value in evidence
    ):
        errors.append("source_evidence 至少包含一条原页核对依据")

    if method in {"structured-table-rebuild", "semantic-grid-rebuild"}:
        tables = payload.get("tables")
        if not isinstance(tables, list) or not tables:
            errors.append("表格载荷必须包含非空 tables")
        else:
            for index, table in enumerate(tables):
                if not isinstance(table, dict):
                    errors.append(f"tables[{index}] 必须是对象")
                    continue
                errors.extend(_validate_table_contract(table, index))
                rows = table.get("row_count")
                columns = table.get("column_count")
                cells = table.get("cells")
                matrix = table.get("rows")
                if not isinstance(rows, int) or rows < 2:
                    if not isinstance(matrix, list) or len(matrix) < 2:
                        errors.append(
                            f"tables[{index}] 必须提供至少两行 rows，"
                            "或有效 row_count"
                        )
                if not isinstance(columns, int) or columns < 2:
                    if not (
                        isinstance(matrix, list)
                        and matrix
                        and isinstance(matrix[0], list)
                        and len(matrix[0]) >= 2
                    ):
                        errors.append(
                            f"tables[{index}] 必须提供至少两列 rows，"
                            "或有效 column_count"
                        )
                if not (
                    isinstance(cells, list) and len(cells) >= 4
                ) and not (
                    isinstance(matrix, list)
                    and sum(
                        len(row)
                        for row in matrix
                        if isinstance(row, list)
                    )
                    >= 4
                ):
                    errors.append(
                        f"tables[{index}] 至少包含 4 个结构化单元格"
                    )
    elif method == "vector-rebuild":
        figures = payload.get("figures")
        if not isinstance(figures, list) or not figures:
            errors.append("矢量图载荷必须包含非空 figures")
        else:
            for index, figure in enumerate(figures):
                if not isinstance(figure, dict):
                    errors.append(f"figures[{index}] 必须是对象")
                    continue
                errors.extend(_validate_vector_contract(figure, index))
                labels = figure.get("labels")
                nodes = figure.get("nodes")
                circles = figure.get("circles")
                panels = figure.get("panels")
                figure_type = str(figure.get("type") or "").lower()
                if figure_type in {"bar-panels", "grouped-bar-panels"}:
                    if not isinstance(panels, list) or not panels:
                        errors.append(
                            f"figures[{index}] 的柱状图必须包含 panels"
                        )
                    else:
                        for panel_index, panel in enumerate(panels):
                            groups = (
                                panel.get("groups")
                                if isinstance(panel, dict)
                                else None
                            )
                            if not isinstance(groups, list) or len(groups) < 2:
                                errors.append(
                                    f"figures[{index}].panels[{panel_index}] "
                                    "必须包含至少两个组别"
                                )
                                continue
                            for group_index, group in enumerate(groups):
                                if not (
                                    isinstance(group, dict)
                                    and str(
                                        group.get("translation")
                                        or group.get("label")
                                        or ""
                                    ).strip()
                                    and isinstance(
                                        group.get("value"),
                                        (int, float),
                                    )
                                ):
                                    errors.append(
                                        f"figures[{index}].panels[{panel_index}]"
                                        f".groups[{group_index}] "
                                        "必须包含组别名称和数值"
                                    )
                elif figure_type == "layout":
                    if not isinstance(labels, list) or not labels:
                        errors.append(
                            f"figures[{index}] 的 layout 必须包含 labels"
                        )
                elif figure_type == "venn":
                    if not isinstance(circles, list) or len(circles) < 2:
                        errors.append(
                            f"figures[{index}] 的 venn 必须包含至少两个 circles"
                        )
                elif figure_type == "pyramid":
                    levels = figure.get("levels")
                    if not isinstance(levels, list) or len(levels) < 2:
                        errors.append(
                            f"figures[{index}] 的 pyramid 必须包含至少两个 levels"
                        )
                elif not (
                    isinstance(nodes, list) and nodes
                    or isinstance(figure.get("series"), list)
                    and figure.get("series")
                    or isinstance(panels, list)
                    and panels
                    or isinstance(labels, list)
                    and labels
                ):
                    errors.append(
                        f"figures[{index}] 必须包含节点、序列或标签"
                    )
                has_structure = any(
                    isinstance(figure.get(key), list) and figure.get(key)
                    for key in (
                        "nodes",
                        "edges",
                        "series",
                        "panels",
                        "shapes",
                        "connectors",
                        "circles",
                        "levels",
                        "annotations",
                    )
                )
                if not has_structure:
                    errors.append(
                        f"figures[{index}] 必须包含边、连线、序列或形状结构"
                    )
    elif method in {"image-text-localization", "ocr-region-rebuild"}:
        regions = payload.get("regions")
        if not isinstance(regions, list) or not regions:
            errors.append("图像/OCR 载荷必须包含非空 regions")
        else:
            for index, region in enumerate(regions):
                if not isinstance(region, dict):
                    errors.append(f"regions[{index}] 必须是对象")
                    continue
                if not (
                    isinstance(region.get("xref"), int)
                    or isinstance(region.get("source_bbox"), list)
                ):
                    errors.append(
                        f"regions[{index}] 必须提供 xref 或 source_bbox"
                    )
                if not str(
                    region.get("translation")
                    or region.get("caption")
                    or ""
                ).strip():
                    errors.append(
                        f"regions[{index}] 缺少目标语言文字或图题"
                    )
                localized_labels = region.get("localized_labels")
                if (
                    region.get("semantic_text_expected") is True
                    and not (
                        isinstance(localized_labels, list)
                        and localized_labels
                    )
                ):
                    errors.append(
                        f"regions[{index}] 的语义图像必须提供 "
                        "localized_labels"
                    )
                if isinstance(localized_labels, list):
                    for label_index, label in enumerate(localized_labels):
                        if isinstance(label, str) and label.strip():
                            continue
                        if not isinstance(label, dict) or not str(
                            label.get("translation")
                            or label.get("target")
                            or label.get("localized")
                            or ""
                        ).strip():
                            errors.append(
                                f"regions[{index}].localized_labels"
                                f"[{label_index}] 缺少目标语言文字"
                            )
                width_ratio = region.get("display_width_ratio")
                if width_ratio is not None and (
                    isinstance(width_ratio, bool)
                    or not isinstance(width_ratio, (int, float))
                    or not 0.3 <= float(width_ratio) <= 1.0
                ):
                    errors.append(
                        f"regions[{index}].display_width_ratio "
                        "必须在 0.3 至 1.0 之间"
                    )
                max_height = region.get("display_max_height_pt")
                if max_height is not None and (
                    isinstance(max_height, bool)
                    or not isinstance(max_height, (int, float))
                    or not 120 <= float(max_height) <= 520
                ):
                    errors.append(
                        f"regions[{index}].display_max_height_pt "
                        "必须在 120 至 520 之间"
                    )
    elif method in {"custom-page-reflow", "manual-reading-order-rebuild"}:
        ordered = payload.get("ordered_block_ids")
        if not isinstance(ordered, list) or not ordered:
            errors.append("重排载荷必须包含 ordered_block_ids")
    components = payload.get("components")
    if components is not None:
        if not isinstance(components, list) or not components:
            errors.append("payload.components 必须是非空数组")
        else:
            for index, component in enumerate(components):
                if not isinstance(component, dict):
                    errors.append(f"components[{index}] 必须是对象")
                    continue
                component_method = component.get("method")
                component_payload = component.get("payload")
                component_errors = validate_complex_payload_item(
                    {
                        "method": component_method,
                        "payload": component_payload,
                        "source_evidence": item.get("source_evidence"),
                    }
                )
                errors.extend(
                    f"components[{index}]: {error}"
                    for error in component_errors
                )
    return errors


def set_complex_payload(
    job_dir: Path,
    page: int,
    payload_file: Path,
    source_evidence: list[str],
    *,
    ready: bool,
    notes: str,
) -> dict[str, Any]:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    payload_path = job_dir / job.get("files", {}).get(
        "complex_content_payload",
        "complex_content.json",
    )
    data = load_json(payload_path)
    matches = [
        item
        for item in data.get("items", [])
        if isinstance(item, dict) and item.get("page") == page
    ]
    if len(matches) != 1:
        raise SkillError(f"第 {page} 页没有唯一的复杂内容模板")
    item = matches[0]
    payload = load_json(payload_file.resolve())
    if not isinstance(payload, dict):
        raise SkillError("载荷文件顶层必须是对象")
    item["payload"] = payload
    item["source_evidence"] = [
        value.strip() for value in source_evidence if value.strip()
    ]
    item["notes"] = notes.strip()
    item["status"] = "ready" if ready else "draft"
    if ready:
        errors = validate_complex_payload_item(item)
        if errors:
            raise SkillError("复杂内容载荷尚不完整: " + "；".join(errors))
    write_json(payload_path, data)
    return item


def main() -> int:
    parser = argparse.ArgumentParser(
        description="填写表格、模型图、截图、OCR 或阅读顺序的结构化重建载荷"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--page", type=int, required=True)
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--source-evidence", action="append", default=[])
    parser.add_argument("--notes", default="")
    parser.add_argument("--ready", action="store_true")
    args = parser.parse_args()
    try:
        item = set_complex_payload(
            args.job_dir,
            args.page,
            args.payload,
            args.source_evidence,
            ready=args.ready,
            notes=args.notes,
        )
        print(
            f"复杂内容载荷已更新: 第 {item['page']} 页，"
            f"状态 {item['status']}"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
