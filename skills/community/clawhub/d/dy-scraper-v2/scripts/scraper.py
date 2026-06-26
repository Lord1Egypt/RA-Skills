#!/usr/bin/env python3
"""抖音爆款爬虫 - 使用 Playwright 自动化浏览器爬取抖音搜索结果，失败时降级到 Brave 搜索"""

import argparse
import csv
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None


@dataclass
class VideoData:
    title: str = ""
    description: str = ""
    author: str = ""
    play_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    url: str = ""
    tags: list | None = None
    publish_time: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        data["tags"] = self.tags or []
        return data


def _parse_count(text: str) -> int:
    if not text:
        return 0
    text = text.strip().replace(",", "").replace(" ", "")
    try:
        return int(float(text))
    except ValueError:
        pass
    m = re.match(r"([\d.]+)\s*万", text)
    if m:
        return int(float(m.group(1)) * 10000)
    m = re.match(r"([\d.]+)\s*亿", text)
    if m:
        return int(float(m.group(1)) * 100000000)
    return 0


class DouyinScraper:
    DOUYIN_SEARCH = "https://www.douyin.com/search/"

    def __init__(self, headless: bool = True, delay: float = 2.0, timeout: int = 30000):
        self.headless = headless
        self.delay = delay
        self.timeout = timeout

    def search(self, keyword: str, limit: int) -> list[VideoData]:
        """Try Playwright first, then fall back to web search API."""
        # Try Playwright
        results = self._search_playwright(keyword, limit)
        if results:
            return results

        print("⚠️  Playwright 未获取到数据，尝试 web search fallback...")
        return self._search_web(keyword, limit)

    def _search_playwright(self, keyword: str, limit: int) -> list[VideoData]:
        if sync_playwright is None:
            return []

        results: list[VideoData] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            )
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 900},
                locale="zh-CN",
            )
            page = ctx.new_page()
            try:
                url = f"{self.DOUYIN_SEARCH}{keyword}"
                print(f"🔍 [Playwright] 正在搜索: {keyword}")
                page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
                time.sleep(self.delay + 3)

                # scroll to load
                for _ in range(3):
                    page.evaluate("window.scrollBy(0, 800)")
                    time.sleep(0.8)

                # Try to find video links
                cards = page.query_selector_all("a[href*='/video/']")
                seen = set()
                for card in cards[:limit * 2]:
                    href = card.get_attribute("href") or ""
                    if "/video/" not in href:
                        continue
                    if href.startswith("/"):
                        video_url = f"https://www.douyin.com{href}"
                    else:
                        video_url = href
                    vid = re.search(r"/video/(\d+)", video_url)
                    if not vid or vid.group(1) in seen:
                        continue
                    seen.add(vid.group(1))

                    title = card.inner_text().strip()[:200] or f"抖音视频 {vid.group(1)}"
                    results.append(
                        VideoData(
                            title=title,
                            description="",
                            author="",
                            url=video_url,
                            tags=[keyword],
                            publish_time=date.today().isoformat(),
                        )
                    )
                    if len(results) >= limit:
                        break

            except Exception as exc:
                print(f"⚠️  Playwright 搜索出错: {exc}")
            finally:
                browser.close()

        if results:
            print(f"✅ [Playwright] 获取到 {len(results)} 条结果")
        return results

    def _search_web(self, keyword: str, limit: int) -> list[VideoData]:
        """Use Brave web search API via openclaw's web_search tool (CLI fallback: curl)."""
        results: list[VideoData] = []
        try:
            # Use the openclaw web_search via the gateway API
            import urllib.request
            import urllib.parse

            query = f"site:douyin.com {keyword}"
            # Try using the built-in web search by calling the CLI
            proc = subprocess.run(
                ["curl", "-s", "https://api.search.brave.com/res/v1/web/search",
                 "-H", "Accept: application/json",
                 "-H", f"X-Subscription-Token: {self._get_brave_key()}",
                 "--", f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count={min(limit, 10)}"],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data = json.loads(proc.stdout)
                for item in data.get("web", {}).get("results", [])[:limit]:
                    url = item.get("url", "")
                    if "douyin.com" not in url:
                        continue
                    title = item.get("title", "").strip()
                    desc = item.get("description", "").strip()
                    results.append(
                        VideoData(
                            title=title,
                            description=desc,
                            author="",
                            url=url,
                            tags=[keyword],
                            publish_time=date.today().isoformat(),
                        )
                    )
        except Exception as exc:
            print(f"⚠️  Web search fallback 出错: {exc}")

        if results:
            print(f"✅ [Web Search] 获取到 {len(results)} 条结果")
        else:
            print("⚠️  Web search 也未获取到数据，返回示例数据")
            results = self._mock_search(keyword, limit)

        return results

    def _get_brave_key(self) -> str:
        """Try to read Brave API key from env."""
        import os
        return os.environ.get("BRAVE_API_KEY", "")

    def hot(self, category: str, limit: int) -> list[VideoData]:
        """Hot list - uses web search as primary method."""
        results: list[VideoData] = []
        try:
            import subprocess
            query = f"site:douyin.com 抖音热榜 {category}" if category else "site:douyin.com 抖音热榜"
            proc = subprocess.run(
                ["curl", "-s", f"https://api.search.brave.com/res/v1/web/search?q={query}&count={min(limit, 10)}",
                 "-H", "Accept: application/json",
                 "-H", f"X-Subscription-Token: {self._get_brave_key()}"],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data = json.loads(proc.stdout)
                for item in data.get("web", {}).get("results", [])[:limit]:
                    url = item.get("url", "")
                    title = item.get("title", "").strip()
                    desc = item.get("description", "").strip()
                    results.append(
                        VideoData(
                            title=title,
                            description=desc,
                            author="",
                            url=url,
                            tags=["热榜", category] if category else ["热榜"],
                            publish_time=date.today().isoformat(),
                        )
                    )
        except Exception:
            pass

        if results:
            print(f"✅ 获取到 {len(results)} 条热榜数据")
        else:
            print("⚠️  未获取到数据，返回示例数据")
            results = self._mock_hot(category, limit)

        return results

    def _mock_search(self, keyword: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        return [
            VideoData(
                title=f"{keyword}相关视频 {i + 1}",
                description=f"这是关于{keyword}的示例描述（真实数据暂不可用）",
                author=f"作者{i + 1}",
                play_count=10000 * (i + 1),
                like_count=1000 * (i + 1),
                comment_count=100 * (i + 1),
                share_count=50 * (i + 1),
                url=f"https://www.douyin.com/search/{keyword}",
                tags=[keyword, "热门", "示例数据"],
                publish_time=today,
            )
            for i in range(min(limit, 10))
        ]

    def _mock_hot(self, category: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        label = category or "全部"
        return [
            VideoData(
                title=f"{label}热榜视频 {i + 1}",
                description=f"{label}分类示例热榜数据（真实数据暂不可用）",
                author=f"热门作者{i + 1}",
                play_count=50000 * (i + 1),
                like_count=5000 * (i + 1),
                comment_count=500 * (i + 1),
                share_count=200 * (i + 1),
                url="https://www.douyin.com/hot",
                tags=["热榜", label, "示例数据"],
                publish_time=today,
            )
            for i in range(min(limit, 20))
        ]


def write_json(items: list[VideoData], output: Path) -> None:
    output.write_text(
        json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_csv(items: list[VideoData], output: Path) -> None:
    if not items:
        output.write_text("", encoding="utf-8")
        return
    fieldnames = list(items[0].to_dict().keys())
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = item.to_dict()
            row["tags"] = "|".join(row["tags"])
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音爆款爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="搜索关键词")
    search_p.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    search_p.add_argument("--limit", "-n", type=int, default=10, help="结果数量")
    search_p.add_argument("--output", "-o", help="输出文件路径")
    search_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    search_p.add_argument("--headless", action="store_true", default=True)
    search_p.add_argument("--no-headless", dest="headless", action="store_false")
    search_p.add_argument("--delay", type=float, default=2.0, help="请求间隔(秒)")

    hot_p = sub.add_parser("hot", help="获取热榜")
    hot_p.add_argument("--category", "-c", default="", help="分类")
    hot_p.add_argument("--limit", "-n", type=int, default=20, help="结果数量")
    hot_p.add_argument("--output", "-o", help="输出文件路径")
    hot_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")

    args = parser.parse_args()
    scraper = DouyinScraper(headless=getattr(args, "headless", True), delay=getattr(args, "delay", 2.0))

    if args.command == "search":
        items = scraper.search(args.keyword, args.limit)
    else:
        items = scraper.hot(args.category, args.limit)

    for i, item in enumerate(items, 1):
        print(f"{i}. {item.title} | {item.author} | 👍{item.like_count} | {item.url}")

    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(items, output)
        else:
            write_json(items, output)
        print(f"💾 已保存到: {args.output}")


if __name__ == "__main__":
    main()
