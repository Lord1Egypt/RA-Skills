#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音登录 Cookie 获取脚本。
"""

import argparse
import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("错误：未安装 playwright")
    print("请运行：pip install playwright && playwright install chromium")
    raise SystemExit(1)


COOKIE_DIR = Path(__file__).resolve().parent.parent / "cookies"
DEFAULT_COOKIE_FILE = COOKIE_DIR / "douyin.json"
INVALID_COOKIE_NAME_CHARS = set('<>:"/\\|?*')


def resolve_cookie_file(cookie_name: str = "") -> Path:
    COOKIE_DIR.mkdir(parents=True, exist_ok=True)

    raw_name = (cookie_name or "").strip()
    if not raw_name:
        return DEFAULT_COOKIE_FILE

    safe_name = "".join(
        "_" if char in INVALID_COOKIE_NAME_CHARS or ord(char) < 32 else char
        for char in raw_name
    ).rstrip(" .")
    if not safe_name:
        raise ValueError("Cookie 名称不能为空，且不能只包含非法文件名字符。")

    return COOKIE_DIR / f"douyin-{safe_name}.json"


async def get_douyin_cookie(cookie_file: Path) -> None:
    print("=" * 50)
    print("抖音登录 Cookie 获取")
    print("=" * 50)
    print()
    print(f"Cookie 档案: {cookie_file.name}")
    print("即将打开浏览器，请使用抖音 APP 扫码登录。")
    print("登录成功后，请在 Playwright 调试窗口中点击“继续”。")
    print()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("正在打开抖音创作者中心，请稍候...")
        try:
            await page.goto(
                "https://creator.douyin.com/",
                timeout=120000,
                wait_until="domcontentloaded",
            )
        except Exception as exc:  # noqa: BLE001
            print(f"页面加载较慢，但浏览器已打开，可继续操作: {exc}")

        print("请在浏览器中扫码登录，然后点击“继续”保存 Cookie。")
        print()

        await page.pause()
        await context.storage_state(path=str(cookie_file))

        print()
        print("=" * 50)
        print(f"Cookie 已保存到: {cookie_file}")
        print("=" * 50)

        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音 Cookie 获取")
    parser.add_argument(
        "--cookie-name",
        default="",
        help="可选 Cookie 档案名；不传时使用默认 douyin.json",
    )
    args = parser.parse_args()

    try:
        cookie_file = resolve_cookie_file(args.cookie_name)
    except ValueError as exc:
        print(f"错误：{exc}")
        raise SystemExit(1) from exc

    asyncio.run(get_douyin_cookie(cookie_file))


if __name__ == "__main__":
    main()
