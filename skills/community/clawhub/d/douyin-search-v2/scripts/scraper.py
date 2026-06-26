#!/usr/bin/env python3
"""抖音搜索爬虫 - 使用 Playwright 爬取抖音搜索结果和热榜数据。

支持:
  - 关键词搜索视频 (移动端页面渲染)
  - 获取热榜 (公开 API)
  - JSON / CSV 输出
  - 自然语言查询 (自动提取关键词)
"""

import argparse
import csv
import json
import re
import sys
import time
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

    def to_dict(self) -> dict:
        data = asdict(self)
        data["tags"] = self.tags or []
        return data


# ---------------------------------------------------------------------------
# Natural-language keyword extraction
# ---------------------------------------------------------------------------

NL_PATTERNS = [
    # "搜索一下海鲜视频" → "海鲜"
    re.compile(r"(?:搜索|搜一下|搜搜|找|查找|查一下|看看).{0,4}?([^\s,，。！？]{1,20})(?:视频|内容|帖子|文案|直播)?(?:的?相关|的?内容)?$"),
    # "帮我搜海鲜" → "海鲜"
    re.compile(r"(?:帮我|给我|想|要).{0,2}(?:搜|找|看|查)(?:一下|一搜|一找)?(.{1,20})"),
    # "海鲜视频" → "海鲜"
    re.compile(r"^([^\s,，。！？]{1,20})(?:视频|内容|帖子|文案|直播)$"),
    # fallback: just use the whole query
    re.compile(r"^(.+)$"),
]

STOP_WORDS = {"一下", "一些", "相关", "视频", "内容", "帖子", "文案", "直播", "的", "了", "吗", "吧", "呢", "帮", "我", "给", "想", "要", "搜", "找", "看", "查", "搜索", "看看"}


def extract_keyword(query: str) -> str:
    """Extract a search keyword from a natural-language query."""
    q = query.strip()
    for pat in NL_PATTERNS:
        m = pat.search(q)
        if m:
            kw = m.group(1).strip()
            # Remove stop words from edges
            for w in sorted(STOP_WORDS, key=len, reverse=True):
                if kw.startswith(w):
                    kw = kw[len(w):]
                if kw.endswith(w):
                    kw = kw[:-len(w)]
            if kw:
                return kw
    return q


# ---------------------------------------------------------------------------
# Hot search API (no auth required)
# ---------------------------------------------------------------------------

def fetch_hot_search(limit: int = 20) -> list[VideoData]:
    """Fetch hot search words from Douyin's public API."""
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"⚠️  热榜 API 请求失败: {e}", file=sys.stderr)
        return []

    word_list = data.get("data", {}).get("word_list", [])
    results = []
    today = date.today().isoformat()
    for i, w in enumerate(word_list[:limit]):
        results.append(VideoData(
            title=w.get("word", ""),
            description=w.get("sentence_tag", ""),
            author="",
            play_count=w.get("hot_value", 0),
            like_count=0,
            comment_count=0,
            share_count=0,
            url=f"https://www.douyin.com/search/{urllib.request.quote(w.get('word', ''))}",
            tags=["热榜"],
            publish_time=today,
        ))
    return results


# ---------------------------------------------------------------------------
# Playwright-based search (mobile web)
# ---------------------------------------------------------------------------

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


def search_videos(keyword: str, limit: int = 10, headless: bool = True, delay: float = 2.0) -> list[VideoData]:
    """Search Douyin videos using Playwright with mobile user-agent.

    The mobile web version renders search results without login (though
    with a captcha gate on some requests).  We extract visible result
    cards from the rendered page.
    """
    if sync_playwright is None:
        print("⚠️  Playwright 未安装，返回空结果。请运行: pip install playwright && playwright install chromium", file=sys.stderr)
        return []

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=MOBILE_UA,
            viewport={"width": 390, "height": 844},
            is_mobile=True,
        )
        page = ctx.new_page()

        try:
            page.goto(
                f"https://www.douyin.com/search/{urllib.request.quote(keyword)}",
                wait_until="commit",
                timeout=60000,
            )
            # Wait for redirect to so.douyin.com to complete
            time.sleep(2)
            try:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception:
                pass
            time.sleep(delay)

            # Scroll to load more content
            for _ in range(min(limit // 5, 4)):
                try:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                except Exception:
                    pass
                time.sleep(1.5)

            # Check for captcha
            try:
                html = page.content()
                if "验证码" in html:
                    print("⚠️  遇到验证码页面，尝试等待...", file=sys.stderr)
                    time.sleep(5)
            except Exception:
                pass

            # Extract results from the rendered page
            raw_items = page.evaluate("""(limit) => {
                const items = [];
                const body = document.body;
                const allText = body.innerText || '';
                
                // Split by newlines and look for result blocks
                // Each result typically has: author, description, stats
                const lines = allText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                
                let currentItem = null;
                let lineCount = 0;
                
                for (let i = 0; i < lines.length && items.length < limit * 3; i++) {
                    const line = lines[i];
                    
                    // Skip navigation / UI chrome
                    if (/^(综合|AI搜索|图片|视频|直播|用户|大家还在搜|搜索|广告|宣传|团|查看|充值|客户端|壁纸|通知|投稿|登录|精选|推荐|关注|朋友|我的|小游戏)$/.test(line)) continue;
                    
                    // Detect author line (short, no punctuation at end, often followed by description)
                    const isAuthor = line.length <= 20 && line.length >= 2 
                        && !line.endsWith('。') && !line.endsWith('！') && !line.endsWith('？')
                        && !line.includes('查看') && !line.includes('套餐')
                        && !/^\\d+$/.test(line) && !line.startsWith('¥');
                    
                    // Detect stats line (contains numbers with possible Chinese labels)
                    const statsMatch = line.match(/^(\\d+)\\s*(\\d+)\\s*(\\d+)\\s*(\\d+)$/);
                    
                    // Detect date line
                    const dateMatch = line.match(/^20\\d{2}[./-]\\d{1,2}[./-]\\d{1,2}$/);
                    
                    if (isAuthor && !currentItem) {
                        currentItem = { author: line, description: '', date: '', stats: [] };
                    } else if (currentItem) {
                        if (dateMatch) {
                            currentItem.date = line;
                        } else if (statsMatch) {
                            currentItem.stats = [parseInt(statsMatch[1]), parseInt(statsMatch[2]), parseInt(statsMatch[3]), parseInt(statsMatch[4])];
                            items.push(currentItem);
                            currentItem = null;
                        } else if (line.length > 15 && !line.startsWith('¥') && !line.includes('套餐') && !line.includes('查看地址')) {
                            if (!currentItem.description) {
                                currentItem.description = line;
                            }
                        }
                    }
                }
                
                // Also collect any remaining items without perfect structure
                return items;
            }""", limit)

            today = date.today().isoformat()
            for item in raw_items[:limit]:
                stats = item.get("stats", [0, 0, 0, 0])
                results.append(VideoData(
                    title=item.get("description", "")[:80],
                    description=item.get("description", ""),
                    author=item.get("author", ""),
                    play_count=stats[0] if len(stats) > 0 else 0,
                    like_count=stats[1] if len(stats) > 1 else 0,
                    comment_count=stats[2] if len(stats) > 2 else 0,
                    share_count=stats[3] if len(stats) > 3 else 0,
                    url=f"https://www.douyin.com/search/{urllib.request.quote(keyword)}",
                    tags=[keyword, "搜索"],
                    publish_time=item.get("date", today),
                ))

            # Fallback: if structured extraction failed, use raw text
            if not results:
                try:
                    body_text = page.inner_text("body")
                    results = _parse_raw_text(body_text, keyword, limit)
                except Exception:
                    pass

        except Exception as e:
            print(f"⚠️  搜索出错: {e}", file=sys.stderr)
        finally:
            browser.close()

    return results


def _parse_raw_text(text: str, keyword: str, limit: int) -> list[VideoData]:
    """Parse raw page text into VideoData items as a fallback."""
    results = []
    today = date.today().isoformat()
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Skip UI chrome
    skip = {"综合", "AI搜索", "图片", "视频", "直播", "用户", "搜索", "广告", "宣传", "团", "充值", "客户端", "壁纸", "通知", "投稿", "登录"}

    i = 0
    while i < len(lines) and len(results) < limit:
        line = lines[i]
        if line in skip or line.startswith("¥") or "查看地址" in line or "套餐" in line:
            i += 1
            continue

        # Look for a pattern: author (short) → description (long) → date → stats
        if len(line) <= 20 and i + 1 < len(lines) and len(lines[i + 1]) > 20:
            author = line
            desc = lines[i + 1]
            dt = ""
            stats = [0, 0, 0, 0]

            # Check for date
            if i + 2 < len(lines) and re.match(r"20\d{2}[./-]\d{1,2}[./-]\d{1,2}", lines[i + 2]):
                dt = lines[i + 2]
                j = i + 3
            else:
                j = i + 2

            # Check for stats (4 numbers on one line)
            if j < len(lines):
                m = re.match(r"^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$", lines[j])
                if m:
                    stats = [int(m.group(k)) for k in range(1, 5)]

            results.append(VideoData(
                title=desc[:80],
                description=desc,
                author=author,
                play_count=stats[0],
                like_count=stats[1],
                comment_count=stats[2],
                share_count=stats[3],
                url=f"https://www.douyin.com/search/{urllib.request.quote(keyword)}",
                tags=[keyword, "搜索"],
                publish_time=dt or today,
            ))
            i = j + 1
        else:
            i += 1

    return results


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_json(items: list[VideoData], output: Path) -> None:
    output.write_text(
        json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"💾 已保存到: {output}")


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
    print(f"💾 已保存到: {output}")


def display_results(items: list[VideoData]) -> None:
    if not items:
        print("没有找到结果。")
        return
    print("\n" + "=" * 70)
    print(f"📊 搜索结果 ({len(items)} 条)")
    print("=" * 70)
    for i, item in enumerate(items, 1):
        print(f"\n{i}. {item.title}")
        if item.author:
            print(f"   👤 作者: {item.author}")
        if item.play_count or item.like_count:
            print(f"   ▶️ 播放: {item.play_count:,} | 👍 点赞: {item.like_count:,} | 💬 评论: {item.comment_count:,}")
        if item.publish_time:
            print(f"   📅 日期: {item.publish_time}")
        if item.tags:
            print(f"   🏷️ 标签: {', '.join(item.tags)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="抖音搜索爬虫")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    search_p = sub.add_parser("search", help="搜索关键词")
    search_p.add_argument("--keyword", "-k", help="搜索关键词（支持自然语言，如 '搜索一下海鲜视频'）")
    search_p.add_argument("--limit", "-n", type=int, default=10)
    search_p.add_argument("--output", "-o", help="输出文件路径")
    search_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    search_p.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")
    search_p.add_argument("--delay", type=float, default=3.0, help="页面等待时间（秒）")

    # hot
    hot_p = sub.add_parser("hot", help="获取热榜")
    hot_p.add_argument("--limit", "-n", type=int, default=20)
    hot_p.add_argument("--output", "-o", help="输出文件路径")
    hot_p.add_argument("--format", "-f", choices=["json", "csv"], default="json")

    args = parser.parse_args()

    if args.command == "search":
        if not args.keyword:
            print("❌ 请提供搜索关键词 (--keyword)", file=sys.stderr)
            sys.exit(1)

        # Auto-extract keyword from natural language
        keyword = extract_keyword(args.keyword)
        if keyword != args.keyword:
            print(f"💡 解析自然语言: '{args.keyword}' → 关键词: '{keyword}'")

        items = search_videos(
            keyword=keyword,
            limit=args.limit,
            headless=not args.no_headless,
            delay=args.delay,
        )
        display_results(items)

        if args.output and items:
            output = Path(args.output)
            if args.format == "csv":
                write_csv(items, output)
            else:
                write_json(items, output)

    elif args.command == "hot":
        items = fetch_hot_search(limit=args.limit)
        display_results(items)

        if args.output and items:
            output = Path(args.output)
            if args.format == "csv":
                write_csv(items, output)
            else:
                write_json(items, output)


if __name__ == "__main__":
    main()
