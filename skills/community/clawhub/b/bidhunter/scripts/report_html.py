#!/usr/bin/env python3
"""
report_html.py - Generate HTML visual briefing report.

Usage:
  python3 report_html.py <qual_file.jsonl> <date> <output_path>
"""

import json
import sys
import os
from collections import defaultdict
from datetime import datetime


VERDICT_STYLE = {
    "investable":     {"color": "#16a34a", "bg": "#f0fdf4", "label": "可投",   "icon": "check-circle"},
    "not_investable": {"color": "#dc2626", "bg": "#fef2f2", "label": "不可投", "icon": "x-circle"},
    "needs_review":   {"color": "#d97706", "bg": "#fffbeb", "label": "需确认", "icon": "alert-triangle"},
    "skip":           {"color": "#6b7280", "bg": "#f9fafb", "label": "跳过",   "icon": "minus-circle"},
}


def load_results(path):
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return results


def generate_html(results, date_str):
    active = [r for r in results if r.get("verdict") != "skip"]
    stats = defaultdict(int)
    for r in active:
        stats[r.get("verdict", "needs_review")] += 1
    total = len(active)

    # Build stat cards
    stat_cards = ""
    for verdict, style in VERDICT_STYLE.items():
        if verdict == "skip":
            continue
        count = stats.get(verdict, 0)
        pct = f"{count * 100 // total}%" if total > 0 else "0%"
        stat_cards += f"""
        <div class="stat-card" style="border-color: {style['color']}">
            <div class="stat-number" style="color: {style['color']}">{count}</div>
            <div class="stat-label">{style['label']}</div>
            <div class="stat-pct">{pct}</div>
        </div>"""

    # Build item cards with sequential numbering
    items_html = ""
    seq = 1
    for item in sorted(active, key=lambda x: {"investable": 0, "needs_review": 1, "not_investable": 2}.get(x.get("verdict", ""), 3)):
        verdict = item.get("verdict", "needs_review")
        style = VERDICT_STYLE.get(verdict, VERDICT_STYLE["needs_review"])
        title = item.get("title", "")
        rid = item.get("id", "")
        url = item.get("url", "")
        reason = item.get("reason", "")
        entity = item.get("assigned_entity_name", item.get("assigned_entity", ""))
        caps = item.get("matched_capabilities", [])
        region_info = item.get("region_info", {})
        is_priority = region_info.get("is_priority", False)
        region = region_info.get("region", "")
        source = item.get("source", "")
        publish_time = item.get("publish_time", "")

        priority_badge = '<span class="badge priority">重点</span>' if is_priority else ""
        region_badge = f'<span class="badge region">{region}</span>' if region else ""
        source_badge = f'<span class="badge source">{source}</span>' if source else ""
        entity_badge = f'<span class="badge entity">{entity}</span>' if entity else ""
        score_badge = ""
        if verdict == "investable":
            sc = item.get("score")
            lvl = item.get("score_level", "")
            if isinstance(sc, int):
                score_badge = f'<span class="badge score">🔥 {lvl} {sc}</span>'
        caps_html = '<div class="caps">' + "".join(f'<span class="cap-tag">{c}</span>' for c in caps) + '</div>' if caps else ""
        link_html = f'<a href="{url}" target="_blank" class="detail-link">查看详情</a>' if url else ""

        items_html += f"""
        <div class="item-card" style="border-left-color: {style['color']}; background: {style['bg']}">
            <div class="item-header">
                <span class="seq-num">#{seq}</span>
                <span class="verdict-badge" style="background: {style['color']}; color: white;">{style['label']}</span>
                {priority_badge}{region_badge}{source_badge}{entity_badge}{score_badge}
            </div>
            <div class="item-title">{title}</div>
            <div class="item-reason">{reason}</div>
            {caps_html}
            <div class="item-meta">
                <span>ID: {rid}</span>
                {f'<span>发布时间: {publish_time}</span>' if publish_time else ''}
            </div>
            {link_html}
        </div>"""
        seq += 1

    if total == 0:
        items_html = '<div class="empty">今日无新公告。</div>'

    # Feedback section
    feedback_section = """
        <div class="feedback-section">
            <div class="feedback-title">💬 帮助优化判断</div>
            <div class="feedback-desc">如果您认为某条判断有误，欢迎反馈：</div>
            <div class="feedback-format">
                <div class="feedback-format-label">反馈格式：</div>
                <div class="feedback-example">反馈 [#序号] [准确 / 有误] [原因]</div>
                <div class="feedback-example">示例：反馈 #3 有误 应该是可投</div>
            </div>
            <div class="feedback-note">📋 您的反馈将用于优化资质规则库，提升判断准确率。</div>
            <div class="feedback-note">反馈发到 ClawHub（clawhub.ai）或 SkillHub（skillhub.cn）的 bidhunter 评论区。</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>可投简报 - {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 20px; }}
        .tip-banner {{ background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 16px; margin-bottom: 24px; font-size: 13px; color: #1d4ed8; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; color: #0f172a; margin-bottom: 8px; }}
        .header .date {{ color: #64748b; font-size: 14px; }}
        .stats {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap; }}
        .stat-card {{ background: white; border-radius: 12px; padding: 20px 32px; text-align: center; border: 2px solid; min-width: 140px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .stat-number {{ font-size: 36px; font-weight: 700; }}
        .stat-label {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
        .stat-pct {{ font-size: 12px; color: #94a3b8; margin-top: 2px; }}
        .items {{ max-width: 800px; margin: 0 auto; }}
        .item-card {{ background: white; border-radius: 10px; padding: 16px 20px; margin-bottom: 12px; border-left: 4px solid; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .item-header {{ display: flex; gap: 8px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }}
        .seq-num {{ display: inline-flex; align-items: center; justify-content: center; background: #f1f5f9; color: #475569; border-radius: 4px; font-size: 12px; font-weight: 700; padding: 1px 7px; min-width: 28px; }}
        .verdict-badge {{ padding: 2px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
        .badge {{ padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; }}
        .badge.priority {{ background: #fef3c7; color: #92400e; }}
        .badge.region {{ background: #dbeafe; color: #1e40af; }}
        .badge.source {{ background: #e0e7ff; color: #3730a3; }}
        .badge.entity {{ background: #d1fae5; color: #065f46; }}
        .badge.score {{ background: #fee2e2; color: #b91c1c; font-weight: 700; }}
        .item-title {{ font-size: 16px; font-weight: 600; margin-bottom: 6px; line-height: 1.4; }}
        .item-reason {{ font-size: 13px; color: #475569; margin-bottom: 8px; }}
        .caps {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }}
        .cap-tag {{ background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
        .item-meta {{ font-size: 12px; color: #94a3b8; display: flex; gap: 16px; }}
        .detail-link {{ display: inline-block; margin-top: 8px; color: #2563eb; text-decoration: none; font-size: 13px; font-weight: 500; }}
        .detail-link:hover {{ text-decoration: underline; }}
        .empty {{ text-align: center; padding: 60px; color: #94a3b8; font-size: 16px; }}
        .feedback-section {{ max-width: 800px; margin: 30px auto; background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 20px 24px; }}
        .feedback-title {{ font-size: 16px; font-weight: 700; color: #92400e; margin-bottom: 10px; }}
        .feedback-desc {{ font-size: 13px; color: #78350f; margin-bottom: 12px; }}
        .feedback-format {{ background: white; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px; }}
        .feedback-format-label {{ font-size: 12px; color: #64748b; margin-bottom: 6px; }}
        .feedback-example {{ font-size: 13px; color: #1e293b; font-family: monospace; margin-top: 4px; }}
        .feedback-note {{ font-size: 12px; color: #92400e; }}
    </style>
</head>
<body>
    <div class="tip-banner">💡 本文件为本地生成，请用浏览器打开查看完整效果</div>
    <div class="header">
        <h1>可投简报</h1>
        <div class="date">{date_str} | 总计: {total} 条</div>
    </div>
    <div class="stats">{stat_cards}</div>
    <div class="items">{items_html}</div>
    {feedback_section}
</body>
</html>"""


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 report_html.py <qual_file.jsonl> <date> <output_path>", file=sys.stderr)
        sys.exit(1)

    qual_path = sys.argv[1]
    date_str = sys.argv[2]
    output_path = sys.argv[3]

    results = load_results(qual_path)
    html = generate_html(results, date_str)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML report saved to: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
