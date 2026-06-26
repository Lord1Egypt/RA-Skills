#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fetch_arxiv_weekly.py

功能：
- 根据 arXiv 分类代码 + 关键词检索论文
- 过滤最近 N 天（默认 7 天）
- 输出结构化 JSON，供 OpenClaw skill 后续生成周报

示例：
python3 fetch_arxiv_weekly.py --category cs.CV --keywords "IRSTD" --days 7 --max-results 30

说明：
- 这里使用 arXiv 官方 API（Atom XML）
- 日期优先使用 updated 字段做最近时间窗口过滤
- 相关性打分采用简单规则：标题命中 > 摘要命中
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List, Optional

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


@dataclass
class ArxivPaper:
    title: str
    summary: str
    authors: List[str]
    published: str
    updated: str
    arxiv_id: str
    abs_url: str
    pdf_url: str
    primary_category: Optional[str]
    categories: List[str]
    relevance_score: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="按 arXiv 分类和关键词检索最近一周论文，并输出 JSON。"
    )
    parser.add_argument(
        "--category",
        required=True,
        help="arXiv 分类代码，例如 cs.LG、cs.CL、cs.CV。",
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help='关键词列表，使用英文逗号分隔，例如 "multimodal,reasoning,agent"。',
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="时间窗口，默认最近 7 天。",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=30,
        help="从 arXiv 拉取的候选论文数量，默认 30。",
    )
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        default="lastUpdatedDate",
        help="arXiv API 排序方式，默认按最后更新时间排序。",
    )
    parser.add_argument(
        "--sort-order",
        choices=["ascending", "descending"],
        default="descending",
        help="排序方向，默认降序。",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="是否美化 JSON 输出。",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def split_keywords(keywords_text: str) -> List[str]:
    items = [k.strip() for k in keywords_text.split(",")]
    return [k for k in items if k]


def build_search_query(category: str, keywords: List[str]) -> str:
    """
    构造 arXiv search_query。
    示例：
      cat:cs.LG AND (all:"multimodal" AND all:"reasoning")
    """
    category = category.strip()
    if not category:
        raise ValueError("category 不能为空")

    query_parts = [f"cat:{category}"]

    if keywords:
        keyword_parts = [f'all:"{kw}"' for kw in keywords]
        query_parts.append("(" + " AND ".join(keyword_parts) + ")")

    return " AND ".join(query_parts)


def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OpenClaw-arxiv-weekly-report/0.1 (Python urllib)"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def parse_iso_datetime(value: str) -> dt.datetime:
    # arXiv 常见格式：2026-03-18T12:34:56Z
    return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc
    )


def compute_relevance_score(title: str, summary: str, keywords: List[str]) -> float:
    title_l = title.lower()
    summary_l = summary.lower()
    score = 0.0

    for kw in keywords:
        kw_l = kw.lower()
        if kw_l in title_l:
            score += 3.0
        if kw_l in summary_l:
            score += 1.5

    # 轻微偏向标题更短更聚焦的论文
    if len(title.split()) <= 20:
        score += 0.2

    return score


def parse_entry(entry: ET.Element, keywords: List[str]) -> ArxivPaper:
    title = normalize_text(entry.findtext("atom:title", default="", namespaces=ATOM_NS))
    summary = normalize_text(entry.findtext("atom:summary", default="", namespaces=ATOM_NS))
    published = normalize_text(
        entry.findtext("atom:published", default="", namespaces=ATOM_NS)
    )
    updated = normalize_text(
        entry.findtext("atom:updated", default="", namespaces=ATOM_NS)
    )

    authors = []
    for author in entry.findall("atom:author", ATOM_NS):
        name = normalize_text(author.findtext("atom:name", default="", namespaces=ATOM_NS))
        if name:
            authors.append(name)

    abs_url = ""
    pdf_url = ""
    arxiv_id = ""

    id_text = normalize_text(entry.findtext("atom:id", default="", namespaces=ATOM_NS))
    if id_text:
        abs_url = id_text
        arxiv_id = id_text.rstrip("/").split("/")[-1]

    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href", "").strip()
        title_attr = link.attrib.get("title", "").strip().lower()
        type_attr = link.attrib.get("type", "").strip().lower()

        if href and not abs_url and link.attrib.get("rel") == "alternate":
            abs_url = href

        if title_attr == "pdf" or type_attr == "application/pdf":
            pdf_url = href

    categories = []
    primary_category = None

    for cat in entry.findall("atom:category", ATOM_NS):
        term = cat.attrib.get("term", "").strip()
        if term:
            categories.append(term)

    if categories:
        primary_category = categories[0]

    score = compute_relevance_score(title, summary, keywords)

    return ArxivPaper(
        title=title,
        summary=summary,
        authors=authors,
        published=published,
        updated=updated,
        arxiv_id=arxiv_id,
        abs_url=abs_url,
        pdf_url=pdf_url,
        primary_category=primary_category,
        categories=categories,
        relevance_score=score,
    )


def query_arxiv(
    category: str,
    keywords: List[str],
    max_results: int,
    sort_by: str,
    sort_order: str,
) -> List[ArxivPaper]:
    search_query = build_search_query(category, keywords)
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    url = ARXIV_API_URL + "?" + urllib.parse.urlencode(params)

    xml_text = fetch_url(url)
    root = ET.fromstring(xml_text)

    entries = root.findall("atom:entry", ATOM_NS)
    papers = [parse_entry(entry, keywords) for entry in entries]
    return papers


def filter_recent_papers(papers: List[ArxivPaper], days: int) -> List[ArxivPaper]:
    now = dt.datetime.now(dt.timezone.utc)
    threshold = now - dt.timedelta(days=days)

    result = []
    for paper in papers:
        date_str = paper.updated or paper.published
        if not date_str:
            continue
        try:
            paper_dt = parse_iso_datetime(date_str)
        except ValueError:
            continue
        if paper_dt >= threshold:
            result.append(paper)
    return result


def sort_papers(papers: List[ArxivPaper]) -> List[ArxivPaper]:
    # 先按 relevance_score 降序，再按 updated 降序
    def key_fn(p: ArxivPaper):
        try:
            updated_dt = parse_iso_datetime(p.updated or p.published)
        except ValueError:
            updated_dt = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
        return (p.relevance_score, updated_dt.timestamp())

    return sorted(papers, key=key_fn, reverse=True)


def build_output(
    category: str,
    keywords: List[str],
    days: int,
    fetched_count: int,
    papers: List[ArxivPaper],
) -> dict:
    return {
        "query": {
            "category": category,
            "keywords": keywords,
            "days": days,
            "fetched_count": fetched_count,
            "matched_count": len(papers),
            "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "papers": [asdict(p) for p in papers],
    }


def main() -> int:
    args = parse_args()

    keywords = split_keywords(args.keywords)
    if not keywords:
        print("错误：至少需要一个关键词。", file=sys.stderr)
        return 2

    try:
        papers = query_arxiv(
            category=args.category,
            keywords=keywords,
            max_results=args.max_results,
            sort_by=args.sort_by,
            sort_order=args.sort_order,
        )
    except urllib.error.URLError as e:
        print(f"错误：网络请求失败：{e}", file=sys.stderr)
        return 3
    except ET.ParseError as e:
        print(f"错误：解析 arXiv 返回数据失败：{e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"错误：检索失败：{e}", file=sys.stderr)
        return 5

    fetched_count = len(papers)
    papers = filter_recent_papers(papers, args.days)
    papers = sort_papers(papers)

    output = build_output(
        category=args.category,
        keywords=keywords,
        days=args.days,
        fetched_count=fetched_count,
        papers=papers,
    )

    if args.pretty:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())