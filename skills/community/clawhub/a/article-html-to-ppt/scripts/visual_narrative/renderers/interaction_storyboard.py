from __future__ import annotations

from typing import Any

from .common import RenderResult, add_bound_connector, add_box, add_text, content_box, resolve_style


def render(
    slide: Any,
    obj: dict[str, Any],
    intent: dict[str, Any],
    style: dict[str, Any],
) -> dict[str, Any]:
    content = obj.get("content") if isinstance(obj.get("content"), dict) else {}
    steps = content.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError("INTERACTION_STORYBOARD_STEPS_REQUIRED")

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    names: list[str] = []
    derived_name = "Label:interaction_storyboard:derived"
    add_text(
        slide,
        name=derived_name,
        text="PRD 派生示意",
        x=x,
        y=y - 0.3,
        w=1.45,
        h=0.22,
        color=colors["slate_text"],
        font_size=10,
        bold=True,
    )
    names.append(derived_name)
    source_refs = _strings(content.get("source_refs"))
    source_width = max(2.15, (w - 1.55) / max(1, len(source_refs)))
    for index, source in enumerate(source_refs):
        name = f"Source:interaction_storyboard:{index}"
        add_text(
            slide,
            name=name,
            text=f"来源：{source}",
            x=x + 1.55 + index * source_width,
            y=y - 0.3,
            w=source_width,
            h=0.28,
            color=colors["slate_text"],
            font_size=10,
        )
        names.append(name)

    # ── Main flow: steps in a horizontal row ───────────────────────────
    main_steps = [s for s in steps if isinstance(s, dict) and s.get("kind") != "error"]
    error_steps = [s for s in steps if isinstance(s, dict) and s.get("kind") == "error"]

    node_w = max(1.45, min(2.0, (w - 0.2 * (len(main_steps) - 1)) / len(main_steps)))
    total_w = node_w * len(main_steps) + 0.2 * (len(main_steps) - 1)
    start_x = x + max(0, (w - total_w) / 2)
    node_y = y + max(0.3, (h - 1.15) / 2)

    shapes: dict[str, Any] = {}
    for index, step in enumerate(main_steps):
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("id") or f"step-{index}")
        label = str(step.get("label") or step_id)
        kind = str(step.get("kind") or "state")
        if kind == "error":
            continue  # handled below
        fill = colors["mist_blue"] if kind in {"async_state", "result"} else colors["paper_white"]
        name = f"Component:interaction_storyboard:step:{step_id}"
        shapes[step_id] = add_box(
            slide,
            name=name,
            x=start_x + index * (node_w + 0.2),
            y=node_y,
            w=node_w,
            h=1.15,
            fill=fill,
            line=colors["signal_blue"] if kind == "async_state" else colors["hairline_grey"],
            text=f"{kind}\n{label}",
            text_color=colors["ink_navy"],
            font_size=10,
            bold=True,
        )
        names.append(name)

        # State sub-boxes per kind
        if kind == "action":
            state = add_box(
                slide, name=f"State:interaction_storyboard:{step_id}:entry_trigger",
                x=start_x + index * (node_w + 0.2) + 0.10, y=node_y + 0.58,
                w=node_w - 0.20, h=0.38,
                fill=colors["paper_white"], line=colors["hairline_grey"],
                text="选择节点 · 触发入口",
                text_color=colors["slate_text"], font_size=10,
            )
            names.append(state.name)
        elif kind == "async_state":
            state = add_box(
                slide, name=f"State:interaction_storyboard:{step_id}:assistant_bubble",
                x=start_x + index * (node_w + 0.2) + 0.10, y=node_y + 0.58,
                w=node_w - 0.20, h=0.38,
                fill=colors["paper_white"], line=colors["insight_blue"],
                text="AI 反馈 · 流式生成中",
                text_color=colors["signal_blue"], font_size=10,
            )
            names.append(state.name)
        elif kind == "result":
            state = add_box(
                slide, name=f"State:interaction_storyboard:{step_id}:diff_preview",
                x=start_x + index * (node_w + 0.2) + 0.10, y=node_y + 0.58,
                w=node_w - 0.20, h=0.38,
                fill=colors["paper_white"], line=colors["hairline_grey"],
                text="Diff / 结果预览",
                text_color=colors["slate_text"], font_size=10,
            )
            names.append(state.name)
        elif kind == "decision":
            state = add_box(
                slide, name=f"State:interaction_storyboard:{step_id}:decision_controls",
                x=start_x + index * (node_w + 0.2) + 0.10, y=node_y + 0.58,
                w=node_w - 0.20, h=0.38,
                fill=colors["paper_white"], line=colors["success"],
                text="采纳  /  撤销",
                text_color=colors["success"], font_size=10,
            )
            names.append(state.name)

    # ── Transitions between main steps ────────────────────────────────
    for index, transition in enumerate(content.get("transitions") or []):
        if not isinstance(transition, dict):
            continue
        start = shapes.get(str(transition.get("from") or ""))
        end = shapes.get(str(transition.get("to") or ""))
        if start is None or end is None:
            continue
        name = f"Connector:interaction_storyboard:transition:{index}"
        add_bound_connector(slide, start, end, name=name, color=colors["signal_blue"])
        names.append(name)

    # ── ERROR / CONFLICT branch ───────────────────────────────────────
    if error_steps:
        last_main = max(main_steps, key=lambda s: _step_order(s.get("kind", "state")))
        last_main_id = str(last_main.get("id", ""))
        last_shape = shapes.get(last_main_id)
        if last_shape is not None:
            err_y = node_y + 1.55
            err_w = max(1.8, (w - 0.3) / len(error_steps))
            for ei, err in enumerate(error_steps):
                if not isinstance(err, dict):
                    continue
                err_id = str(err.get("id") or f"error-{ei}")
                err_label = str(err.get("label") or "ERROR")
                err_action = str(err.get("action") or "重试 / 重新生成 / 查看差异")
                ex = x + 0.2 + ei * (err_w + 0.2)
                err_box = add_box(
                    slide, name=f"Component:interaction_storyboard:error:{err_id}",
                    x=ex, y=err_y, w=err_w, h=0.75,
                    fill=colors["paper_white"], line=colors["warning"],
                    text=f"⚠ {err_label}\n{err_action}",
                    text_color=colors["ink_navy"], font_size=10,
                )
                names.append(err_box.name)
                # Connector from last main step to error
                add_bound_connector(
                    slide, last_shape, err_box,
                    name=f"Connector:interaction_storyboard:error_branch:{err_id}",
                    color=colors["warning"], vertical=True,
                )
                names.append(f"Connector:interaction_storyboard:error_branch:{err_id}")

    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()


def _step_order(kind: str) -> int:
    order = {"action": 0, "async_state": 1, "result": 2, "decision": 3}
    return order.get(kind, 99)


def _strings(value: Any) -> list[str]:
    return [item.strip() for item in value if isinstance(item, str) and item.strip()] if isinstance(value, list) else []
