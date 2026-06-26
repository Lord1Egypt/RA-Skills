"""Optional Playwright browser collector used as hard anti-scraping fallback."""

from __future__ import annotations

import asyncio
import os
import random
import time
from pathlib import Path
from typing import Any

from datapulse.core.models import SourceType
from datapulse.core.utils import clean_text, run_sync

from .base import BaseCollector, ParseResult

_BROWSER_REQUEST_LOCK = asyncio.Lock()
_LAST_HUMAN_REQUEST_MONO = 0.0


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(int(default))).strip().lower()
    if value == "":
        return default
    return value not in {"0", "false", "no", "off", "n", "f"}


def _env_float(name: str, default: float, min_value: float | None = None, max_value: float | None = None) -> float:
    raw = os.getenv(name, "").strip()
    try:
        value = float(raw) if raw else default
    except (TypeError, ValueError):
        return default
    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
    return value


def _env_int(name: str, default: int, min_value: int | None = None, max_value: int | None = None) -> int:
    raw = os.getenv(name, "").strip()
    try:
        value = int(raw) if raw else default
    except (TypeError, ValueError):
        return default
    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
    return value


def _env_int_range(name_min: str, name_max: str, default_min: int, default_max: int, *, minimum: int = 200, maximum: int = 10000) -> tuple[int, int]:
    min_seconds = _env_int(name_min, default_min, min_value=minimum, max_value=maximum)
    max_seconds = _env_int(name_max, default_max, min_value=minimum, max_value=maximum)
    if max_seconds < min_seconds:
        max_seconds = min_seconds
    return min_seconds, max_seconds


def _human_wait_ms(min_ms: int, max_ms: int) -> int:
    return random.randint(min_ms, max_ms)


async def _throttle_requests(interval_seconds: float, jitter_seconds: float) -> None:
    if interval_seconds <= 0:
        return

    global _LAST_HUMAN_REQUEST_MONO
    async with _BROWSER_REQUEST_LOCK:
        now = time.monotonic()
        if _LAST_HUMAN_REQUEST_MONO == 0.0:
            _LAST_HUMAN_REQUEST_MONO = now
            return

        elapsed = now - _LAST_HUMAN_REQUEST_MONO
        required = max(0.0, interval_seconds + random.uniform(0.0, jitter_seconds) - elapsed)
        if required > 0:
            await asyncio.sleep(required)
        _LAST_HUMAN_REQUEST_MONO = time.monotonic()


async def _simulate_human_page_read(page: Any) -> None:
    viewport = await page.evaluate("() => ({width: window.innerWidth, height: window.innerHeight})")
    width = max(800, int(viewport.get("width", 1280)))
    height = max(600, int(viewport.get("height", 720)))

    # Simulate mouse jitter.
    for _ in range(_env_int("DATAPULSE_BROWSER_HUMAN_MOUSE_MOVES", 2, min_value=1, max_value=8)):
        x = random.randint(80, max(120, width - 80))
        y = random.randint(120, max(140, height - 120))
        await page.mouse.move(x, y, steps=_env_int("DATAPULSE_BROWSER_HUMAN_MOUSE_STEPS", 20, min_value=6, max_value=40))
        await page.wait_for_timeout(_human_wait_ms(150, 700))


async def _simulate_scroll(page: Any, *, traffic_profile: str) -> None:
    min_steps, max_steps = _env_int_range(
        "DATAPULSE_BROWSER_SCROLL_STEPS_MIN",
        "DATAPULSE_BROWSER_SCROLL_STEPS_MAX",
        2,
        5,
        minimum=1,
        maximum=12,
    )
    if traffic_profile != "xhs":
        max_steps = min(max_steps, 3)
        min_steps = min(min_steps, max_steps)

    for _ in range(random.randint(min_steps, max_steps)):
        distance = random.randint(180, 520)
        await page.evaluate("(offset) => window.scrollBy({ top: offset, left: 0, behavior: 'auto' })", distance)
        min_wait, max_wait = _env_int_range(
            "DATAPULSE_BROWSER_SCROLL_WAIT_MS_MIN",
            "DATAPULSE_BROWSER_SCROLL_WAIT_MS_MAX",
            600,
            1600,
            minimum=100,
            maximum=5000,
        )
        await page.wait_for_timeout(_human_wait_ms(min_wait, max_wait))


class BrowserCollector(BaseCollector):
    name = "browser"
    source_type = SourceType.GENERIC
    reliability = 0.68

    def can_handle(self, url: str) -> bool:
        return True

    def parse(
        self,
        url: str,
        storage_state: str | None = None,
        *,
        human_like: bool | None = None,
        traffic_profile: str = "generic",
    ) -> ParseResult:
        try:
            from playwright.async_api import async_playwright
        except Exception:
            return ParseResult.failure(url, "Playwright is not installed")

        human_like = _env_bool("DATAPULSE_BROWSER_HUMAN_LIKE", False) if human_like is None else human_like
        min_interval = _env_float(
            "DATAPULSE_BROWSER_MIN_INTERVAL_SECONDS",
            0.0 if not human_like else 2.2,
            min_value=0.0,
            max_value=20.0,
        )
        interval_jitter = _env_float(
            "DATAPULSE_BROWSER_INTERVAL_JITTER_SECONDS",
            0.0 if not human_like else 1.5,
            min_value=0.0,
            max_value=10.0,
        )
        min_start_wait, max_start_wait = _env_int_range(
            "DATAPULSE_BROWSER_PRE_NAV_WAIT_MS_MIN",
            "DATAPULSE_BROWSER_PRE_NAV_WAIT_MS_MAX",
            350,
            1100,
            minimum=50,
            maximum=6000,
        )
        min_settle_wait, max_settle_wait = _env_int_range(
            "DATAPULSE_BROWSER_POST_NAV_WAIT_MS_MIN",
            "DATAPULSE_BROWSER_POST_NAV_WAIT_MS_MAX",
            900,
            2200,
            minimum=200,
            maximum=8000,
        )

        async def _run() -> ParseResult:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                await _throttle_requests(min_interval, interval_jitter)
                kwargs: dict[str, Any] = {}
                if storage_state and Path(storage_state).exists():
                    kwargs["storage_state"] = storage_state
                if _env_bool("DATAPULSE_BROWSER_USE_STEALTH_HEADERS", True):
                    locale = os.getenv("DATAPULSE_BROWSER_LOCALE", "zh-CN").strip()
                    if locale:
                        kwargs["locale"] = locale
                    timezone = os.getenv("DATAPULSE_BROWSER_TIMEZONE", "Asia/Shanghai").strip()
                    if timezone:
                        kwargs["timezone_id"] = timezone
                if _env_bool("DATAPULSE_BROWSER_RANDOMIZE_VIEWPORT", True):
                    kwargs["viewport"] = {
                        "width": random.randint(1180, 1440),
                        "height": random.randint(780, 980),
                    }
                if ua := os.getenv("DATAPULSE_BROWSER_USER_AGENT"):
                    kwargs["user_agent"] = ua

                context = await browser.new_context(**kwargs)
                page: Any = await context.new_page()
                try:
                    if human_like:
                        if _env_bool("DATAPULSE_BROWSER_DISABLE_WEBDRIVER", True):
                            await page.add_init_script(
                                """
                                Object.defineProperty(navigator, 'webdriver', {
                                    get: () => false
                                });
                                """
                            )
                        await page.add_init_script(
                            """
                            window.chrome = { runtime: {} };
                            """
                        )

                    await page.wait_for_timeout(_human_wait_ms(min_start_wait, max_start_wait))
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    if human_like:
                        await _simulate_human_page_read(page)
                        await _simulate_scroll(page, traffic_profile=traffic_profile)
                    else:
                        await page.wait_for_timeout(1200)
                    title = await page.title()
                    if human_like:
                        await page.wait_for_timeout(_human_wait_ms(min_settle_wait, max_settle_wait))
                    content = await page.evaluate(
                        """() => {
                        const selectors = [
                          'article .note-content',
                          '.note-content',
                          '.note-text',
                          'article',
                          'main',
                          '.content',
                          'body',
                        ];
                        for (const selector of selectors) {
                          const el = document.querySelector(selector);
                          if (el && typeof el.innerText === 'string' && el.innerText.trim()) {
                            return el.innerText;
                          }
                        }
                        return '';
                    }"""
                    )
                    return ParseResult(
                        url=url,
                        title=(title or "").strip()[:200],
                        content=clean_text(content or ""),
                        author="",
                        source_type=self.source_type,
                        tags=["playwright", "browser"],
                        confidence_flags=["browser-fallback"],
                        extra={"source": "playwright"},
                    )
                finally:
                    await context.close()
                    await browser.close()

        return run_sync(_run())
