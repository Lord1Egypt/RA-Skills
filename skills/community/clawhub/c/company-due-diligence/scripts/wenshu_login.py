#!/usr/bin/env python3
"""
裁判文书网交互式登录脚本

使用方法:
    python scripts/wenshu_login.py

流程:
    1. 打开浏览器窗口
    2. 用户手动完成登录（可能需要验证码）
    3. 登录成功后自动保存 cookies
    4. 后续查询使用保存的 cookies
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
COOKIES_FILE = CONFIG_DIR / "wenshu_cookies.json"
STORAGE_FILE = CONFIG_DIR / "wenshu_storage.json"

WENSHU_URL = "http://wenshu.court.gov.cn/"


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

    # 保存 storage state
    context.storage_state(path=str(STORAGE_FILE))

    print(f"✓ Cookies 已保存到: {COOKIES_FILE}")
    print(f"✓ Storage 已保存到: {STORAGE_FILE}")


def load_storage_state():
    """加载保存的 storage state"""
    if not STORAGE_FILE.exists():
        return None

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def check_login_status(page) -> bool:
    """检查是否已登录"""
    try:
        # 检查是否有用户信息元素
        page.wait_for_selector('.user-info, .login-info, [class*="user"]', timeout=5000)
        return True
    except:
        # 检查页面是否包含登录相关文字
        try:
            content = page.content()
            if '登录' in content and '注册' in content:
                return False
            return True
        except:
            return False


def interactive_login():
    """交互式登录"""
    print("=" * 60)
    print("裁判文书网交互式登录")
    print("=" * 60)
    print()
    print("流程说明:")
    print("1. 浏览器窗口将打开")
    print("2. 请在浏览器中完成登录")
    print("   - 如有验证码，请手动输入")
    print("3. 登录成功后，回到此终端按回车键")
    print("4. Cookies 将自动保存")
    print()
    print("提示: 裁判文书网可能需要验证码，请耐心操作")
    print()
    input("按回车键继续...")
    print()

    with sync_playwright() as p:
        # 启动浏览器
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

        # 访问裁判文书网
        print("正在打开裁判文书网...")
        page.goto(WENSHU_URL, wait_until='networkidle', timeout=60000)
        time.sleep(3)

        # 检查是否已经登录
        if check_login_status(page):
            print("✓ 检测到已登录状态")
            save_cookies(context, page)
            browser.close()
            return True

        # 等待用户登录
        print()
        print("请在浏览器中完成登录:")
        print("  1. 点击页面上的登录按钮")
        print("  2. 输入用户名密码")
        print("  3. 如有验证码，请手动输入")
        print()
        print("登录成功后，请回到此终端按回车键保存登录状态...")
        print()

        # 等待用户操作
        input()

        # 再次检查登录状态
        page.goto(WENSHU_URL, wait_until='networkidle', timeout=30000)
        time.sleep(2)

        # 截图确认
        page.screenshot(path="/tmp/wenshu_login.png")
        print("截图已保存: /tmp/wenshu_login.png")

        print()
        print("无论登录是否成功，都可以保存当前状态用于后续查询。")
        choice = input("是否保存当前 Cookies? (y/n): ").lower()
        
        if choice == 'y':
            save_cookies(context, page)
            browser.close()
            return True

        browser.close()
        return False


def test_cookies():
    """测试保存的 cookies 是否有效"""
    print("=" * 60)
    print("测试裁判文书网 Cookies")
    print("=" * 60)
    print()

    storage = load_storage_state()
    if not storage:
        print("✗ 未找到保存的登录状态")
        print("  请先运行: python scripts/wenshu_login.py")
        return False

    print("正在测试登录状态...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=storage)
        page = context.new_page()

        try:
            page.goto(WENSHU_URL, wait_until='networkidle', timeout=30000)
            time.sleep(3)

            if check_login_status(page):
                print("✓ 登录状态有效!")
                browser.close()
                return True
            else:
                print("⚠ 登录状态可能已过期或需要验证码")
                print("  建议重新运行: python scripts/wenshu_login.py")
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

    parser = argparse.ArgumentParser(description="裁判文书网登录管理")
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
