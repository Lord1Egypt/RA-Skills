from __future__ import annotations

from typing import Any

from .common import RenderResult, add_box, add_text, content_box, resolve_style


def render(
    slide: Any,
    obj: dict[str, Any],
    intent: dict[str, Any],
    style: dict[str, Any],
) -> dict[str, Any]:
    content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
    rows = _labels(content.get("rows"))
    columns = _labels(content.get("columns"))
    values = content.get("values")
    if not rows or not columns or not isinstance(values, list) or len(values) != len(rows):
        raise ValueError("HEAT_MATRIX_DATA_INVALID")
    if any(not isinstance(row, list) or len(row) != len(columns) for row in values):
        raise ValueError("HEAT_MATRIX_DATA_INVALID")

    numeric = [float(value) for row in values for value in row]
    minimum, maximum = min(numeric), max(numeric)
    spread = maximum - minimum
    highlighted = {
        tuple(cell)
        for cell in content.get("highlighted_cells", [])
        if isinstance(cell, list) and len(cell) == 2
    }
    suffix = str(content.get("value_suffix") or "")
    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    label_w, header_h = 1.35, 0.45
    grid_w = w - label_w
    grid_h = min(h - header_h - 0.55, 3.5)
    cell_w, cell_h = grid_w / len(columns), grid_h / len(rows)
    names: list[str] = []

    for column_index, column in enumerate(columns):
        name = f"Component:heat_matrix:column:{column_index}"
        add_text(
            slide,
            name=name,
            text=column,
            x=x + label_w + column_index * cell_w,
            y=y,
            w=cell_w,
            h=header_h,
            color=colors["slate_text"],
            font_size=10.5,
            bold=True,
        )
        names.append(name)

    for row_index, row_label in enumerate(rows):
        row_y = y + header_h + row_index * cell_h
        label_name = f"Component:heat_matrix:row:{row_index}"
        add_text(
            slide,
            name=label_name,
            text=row_label,
            x=x,
            y=row_y,
            w=label_w - 0.08,
            h=cell_h,
            color=colors["ink_navy"],
            font_size=10.5,
            bold=True,
        )
        names.append(label_name)
        for column_index, value in enumerate(values[row_index]):
            number = float(value)
            ratio = (number - minimum) / spread if spread else 0.5
            fill = colors["signal_blue"] if ratio >= 0.52 else colors["mist_blue"]
            highlighted_cell = (row_index, column_index) in highlighted
            cell_name = f"Component:heat_matrix:cell:{row_index}:{column_index}"
            add_box(
                slide,
                name=cell_name,
                x=x + label_w + column_index * cell_w + 0.02,
                y=row_y + 0.02,
                w=cell_w - 0.04,
                h=cell_h - 0.04,
                fill=fill,
                line=colors["signal_blue"] if highlighted_cell else colors["paper_white"],
                line_width=2.0 if highlighted_cell else 0.7,
                text=f"{_format_value(value)}{suffix}",
                text_color=colors["paper_white"] if ratio >= 0.52 else colors["ink_navy"],
                font_size=10.5,
                bold=highlighted_cell,
                radius=False,
            )
            names.append(cell_name)

    legend_y = y + header_h + grid_h + 0.16
    for index, (label, fill) in enumerate(
        (("低", colors["mist_blue"]), ("高", colors["signal_blue"]))
    ):
        legend_name = f"Component:heat_matrix:legend:{index}"
        add_box(
            slide,
            name=legend_name,
            x=x + label_w + index * 0.62,
            y=legend_y,
            w=0.52,
            h=0.28,
            fill=fill,
            line=colors["hairline_grey"],
            text=label,
            text_color=colors["ink_navy"] if index == 0 else colors["paper_white"],
            font_size=10.5,
            radius=False,
        )
        names.append(legend_name)
    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()


def _labels(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _format_value(value: Any) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"
