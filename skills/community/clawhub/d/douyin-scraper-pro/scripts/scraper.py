#!/usr/bin/env python3
"""抖音爆款爬虫 - Python 版本，使用 Playwright 移动端提取真实数据"""

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
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
    tags: list = field(default_factory=list)
    publish_time: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _parse_count(text: str) -> int:
    """Parse Chinese count strings like '1.2万' or '3.5亿' to int."""
    if not text:
        return 0
    text = text.strip().replace(",", "")
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
    nums = re.findall(r"\d+", text)
    if nums:
        return int(nums[0])
    return 0


MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)


class DouyinScraper:
    def __init__(self, headless: bool = True, delay: float = 2.0):
        self.headless = headless
        self.delay = delay

    def _launch_browser(self, p):
        browser = p.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )
        context = browser.new_context(
            user_agent=MOBILE_UA,
            viewport={"width": 390, "height": 844},
            locale="zh-CN",
            is_mobile=True,
        )
        page = context.new_page()
        return browser, page

    def _extract_search_results(self, page, keyword: str, limit: int) -> list:
        """Extract video data from Douyin mobile search page."""
        videos = []
        try:
            page.wait_for_selector('[class*="h5-video-card"], [class*="video-card"]', timeout=15000)
            time.sleep(self.delay)
        except Exception:
            pass

        # Scroll to load more results
        scrolls = max(1, limit // 5)
        for i in range(scrolls):
            page.evaluate(f"window.scrollTo(0, {(i + 1) * 800})")
            time.sleep(1.5)

        cards = page.query_selector_all('[class*="h5-video-card"]')
        if not cards:
            cards = page.query_selector_all('[class*="video-card"]')

        for card in cards[:limit]:
            try:
                text = card.inner_text()
                lines = [l.strip() for l in text.split("\n") if l.strip()]

                # Skip ads (contain '广告')
                if any("广告" in l for l in lines):
                    continue

                video = VideoData()
                video.tags = []

                # Get link
                link = card.query_selector('a[href*="/video/"]')
                href = ""
                if link:
                    href = link.get_attribute("href") or ""
                    if href.startswith("/"):
                        href = "https://www.douyin.com" + href

                # Parse lines: author, date, title, then stats
                author = lines[0] if len(lines) > 0 else ""
                date_str = lines[1] if len(lines) > 1 else ""
                title = lines[2] if len(lines) > 2 else ""

                # Extract tags from title
                tags = re.findall(r"#(\S+)", title)

                # Stats are the remaining numeric lines
                stat_lines = lines[3:] if len(lines) > 3 else []
                stats = []
                for s in stat_lines:
                    s = s.strip()
                    if re.match(r"^[\d.]+万?$", s):
                        val = s.replace("万", "")
                        try:
                            stats.append(int(float(val) * 10000) if "万" in s else int(float(val)))
                        except ValueError:
                            pass

                video.title = title
                video.description = title
                video.author = author
                video.publish_time = date_str
                video.url = href
                video.tags = tags
                if len(stats) >= 1:
                    video.like_count = stats[0]
                if len(stats) >= 2:
                    video.comment_count = stats[1]
                if len(stats) >= 3:
                    video.play_count = stats[2]
                if len(stats) >= 4:
                    video.share_count = stats[3]

                if not video.title:
                    continue

                videos.append(video)
            except Exception:
                continue

        return videos

    def _extract_hot_results(self, page, limit: int) -> list:
        """Extract hot/trending data from Douyin hot page."""
        videos = []
        try:
            page.wait_for_selector('[class*="hot"], [class*="trending"]', timeout=15000)
            time.sleep(self.delay)
        except Exception:
            pass

        for i in range(3):
            page.evaluate(f"window.scrollTo(0, {(i + 1) * 800})")
            time.sleep(1.5)

        cards = page.query_selector_all('[class*="h5-video-card"]')
        if not cards:
            cards = page.query_selector_all('[class*="hot-item"], [class*="trending-item"]')

        for card in cards[:limit]:
            try:
                text = card.inner_text()
                lines = [l.strip() for l in text.split("\n") if l.strip()]
                if any("广告" in l for l in lines):
                    continue

                video = VideoData()
                video.tags = ["热榜"]

                link = card.query_selector('a[href*="/video/"]')
                href = ""
                if link:
                    href = link.get_attribute("href") or ""
                    if href.startswith("/"):
                        href = "https://www.douyin.com" + href

                video.title = lines[2] if len(lines) > 2 else (lines[0] if lines else "")
                video.author = lines[0] if len(lines) > 0 else ""
                video.url = href
                video.publish_time = date.today().isoformat()

                if video.title:
                    videos.append(video)
            except Exception:
                continue

        return videos

    def _extract_video_detail(self, page, url: str) -> VideoData:
        """Extract details from a single video page."""
        video = VideoData(url=url, tags=[])
        try:
            page.wait_for_selector('[class*="desc"], [class*="detail"]', timeout=15000)
            time.sleep(self.delay)
        except Exception:
            pass

        try:
            desc_el = page.query_selector('[class*="desc"], [class*="caption"], [class*="title"]')
            if desc_el:
                text = desc_el.inner_text().strip()
                video.title = text[:100]
                video.description = text
                tags = re.findall(r"#(\S+)", text)
                video.tags = tags
        except Exception:
            pass

        try:
            author_el = page.query_selector('[class*="author"], [class*="nickname"]')
            if author_el:
                video.author = author_el.inner_text().strip()
        except Exception:
            pass

        video.publish_time = date.today().isoformat()
        return video

    def search(self, keyword: str, limit: int) -> list:
        if sync_playwright is None:
            print("⚠️  Playwright 未安装，请运行: pip install playwright && playwright install chromium", file=sys.stderr)
            return []

        with sync_playwright() as p:
            browser, page = self._launch_browser(p)
            try:
                search_url = f"https://www.douyin.com/search/{keyword}"
                print(f"🔍 搜索: {keyword}", file=sys.stderr)
                page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                videos = self._extract_search_results(page, keyword, limit)
                print(f"✅ 获取到 {len(videos)} 条结果", file=sys.stderr)
                return videos
            except Exception as e:
                print(f"⚠️  搜索出错: {e}", file=sys.stderr)
                return []
            finally:
                browser.close()

    def hot(self, category: str, limit: int) -> list:
        if sync_playwright is None:
            print("⚠️  Playwright 未安装", file=sys.stderr)
            return []

        with sync_playwright() as p:
            browser, page = self._launch_browser(p)
            try:
                url = "https://www.douyin.com/hot"
                if category:
                    url += f"/{category}"
                print(f"🔥 获取热榜", file=sys.stderr)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                videos = self._extract_hot_results(page, limit)
                print(f"✅ 获取到 {len(videos)} 条热榜数据", file=sys.stderr)
                return videos
            except Exception as e:
                print(f"⚠️  获取热榜出错: {e}", file=sys.stderr)
                return []
            finally:
                browser.close()

    def analyze(self, url: str) -> VideoData:
        if sync_playwright is None:
            print("⚠️  Playwright 未安装", file=sys.stderr)
            return VideoData(url=url)

        with sync_playwright() as p:
            browser, page = self._launch_browser(p)
            try:
                print(f"🎬 分析视频: {url}", file=sys.stderr)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                video = self._extract_video_detail(page, url)
                print(f"✅ 分析完成", file=sys.stderr)
                return video
            except Exception as e:
                print(f"⚠️  分析出错: {e}", file=sys.stderr)
                return VideoData(url=url)
            finally:
                browser.close()


def write_json(items, output: Path) -> None:
    data = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(items, output: Path) -> None:
    if not items:
        output.write_text("", encoding="utf-8")
        return
    dicts = [item.to_dict() if hasattr(item, "to_dict") else item for item in items]
    fieldnames = list(dicts[0].keys())
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in dicts:
            row = dict(d)
            row["tags"] = "|".join(row.get("tags", []))
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音爆款爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="搜索关键词")
    search_p.add_argument("--keyword", required=True, help="搜索关键词")
    search_p.add_argument("--limit", type=int, default=10, help="结果数量")
    search_p.add_argument("--output", help="输出文件路径")
    search_p.add_argument("--format", choices=["json", "csv"], default="json")

    hot_p = sub.add_parser("hot", help="获取热榜")
    hot_p.add_argument("--category", default="", help="分类")
    hot_p.add_argument("--limit", type=int, default=20, help="结果数量")
    hot_p.add_argument("--output", help="输出文件路径")
    hot_p.add_argument("--format", choices=["json", "csv"], default="json")

    analyze_p = sub.add_parser("analyze", help="分析视频链接")
    analyze_p.add_argument("--url", required=True, help="视频链接")
    analyze_p.add_argument("--output", help="输出文件路径")
    analyze_p.add_argument("--format", choices=["json", "csv"], default="json")

    args = parser.parse_args()
    scraper = DouyinScraper()

    if args.command == "search":
        items = scraper.search(args.keyword, args.limit)
        print(json.dumps([v.to_dict() for v in items], ensure_ascii=False, indent=2))
        if args.output and items:
            if args.format == "json":
                write_json(items, Path(args.output))
            else:
                write_csv(items, Path(args.output))

    elif args.command == "hot":
        items = scraper.hot(args.category, args.limit)
        print(json.dumps([v.to_dict() for v in items], ensure_ascii=False, indent=2))
        if args.output and items:
            if args.format == "json":
                write_json(items, Path(args.output))
            else:
                write_csv(items, Path(args.output))

    elif args.command == "analyze":
        video = scraper.analyze(args.url)
        print(json.dumps(video.to_dict(), ensure_ascii=False, indent=2))
        if args.output:
            if args.format == "json":
                write_json([video], Path(args.output))
            else:
                write_csv([video], Path(args.output))


if __name__ == "__main__":
    main()
