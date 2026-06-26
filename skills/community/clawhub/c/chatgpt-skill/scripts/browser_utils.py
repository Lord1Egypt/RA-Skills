"""Browser utilities for chatgpt-skill."""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from patchright.sync_api import BrowserContext, Page, Playwright

from config import (
    ACCOUNT_CHOOSER_TEXT_HINTS,
    APP_READY_SELECTORS,
    BROWSER_ARGS,
    BROWSER_PROFILE_DIR,
    CHATGPT_ALT_URL,
    CHATGPT_BASE_URL,
    CHATGPT_PROXY_BYPASS_ENV,
    CHATGPT_PROXY_URL_ENV,
    LOGIN_TEXT_HINTS,
    LOGIN_URL_HINTS,
    NETWORK_ERROR_TEXT_HINTS,
    PAGE_LOAD_TIMEOUT_MS,
    SCREENSHOTS_DIR,
    STATE_FILE,
    UI_SHORT_TIMEOUT_MS,
    USER_AGENT,
    VERIFICATION_TEXT_HINTS,
)
from errors import ChatGPTSkillError
from storage import utcnow_iso


CONVERSATION_URL_RE = re.compile(r"/c/([0-9a-fA-F-]+)")
CONVERSATION_FIELD_RES = [
    re.compile(r'"conversation_id"\s*:\s*"([0-9a-fA-F-]+)"', re.IGNORECASE),
    re.compile(r'"conversationId"\s*:\s*"([0-9a-fA-F-]+)"', re.IGNORECASE),
    re.compile(r"conversation(?:_id|Id)[^0-9a-fA-F]+([0-9a-fA-F-]{36})", re.IGNORECASE),
    re.compile(r'"(?:clientThreadId|client_thread_id|threadId|thread_id)"\s*:\s*"(WEB:[0-9a-fA-F-]{36})"', re.IGNORECASE),
]
UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
CLIENT_THREAD_ID_RE = re.compile(r"\bWEB:[0-9a-fA-F-]{36}\b", re.IGNORECASE)


class BrowserFactory:
    DISPLAY_CANDIDATES = (":1", ":0")

    @staticmethod
    def _discover_proxy_url() -> Optional[str]:
        return (
            os.getenv(CHATGPT_PROXY_URL_ENV)
            or os.getenv("HTTPS_PROXY")
            or os.getenv("https_proxy")
            or os.getenv("HTTP_PROXY")
            or os.getenv("http_proxy")
            or os.getenv("ALL_PROXY")
            or os.getenv("all_proxy")
        )

    @staticmethod
    def _discover_display() -> Optional[str]:
        current = os.getenv("DISPLAY")
        if current:
            return current
        for display in BrowserFactory.DISPLAY_CANDIDATES:
            socket_path = Path(f"/tmp/.X11-unix/X{display.lstrip(':')}")
            if socket_path.exists():
                return display
        return None

    @staticmethod
    def recommended_headless(default: bool = True) -> bool:
        if os.getenv("CHATGPT_FORCE_HEADLESS") == "1":
            return True
        if os.getenv("CHATGPT_FORCE_HEADFUL") == "1":
            return False
        return BrowserFactory._discover_display() is None if default else False

    @staticmethod
    def _build_launch_env(headless: bool) -> Optional[dict]:
        if headless:
            return None
        display = BrowserFactory._discover_display()
        if not display:
            return None
        launch_env = os.environ.copy()
        launch_env["DISPLAY"] = display
        return launch_env

    @staticmethod
    def _get_proxy_settings() -> Tuple[Optional[dict], List[str]]:
        proxy_url = BrowserFactory._discover_proxy_url()
        if not proxy_url:
            return None, []

        parsed = urlparse(proxy_url)
        if not parsed.scheme or not parsed.hostname:
            raise ChatGPTSkillError("proxy_error", f"Invalid proxy URL: {proxy_url}")

        server = f"{parsed.scheme}://{parsed.hostname}"
        if parsed.port:
            server += f":{parsed.port}"

        proxy = {"server": server}
        if parsed.username:
            proxy["username"] = parsed.username
        if parsed.password:
            proxy["password"] = parsed.password

        bypass = os.getenv(CHATGPT_PROXY_BYPASS_ENV) or os.getenv("NO_PROXY") or os.getenv("no_proxy")
        if bypass:
            proxy["bypass"] = bypass

        return proxy, [f"--proxy-server={server}"]

    @staticmethod
    def proxy_diagnostics() -> Dict[str, Any]:
        proxy_url = BrowserFactory._discover_proxy_url()
        details: Dict[str, Any] = {
            "proxy_configured": bool(proxy_url),
            "proxy_env_vars_checked": [
                CHATGPT_PROXY_URL_ENV,
                "HTTPS_PROXY",
                "HTTP_PROXY",
                "ALL_PROXY",
            ],
        }
        if not proxy_url:
            details["hint"] = "Direct access to ChatGPT may be blocked on this machine. Set CHATGPT_PROXY_URL or a standard *_PROXY variable and retry."
            return details

        parsed = urlparse(proxy_url)
        server = f"{parsed.scheme}://{parsed.hostname}"
        if parsed.port:
            server += f":{parsed.port}"
        details["proxy_server"] = server
        return details

    @staticmethod
    def launch_persistent_context(
        playwright: Playwright,
        *,
        headless: bool = True,
        user_data_dir: str = str(BROWSER_PROFILE_DIR),
    ) -> BrowserContext:
        BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        proxy, proxy_args = BrowserFactory._get_proxy_settings()

        launch_kwargs = dict(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=headless,
            no_viewport=True,
            ignore_default_args=["--enable-automation"],
            user_agent=USER_AGENT,
            args=BROWSER_ARGS + proxy_args,
            proxy=proxy,
        )

        launch_env = BrowserFactory._build_launch_env(headless=headless)
        if launch_env is not None:
            launch_kwargs["env"] = launch_env

        try:
            context = playwright.chromium.launch_persistent_context(**launch_kwargs)
        except Exception as error:
            error_text = str(error)
            if "ProcessSingleton" not in error_text and "existing browser session" not in error_text:
                raise
            fallback_root = tempfile.mkdtemp(prefix="chatgpt-profile-")
            fallback_dir = os.path.join(fallback_root, "browser_profile")
            try:
                shutil.copytree(
                    user_data_dir,
                    fallback_dir,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("Singleton*", "DevToolsActivePort"),
                )
                for lock_name in ["SingletonLock", "SingletonCookie", "SingletonSocket", "DevToolsActivePort"]:
                    lock_path = os.path.join(fallback_dir, lock_name)
                    if os.path.exists(lock_path):
                        os.remove(lock_path)
            except Exception as copy_error:
                raise ChatGPTSkillError(
                    "profile_in_use",
                    "Browser profile is already in use and could not be cloned",
                    details={"cause": str(copy_error)},
                ) from copy_error
            launch_kwargs["user_data_dir"] = fallback_dir
            context = playwright.chromium.launch_persistent_context(**launch_kwargs)

        BrowserFactory._inject_storage_state(context)
        return context

    @staticmethod
    def _inject_storage_state(context: BrowserContext):
        if not STATE_FILE.exists():
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            cookies = payload.get("cookies") or []
            if cookies:
                context.add_cookies(cookies)
        except Exception:
            return


class StealthUtils:
    @staticmethod
    def random_delay(min_ms: int = 80, max_ms: int = 240):
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

    @staticmethod
    def random_mouse_movement(page: Page):
        try:
            for _ in range(random.randint(1, 3)):
                page.mouse.move(
                    random.randint(40, 900),
                    random.randint(40, 700),
                    steps=random.randint(2, 7),
                )
                StealthUtils.random_delay(40, 120)
        except Exception:
            return


def normalize_chatgpt_url(url: Optional[str]) -> str:
    if not url:
        return CHATGPT_BASE_URL
    normalized = url.strip()
    normalized = normalized.replace(CHATGPT_ALT_URL, CHATGPT_BASE_URL)
    if normalized.endswith("/") and normalized != CHATGPT_BASE_URL + "/":
        normalized = normalized.rstrip("/")
    return normalized


def conversation_url(conversation_id: str) -> str:
    if not is_url_addressable_conversation_id(conversation_id):
        raise ValueError(f"Conversation id is not URL-addressable: {conversation_id}")
    return f"{CHATGPT_BASE_URL}/c/{conversation_id}"


def is_client_thread_id(value: Optional[str]) -> bool:
    return bool(value and CLIENT_THREAD_ID_RE.fullmatch(value))


def is_url_addressable_conversation_id(value: Optional[str]) -> bool:
    return bool(value) and not is_client_thread_id(value)


def _normalize_uuid(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    match = UUID_RE.search(value)
    if not match:
        return None
    return match.group(0)


def extract_conversation_id(text: str, *, allow_bare_uuid: bool = False) -> Optional[str]:
    if not text:
        return None
    match = CONVERSATION_URL_RE.search(text)
    if match:
        return match.group(1)
    for pattern in CONVERSATION_FIELD_RES:
        match = pattern.search(text)
        if match:
            return match.group(1)
    match = CLIENT_THREAD_ID_RE.search(text)
    if match:
        return match.group(0)
    if allow_bare_uuid:
        return _normalize_uuid(text)
    return None


def extract_conversation_state(page: Page) -> Dict[str, Any]:
    final_url = page.url
    candidates: List[Dict[str, str]] = []
    seen_ids = set()

    def add_candidate(raw: Any, source: str):
        if raw is None:
            return
        if isinstance(raw, str):
            text = raw
        else:
            try:
                text = json.dumps(raw, ensure_ascii=False)
            except Exception:
                text = str(raw)
        allow_bare_uuid = source.startswith("data-attr:") or "history" in source.lower()
        conversation_id = extract_conversation_id(text, allow_bare_uuid=allow_bare_uuid)
        if not conversation_id or conversation_id in seen_ids:
            return
        seen_ids.add(conversation_id)
        candidates.append({"conversation_id": conversation_id, "source": source})

    add_candidate(final_url, "page.url")

    if not candidates:
        try:
            page_candidates = page.evaluate(
                """() => {
                    const items = [];
                    const push = (value, source) => {
                        if (value === null || value === undefined) return;
                        let text = "";
                        try {
                            text = typeof value === "string" ? value : JSON.stringify(value);
                        } catch {
                            try {
                                text = String(value);
                            } catch {
                                return;
                            }
                        }
                        if (!text) return;
                        if (text.length > 6000) {
                            text = text.slice(0, 6000);
                        }
                        items.push({ source, text });
                    };

                    push(window.location && window.location.href, "window.location.href");
                    try { push(window.history && window.history.state, "window.history.state"); } catch {}
                    try { push(window.navigation && window.navigation.currentEntry && window.navigation.currentEntry.url, "window.navigation.currentEntry.url"); } catch {}
                    try { push(window.__NEXT_DATA__, "window.__NEXT_DATA__"); } catch {}
                    try { push(document.querySelector("script#__NEXT_DATA__")?.textContent, "script#__NEXT_DATA__"); } catch {}
                    try {
                        for (const key of Object.keys(localStorage)) {
                            push({ key, value: localStorage.getItem(key) }, `localStorage:${key}`);
                        }
                    } catch {}
                    try {
                        for (const key of Object.keys(sessionStorage)) {
                            push({ key, value: sessionStorage.getItem(key) }, `sessionStorage:${key}`);
                        }
                    } catch {}
                    try {
                        document.querySelectorAll('a[href*="/c/"]').forEach((node, index) => push(node.href, `anchor:${index}`));
                    } catch {}
                    try {
                        performance.getEntriesByType('resource').slice(-80).forEach((entry, index) => push(entry.name, `resource:${index}`));
                    } catch {}
                    try {
                        document.querySelectorAll('[data-conversation-id],[data-conversationid]').forEach((node, index) => {
                            push(node.getAttribute('data-conversation-id') || node.getAttribute('data-conversationid'), `data-attr:${index}`);
                        });
                    } catch {}
                    return items;
                }"""
            )
        except Exception:
            page_candidates = []

        if isinstance(page_candidates, list):
            for item in page_candidates:
                if not isinstance(item, dict):
                    continue
                add_candidate(item.get("text"), item.get("source") or "page")

    primary = candidates[0] if candidates else {}
    return {
        "conversation_id": primary.get("conversation_id"),
        "source": primary.get("source"),
        "candidates": candidates,
        "final_url": final_url,
    }


def wait_for_any(page: Page, selectors: List[str], timeout_ms: int, state: str = "visible") -> Optional[str]:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        for selector in selectors:
            try:
                locator = page.locator(selector).first
                if locator.count() == 0:
                    continue
                if state == "visible":
                    if locator.is_visible(timeout=250):
                        return selector
                else:
                    page.wait_for_selector(selector, timeout=250, state=state)
                    return selector
            except Exception:
                continue
    return None


def read_page_text(page: Page, max_chars: int = 8000) -> str:
    try:
        text = page.locator("body").inner_text(timeout=1000)
        return text[:max_chars].lower()
    except Exception:
        return ""


def classify_page(page: Page) -> Dict[str, str]:
    url = (page.url or "").lower()
    body_text = read_page_text(page)

    if wait_for_any(page, APP_READY_SELECTORS, timeout_ms=UI_SHORT_TIMEOUT_MS):
        return {"status": "chat_ready", "final_url": page.url}

    if any(hint in body_text for hint in VERIFICATION_TEXT_HINTS):
        return {"status": "verification_required", "final_url": page.url}

    if any(hint in body_text for hint in ACCOUNT_CHOOSER_TEXT_HINTS):
        return {"status": "account_chooser", "final_url": page.url}

    if any(hint in url for hint in LOGIN_URL_HINTS) or any(hint in body_text for hint in LOGIN_TEXT_HINTS):
        return {"status": "login_page", "final_url": page.url}

    if any(hint in body_text for hint in NETWORK_ERROR_TEXT_HINTS):
        return {"status": "load_failed", "final_url": page.url}

    return {"status": "page_structure_changed", "final_url": page.url}


def wait_for_app_ready(page: Page, timeout_ms: int) -> Dict[str, str]:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        classification = classify_page(page)
        if classification["status"] == "chat_ready":
            return classification
        if classification["status"] in {"login_page", "account_chooser", "verification_required", "load_failed"}:
            return classification
        time.sleep(0.5)
    return classify_page(page)


def ensure_chat_ready(page: Page, *, timeout_ms: int) -> Dict[str, str]:
    classification = wait_for_app_ready(page, timeout_ms)
    status = classification["status"]
    if status == "chat_ready":
        return classification
    if status == "login_page":
        raise ChatGPTSkillError("login_redirected", "Redirected to ChatGPT login page", details=classification)
    if status == "account_chooser":
        raise ChatGPTSkillError("account_chooser", "Reached account chooser instead of ChatGPT app", details=classification)
    if status == "verification_required":
        raise ChatGPTSkillError("verification_required", "Human verification or two-step challenge is blocking access", details=classification)
    if status == "load_failed":
        raise ChatGPTSkillError("page_load_failed", "ChatGPT page failed to load", details=classification)
    raise ChatGPTSkillError("page_structure_changed", "Could not recognize the ChatGPT page structure", details=classification)


def goto_and_classify(page: Page, target_url: str) -> Dict[str, str]:
    normalized_url = normalize_chatgpt_url(target_url)
    last_error = None
    for attempt in range(1, 4):
        try:
            page.goto(normalized_url, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)
            time.sleep(1)
            return classify_page(page)
        except Exception as error:
            last_error = error
            if attempt < 3:
                time.sleep(attempt)
                continue
    raise ChatGPTSkillError(
        "network_error",
        "Failed to load ChatGPT page",
        details={
            "cause": str(last_error),
            "target_url": normalized_url,
            "attempts": 3,
            **BrowserFactory.proxy_diagnostics(),
        },
    ) from last_error


def take_debug_screenshot(page: Page, prefix: str) -> Optional[str]:
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}-{utcnow_iso().replace(':', '-')}.png"
    path = SCREENSHOTS_DIR / filename
    try:
        page.screenshot(path=str(path), full_page=True)
        return str(path)
    except Exception:
        return None
