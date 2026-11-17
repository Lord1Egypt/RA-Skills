#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
# ]
# ///
"""
台灣棒球維基館 (twbsball) 爬蟲工具
使用 Scrapling StealthyFetcher 繞過 Anubis 防護
"""

import argparse
import sys
from scrapling.fetchers import StealthyFetcher, StealthySession


def fetch_page(title: str, wait: int = 10000) -> str:
    """抓取維基館頁面全文，回傳 #mw-content-text 的純文字"""
    url = f"https://twbsball.dils.tku.edu.tw/wiki/index.php?title={title}"
    page = StealthyFetcher.fetch(url, headless=True, wait=wait)
    content = page.css("#mw-content-text")
    if not content:
        print(f"⚠️ 找不到 #mw-content-text，頁面結構可能已變更", file=sys.stderr)
        return ""
    return content[0].get_all_text()


def fetch_pages(titles: list[str], wait: int = 10000) -> dict[str, str]:
    """一次抓取多個頁面（共用同一個 browser 實例）"""
    results = {}
    with StealthySession(headless=True) as session:
        for title in titles:
            url = f"https://twbsball.dils.tku.edu.tw/wiki/index.php?title={title}"
            page = session.fetch(url)
            content = page.css("#mw-content-text")
            results[title] = content[0].get_all_text() if content else ""
    return results


def main():
    parser = argparse.ArgumentParser(description="台灣棒球維基館爬蟲")
    parser.add_argument("title", help="頁面標題，例如: 中華職棒年度最有價值球員")
    parser.add_argument("--wait", type=int, default=10000, help="等待 Anubis PoW 的毫秒數 (default: 10000)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="輸出格式")
    args = parser.parse_args()

    print(f"🔍 正在爬取: {args.title} ...", file=sys.stderr)
    text = fetch_page(args.title, wait=args.wait)

    if args.output == "json":
        import json
        print(json.dumps({"title": args.title, "content": text, "length": len(text)}, ensure_ascii=False))
    else:
        print(text)


if __name__ == "__main__":
    main()
