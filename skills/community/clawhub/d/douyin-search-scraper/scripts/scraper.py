#!/usr/bin/env python3
"""抖音搜索爬虫 - 使用 Playwright + 移动端 UA 解析真实搜索结果"""

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
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
    """Parse Chinese count strings like '1.2万', '3.5亿', '500' to int."""
    if not text:
        return 0
    text = text.strip().replace(",", "").replace(" ", "")
    try:
        if "亿" in text:
            return int(float(text.replace("亿", "")) * 100_000_000)
        if "万" in text:
            return int(float(text.replace("万", "")) * 10_000)
        return int(re.sub(r"[^\d]", "", text) or 0)
    except (ValueError, TypeError):
        return 0


# Mobile UA - Douyin mobile web shows search results without login
_MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


class DouyinScraper:
    """Scrape Douyin search results using mobile web (no login required)."""

    SEARCH_URL = "https://www.douyin.com/search/{keyword}"
    HOT_URL = "https://www.douyin.com/hot"

    def __init__(self, headless: bool = True, delay: float = 2.0, timeout: int = 30000):
        self.headless = headless
        self.delay = delay
        self.timeout = timeout

    def _make_context(self, browser):
        return browser.new_context(
            user_agent=_MOBILE_UA,
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            locale="zh-CN",
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def search(self, keyword: str, limit: int = 10) -> list[VideoData]:
        if sync_playwright is None:
            print("⚠️  playwright 未安装，返回空结果", file=sys.stderr)
            return []

        results: list[VideoData] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            )
            context = self._make_context(browser)
            page = context.new_page()

            url = self.SEARCH_URL.format(keyword=keyword)
            print(f"🔍 搜索: {keyword}", file=sys.stderr)
            print(f"   URL: {url}", file=sys.stderr)

            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            # Wait for card-list to populate
            try:
                page.wait_for_selector(".card-list .card-item", timeout=10000)
            except Exception:
                time.sleep(4)

            time.sleep(self.delay)

            # Scroll to load more
            for _ in range(min(limit // 4, 4)):
                page.evaluate("window.scrollBy(0, 1200)")
                time.sleep(1.5)

            # Parse card items
            cards = page.query_selector_all(".card-list .card-item")
            print(f"   找到 {len(cards)} 个卡片", file=sys.stderr)

            for card in cards:
                if len(results) >= limit:
                    break
                try:
                    video = self._parse_card(card, keyword)
                    if video and video.title:
                        results.append(video)
                except Exception:
                    continue

            browser.close()

        print(f"✅ 获取到 {len(results)} 条结果", file=sys.stderr)
        return results

    def _parse_card(self, card, keyword: str) -> VideoData | None:
        """Parse a .card-item element from Douyin mobile search results."""
        text = card.inner_text().strip()
        if not text or "广告" in text.split("\n")[-1] if text else False:
            # Skip pure ad cards (but keep video ads with content)
            pass

        lines = text.split("\n")
        lines = [l.strip() for l in lines if l.strip()]

        if not lines:
            return None

        # Skip non-video cards: "大家还在搜", "商品·", pure ad cards
        first_line = lines[0]
        if first_line in ("大家还在搜", "查看全部商品") or first_line.startswith("商品"):
            return None
        # Skip cards that are just ads with no real video content
        if "广告" in lines and len(lines) < 5 and not any(re.match(r"\d{4}\.\d", l) for l in lines):
            return None

        # Pattern: author, date, description, stats, possibly ad tag
        author = ""
        publish_time = ""
        description = ""
        stats: list[int] = []

        # First line is usually author name
        author = lines[0]

        # Second line might be date (YYYY.M.DD format) or description
        idx = 1
        if idx < len(lines) and re.match(r"\d{4}\.\d{1,2}\.\d{1,2}", lines[idx]):
            date_str = lines[idx]
            parts = date_str.split(".")
            try:
                publish_time = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
            except (ValueError, IndexError):
                publish_time = date_str
            idx += 1

        # Rest is description + stats
        desc_parts = []
        while idx < len(lines):
            line = lines[idx]
            # Check if line is a number (stat)
            if re.match(r"^[\d,.]+$", line.replace("万", "").replace("亿", "")):
                stats.append(_parse_count(line))
            elif line in ("广告", "团"):
                idx += 1
                # Skip ad-related content after "团" marker
                while idx < len(lines) and not re.match(r"^[\d,.万亿]+$", lines[idx]):
                    idx += 1
                continue
            else:
                desc_parts.append(line)
            idx += 1

        description = " ".join(desc_parts)

        # Extract tags from description
        tags = re.findall(r"#(\S+)", description)
        if keyword not in tags:
            tags.insert(0, keyword)

        # Try to get a link from the card
        link = card.query_selector("a[href]")
        href = ""
        if link:
            href = link.get_attribute("href") or ""
            if href.startswith("/"):
                href = "https://www.douyin.com" + href

        # Map stats: typically [likes, comments, shares] or similar
        like_count = stats[0] if len(stats) > 0 else 0
        comment_count = stats[1] if len(stats) > 1 else 0
        share_count = stats[2] if len(stats) > 2 else 0

        return VideoData(
            title=description[:100] if description else author,
            description=description,
            author=author,
            like_count=like_count,
            comment_count=comment_count,
            share_count=share_count,
            url=href or f"https://www.douyin.com/search/{keyword}",
            tags=tags[:8],
            publish_time=publish_time or date.today().isoformat(),
        )

    # ------------------------------------------------------------------
    # Hot / Trending
    # ------------------------------------------------------------------
    def hot(self, category: str = "", limit: int = 20) -> list[VideoData]:
        if sync_playwright is None:
            print("⚠️  playwright 未安装，返回空结果", file=sys.stderr)
            return []

        results: list[VideoData] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            )
            context = self._make_context(browser)
            page = context.new_page()

            url = self.HOT_URL
            if category:
                url += f"/{category}"
            print(f"🔥 获取热榜: {category or '全部'}", file=sys.stderr)

            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            time.sleep(4)

            # Parse whatever content is available
            items = page.query_selector_all(".card-list .card-item, [class*='hot'] li, [class*='trending'] li")
            for item in items[:limit]:
                try:
                    text = item.inner_text().strip()
                    if text:
                        results.append(VideoData(
                            title=text[:100],
                            url=self.HOT_URL,
                            tags=["热榜", category] if category else ["热榜"],
                            publish_time=date.today().isoformat(),
                        ))
                except Exception:
                    continue

            browser.close()

        print(f"✅ 获取到 {len(results)} 条热榜", file=sys.stderr)
        return results


# ------------------------------------------------------------------
# Output helpers
# ------------------------------------------------------------------
def write_json(items: list[VideoData], output: Path) -> None:
    output.write_text(
        json.dumps([i.to_dict() for i in items], ensure_ascii=False, indent=2),
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


def print_results(items: list[VideoData]) -> None:
    for i, v in enumerate(items, 1):
        likes = f"👍{v.like_count:,}" if v.like_count else ""
        comments = f"💬{v.comment_count:,}" if v.comment_count else ""
        date_str = f"📅{v.publish_time}" if v.publish_time else ""
        print(f"{i}. @{v.author}  {date_str}  {likes}{comments}")
        if v.description:
            print(f"   {v.description[:120]}")
        if v.tags:
            print(f"   #{' #'.join(v.tags)}")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="抖音搜索爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("search", help="搜索关键词")
    sp.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    sp.add_argument("--limit", "-n", type=int, default=10, help="结果数量")
    sp.add_argument("--output", "-o", help="输出文件路径")
    sp.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    sp.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")

    hp = sub.add_parser("hot", help="获取热榜")
    hp.add_argument("--category", "-c", default="", help="分类")
    hp.add_argument("--limit", "-n", type=int, default=20, help="结果数量")
    hp.add_argument("--output", "-o", help="输出文件路径")
    hp.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    hp.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")

    args = parser.parse_args()
    headless = not getattr(args, "no_headless", False)
    scraper = DouyinScraper(headless=headless)

    if args.command == "search":
        items = scraper.search(args.keyword, args.limit)
    else:
        items = scraper.hot(args.category, args.limit)

    print_results(items)

    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(items, output)
        else:
            write_json(items, output)
        print(f"\n💾 已保存到 {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
