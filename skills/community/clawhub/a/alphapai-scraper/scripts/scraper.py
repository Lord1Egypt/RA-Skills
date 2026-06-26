#!/usr/bin/env python3
"""
AlphaPai comment scraper with multi-auth and extraction fallbacks.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

from playwright.async_api import (
    BrowserContext,
    Error as PlaywrightError,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from archive_store import index_articles
from common import (
    build_run_stamp,
    choose_output_extension,
    ensure_runtime_dirs,
    is_within_window,
    load_auth_bundle,
    load_settings,
    parse_time_label_to_minutes,
    resolve_path,
    should_stop_on_time_label,
)

ITEM_SELECTORS = [
    ".comment-item",
    ".post-item",
    "[class*='comment']",
    "[class*='article-item']",
    "[class*='feed-item']",
    "li[class]",
    "div[class*='item']",
]

TIME_SELECTORS = [
    "[class*='time']",
    "[class*='date']",
    "time",
    ".ago",
    "[class*='ago']",
]

TITLE_SELECTORS = [
    "[class*='title']",
    "h1",
    "h2",
    "h3",
    "[class*='heading']",
]

MODAL_SELECTORS = [
    "[class*='modal']",
    "[class*='dialog']",
    "[class*='popup']",
    "[class*='detail']",
    "[role='dialog']",
]

DETAIL_CONTENT_SELECTORS = [
    "article",
    "main",
    "[class*='detail']",
    "[class*='content']",
    "[class*='article']",
    "body",
]

NOISE_WORDS = {
    "复制",
    "分享",
    "举报",
    "收藏",
    "点赞",
    "评论",
    "关注",
    "取消关注",
    "查看原文",
    "展开",
    "收起",
}


@dataclass
class ScrapedArticle:
    title: str
    time_label: str
    age_minutes: int | None
    content: str
    source_strategy: str


def clean_text(raw: str) -> str:
    cleaned: list[str] = []
    seen: set[str] = set()
    for line in raw.splitlines():
        line = re.sub(r"\s+", " ", line.strip())
        if not line or line in NOISE_WORDS or len(line) < 2:
            continue
        if line in seen:
            continue
        cleaned.append(line)
        seen.add(line)
    return "\n".join(cleaned)


async def launch_contexts(playwright, settings: dict[str, Any], mode: str):
    browser_settings = settings["browser"]
    timeout_ms = int(browser_settings["timeout_ms"])

    if mode == "profile":
        profile_dir = resolve_path(browser_settings["profile_user_data_dir"])
        if profile_dir is None:
            raise RuntimeError("Missing browser.profile_user_data_dir")
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            channel="chrome",
            headless=bool(browser_settings["headless"]),
            ignore_default_args=["--enable-automation"],
            args=[
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context.set_default_timeout(timeout_ms)
        return None, context

    browser = await playwright.chromium.launch(
        headless=bool(browser_settings["headless"])
    )
    storage_state_path = resolve_path(browser_settings.get("storage_state_file"))
    context_kwargs: dict[str, Any] = {"ignore_https_errors": True}
    if storage_state_path and storage_state_path.exists():
        context_kwargs["storage_state"] = str(storage_state_path)
    context = await browser.new_context(**context_kwargs)
    context.set_default_timeout(timeout_ms)
    return browser, context


async def page_body_text(page: Page, limit: int = 2000) -> str:
    try:
        text = await page.locator("body").inner_text(timeout=2000)
    except Exception:
        return ""
    return text[:limit]


async def page_has_list_items(page: Page) -> bool:
    for selector in ITEM_SELECTORS:
        try:
            if await page.locator(selector).count():
                return True
        except PlaywrightError:
            continue
    return False


async def validate_authenticated(page: Page, settings: dict[str, Any]) -> bool:
    login_keyword = settings["site"]["login_path_keyword"]
    if login_keyword in page.url:
        return False

    body = await page_body_text(page)
    unauth_keywords = ["验证码登录", "手机号登录", "欢迎登录", "登录后查看"]
    if any(keyword in body for keyword in unauth_keywords) and not await page_has_list_items(page):
        return False

    return True


async def apply_token_auth(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
) -> tuple[bool, str]:
    token = auth_bundle["token"]
    if not token:
        return False, "缺少 USER_AUTH_TOKEN"

    base_url = settings["site"]["base_url"]
    target_url = settings["site"]["target_url"]
    storage_key = settings["site"]["token_storage_key"]

    init_script = json.dumps(
        {
            "origin": base_url,
            "key": storage_key,
            "token": token,
        },
        ensure_ascii=False,
    )
    await context.add_init_script(
        script=f"""
        (() => {{
          const payload = {init_script};
          if (window.location.origin === payload.origin) {{
            window.localStorage.setItem(payload.key, payload.token);
          }}
        }})();
        """
    )
    await page.goto(base_url, wait_until="domcontentloaded")
    await page.evaluate(
        """(payload) => {
            window.localStorage.setItem(payload.key, payload.token);
        }""",
        {"key": storage_key, "token": token},
    )
    await page.goto(target_url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    if await validate_authenticated(page, settings):
        return True, "localStorage token 注入成功"
    return False, "token 注入后仍未进入目标页"


async def apply_storage_state_auth(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
) -> tuple[bool, str]:
    storage_state_file = auth_bundle.get("storage_state_file") or ""
    if not storage_state_file:
        return False, "未配置 storage state 文件"
    if not resolve_path(storage_state_file) or not resolve_path(storage_state_file).exists():
        return False, "storage state 文件不存在"

    await page.goto(settings["site"]["target_url"], wait_until="domcontentloaded")
    await page.wait_for_timeout(1200)
    if await validate_authenticated(page, settings):
        return True, "复用缓存 storage state 成功"
    return False, "缓存 storage state 已失效"


async def apply_cookies_auth(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
) -> tuple[bool, str]:
    cookies = auth_bundle["cookies"]
    if not cookies:
        return False, "缺少 cookies"

    await context.add_cookies(cookies)
    await page.goto(settings["site"]["target_url"], wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    if await validate_authenticated(page, settings):
        return True, "cookies 注入成功"
    return False, "cookies 注入后仍未进入目标页"


async def try_fill(page: Page, selectors: list[str], value: str) -> bool:
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if await locator.count():
                await locator.click()
                await locator.fill(value)
                return True
        except Exception:
            continue
    return False


async def try_submit(page: Page, selectors: list[str]) -> bool:
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if await locator.count():
                await locator.click()
                return True
        except Exception:
            continue
    try:
        await page.keyboard.press("Enter")
        return True
    except Exception:
        return False


async def apply_credentials_auth(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
) -> tuple[bool, str]:
    credentials = auth_bundle["credentials"]
    username = credentials.get("username") or ""
    password = credentials.get("password") or ""
    if not username or not password:
        return False, "缺少账号密码"

    selectors = settings["auth"]["selectors"]
    await page.goto(settings["site"]["login_url"], wait_until="domcontentloaded")
    await page.wait_for_timeout(1000)

    filled_user = await try_fill(page, selectors["username"], username)
    filled_password = await try_fill(page, selectors["password"], password)
    submitted = await try_submit(page, selectors["submit"])
    await page.wait_for_timeout(2500)
    if not (filled_user and filled_password and submitted):
        return False, "登录表单定位失败，请补充 selectors"

    await page.goto(settings["site"]["target_url"], wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    if await validate_authenticated(page, settings):
        return True, "账号密码登录成功"
    return False, "账号密码提交后仍未进入目标页，可能存在验证码或表单变更"


async def apply_profile_auth(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
) -> tuple[bool, str]:
    await page.goto(settings["site"]["target_url"], wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    if await validate_authenticated(page, settings):
        return True, "复用本机 Chrome Profile 成功"
    return False, "Profile 模式未进入目标页"


AUTH_HANDLERS = {
    "storage_state": apply_storage_state_auth,
    "token": apply_token_auth,
    "cookies": apply_cookies_auth,
    "credentials": apply_credentials_auth,
    "profile": apply_profile_auth,
}


async def authenticate(
    context: BrowserContext,
    page: Page,
    settings: dict[str, Any],
    auth_bundle: dict[str, Any],
    launch_mode: str,
) -> tuple[bool, list[str]]:
    logs: list[str] = []
    methods = settings["auth"]["methods"]

    if launch_mode == "profile":
        ok, message = await apply_profile_auth(context, page, settings, auth_bundle)
        logs.append(f"profile: {message}")
        return ok, logs

    for method in methods:
        if method == "profile":
            continue
        handler = AUTH_HANDLERS[method]
        try:
            ok, message = await handler(context, page, settings, auth_bundle)
        except Exception as exc:
            ok, message = False, f"{method} 异常: {exc}"
        logs.append(f"{method}: {message}")
        if ok:
            return True, logs

    return False, logs


async def get_item_count(page: Page) -> tuple[int, str | None]:
    for selector in ITEM_SELECTORS:
        try:
            count = await page.locator(selector).count()
        except PlaywrightError:
            continue
        if count:
            return count, selector
    return 0, None


async def get_text_from_candidates(scope: Any, selectors: list[str]) -> str:
    for selector in selectors:
        try:
            locator = scope.locator(selector).first
            if await locator.count():
                text = (await locator.inner_text()).strip()
                if text:
                    return text
        except Exception:
            continue
    return ""


async def close_modal(page: Page) -> None:
    close_selectors = [
        "[class*='close']",
        "[aria-label*='关闭']",
        "[aria-label*='close']",
        "button[class*='close']",
        ".modal-close",
    ]
    for selector in close_selectors:
        try:
            locator = page.locator(selector).first
            if await locator.count():
                await locator.click(timeout=1000)
                await page.wait_for_timeout(500)
                return
        except Exception:
            continue
    try:
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
    except Exception:
        pass


async def extract_from_modal(page: Page, item, settings: dict[str, Any]) -> str | None:
    await item.scroll_into_view_if_needed()
    await item.click(timeout=3000)
    await page.wait_for_timeout(int(settings["scrape"]["detail_wait_ms"]))
    for selector in MODAL_SELECTORS:
        try:
            modal = page.locator(selector).last
            if await modal.count():
                text = clean_text(await modal.inner_text())
                await close_modal(page)
                if len(text) > 40:
                    return text
        except Exception:
            continue
    await close_modal(page)
    return None


async def extract_from_link(context: BrowserContext, item, settings: dict[str, Any]) -> str | None:
    try:
        link = item.locator("a[href]").first
        if not await link.count():
            return None
        href = await link.get_attribute("href")
        if not href:
            return None
    except Exception:
        return None

    detail_url = urljoin(settings["site"]["base_url"], href)
    detail_page = await context.new_page()
    try:
        await detail_page.goto(detail_url, wait_until="domcontentloaded")
        await detail_page.wait_for_timeout(int(settings["scrape"]["detail_wait_ms"]))
        for selector in DETAIL_CONTENT_SELECTORS:
            try:
                locator = detail_page.locator(selector).first
                if await locator.count():
                    text = clean_text(await locator.inner_text())
                    if len(text) > 40:
                        return text
            except Exception:
                continue
        return None
    finally:
        await detail_page.close()


async def extract_from_card(item) -> str | None:
    try:
        text = clean_text(await item.inner_text())
    except Exception:
        return None
    return text if len(text) > 40 else None


async def save_storage_state(context: BrowserContext, settings: dict[str, Any]) -> None:
    if not settings["browser"]["save_storage_state"]:
        return
    path = resolve_path(settings["browser"]["storage_state_file"])
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    await context.storage_state(path=str(path))


def render_raw_output(
    articles: list[ScrapedArticle], lookback_hours: float, stamp: str, raw_format: str
) -> str:
    if raw_format == "txt":
        lines = [
            f"Alpha派点评原文",
            f"抓取时间: {stamp}",
            f"窗口: 最近 {lookback_hours:g} 小时",
            f"篇数: {len(articles)}",
            "",
        ]
        for index, article in enumerate(articles, start=1):
            lines.extend(
                [
                    "=" * 60,
                    f"[{index:02d}] {article.title}",
                    f"时间: {article.time_label}",
                    f"来源: {article.source_strategy}",
                    "-" * 40,
                    article.content,
                    "",
                ]
            )
        return "\n".join(lines).strip() + "\n"

    lines = [
        f"# Alpha派点评原文",
        "",
        f"- 抓取时间: `{stamp}`",
        f"- 窗口: 最近 `{lookback_hours:g}` 小时",
        f"- 篇数: `{len(articles)}`",
        "",
    ]
    for index, article in enumerate(articles, start=1):
        lines.extend(
            [
                f"## [{index:02d}] {article.title}",
                "",
                f"- 时间: `{article.time_label}`",
                f"- 来源: `{article.source_strategy}`",
                "",
                article.content,
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


async def scrape_latest_comments(
    settings: dict[str, Any],
    lookback_hours: float,
) -> dict[str, Any]:
    auth_bundle = load_auth_bundle(settings)
    runtime_dirs = ensure_runtime_dirs(settings)
    raw_ext = choose_output_extension(settings, "raw_format")
    stamp = build_run_stamp()

    debug_log: list[str] = []

    async with async_playwright() as playwright:
        last_error = "未执行"
        for launch_mode in settings["browser"]["launch_strategy"]:
            browser = None
            context = None
            page = None
            try:
                browser, context = await launch_contexts(playwright, settings, launch_mode)
                page = await context.new_page()

                ok, auth_logs = await authenticate(
                    context=context,
                    page=page,
                    settings=settings,
                    auth_bundle=auth_bundle,
                    launch_mode=launch_mode,
                )
                debug_log.extend([f"[{launch_mode}] {line}" for line in auth_logs])
                if not ok:
                    last_error = f"{launch_mode} 登录失败"
                    continue

                await save_storage_state(context, settings)
                await page.goto(settings["site"]["target_url"], wait_until="domcontentloaded")
                await page.wait_for_timeout(int(settings["scrape"]["list_wait_ms"]))

                articles: list[ScrapedArticle] = []
                seen_keys: set[str] = set()
                stop_scraping = False

                for round_index in range(int(settings["scrape"]["max_scroll_rounds"])):
                    item_count, active_selector = await get_item_count(page)
                    debug_log.append(
                        f"[{launch_mode}] round {round_index + 1}: selector={active_selector}, count={item_count}"
                    )
                    if item_count == 0 or not active_selector:
                        break

                    items = page.locator(active_selector)
                    for index in range(item_count):
                        item = items.nth(index)
                        time_label = await get_text_from_candidates(item, TIME_SELECTORS)
                        title = await get_text_from_candidates(item, TITLE_SELECTORS)
                        if not title:
                            title = clean_text(await item.inner_text())[:60] or "未命名点评"

                        item_key = f"{time_label}|{title}"
                        if item_key in seen_keys:
                            continue
                        seen_keys.add(item_key)

                        age_minutes = parse_time_label_to_minutes(time_label)
                        if settings["scrape"]["require_time_label"] and not time_label:
                            continue
                        if time_label and should_stop_on_time_label(time_label, lookback_hours):
                            stop_scraping = True
                            debug_log.append(
                                f"[{launch_mode}] stop at item {index + 1} because time={time_label}"
                            )
                            break
                        if time_label and not is_within_window(time_label, lookback_hours):
                            continue

                        content = None
                        source_strategy = ""
                        try:
                            content = await extract_from_modal(page, item, settings)
                            if content:
                                source_strategy = "modal_click"
                        except PlaywrightTimeoutError:
                            content = None
                        except Exception:
                            content = None

                        if not content:
                            content = await extract_from_link(context, item, settings)
                            if content:
                                source_strategy = "detail_link"

                        if not content and settings["scrape"]["allow_card_fallback"]:
                            content = await extract_from_card(item)
                            if content:
                                source_strategy = "card_fallback"

                        if content:
                            articles.append(
                                ScrapedArticle(
                                    title=title,
                                    time_label=time_label or "未知时间",
                                    age_minutes=age_minutes,
                                    content=content,
                                    source_strategy=source_strategy or "unknown",
                                )
                            )
                            if len(articles) >= int(settings["scrape"]["max_items"]):
                                stop_scraping = True
                                break

                    if stop_scraping:
                        break

                    previous_height = await page.evaluate("document.body.scrollHeight")
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(int(settings["scrape"]["list_wait_ms"]))
                    new_height = await page.evaluate("document.body.scrollHeight")
                    if new_height == previous_height:
                        break

                if not articles:
                    last_error = "登录成功，但未抓到符合窗口要求的点评"
                    continue

                raw_path = runtime_dirs["raw_dir"] / f"{stamp}.{raw_ext}"
                raw_content = render_raw_output(articles, lookback_hours, stamp, raw_ext)
                raw_path.write_text(raw_content, encoding="utf-8")

                indexed = index_articles(
                    settings,
                    run_id=stamp,
                    raw_file=str(raw_path),
                    scraped_at=datetime.now().isoformat(timespec="seconds"),
                    lookback_hours=lookback_hours,
                    articles=articles,
                )

                debug_path = runtime_dirs["runtime_dir"] / f"{stamp}_scrape.json"
                debug_path.write_text(
                    json.dumps(
                        {
                            "launch_mode": launch_mode,
                            "lookback_hours": lookback_hours,
                            "items": [article.__dict__ for article in articles],
                            "log": debug_log,
                            "normalized_file": indexed["normalized_file"],
                            "index": {
                                "db_path": indexed["db_path"],
                                "inserted": indexed["inserted"],
                                "total": indexed["total"],
                                "vector_path": indexed.get("vector_path", ""),
                                "vector_chunks": indexed.get("vector_chunks", 0),
                                "vector_enabled": indexed.get("vector_enabled", False),
                            },
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )

                return {
                    "ok": True,
                    "raw_file": str(raw_path),
                    "normalized_file": indexed["normalized_file"],
                    "db_path": indexed["db_path"],
                    "vector_path": indexed.get("vector_path", ""),
                    "vector_chunks": indexed.get("vector_chunks", 0),
                    "indexed_count": indexed["inserted"],
                    "count": len(articles),
                    "launch_mode": launch_mode,
                    "debug_file": str(debug_path),
                }
            except Exception as exc:
                last_error = f"{launch_mode} 抓取异常: {exc}"
                debug_log.append(last_error)
            finally:
                if context:
                    await context.close()
                if browser:
                    await browser.close()

    return {
        "ok": False,
        "error": last_error,
        "log": debug_log,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AlphaPai scraper")
    parser.add_argument("--hours", type=float, default=None)
    parser.add_argument("--settings", help="Path to settings file")
    parser.add_argument("--output-dir", help="Override output base dir")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = load_settings(args.settings)
    if args.output_dir:
        settings["output"]["base_dir"] = args.output_dir
    lookback_hours = (
        args.hours
        if args.hours is not None
        else float(settings["scrape"]["default_lookback_hours"])
    )
    result = asyncio.run(scrape_latest_comments(settings, lookback_hours))
    if result["ok"]:
        print(result["raw_file"])
        return 0
    print(result["error"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
