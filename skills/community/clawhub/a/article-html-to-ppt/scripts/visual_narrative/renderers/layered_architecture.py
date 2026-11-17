from __future__ import annotations

from typing import Any

from .common import (
    RenderResult,
    add_bound_connector,
    add_box,
    add_text,
    content_box,
    resolve_style,
)


def render(
    slide: Any,
    obj: dict[str, Any],
    intent: dict[str, Any],
    style: dict[str, Any],
) -> dict[str, Any]:
    content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
    layers = content.get("layers")
    if not isinstance(layers, list) or len(layers) < 2:
        raise ValueError("LAYERED_ARCHITECTURE_LAYERS_REQUIRED")

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    boundary_name = "Boundary:layered_architecture:primary"
    add_box(
        slide,
        name=boundary_name,
        x=x,
        y=y,
        w=w,
        h=h,
        fill=None,
        line=colors["hairline_grey"],
        radius=False,
    )
    names = [boundary_name]
    boundary_label = str(content.get("boundary_label") or "").strip()
    if boundary_label:
        boundary_label_name = "Component:layered_architecture:boundary_label"
        add_text(
            slide,
            name=boundary_label_name,
            text=boundary_label,
            x=x + 0.18,
            y=y + 0.03,
            w=w - 0.36,
            h=0.28,
            color=colors["slate_text"],
            font_size=10.5,
            bold=True,
        )
        names.append(boundary_label_name)
    gap = 0.16
    inner_y = y + 0.38
    layer_h = (h - 0.55 - gap * (len(layers) - 1)) / len(layers)
    layer_shapes: list[Any] = []
    for index, layer in enumerate(layers):
        if isinstance(layer, dict):
            label = str(layer.get("label") or f"第 {index + 1} 层")
            nodes = layer.get("nodes") if isinstance(layer.get("nodes"), list) else []
        else:
            label, nodes = str(layer), []
        text = label
        if nodes:
            text += "\n" + "  ·  ".join(str(node) for node in nodes)
        name = f"Component:layered_architecture:layer:{index}"
        shape = add_box(
            slide,
            name=name,
            x=x + 0.28,
            y=inner_y + index * (layer_h + gap),
            w=w - 0.56,
            h=layer_h,
            fill=colors["mist_blue"] if index % 2 == 0 else colors["paper_white"],
            line=colors["insight_blue"] if index < 2 else colors["hairline_grey"],
            text=text,
            text_color=colors["ink_navy"],
            font_size=10,
            bold=True,
            radius=True,
        )
        layer_shapes.append(shape)
        names.append(name)

    for index, (before, after) in enumerate(zip(layer_shapes, layer_shapes[1:])):
        name = f"Connector:layered_architecture:main:{index}"
        add_bound_connector(
            slide,
            before,
            after,
            name=name,
            color=colors["signal_blue"],
            vertical=True,
            width_pt=1.8,
        )
        names.append(name)
    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()
