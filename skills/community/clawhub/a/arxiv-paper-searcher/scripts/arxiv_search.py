#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv 论文搜索脚本
支持自定义搜索关键词，获取最新论文数据。

说明：
- 该脚本负责搜索与结构化数据输出
- 热点提取、创新性评估、趋势判断建议由上层 skill/agent 完成
- 默认使用中国时区（Asia/Shanghai）记录搜索时间
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

try:
    import arxiv
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "未安装依赖 arxiv，请先执行：pip install arxiv"
    ) from exc

CHINA_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_MAX_RESULTS = 20
MAX_RESULTS_LIMIT = 100


def positive_int(value: str) -> int:
    """argparse 用正整数校验。"""
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("数量必须是整数") from exc

    if ivalue <= 0:
        raise argparse.ArgumentTypeError("数量必须大于 0")
    if ivalue > MAX_RESULTS_LIMIT:
        raise argparse.ArgumentTypeError(f"数量不能超过 {MAX_RESULTS_LIMIT}")
    return ivalue


def normalize_sort(sort: str) -> arxiv.SortCriterion:
    mapping = {
        "date": arxiv.SortCriterion.SubmittedDate,
        "updated": arxiv.SortCriterion.LastUpdatedDate,
        "relevance": arxiv.SortCriterion.Relevance,
    }
    return mapping[sort]


def format_result_datetime(dt: datetime | None) -> str | None:
    """保留完整时间戳；若有时区信息则转为 Asia/Shanghai。"""
    if dt is None: return None
    if dt.tzinfo is not None: dt = dt.astimezone(CHINA_TZ)
    return dt.isoformat(timespec="seconds")


def search_papers(query: str, max_results: int = DEFAULT_MAX_RESULTS, sort: str = "date") -> List[Dict[str, Any]]:
    """
    搜索 arXiv 论文。

    Args:
        query: 搜索关键词（支持 arXiv 语法）
        max_results: 最大结果数
        sort: 排序方式，支持 date / updated / relevance

    Returns:
        论文列表
    """
    print("正在从 arXiv 搜索论文...")
    print(f"搜索词：{query}")
    print(f"最大结果数：{max_results}")
    print(f"排序方式：{sort}")
    print()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=normalize_sort(sort),
        sort_order=arxiv.SortOrder.Descending,
    )

    client = arxiv.Client(page_size=min(max_results, 100), delay_seconds=3.0, num_retries=3)

    papers: List[Dict[str, Any]] = []
    for result in client.results(search):
        published_at = format_result_datetime(result.published)
        updated_at = format_result_datetime(result.updated)
        
        papers.append(
            {
                "title": result.title.strip(),
                "authors": [author.name for author in result.authors],
                "published": published_at,
                "updated": updated_at,
                "published_date": published_at[:10] if published_at else None,
                "updated_date": updated_at[:10] if updated_at else None,
                "summary": " ".join(result.summary.split()),
                "pdf_url": result.pdf_url,
                "entry_id": result.entry_id,
                "primary_category": getattr(result, "primary_category", None),
                "categories": list(result.categories),
            }
        )

    return papers


def save_papers_data(papers: List[Dict[str, Any]], query: str, filepath: str, sort: str) -> str:
    """保存论文数据到 JSON 文件。"""
    directory = os.path.dirname(os.path.abspath(filepath))
    if directory:
        os.makedirs(directory, exist_ok=True)

    data = {
        "search_time": datetime.now(CHINA_TZ).isoformat(timespec="seconds"),
        "timezone": "Asia/Shanghai",
        "query": query,
        "sort": sort,
        "count": len(papers),
        "papers": papers,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"论文数据已保存：{filepath}")
    return filepath


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="arXiv 论文搜索工具")
    parser.add_argument("--query", "-q", required=True, help="搜索关键词")
    parser.add_argument("--max", "-m", type=positive_int, default=DEFAULT_MAX_RESULTS, help=f"最大结果数，1-{MAX_RESULTS_LIMIT}")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径，可只写文件名")
    parser.add_argument("--sort", "-s", choices=["date", "updated", "relevance"], default="date", help="排序方式")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print("=" * 60)
    print("📊 arXiv 论文搜索")
    print("=" * 60)
    print()

    try:
        papers = search_papers(args.query, max_results=args.max, sort=args.sort)

        if not papers:
            print("❌ 未找到相关论文")
            return 1

        print(f"✅ 找到 {len(papers)} 篇论文")
        print()

        if args.output:
            save_papers_data(papers, args.query, args.output, args.sort)

        print("=" * 60)
        print("📋 论文列表")
        print("=" * 60)
        print()

        for i, paper in enumerate(papers, 1):
            authors_preview = ", ".join(paper["authors"][:3])
            if len(paper["authors"]) > 3: authors_preview += " et al."

            categories_preview = ", ".join(paper["categories"][:3]) if paper["categories"] else "N/A"
            link = paper["pdf_url"] or paper["entry_id"]
            display_date = paper.get("published_date") or (paper["published"][:10] if paper.get("published") else "N/A")

            print(f"{i}. {paper['title']}")
            print(f"   作者：{authors_preview}")
            print(f"   时间：{display_date}")
            print(f"   分类：{categories_preview}")
            print(f"   链接：{link}")
            print()

        print("=" * 60)
        print("✅ 搜索完成！")
        if args.output:
            print(f"📁 数据文件：{args.output}")
        print("=" * 60)
        return 0

    except KeyboardInterrupt:
        print("\n⚠️ 用户已中断")
        return 130
    except Exception as e:
        print(f"❌ 执行出错：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
