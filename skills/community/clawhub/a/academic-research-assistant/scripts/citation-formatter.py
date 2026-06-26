#!/usr/bin/env python3
"""
参考文献格式转换工具
支持常见格式之间的转换：APA, IEEE, GB/T 7714
"""

import json
import sys
from typing import Dict, List, Optional


def format_apa(ref: Dict) -> str:
    """生成APA 7th格式的参考文献"""
    authors = ref.get("authors", [])
    year = ref.get("year", "")
    title = ref.get("title", "")
    journal = ref.get("journal", "")
    volume = ref.get("volume", "")
    issue = ref.get("issue", "")
    pages = ref.get("pages", "")
    doi = ref.get("doi", "")
    publisher = ref.get("publisher", "")

    # 作者格式：LastName, F., & LastName, F.
    author_str = ""
    if authors:
        parts = []
        for a in authors:
            parts.append(f"{a.get('last', '')}, {a.get('first', '')[:1]}.")
        if len(parts) > 1:
            author_str = ", ".join(parts[:-1]) + f", & {parts[-1]}"
        else:
            author_str = parts[0]

    # 期刊论文
    if journal:
        result = f"{author_str} ({year}). {title}. *{journal}*, *{volume}*"
        if issue:
            result += f"({issue})"
        result += f", {pages}."
        if doi:
            result += f" https://doi.org/{doi}"
        return result

    # 图书
    result = f"{author_str} ({year}). *{title}*"
    if publisher:
        result += f". {publisher}."
    return result


def format_ieee(ref: Dict) -> str:
    """生成IEEE格式的参考文献"""
    authors = ref.get("authors", [])
    year = ref.get("year", "")
    title = ref.get("title", "")
    journal = ref.get("journal", "")
    volume = ref.get("volume", "")
    issue = ref.get("issue", "")
    pages = ref.get("pages", "")
    doi = ref.get("doi", "")
    publisher = ref.get("publisher", "")

    # 作者格式：F. LastName, F. LastName, and F. LastName
    author_str = ""
    if authors:
        parts = []
        for a in authors:
            first = a.get("first", "")
            last = a.get("last", "")
            if first:
                parts.append(f"{first[:1]}. {last}")
            else:
                parts.append(last)
        if len(parts) > 1:
            author_str = ", ".join(parts[:-1]) + f", and {parts[-1]}"
        else:
            author_str = parts[0]

    # 期刊论文
    if journal:
        result = f'{author_str}, "{title}," *{journal}*, vol. {volume}'
        if issue:
            result += f", no. {issue}"
        result += f", pp. {pages}, {year}."
        if doi:
            result += f" doi: {doi}"
        return result

    # 图书
    result = f'{author_str}, *{title}*'
    if publisher:
        result += f". {publisher}"
    result += f", {year}."
    return result


def format_gbt7714(ref: Dict) -> str:
    """生成GB/T 7714格式的参考文献（中文学术期刊格式）"""
    authors = ref.get("authors", [])
    year = ref.get("year", "")
    title = ref.get("title", "")
    journal = ref.get("journal", "")
    volume = ref.get("volume", "")
    issue = ref.get("issue", "")
    pages = ref.get("pages", "")
    doi = ref.get("doi", "")
    pub_type = ref.get("type", "J")

    # 作者格式
    author_str = ""
    if authors:
        parts = []
        for a in authors:
            last = a.get("last", "")
            first = a.get("first", "")
            parts.append(f"{last}{first}")
        if len(parts) > 3:
            author_str = ", ".join(parts[:3]) + ", 等"
        else:
            author_str = ", ".join(parts)

    if pub_type == "J":  # 期刊
        result = f"{author_str}. {title}[J]. {journal}, {year}"
        if volume:
            result += f", {volume}"
        if issue:
            result += f"({issue})"
        if pages:
            result += f": {pages}."
        return result
    elif pub_type == "M":  # 图书
        publisher = ref.get("publisher", "")
        result = f"{author_str}. {title}[M]. {publisher}, {year}."
        return result
    elif pub_type == "D":  # 学位论文
        institution = ref.get("institution", "")
        result = f"{author_str}. {title}[D]. {institution}, {year}."
        return result
    elif pub_type == "C":  # 会议
        conference = ref.get("conference", "")
        result = f"{author_str}. {title}[C]//{conference}. {publisher}, {year}"
        if pages:
            result += f": {pages}."
        return result

    return ""


def convert_citation(ref: Dict, target_format: str = "apa") -> str:
    """
    转换参考文献格式

    Args:
        ref: 参考文献数据字典
        target_format: 目标格式 ("apa", "ieee", "gbt7714")

    Returns:
        格式化的参考文献字符串
    """
    formats = {
        "apa": format_apa,
        "ieee": format_ieee,
        "gbt7714": format_gbt7714,
        "gb": format_gbt7714,
    }

    formatter = formats.get(target_format.lower(), format_apa)
    return formatter(ref)


# 示例用法
DEMO_REFS = {
    "journal_article": {
        "authors": [
            {"last": "Zhang", "first": "Lei"},
            {"last": "Wang", "first": "Yu"},
            {"last": "Li", "first": "Xiaoming"},
        ],
        "year": "2025",
        "title": "Deep learning in medical imaging: A comprehensive review",
        "journal": "Nature Reviews Bioengineering",
        "volume": "3",
        "issue": "2",
        "pages": "115-132",
        "doi": "10.1038/s44286-025-00001-x",
    },
    "book": {
        "authors": [
            {"last": "Smith", "first": "John"},
            {"last": "Chen", "first": "Wei"},
        ],
        "year": "2024",
        "title": "Machine Learning for Healthcare",
        "publisher": "MIT Press",
    },
    "chinese_journal": {
        "authors": [
            {"last": "张", "first": "三"},
            {"last": "李", "first": "四"},
            {"last": "王", "first": "五"},
        ],
        "year": "2025",
        "title": "基于深度学习的心电图分析方法研究",
        "journal": "中国生物医学工程学报",
        "volume": "44",
        "issue": "2",
        "pages": "123-135",
        "type": "J",
    },
}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        for key, ref in DEMO_REFS.items():
            print(f"\n=== {key} ===")
            print(f"APA:     {convert_citation(ref, 'apa')}")
            print(f"IEEE:    {convert_citation(ref, 'ieee')}")
            print(f"GB/T 7714: {convert_citation(ref, 'gbt7714')}")
    else:
        # 从stdin读取JSON
        try:
            data = json.load(sys.stdin)
            fmt = sys.argv[1] if len(sys.argv) > 1 else "apa"
            result = convert_citation(data, fmt)
            print(result)
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            print("使用: citation-formatter.py <格式(apa/ieee/gbt7714)> < input.json")
            print(" 或: citation-formatter.py demo")
