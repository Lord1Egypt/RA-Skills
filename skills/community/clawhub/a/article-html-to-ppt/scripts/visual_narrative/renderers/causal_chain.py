from __future__ import annotations

from typing import Any

from .common import RenderResult, add_bound_connector, add_box, content_box, resolve_style


def render(slide: Any, obj: dict[str, Any], intent: dict[str, Any], style: dict[str, Any]) -> dict[str, Any]:
    content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
    nodes = content.get("nodes")
    if not isinstance(nodes, list) or len(nodes) < 3:
        raise ValueError("CAUSAL_CHAIN_NODES_REQUIRED")

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    primary = [item for item in nodes if isinstance(item, dict) and item.get("priority") != "supporting"]
    if len(primary) < 3:
        primary = [item for item in nodes if isinstance(item, dict)][:3]
    primary = primary[:5]
    gap = 0.32
    node_w = (w - gap * (len(primary) - 1)) / len(primary)
    shapes: list[Any] = []
    names: list[str] = []
    for index, node in enumerate(primary):
        label = str(node.get("label") or f"环节 {index + 1}")
        role = str(node.get("role") or "")
        name = f"Component:causal_chain:node:{index}"
        shape = add_box(
            slide, name=name, x=x + index * (node_w + gap), y=y + 1.2,
            w=node_w, h=1.15,
            fill=colors["signal_blue"] if index == len(primary) - 1 else colors["mist_blue"],
            line=colors["insight_blue"], text=f"{label}\n{role}" if role else label,
            text_color=colors["paper_white"] if index == len(primary) - 1 else colors["ink_navy"],
            font_size=10.5, bold=True,
        )
        shapes.append(shape)
        names.append(name)
    for index, (before, after) in enumerate(zip(shapes, shapes[1:])):
        name = f"Connector:causal_chain:main:{index}"
        add_bound_connector(slide, before, after, name=name, color=colors["signal_blue"], width_pt=1.8)
        names.append(name)
    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()
