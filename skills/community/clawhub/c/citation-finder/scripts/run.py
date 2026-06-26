"""
run.py — Main entry point for Citation Finder
Usage: python run.py "your fuzzy paper title"
"""

import sys
import json
import concurrent.futures
from rapidfuzz import fuzz

# Add scripts dir to path when running standalone
import os
sys.path.insert(0, os.path.dirname(__file__))

from search_en import search_english
from search_cn import search_chinese
from format_cite import format_all


CONFIDENCE_HIGH = 75   # Return directly
CONFIDENCE_MID  = 45   # Show candidates


def detect_language(query: str) -> str:
    """Rough language detection: chinese / english / mixed."""
    cn_chars = sum(1 for c in query if '\u4e00' <= c <= '\u9fff')
    ratio = cn_chars / max(len(query), 1)
    if ratio > 0.3:
        return "chinese"
    elif ratio > 0.05:
        return "mixed"
    return "english"


def search_all(query: str) -> list[dict]:
    """Search English and Chinese sources in parallel."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_en = executor.submit(search_english, query)
        future_cn = executor.submit(search_chinese, query)
        en_results = future_en.result()
        cn_results = future_cn.result()

    all_results = en_results + cn_results

    # Re-score everything against the original query
    for r in all_results:
        r["confidence"] = fuzz.token_sort_ratio(query.lower(), r["title"].lower())

    all_results.sort(key=lambda x: x["confidence"], reverse=True)
    return all_results


def format_output(paper: dict, query: str) -> str:
    """Format the final output with citations and source URL."""
    citations = format_all(paper)

    lines = []
    lines.append(f"📄 找到文献：**{paper['title']}**")

    authors = paper.get("authors", [])
    if authors:
        author_names = []
        for a in authors[:3]:
            name = a.get("family", "")
            given = a.get("given", "")
            if given:
                name = f"{given} {name}"
            author_names.append(name)
        if len(paper["authors"]) > 3:
            author_names.append("等")
        lines.append(f"👤 作者：{', '.join(author_names)}")

    if paper.get("year"):
        lines.append(f"📅 年份：{paper['year']}")
    if paper.get("journal"):
        lines.append(f"📰 期刊/来源：{paper['journal']}")

    doi = paper.get("doi", "")
    url = paper.get("url", "")
    if doi:
        lines.append(f"🔗 DOI：https://doi.org/{doi}")
    elif url:
        lines.append(f"🔗 链接：{url}")

    lines.append("")
    lines.append("─── 引文格式 ───")
    for fmt_name, cite_text in citations.items():
        lines.append(f"\n【{fmt_name}】\n{cite_text}")

    return "\n".join(lines)


def format_candidates(candidates: list[dict]) -> str:
    """Format candidate list for user to choose from."""
    lines = ["🔍 找到以下候选文献，请回复编号确认：", ""]
    for i, c in enumerate(candidates, 1):
        authors = c.get("authors", [])
        first_author = authors[0].get("family", "") if authors else ""
        year = c.get("year", "")
        journal = c.get("journal", "")
        source = c.get("source", "")
        conf = c.get("confidence", 0)
        lines.append(f"{i}. 《{c['title']}》")
        if first_author or year:
            lines.append(f"   {first_author}{', ' + str(year) if year else ''}{', ' + journal if journal else ''}")
        lines.append(f"   来源：{source}  匹配度：{conf}%")
        lines.append("")
    lines.append("回复 1/2/3 选择对应文献，或输入更多信息重新搜索。")
    return "\n".join(lines)


def find_citation(query: str) -> str:
    """Main function: search, match, and format citation."""
    print(f"🔍 搜索中：{query}", file=sys.stderr)

    results = search_all(query)

    if not results:
        return "❌ 未找到相关文献，请尝试提供更准确的标题或作者信息。"

    top = results[0]
    confidence = top.get("confidence", 0)

    if confidence >= CONFIDENCE_HIGH:
        return format_output(top, query)
    elif confidence >= CONFIDENCE_MID:
        candidates = results[:3]
        return format_candidates(candidates)
    else:
        candidates = results[:3]
        header = f"⚠️ 未能精确匹配，以下是相关性最高的结果（匹配度 {confidence}%）：\n"
        return header + format_candidates(candidates)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python run.py \"模糊文献标题\"")
        print("示例: python run.py \"attention is all you need\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = find_citation(query)
    print(result)
