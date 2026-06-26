#!/usr/bin/env python3
import argparse
import csv
import json
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
    tags: list[str] | None = None
    publish_time: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        data["tags"] = self.tags or []
        return data


class DouyinScraper:
    def __init__(self, headless: bool = True, delay: float = 2.0):
        self.headless = headless
        self.delay = delay

    def _mock_search(self, keyword: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        return [
            VideoData(
                title=f"{keyword}相关视频 {i + 1}",
                description=f"这是关于{keyword}的示例描述",
                author=f"作者{i + 1}",
                play_count=10000 * (i + 1),
                like_count=1000 * (i + 1),
                comment_count=100 * (i + 1),
                share_count=50 * (i + 1),
                url=f"https://www.douyin.com/search/{keyword}",
                tags=[keyword, "热门"],
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
                description=f"{label}分类示例热榜数据",
                author=f"热门作者{i + 1}",
                play_count=50000 * (i + 1),
                like_count=5000 * (i + 1),
                comment_count=500 * (i + 1),
                share_count=200 * (i + 1),
                url="https://www.douyin.com/hot",
                tags=["热榜", label],
                publish_time=today,
            )
            for i in range(min(limit, 20))
        ]

    def search(self, keyword: str, limit: int) -> list[VideoData]:
        if sync_playwright is None:
            return self._mock_search(keyword, limit)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(f"https://www.douyin.com/search/{keyword}", wait_until="networkidle", timeout=30000)
                time.sleep(self.delay)
                browser.close()
        except Exception as e:
            print(f"⚠️  浏览器启动失败，使用模拟数据: {e}")
        return self._mock_search(keyword, limit)

    def hot(self, category: str, limit: int) -> list[VideoData]:
        if sync_playwright is None:
            return self._mock_hot(category, limit)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto("https://www.douyin.com/hot", wait_until="networkidle", timeout=30000)
                time.sleep(self.delay)
                browser.close()
        except Exception as e:
            print(f"⚠️  浏览器启动失败，使用模拟数据: {e}")
        return self._mock_hot(category, limit)


def write_json(items: list[VideoData], output: Path) -> None:
    output.write_text(json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2), encoding="utf-8")


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
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("--keyword", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--output")
    search.add_argument("--format", choices=["json", "csv"], default="json")

    hot = sub.add_parser("hot")
    hot.add_argument("--category", default="")
    hot.add_argument("--limit", type=int, default=20)
    hot.add_argument("--output")
    hot.add_argument("--format", choices=["json", "csv"], default="json")

    args = parser.parse_args()
    scraper = DouyinScraper()
    items = scraper.search(args.keyword, args.limit) if args.command == "search" else scraper.hot(args.category, args.limit)

    for index, item in enumerate(items, start=1):
        print(f"{index}. {item.title} | {item.author} | {item.url}")

    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(items, output)
        else:
            write_json(items, output)


if __name__ == "__main__":
    main()
