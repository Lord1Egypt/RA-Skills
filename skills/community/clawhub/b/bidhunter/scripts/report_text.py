#!/usr/bin/env python3
"""
report_text.py - Generate plain text briefing report.
Suitable for IM push (WeChat, DingTalk, Feishu, Email).

Usage:
  python3 report_text.py <qual_file.jsonl> <date>
  python3 report_text.py <qual_file.jsonl> <date> --summary   # 精华版，Top 5

  Output: text report to stdout.
"""

import json
import sys
from collections import defaultdict

VERDICT_EMOJI = {
    "investable":    "[可投]",
    "not_investable": "[不可投]",
    "needs_review":   "[需确认]",
    "skip":           "[跳过]",
}

VERDICT_ORDER = {"investable": 0, "needs_review": 1, "not_investable": 2}


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


def format_item(item, seq_num):
    """Format a single item for text output."""
    title = item.get("title", "")
    rid = item.get("id", "")
    url = item.get("url", "")
    verdict = item.get("verdict", "needs_review")
    reason = item.get("reason", "")
    entity = item.get("assigned_entity_name", item.get("assigned_entity", ""))
    caps = item.get("matched_capabilities", [])
    region_info = item.get("region_info", {})
    is_priority = region_info.get("is_priority", False)
    region = region_info.get("region", "")

    emoji = VERDICT_EMOJI.get(verdict, "[?]")
    score = item.get("score")
    level = item.get("score_level", "")
    if verdict == "investable" and isinstance(score, int):
        emoji = f"[可投·{level} {score}]"
    caps_str = f" | 匹配: {', '.join(caps)}" if caps else ""
    entity_str = f" | 主体: {entity}" if entity else ""
    region_str = f" | {region}" if region else ""
    priority_str = " [重点]" if is_priority else ""

    lines = [
        f"#{seq_num} {title}",
        f"   {emoji} {reason}{caps_str}{entity_str}{region_str}{priority_str}",
    ]
    if url:
        lines.append(f"   链接: {url}")
    return "\n".join(lines)


FEEDBACK_GUIDANCE = """
💡 判断有误？请反馈帮助优化：
   格式：反馈 [#序号] [准确/有误] [原因]
   例如：反馈 #3 有误 应该是可投
   反馈发到：ClawHub（clawhub.ai）或 SkillHub（skillhub.cn）的 bidhunter 评论区

📋 反馈示例：
   反馈 #1 有误 #3 准确 #7 有误
"""


def build_report(results, date_str, summary_mode=False):
    """Build the text report string."""
    active = [r for r in results if r.get("verdict") != "skip"]

    stats = defaultdict(int)
    for r in active:
        stats[r.get("verdict", "needs_review")] += 1
    total = len(active)

    investable = [r for r in active if r.get("verdict") == "investable"]
    not_investable = [r for r in active if r.get("verdict") == "not_investable"]
    needs_review = [r for r in active if r.get("verdict") == "needs_review"]
    priority_items = [r for r in active if r.get("region_info", {}).get("is_priority", False)]
    # A1: sort by match score desc so the strongest leads
    investable.sort(key=lambda r: r.get("score", 0), reverse=True)
    priority_items.sort(key=lambda r: r.get("score", 0), reverse=True)

    lines = []
    header = f"【可投简报·研判 {date_str}】总{total}｜可投{stats['investable']}｜不可投{stats['not_investable']}｜需确认{stats['needs_review']}"
    lines.append("=" * len(header))
    lines.append(header)
    lines.append("=" * len(header))

    if summary_mode:
        # 精华版：只显示优先级地区 + 可投标讯，最多 Top 5
        top_items = priority_items[:5]
        if len(top_items) < 5:
            remaining = [r for r in investable if not r.get("region_info", {}).get("is_priority", False)]
            for r in remaining:
                if len(top_items) >= 5:
                    break
                top_items.append(r)

        if not top_items:
            lines.append("")
            lines.append("今日无优先或可投标讯。")
        else:
            lines.append("")
            lines.append("【精华版 Top 5】")
            for i, item in enumerate(top_items, 1):
                lines.append("")
                lines.append(format_item(item, i))
    else:
        # 完整版
        if priority_items:
            lines.append("")
            lines.append("【重点地区专项】")
            seq = 1
            for item in priority_items:
                lines.append("")
                lines.append(format_item(item, seq))
                seq += 1

        if investable:
            lines.append("")
            lines.append("【可投标】")
            priority_count = len(priority_items)
            for i, item in enumerate(investable, priority_count + 1):
                if not item.get("region_info", {}).get("is_priority", False):
                    lines.append("")
                    lines.append(format_item(item, i))

        if needs_review:
            lines.append("")
            lines.append("【需确认】")
            seq = 1
            for item in needs_review:
                lines.append("")
                lines.append(format_item(item, seq))
                seq += 1

        if not_investable:
            lines.append("")
            lines.append("【不可投标】")
            seq = 1
            for item in not_investable:
                lines.append("")
                lines.append(format_item(item, seq))
                seq += 1

    if total == 0:
        lines.append("")
        lines.append("今日无新公告。")

    lines.append(FEEDBACK_GUIDANCE)
    return "\n".join(lines)


def main():
    summary_mode = False

    # Parse --summary if present
    args = [a for a in sys.argv[1:] if a != "--summary"]
    summary_mode = len(args) != len(sys.argv[1:])

    if len(args) < 2:
        print("Usage: python3 report_text.py <qual_file.jsonl> <date> [--summary]", file=sys.stderr)
        sys.exit(1)

    qual_path = args[0]
    date_str = args[1]

    results = load_results(qual_path)
    report = build_report(results, date_str, summary_mode=summary_mode)
    print(report)


if __name__ == "__main__":
    main()
