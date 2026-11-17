"""
多格式输出 (v1.0)

将处理结果输出为三种格式:
  1. 结构化笔记 (Markdown) — 完整转录+分析, 存档
  2. 知识卡片 (卡片式) — 精简摘要+关键点, 分享
  3. 错题集 (列表式) — 新发现的转录错误, 积累校正

使用:
    from biliyoutik2brain.core.formatter import format_all, FormatType
    format_all(result, output_dir)
"""

import os, json, time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from . import paths


class FormatType(Enum):
    NOTE = "note"          # 结构化笔记 (完整)
    CARD = "card"          # 知识卡片 (精简)
    ERRORS = "errors"      # 错题集


@dataclass
class FormatResult:
    """一次处理的所有输出"""
    note: str = ""       # 笔记文件路径
    card: str = ""       # 卡片文件路径
    errors: str = ""     # 错题文件路径


# ═══════════════════════════════════════════════════════════════
#  结构化笔记
# ═══════════════════════════════════════════════════════════════

def format_note(
    title: str,
    uploader: str,
    url: str,
    corrected_text: str,
    analysis: Dict,
    domain: str = "",
    model: str = "",
    pipeline_time: float = 0.0,
) -> str:
    """生成结构化笔记 (Markdown)"""
    date = time.strftime("%Y-%m-%d %H:%M")
    lines = [f"# {title}", ""]

    lines.append(f"- **UP主**: {uploader}")
    lines.append(f"- **来源**: {url}")
    lines.append(f"- **处理日期**: {date}")
    if domain:
        lines.append(f"- **领域**: {domain}")
    if model:
        lines.append(f"- **模型**: {model}")
    if pipeline_time:
        lines.append(f"- **管线耗时**: {pipeline_time:.1f}s")
    lines.append("")

    # 摘要
    summary = analysis.get("summary", "")
    if summary:
        lines.append("## 摘要")
        lines.append(summary)
        lines.append("")

    # 关键词
    keywords = analysis.get("keywords", [])
    if keywords:
        lines.append("## 关键词")
        lines.append(", ".join(f"`{kw}`" for kw in keywords[:10]))
        lines.append("")

    # 主题
    topics = analysis.get("topics", [])
    if topics:
        lines.append("## 主题")
        for t in topics[:5]:
            lines.append(f"- {t}")
        lines.append("")

    # 章节
    chapters = analysis.get("chapters", [])
    if chapters:
        lines.append("## 章节")
        for i, ch in enumerate(chapters[:10], 1):
            key_pts = ", ".join(ch.get("key_points", [])[:3])
            lines.append(f"{i}. **{ch.get('title', '')}**  " + (f"({key_pts})" if key_pts else ""))
        lines.append("")

    # 完整文本
    lines.append("## 修正文本")
    lines.append(corrected_text)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  知识卡片
# ═══════════════════════════════════════════════════════════════

def format_card(
    title: str,
    uploader: str,
    url: str,
    analysis: Dict,
    domain: str = "",
) -> str:
    """生成知识卡片 (精简版 Markdown)"""
    date = time.strftime("%Y-%m-%d")
    summary = analysis.get("summary", "")
    keywords = analysis.get("keywords", [])
    topics = analysis.get("topics", [])
    chapters = analysis.get("chapters", [])

    lines = [
        f"## {title[:60]}",
        "",
        f"> **{uploader}** · {domain} · {date}",
        "",
    ]

    if summary:
        lines.append(summary[:300])
        lines.append("")

    if keywords:
        lines.append(f"**关键词**: {' · '.join(keywords[:8])}")
        lines.append("")

    if topics:
        lines.append(f"**主题**: {' / '.join(topics[:5])}")

    if chapters:
        lines.append("")
        for i, ch in enumerate(chapters[:5], 1):
            pts = ", ".join(ch.get("key_points", [])[:3])
            lines.append(f"- {ch.get('title', '')}" + (f" — {pts}" if pts else ""))

    # 来源链接
    lines.append("")
    lines.append(f"📎 {url}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  错题集
# ═══════════════════════════════════════════════════════════════

def format_errors(
    uploader: str,
    corrections: List[Dict],
    error_categories: Dict,
    low_conf_regions: List,
) -> str:
    """生成错题集 (列表式)"""
    date = time.strftime("%Y-%m-%d")
    lines = [f"# 错题集 — {uploader} ({date})", ""]

    # 统计
    if corrections:
        # 兼容 dict (chunk.__dict__) 和 List[Dict] 两种输入
        corr_list = list(corrections.items()) if isinstance(corrections, dict) else corrections
        lines.append(f"本次修正: {len(corr_list)}条")
        for corr in (corr_list if isinstance(corr_list, list) else [corr_list])[:15]:
            if isinstance(corr, tuple):
                k, v = corr
                lines.append(f"- {k}: {str(v)[:80]}")
                continue
            orig = corr.get("original", "?")
            corr_text = corr.get("corrected", "?")
            if orig != corr_text:
                lines.append(f"- {orig} → {corr_text}")
        lines.append("")

    # 分类统计
    if error_categories:
        lines.append("## 错题类型分布")
        sorted_cats = sorted(error_categories.items(), key=lambda x: x[1]["count"], reverse=True)
        for cat_name, cat_data in sorted_cats:
            if cat_data["count"] > 0:
                lines.append(f"- **{cat_data['label']}**: {cat_data['count']}次")
                examples = cat_data.get("examples", [])
                for ex in examples[:5]:
                    lines.append(f"  - {ex}")
        lines.append("")

    # 低置信区域
    if low_conf_regions:
        lines.append("## 低置信区域")
        for i, region in enumerate(low_conf_regions[:10]):
            lines.append(f"{i+1}. [{region.avg_confidence:.2f}] \"{region.text[:40]}\"")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  统一输出
# ═══════════════════════════════════════════════════════════════

def format_all(
    title: str,
    uploader: str,
    url: str,
    video_id: str,
    corrected_text: str,
    analysis: Dict,
    corrections: List[Dict] = None,
    error_categories: Dict = None,
    low_conf_regions: List = None,
    domain: str = "",
    model: str = "",
    pipeline_time: float = 0.0,
    output_dir: str = None,
) -> FormatResult:
    """一次性生成三种格式输出

    Returns:
        FormatResult(note, card, errors) — 各格式的文件路径
    """
    out = output_dir or paths.storage_path("")
    safe_name = uploader.replace(" ", "_").replace("/", "_")
    date_str = time.strftime("%Y%m%d")
    note_dir = os.path.join(out, "notes")
    card_dir = os.path.join(out, "cards")
    err_dir = os.path.join(out, "errors")
    for d in [note_dir, card_dir, err_dir]:
        os.makedirs(d, exist_ok=True)

    result = FormatResult()

    # 结构化笔记
    note_content = format_note(title, uploader, url, corrected_text, analysis,
                               domain, model, pipeline_time)
    note_path = os.path.join(note_dir, f"{safe_name}_{video_id}_{date_str}.md")
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(note_content)
    result.note = note_path
    print(f"  [输出] 📝 笔记: {os.path.basename(note_path)} ({len(note_content)}字)")

    # 知识卡片
    card_content = format_card(title, uploader, url, analysis, domain)
    card_path = os.path.join(card_dir, f"{safe_name}_{video_id}_{date_str}_card.md")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(card_content)
    result.card = card_path
    print(f"  [输出] 🃏 卡片: {os.path.basename(card_path)} ({len(card_content)}字)")

    # 错题集
    if corrections or error_categories:
        err_content = format_errors(uploader, corrections or [],
                                    error_categories or {}, low_conf_regions or [])
        err_path = os.path.join(err_dir, f"{safe_name}_{video_id}_{date_str}_errors.md")
        with open(err_path, "w", encoding="utf-8") as f:
            f.write(err_content)
        result.errors = err_path
        print(f"  [输出] ❌ 错题: {os.path.basename(err_path)} ({len(err_content)}字)")

    return result
