#!/usr/bin/env python3
"""抖音爆款爬虫 - 使用 Playwright 爬取抖音搜索结果和热榜数据。"""

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


def _parse_count(text: str) -> int:
    """将 '1.2万' '3.5亿' 等中文数字转为整数。"""
    if not text:
        return 0
    text = text.strip().replace(",", "").replace(" ", "")
    try:
        return int(float(text))
    except ValueError:
        pass
    m = re.match(r"([\d.]+)\s*万", text)
    if m:
        return int(float(m.group(1)) * 10_000)
    m = re.match(r"([\d.]+)\s*亿", text)
    if m:
        return int(float(m.group(1)) * 100_000_000)
    m = re.match(r"([\d.]+)\s*w", text, re.I)
    if m:
        return int(float(m.group(1)) * 10_000)
    return 0


class DouyinScraper:
    def __init__(self, headless: bool = True, delay: float = 2.0, cookie_file: str | None = None):
        self.headless = headless
        self.delay = delay
        self.cookie_file = cookie_file

    # ------------------------------------------------------------------
    # Real scraping (Playwright)
    # ------------------------------------------------------------------

    def _launch_browser(self, p):
        launch_opts = dict(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )
        # Try Playwright's bundled chromium first; fall back to system chromium
        try:
            browser = p.chromium.launch(**launch_opts)
        except Exception as e:
            import shutil
            sys_chromium = shutil.which("chromium-browser") or shutil.which("chromium") or shutil.which("google-chrome")
            if sys_chromium:
                print(f"⚠️  Playwright 浏览器未安装，使用系统 Chromium: {sys_chromium}", file=sys.stderr)
                launch_opts["executable_path"] = sys_chromium
                browser = p.chromium.launch(**launch_opts)
            else:
                raise
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        )
        return browser, page

    def _extract_search_results(self, page, keyword: str, limit: int) -> list[VideoData]:
        """从抖音搜索结果页提取视频卡片数据。"""
        videos: list[VideoData] = []

        # 等待搜索结果卡片出现
        try:
            page.wait_for_selector(
                "[class*='video'], [class*='card'], [class*='search-result'], "
                "[data-e2e='search-card'], [class*='feed'], [class*='item']",
                timeout=10000,
            )
        except Exception:
            pass

        # 滚动加载更多
        for _ in range(min(3, (limit // 10) + 1)):
            page.mouse.wheel(0, 1500)
            time.sleep(1)

        # 尝试多种选择器策略
        cards = page.query_selector_all(
            "[data-e2e='search-card'], "
            "[class*='video-card'], "
            "[class*='search-result-card'], "
            "[class*='feed-card'], "
            "[class*='item'][class*='video']"
        )

        # 如果上面没找到，尝试更宽泛的选择器
        if not cards:
            cards = page.query_selector_all(
                "[class*='card'], [class*='item']"
            )

        for card in cards[:limit]:
            try:
                video = VideoData()

                # 标题
                title_el = card.query_selector(
                    "[class*='title'], [class*='desc'], h3, h2, p"
                )
                if title_el:
                    video.title = title_el.inner_text().strip()

                # 作者
                author_el = card.query_selector(
                    "[class*='author'], [class*='name'], [class*='user']"
                )
                if author_el:
                    video.author = author_el.inner_text().strip()

                # 链接
                link_el = card.query_selector("a[href*='video'], a[href*='note']")
                if link_el:
                    href = link_el.get_attribute("href") or ""
                    if href.startswith("/"):
                        href = "https://www.douyin.com" + href
                    video.url = href

                # 互动数据 - 播放/点赞/评论
                stats = card.query_selector_all("[class*='count'], [class*='num'], [class*='stat']")
                stat_values = []
                for s in stats:
                    txt = s.inner_text().strip()
                    if txt:
                        stat_values.append(_parse_count(txt))

                if len(stat_values) >= 1:
                    video.play_count = stat_values[0]
                if len(stat_values) >= 2:
                    video.like_count = stat_values[1]
                if len(stat_values) >= 3:
                    video.comment_count = stat_values[2]
                if len(stat_values) >= 4:
                    video.share_count = stat_values[3]

                # 标签
                tag_els = card.query_selector_all("[class*='tag'], [class*='hash']")
                video.tags = [t.inner_text().strip().lstrip("#") for t in tag_els if t.inner_text().strip()]
                if not video.tags:
                    video.tags = [keyword]

                video.publish_time = date.today().isoformat()
                video.description = video.title  # 抖音搜索结果中 description 通常就是 title

                if video.title:  # 至少要有标题
                    videos.append(video)
            except Exception:
                continue

        return videos

    def _extract_hot_results(self, page, category: str, limit: int) -> list[VideoData]:
        """从抖音热榜页提取数据。"""
        videos: list[VideoData] = []

        try:
            page.wait_for_selector(
                "[class*='hot'], [class*='rank'], [class*='trending'], "
                "[data-e2e='hot-card']",
                timeout=10000,
            )
        except Exception:
            pass

        items = page.query_selector_all(
            "[data-e2e='hot-card'], "
            "[class*='hot-item'], "
            "[class*='rank-item'], "
            "[class*='trending-item']"
        )

        if not items:
            items = page.query_selector_all("[class*='item'], [class*='card']")

        for item in items[:limit]:
            try:
                video = VideoData()
                title_el = item.query_selector("[class*='title'], [class*='desc'], h3, p")
                if title_el:
                    video.title = title_el.inner_text().strip()

                author_el = item.query_selector("[class*='author'], [class*='name']")
                if author_el:
                    video.author = author_el.inner_text().strip()

                hot_val_el = item.query_selector("[class*='hot-value'], [class*='heat'], [class*='count']")
                if hot_val_el:
                    video.play_count = _parse_count(hot_val_el.inner_text())

                video.tags = ["热榜", category] if category else ["热榜"]
                video.publish_time = date.today().isoformat()
                video.url = "https://www.douyin.com/hot"

                if video.title:
                    videos.append(video)
            except Exception:
                continue

        return videos

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def _detect_captcha(self, page) -> bool:
        """检测是否被验证码拦截。"""
        title = page.title()
        if '验证码' in title or 'captcha' in title.lower():
            return True
        if page.query_selector('[class*="captcha"], [class*="verify"], [class*="slider"]'):
            return True
        return False

    def search(self, keyword: str, limit: int = 10) -> list[VideoData]:
        if sync_playwright is None:
            print("⚠️  Playwright 未安装，返回模拟数据", file=sys.stderr)
            return self._mock_search(keyword, limit)

        with sync_playwright() as p:
            browser, page = self._launch_browser(p)
            try:
                # Load cookies if available
                if self.cookie_file and Path(self.cookie_file).exists():
                    cookies = json.loads(Path(self.cookie_file).read_text())
                    browser_context = page.context
                    browser_context.add_cookies(cookies)

                url = f"https://www.douyin.com/search/{keyword}"
                print(f"🔍 正在搜索: {keyword}", file=sys.stderr)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(self.delay + 1)  # extra wait for captcha page to render

                if self._detect_captcha(page):
                    print("⚠️  抖音要求验证码，无法自动绕过。", file=sys.stderr)
                    print("   提示：可通过以下方式获取真实数据：", file=sys.stderr)
                    print("   1. 使用 --cookie-file 参数传入浏览器 cookie", file=sys.stderr)
                    print("   2. 通过 OpenClaw browser 工具在已登录浏览器中操作", file=sys.stderr)
                    print("   当前返回模拟数据供参考", file=sys.stderr)
                    return self._mock_search(keyword, limit)

                videos = self._extract_search_results(page, keyword, limit)
                if not videos:
                    print("⚠️  未能提取到页面数据，返回模拟数据", file=sys.stderr)
                    return self._mock_search(keyword, limit)
                print(f"✅ 已获取 {len(videos)} 条视频数据", file=sys.stderr)
                return videos
            finally:
                browser.close()

    def hot(self, category: str = "", limit: int = 20) -> list[VideoData]:
        if sync_playwright is None:
            print("⚠️  Playwright 未安装，返回模拟数据", file=sys.stderr)
            return self._mock_hot(category, limit)

        with sync_playwright() as p:
            browser, page = self._launch_browser(p)
            try:
                if self.cookie_file and Path(self.cookie_file).exists():
                    cookies = json.loads(Path(self.cookie_file).read_text())
                    page.context.add_cookies(cookies)

                url = f"https://www.douyin.com/hot/{category}" if category else "https://www.douyin.com/hot"
                print(f"🔥 正在获取热榜: {category or '全部'}", file=sys.stderr)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(self.delay)

                if self._detect_captcha(page):
                    print("⚠️  抖音要求验证码，返回模拟数据", file=sys.stderr)
                    return self._mock_hot(category, limit)

                videos = self._extract_hot_results(page, category, limit)
                if not videos:
                    print("⚠️  未能提取到页面数据，返回模拟数据", file=sys.stderr)
                    return self._mock_hot(category, limit)
                print(f"✅ 已获取 {len(videos)} 条热榜数据", file=sys.stderr)
                return videos
            finally:
                browser.close()

    # ------------------------------------------------------------------
    # Fallback mock
    # ------------------------------------------------------------------

    def _mock_search(self, keyword: str, limit: int) -> list[VideoData]:
        today = date.today().isoformat()
        return [
            VideoData(
                title=f"{keyword}相关视频 {i + 1}",
                description=f"这是关于{keyword}的示例描述（模拟数据）",
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
                description=f"{label}分类示例热榜数据（模拟数据）",
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


# ------------------------------------------------------------------
# Output helpers
# ------------------------------------------------------------------

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


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="抖音爆款爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="搜索关键词")
    search_p.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    search_p.add_argument("--limit", "-n", type=int, default=10, help="返回数量")
    search_p.add_argument("--output", "-o", help="输出文件路径")
    search_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")

    hot_p = sub.add_parser("hot", help="获取热榜")
    hot_p.add_argument("--category", "-c", default="", help="分类")
    hot_p.add_argument("--limit", "-n", type=int, default=20, help="返回数量")
    hot_p.add_argument("--output", "-o", help="输出文件路径")
    hot_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")

    args = parser.parse_args()
    scraper = DouyinScraper()

    if args.command == "search":
        items = scraper.search(args.keyword, args.limit)
    else:
        items = scraper.hot(args.category, args.limit)

    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item.title} | {item.author} | ▶{item.play_count} 👍{item.like_count} | {item.url}")

    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(items, output)
        else:
            write_json(items, output)
        print(f"\n💾 已保存到: {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
