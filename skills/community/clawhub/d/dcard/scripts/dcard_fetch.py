#!/home/linuxbrew/.linuxbrew/opt/python@3.14/bin/python3.14
"""
Dcard 文章工具 — 單篇抓取 + 看板列表

Usage:
  dcard_fetch.py <post-url-or-id>
  dcard_fetch.py --forum relationship --id 261529038
  dcard_fetch.py list relationship
  dcard_fetch.py list relationship --sort popular --limit 10
  dcard_fetch.py list --all-forums
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

_CAMOUFOX = "/home/ichen/.cache/camoufox/camoufox"
_JS_DIR = Path(__file__).parent


# ── browser helpers ─────────────────────────────


def _browser():
    from patchright.sync_api import sync_playwright

    ps = sync_playwright().start()
    browser = ps.firefox.launch(headless=True, executable_path=_CAMOUFOX, args=["--no-sandbox"])
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-TW",
        timezone_id="Asia/Taipei",
    )
    page = context.new_page()
    return ps, browser, page


# ── fetch single post ────────────────────────────


def fetch_post(forum: str | None, post_id: str) -> dict:
    url = f"https://www.dcard.tw/f/{forum or 'relationship'}/p/{post_id}"
    ps, browser, page = _browser()

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        for _ in range(4):
            page.wait_for_timeout(5000)
            title = page.title()
            if title and title != "Dcard" and "Dcard" in title:
                break

        html = page.content()
        post_data = _extract_post(html)
        if not post_data:
            post_data = {"title": page.title(), "text": page.inner_text("body"), "images": []}
            if post_data["title"] == "Dcard":
                post_data["text"] = "（無法載入文章，可能不存在或需登入）"
        post_data["url"] = url
        post_data["post_id"] = post_id
        return post_data
    finally:
        browser.close()
        ps.stop()


def _extract_post(html: str) -> dict | None:
    import lxml.html

    try:
        root = lxml.html.fromstring(html)
        for script in root.cssselect('script[type="application/ld+json"]'):
            text = script.text_content().strip()
            if '"SocialMediaPosting"' in text:
                data = json.loads(text)
                images = [
                    img.get("src")
                    for img in root.cssselect("img[src*='megapx-assets']")
                    if "orig" in (img.get("src") or "") or "1280" in (img.get("src") or "")
                ]
                return {"title": data.get("headline", "").strip(), "text": data.get("text", "").strip(), "images": images}
    except Exception:
        pass
    return None


# ── list forum posts ─────────────────────────────


@dataclass
class PostItem:
    title: str
    post_id: str
    forum: str
    time_ago: str = ""
    preview: str = ""
    like_count: int = 0
    comment_count: int = 0


def list_posts(forum: str, sort: str = "popular", limit: int = 15) -> List[PostItem]:
    if sort == "latest":
        url = f"https://www.dcard.tw/f/{forum}?latest=true"
    else:
        url = f"https://www.dcard.tw/f/{forum}"

    ps, browser, page = _browser()

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)

        js_file = _JS_DIR / "_list_posts.js"
        with open(js_file) as f:
            js_code = f.read()

        raw = page.evaluate(js_code, forum)
        return [PostItem(**p) for p in raw[:limit]]
    finally:
        browser.close()
        ps.stop()


def list_all_forums() -> dict:
    """抓熱門看板列表"""
    ps, browser, page = _browser()
    try:
        page.goto("https://www.dcard.tw/f/relationship", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(5000)
        forums = page.evaluate("""
            () => {
                const items = [];
                const seen = new Set();
                document.querySelectorAll('a[href*="/f/"]:not([href*="/p/"])').forEach(a => {
                    const m = a.href.match(/\\/f\\/([\\w-]+)/);
                    if (!m || m[1] === 'popular' || seen.has(m[1])) return;
                    seen.add(m[1]);
                    items.push({name: a.textContent.trim() || m[1], slug: m[1]});
                });
                return items.slice(0, 30);
            }
        """)
        return {"forums": forums}
    finally:
        browser.close()
        ps.stop()


# ── output formatting ────────────────────────────


def fmt_post(data: dict, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    lines = [f"標題：{data.get('title', '')}", f"網址：{data.get('url', '')}", "", data.get("text", "")]
    imgs = data.get("images", [])
    if imgs:
        lines.extend(["", "— 圖片 —"] + imgs)
    return "\n".join(lines)


def fmt_list(items: List[PostItem], forum: str, sort: str, fmt: str) -> str:
    if fmt == "json":
        return json.dumps({"forum": forum, "sort": sort, "count": len(items), "posts": [asdict(p) for p in items]},
                          ensure_ascii=False, indent=2)
    label = "🔥 熱門" if sort == "popular" else "🕐 最新"
    lines = [f"=== Dcard /{forum} {label} ===", ""]
    for i, p in enumerate(items, 1):
        prev = (p.preview[:80] + "…") if len(p.preview) > 80 else p.preview
        lines.append(f"{i:2d}. {p.title}")
        if p.time_ago: lines.append(f"    ⏱ {p.time_ago}")
        if prev: lines.append(f"    💬 {prev}")
        lines.append(f"    🔗 https://www.dcard.tw/f/{p.forum}/p/{p.post_id}")
        lines.append("")
    lines.append(f"共 {len(items)} 篇文章")
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────


def _parse_id(s: str) -> tuple:
    m = re.search(r'/f/(\w+)/p/(\d+)', s)
    if m: return m.group(1), m.group(2)
    m = re.search(r'/p/(\d+)', s)
    if m: return None, m.group(1)
    if s.isdigit(): return None, s
    return None, None


def cmd_fetch(args):
    pid = args.id
    forum = args.forum
    if not pid and args.url_or_id:
        f, _id = _parse_id(args.url_or_id)
        forum = forum or f
        pid = _id
    if not pid:
        print("錯誤：請提供文章 ID 或 URL", file=sys.stderr)
        sys.exit(1)
    print(fmt_post(fetch_post(forum, pid), args.format))


def cmd_list(args):
    if args.all_forums:
        data = list_all_forums()
        if args.format == "json":
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print("=== Dcard 熱門看板 ===")
            for f in data.get("forums", []):
                print(f"  {f['name']:20s} /{f['slug']}")
        return
    if not args.forum:
        print("錯誤：請提供看板名稱（如 relationship）或使用 --all-forums", file=sys.stderr)
        sys.exit(1)
    items = list_posts(args.forum, sort=args.sort, limit=args.limit)
    print(fmt_list(items, args.forum, args.sort, args.format))


def main():
    parser = argparse.ArgumentParser(description="Dcard 文章工具")
    sub = parser.add_subparsers(dest="command")
    # fetch
    pf = sub.add_parser("fetch", help="抓取單篇文章")
    pf.add_argument("url_or_id", nargs="?")
    pf.add_argument("--forum", "-f", default=None)
    pf.add_argument("--id", "-i", default=None)
    pf.add_argument("--format", "-o", choices=["text", "json"], default="text")
    # list
    pl = sub.add_parser("list", help="看板文章列表")
    pl.add_argument("forum", nargs="?", default=None)
    pl.add_argument("--sort", "-s", choices=["popular", "latest"], default="popular")
    pl.add_argument("--limit", "-l", type=int, default=15)
    pl.add_argument("--format", "-o", choices=["text", "json"], default="text")
    pl.add_argument("--all-forums", "-A", action="store_true", help="顯示熱門看板")
    args = parser.parse_args()
    if args.command == "list":
        cmd_list(args)
    elif args.command == "fetch":
        cmd_fetch(args)
    else:
        # default = fetch
        args.command = "fetch"
        cmd_fetch(args)


if __name__ == "__main__":
    main()
