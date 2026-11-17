from __future__ import annotations

from typing import Any

from .common import (
    RenderResult,
    add_bound_connector,
    add_box,
    add_circle,
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
    phases = content.get("phases")
    milestones = content.get("milestones")
    if not isinstance(phases, list) or len(phases) < 2:
        raise ValueError("PHASE_ROADMAP_PHASES_REQUIRED")
    if not isinstance(milestones, list):
        milestones = []

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    gap = 0.28
    phase_w = (w - gap * (len(phases) - 1)) / len(phases)
    phase_shapes: list[Any] = []
    names: list[str] = []

    for index, phase in enumerate(phases):
        if isinstance(phase, dict):
            label = str(phase.get("label") or f"阶段 {index + 1}")
            period = str(phase.get("period") or "")
            objective = str(phase.get("objective") or "")
        else:
            label, period, objective = str(phase), "", ""
        text = "\n".join(value for value in (label, period, objective) if value)
        name = f"Component:phase_roadmap:phase:{index}"
        shape = add_box(
            slide,
            name=name,
            x=x + index * (phase_w + gap),
            y=y + index * 0.22,
            w=phase_w,
            h=1.45,
            fill=colors["mist_blue"] if index < len(phases) - 1 else colors["signal_blue"],
            line=colors["insight_blue"],
            text=text,
            text_color=colors["ink_navy"] if index < len(phases) - 1 else colors["paper_white"],
            font_size=10.5,
            bold=True,
        )
        phase_shapes.append(shape)
        names.append(name)

    for index, (before, after) in enumerate(zip(phase_shapes, phase_shapes[1:])):
        name = f"Connector:phase_roadmap:dependency:{index}"
        add_bound_connector(
            slide,
            before,
            after,
            name=name,
            color=colors["signal_blue"],
            width_pt=1.7,
        )
        names.append(name)

    phase_counts = [0 for _ in phases]
    for index, milestone in enumerate(milestones):
        if isinstance(milestone, dict):
            label = str(milestone.get("label") or f"里程碑 {index + 1}")
            phase_index = milestone.get("phase", 0)
        else:
            label, phase_index = str(milestone), 0
        phase_index = int(phase_index) if isinstance(phase_index, (int, float)) else 0
        phase_index = max(0, min(len(phases) - 1, phase_index))
        local_index = phase_counts[phase_index]
        phase_counts[phase_index] += 1
        name = f"Component:phase_roadmap:milestone:{index}"
        add_circle(
            slide,
            name=name,
            x=x + phase_index * (phase_w + gap) + 0.18 + local_index * 1.12,
            y=y + 2.25 + phase_index * 0.22,
            w=1.0,
            h=0.62,
            fill=colors["paper_white"],
            line=colors["success"],
            text=label,
            text_color=colors["ink_navy"],
            font_size=10.5,
        )
        names.append(name)
    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()
