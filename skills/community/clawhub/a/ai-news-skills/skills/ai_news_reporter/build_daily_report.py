#!/usr/bin/env python3
"""Build a signal-first markdown daily report draft."""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional


THEME_ORDER = ["算力", "应用", "商业", "人才", "安全", "资本", "基础设施"]


def read_payload(path: Optional[str]) -> Dict[str, object]:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def group_by_theme(signals: List[Dict[str, object]]) -> Dict[str, List[Dict[str, object]]]:
    grouped = defaultdict(list)
    for signal in signals:
        grouped[signal.get("theme", "")].append(signal)
    return grouped


def top_signals(signals: List[Dict[str, object]], limit: int = 3) -> List[Dict[str, object]]:
    return sorted(signals, key=lambda signal: int(signal.get("source_count", 0) or 0), reverse=True)[:limit]


def _value(signal: Dict[str, object], key: str, fallback: str = "") -> str:
    return str(signal.get(key, fallback) or fallback).strip()


def _open_questions(signal: Dict[str, object]) -> List[str]:
    value = signal.get("open_questions")
    if isinstance(value, list):
        questions = [str(item).strip() for item in value if str(item).strip()]
        if questions:
            return questions[:3]
    headline = _value(signal, "headline")
    return [
        f"{headline} 是否已有足够公开证据支持？",
        "这一变化是短期波动，还是会持续影响后续判断？",
    ]


def _evidence_links(signal: Dict[str, object]) -> List[str]:
    value = signal.get("evidence_links")
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def build_report(signals: List[Dict[str, object]], report_date: str) -> str:
    top = top_signals(signals)
    grouped = group_by_theme(signals)

    lines = [f"# AI日报｜{report_date}", ""]
    lines.append(f"统计范围：{report_date} 过去24小时")
    lines.append(f"原始记录：{len(signals)}")
    lines.append(f"去重后：{len(signals)}")
    lines.append(f"进入正文：{len(top)}")
    lines.append("")

    lines.append("## 今日新增信号")
    if not top:
        lines.append("")
        lines.append("今天没有形成足够强的新信号，建议继续观察原始新闻池。")
    for idx, signal in enumerate(top, start=1):
        lines.append("")
        lines.append(f"### Signal {idx}：{_value(signal, 'headline')}")
        lines.append(f"事件描述：{_value(signal, 'headline')}")
        lines.append("")
        lines.append(f"问题还原：{_value(signal, 'problem_statement')}")
        lines.append("")
        lines.append(f"所属主题：{_value(signal, 'theme')}")
        lines.append(f"所属链路：{_value(signal, 'chain')}")
        lines.append(f"所属节点：{_value(signal, 'node')}")
        lines.append("")
        lines.append(f"旧方案：{_value(signal, 'old_solution')}")
        lines.append("")
        lines.append(f"新变化：{_value(signal, 'new_solution')}")
        lines.append("")
        lines.append(f"为什么重要：{_value(signal, 'why_it_matters')}")
        lines.append("")
        lines.append("待验证问题：")
        for i, question in enumerate(_open_questions(signal), start=1):
            lines.append(f"{i}. {question}")
        lines.append("")
        lines.append(f"判断更新：{_value(signal, 'why_it_matters')}")
        links = _evidence_links(signal)
        lines.append("")
        lines.append("关键原文链接：")
        if links:
            for link in links:
                lines.append(f"- {link}")
        else:
            lines.append("- 暂无结构化原文链接，请回查原始新闻表。")

    lines.append("")
    lines.append("## 分主题观察")
    for theme in THEME_ORDER:
        theme_signals = grouped.get(theme, [])
        lines.append("")
        lines.append(f"### {theme}")
        if not theme_signals:
            lines.append("- 新增信号：无")
            lines.append("- 判断更新：暂无足够新证据。")
            lines.append("- 当前卡点：缺少可以推动判断变化的新增信号。")
            lines.append("- 待验证问题：是否会在后续24小时内出现更强证据。")
            continue

        primary = theme_signals[0]
        lines.append("- 新增信号：")
        for signal in theme_signals[:3]:
            lines.append(f"  - {_value(signal, 'headline')}")
        lines.append(f"- 判断更新：{_value(primary, 'why_it_matters')}")
        lines.append("- 当前卡点：仍需更多公开案例、数字或官方信息来确认趋势。")
        questions = _open_questions(primary)
        lines.append(f"- 待验证问题：{questions[0] if questions else '暂无'}")

    lines.append("")
    lines.append("## 今日判断更新")
    if not top:
        lines.append("")
        lines.append("今天没有足够强的证据触发判断更新。")
    for idx, signal in enumerate(top, start=1):
        lines.append("")
        lines.append(f"{idx}. 原判断：主题“{_value(signal, 'theme')}”相关判断仍需更多证据。")
        lines.append(f"   新证据：{_value(signal, 'headline')}")
        lines.append(f"   更新后判断：{_value(signal, 'why_it_matters')}")

    lines.append("")
    lines.append("## 高优先级待验证问题")
    if not top:
        lines.append("")
        lines.append("1. 今天暂无高优先级待验证问题。")
    for idx, signal in enumerate(top, start=1):
        questions = _open_questions(signal)
        lines.append("")
        lines.append(f"{idx}. 问题：{questions[0]}")
        lines.append("   为什么关键：这决定它是短期噪音，还是足以更新行业判断的证据。")
        lines.append("   下一步该看什么证据：企业案例、价格数据、政策细则、官方公告或复盘文章。")

    lines.append("")
    lines.append("## 关键原文链接")
    if not top:
        lines.append("- 暂无")
    for signal in top:
        links = _evidence_links(signal)
        if not links:
            lines.append(f"- {_value(signal, 'headline')} | {_value(signal, 'theme')} | 暂无结构化链接")
            continue
        for link in links:
            lines.append(f"- {_value(signal, 'headline')} | {_value(signal, 'theme')} | {link}")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a markdown daily report draft from signals.")
    parser.add_argument("--input", help="Path to signals JSON. Reads stdin when omitted.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD. Defaults to today.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = read_payload(args.input)
    signals = payload.get("signals", [])
    report_date = args.date or datetime.now().strftime("%Y-%m-%d")
    print(build_report(signals, report_date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
