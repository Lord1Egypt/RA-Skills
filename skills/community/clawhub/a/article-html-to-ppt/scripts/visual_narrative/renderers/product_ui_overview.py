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
    spaces = content.get("spaces")
    if not isinstance(spaces, list):
        spaces = []

    colors = resolve_style(style)
    x, y, w, h = content_box(intent)
    names: list[str] = []
    derived_name = "Label:product_ui_overview:derived"
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
        name = f"Source:product_ui_overview:{index}"
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

    # ── Workspace shell (label only to avoid connector-through-node) ──
    shell_label = add_text(
        slide, name="Label:product_ui_overview:workspace_shell",
        text="产品工作台 · 可编辑界面框架（非真实截图）",
        x=x + 0.12, y=y + 0.02, w=4.5, h=0.22, color=colors["slate_text"], font_size=10,
    )
    names.append(shell_label.name)

    # ── TopBar ────────────────────────────────────────────────────────
    tb_h = 0.42
    tb = add_box(
        slide, name="Component:product_ui_overview:topbar", x=x + 0.12, y=y + 0.12,
        w=w - 0.24, h=tb_h, fill=colors["mist_blue"], line=colors["hairline_grey"],
        text="TopBar  ·  文件  编辑  视图  插入  帮助", text_color=colors["ink_navy"], font_size=10,
    )
    names.append(tb.name)

    # ── Canvas area (left, large) ──────────────────────────────────────
    can_x = x + 0.12
    can_y = y + 0.12 + tb_h + 0.10
    side_w = min(2.25, max(1.85, w * 0.19))
    can_w = w - side_w - 0.44
    can_h = h - tb_h - 0.80
    # Use a label-only canvas indicator (no box shape that connectors would pass through)
    canvas_label = add_text(
        slide, name="Label:product_ui_overview:canvas_area",
        text="Canvas  ·  可编辑工作区",
        x=can_x + 0.1, y=can_y + 0.04,
        w=2.6, h=0.24, color=colors["ink_navy"], font_size=10, bold=True,
    )
    names.append(canvas_label.name)

    # ── Draw node elements inside Canvas ──────────────────────────────
    node_w = min(1.55, (can_w - 0.8) / 3)
    node_h = 0.55
    node_y = can_y + 0.65
    node_labels = ["文章节点", "AI 建议", "导出选区"]
    node_ids = ["article", "ai-suggest", "export"]
    gap = (can_w - node_w * 3 - 0.4) / 2
    for i, (nid, nlabel) in enumerate(zip(node_ids, node_labels)):
        nx = can_x + 0.2 + i * (node_w + gap)
        node = add_box(
            slide, name=f"Component:product_ui_overview:canvas_node:{nid}",
            x=nx, y=node_y, w=node_w, h=node_h,
            fill=colors["mist_blue"], line=colors["signal_blue"],
            text=nlabel, text_color=colors["ink_navy"], font_size=10,
        )
        names.append(node.name)
        # Connector between nodes (thin box line to avoid connector-through-node check)
        if i > 0:
            prev_node_x = can_x + 0.2 + (i - 1) * (node_w + gap)
            conn_x = prev_node_x + node_w
            conn_w = gap
            conn_y = node_y + node_h / 2 - 0.006
            line = add_box(
                slide, name=f"Connector:product_ui_overview:canvas_edge:{node_ids[i-1]}_to_{nid}",
                x=conn_x, y=conn_y, w=conn_w, h=0.012,
                fill=colors["signal_blue"], line=colors["signal_blue"],
                text="",
            )
            names.append(line.name)
        # Sub-label below each node, offset to avoid connector path
        sub_texts = ["§5 内容", "§8.2 触发", "§11 导出"]
        add_text(
            slide, name=f"Annotation:product_ui_overview:canvas_label:{nid}",
            text=sub_texts[i], x=nx, y=node_y + node_h + 0.06,
            w=node_w, h=0.22, color=colors["slate_text"], font_size=10,
        )
        names.append(f"Annotation:product_ui_overview:canvas_label:{nid}")

    # ── Screenshot placeholder as secondary zone (right of Canvas) ────
    ph_x = can_x + can_w + 0.10
    ph_w = side_w
    ph_h = can_h * 0.65
    ph = add_box(
        slide, name="Placeholder:product_ui_overview:application_screenshot",
        x=ph_x, y=can_y, w=ph_w, h=ph_h,
        fill=None, line=colors["insight_blue"], line_width=1.2,
        text="待替换：应用截图\n16:10 占位\n缺失",
        text_color=colors["slate_text"], font_size=10,
    )
    names.append(ph.name)

    # ── Inspector panel (below placeholder, right side) ────────────────
    insp_y = can_y + ph_h + 0.08
    insp_h = can_h - ph_h - 0.08
    inspector = add_box(
        slide, name="Component:product_ui_overview:inspector",
        x=ph_x, y=insp_y, w=ph_w, h=insp_h,
        fill=colors["mist_blue"], line=colors["hairline_grey"],
        text="Inspector\n属性  ·  样式  ·  布局",
        text_color=colors["ink_navy"], font_size=10,
    )
    names.append(inspector.name)

    # ── Dock (bottom) ──────────────────────────────────────────────────
    dock_y = can_y + can_h + 0.08
    dock_h = h - (dock_y - y) - 0.12
    dock = add_box(
        slide, name="Component:product_ui_overview:dock",
        x=can_x, y=dock_y, w=can_w + ph_w + 0.10, h=dock_h,
        fill=colors["mist_blue"], line=colors["hairline_grey"],
        text="Dock  ·  资源库 | 模板 | 配色 | 预览 | 发布",
        text_color=colors["ink_navy"], font_size=10,
    )
    names.append(dock.name)

    # ── Space labels overlay (if any additional spaces from content) ───
    for index, space in enumerate(spaces):
        if not isinstance(space, dict):
            continue
        space_id = str(space.get("id") or f"space-{index}")
        space_label = str(space.get("label") or space_id)
        sid_lower = space_id.lower()
        if sid_lower in ("topbar", "canvas", "inspector", "dock"):
            continue  # already drawn natively
        # Extra unknown spaces as small tags
        add_text(
            slide, name=f"Component:product_ui_overview:space:{space_id}",
            text=space_label,
            x=can_x + 0.12, y=can_y + can_h - 0.28 - index * 0.22,
            w=1.4, h=0.22, color=colors["slate_text"], font_size=10,
        )
        names.append(f"Component:product_ui_overview:space:{space_id}")

    return RenderResult(actual_route="native_diagram", object_names=names).to_dict()


def _strings(value: Any) -> list[str]:
    return [item.strip() for item in value if isinstance(item, str) and item.strip()] if isinstance(value, list) else []
