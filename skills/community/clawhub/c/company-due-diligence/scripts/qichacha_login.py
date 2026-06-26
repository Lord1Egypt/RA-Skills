#!/usr/bin/env python3
"""
企查查交互式登录脚本

使用方法:
    python scripts/qichacha_login.py

流程:
    1. 打开浏览器窗口
    2. 用户手动登录企查查
    3. 登录成功后自动保存 cookies
    4. 后续查询使用保存的 cookies 自动登录
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("错误: Playwright 未安装")
    print("请运行: pip install playwright && playwright install chromium")
    sys.exit(1)

# 配置
CONFIG_DIR = Path.home() / ".due_diligence"
COOKIES_FILE = CONFIG_DIR / "qichacha_cookies.json"
STORAGE_FILE = CONFIG_DIR / "qichacha_storage.json"

QICHACHA_URL = "https://www.qcc.com/"
LOGIN_URL = "https://www.qcc.com/user_login"


def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_cookies(context, page):
    """保存 cookies 和 storage state"""
    ensure_config_dir()

    # 保存 cookies
    cookies = context.cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)

    # 保存 storage state (包括 localStorage)
    context.storage_state(path=str(STORAGE_FILE))

    print(f"✓ Cookies 已保存到: {COOKIES_FILE}")
    print(f"✓ Storage 已保存到: {STORAGE_FILE}")


def load_cookies():
    """加载保存的 cookies"""
    if not COOKIES_FILE.exists():
        return None

    with open(COOKIES_FILE, "r") as f:
        return json.load(f)


def load_storage_state():
    """加载保存的 storage state"""
    if not STORAGE_FILE.exists():
        return None

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def check_login_status(page) -> bool:
    """检查是否已登录"""
    try:
        # 检查是否有用户头像或用户名元素
        page.wait_for_selector('.user-info, .header-user, [class*="user"], .m-l-xs', timeout=5000)
        return True
    except:
        return False


def interactive_login():
    """交互式登录"""
    print("=" * 60)
    print("企查查交互式登录")
    print("=" * 60)
    print()
    print("流程说明:")
    print("1. 浏览器窗口将打开")
    print("2. 请在浏览器中完成登录（扫码或密码登录）")
    print("3. 登录成功后，回到此终端按回车键")
    print("4. Cookies 将自动保存")
    print()
    print("提示: 登录后请访问任意公司详情页确认登录状态")
    print()
    input("按回车键继续...")
    print()

    with sync_playwright() as p:
        # 启动浏览器（非 headless，显示窗口）
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )

        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = context.new_page()

        # 访问企查查
        print("正在打开企查查...")
        page.goto(QICHACHA_URL, wait_until='networkidle', timeout=30000)
        time.sleep(2)

        # 检查是否已经登录
        if check_login_status(page):
            print("✓ 检测到已登录状态")
            save_cookies(context, page)
            browser.close()
            return True

        # 跳转到登录页
        print("请完成登录...")
        try:
            login_btn = page.query_selector('text=登录')
            if login_btn:
                login_btn.click()
                time.sleep(2)
        except:
            pass

        # 等待用户登录
        print()
        print("请在浏览器中完成登录:")
        print("  - 方式1: 扫码登录")
        print("  - 方式2: 密码登录")
        print()
        print("登录成功后，请回到此终端按回车键保存登录状态...")
        print()

        # 等待用户操作
        input()

        # 检查登录状态
        page.goto(QICHACHA_URL, wait_until='networkidle')
        time.sleep(2)

        if check_login_status(page):
            print("✓ 登录成功!")
            save_cookies(context, page)
            browser.close()
            return True
        else:
            print("⚠ 未检测到登录状态，请重试")
            print("  如果已完成登录，可能是页面加载问题")
            print("  请确认浏览器中能看到用户信息")

            choice = input("是否仍然保存当前状态? (y/n): ").lower()
            if choice == 'y':
                save_cookies(context, page)
                browser.close()
                return True

            browser.close()
            return False


def test_cookies():
    """测试保存的 cookies 是否有效"""
    print("=" * 60)
    print("测试企查查 Cookies")
    print("=" * 60)
    print()

    storage = load_storage_state()
    if not storage:
        print("✗ 未找到保存的登录状态")
        print("  请先运行: python scripts/qichacha_login.py")
        return False

    print("正在测试登录状态...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=storage)
        page = context.new_page()

        try:
            page.goto(QICHACHA_URL, wait_until='networkidle', timeout=30000)
            time.sleep(2)

            if check_login_status(page):
                print("✓ 登录状态有效!")
                browser.close()
                return True
            else:
                print("✗ 登录状态已过期")
                print("  请重新运行: python scripts/qichacha_login.py")
                browser.close()
                return False

        except Exception as e:
            print(f"✗ 测试失败: {e}")
            browser.close()
            return False


def clear_cookies():
    """清除保存的 cookies"""
    if COOKIES_FILE.exists():
        COOKIES_FILE.unlink()
        print(f"✓ 已删除: {COOKIES_FILE}")

    if STORAGE_FILE.exists():
        STORAGE_FILE.unlink()
        print(f"✓ 已删除: {STORAGE_FILE}")

    print("✓ 登录状态已清除")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="企查查登录管理")
    parser.add_argument("--test", action="store_true", help="测试登录状态")
    parser.add_argument("--clear", action="store_true", help="清除登录状态")

    args = parser.parse_args()

    if args.test:
        test_cookies()
    elif args.clear:
        clear_cookies()
    else:
        interactive_login()


if __name__ == "__main__":
    main()
