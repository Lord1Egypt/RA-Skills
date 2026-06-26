#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音 Cookie 有效性检查脚本。
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


async def check_cookie(cookie_file: Path) -> bool:
    print("=" * 50)
    print("抖音 Cookie 有效性检查")
    print("=" * 50)
    print()

    if not cookie_file.exists():
        print(f"Cookie 文件不存在: {cookie_file}")
        print()
        print("请先运行 get_cookie.py 获取 Cookie。")
        return False

    print(f"Cookie 档案: {cookie_file.name}")
    print(f"Cookie 文件: {cookie_file}")
    print("正在验证 Cookie 是否有效...")
    print()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        try:
            context = await browser.new_context(storage_state=str(cookie_file))
            page = await context.new_page()

            await page.goto(
                "https://creator.douyin.com/creator-micro/content/upload",
                timeout=120000,
            )

            try:
                await page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/upload",
                    timeout=10000,
                )
            except Exception:
                pass

            login_required = False
            if await page.get_by_text("手机号登录").count() > 0:
                login_required = True
            elif await page.get_by_text("扫码登录").count() > 0:
                login_required = True
            elif "login" in page.url.lower():
                login_required = True

            await context.close()
            await browser.close()

            if login_required:
                print("Cookie 已失效，需要重新登录。")
                print()
                print("请运行 get_cookie.py 重新获取 Cookie。")
                return False

            print("Cookie 有效，可以正常使用。")
            return True

        except Exception as exc:  # noqa: BLE001
            print(f"检查过程中出错: {exc}")
            await browser.close()
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description="抖音 Cookie 有效性检查")
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

    result = asyncio.run(check_cookie(cookie_file))
    raise SystemExit(0 if result else 1)


if __name__ == "__main__":
    main()
