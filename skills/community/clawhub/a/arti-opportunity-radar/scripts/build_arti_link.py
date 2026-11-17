#!/usr/bin/env python3
"""Build a safe ARTi news-analysis deep link."""

from __future__ import annotations

import argparse
from urllib.parse import urlencode, urlparse


DEFAULT_BASE_URL = "https://artifin.ai/app/agent"


def http_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("expected an absolute http(s) URL")
    return value


def single_line(value: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise argparse.ArgumentTypeError("value must not be empty")
    return cleaned


def build_link(
    *,
    symbol: str,
    label: str,
    title: str,
    source_url: str,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    prompt = (
        f"请分析新闻《{title}》对 {label}（{symbol}）的潜在影响。"
        f"原文：{source_url}。"
        "请先核验事实，再分析业务暴露度、因果链、反方证据、关键风险和仍缺失的信息；"
        "不要给出买卖建议或确定性涨跌结论。"
    )
    query = urlencode(
        {
            "q": prompt,
            "agent": "news-analyst",
            "utm_source": "arti-opportunity-radar",
            "utm_medium": "agent-skill",
        }
    )
    return f"[用 ARTi 分析 {label}]({base_url}?{query})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", required=True, type=single_line)
    parser.add_argument("--label", required=True, type=single_line)
    parser.add_argument("--title", required=True, type=single_line)
    parser.add_argument("--source-url", required=True, type=http_url)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, type=http_url)
    args = parser.parse_args()
    print(
        build_link(
            symbol=args.symbol,
            label=args.label,
            title=args.title,
            source_url=args.source_url,
            base_url=args.base_url,
        )
    )


if __name__ == "__main__":
    main()
