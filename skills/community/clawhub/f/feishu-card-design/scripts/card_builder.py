#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu-card-design 卡片构建工具 (Python Builder API)

提供函数式 API 帮助 Agent 用 Python 代码生成符合 feishu-card-design 规范的卡片 JSON.
所有函数返回的都是 dict, 可直接 json.dumps 后通过飞书 OpenAPI 发送.

设计原则:
  - 函数式 (无类状态, 易组合)
  - 强制邻近色环 (调用方传 header_template, builder 自动校验 background_style)
  - 默认合规 (不传 background_style 时使用 'default' 而非乱填色)
  - 双重保险 (column_set + column 都设 background_style)

最小示例:
    from card_builder import build_card, header, markdown, column_block, button, note

    card = build_card(
        header=header("20260719-存量日报-归档30篇", template="turquoise",
                      subtitle="2026-07-19 · obsidian-loop v2.1"),
        elements=[
            markdown("**今日产出**: 30 篇素材入库"),
            column_block("📦 **归档概览**\\n- 30 篇 / 18 atoms", bg_color="turquoise-50"),
            column_block("💎 **5★ 精选**\\n- atom-07 · 排期是关键", bg_color="yellow-50"),
            column_block("📊 **统计**\\n- 22% 覆盖率", bg_color="grey-50"),
            button("📄 查看完整日报", url="https://example.com/full-report",
                   button_type="primary"),
            note("🤖 obsidian-loop v2.1 · schema 2.0 · 邻近色环 turquoise+yellow+grey"),
        ],
    )

    import json
    print(json.dumps(card, ensure_ascii=False, indent=2))
"""
from typing import Optional, Union, List, Dict, Any
import json

# ============================================================
# 色系定义 (与 card_validator.py 一致)
# ============================================================

ALLOWED_TEMPLATES = {
    "turquoise", "blue", "green", "indigo", "violet", "red",
    "yellow", "wheat", "grey",
}

ALLOWED_BG_COLORS = {
    "default",
    "blue-50", "yellow-50", "grey-50", "green-50", "red-50",
    "turquoise-50", "indigo-50", "violet-50", "wheat-50",
}

ADJACENT_COLOR_GROUPS = {
    "turquoise": {"turquoise", "blue", "green"},
    "blue":      {"blue", "turquoise", "indigo", "violet"},
    "green":     {"green", "turquoise", "yellow"},
    "indigo":    {"indigo", "blue", "violet"},
    "violet":    {"violet", "indigo", "red", "blue"},
    "red":       {"red", "violet", "yellow"},
    "yellow":    {"yellow", "green", "red", "wheat"},
    "wheat":     {"wheat", "yellow"},
    "grey":      {"grey"},
}


class CardBuildError(ValueError):
    """卡片构建错误"""


def _check_bg_color(bg_color: str, header_template: str) -> None:
    """检查 bg_color 是否在 header_template 的邻近色环内

    语义中性色 (yellow-50 / grey-50) 与任何 header.template 搭配都允许,
    不计入 3 主色系限制. 主色系 = turquoise/blue/green/indigo/violet/red/wheat.
    """
    if bg_color == "default" or bg_color is None:
        return
    if bg_color not in ALLOWED_BG_COLORS:
        raise CardBuildError(
            f"background_style={bg_color!r} 不在允许列表 {sorted(ALLOWED_BG_COLORS)}"
        )
    hue = bg_color.split("-")[0]
    # yellow 和 grey 是语义中性色, 任何 header 模板都允许搭配
    if hue in {"yellow", "grey"}:
        return
    allowed = ADJACENT_COLOR_GROUPS.get(header_template, set()) | {"grey", "yellow"}
    if hue not in allowed:
        raise CardBuildError(
            f"background_style={bg_color!r} 不在 header.template={header_template!r} "
            f"的邻近色环内 (允许 = {sorted(allowed - {'grey', 'yellow'})} + grey/yellow)"
        )


# ============================================================
# Header
# ============================================================

def header(title: str,
           template: str = "blue",
           subtitle: Optional[str] = None,
           icon_token: Optional[str] = None) -> dict:
    """构建 Card 2.0 header

    Args:
        title: 标题 (建议格式 YYYYMMDD-类型-关键信息)
        template: 主题色, turquoise/blue/green/indigo/violet/red/yellow/wheat/grey
        subtitle: 副标题 (可选)
        icon_token: 图标 token (可选, 如 'myai_colorful')

    Returns:
        Card 2.0 header dict
    """
    if template not in ALLOWED_TEMPLATES:
        raise CardBuildError(
            f"template={template!r} 不在允许列表 {sorted(ALLOWED_TEMPLATES)}"
        )
    h = {
        "title": {"tag": "plain_text", "content": title},
        "template": template,
    }
    if subtitle:
        h["subtitle"] = {"tag": "plain_text", "content": subtitle}
    if icon_token:
        h["icon"] = {"tag": "standard_icon", "token": icon_token}
    return h


# ============================================================
# Body Elements
# ============================================================

def markdown(content: str) -> dict:
    """构建 markdown 元素 (替代废弃的 lark_md)"""
    return {"tag": "markdown", "content": content}


def hr() -> dict:
    """构建分隔线"""
    return {"tag": "hr"}


def column_block(content: str,
                 bg_color: Optional[str] = None,
                 header_template: Optional[str] = None,
                 weight: int = 1,
                 vertical_align: str = "top") -> dict:
    """构建单列 column_set + column 元素 (4 段式标准块)

    Args:
        content: markdown 内容
        bg_color: 背景色块, 如 'blue-50' / 'yellow-50' / 'grey-50' / 'default'
        header_template: 用于校验 bg_color 是否在邻近色环内 (强烈建议传)
        weight: column 权重, 默认 1
        vertical_align: 垂直对齐, 默认 'top'

    Returns:
        Card 2.0 column_set dict (含双重保险: column_set + column 都设 background_style)
    """
    if header_template and bg_color:
        _check_bg_color(bg_color, header_template)

    column = {
        "tag": "column",
        "width": "weighted",
        "weight": weight,
        "vertical_align": vertical_align,
        "elements": [{"tag": "markdown", "content": content}],
    }
    column_set = {
        "tag": "column_set",
        "flex_mode": "none",
        "columns": [column],
    }
    # 双重保险: column_set 和 column 都设 background_style
    # 注意: column_set / column 不支持 padding（飞书 API 报 230099），用 body.padding 统一控制
    if bg_color and bg_color != "default":
        column["background_style"] = bg_color
        column_set["background_style"] = bg_color
    return column_set


def columns_block(items: List[dict],
                  bg_color: Optional[str] = None,
                  header_template: Optional[str] = None,
                  weights: Optional[List[int]] = None) -> dict:
    """构建多列 column_set (用于 2/3 列统计块)

    Args:
        items: 每列的 markdown 内容列表, 如 [{"content": "📊 30篇", ...}]
        bg_color: 整体背景色 (所有列共用)
        header_template: 用于校验 bg_color
        weights: 每列权重, 默认每列等权

    Returns:
        Card 2.0 column_set dict
    """
    if header_template and bg_color:
        _check_bg_color(bg_color, header_template)

    n = len(items)
    if weights is None:
        weights = [1] * n
    if len(weights) != n:
        raise CardBuildError(f"weights 长度 {len(weights)} != items 长度 {n}")

    columns = []
    for item, w in zip(items, weights):
        content = item.get("content", "") if isinstance(item, dict) else str(item)
        col = {
            "tag": "column",
            "width": "weighted",
            "weight": w,
            "vertical_align": "top",
            "elements": [{"tag": "markdown", "content": content}],
        }
        if bg_color and bg_color != "default":
            col["background_style"] = bg_color
        columns.append(col)

    cs = {"tag": "column_set", "flex_mode": "none", "columns": columns}
    if bg_color and bg_color != "default":
        cs["background_style"] = bg_color
    return cs


def button(text: str,
           url: Optional[str] = None,
           button_type: str = "default",
           width: str = "fill",
           callback: Optional[dict] = None) -> dict:
    """构建 button 元素 (Card 2.0 直接用 button, 不要 action 包装)

    Args:
        text: 按钮文本
        url: 点击打开的 URL (open_url behavior)
        button_type: 'primary' / 'default' / 'danger'
        width: 'fill' / 'default'
        callback: 飞书回调对象 (替代 url, 用于交互卡片)

    Returns:
        Card 2.0 button dict
    """
    if button_type not in {"primary", "default", "danger"}:
        raise CardBuildError(f"button_type={button_type!r} 必须是 primary/default/danger")
    btn = {
        "tag": "button",
        "text": {"tag": "plain_text", "content": text},
        "type": button_type,
        "width": width,
    }
    if url:
        btn["behaviors"] = [{"type": "open_url", "default_url": url}]
    elif callback:
        btn["behaviors"] = [{"type": "callback", "value": callback}]
    else:
        btn["behaviors"] = []
    return btn


def note(content: str) -> dict:
    """构建 footer 来源标识（用 markdown 引用样式，note 元素已废弃）

    Card 2.0 V2 不再支持 note 元素，改用 markdown + > 引用样式作为 footer.
    保留 note() 函数名以兼容旧调用方，但返回 markdown 元素.
    """
    return {"tag": "markdown", "content": f"> {content}"}


# ============================================================
# 整卡构建
# ============================================================

def build_card(header: dict,
               elements: List[dict],
               wide_screen_mode: bool = True,
               update_multi: bool = True,
               padding: str = "16px 16px 16px 16px") -> dict:
    """组装完整 Card 2.0 dict

    Args:
        header: header() 函数返回的 dict
        elements: body.elements 列表 (markdown/column_block/hr/button/note=markdown 引用)
        wide_screen_mode: 宽屏模式
        update_multi: 多端更新同步
        padding: body 内边距（仅 body 支持，column_set/column 不支持）

    Returns:
        完整 Card 2.0 dict, 可直接 json.dumps 后通过飞书 OpenAPI 发送
    """
    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": wide_screen_mode,
            "update_multi": update_multi,
        },
        "header": header,
        "body": {
            "direction": "vertical",
            "padding": padding,
            "elements": elements,
        },
    }


# ============================================================
# 便捷预设 (常用报告类型)
# ============================================================

def stock_card(title: str, subtitle: str, main_block: str,
               highlight_block: str, stat_block: str,
               doc_url: Optional[str] = None,
               footer: Optional[str] = None) -> dict:
    """存量日报预设 (turquoise 系)"""
    elements = [
        column_block(main_block, bg_color="turquoise-50", header_template="turquoise"),
        hr(),
        column_block(highlight_block, bg_color="yellow-50", header_template="turquoise"),
        hr(),
        column_block(stat_block, bg_color="grey-50", header_template="turquoise"),
    ]
    if doc_url:
        elements.append(hr())
        elements.append(button("📄 查看完整存量日报", url=doc_url, button_type="primary"))
    if footer:
        elements.append(note(footer))
    return build_card(
        header=header(title, template="turquoise", subtitle=subtitle),
        elements=elements,
    )


def flow_card(title: str, subtitle: str, main_block: str,
              secondary_block: str, fusion_block: str,
              stat_block: str,
              doc_url: Optional[str] = None,
              footer: Optional[str] = None) -> dict:
    """增量日报预设 (blue 系)"""
    elements = [
        column_block(main_block, bg_color="blue-50", header_template="blue"),
        hr(),
        column_block(secondary_block, bg_color="default", header_template="blue"),
        hr(),
        column_block(fusion_block, bg_color="yellow-50", header_template="blue"),
        hr(),
        column_block(stat_block, bg_color="grey-50", header_template="blue"),
    ]
    if doc_url:
        elements.append(hr())
        elements.append(button("📄 查看完整增量日报", url=doc_url, button_type="primary"))
    if footer:
        elements.append(note(footer))
    return build_card(
        header=header(title, template="blue", subtitle=subtitle),
        elements=elements,
    )


def action_card(title: str, subtitle: str, actions: List[dict],
                prompt_block: Optional[str] = None,
                doc_url: Optional[str] = None,
                prompt_url: Optional[str] = None,
                footer: Optional[str] = None) -> dict:
    """行动清单预设 (green 系)

    Args:
        actions: 行动列表, 每项 dict 含 content + bg_color ('green-50'/'default')
    """
    elements = []
    for i, act in enumerate(actions):
        elements.append(column_block(
            act["content"],
            bg_color=act.get("bg_color", "green-50"),
            header_template="green",
        ))
        if i < len(actions) - 1:
            elements.append(hr())
    if prompt_block:
        elements.append(hr())
        elements.append(column_block(prompt_block, bg_color="yellow-50",
                                     header_template="green"))
    if prompt_url:
        elements.append(hr())
        elements.append(button("📋 复制提示词并开始", url=prompt_url, button_type="primary"))
    if doc_url:
        elements.append(button("📄 查看完整行动清单", url=doc_url, button_type="default"))
    if footer:
        elements.append(note(footer))
    return build_card(
        header=header(title, template="green", subtitle=subtitle),
        elements=elements,
    )


def health_card(title: str, subtitle: str, critical_block: str,
                important_block: str, stat_block: str,
                fix_url: Optional[str] = None,
                doc_url: Optional[str] = None,
                footer: Optional[str] = None) -> dict:
    """健康报告预设 (red 系)"""
    elements = [
        column_block(critical_block, bg_color="red-50", header_template="red"),
        hr(),
        column_block(important_block, bg_color="yellow-50", header_template="red"),
        hr(),
        column_block(stat_block, bg_color="grey-50", header_template="red"),
    ]
    if fix_url:
        elements.append(hr())
        elements.append(button("🔧 立即修复 Critical 项", url=fix_url, button_type="primary"))
    if doc_url:
        elements.append(button("📄 查看完整健康报告", url=doc_url, button_type="default"))
    if footer:
        elements.append(note(footer))
    return build_card(
        header=header(title, template="red", subtitle=subtitle),
        elements=elements,
    )


def weekly_card(title: str, subtitle: str, trend_block: str,
                emergence_block: str, stat_block: str, next_week_block: str,
                doc_url: Optional[str] = None,
                footer: Optional[str] = None) -> dict:
    """周报预设 (indigo 系)"""
    elements = [
        column_block(trend_block, bg_color="indigo-50", header_template="indigo"),
        hr(),
        column_block(emergence_block, bg_color="yellow-50", header_template="indigo"),
        hr(),
        column_block(stat_block, bg_color="grey-50", header_template="indigo"),
        hr(),
        column_block(next_week_block, bg_color="default", header_template="indigo"),
    ]
    if doc_url:
        elements.append(hr())
        elements.append(button("📄 查看完整周报", url=doc_url, button_type="primary"))
    if footer:
        elements.append(note(footer))
    return build_card(
        header=header(title, template="indigo", subtitle=subtitle),
        elements=elements,
    )


# ============================================================
# CLI 自检
# ============================================================

if __name__ == "__main__":
    # 自检: 生成一份 demo 卡片并打印
    demo = stock_card(
        title="20260719-存量日报-归档30篇-Atoms18条",
        subtitle="2026-07-19 · obsidian-loop v2.1 · 04:00 自动生成",
        main_block="📦 **归档概览**\n\n| 来源 | 篇数 |\n|------|------|\n| waytoagi | 12 |\n| 公众号 | 8 |",
        highlight_block="💎 **5★ 精选**\n\n**atom-07** · 排期是关键\n> 「整理没用, 排期才有用。」—— 卡尔",
        stat_block="📊 **统计**\n- 30 篇 / 18 atoms / 22% 覆盖率",
        doc_url="https://example.com/stock-report",
        footer="🤖 obsidian-loop v2.1 · schema 2.0 · 邻近色环 turquoise+yellow+grey",
    )
    print(json.dumps(demo, ensure_ascii=False, indent=2))
