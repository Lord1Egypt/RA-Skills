#!/usr/bin/env python3
"""Feishu (Lark) headline card builder — 构造周报头条 interactive 卡片。

设计原则（沿用 skill 合规约束）：
- 仅负责**构造** interactive 卡片（消息卡片），承载本周头条速览 + 三视角看点 + 分角色摘要
  + 「查看完整周报」按钮（链接带 ?src=feishu&uid= 度量参数）。
- 防御式处理 report 各字段，任一缺失都不崩，缺失段落自动跳过。
- 发送通道已迁移至飞书连接器（delivery/feishu_connector.py，经 lark-cli，密钥不落盘）；
  本模块不再持有任何 webhook 发送逻辑。

飞书卡片协议（精简）：card = {"msg_type": "interactive", "card": {...}}
（实际发送由连接器走 lark-cli `api POST /open-apis/im/v1/messages`）。
"""
from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger("aiweekly.delivery.feishu")

# 角色 icon 映射（audience_summary 中文键）
_ROLE_ICON = {
    "开发者": "🧑\u200d💻",
    "AI 产品经理": "🧑\u200d💼",
    "科技媒体工作者": "📝",
    "PM": "🧑\u200d💼",
    "自媒体": "📝",
}

# 合法卡片链接：仅允许 http/https，且不含空白与括号（避免飞书链接语法破坏）
_URL_RE = re.compile(r"^https?://[^\s()<>]+$")


def _md_escape(text: str) -> str:
    """转义飞书 lark_md 的控制字符，防止不可信 RSS 内容破坏卡片排版。

    只用于用户/外部内容（标题、摘要、看点、关键词）；模板自带的 ``**`` ``_``
    等强调符由调用方负责、不在此转义。
    转义集：反斜杠、反引号、``*``、``_``、``~``、``[ ] ( )``、``>``、``#``。
    """
    if not text:
        return ""
    rep = (
        ("\\", "＼"), ("`", "｀"), ("*", "＊"), ("_", "＿"),
        ("~", "～"), ("[", "［"), ("]", "］"),
        ("(", "（"), (")", "）"), (">", "〉"), ("#", "＃"),
    )
    for a, b in rep:
        text = text.replace(a, b)
    return text


def _safe_url(url: str) -> str:
    """返回可通过飞书链接语法安全嵌入的 URL；不合法则返回空串（降级为纯文本）。"""
    u = (url or "").strip()
    return u if _URL_RE.match(u) else ""


def _truncate(text: str, n: int) -> str:
    text = (text or "").strip()
    return text[:n] + ("…" if len(text) > n else "") if text else ""


def build_headline_card(report: dict[str, Any]) -> dict[str, Any]:
    """从 report.json 头条载荷构造飞书 interactive 卡片。

    report 期望字段（全部可选，缺失即跳过该段落）：
      week, generated_at, lead,
      headlines[{title,url,summary,source,category,mustRead}],
      insights[{kicker,title,insight}],
      audience{dict: 角色->摘要},
      keywords[{term,tag}],
      view_url, view_label
    """
    report = report or {}
    week = _md_escape(report.get("week") or "本周")

    header = {
        "title": {"tag": "plain_text", "content": f"📊 AI 行业周报 · {week}"},
        "template": "blue",
    }
    elements: list[dict[str, Any]] = []

    # 1) 本周主线
    lead = report.get("lead")
    if lead:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": f"**本周主线**\n{_md_escape(_truncate(lead, 120))}"},
        })

    # 2) 本周重点（headlines，按分数排序取前 5）
    headlines = [h for h in (report.get("headlines") or []) if h.get("title")]
    if headlines:
        lines = ["**🔥 本周重点**"]
        for i, h in enumerate(headlines[:5], 1):
            title = _md_escape(h.get("title", ""))
            url = _safe_url(h.get("url", ""))
            summary = _md_escape(_truncate(h.get("summary", ""), 56))
            src = _md_escape(h.get("source", ""))
            must = " 🔥" if h.get("mustRead") else ""
            t = f"[{title}]({url})" if url else title
            line = f"{i}. {t}{must}"
            if src or summary:
                tail = " · ".join(x for x in [src, summary] if x)
                line += f"\n   _{tail}_" if tail else ""
            lines.append(line)
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}})

    # 3) 本周看点（insights，取前 3）
    insights = [x for x in (report.get("insights") or []) if x.get("title")]
    if insights:
        lines = ["**💡 本周看点**"]
        for ins in insights[:3]:
            kicker = _md_escape(ins.get("kicker", ""))
            title = _md_escape(ins.get("title", ""))
            insight = _md_escape(_truncate(ins.get("insight", ""), 70))
            head = f"{kicker} · {title}" if kicker else title
            line = f"• **{head}**"
            if insight:
                line += f"\n  {insight}"
            lines.append(line)
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}})

    # 4) 给不同角色（audience_summary）
    audience = report.get("audience") or {}
    if isinstance(audience, dict) and audience:
        lines = ["**👥 给不同角色**"]
        for role, text in audience.items():
            if not text:
                continue
            icon = _ROLE_ICON.get(role, "•")
            lines.append(f"{icon} **{_md_escape(role)}**：{_md_escape(_truncate(str(text), 80))}")
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}})

    # 5) 本周关键词（publish 已按优先级排好序，[:6] 截断不丢保送词）
    keywords = [_md_escape(k.get("term", "")) for k in (report.get("keywords") or []) if k.get("term")]
    if keywords:
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": f"**🔖 本周关键词**：{'、'.join(keywords[:6])}"},
        })

    # 6) 查看完整周报（按钮 / 回退 note）
    view_url = _safe_url(report.get("view_url") or "")
    if view_url:
        elements.append({
            "tag": "action",
            "actions": [{
                "tag": "button",
                "text": {"tag": "plain_text", "content": report.get("view_label", "查看完整周报")},
                "type": "primary",
                "url": view_url,
            }],
        })
    else:
        elements.append({
            "tag": "note",
            "elements": [{"tag": "plain_text",
                          "content": report.get("view_label", "完整周报见本地生成的 HTML 文件")}],
        })

    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": header,
            "elements": elements,
        },
    }
