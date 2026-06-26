"""Platform session management helpers for authenticated browser fallback."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Dict

from datapulse.core.utils import run_sync, session_path

try:
    from playwright.async_api import async_playwright
except Exception:
    async_playwright = None  # type: ignore[assignment]

logger = logging.getLogger("datapulse.session")


PLATFORM_LOGIN_URLS: Dict[str, str] = {
    "xhs": "https://www.xiaohongshu.com/explore",
    "wechat": "https://mp.weixin.qq.com",
}

_DEFAULT_LOGIN_TIMEOUT_SECONDS = int(os.getenv("DATAPULSE_LOGIN_TIMEOUT_SECONDS", "600"))
_DEFAULT_LOGIN_POLL_SECONDS = float(os.getenv("DATAPULSE_LOGIN_POLL_SECONDS", "2"))


def supported_platforms() -> list[str]:
    return sorted(PLATFORM_LOGIN_URLS.keys())


def login_platform(platform: str) -> str:
    """Run a manual login flow and persist Playwright storage state."""
    platform = platform.lower().strip()
    if platform not in PLATFORM_LOGIN_URLS:
        raise ValueError(f"Unsupported platform: {platform}")

    if async_playwright is None:
        raise RuntimeError("Playwright is not installed. Install with: pip install -e '.[browser]'")

    return run_sync(_login(platform))


def _run_instructions(platform: str, state_path: Path) -> str:
    return (
        f"Platform: {platform}\n"
        f"Session saved to: {state_path}\n"
        "1) Complete login in the opened browser window.\n"
        "2) Wait for the page state to settle; session auto-save will trigger when login is detected.\n"
        "3) If detection does not trigger, it will auto-save again after timeout (default 10 minutes)."
    )


async def _is_login_complete(page, platform: str) -> bool:
    try:
        current_url = (page.url or "").lower()
        if any(piece in current_url for piece in ("/login", "/passport", "/signin", "/auth")):
            return False
    except Exception:
        current_url = ""

    if platform == "xhs":
        # XHS 的公开页通常也会带一些通用 session cookie，不能仅凭 cookie 判定。
        # 以 /user/me 为最终信号，guest:false 才算真实账号态。
        try:
            me_ok = await page.evaluate(
                """async () => {
                try {
                    const response = await fetch(
                        'https://edith.xiaohongshu.com/api/sns/web/v2/user/me',
                        {credentials: 'include', headers: {'Accept': 'application/json'}, cache: 'no-store'}
                    );
                    if (!response || !response.ok) {
                        return false;
                    }
                    const payload = await response.json();
                    return !!(
                        payload &&
                        payload.success === true &&
                        payload.data &&
                        payload.data.guest === false
                    );
                } catch {
                    return false;
                }
            }"""
            )
            if me_ok:
                return True
        except Exception:
            pass

    if platform != "xhs":
        try:
            cookies = await page.context.cookies()
            auth_like_cookie = any(
                any(token in (cookie.get("name", "").lower() or "") for token in ("token", "session", "auth", "access", "userid", "uid"))
                for cookie in cookies
            )
            if auth_like_cookie:
                return True
        except Exception:
            pass

        try:
            keys = await page.evaluate(
                "() => {\n                try {\n                    const storage = window.localStorage || {};\n                    return Object.keys(storage).filter((k) => /(token|access|auth|session|uid|userid|user|login|passport)/i.test(k));\n                } catch {\n                    return [];\n                }\n            }"
            )
            if keys:
                return True
        except Exception:
            pass

    if not current_url:
        return False

    # xiaohongshu 主页在未登录时常伴随明显登录提示；有导航到用户态路径或业务页面可视为登录成功
    if current_url.startswith("https://www.xiaohongshu.com") and "xiaohongshu.com" in current_url:
        if any(path in current_url for path in ("/user/", "/profile/", "/notes/", "/note/", "/explore/settings", "/favorite/")):
            return True

    return False


async def _login(platform: str) -> str:
    state_path = Path(session_path(platform))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    start_url = PLATFORM_LOGIN_URLS[platform]
    timeout_seconds = _DEFAULT_LOGIN_TIMEOUT_SECONDS
    poll_seconds = max(0.5, _DEFAULT_LOGIN_POLL_SECONDS)
    deadline = time.monotonic() + timeout_seconds

    async with async_playwright() as p:  # type: ignore[union-attr]
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            logger.info("Starting login for %s: %s", platform, start_url)
            await page.goto(start_url, wait_until="domcontentloaded", timeout=60000)
            print(_run_instructions(platform, state_path))
            try:
                while time.monotonic() < deadline:
                    if page.is_closed():
                        break
                    if await _is_login_complete(page, platform):
                        logger.info("Login completion detected for %s; persisting session.", platform)
                        break
                    await page.wait_for_timeout(int(poll_seconds * 1000))
            except KeyboardInterrupt:
                logger.info("Login flow for %s interrupted by user; saving session anyway.", platform)
            await context.storage_state(path=str(state_path))
            return str(state_path)
        finally:
            await context.close()
            await browser.close()
