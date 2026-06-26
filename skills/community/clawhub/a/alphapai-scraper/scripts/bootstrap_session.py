#!/usr/bin/env python3
"""
One-time manual login bootstrap for AlphaPai.
Opens a headed browser, waits for the user to complete login, then saves storage state.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

from common import ensure_runtime_dirs, load_settings, resolve_path


async def wait_until_authenticated(page, settings: dict, timeout_seconds: int) -> bool:
    target_url = settings["site"]["target_url"]
    for _ in range(timeout_seconds):
        try:
            if "/login" not in page.url:
                await page.goto(target_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(1000)
                body = await page.locator("body").inner_text(timeout=2000)
                if "登录" not in body or "点评" in body or "comment" in page.url:
                    return True
        except Exception:
            pass
        await page.wait_for_timeout(1000)
    return False


async def main_async(settings_path: str | None, timeout_seconds: int) -> int:
    settings = load_settings(settings_path)
    settings["browser"]["headless"] = False
    runtime_dirs = ensure_runtime_dirs(settings)
    storage_state_path = resolve_path(settings["browser"]["storage_state_file"])
    assert storage_state_path is not None
    storage_state_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        print("打开登录页，请在浏览器里完成 Alpha派登录。")
        print(f"登录页: {settings['site']['login_url']}")
        await page.goto(settings["site"]["login_url"], wait_until="domcontentloaded")

        ok = await wait_until_authenticated(page, settings, timeout_seconds)
        if not ok:
            print("未在等待时间内检测到登录成功。")
            await browser.close()
            return 1

        await context.storage_state(path=str(storage_state_path))
        cookies = await context.cookies()
        cookies_path = runtime_dirs["runtime_dir"] / "bootstrap_cookies.json"
        cookies_path.write_text(
            json.dumps({"cookies": cookies}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"已保存 storage state: {storage_state_path}")
        print(f"已保存 cookies 备份: {cookies_path}")
        await browser.close()
        return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap AlphaPai login session")
    parser.add_argument("--settings", help="Path to settings file")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return asyncio.run(main_async(args.settings, args.timeout_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
