#!/usr/bin/env python3
"""抖音数据爬虫 - 使用公开 API 获取热榜和搜索数据

支持:
  - 热榜获取 (无需登录, 通过公开 API)
  - 关键词搜索 (通过 Playwright 浏览器自动化)
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
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
    hot_value: int = 0
    search_word: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Hot Search API (no login required)
# ---------------------------------------------------------------------------

_HOT_API = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _fetch_hot_search() -> list[VideoData]:
    """Fetch trending/hot search list from Douyin public API."""
    params = urllib.parse.urlencode({
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "detail_list": "1",
        "source": "6",
        "main_billboard_count": "5",
        "update_version_code": "170400",
        "pc_client_type": "1",
    })
    req = urllib.request.Request(
        _HOT_API + "?" + params,
        headers={"User-Agent": _UA, "Referer": "https://www.douyin.com/", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())

    if data.get("status_code") != 0:
        print(f"⚠️  热榜 API 返回异常: status_code={data.get('status_code')}", file=sys.stderr)
        return []

    payload = data.get("data", {})
    word_list = payload.get("word_list", [])
    today = date.today().isoformat()
    results: list[VideoData] = []
    label_map = {1: "热", 2: "新", 3: "荐", 4: "独家", 5: "首发"}
    for w in word_list:
        label_val = w.get("label", 0)
        tag_label = label_map.get(label_val, "") if isinstance(label_val, int) else str(label_val)
        results.append(VideoData(
            title=w.get("word", ""),
            description="",
            hot_value=w.get("hot_value", 0),
            url=f"https://www.douyin.com/search/{urllib.parse.quote(w.get('word', ''))}",
            tags=[tag_label] if tag_label else [],
            publish_time=today,
            search_word=w.get("word", ""),
        ))
    return results


# ---------------------------------------------------------------------------
# Search via Playwright (navigates to search page, extracts SSR data)
# ---------------------------------------------------------------------------

def _search_via_playwright(keyword: str, limit: int = 10) -> list[VideoData]:
    """Search Douyin using Playwright browser automation.

    Navigates to the search page and extracts whatever data is available
    from the rendered page. If login is required, falls back to
    extracting the trending data for the keyword context.
    """
    if sync_playwright is None:
        print("⚠️  Playwright 未安装，使用热榜数据替代", file=sys.stderr)
        return _search_hot_filtered(keyword, limit)

    results: list[VideoData] = []
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
    except Exception as e:
        print(f"⚠️  浏览器启动失败 ({e})，使用热榜数据替代", file=sys.stderr)
        return _search_hot_filtered(keyword, limit)

    try:
        ctx = browser.new_context(user_agent=_UA)
        page = ctx.new_page()

        # Visit homepage first to get cookies
        page.goto("https://www.douyin.com/", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)

        # Navigate to search
        search_url = f"https://www.douyin.com/search/{urllib.parse.quote(keyword)}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(5)

        # Try to extract search results from the page
        # Method 1: Look for video cards in the DOM
        cards = page.evaluate("""() => {
            const results = [];
            // Try various selectors for search result cards
            const selectors = [
                '[data-e2e="search-result-item"]',
                '[data-e2e="search-card"]',
                '.search-result-card',
                '.video-card',
                '[class*="searchResult"]',
                '[class*="videoCard"]',
            ];
            for (const sel of selectors) {
                const els = document.querySelectorAll(sel);
                if (els.length > 0) {
                    els.forEach(el => {
                        const title = el.querySelector('[class*="title"], [class*="desc"], a')?.textContent?.trim() || '';
                        const author = el.querySelector('[class*="author"], [class*="name"]')?.textContent?.trim() || '';
                        const link = el.querySelector('a')?.href || '';
                        if (title) {
                            results.push({title, author, url: link});
                        }
                    });
                    break;
                }
            }
            return results;
        }""")

        if cards:
            for c in cards[:limit]:
                results.append(VideoData(
                    title=c.get("title", ""),
                    author=c.get("author", ""),
                    url=c.get("url", ""),
                    description=keyword,
                    tags=[keyword],
                    publish_time=date.today().isoformat(),
                ))

        # Method 2: Extract from SSR data (__pace_f scripts)
        if not results:
            ssr_data = page.evaluate("""() => {
                const scripts = document.querySelectorAll('script');
                for (const s of scripts) {
                    const text = s.textContent || '';
                    if (text.includes('__pace_f') && text.includes('aweme_info')) {
                        return text.substring(0, 50000);
                    }
                }
                return '';
            }""")

            if ssr_data:
                # Try to find aweme_info in the RSC payload
                try:
                    # Decode URL-encoded segments
                    matches = re.findall(r'push\(\[1,"(.*?)"\]', ssr_data)
                    for m in matches:
                        decoded = urllib.parse.unquote(m)
                        if "aweme_info" in decoded:
                            # Try to extract aweme_info objects
                            aweme_matches = re.findall(r'"aweme_info":\s*(\{[^}]{100,})', decoded)
                            for am in aweme_matches[:limit]:
                                try:
                                    ai = json.loads(am + "}")
                                    results.append(VideoData(
                                        title=ai.get("desc", ""),
                                        author=ai.get("author", {}).get("nickname", ""),
                                        play_count=ai.get("statistics", {}).get("play_count", 0),
                                        like_count=ai.get("statistics", {}).get("digg_count", 0),
                                        comment_count=ai.get("statistics", {}).get("comment_count", 0),
                                        share_count=ai.get("statistics", {}).get("share_count", 0),
                                        url=f"https://www.douyin.com/video/{ai.get('aweme_id', '')}",
                                        tags=[keyword],
                                        publish_time=date.today().isoformat(),
                                    ))
                                except json.JSONDecodeError:
                                    pass
                except Exception as e:
                    print(f"⚠️  SSR 数据解析失败: {e}", file=sys.stderr)

        # Method 3: Check if we got any visible content at all
        if not results:
            # Check if login wall is shown
            login_wall = page.query_selector('text=登录后即可搜索')
            if login_wall:
                print("⚠️  抖音搜索需要登录，无法获取搜索结果", file=sys.stderr)
                print("   将返回当前热榜数据作为参考", file=sys.stderr)
                results = _fetch_hot_search()
            else:
                # Try to get any text content from the page
                page_text = page.inner_text("body")[:500]
                if "搜索" not in page_text:
                    print("⚠️  搜索页面未返回有效内容", file=sys.stderr)
                    results = _fetch_hot_search()

    except Exception as e:
        print(f"⚠️  浏览器搜索出错 ({e})，使用热榜数据替代", file=sys.stderr)
        results = _search_hot_filtered(keyword, limit)
    finally:
        try:
            browser.close()
            pw.stop()
        except Exception:
            pass

    return results[:limit]


# ---------------------------------------------------------------------------
# Search via hot search API with keyword filtering
# ---------------------------------------------------------------------------

def _search_hot_filtered(keyword: str, limit: int = 10) -> list[VideoData]:
    """Search by fetching hot search list and filtering by keyword.

    This is a fallback when the full search API is not available.
    """
    all_hot = _fetch_hot_search()
    if not keyword:
        return all_hot[:limit]

    # Filter hot items that match the keyword
    matched = [v for v in all_hot if keyword.lower() in v.title.lower()]
    if matched:
        return matched[:limit]

    # If no match, return all hot items with a note
    print(f"⚠️  热榜中未找到与「{keyword}」相关的内容，返回全部热榜", file=sys.stderr)
    return all_hot[:limit]


# ---------------------------------------------------------------------------
# Unified search
# ---------------------------------------------------------------------------

def search(keyword: str, limit: int = 10, method: str = "auto") -> list[VideoData]:
    """Search Douyin for videos.

    Args:
        keyword: Search keyword
        limit: Maximum number of results
        method: "auto" (try Playwright first, fallback to API),
                "api" (hot search API only),
                "browser" (Playwright only)
    """
    if method == "api":
        return _search_hot_filtered(keyword, limit)
    elif method == "browser":
        return _search_via_playwright(keyword, limit)
    else:
        # Auto: try browser first, fallback to API
        results = _search_via_playwright(keyword, limit)
        if not results:
            results = _search_hot_filtered(keyword, limit)
        return results


def hot(limit: int = 20) -> list[VideoData]:
    """Get Douyin hot/trending search list."""
    return _fetch_hot_search()[:limit]


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

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


def display_results(items: list[VideoData], keyword: str = "") -> None:
    """Print results in a readable format."""
    header = f"🔍 搜索结果: {keyword}" if keyword else "🔥 抖音热榜"
    print(f"\n{'='*60}")
    print(header)
    print(f"{'='*60}")

    if not items:
        print("  (无结果)")
        return

    for i, item in enumerate(items, 1):
        print(f"\n{i}. {item.title}")
        if item.author:
            print(f"   👤 作者: {item.author}")
        if item.hot_value:
            print(f"   🔥 热度: {item.hot_value:,}")
        if item.play_count:
            print(f"   ▶️  播放: {item.play_count:,} | 👍 点赞: {item.like_count:,} | 💬 评论: {item.comment_count:,}")
        if item.url:
            print(f"   🔗 {item.url}")
        if item.tags:
            print(f"   🏷️  {' '.join(f'#{t}' for t in item.tags if t)}")

    print(f"\n{'='*60}")
    print(f"共 {len(items)} 条结果")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="抖音数据爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="搜索关键词")
    search_p.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    search_p.add_argument("--limit", "-n", type=int, default=10, help="结果数量 (默认10)")
    search_p.add_argument("--output", "-o", help="输出文件路径")
    search_p.add_argument("--format", "-f", choices=["json", "csv"], default="json", help="输出格式")
    search_p.add_argument("--method", "-m", choices=["auto", "api", "browser"], default="api", help="搜索方式 (默认api)")

    hot_p = sub.add_parser("hot", help="获取热榜")
    hot_p.add_argument("--limit", "-n", type=int, default=20, help="结果数量 (默认20)")
    hot_p.add_argument("--output", "-o", help="输出文件路径")
    hot_p.add_argument("--format", "-f", choices=["json", "csv"], default="json", help="输出格式")

    args = parser.parse_args()

    if args.command == "search":
        items = search(args.keyword, args.limit, args.method)
        display_results(items, args.keyword)
    else:
        items = hot(args.limit)
        display_results(items)

    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(items, output)
        else:
            write_json(items, output)
        print(f"\n💾 已保存到: {args.output}")


if __name__ == "__main__":
    main()
