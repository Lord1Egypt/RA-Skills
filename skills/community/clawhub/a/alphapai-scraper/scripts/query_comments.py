#!/usr/bin/env python3
"""
Query indexed AlphaPai comments and generate a focused summary.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any

from analyze import fallback_analysis, run_ai_analysis
from archive_store import query_comments
from common import ensure_runtime_dirs, load_settings

NO_RESULT_TEMPLATE = "alphapai最近{days:g}天没有相关点评"


def build_query_prompt(
    query: str,
    lookback_days: float,
    items: list[dict[str, Any]],
    settings: dict[str, Any],
) -> str:
    target_length = int(settings["ai"]["target_length_chars"])
    custom_requirements = str(settings["ai"].get("custom_requirements") or "").strip()
    custom_block = f"\n额外格式要求：\n{custom_requirements}\n" if custom_requirements else ""

    snippets: list[str] = []
    for index, item in enumerate(items, start=1):
        snippets.extend(
            [
                f"[{index:02d}] {item['title']}",
                f"时间: {item['time_label']} | 入库时间: {item['scraped_at']}",
                item["content"][:500],
                "",
            ]
        )
    evidence = "\n".join(snippets).strip()

    return f"""你是一位擅长二级市场信息检索和归纳的研究员。请根据 AlphaPai 点评库中最近 {lookback_days:g} 天与“{query}”相关的原文，输出一份适合手机阅读的中文摘要。

必须遵守以下要求：
1. 总字数控制在 {target_length - 100} 到 {target_length + 150} 字。
2. 第一段必须是“检索结论”，直接回答最近 {lookback_days:g} 天关于“{query}”到底出现了哪些重点更新。
3. 第二部分必须是“时间线 / 重点更新”，按时间顺序或重要性提炼最关键的信息，不要遗漏重复出现的重要信号。
4. 第三部分必须是“行业 / 标的归类”，优先按行业或具体股票标的分组。
5. 第四部分必须是“边际变化”，重点突出加单、涨价、公告、订单、政策、业绩、预期差等增量信息。
6. 最后一部分必须是“待验证”，把传闻、口径不完整、强结论不足的内容单独列出。
7. 每个要点尽量 1-2 行，适合手机阅读。
8. 重要股票、公司、产品、产业链关键词请加粗。{custom_block}

建议输出骨架：
# AlphaPai 检索摘要
## 检索结论
## 时间线 / 重点更新
## 行业 / 标的归类
## 边际变化
## 待验证

下面是命中的原文片段：

{evidence}
"""


def fallback_query_analysis(query: str, lookback_days: float, items: list[dict[str, Any]]) -> str:
    pseudo_raw = [
        "# AlphaPai query corpus",
        f"- query: {query}",
        f"- days: {lookback_days:g}",
        "",
    ]
    for item in items:
        pseudo_raw.extend(
            [
                f"## {item['title']}",
                f"- 时间: `{item['time_label']}`",
                f"- 来源: `{item['source_strategy']}`",
                item["content"],
                "",
            ]
        )
    base = fallback_analysis("\n".join(pseudo_raw), lookback_days * 24)
    base = base.replace("# Alpha派摘要", "# AlphaPai 检索摘要", 1)
    base = base.replace("## 今日结论", "## 检索结论", 1)
    base = base.replace("## 边际变化 / 增量信息 TOP5", "## 时间线 / 重点更新", 1)
    base = base.replace("## 行业 / 标的脉络", "## 行业 / 标的归类", 1)
    base = base.replace("## 情绪温度计", "## 边际变化", 1)
    tail = "\n## 待验证\n- 规则引擎仅基于命中文本做归纳，建议结合原文二次确认。\n"
    if "## 待验证" not in base:
        base = base.rstrip() + tail
    return base


def generate_query_report(
    settings: dict[str, Any],
    *,
    query: str,
    lookback_days: float,
    limit: int = 50,
    retrieval_mode: str = "hybrid",
) -> dict[str, Any]:
    runtime_dirs = ensure_runtime_dirs(settings)
    result = query_comments(
        settings,
        query=query,
        lookback_days=lookback_days,
        limit=limit,
        retrieval_mode=retrieval_mode,
    )
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = runtime_dirs["report_dir"] / f"{stamp}_query_summary.md"
    meta_path = runtime_dirs["runtime_dir"] / f"{stamp}_query.json"

    if not result["items"]:
        message = NO_RESULT_TEMPLATE.format(days=lookback_days)
        report_path.write_text(message + "\n", encoding="utf-8")
        meta_path.write_text(
            json.dumps(
                {
                    "query": query,
                    "lookback_days": lookback_days,
                    "matched": 0,
                    "terms": result.get("terms", []),
                    "db_path": result.get("db_path", ""),
                    "vector_path": result.get("vector_path", ""),
                    "retrieval_mode": retrieval_mode,
                    "report_file": str(report_path),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return {
            "ok": True,
            "matched": 0,
            "report_file": str(report_path),
            "meta_file": str(meta_path),
            "message": message,
        }

    prompt = build_query_prompt(query, lookback_days, result["items"], settings)
    report = run_ai_analysis(prompt, settings)
    engine = "ai"
    if not report:
        report = fallback_query_analysis(query, lookback_days, result["items"])
        engine = "fallback"

    report_path.write_text(report.strip() + "\n", encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "query": query,
                "lookback_days": lookback_days,
                "matched": len(result["items"]),
                "terms": result.get("terms", []),
                "db_path": result.get("db_path", ""),
                "vector_path": result.get("vector_path", ""),
                "retrieval_mode": retrieval_mode,
                "engine": engine,
                "report_file": str(report_path),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "ok": True,
        "matched": len(result["items"]),
        "report_file": str(report_path),
        "meta_file": str(meta_path),
        "engine": engine,
        "terms": result.get("terms", []),
        "vector_path": result.get("vector_path", ""),
        "retrieval_mode": retrieval_mode,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query AlphaPai indexed comments")
    parser.add_argument("--query", required=True, help="Keyword or topic to search")
    parser.add_argument("--days", type=float, default=7, help="Look back N days")
    parser.add_argument("--limit", type=int, default=50, help="Maximum matched records")
    parser.add_argument(
        "--mode",
        choices=["exact", "vector", "hybrid"],
        default="hybrid",
        help="Retrieval mode",
    )
    parser.add_argument("--json", action="store_true", help="Print raw retrieval result as JSON")
    parser.add_argument("--settings", help="Path to settings file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = load_settings(args.settings)
    if args.json:
        result = query_comments(
            settings,
            query=args.query,
            lookback_days=args.days,
            limit=args.limit,
            retrieval_mode=args.mode,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    result = generate_query_report(
        settings,
        query=args.query,
        lookback_days=args.days,
        limit=args.limit,
        retrieval_mode=args.mode,
    )
    if result["ok"]:
        print(result["report_file"])
        return 0
    print(result.get("error", "query failed"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
