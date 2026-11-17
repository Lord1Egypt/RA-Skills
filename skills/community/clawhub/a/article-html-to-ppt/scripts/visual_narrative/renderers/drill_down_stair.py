from __future__ import annotations

from typing import Any

from .common import RenderResult, add_bound_connector, add_box, content_box, resolve_style


def render(
    slide: Any,
    obj: dict[str, Any],
    intent: dict[str, Any],
    style: dict[str, Any],
) -> dict[str, Any]:
    content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
    levels = content.get("levels")
    if not isinstance(levels, list) or len(levels) < 2:
        raise ValueError("DRILL_DOWN_LEVELS_REQUIRED")

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    count = len(levels)
    step_y = min(0.92, (h - 0.72) / max(count - 1, 1))
    step_x = min(1.05, w * 0.09)
    level_shapes: list[Any] = []
    names: list[str] = []

    for index, level in enumerate(levels):
        if isinstance(level, dict):
            label = str(level.get("label") or f"层级 {index + 1}")
            detail = str(level.get("detail") or "")
        else:
            label, detail = str(level), ""
        text = label if not detail else f"{label}\n{detail}"
        name = f"Component:drill_down_stair:level:{index}"
        shape = add_box(
            slide,
            name=name,
            x=x + index * step_x,
            y=y + index * step_y,
            w=max(2.2, w - 2.0 - index * step_x * 1.15),
            h=0.72,
            fill=colors["signal_blue"] if index == count - 1 else colors["mist_blue"],
            line=colors["signal_blue"],
            text=text,
            text_color=colors["paper_white"] if index == count - 1 else colors["ink_navy"],
            font_size=10.5,
            bold=True,
        )
        level_shapes.append(shape)
        names.append(name)

    for index, (before, after) in enumerate(zip(level_shapes, level_shapes[1:])):
        name = f"Connector:drill_down_stair:focus:{index}"
        add_bound_connector(
            slide,
            before,
            after,
            name=name,
            color=colors["signal_blue"],
            vertical=True,
            width_pt=2.0,
        )
        names.append(name)
    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()
