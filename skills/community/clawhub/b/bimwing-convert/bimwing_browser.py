#!/usr/bin/env python3
"""BIMWing 浏览器自动化兜底：当 API 直连失败/接口变动时，用 Playwright 驱动网页完成
登录 -> 上传 -> 等待转码 -> 点分享 -> 复制 shareUrl。

依赖: pip install playwright && playwright install chromium
选择器尽量用"可见文字/角色"定位，降低对 DOM 变动的敏感度。
"""
import sys
import time
from bimwing_client import load_credentials


def convert_and_share(file_path, mobile, password, headless=True, timeout=1800):
    from playwright.sync_api import sync_playwright

    WEB = "https://bimwing.letsgrp.com"
    share_url = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(f"{WEB}/login", wait_until="networkidle")

        # 1) 登录：按提示填手机号/密码（字段用 placeholder/相邻文字定位）
        page.fill('input[placeholder*="手机"], input[placeholder*="账号"], input[type="tel"]',
                  mobile)
        page.fill('input[type="password"]', password)
        # 点登录按钮（按文字）
        page.get_by_text("登录", exact=True).click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # 2) 进入上传：点击"上传模型/上传"按钮
        for label in ["上传模型", "上传文件", "上传", "拖拽"]:
            try:
                page.get_by_text(label, exact=False).first.click(timeout=3000)
                break
            except Exception:
                continue

        # 3) 选文件：BIMWing 一般用隐藏的 file input
        file_input = page.wait_for_selector('input[type="file"]', timeout=10000)
        file_input.set_input_files(file_path)

        # 4) 等待转码完成：轮询直到出现"分享"按钮或可查看
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                # 转码完成后一般出现"分享"或"查看"入口
                page.get_by_text("分享", exact=False).first.wait_for(timeout=3000)
                break
            except Exception:
                time.sleep(5)
        else:
            raise TimeoutError("等待转码完成超时")

        # 5) 点分享，复制链接
        page.get_by_text("分享", exact=False).first.click()
        time.sleep(2)
        # 分享弹窗里的链接输入框
        link_input = page.wait_for_selector(
            'input[readonly], input[value^="http"], textarea', timeout=8000)
        share_url = link_input.input_value() or link_input.get_attribute("value")
        browser.close()

    return share_url


def main():
    if len(sys.argv) < 2:
        print("用法: python3 bimwing_browser.py <模型文件路径>")
        sys.exit(1)
    file_path = sys.argv[1]
    mobile, password = load_credentials()
    if not mobile or not password:
        print("缺少 BIMWing 凭证：请设置环境变量 BIMWING_MOBILE/PASSWORD 或填写 config.json")
        sys.exit(2)
    url = convert_and_share(file_path, mobile, password)
    print("\n=== BIMWing 分享链接（浏览器兜底）===")
    print(url)


if __name__ == "__main__":
    main()
