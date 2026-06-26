#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from typing import Optional

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

SEARCH_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def normalize_subject_url(url: str) -> Optional[str]:
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "url" in qs and qs["url"]:
        url = qs["url"][0]
    m = re.search(r"https?://book\.douban\.com/subject/\d+/?", url)
    return m.group(0) if m else None


def search_first_book(book_name: str) -> str:
    url = "https://www.douban.com/search?cat=1001&q=" + urllib.parse.quote(book_name)
    resp = requests.get(url, headers={"User-Agent": SEARCH_UA}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.select(".result .title a, .result .pic a"):
        href = a.get("href", "")
        subject_url = normalize_subject_url(href)
        if subject_url:
            return subject_url

    # fallback: regex on raw html
    m = re.search(r'https?://www\.douban\.com/link2/\?url=([^"\']+)', resp.text)
    if m:
        subject_url = normalize_subject_url(urllib.parse.unquote(m.group(1)))
        if subject_url:
            return subject_url

    raise RuntimeError(f"未找到《{book_name}》的豆瓣图书结果")


def ensure_parent(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def detect_logged_in(page) -> bool:
    try:
        if page.locator("text=登录/注册").count() > 0:
            return False
    except Exception:
        pass
    try:
        if page.locator("#db-nav-sns .nav-user-account, .top-nav-info a[href*='people']").count() > 0:
            return True
    except Exception:
        pass
    # fallback: if page contains interest section but not login/register it's often okay
    return page.locator("#interest_sect, .aside, #wrapper").count() > 0


def already_in_wishlist(page) -> bool:
    checks = [
        "text=我想读这本书",
        "a.collect_btn[name^='pbtn-']:has-text('修改')",
        "input[type=submit][value='删除']",
    ]
    for sel in checks:
        try:
            if page.locator(sel).count() > 0:
                return True
        except Exception:
            pass
    return False


def click_want_to_read(page) -> bool:
    primary_selectors = [
        "input[type=submit][value='想读']",
        "#interest_sect input[type=submit][value='想读']",
        "a:has-text('想读')",
        "button:has-text('想读')",
        "text=想读",
    ]
    opened = False
    for sel in primary_selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                loc.click(timeout=3000)
                page.wait_for_timeout(1200)
                opened = True
                break
        except Exception:
            continue

    if not opened:
        return False

    # 豆瓣第一次点击“想读”只会弹出收藏表单，必须再点一次“保存”。
    save_selectors = [
        "form[action*='/j/subject/'][method='POST'] input[type=submit][value='保存']",
        "input[type=submit][value='保存']",
    ]
    for sel in save_selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                loc.click(timeout=3000)
                page.wait_for_timeout(1800)
                return True
        except Exception:
            continue

    # 没有保存按钮时，可能是已经在想读列表里，或者页面结构变化。
    return True


def detect_success(page) -> bool:
    if already_in_wishlist(page):
        return True

    success_markers = [
        "我想读这本书",
        "修改",
        "删除",
    ]
    for text in success_markers:
        try:
            if page.locator(f"text={text}").count() > 0:
                return True
        except Exception:
            pass
    return False


def run(book_name: str, profile_dir: str, headed: bool = False, login_only: bool = False):
    ensure_parent(profile_dir)
    result = {
        "book_name": book_name,
        "profile_dir": profile_dir,
        "headed": headed,
    }

    if not login_only:
        subject_url = search_first_book(book_name)
        result["subject_url"] = subject_url
    else:
        subject_url = "https://book.douban.com/"
        result["subject_url"] = subject_url

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=not headed,
            viewport={"width": 1440, "height": 1000},
            user_agent=SEARCH_UA,
            locale="zh-CN",
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(subject_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)

        if login_only:
            result.update({
                "status": "login_required",
                "message": "请在打开的浏览器中完成豆瓣登录，然后重新运行本脚本。",
                "current_url": page.url,
            })
            print(json.dumps(result, ensure_ascii=False, indent=2))
            input("登录完成后按回车关闭浏览器... ")
            context.close()
            return

        result["current_url"] = page.url
        result["logged_in_before_click"] = detect_logged_in(page)
        result["already_in_wishlist_before_click"] = already_in_wishlist(page)

        if result["already_in_wishlist_before_click"]:
            clicked = False
        else:
            clicked = click_want_to_read(page)
        result["clicked"] = clicked
        result["current_url_after_click"] = page.url
        page.wait_for_timeout(1500)

        # detect login redirect / popup-ish signals
        page_text = page.locator("body").inner_text(timeout=3000)[:3000]
        needs_login = (
            (not result["logged_in_before_click"]) or
            ("扫码登录" in page_text) or
            ("登录豆瓣" in page_text) or
            ("注册/登录" in page_text)
        )
        result["needs_login"] = needs_login
        result["success"] = (result["already_in_wishlist_before_click"] or clicked) and detect_success(page) and (not needs_login)
        result["title"] = page.title()

        print(json.dumps(result, ensure_ascii=False, indent=2))
        context.close()


def main():
    parser = argparse.ArgumentParser(description="Add a Douban book to wishlist")
    parser.add_argument("book_name", nargs="?", help="书名")
    parser.add_argument(
        "--profile-dir",
        default=os.path.expanduser("~/.openclaw/browser-profiles/douban-playwright"),
        help="Playwright 持久化用户目录",
    )
    parser.add_argument("--headed", action="store_true", help="显示浏览器窗口")
    parser.add_argument("--login", action="store_true", help="仅打开浏览器供手动登录")
    args = parser.parse_args()

    if not args.login and not args.book_name:
        parser.error("需要提供书名，或使用 --login")

    run(args.book_name or "", args.profile_dir, headed=args.headed, login_only=args.login)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)
