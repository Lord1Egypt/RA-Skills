#!/usr/bin/env python3
"""Douyin Search Script — Playwright-based search with persistent login.

Strategy:
1. Try Playwright with persistent profile (needs prior login)
2. If no results (not logged in), fall back to suggestion API
3. Optionally try using an external browser profile (e.g. OpenClaw's)

Usage:
    python3 douyin_search.py <keyword> [--count N] [--json]
    python3 douyin_search.py --login           # open browser for QR login
    python3 douyin_search.py --suggestions <kw> # just get keyword suggestions
"""

import argparse
import httpx
import json
import os
import sys
import time
import urllib.parse

PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".browser-profile")
OPENCLAW_PROFILE = "/root/.openclaw/browser/openclaw/user-data"


def get_suggestions(keyword: str) -> list[dict]:
    """Get search suggestions from Douyin's public API (no login required)."""
    url = f"https://www.douyin.com/aweme/v1/web/search/sug/?keyword={urllib.parse.quote(keyword)}&aid=6383"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/",
    }
    try:
        r = httpx.get(url, headers=headers, timeout=10)
        data = r.json()
        suggestions = []
        for item in data.get("sug_list", []):
            suggestions.append({
                "keyword": item.get("content", ""),
                "word": item.get("word_record", {}).get("words_content", ""),
            })
        return suggestions
    except Exception as e:
        return [{"keyword": keyword, "error": str(e)}]


def search_with_playwright(keyword: str, count: int = 10, profile_dir: str = None) -> dict:
    """Search Douyin using Playwright with persistent browser profile."""
    from playwright.sync_api import sync_playwright

    use_dir = profile_dir or PROFILE_DIR
    os.makedirs(use_dir, exist_ok=True)
    results = []
    has_login = False

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                use_dir,
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 900},
                locale="zh-CN",
            )
        except Exception as e:
            return {"status": "error", "message": f"Browser launch failed: {e}", "results": []}

        page = context.new_page()

        # Intercept search API responses
        def handle_response(response):
            nonlocal results
            url = response.url
            if "search/item" in url or "general/search" in url:
                try:
                    data = response.json()
                    aweme_list = data.get("aweme_list") or []
                    if not aweme_list and data.get("data"):
                        for d in data["data"]:
                            if d.get("aweme_info"):
                                aweme_list.append(d["aweme_info"])
                    for item in aweme_list:
                        stats = item.get("statistics", {})
                        results.append({
                            "title": item.get("desc", "").strip(),
                            "author": item.get("author", {}).get("nickname", ""),
                            "aweme_id": item.get("aweme_id", ""),
                            "url": f"https://www.douyin.com/video/{item.get('aweme_id', '')}",
                            "likes": stats.get("digg_count", 0),
                            "comments": stats.get("comment_count", 0),
                            "plays": stats.get("play_count", 0),
                            "shares": stats.get("share_count", 0),
                            "duration": item.get("video", {}).get("duration", 0),
                            "cover": (
                                item.get("video", {}).get("cover", {}).get("url_list", [""])[0]
                                if item.get("video", {}).get("cover")
                                else ""
                            ),
                            "create_time": item.get("create_time", 0),
                        })
                except Exception:
                    pass

        page.on("response", handle_response)

        encoded_kw = urllib.parse.quote(keyword)
        search_url = f"https://www.douyin.com/search/{encoded_kw}"
        page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
        time.sleep(4)

        # Check for login prompt
        try:
            login_el = page.query_selector('text=登录后即可搜索')
            if login_el:
                has_login = False
            else:
                has_login = True
        except Exception:
            pass

        # Scroll to trigger lazy loading
        if has_login or results:
            for _ in range(min(3, max(1, count // 10))):
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(2)

        # Fallback: scrape rendered cards if API interception missed
        if not results:
            try:
                cards = page.query_selector_all('[data-e2e="search-video"], [class*="videoCard"], [class*="video-card"]')
                for card in cards[:count]:
                    try:
                        title_el = card.query_selector('[class*="title"], [class*="desc"], a')
                        title = title_el.inner_text().strip() if title_el else ""
                        href = title_el.get_attribute("href") if title_el else ""
                        if href and not href.startswith("http"):
                            href = "https://www.douyin.com" + href
                        author_el = card.query_selector('[class*="author"], [class*="name"]')
                        author = author_el.inner_text().strip() if author_el else ""
                        results.append({
                            "title": title,
                            "author": author,
                            "url": href,
                            "aweme_id": "",
                            "likes": 0,
                            "comments": 0,
                            "plays": 0,
                        })
                    except Exception:
                        continue
            except Exception:
                pass

        context.close()

    return {
        "status": "ok" if results else "no_results",
        "keyword": keyword,
        "count": len(results),
        "results": results[:count],
    }


def search(keyword: str, count: int = 10) -> dict:
    """Main search function with fallback chain."""
    # Step 1: Try Playwright with own profile
    result = search_with_playwright(keyword, count)

    if result["count"] > 0:
        return result

    # Step 2: Try with OpenClaw browser profile
    if os.path.exists(OPENCLAW_PROFILE):
        result2 = search_with_playwright(keyword, count, profile_dir=OPENCLAW_PROFILE)
        if result2["count"] > 0:
            return result2

    # Step 3: Fallback to suggestion API
    suggestions = get_suggestions(keyword)
    return {
        "status": "suggestions_only",
        "message": "未登录抖音，无法获取完整搜索结果。以下为相关搜索词建议：",
        "keyword": keyword,
        "suggestions": suggestions[:10],
        "results": [],
    }


def do_login():
    """Open a headed browser for QR code login."""
    from playwright.sync_api import sync_playwright

    os.makedirs(PROFILE_DIR, exist_ok=True)
    print("🌐 正在打开浏览器，请在抖音页面扫码登录...")
    print("   登录成功后请关闭浏览器窗口。")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False,
            args=["--no-sandbox"],
            viewport={"width": 1280, "height": 900},
            locale="zh-CN",
        )
        page = context.new_page()
        page.goto("https://www.douyin.com", timeout=30000)
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass
        context.close()

    print("✅ 登录状态已保存！")


def main():
    parser = argparse.ArgumentParser(description="抖音搜索工具")
    parser.add_argument("keyword", nargs="?", help="搜索关键词")
    parser.add_argument("--count", type=int, default=10, help="结果数量")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--login", action="store_true", help="打开浏览器登录")
    parser.add_argument("--suggestions", action="store_true", help="仅获取搜索建议")

    args = parser.parse_args()

    if args.login:
        do_login()
        return

    if not args.keyword:
        parser.error("请提供搜索关键词，或使用 --login 登录")

    if args.suggestions:
        suggestions = get_suggestions(args.keyword)
        if args.json:
            print(json.dumps({"keyword": args.keyword, "suggestions": suggestions}, ensure_ascii=False, indent=2))
        else:
            print(f'\n💡 "{args.keyword}" 相关搜索词：\n')
            for s in suggestions:
                print(f'  • {s["keyword"]}')
        return

    result = search(args.keyword, count=args.count)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "suggestions_only":
        print(f'\n⚠️ {result["message"]}\n')
        for s in result["suggestions"]:
            print(f'  • {s["keyword"]}')
        print('\n登录抖音后即可获取完整搜索结果。运行: python3 scripts/douyin_search.py --login')
    elif result["count"] == 0:
        print(f'\n搜索 "{result["keyword"]}" 未找到结果。可能需要先登录抖音。')
    else:
        print(f'\n🔍 搜索 "{result["keyword"]}" — 共 {result["count"]} 个结果\n')
        for i, r in enumerate(result["results"], 1):
            print(f"  {i}. {r['author']} — {r['title'][:60]}")
            if r['likes'] or r['plays']:
                print(f"     ❤️ {r['likes']}  💬 {r['comments']}  ▶️ {r['plays']}")
            print(f"     🔗 {r['url']}")
            print()


if __name__ == "__main__":
    main()