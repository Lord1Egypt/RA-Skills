#!/usr/bin/env python3
"""牛顿浏览器交互服务

在牛顿 Electron 客户端中，通过内嵌浏览器完成页面跳转和操作。
本模块负责：
1. 生成浏览器操作指令，由牛顿客户端执行
2. 等待浏览器操作结果
3. 检测登录/授权完成状态

牛顿客户端通过解析 Skill 返回的 JSON 中的 browser_action 字段来触发浏览器行为。
"""

import os
import time
import json
import sys
from typing import Optional, Dict, List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _errors import BrowserError
from _const import BROWSER_TIMEOUT, QR_LOGIN_TIMEOUT


# ── 牛顿浏览器交互（主方案）─────────────────────────────────────────────────────

class BrowserAction:
    """浏览器操作指令常量"""
    OPEN_URL = "open_url"
    WAIT_FOR_LOGIN = "wait_for_login"
    GET_PAGE_INFO = "get_page_info"
    CLOSE_BROWSER = "close_browser"
    CLICK_ELEMENT = "click_element"


def build_browser_action(action: str, **kwargs) -> dict:
    """
    构建浏览器操作指令。

    牛顿客户端会解析返回 JSON 中的 browser_action 字段并执行对应操作。
    操作完成后，牛顿客户端会将结果通过 stdin 或回调重新传入 Skill。
    """
    return {
        "browser_action": action,
        "browser_params": kwargs,
    }


def open_auth_url(url: str, wait_for_login: bool = True, timeout: int = BROWSER_TIMEOUT) -> dict:
    """
    在牛顿内嵌浏览器中打开授权链接。

    Returns:
        包含 browser_action 的 dict，牛顿客户端会拦截并打开浏览器。
    """
    return build_browser_action(
        BrowserAction.OPEN_URL,
        url=url,
        wait_for_login=wait_for_login,
        timeout=timeout,
    )


def wait_for_browser_result(timeout: int = BROWSER_TIMEOUT) -> dict:
    """
    等待浏览器操作完成并获取结果。

    在牛顿客户端中，浏览器操作结果会通过以下方式回传：
    1. 环境变量 NEWTON_BROWSER_RESULT
    2. 或通过牛顿客户端的回调机制

    Returns:
        {"success": bool, "final_url": str, "title": str, "error": str}
    """
    # 检查是否有浏览器结果通过环境变量传入
    result_env = os.environ.get("NEWTON_BROWSER_RESULT")
    if result_env:
        try:
            return json.loads(result_env)
        except json.JSONDecodeError:
            pass

    # 默认返回等待指令，由牛顿客户端处理
    return build_browser_action(
        BrowserAction.WAIT_FOR_LOGIN,
        timeout=timeout,
    )


def close_browser() -> dict:
    """关闭牛顿内嵌浏览器。"""
    return build_browser_action(BrowserAction.CLOSE_BROWSER)


# ── 登录检测逻辑（供 Skill 使用）────────────────────────────────────────────────

def is_login_success_by_url(current_url: str, platform: str = None) -> bool:
    """
    根据 URL 判断是否登录/授权成功。

    各平台授权完成后的 URL 特征：
    - 淘宝：跳转到卖家中心或授权回调页
    - 抖音：跳转到抖店或授权回调页
    - 拼多多：跳转到商家后台或授权回调页
    """
    if not current_url:
        return False

    # 登录完成标志：URL 离开登录页域名
    login_patterns = [
        "login.taobao.com",
        "fxg.jinritemai.com/login",
        "mms.pinduoduo.com/login",
        "login.kuaishou.com",
        "accounts.douyin.com",
    ]

    is_login_page = any(pattern in current_url for pattern in login_patterns)
    return not is_login_page


def is_auth_callback_url(url: str) -> bool:
    """判断 URL 是否是授权回调页。"""
    if not url:
        return False

    callback_patterns = [
        "/auth/callback",
        "/oauth/callback",
        "/callback",
        "auth_success",
        "authorize_success",
    ]

    return any(pattern in url for pattern in callback_patterns)


# ── 浏览器状态轮询（Fallback）──────────────────────────────────────────────────

def poll_browser_state(poll_interval: int = 3, max_attempts: int = 60,
                        check_fn = None) -> dict:
    """
    轮询浏览器状态，直到条件满足或超时。

    在牛顿客户端中，此轮询由客户端代为实现，Skill 只需返回轮询指令。
    在非牛顿环境（如测试），可以通过 Playwright 直接轮询。
    """
    # 牛顿客户端模式下，返回轮询指令
    if os.environ.get("NEWTON_CLIENT") == "true":
        return build_browser_action(
            BrowserAction.GET_PAGE_INFO,
            poll_interval=poll_interval,
            max_attempts=max_attempts,
        )

    # 非牛顿环境：尝试使用 Playwright fallback
    return _poll_with_playwright(poll_interval, max_attempts, check_fn)


# ── Playwright Fallback（非牛顿环境）───────────────────────────────────────────

def _poll_with_playwright(poll_interval: int, max_attempts: int,
                          check_fn) -> dict:
    """使用 Playwright 直接轮询浏览器状态（fallback）。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "Playwright 未安装，无法在非牛顿环境中操作浏览器。"
                     "请在牛顿客户端中运行此 Skill。"
        }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        pages = context.pages

        if not pages:
            browser.close()
            return {"success": False, "error": "没有打开的页面"}

        page = pages[-1]

        for attempt in range(max_attempts):
            try:
                current_url = page.url
                title = page.title()

                if check_fn and check_fn(current_url):
                    browser.close()
                    return {
                        "success": True,
                        "final_url": current_url,
                        "title": title,
                    }

            except Exception:
                pass

            time.sleep(poll_interval)

        browser.close()
        return {
            "success": False,
            "error": f"轮询超时（{poll_interval * max_attempts}秒）",
        }


def open_url_with_playwright(url: str, wait_seconds: int = 10) -> dict:
    """使用 Playwright 打开 URL（fallback 方案）。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "Playwright 未安装，无法打开浏览器。"
        }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, timeout=wait_seconds * 1000)
            page.wait_for_load_state("domcontentloaded", timeout=wait_seconds * 1000)

            result = {
                "success": True,
                "final_url": page.url,
                "title": page.title(),
            }
            browser.close()
            return result
    except Exception as e:
        return {"success": False, "error": str(e)}
