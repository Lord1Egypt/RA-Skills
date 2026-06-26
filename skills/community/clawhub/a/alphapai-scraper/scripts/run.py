#!/usr/bin/env python3
"""
AlphaPai one-shot runner.
"""

from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze import generate_report
from common import load_settings
from query_comments import generate_query_report
from scraper import scrape_latest_comments
from send_feishu import send_feishu_report


def notify(title: str, message: str) -> None:
    try:
        script = (
            f'display notification "{message}" with title "{title}" sound name "Glass"'
        )
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True, text=True)
    except Exception:
        pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AlphaPai scraper runner")
    parser.add_argument("--hours", type=float, help="Look back N hours. Defaults to settings.")
    parser.add_argument("--query", help="Search indexed AlphaPai comments instead of scraping.")
    parser.add_argument("--days", type=float, default=7, help="Look back N days when querying.")
    parser.add_argument("--query-limit", type=int, default=50, help="Maximum indexed items to summarize.")
    parser.add_argument(
        "--query-mode",
        choices=["exact", "vector", "hybrid"],
        default="hybrid",
        help="Retrieval mode when querying the indexed archive.",
    )
    parser.add_argument("--settings", help="Path to settings JSON.")
    parser.add_argument("--output-dir", help="Override output base dir for this run.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Force headless browser for this run.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Force visible browser for this run.",
    )
    parser.add_argument(
        "--skip-feishu",
        action="store_true",
        help="Generate files only, do not send webhook message.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = load_settings(args.settings)
    if args.output_dir:
        settings["output"]["base_dir"] = args.output_dir
    if args.headless:
        settings["browser"]["headless"] = True
    if args.headed:
        settings["browser"]["headless"] = False

    if args.query:
        print("AlphaPai 点评库查询")
        print("=" * 48)
        print(f"查询词: {args.query}")
        print(f"时间窗口: 最近 {args.days:g} 天")
        print(f"检索模式: {args.query_mode}")
        print(f"输出目录: {settings['output']['base_dir']}")
        notify("AlphaPai", "开始查询点评库")

        query_result = generate_query_report(
            settings,
            query=args.query,
            lookback_days=args.days,
            limit=args.query_limit,
            retrieval_mode=args.query_mode,
        )
        if not query_result["ok"]:
            notify("AlphaPai", "查询失败，请查看终端日志")
            print(f"\n❌ 查询失败: {query_result['error']}")
            return 1

        webhook_result = None
        if not args.skip_feishu:
            webhook_result = send_feishu_report(
                report_file=query_result["report_file"],
                settings=settings,
                lookback_hours=args.days * 24,
            )

        notify("AlphaPai", "查询完成")
        print("\n✅ 查询完成")
        print(f"摘要: {query_result['report_file']}")
        print(f"命中条数: {query_result['matched']}")
        if query_result.get("terms"):
            print(f"检索词: {', '.join(query_result['terms'])}")
        print(f"向量索引: {query_result.get('vector_path', 'N/A')}")
        if webhook_result:
            if webhook_result["sent"]:
                print("飞书: 已发送")
            elif webhook_result["reason"]:
                print(f"飞书: 未发送（{webhook_result['reason']}）")
        return 0

    lookback_hours = (
        args.hours
        if args.hours is not None
        else float(settings["scrape"]["default_lookback_hours"])
    )

    print("AlphaPai 评论抓取")
    print("=" * 48)
    print(f"回看窗口: {lookback_hours:g} 小时")
    print(f"输出目录: {settings['output']['base_dir']}")
    notify("AlphaPai", "开始抓取最新点评")

    scrape_result = asyncio.run(
        scrape_latest_comments(settings=settings, lookback_hours=lookback_hours)
    )
    if not scrape_result["ok"]:
        notify("AlphaPai", "抓取失败，请查看终端日志")
        print(f"\n❌ 抓取失败: {scrape_result['error']}")
        return 1

    notify("AlphaPai", "原文抓取完成，开始生成摘要")
    report_result = generate_report(
        raw_file=scrape_result["raw_file"],
        settings=settings,
        lookback_hours=lookback_hours,
    )

    if not report_result["ok"]:
        notify("AlphaPai", "摘要生成失败，请查看终端日志")
        print(f"\n❌ 摘要生成失败: {report_result['error']}")
        return 1

    webhook_result = None
    if not args.skip_feishu:
        webhook_result = send_feishu_report(
            report_file=report_result["report_file"],
            settings=settings,
            lookback_hours=lookback_hours,
        )

    notify("AlphaPai", "全部完成")
    print("\n✅ 执行完成")
    print(f"原文: {scrape_result['raw_file']}")
    print(f"结构化: {scrape_result['normalized_file']}")
    print(f"索引库: {scrape_result['db_path']}")
    print(f"摘要: {report_result['report_file']}")
    if webhook_result:
        if webhook_result["sent"]:
            print("飞书: 已发送")
        elif webhook_result["reason"]:
            print(f"飞书: 未发送（{webhook_result['reason']}）")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
