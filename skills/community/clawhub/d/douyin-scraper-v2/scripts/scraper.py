#!/usr/bin/env python3
"""
抖音爆款爬虫 v2.0 - Python 版本
使用抖音 Web API 获取热榜和搜索建议 (无需登录)
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from dataclasses import asdict, dataclass, field
from pathlib import Path

COMMON_PARAMS = {
    "aid": "6383",
    "device_platform": "webapp",
    "channel": "channel_pc_web",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.douyin.com/",
    "Accept": "application/json, text/plain, */*",
}


def _api_get(endpoint: str, extra: dict | None = None) -> dict:
    params = {**COMMON_PARAMS, **(extra or {})}
    qs = urllib.parse.urlencode(params)
    url = f"https://www.douyin.com/aweme/v1/web{endpoint}?{qs}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fmt(n: int) -> str:
    if n >= 100_000_000:
        return f"{n / 100_000_000:.1f}亿"
    if n >= 10_000:
        return f"{n / 10_000:.1f}万"
    return str(n)


@dataclass
class HotItem:
    rank: int = 0
    word: str = ""
    hot_value: int = 0
    video_count: int = 0
    group_id: str = ""
    sentence_id: str = ""
    cover: str = ""


@dataclass
class SuggestItem:
    word: str = ""
    group_id: str = ""


@dataclass
class SearchResult:
    keyword: str = ""
    matched_hot: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    hot_list: list = field(default_factory=list)
    note: str = ""


class DouyinAPI:
    def get_hot_search(self, limit: int = 50) -> list[HotItem]:
        data = _api_get("/hot/search/list/", {"detail_list": "1", "source": "6"})
        if data.get("status_code") != 0:
            raise RuntimeError(f"热榜API错误: {data.get('status_msg', 'unknown')}")
        word_list = data.get("data", {}).get("word_list", [])
        return [
            HotItem(
                rank=i + 1,
                word=w.get("word", ""),
                hot_value=w.get("hot_value", 0),
                video_count=w.get("video_count", 0),
                group_id=w.get("group_id", ""),
                sentence_id=w.get("sentence_id", ""),
                cover=(w.get("word_cover") or {}).get("url_list", [""])[0],
            )
            for i, w in enumerate(word_list[:limit])
        ]

    def get_suggestions(self, keyword: str, limit: int = 10) -> list[SuggestItem]:
        data = _api_get("/search/sug/", {"keyword": keyword, "count": str(limit)})
        sug_list = data.get("sug_list", [])
        return [
            SuggestItem(
                word=(s.get("word_record") or {}).get("words_content", s.get("content", "")),
                group_id=(s.get("word_record") or {}).get("group_id", ""),
            )
            for s in sug_list[:limit]
        ]

    def search(self, keyword: str, limit: int = 20) -> SearchResult:
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            hot_f = pool.submit(self.get_hot_search, 50)
            sug_f = pool.submit(self.get_suggestions, keyword, 20)
            hot_list = hot_f.result()
            suggestions = sug_f.result()

        matched = [h for h in hot_list if keyword in h.word or h.word in keyword]
        related = [s for s in suggestions if keyword in s.word or s.word in keyword]

        if matched:
            note = f"在热榜中找到 {len(matched)} 个匹配话题"
        elif related:
            note = f"热榜无直接匹配，但找到 {len(related)} 个相关搜索建议"
        else:
            note = "未找到匹配结果，返回当前热榜供参考"

        return SearchResult(
            keyword=keyword,
            matched_hot=[asdict(m) for m in matched],
            suggestions=[asdict(s) for s in related],
            hot_list=[asdict(h) for h in hot_list],
            note=note,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音爆款爬虫 v2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    p_hot = sub.add_parser("hot", help="获取热榜")
    p_hot.add_argument("--limit", type=int, default=50)
    p_hot.add_argument("--output")
    p_hot.add_argument("--format", choices=["json", "csv"], default="json")

    p_sug = sub.add_parser("suggest", help="获取搜索建议")
    p_sug.add_argument("--keyword", required=True)
    p_sug.add_argument("--limit", type=int, default=10)
    p_sug.add_argument("--output")

    p_search = sub.add_parser("search", help="搜索 (热榜匹配+搜索建议)")
    p_search.add_argument("--keyword", required=True)
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--output")
    p_search.add_argument("--format", choices=["json", "csv"], default="json")

    args = parser.parse_args()
    api = DouyinAPI()

    if args.command == "hot":
        print("🔥 正在获取抖音热榜...")
        items = api.get_hot_search(args.limit)
        print("\n🔥 抖音热榜")
        print("─" * 50)
        for item in items:
            print(f"  {item.rank:>2}. {item.word}  🔥{fmt(item.hot_value)}  🎬{item.video_count}个视频")
        if args.output:
            Path(args.output).write_text(
                json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"\n💾 已保存到: {args.output}")

    elif args.command == "suggest":
        print(f"💡 正在获取搜索建议: {args.keyword}")
        items = api.get_suggestions(args.keyword, args.limit)
        print("\n💡 搜索建议:")
        for s in items:
            print(f"  • {s.word}")
        if args.output:
            Path(args.output).write_text(
                json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2), encoding="utf-8"
            )

    elif args.command == "search":
        print(f"🔍 正在搜索: {args.keyword}")
        result = api.search(args.keyword, args.limit)
        print(f"\n🔍 搜索: {result.keyword}")
        print(f"   {result.note}")
        if result.matched_hot:
            print("\n🎯 热榜匹配:")
            for item in result.matched_hot:
                print(f"  • {item['word']}  🔥{fmt(item['hot_value'])}  🎬{item['video_count']}个视频")
        if result.suggestions:
            print("\n💡 相关搜索:")
            for s in result.suggestions:
                print(f"  • {s['word']}")
        if not result.matched_hot and not result.suggestions:
            print("\n📋 当前热榜:")
            for item in result.hot_list[:10]:
                print(f"  {item['rank']:>2}. {item['word']}  🔥{fmt(item['hot_value'])}")
        if args.output:
            Path(args.output).write_text(
                json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"\n💾 已保存到: {args.output}")


if __name__ == "__main__":
    main()
