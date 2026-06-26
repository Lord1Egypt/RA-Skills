#!/usr/bin/env python3
"""
日报 HTML 渲染器

输入：output/daily/{date}.json
输出：output/daily/{date}.html

目标：让 AI 只负责生成结构化日报数据，由脚本负责稳定输出 HTML，
避免每次都由模型重写整页结构、样式和反馈脚本。
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import sys
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output" / "daily"
ARCHIVE_DIR = ROOT_DIR / "output" / "archive"


def load_profile_window_days(default: int = 3) -> int:
    """从 profile.yaml 读取 collection.window_days，读取失败时返回默认值。"""
    config_path = ROOT_DIR / "config" / "profile.yaml"
    if not config_path.exists():
        return default
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        return int(cfg.get("collection", {}).get("window_days", default))
    except Exception:
        # pyyaml 不可用或解析失败，简单正则提取
        try:
            import re
            text = config_path.read_text(encoding="utf-8")
            m = re.search(r"window_days\s*:\s*(\d+)", text)
            return int(m.group(1)) if m else default
        except Exception:
            return default

PRIORITY_ICON = {
    "major": '<i class="fa-solid fa-fire text-red-500 mr-1.5 text-xs"></i>',
    "notable": '<i class="fa-solid fa-thumbtack text-amber-500 mr-1.5 text-xs"></i>',
    "normal": "",
}

SOURCE_TIER_BADGE = {
    "tier-1": '<span class="inline-flex items-center gap-0.5 text-[10px] text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded ml-1.5" title="官方一手来源"><i class="fa-solid fa-shield-halved text-[9px]"></i>一手</span>',
    "tier-2": '<span class="inline-flex items-center gap-0.5 text-[10px] text-blue-500 bg-blue-50 px-1.5 py-0.5 rounded ml-1.5" title="主流媒体来源"><i class="fa-solid fa-newspaper text-[9px]"></i>媒体</span>',
    "tier-3": '<span class="inline-flex items-center gap-0.5 text-[10px] text-gray-400 bg-gray-50 px-1.5 py-0.5 rounded ml-1.5" title="社区来源"><i class="fa-solid fa-users text-[9px]"></i>社区</span>',
}

CONFIDENCE_ICON = {
    "high": '<span class="inline-flex items-center gap-0.5 text-[10px] text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded ml-1" title="高置信度"><i class="fa-solid fa-circle-check text-[9px]"></i>高可信</span>',
    "medium": '<span class="inline-flex items-center gap-0.5 text-[10px] text-amber-500 bg-amber-50 px-1.5 py-0.5 rounded ml-1" title="中等置信度"><i class="fa-solid fa-circle-minus text-[9px]"></i>待验证</span>',
    "low": '<span class="inline-flex items-center gap-0.5 text-[10px] text-red-400 bg-red-50 px-1.5 py-0.5 rounded ml-1" title="低置信度"><i class="fa-solid fa-circle-exclamation text-[9px]"></i>存疑</span>',
}

ACTION_META = {
    "learn": {
        "label": "建议学习",
        "icon": "fa-solid fa-book-open",
        "icon_class": "text-blue-500",
        "title_class": "text-blue-600",
    },
    "try": {
        "label": "建议尝试",
        "icon": "fa-solid fa-wrench",
        "icon_class": "text-emerald-500",
        "title_class": "text-emerald-600",
    },
    "watch": {
        "label": "持续关注",
        "icon": "fa-solid fa-eye",
        "icon_class": "text-amber-500",
        "title_class": "text-amber-600",
    },
    "alert": {
        "label": "需要警惕",
        "icon": "fa-solid fa-triangle-exclamation",
        "icon_class": "text-red-500",
        "title_class": "text-red-600",
    },
}

TREND_META = {
    "rising": {
        "label": "上升",
        "icon": "fa-solid fa-arrow-trend-up",
        "icon_class": "text-emerald-500",
        "label_class": "text-emerald-600",
        "tag_class": "bg-emerald-50 text-emerald-700",
    },
    "cooling": {
        "label": "消退",
        "icon": "fa-solid fa-arrow-trend-down",
        "icon_class": "text-gray-400",
        "label_class": "text-gray-500",
        "tag_class": "bg-gray-50 text-gray-500",
    },
    "steady": {
        "label": "持续",
        "icon": "fa-solid fa-fire",
        "icon_class": "text-red-500",
        "label_class": "text-red-600",
        "tag_class": "bg-red-50 text-red-600",
    },
}


def h(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def serialize_tags_attr(tags: list[str]) -> str:
    raw = json.dumps(tags, ensure_ascii=False)
    return base64.b64encode(raw.encode("utf-8")).decode("ascii")


def join_html(parts: list[str]) -> str:
    return "\n".join(part for part in parts if part)


def render_date_label(meta: dict[str, Any]) -> str:
    label = meta.get("date_label")
    if label:
        return h(label)
    date_str = meta.get("date")
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return f"{dt.year}年{dt.month}月{dt.day}日 · {weekdays[dt.weekday()]}"
    except ValueError:
        return h(date_str)


def render_tags(tags: list[str], exploration: bool = False) -> str:
    classes = "bg-gray-100 text-gray-500" if exploration else "bg-[#F3F0FF] text-accent"
    return "".join(
        f'<span class="{classes} text-[11px] px-2.5 py-0.5 rounded-full">{h(tag)}</span>'
        for tag in tags
    )


def render_summary(summary: dict[str, Any] | str) -> str:
    if isinstance(summary, dict):
        what_happened = h(summary.get("what_happened", ""))
        why_it_matters = h(summary.get("why_it_matters", ""))
        parts = []
        if what_happened:
            parts.append(
                '<p class="mb-0.5"><strong class="text-gray-700">发生了什么：</strong>'
                f"{what_happened}</p>"
            )
        if why_it_matters:
            parts.append(
                '<p><strong class="text-gray-700">为什么重要：</strong>'
                f"{why_it_matters}</p>"
            )
        return join_html(parts)
    return h(summary)


def normalize_meta(meta: Any) -> dict[str, Any]:
    if not isinstance(meta, dict):
        raise ValueError("payload.meta 必须存在且为对象")
    date = meta.get("date")
    if not isinstance(date, str) or not date.strip():
        raise ValueError("payload.meta.date 缺失或不是有效字符串")
    # 用实际渲染时间覆盖，确保页面显示的时间准确
    now = datetime.now()
    return {
        "date": date.strip(),
        "date_label": meta.get("date_label", ""),
        "generated_at": now.strftime("%Y-%m-%d %H:%M"),
        "generated_time": now.strftime("%H:%M"),
        "role": meta.get("role", ""),
    }


def normalize_actions(items: Any) -> list[dict[str, Any]]:
    if items is None:
        return []
    if not isinstance(items, list):
        raise ValueError("payload.left_sidebar.actions 必须为数组")
    normalized = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"payload.left_sidebar.actions[{idx}] 必须为对象")
        action_type = item.get("type", "watch")
        if action_type not in ACTION_META:
            action_type = "watch"
        normalized.append(
            {"type": action_type, "text": item.get("text", ""), "prompt": item.get("prompt", "")}
        )
    return normalized


def normalize_overview(items: Any) -> list[dict[str, Any]]:
    if items is None:
        return []
    if not isinstance(items, list):
        raise ValueError("payload.left_sidebar.overview 必须为数组")
    normalized = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"payload.left_sidebar.overview[{idx}] 必须为对象")
        normalized.append({"title": item.get("title", ""), "text": item.get("text", "")})
    return normalized


def normalize_trends(trends: Any) -> dict[str, Any]:
    if trends is None:
        return {"rising": [], "cooling": [], "steady": [], "insight": ""}
    if not isinstance(trends, dict):
        raise ValueError("payload.left_sidebar.trends 必须为对象")

    def ensure_tag_list(name: str) -> list[str]:
        value = trends.get(name, [])
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValueError(f"payload.left_sidebar.trends.{name} 必须为数组")
        return [str(tag) for tag in value]

    return {
        "rising": ensure_tag_list("rising"),
        "cooling": ensure_tag_list("cooling"),
        "steady": ensure_tag_list("steady"),
        "insight": trends.get("insight", ""),
    }


def normalize_articles(items: Any) -> list[dict[str, Any]]:
    if items is None:
        return []
    if not isinstance(items, list):
        raise ValueError("payload.articles 必须为数组")
    normalized = []
    for idx, article in enumerate(items, start=1):
        if not isinstance(article, dict):
            raise ValueError(f"payload.articles[{idx}] 必须为对象")
        tags = article.get("tags", [])
        if tags is None:
            tags = []
        if not isinstance(tags, list):
            raise ValueError(f"payload.articles[{idx}].tags 必须为数组")
        priority = article.get("priority", "normal")
        if priority not in PRIORITY_ICON:
            priority = "normal"
        summary = article.get("summary", "")
        if not isinstance(summary, (dict, str)):
            raise ValueError(f"payload.articles[{idx}].summary 必须为字符串或对象")
        credibility = article.get("credibility")
        if credibility is not None and not isinstance(credibility, dict):
            credibility = None
        normalized.append(
            {
                "id": article.get("id") or f"article-{idx}",
                "title": article.get("title", ""),
                "priority": priority,
                "time_label": article.get("time_label", ""),
                "source_date": article.get("source_date", ""),
                "source": article.get("source", ""),
                "url": article.get("url", "#"),
                "summary": summary,
                "relevance": article.get("relevance", ""),
                "tags": [str(tag) for tag in tags],
                "is_exploration": bool(article.get("is_exploration")),
                "credibility": credibility,
            }
        )
    return normalized


def normalize_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("payload 顶层必须为对象")

    left_sidebar = payload.get("left_sidebar", {})
    if not isinstance(left_sidebar, dict):
        raise ValueError("payload.left_sidebar 必须为对象")

    data_sources = payload.get("data_sources", [])
    if data_sources is None:
        data_sources = []
    if not isinstance(data_sources, list):
        raise ValueError("payload.data_sources 必须为数组")

    return {
        "meta": normalize_meta(payload.get("meta")),
        "raw_capture_path": payload.get("raw_capture_path", ""),
        "left_sidebar": {
            "overview": normalize_overview(left_sidebar.get("overview", [])),
            "actions": normalize_actions(left_sidebar.get("actions", [])),
            "trends": normalize_trends(left_sidebar.get("trends", {})),
        },
        "articles": normalize_articles(payload.get("articles", [])),
        "data_sources": [str(source) for source in data_sources],
    }


def render_credibility_badges(credibility: dict[str, Any] | None) -> str:
    """渲染置信度、来源等级和交叉引用徽章。"""
    if not credibility:
        return ""
    parts: list[str] = []
    tier = credibility.get("source_tier", "")
    if tier in SOURCE_TIER_BADGE:
        parts.append(SOURCE_TIER_BADGE[tier])
    conf = credibility.get("confidence", "")
    if conf in CONFIDENCE_ICON:
        parts.append(CONFIDENCE_ICON[conf])
    cross = credibility.get("cross_refs")
    if isinstance(cross, int) and cross >= 2:
        # 构建 tooltip 内容：优先用 sources 数组渲染可点击链接，fallback 到 evidence 文本
        sources_list = credibility.get("sources", [])
        if isinstance(sources_list, list) and sources_list:
            link_items = []
            for src in sources_list:
                if not isinstance(src, dict):
                    continue
                name = h(src.get("name", ""))
                url = src.get("url", "")
                if name and url:
                    link_items.append(
                        f'<a href="{h(url)}" target="_blank" '
                        f'class="cred-tooltip-link">{name}'
                        f'<i class="fa-solid fa-arrow-up-right-from-square text-[8px] ml-0.5 opacity-60"></i></a>'
                    )
                elif name:
                    link_items.append(f'<span class="text-gray-300">{name}</span>')
            tooltip_content = "".join(
                f'<span class="cred-tooltip-row">{item}</span>' for item in link_items
            )
        else:
            tooltip_content = h(credibility.get("evidence", f"{cross} 个来源交叉报道"))
        parts.append(
            f'<span class="cred-tooltip inline-flex items-center gap-0.5 text-[10px] text-violet-500 bg-violet-50 px-1.5 py-0.5 rounded ml-1 cursor-help">'
            f'<i class="fa-solid fa-code-merge text-[9px]"></i>{cross}源验证'
            f'<span class="cred-tooltip-text">{tooltip_content}</span>'
            f'</span>'
        )
    return "".join(parts)


def render_article(article: dict[str, Any], index: int) -> str:
    article_id = article.get("id") or f"article-{index}"
    exploration = bool(article.get("is_exploration"))
    priority = article.get("priority", "normal")
    border = " border border-dashed border-gray-200" if exploration else ""
    icon = PRIORITY_ICON.get(priority, "")
    title = h(article.get("title", ""))
    time_label = h(article.get("time_label", ""))
    source = h(article.get("source", ""))
    url = h(article.get("url", "#"))
    relevance = h(article.get("relevance", ""))
    tags = article.get("tags", [])
    title_prefix = (
        '<i class="fa-solid fa-compass text-gray-400 mr-1.5 text-xs"></i>'
        '<span class="text-gray-400 text-[11px] font-normal mr-1.5">拓展</span>'
        if exploration
        else icon
    )
    relevance_block = ""
    if relevance:
        relevance_block = (
            '<div class="bg-[#F8F7FF] rounded-lg px-3 py-2 text-[13px] text-gray-700 my-2">'
            '<i class="fa-solid fa-lightbulb text-accent mr-1"></i>'
            f"<strong>与你相关：</strong>{relevance}</div>"
        )

    cred_badges = render_credibility_badges(article.get("credibility"))

    raw_summary = article.get("summary", "")
    if isinstance(raw_summary, dict):
        summary_text = raw_summary.get("what_happened", "") or raw_summary.get("why_it_matters", "")
    else:
        summary_text = str(raw_summary)
    summary_snippet = h(summary_text[:120])
    source_url = h(article.get("url", ""))
    article_date = h(article.get("source_date", ""))

    return f"""        <article class="bg-white rounded-xl shadow-sm p-4 card-hover{border}"
                 data-article-id="{h(article_id)}" data-title="{title}" data-tags="{h(serialize_tags_attr(tags))}"
                 data-summary="{summary_snippet}" data-url="{source_url}" data-priority="{h(priority)}" data-date="{article_date}">
          <div class="flex items-start justify-between">
            <h3 class="text-[15px] font-semibold text-primary leading-snug">{title_prefix}{title}</h3>
            <span class="text-xs text-gray-400 whitespace-nowrap ml-3">{time_label}</span>
          </div>
          <p class="text-xs text-gray-400 mt-1"><i class="fa-solid fa-link mr-1"></i>{source}{cred_badges}</p>
          <div class="ai-gradient-line pl-3 my-2.5 text-[13px] text-gray-600 leading-relaxed">
            {render_summary(article.get("summary", ""))}
          </div>
          {relevance_block}
          <div class="mt-2 sm:flex sm:items-center sm:justify-between">
            <div class="flex gap-1.5 flex-wrap">{render_tags(tags, exploration=exploration)}</div>
            <div class="article-action-bar flex items-center mt-1.5 sm:mt-0 sm:ml-3">
              <a href="{url}" target="_blank" class="text-accent text-xs hover:underline whitespace-nowrap sm:hidden">
                <i class="fa-solid fa-arrow-up-right-from-square mr-1"></i>原文
              </a>
              <span class="btn-group flex items-center gap-2 ml-auto sm:ml-0"></span>
              <a href="{url}" target="_blank" class="text-accent text-xs hover:underline whitespace-nowrap hidden sm:inline ml-3">
                <i class="fa-solid fa-arrow-up-right-from-square mr-1"></i>原文
              </a>
            </div>
          </div>
        </article>"""


def render_overview(items: list[dict[str, Any]]) -> str:
    lines = []
    for idx, item in enumerate(items, start=1):
        lines.append(
            f"""            <li class="flex gap-2.5 items-start">
              <span class="flex-shrink-0 w-5 h-5 rounded-full bg-accent text-white text-[10px] font-bold flex items-center justify-center mt-0.5">{idx}</span>
              <span class="text-gray-700"><strong class="text-primary">{h(item.get("title", ""))}</strong>：{h(item.get("text", ""))}</span>
            </li>"""
        )
    return join_html(lines)


def render_actions(items: list[dict[str, Any]]) -> str:
    lines = []
    for item in items:
        meta = ACTION_META.get(item.get("type", "watch"), ACTION_META["watch"])
        lines.append(
            f"""            <li class="action-item flex items-start gap-2.5 ai-bg rounded-lg px-3 py-2.5"
                data-action-type="{h(item.get("type", "watch"))}"
                data-action-prompt="{h(item.get("prompt", ""))}">
              <i class="{meta["icon"]} {meta["icon_class"]} mt-0.5 text-sm"></i>
              <div class="flex-1">
                <strong class="{meta["title_class"]}">{meta["label"]}</strong>
                <p class="text-gray-600 mt-0.5 leading-relaxed">{h(item.get("text", ""))}</p>
              </div>
            </li>"""
        )
    return join_html(lines)


def render_trends(trends: dict[str, Any]) -> str:
    blocks = []
    for key in ("rising", "cooling", "steady"):
        meta = TREND_META[key]
        tags = "".join(
            f'<span class="{meta["tag_class"]} text-[11px] px-2 py-0.5 rounded-full">{h(tag)}</span>'
            for tag in trends.get(key, [])
        )
        blocks.append(
            f"""            <div class="flex items-center gap-2">
              <span class="flex-shrink-0 w-12 text-right"><i class="{meta["icon"]} {meta["icon_class"]} text-xs mr-0.5"></i><strong class="{meta["label_class"]} text-[11px]">{meta["label"]}</strong></span>
              <div class="flex gap-1.5 flex-wrap">{tags}</div>
            </div>"""
        )

    insight = h(trends.get("insight", ""))
    blocks.append(
        '          <div class="ai-bg rounded-lg px-3 py-3">'
        '            <p class="text-[12px] text-gray-600 leading-relaxed">'
        '              <i class="fa-solid fa-wand-magic-sparkles text-accent mr-1"></i>'
        f'              <strong class="text-primary">AI 洞察：</strong>{insight}'
        "            </p>"
        "          </div>"
    )
    return join_html(blocks)


def render_html(payload: dict[str, Any]) -> str:
    meta = payload.get("meta", {})
    left = payload.get("left_sidebar", {})
    articles = payload.get("articles", [])
    article_items = "\n".join(
        render_article(article, index) for index, article in enumerate(articles, start=1)
    )
    data_sources = h("、".join(payload.get("data_sources", [])))
    title_date = h(meta.get("date", ""))
    date_label = render_date_label(meta)
    item_count = len(articles)
    generated_at = h(meta.get("generated_at", ""))
    role = h(meta.get("role", ""))
    site_title = h(f"{role}日报" if role else "每日情报")
    generated_time = h(meta.get("generated_time", ""))

    default_tools = [
        {"id": "claude", "name": "Claude", "icon": "fa-solid fa-message", "btnClass": "btn-claude", "url": "https://claude.ai/new?q={prompt}"},
        {"id": "chatgpt", "name": "ChatGPT", "icon": "fa-brands fa-openai", "btnClass": "btn-chatgpt", "url": "https://chatgpt.com/?q={prompt}"},
        {"id": "deepseek", "name": "DeepSeek", "icon": "fa-solid fa-magnifying-glass", "btnClass": "btn-deepseek", "url": "https://chat.deepseek.com/?q={prompt}"},
        {"id": "copy", "name": "\u590d\u5236 Prompt", "icon": "fa-regular fa-copy", "btnClass": "btn-copy", "url": None},
    ]
    tools_data = payload.get("tools", default_tools)
    tools_js = json.dumps(tools_data, ensure_ascii=False)

    # OG 标签：取前3条 major/notable 文章标题作为摘要
    top_articles = [
        a for a in articles if a.get("priority") in ("major", "notable")
    ][:3]
    if not top_articles:
        top_articles = articles[:3]

    _icons = ["🔥", "🚀", "📌"]

    def _display_width(s: str) -> int:
        """计算显示宽度：CJK 字符 = 2，其他 = 1。"""
        w = 0
        for c in s:
            cp = ord(c)
            if (0x1100 <= cp <= 0x115F or 0x2E80 <= cp <= 0xA4CF or
                    0xAC00 <= cp <= 0xD7A3 or 0xF900 <= cp <= 0xFAFF or
                    0xFE10 <= cp <= 0xFE6F or 0xFF00 <= cp <= 0xFF60 or
                    0xFFE0 <= cp <= 0xFFE6):
                w += 2
            else:
                w += 1
        return w

    def _shorten_by_width(title: str, max_width: int) -> str:
        """先提取冒号前主干，再按显示宽度在词边界截断（不在词中间截断）。"""
        for sep in ("：", ":", "——", "—", " - "):
            if sep in title:
                title = title.split(sep)[0].strip()
                break
        if _display_width(title) <= max_width:
            return title
        # 逐词累加，找到加下一个词后超出 max_width-1（留省略号位）时停止
        words = title.split(" ")
        result = ""
        for word in words:
            candidate = (result + " " + word).strip()
            if _display_width(candidate) > max_width - 1:
                break
            result = candidate
        return (result + "…") if result else title[:max_width - 1] + "…"

    # og:title：第一条头条（显示宽度 24，词边界截断）
    # og:description：后两条头条（每条显示宽度 18，用 · 分隔）
    og_title = h(f"{_icons[0]} {_shorten_by_width(top_articles[0].get('title', ''), 24)}" if top_articles else site_title)
    og_desc_parts = [
        f"{_icons[i + 1]} {_shorten_by_width(a.get('title', ''), 18)}"
        for i, a in enumerate(top_articles[1:3])
    ]
    og_description = h(" · ".join(og_desc_parts)) if og_desc_parts else h(site_title)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>日报 · {title_date}</title>
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{site_title}">
  <meta name="description" content="{og_description}">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            primary: '#1A1A2E',
            accent: '#6C5CE7',
            'accent-hover': '#5A4BD1',
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    .ai-gradient-line {{ border-left: 3px solid; border-image: linear-gradient(to bottom, #6C5CE7, #3B82F6) 1; }}
    .ai-bg {{ background: linear-gradient(135deg, #F8F7FF, #F0F7FF); }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif; }}
    .card-hover {{ transition: box-shadow 0.2s ease, transform 0.2s ease; }}
    .card-hover:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-1px); }}
    .sidebar-scroll::-webkit-scrollbar {{ width: 4px; }}
    .sidebar-scroll::-webkit-scrollbar-track {{ background: transparent; }}
    .sidebar-scroll::-webkit-scrollbar-thumb {{ background: #E5E7EB; border-radius: 2px; }}
    .feed-scroll::-webkit-scrollbar {{ width: 5px; }}
    .feed-scroll::-webkit-scrollbar-track {{ background: transparent; }}
    .feed-scroll::-webkit-scrollbar-thumb {{ background: #E5E7EB; border-radius: 3px; }}

    .vote-btn {{ cursor: pointer; user-select: none; transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 12px; border: 1px solid #E5E7EB; background: #F9FAFB; color: #6B7280; font-size: 12px; }}
    .vote-btn:hover {{ border-color: #6C5CE7; color: #6C5CE7; background: #F5F3FF; }}
    .vote-btn.voted {{ border-color: #6C5CE7; color: #6C5CE7; background: #EDE9FE; font-weight: 600; }}
    .bookmark-btn {{ cursor: pointer; user-select: none; transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 12px; border: 1px solid #E5E7EB; background: #F9FAFB; color: #6B7280; font-size: 12px; }}
    .bookmark-btn:hover {{ border-color: #F59E0B; color: #F59E0B; background: #FFFBEB; }}
    .bookmark-btn.bookmarked {{ border-color: #F59E0B; color: #D97706; background: #FEF3C7; font-weight: 600; }}
    @media (max-width: 639px) {{
      .vote-btn, .bookmark-btn {{ font-size: 14px; padding: 6px 14px; border-radius: 14px; gap: 5px; }}
    }}
    .tag-clickable {{ cursor: pointer; transition: all 0.15s ease; }}
    .tag-clickable:hover {{ transform: scale(1.05); box-shadow: 0 1px 4px rgba(108,92,231,0.2); }}
    .tag-clickable.tag-clicked {{ background: #6C5CE7 !important; color: white !important; }}

    .action-item {{ position: relative; }}
    .ai-trigger-wrap {{
      position: absolute; top: 4px; right: 4px;
      display: flex; align-items: flex-start; z-index: 50;
      pointer-events: none;
    }}
    .ai-trigger-icon {{
      width: 26px; height: 26px; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      color: #C4B5FD; font-size: 12px; cursor: pointer;
      transition: all 0.15s ease; flex-shrink: 0;
      pointer-events: auto;
    }}
    .ai-trigger-icon:hover {{ background: #6C5CE7; color: white; }}
    .ai-menu {{
      background: white; border-radius: 10px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.12), 0 1px 3px rgba(0,0,0,0.06);
      padding: 6px; min-width: 156px;
      opacity: 0; pointer-events: none;
      transform: translateX(8px);
      transition: opacity 0.18s ease, transform 0.18s ease;
      margin-right: 4px;
    }}
    .ai-menu.open {{ opacity: 1; pointer-events: auto; transform: translateX(0); }}
    .ai-menu-item {{
      display: flex; align-items: center; gap: 8px;
      padding: 7px 12px; border-radius: 7px; font-size: 12px;
      color: #4B5563; cursor: pointer; transition: background 0.12s ease; white-space: nowrap;
    }}
    .ai-menu-item:hover {{ background: #F5F3FF; color: #6C5CE7; }}
    .ai-menu-item i {{ width: 16px; text-align: center; font-size: 13px; }}
    .ai-menu-item .item-icon-claude {{ color: #C96E2B; }}
    .ai-menu-item .item-icon-chatgpt {{ color: #0FA47F; }}
    .ai-menu-item .item-icon-deepseek {{ color: #2563EB; }}
    .ai-menu-item .item-icon-copy {{ color: #9CA3AF; }}
    .ai-menu-sep {{ height: 1px; background: #F3F4F6; margin: 4px 8px; }}

    .card-ai-wrap {{ position: relative; flex-shrink: 0; }}
    .card-ai-wrap .ai-menu {{ position: absolute; bottom: calc(100% + 6px); right: 0; margin-right: 0; }}
    .card-ai-btn {{
      display: inline-flex; align-items: center; gap: 3px;
      padding: 2px 8px; border-radius: 6px; font-size: 11px;
      cursor: pointer; transition: all 0.15s ease; color: #C4B5FD; white-space: nowrap;
    }}
    .card-ai-btn:hover {{ background: #6C5CE7; color: white; }}

    .cred-tooltip {{ position: relative; }}
    .cred-tooltip .cred-tooltip-text {{
      visibility: hidden; opacity: 0;
      position: absolute; bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%);
      background: #1A1A2E; color: #fff; font-size: 11px; line-height: 1.5;
      padding: 8px 12px; border-radius: 8px; white-space: nowrap; z-index: 100;
      transition: opacity 0.15s ease, visibility 0.15s ease;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .cred-tooltip .cred-tooltip-text::after {{
      content: ''; position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
      border: 5px solid transparent; border-top-color: #1A1A2E;
    }}
    .cred-tooltip:hover .cred-tooltip-text {{ visibility: visible; opacity: 1; }}
    .cred-tooltip-row {{ display: block; padding: 2px 0; }}
    .cred-tooltip-link {{
      color: #C4B5FD; text-decoration: none; transition: color 0.1s ease;
    }}
    .cred-tooltip-link:hover {{ color: #fff; text-decoration: underline; }}

    .toast {{
      position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(80px);
      background: #1A1A2E; color: white; padding: 10px 20px; border-radius: 10px;
      font-size: 13px; z-index: 9999; transition: transform 0.3s ease, opacity 0.3s ease; opacity: 0;
    }}
    .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
  </style>
</head>
<body class="bg-[#FAFBFC] text-primary lg:h-screen lg:overflow-hidden flex flex-col">

  <header class="flex-shrink-0 bg-white border-b border-gray-100 px-4 lg:px-8 py-3 lg:py-4">
    <div class="max-w-[1600px] mx-auto">
      <div class="flex items-center justify-between">
        <h1 class="text-lg lg:text-2xl font-bold text-primary"><i class="fa-solid fa-newspaper text-accent mr-1.5 lg:mr-2"></i>{site_title}</h1>
        <div class="flex items-center gap-2">
          <span class="text-gray-400 text-xs hidden lg:inline"><i class="fa-regular fa-clock mr-1"></i>生成于 {generated_time}</span>
          <span class="inline-block bg-[#F3F0FF] text-accent text-xs font-medium px-2 lg:px-3 py-1 lg:py-1.5 rounded-full"><i class="fa-solid fa-user mr-1"></i>{role}</span>
        </div>
      </div>
      <div class="flex items-center gap-2 mt-1 lg:mt-0.5 text-xs text-gray-400">
        <span><i class="fa-regular fa-calendar mr-1"></i>{date_label}</span>
        <span class="text-gray-200">·</span>
        <span class="bg-accent/10 text-accent font-medium px-2 py-0.5 rounded-full">{item_count} 条资讯</span>
        <span class="lg:hidden"><span class="text-gray-200 mx-0.5">·</span><i class="fa-regular fa-clock mr-0.5"></i>{generated_time}</span>
      </div>
    </div>
  </header>

  <div class="flex-1 flex flex-col lg:flex-row lg:overflow-hidden max-w-[1600px] mx-auto w-full">

    <aside class="w-full lg:w-[420px] flex-shrink-0 border-b lg:border-b-0 lg:border-r border-gray-100 bg-white lg:overflow-y-auto sidebar-scroll">
      <div class="p-5 space-y-5">

        <section>
          <h2 class="text-base font-semibold text-primary mb-3 flex items-center">
            <span class="w-6 h-6 rounded-md bg-accent/10 flex items-center justify-center mr-2"><i class="fa-solid fa-bolt text-accent text-[10px]"></i></span>今日速览
          </h2>
          <ol class="space-y-3 text-[13px] leading-relaxed">
{render_overview(left.get("overview", []))}
          </ol>
        </section>

        <hr class="border-gray-100">

        <section>
          <h2 class="text-base font-semibold text-primary mb-3 flex items-center">
            <span class="w-6 h-6 rounded-md bg-accent/10 flex items-center justify-center mr-2"><i class="fa-solid fa-bullseye text-accent text-[10px]"></i></span>今日行动建议
          </h2>
          <ul class="space-y-2.5 text-[13px]">
{render_actions(left.get("actions", []))}
          </ul>
        </section>

        <hr class="border-gray-100">

        <section>
          <h2 class="text-base font-semibold text-primary mb-3 flex items-center">
            <span class="w-6 h-6 rounded-md bg-accent/10 flex items-center justify-center mr-2"><i class="fa-solid fa-chart-line text-accent text-[10px]"></i></span>趋势雷达
          </h2>
          <div class="space-y-2 text-[13px] mb-3">
{render_trends(left.get("trends", {}))}
          </div>
        </section>

      </div>
    </aside>

    <main class="flex-1 lg:overflow-y-auto feed-scroll px-4 lg:px-8 py-6 min-w-0">
      <h2 class="text-lg font-semibold text-primary mb-4 flex items-center">
        <span class="w-7 h-7 rounded-lg bg-accent/10 flex items-center justify-center mr-2.5"><i class="fa-solid fa-newspaper text-accent text-xs"></i></span>
        今日资讯<span class="text-xs text-gray-400 font-normal ml-3">按相关度排序 · 共 {item_count} 条</span>
      </h2>
      <div class="space-y-3">
{article_items}
      </div>
      <div class="text-center text-xs text-gray-400 mt-6 pb-4">
        数据来源：{data_sources}<br>
        生成时间 {generated_at}
      </div>
    </main>
  </div>

<div id="toast" class="toast"></div>

<script>
(function() {{
  'use strict';
  const DATE = '{title_date}';
  const IS_HTTP = location.protocol.startsWith('http');
  const events = [];
  const cardTimers = {{}};
  const cardDwellTime = {{}};
  const pageLoadTime = Date.now();
  const sessionId = (window.crypto && typeof window.crypto.randomUUID === 'function')
    ? window.crypto.randomUUID()
    : ('session-' + Date.now() + '-' + Math.random().toString(16).slice(2));
  let leaveHandled = false;

  const AI_TOOLS = {tools_js};

  function ts() {{ return new Date().toISOString(); }}
  function log(event) {{ events.push(event); console.log('%c[反馈]%c ' + event.type, 'color:#6C5CE7;font-weight:bold', 'color:#333', event); }}
  function showToast(msg, dur) {{ const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); setTimeout(() => t.classList.remove('show'), dur || 2000); }}
  function decodeBase64Utf8(value) {{
    const binary = atob(value);
    if (typeof TextDecoder !== 'undefined') {{
      const bytes = Uint8Array.from(binary, ch => ch.charCodeAt(0));
      return new TextDecoder('utf-8').decode(bytes);
    }}
    const escaped = Array.from(binary, ch => '%' + ch.charCodeAt(0).toString(16).padStart(2, '0')).join('');
    return decodeURIComponent(escaped);
  }}
  function parseTags(value) {{
    if (!value) return [];
    try {{
      return JSON.parse(decodeBase64Utf8(value));
    }} catch (err) {{
      return [];
    }}
  }}

  function sendToAI(tool, prompt) {{
    if (tool.id === 'copy') {{ navigator.clipboard.writeText(prompt).then(() => showToast('Prompt 已复制到剪贴板')); }}
    else {{ window.open(tool.url.replace('{{prompt}}', encodeURIComponent(prompt)), '_blank'); showToast('已发送至 ' + tool.name); }}
    log({{ type: 'send_to_ai', tool: tool.id, prompt: prompt.substring(0, 100) + '...', timestamp: ts() }});
  }}

  function showAIMenu(anchor, prompt) {{
    document.querySelectorAll('.ai-menu').forEach(m => m.classList.remove('open'));
    const menu = document.createElement('div'); menu.className = 'ai-menu open';
    AI_TOOLS.forEach((tool, i) => {{
      if (i > 0 && tool.id === 'copy') menu.insertAdjacentHTML('beforeend', '<div class="ai-menu-sep"></div>');
      const item = document.createElement('div'); item.className = 'ai-menu-item';
      item.innerHTML = '<i class="' + tool.icon + ' item-icon-' + tool.id + '"></i><span>' + tool.name + '</span>';
      item.addEventListener('click', e => {{ e.stopPropagation(); sendToAI(tool, prompt); menu.remove(); }});
      menu.appendChild(item);
    }});
    anchor.style.position = 'relative'; anchor.appendChild(menu);
    setTimeout(() => {{ const close = e => {{ if (!menu.contains(e.target)) {{ menu.remove(); document.removeEventListener('click', close); }} }}; document.addEventListener('click', close); }}, 0);
  }}

  const cards = document.querySelectorAll('main article.card-hover');
  cards.forEach((card, i) => {{
    const h3 = card.querySelector('h3'); if (!h3) return;
    const title = h3.textContent.trim().replace(/^[^\\w\\u4e00-\\u9fff]+/, '');
    const id = card.dataset.articleId || ('article-' + (i + 1));
    card.dataset.articleId = id; card.dataset.title = title;
    const tagEls = card.querySelectorAll('span[class*=\"rounded-full\"]');
    const tags = [];
    tagEls.forEach(t => {{
      const text = t.textContent.trim();
      if (text.startsWith('#')) {{ tags.push(text); t.classList.add('tag-clickable');
        t.addEventListener('click', function() {{ const w = this.classList.toggle('tag-clicked'); log({{ type: w ? 'tag_follow' : 'tag_unfollow', tag: text, articleId: id, title, timestamp: ts() }}); }});
      }}
    }});
    card.dataset.tags = card.dataset.tags || '';
    const actionBar = card.querySelector('.article-action-bar');
    if (actionBar) {{
      const btnGroup = actionBar.querySelector('.btn-group');
      btnGroup.innerHTML = '<span class=\"bookmark-btn\" data-bookmarked=\"false\"><i class=\"fa-regular fa-bookmark\"></i> 收藏</span><span class=\"vote-btn\" data-voted=\"false\"><i class=\"fa-regular fa-thumbs-up\"></i> 有用</span>';
      // 恢复 localStorage 收藏状态
      const lsKey = 'bookmark:' + DATE + ':' + id;
      if (localStorage.getItem(lsKey) === '1') {{
        const b = btnGroup.querySelector('.bookmark-btn');
        b.dataset.bookmarked = 'true'; b.classList.add('bookmarked');
        b.innerHTML = '<i class=\"fa-solid fa-bookmark\"></i> 已收藏';
      }}
      btnGroup.querySelector('.vote-btn').addEventListener('click', function() {{
        const v = this.dataset.voted === 'true'; this.dataset.voted = v ? 'false' : 'true'; this.classList.toggle('voted');
        this.innerHTML = v ? '<i class=\"fa-regular fa-thumbs-up\"></i> 有用' : '<i class=\"fa-solid fa-thumbs-up\"></i> 有用';
        log({{ type: v ? 'unvote' : 'vote', articleId: id, title, tags, timestamp: ts() }});
      }});
      btnGroup.querySelector('.bookmark-btn').addEventListener('click', function() {{
        const b = this.dataset.bookmarked === 'true';
        this.dataset.bookmarked = b ? 'false' : 'true'; this.classList.toggle('bookmarked');
        this.innerHTML = b ? '<i class=\"fa-regular fa-bookmark\"></i> 收藏' : '<i class=\"fa-solid fa-bookmark\"></i> 已收藏';
        if (!b) {{
          localStorage.setItem(lsKey, '1');
          const card = this.closest('article[data-article-id]');
          const payload = {{ id, title, tags, summary: card ? card.dataset.summary : '', source_url: card ? card.dataset.url : '', priority: card ? card.dataset.priority : '', date: card ? card.dataset.date : DATE }};
          if (IS_HTTP) fetch('/api/bookmark', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(payload) }})
            .then(r => r.json()).then(j => {{ if (j.graphify === 'disabled') console.warn('[daily] Graphify 未启用，收藏不会写入知识图谱。在 profile.yaml 中设置 graphify.enabled: true 可开启。'); }})
            .catch(() => {{}});
          log({{ type: 'bookmark', articleId: id, title, tags, timestamp: ts() }});
        }} else {{
          localStorage.removeItem(lsKey);
          log({{ type: 'unbookmark', articleId: id, title, tags, timestamp: ts() }});
        }}
      }});
    }}
  }});

  document.querySelectorAll('.action-item').forEach(item => {{
    const prompt = item.dataset.actionPrompt; if (!prompt) return;
    const wrap = document.createElement('div'); wrap.className = 'ai-trigger-wrap';
    const menu = document.createElement('div'); menu.className = 'ai-menu';
    AI_TOOLS.forEach((tool, i) => {{
      if (i > 0 && tool.id === 'copy') menu.insertAdjacentHTML('beforeend', '<div class=\"ai-menu-sep\"></div>');
      const mi = document.createElement('div'); mi.className = 'ai-menu-item';
      mi.innerHTML = '<i class=\"' + tool.icon + ' item-icon-' + tool.id + '\"></i><span>' + tool.name + '</span>';
      mi.addEventListener('click', e => {{ e.stopPropagation(); sendToAI(tool, prompt); }});
      menu.appendChild(mi);
    }});
    wrap.appendChild(menu);
    const icon = document.createElement('span'); icon.className = 'ai-trigger-icon';
    icon.innerHTML = '<i class=\"fa-solid fa-paper-plane\"></i>'; icon.title = '发送至工具';
    wrap.appendChild(icon); item.appendChild(wrap);
    let ht = null;
    function show() {{ clearTimeout(ht); menu.classList.add('open'); }}
    function hide() {{ ht = setTimeout(() => menu.classList.remove('open'), 150); }}
    icon.addEventListener('mouseenter', show); icon.addEventListener('mouseleave', hide);
    menu.addEventListener('mouseenter', show); menu.addEventListener('mouseleave', hide);
  }});

  cards.forEach(card => {{
    const title = card.dataset.title; const tags = parseTags(card.dataset.tags || '');
    const se = card.querySelector('.ai-gradient-line'); const s = se ? se.textContent.trim().substring(0, 200) : '';
    const re = card.querySelector('[class*=\"F8F7FF\"]'); const r = re ? re.textContent.trim() : '';
    const dp = '我在阅读日报时看到了这条资讯，请帮我深入分析：\\n\\n标题：' + title + '\\n标签：' + tags.join(' ') + '\\n摘要：' + s + '\\n' + (r ? '与我的关联：' + r + '\\n' : '') + '\\n请从以下角度展开：\\n1. 技术细节和背景\\n2. 短期和长期影响\\n3. 我应如何应对\\n4. 推荐学习资源';
    const ab = card.querySelector('.flex.items-center.justify-between.mt-2');
    if (ab) {{
      const wrap = document.createElement('span'); wrap.className = 'card-ai-wrap';
      const icon = document.createElement('span'); icon.className = 'card-ai-btn';
      icon.innerHTML = '<i class=\"fa-solid fa-wand-magic-sparkles text-[10px]\"></i>深入分析'; wrap.appendChild(icon);
      const menu = document.createElement('div'); menu.className = 'ai-menu';
      AI_TOOLS.forEach((tool, i) => {{
        if (i > 0 && tool.id === 'copy') menu.insertAdjacentHTML('beforeend', '<div class=\"ai-menu-sep\"></div>');
        const mi = document.createElement('div'); mi.className = 'ai-menu-item';
        mi.innerHTML = '<i class=\"' + tool.icon + ' item-icon-' + tool.id + '\"></i><span>' + tool.name + '</span>';
        mi.addEventListener('click', e => {{ e.stopPropagation(); sendToAI(tool, dp); }});
        menu.appendChild(mi);
      }});
      wrap.appendChild(menu);
      let ht = null;
      function show() {{ clearTimeout(ht); menu.classList.add('open'); }}
      function hide() {{ ht = setTimeout(() => menu.classList.remove('open'), 150); }}
      icon.addEventListener('mouseenter', show); icon.addEventListener('mouseleave', hide);
      menu.addEventListener('mouseenter', show); menu.addEventListener('mouseleave', hide);
      const sl = ab.querySelector('a'); if (sl) ab.insertBefore(wrap, sl);
    }}
  }});

  const fc = document.querySelector('main.feed-scroll');
  if (fc) {{
    const obs = new IntersectionObserver(entries => {{
      entries.forEach(e => {{ const c = e.target, id = c.dataset.articleId; if (!id) return;
        if (e.isIntersecting) {{ cardTimers[id] = Date.now(); }} else if (cardTimers[id]) {{
          const el = Date.now() - cardTimers[id]; cardDwellTime[id] = (cardDwellTime[id] || 0) + el; delete cardTimers[id];
          if (el > 5000) log({{ type: 'dwell', articleId: id, title: c.dataset.title, tags: parseTags(c.dataset.tags || ''), duration_ms: el, timestamp: ts() }});
        }}
      }});
    }}, {{ root: fc, threshold: 0.5 }});
    cards.forEach(c => obs.observe(c));
  }}

  document.querySelectorAll('main a[target=\"_blank\"]').forEach(l => {{
    l.addEventListener('click', function() {{ const c = this.closest('article[data-article-id]');
      if (c) log({{ type: 'click_source', articleId: c.dataset.articleId, title: c.dataset.title, tags: parseTags(c.dataset.tags || ''), url: this.href, timestamp: ts() }});
    }});
  }});

  document.addEventListener('copy', function() {{
    const s = window.getSelection(); if (!s || !s.anchorNode) return;
    const c = s.anchorNode.parentElement?.closest('article[data-article-id]');
    if (c) log({{ type: 'copy', articleId: c.dataset.articleId, title: c.dataset.title, tags: parseTags(c.dataset.tags || ''), copiedText: s.toString().substring(0, 100), timestamp: ts() }});
  }});

  function buildSummary() {{
    Object.keys(cardTimers).forEach(id => {{ cardDwellTime[id] = (cardDwellTime[id] || 0) + (Date.now() - cardTimers[id]); }});
    const totalTime = Math.round((Date.now() - pageLoadTime) / 1000);
    const voteState = new Map();
    const tagState = new Map();
    events.forEach(e => {{
      if ((e.type === 'vote' || e.type === 'unvote') && e.articleId) voteState.set(e.articleId, e);
      if ((e.type === 'tag_follow' || e.type === 'tag_unfollow') && e.tag) tagState.set(e.tag, e.type === 'tag_follow');
    }});
    const voted = [...voteState.values()].filter(e => e.type === 'vote').map(e => ({{ id: e.articleId, title: e.title, tags: e.tags }}));
    const tagFollows = [...tagState.entries()].filter(([, followed]) => followed).map(([tag]) => tag);
    const tagUnfollows = [...tagState.entries()].filter(([, followed]) => !followed).map(([tag]) => tag);
    const clicked = events.filter(e => e.type === 'click_source').map(e => ({{ id: e.articleId, title: e.title, tags: e.tags || [] }}));
    const copied = events.filter(e => e.type === 'copy').map(e => ({{ id: e.articleId, title: e.title, tags: e.tags || [] }}));
    const aiUsage = events.filter(e => e.type === 'send_to_ai');
    const aiCounts = {{}}; aiUsage.forEach(u => {{ aiCounts[u.tool] = (aiCounts[u.tool] || 0) + 1; }});
    const dwellRanking = Object.entries(cardDwellTime).map(([id, ms]) => {{
      const c = document.querySelector(`[data-article-id=\"${{id}}\"]`);
      return {{ articleId: id, title: c ? c.dataset.title : id, tags: c ? parseTags(c.dataset.tags || '') : [], dwell_seconds: Math.round(ms / 1000) }};
    }}).filter(d => d.dwell_seconds > 0).sort((a, b) => b.dwell_seconds - a.dwell_seconds);
    const tagScores = {{}};
    function addTS(tags, w) {{ (tags || []).forEach(t => {{ tagScores[t] = (tagScores[t] || 0) + w; }}); }}
    voted.forEach(v => addTS(v.tags, 3));
    tagFollows.forEach(t => {{ tagScores[t] = (tagScores[t] || 0) + 2; }});
    dwellRanking.forEach(d => {{ if (d.dwell_seconds >= 5) addTS(d.tags, 1); }});
    const tagRanking = Object.entries(tagScores).sort((a, b) => b[1] - a[1]).map(([tag, score]) => ({{ tag, score }}));
    return {{
      date: DATE,
      session: {{ session_id: sessionId, total_time_seconds: totalTime, total_events: events.length, page_load: new Date(pageLoadTime).toISOString() }},
      explicit_feedback: {{ voted, tags_followed: tagFollows, tags_unfollowed: tagUnfollows }},
      implicit_feedback: {{ dwell_ranking: dwellRanking, articles_clicked: clicked, articles_copied: copied }},
      ai_interaction: {{ tools_used: aiCounts, detail: aiUsage.map(u => ({{ tool: u.tool, prompt_preview: u.prompt }})) }},
      interest_profile: {{ tag_scores: tagRanking, top_interests: tagRanking.slice(0, 5).map(t => t.tag) }},
      all_events: events
    }};
  }}

  function onLeave() {{
    if (leaveHandled) return;
    leaveHandled = true;
    const summary = buildSummary();
    if (IS_HTTP) navigator.sendBeacon('/api/feedback', JSON.stringify(summary));
    try {{ const st = JSON.parse(localStorage.getItem('daily_feedback') || '[]'); st.push(summary); if (st.length > 30) st.splice(0, st.length - 30); localStorage.setItem('daily_feedback', JSON.stringify(st)); }} catch(e) {{}}
    console.log('\\n%c╔══════════════════════════════════════════════════╗', 'color:#6C5CE7');
    console.log('%c║     日报反馈汇总 · ' + DATE + '                  ║', 'color:#6C5CE7;font-weight:bold');
    console.log('%c╚══════════════════════════════════════════════════╝', 'color:#6C5CE7');
    console.log(JSON.stringify(summary, null, 2));
  }}
  window.addEventListener('pagehide', onLeave, {{ capture: true }});
  window.addEventListener('beforeunload', onLeave, {{ capture: true }});

  console.log('%c╔══════════════════════════════════════════════════╗', 'color:#6C5CE7');
  console.log('%c║     日报反馈采集已启动 · ' + DATE + '            ║', 'color:#6C5CE7;font-weight:bold');
  console.log('%c╚══════════════════════════════════════════════════╝', 'color:#6C5CE7');
  console.log('%c模式：' + (IS_HTTP ? 'HTTP（反馈自动回流）' : 'File（仅控制台+localStorage）'), 'color:#333;font-weight:bold');
  console.log('  📌 隐式 — 停留时长、原文点击、文本复制');
  console.log('  👆 显式 — 投票(▲)、收藏(🔖)、标签关注');
  console.log('  🤖 AI — 行动建议/深入分析 发送至工具');
  console.log('%c关闭页面时自动输出汇总\\n', 'color:#888');
}})();
</script>
</body>
</html>
"""


def archive_previous_html(output_path: Path) -> Path | None:
    if not output_path.exists():
        return None

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    archive_path = ARCHIVE_DIR / f"{stamp}.html"
    counter = 1
    while archive_path.exists():
        archive_path = ARCHIVE_DIR / f"{stamp}-{counter}.html"
        counter += 1

    shutil.move(str(output_path), str(archive_path))
    return archive_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render daily JSON into HTML")
    parser.add_argument("input", help="Input JSON file path")
    parser.add_argument(
        "--output",
        help="Output HTML file path; defaults to input path with .html suffix",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="即使时间窗口校验有严重警告也继续渲染",
    )
    return parser.parse_args()


def check_time_window(payload: dict[str, Any], window_days: int = 3) -> list[str]:
    """检查文章的 time_label 和 source_date，返回警告列表。

    校验三层：
    1. time_label 是否使用了模糊表述
    2. time_label 中的日期是否在窗口内
    3. source_date 与 time_label 是否一致（交叉校验，防止虚假日期）
    """
    warnings: list[str] = []
    meta_date = payload.get("meta", {}).get("date", "")
    try:
        report_date = datetime.strptime(meta_date, "%Y-%m-%d")
    except ValueError:
        return warnings
    window_start = report_date - timedelta(days=window_days - 1)

    vague_patterns = {"本周", "持续热门", "持续活跃", "近期", "最近", "近日"}

    for article in payload.get("articles", []):
        title = article.get("title", "")
        time_label = article.get("time_label", "")
        source_date = article.get("source_date", "")
        article_id = article.get("id", "?")

        # 层 1：模糊表述检测
        for vague in vague_patterns:
            if vague in time_label:
                warnings.append(
                    f"  [{article_id}] time_label 使用了模糊表述 \"{time_label}\"，"
                    f"应改为具体日期 — {title}"
                )
                break

        # 层 2：time_label 日期窗口检查
        label_date = None
        if time_label in {"今天", "今日"}:
            label_date = report_date
        else:
            m = re.search(r"(\d{1,2})月(\d{1,2})日", time_label)
            if m:
                month, day = int(m.group(1)), int(m.group(2))
                try:
                    label_date = report_date.replace(month=month, day=day)
                    if label_date > report_date:
                        label_date = label_date.replace(year=label_date.year - 1)
                except ValueError:
                    pass

        if label_date and label_date < window_start:
            warnings.append(
                f"  [{article_id}] time_label 日期 {time_label} 超出 {window_days} 日窗口"
                f"（{window_start.strftime('%m-%d')} ~ {report_date.strftime('%m-%d')}）"
                f" — {title}"
            )

        # 层 3：source_date 交叉校验
        if not source_date:
            warnings.append(
                f"  [{article_id}] 缺少 source_date（来源发布日期证据）"
                f" — {title}"
            )
        elif source_date == "unknown":
            warnings.append(
                f"  [{article_id}] source_date 为 unknown，无法验证日期真实性"
                f" — {title}"
            )
        else:
            try:
                src_date = datetime.strptime(source_date, "%Y-%m-%d")
                # 检查 source_date 是否在窗口内
                if src_date < window_start or src_date > report_date:
                    warnings.append(
                        f"  [{article_id}] source_date {source_date} 超出窗口"
                        f"（{window_start.strftime('%Y-%m-%d')} ~ "
                        f"{report_date.strftime('%Y-%m-%d')}）— {title}"
                    )
                # 检查 source_date 与 time_label 是否一致
                if label_date and src_date.date() != label_date.date():
                    warnings.append(
                        f"  [{article_id}] 日期不一致：time_label=\"{time_label}\" "
                        f"但 source_date=\"{source_date}\" — {title}"
                    )
            except ValueError:
                warnings.append(
                    f"  [{article_id}] source_date 格式错误 \"{source_date}\"，"
                    f"应为 YYYY-MM-DD — {title}"
                )

    return warnings


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    try:
        payload = normalize_payload(json.loads(input_path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: payload JSON 解析失败: {exc}") from exc
    except ValueError as exc:
        raise SystemExit(f"ERROR: payload 契约校验失败: {exc}") from exc

    window_days = load_profile_window_days()
    time_warnings = check_time_window(payload, window_days=window_days)
    # 区分严重警告（超窗/不一致）和轻度警告（缺少 source_date）
    severe = [w for w in time_warnings if "超出" in w or "不一致" in w]
    if time_warnings:
        print("⚠️  时间窗口校验警告：", file=sys.stderr)
        for w in time_warnings:
            print(w, file=sys.stderr)
        if severe and not args.force:
            print(
                f"\n❌ 发现 {len(severe)} 条严重问题（超窗或日期不一致），渲染已阻断。",
                file=sys.stderr,
            )
            print("   修复 JSON 后重新渲染，或使用 --force 强制渲染。", file=sys.stderr)
            raise SystemExit(1)
        print("", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    archived = archive_previous_html(output_path)
    output_path.write_text(render_html(payload), encoding="utf-8")
    if archived:
        print(f"Archived previous HTML -> {archived}")
    print(f"Rendered {output_path}")


if __name__ == "__main__":
    main()
