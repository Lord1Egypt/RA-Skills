#!/usr/bin/env python3
"""
Bumble client via Remote Browser Service.
Per workspace/AGENTS.md: session bumble, https://bumble.com/app, SF location.
"""

from __future__ import annotations

import html as html_lib
import json
import mimetypes
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Optional

import requests

# Allow importing rbs_client from same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rbs_client import (
    action,
    create_session,
    element_bounds,
    ensure_session,
    find_element_by_text,
    get_bbox_by_text,
    get_page_content,
    html,
    navigate,
    screenshot,
    set_location,
    snapshot,
    text,
)

SESSION_ID = "bumble"
BUMBLE_APP_URL = "https://bumble.com/app"
BUMBLE_GET_STARTED = "https://bumble.com/get-started"
BUMBLE_CONNECTIONS_URL = "https://bumble.com/app/connections"
BUMBLE_BEELINE_URL = "https://bumble.com/app/beeline"
SF_LAT = 37.78891962482936
SF_LON = -122.41778467794562
CONTINUE_METHODS_SELECTORS = [
    "div.other-methods-button",
    "div.other-methods-button > span.other-methods-button-text",
    "span.other-methods-button-text",
]
USE_CELL_PHONE_SELECTORS = [
    "span.action.text-break-words",  # "Use cell phone number" text span
    "button.primary.button--transparent span.action",  # parent button
]
CONTINUE_BUTTON_SELECTORS = [
    "button[type=submit]",
    "button span.action.text-break-words",  # "Continue" after phone input
]
DEBUG_SCREENSHOT_PATH = Path(__file__).resolve().parent / "bumble_debug.jpg"
COMMON_UI_TEXT = {
    "bumble",
    "beeline",
    "continue",
    "change number",
    "quick sign in",
    "continue with apple",
    "continue with other methods",
    "continue with another methods",
    "use cell phone number",
    "welcome! how do you want to get started?",
    "next, please enter the 6-digit code we just sent you",
    "new matches",
    "messages",
    "search",
    "filters",
    "terms",
    "privacy policy",
}
OTP_INPUT_SELECTOR_TEMPLATE = '.code-field__digit:nth-child({index}) input'
OTP_SUBMIT_SELECTOR = 'button[type="submit"]'
# Sidebar row under a match: "Conversation expired yesterday" / "This match has expired" (connections list).
EXPIRED_CONVERSATION_RE = re.compile(
    r"(conversation\s+expired|this\s+match\s+has\s+expired)",
    re.IGNORECASE,
)
CONTACT_SELECTOR_TEMPLATE = '.contact[data-qa-role="contact"][data-qa-name="{name}"]'
MATCH_QUEUE_SELECTOR_TEMPLATE = '[data-qa-role="carousel-contact"][data-qa-name="{name}"]'
CHAT_INPUT_SELECTOR = '[data-qa-role="chat-input"] textarea'
CHAT_SEND_SELECTOR = "button.message-field__send"
# Chat header sandwich / kebab (vertical dots): opens Unmatch and Block and report.
CHAT_SANDWICH_MENU_SELECTORS = [
    'div.messages-header__menu-section > div.messages-header__menu-item[role="button"]:first-of-type',
    'div.messages-header__menu-item[role="button"]:has([data-qa-icon-name="generic-menu"])',
    '.messages-header__menu [data-qa-icon-name="generic-menu"]',
]
# First dropdown row under that menu is Unmatch on Bumble web.
CHAT_UNMATCH_OPTION_SELECTORS = [
    'div.messages-header__menu div.dropdown div.options div.option[data-qa-role="option"]:first-of-type',
    'div.messages-header__menu .dropdown .options > .option:first-of-type',
]
CHAT_OVERFLOW_MENU_SELECTORS = [
    *CHAT_SANDWICH_MENU_SELECTORS,
    'button[data-qa-role="conversation-actions-button"]',
    'button[data-qa-role="chat-actions-button"]',
    '[data-qa-role="conversation-header-menu"]',
    '[data-qa-role="chat-menu-button"]',
    "aside.page__chat header button[aria-label*='More']",
    "header.page__header button[aria-label*='More']",
    'button[aria-label*="More options"]',
    'button[aria-label*="more options"]',
]
PROFILE_PHOTO_SELECTOR = "aside.page__profile img.profile__photo"
_OVERFLOW_MENU_BUTTON_NAME_RE = re.compile(
    r"(more\s+options|open\s+menu|conversation\s+actions|chat\s+actions|^\s*menu\s*$|^\.\.\.\s*$)",
    re.I,
)
BADGE_KEY_LABELS = {
    "height": "Height",
    "exercise": "Exercise",
    "education": "Education",
    "drinking": "Drinking",
    "smoking": "Smoking",
    "cannabis": "Cannabis",
    "intentions": "Intentions",
    "familyplans": "Family plans",
    "starsign": "Star sign",
    "politics": "Politics",
    "religion": "Religion",
    "pets": "Pets",
    "languages": "Languages",
    "children": "Children",
}


def _normalize_phone_digits(raw: str) -> str:
    """Strip to digits; if 11 digits starting with 1, drop the leading 1 (US +1)."""
    digits = re.sub(r"\D", "", (raw or "").strip())
    if len(digits) == 11 and digits.startswith("1"):
        return digits[1:]
    return digits


def _pause() -> None:
    """Short 1-4 second jitter between actions so the page can settle and rate-limits stay relaxed."""
    time.sleep(random.uniform(1, 4))


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _looks_like_name(value: str) -> bool:
    candidate = _normalize_space(value)
    if not candidate:
        return False
    lower = candidate.lower()
    if lower in COMMON_UI_TEXT:
        return False
    if any(ch.isdigit() for ch in candidate):
        return False
    if len(candidate) > 32 or len(candidate) < 2:
        return False
    if "http" in lower or "@" in candidate:
        return False
    words = candidate.split()
    if len(words) > 3:
        return False
    return all(re.fullmatch(r"[A-Z][A-Za-z'\-]*", word) for word in words)


def _get_interactive_nodes(*, limit: int = 50) -> list[dict[str, Any]]:
    resp = snapshot(SESSION_ID, filter="interactive")
    if resp.status_code != 200:
        return []
    try:
        return (resp.json().get("nodes") or [])[:limit]
    except Exception:
        return []


def _get_html() -> str:
    resp = html(SESSION_ID)
    if resp.status_code != 200:
        return ""
    return resp.text


def _otp_submit_enabled() -> bool:
    page_html = _get_html()
    if not page_html:
        return False
    marker = '<button class="button'
    idx = page_html.find('type="submit"')
    if idx == -1:
        return False
    start = page_html.rfind(marker, 0, idx)
    snippet = page_html[start: idx + 200] if start != -1 else page_html[max(0, idx - 400): idx + 200]
    return 'disabled=""' not in snippet and "is-disabled" not in snippet


def get_state(content: Optional[dict[str, str]] = None) -> str:
    """Classify the visible Bumble state for local debugging."""
    content = content or get_content()
    if not content:
        return "unavailable"
    url = (content.get("url") or "").lower()
    text_content = (content.get("text") or "").lower()
    if "not a robot" in text_content or "unusual activity on your account" in text_content or "try different captcha" in text_content:
        return "captcha_challenge"
    if "confirm-phone" in url or "6-digit code" in text_content:
        return "awaiting_sms_code"
    if "/registration/passkey" in url:
        return "passkey_prompt"
    if "get-started" in url or "how do you want to get started" in text_content:
        return "logged_out"
    if "/app/beeline" in url:
        return "beeline"
    if "/app/connections" in url:
        return "connections"
    if "/app" in url and any(token in text_content for token in ("feedback", "edit profile", "filters", "match queue")):
        return "logged_in"
    if "/app/" in url:
        return "logged_in"
    return "unknown"


def open_connections() -> Optional[dict[str, str]]:
    """Navigate to Bumble connections and return current content."""
    if not resume_existing_session():
        return None
    content = get_content()
    state = get_state(content)
    if state == "passkey_prompt":
        for _ in range(2):
            if not dismiss_passkey_prompt():
                break
            _pause()
            time.sleep(1.5)
            content = get_content()
            if get_state(content) != "passkey_prompt":
                break
        state = get_state(content)
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        return content
    url = (content or {}).get("url", "").lower()
    if "/app/connections" in url:
        return content
    if not url or url in ("about:blank", "data:,"):
        nav = navigate(SESSION_ID, BUMBLE_APP_URL, timeout=30)
        if nav.status_code != 200:
            print(f"Navigate to app failed: {nav.status_code}")
            return None
        _pause()
    nav = navigate(SESSION_ID, BUMBLE_CONNECTIONS_URL, timeout=30)
    if nav.status_code != 200:
        print(f"Navigate to connections failed: {nav.status_code}")
        return None
    _pause()
    return get_content()


def open_beeline() -> Optional[dict[str, str]]:
    """Navigate to Bumble Beeline / likes and return current content."""
    if not resume_existing_session():
        return None
    content = get_content()
    state = get_state(content)
    if state == "passkey_prompt":
        for _ in range(2):
            if not dismiss_passkey_prompt():
                break
            _pause()
            time.sleep(1.5)
            content = get_content()
            if get_state(content) != "passkey_prompt":
                break
        state = get_state(content)
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        return content
    url = (content or {}).get("url", "").lower()
    if "/app/beeline" in url:
        return content
    if not url or url in ("about:blank", "data:,"):
        nav = navigate(SESSION_ID, BUMBLE_APP_URL, timeout=30)
        if nav.status_code != 200:
            print(f"Navigate to app failed: {nav.status_code}")
            return None
        _pause()
    nav = navigate(SESSION_ID, BUMBLE_BEELINE_URL, timeout=30)
    if nav.status_code != 200:
        print(f"Navigate to beeline failed: {nav.status_code}")
        return None
    _pause()
    return get_content()


def extract_visible_match_names(content: Optional[dict[str, str]] = None) -> list[str]:
    """Best-effort extraction of visible match names from text + interactive nodes."""
    content = content or get_content()
    candidates: list[str] = []
    if content:
        for line in (content.get("text") or "").splitlines():
            item = _normalize_space(line)
            if _looks_like_name(item):
                candidates.append(item)
    for node in _get_interactive_nodes():
        item = _normalize_space(str(node.get("name") or ""))
        if _looks_like_name(item):
            candidates.append(item)

    seen: set[str] = set()
    result: list[str] = []
    for item in candidates:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _sidebar_segment_from_raw_text(raw_text: str) -> list[str]:
    """Lines belonging to the connections sidebar (between 'Conversations' and settings/spotlight)."""
    lines = [_normalize_space(line) for line in raw_text.splitlines()]
    lines = [line for line in lines if line]

    start_idx = 0
    for i, line in enumerate(lines):
        if line == "Conversations" or line.endswith("Conversations"):
            start_idx = i + 1
            break

    stop_markers = {"Activate Spotlight", "Bumble Premium is active", "Edit profile", "Settings"}
    segment: list[str] = []
    for line in lines[start_idx:]:
        if any(line.startswith(marker) for marker in stop_markers):
            break
        segment.append(line)
    return segment


def extract_matches_from_raw_text(raw_text: str) -> list[dict[str, Any]]:
    """
    Extract matches from connections sidebar text with expired vs active flag.
    Expired rows show copy like 'Conversation expired yesterday' under the name.
    """
    segment = _sidebar_segment_from_raw_text(raw_text)
    skip_lines = {"(Recent)", "Your move", "Their move", "Expired", "Archived", "Recent"}

    i = 0
    rows: list[dict[str, Any]] = []
    while i < len(segment):
        line = segment[i]
        if line in skip_lines:
            i += 1
            continue
        if not _looks_like_name(line):
            i += 1
            continue
        name = line
        i += 1
        expired = False
        while i < len(segment):
            nxt = segment[i]
            if nxt in skip_lines:
                i += 1
                continue
            if _looks_like_name(nxt):
                break
            if EXPIRED_CONVERSATION_RE.search(nxt):
                expired = True
            i += 1
        rows.append({"name": name, "expired": expired})

    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = str(row["name"]).lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def extract_match_names_from_raw_text(raw_text: str) -> list[str]:
    """Names only (same order as extract_matches_from_raw_text)."""
    return [m["name"] for m in extract_matches_from_raw_text(raw_text)]


def _conversations_sidebar_html_segment(page_html: str) -> str:
    """HTML for the conversations list column (excludes main chat pane when possible)."""
    if not page_html:
        return ""
    key = 'data-qa-role="conversations-tab-section"'
    start = page_html.find(key)
    if start == -1:
        return ""
    end = len(page_html)
    for marker in (
        'class="messages-header"',
        'class="page__chat"',
    ):
        pos = page_html.find(marker, start + len(key))
        if pos != -1 and pos < end:
            end = pos
    return page_html[start:end]


def extract_conversation_contacts_from_html(page_html: str) -> list[dict[str, Any]]:
    """
    Sidebar contacts from DOM (includes expired threads that readability text may omit).
    Each row: name + conversation_expired (bool).
    """
    seg = _conversations_sidebar_html_segment(page_html)
    if not seg:
        return []
    rows: list[dict[str, Any]] = []
    anchor = 'data-qa-role="contact"'
    pos = 0
    while True:
        i = seg.find(anchor, pos)
        if i == -1:
            break
        chunk = seg[i : i + 1800]
        nm = re.search(r'data-qa-name="([^"]+)"', chunk)
        if not nm:
            pos = i + len(anchor)
            continue
        name = html_lib.unescape(nm.group(1).strip())
        low = chunk.lower()
        expired = False
        if EXPIRED_CONVERSATION_RE.search(chunk):
            expired = True
        elif re.search(
            r"contact--expired|conversation-expired|expiration-status-expired|chat-expired",
            low,
        ):
            expired = True
        rows.append({"name": name, "conversation_expired": expired})
        pos = i + len(anchor)
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        key = str(row["name"]).casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def extract_match_queue_names_from_html(page_html: str) -> list[str]:
    """Extract Match Queue names from the connections HTML carousel."""
    if not page_html:
        return []
    start = page_html.find('match-queue-tab-section-content')
    if start == -1:
        return []
    end = page_html.find('conversations-tab-section', start)
    if end == -1:
        end = len(page_html)
    segment = page_html[start:end]
    pattern = re.compile(
        r'data-qa-role="carousel-contact"[^>]*data-qa-name="([^"]+)"'
        r'|data-qa-name="([^"]+)"[^>]*data-qa-role="carousel-contact"'
    )
    names: list[str] = []
    seen: set[str] = set()
    for match in pattern.finditer(segment):
        name = html_lib.unescape(match.group(1) or match.group(2) or "").strip()
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        names.append(name)
    return names


def collect_all_match_entries(
    raw_text: str, page_html: str
) -> list[dict[str, Any]]:
    """Merged list: conversations (DOM + text, with expired flags) + Match Queue names."""
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    text_rows = extract_matches_from_raw_text(raw_text)
    text_by_key = {r["name"].casefold(): r for r in text_rows}

    for row in extract_conversation_contacts_from_html(page_html):
        key = row["name"].casefold()
        if key in seen:
            continue
        seen.add(key)
        expired_flag = bool(row.get("conversation_expired"))
        if text_by_key.get(key, {}).get("expired"):
            expired_flag = True
        entries.append(
            {
                "name": row["name"],
                "source": "conversations",
                "conversation_expired": expired_flag,
                "expired": expired_flag,
            }
        )

    for row in text_rows:
        key = row["name"].casefold()
        if key in seen:
            continue
        seen.add(key)
        expired_flag = bool(row.get("expired", False))
        entries.append(
            {
                "name": row["name"],
                "source": "conversations",
                "conversation_expired": expired_flag,
                "expired": expired_flag,
            }
        )

    for name in extract_match_queue_names_from_html(page_html):
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            {
                "name": name,
                "source": "queue",
                "conversation_expired": None,
                "expired": False,
            }
        )
    return entries


def _beeline_segment_from_raw_text(raw_text: str) -> list[str]:
    """Lines likely belonging to the Beeline / admirers view."""
    lines = [_normalize_space(line) for line in raw_text.splitlines()]
    lines = [line for line in lines if line]

    marker_idx: Optional[int] = None
    for i, line in enumerate(lines):
        lower = line.lower()
        if (
            "liked you" in lower
            or "likes you" in lower
            or "admirers" in lower
            or lower == "beeline"
        ):
            marker_idx = i
            break
    if marker_idx is None:
        return []

    stop_markers = {
        "Conversations",
        "Messages",
        "Activate Spotlight",
        "Bumble Premium is active",
        "Edit profile",
        "Settings",
    }
    segment: list[str] = []
    for line in lines[marker_idx + 1 :]:
        if any(line.startswith(marker) for marker in stop_markers):
            break
        segment.append(line)
    return segment


def extract_likes_from_raw_text(raw_text: str) -> list[dict[str, Any]]:
    """Best-effort extraction of visible admirer names from Beeline text."""
    segment = _beeline_segment_from_raw_text(raw_text)
    if not segment:
        return []

    likes: list[dict[str, Any]] = []
    seen: set[str] = set()

    # On the live Beeline page, names are rendered as alternating lines:
    #   Tina
    #   , 39
    #   Deepika
    #   , 38
    # Prefer this pattern because it avoids false positives like "Enable".
    for idx, line in enumerate(segment[:-1]):
        next_line = segment[idx + 1]
        if not re.fullmatch(r",\s*\d{1,2}", next_line):
            continue
        candidate = _normalize_space(line)
        if len(candidate) < 2 or len(candidate) > 32:
            continue
        if any(ch.isdigit() for ch in candidate):
            continue
        lower = candidate.casefold()
        if lower in seen or lower in COMMON_UI_TEXT:
            continue
        seen.add(lower)
        likes.append({"name": candidate, "visible": True})

    if likes:
        return likes

    for line in segment:
        lower = line.casefold()
        if lower.startswith("enable desktop notifications"):
            break
        if line in {"Enable", "Send", "Back to meeting new people", "Conversations", "Liked You", "Your Beeline"}:
            continue
        if not _looks_like_name(line):
            continue
        key = lower
        if key in seen:
            continue
        seen.add(key)
        likes.append({"name": line, "visible": True})
    return likes


def extract_like_count(raw_text: str) -> Optional[int]:
    """Extract total admirer count when Bumble exposes it in text."""
    source = _normalize_space(raw_text)
    if not source:
        return None
    if "no one has liked you yet" in source.lower() or "you don't have any admirers yet" in source.lower():
        return 0
    patterns = [
        r"(\d+)\s+(?:people\s+)?(?:have\s+)?liked you",
        r"(\d+)\s+admirers?",
        r"liked you\s*[:\-]?\s*(\d+)",
        r"admirers?\s*[:\-]?\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, source, flags=re.I)
        if match:
            try:
                return int(match.group(1))
            except Exception:
                continue
    return None


def beeline_premium_required(raw_text: str, page_html: str = "") -> bool:
    """True when Beeline appears to be gated behind a premium upsell."""
    source = f"{raw_text}\n{page_html}".lower()
    tokens = (
        "see who likes you",
        "unlock your admirers",
        "unlock beeline",
        "upgrade to premium",
        "get premium",
        "bumble premium",
        "admirers are blurred",
        "liked you is part of premium",
    )
    return any(token in source for token in tokens)


def extract_visible_like_names(content: Optional[dict[str, str]] = None) -> list[str]:
    """Fallback extraction of visible admirer names from Beeline text + interactive nodes."""
    content = content or get_content()
    candidates: list[str] = []
    if content:
        for line in (content.get("text") or "").splitlines():
            item = _normalize_space(line)
            if _looks_like_name(item):
                candidates.append(item)
    for node in _get_interactive_nodes():
        item = _normalize_space(str(node.get("name") or ""))
        if _looks_like_name(item):
            candidates.append(item)

    seen: set[str] = set()
    result: list[str] = []
    for item in candidates:
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _contact_selector(match_name: str) -> str:
    escaped = match_name.replace("\\", "\\\\").replace('"', '\\"')
    return CONTACT_SELECTOR_TEMPLATE.format(name=escaped)


def _match_queue_selector(match_name: str) -> str:
    escaped = match_name.replace("\\", "\\\\").replace('"', '\\"')
    return MATCH_QUEUE_SELECTOR_TEMPLATE.format(name=escaped)


def _active_profile_name(page_html: Optional[str] = None) -> str:
    page_html = page_html or _get_html()
    if not page_html:
        return ""
    match = re.search(r'class="profile__name"[^>]* title="([^"]+)"', page_html)
    if match:
        return _normalize_space(html_lib.unescape(match.group(1)))
    match = re.search(
        r'<div class="profile__name"[^>]*>.*?<div class="header-1 text-ellipsis">(.*?)</div>',
        page_html,
        flags=re.S,
    )
    if not match:
        return ""
    return _normalize_space(html_lib.unescape(re.sub(r"<[^>]+>", "", match.group(1))))


def _wait_for_active_match(match_name: str, *, attempts: int = 4, delay_seconds: float = 1.0) -> bool:
    target = _normalize_space(match_name).casefold()
    for attempt in range(attempts):
        active = _active_profile_name()
        if active.casefold() == target:
            return True
        if attempt < attempts - 1:
            time.sleep(delay_seconds)
    return False


def open_match(match_name: str) -> bool:
    """Open a specific Bumble match from the connections list."""
    content = open_connections()
    if not content:
        return False
    state = get_state(content)
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        return False

    if _wait_for_active_match(match_name, attempts=1, delay_seconds=0):
        return True

    selectors = [_contact_selector(match_name), _match_queue_selector(match_name)]
    for selector in selectors:
        bounds_resp = element_bounds(SESSION_ID, selector=selector)
        if bounds_resp.status_code == 200:
            try:
                box = bounds_resp.json()
                x = int(box["x"] + box["width"] / 2)
                y = int(box["y"] + box["height"] / 2)
            except Exception:
                x = y = None
            if x is not None:
                for kind in ("tap", "click"):
                    resp = action(SESSION_ID, kind=kind, x=x, y=y)
                    if resp.status_code == 200:
                        _pause()
                        if _wait_for_active_match(match_name):
                            return True

        for kind in ("tap", "click"):
            resp = action(SESSION_ID, kind=kind, selector=selector)
            if resp.status_code == 200:
                _pause()
                if _wait_for_active_match(match_name):
                    return True
    return False


def extract_messages_from_raw_text(raw_text: str, match_name: str) -> list[str]:
    """Extract visible conversation messages for the selected match."""
    lines = [_normalize_space(line) for line in raw_text.splitlines()]
    lines = [line for line in lines if line]

    start_idx = 0
    for i, line in enumerate(lines):
        if line == "Log out":
            start_idx = i + 1
            break
    if start_idx >= len(lines):
        return []

    segment = lines[start_idx:]
    if segment and segment[0] == match_name:
        segment = segment[1:]

    stop_idx = len(segment)
    for i, line in enumerate(segment):
        if line == match_name and i + 1 < len(segment) and segment[i + 1].startswith(","):
            stop_idx = i
            break
        if line == f"About {match_name}" or line.startswith(f"{match_name}’s location") or line.startswith(f"{match_name}'s location"):
            stop_idx = i
            break
        if line.startswith("Enable desktop notifications"):
            stop_idx = min(stop_idx, i)
            break

    messages = segment[:stop_idx]
    return [line for line in messages if line and line != match_name]


def extract_message_objects_from_html(page_html: str, match_name: str) -> list[dict[str, str]]:
    """Extract visible conversation messages with direction from selected chat HTML."""
    match = re.search(
        r'<div class="messages-list__conversation">(.*?)<div class="messages-list__conversation-pusher">',
        page_html,
        flags=re.S,
    )
    if not match:
        return []

    conversation_html = match.group(1)
    token_pattern = re.compile(
        r'<div class="message-group-date"><div class="p-3 text-align-center text-color-gray-dark">(.*?)</div></div>'
        r'|<div class="message(?: [^"]*)? message--(in|out)(?: [^"]*)?">.*?<div class="message-bubble__text" dir="auto"><div class="p-1 text-break-words"><span>(.*?)</span></div></div>',
        flags=re.S,
    )

    current_date = ""
    messages: list[dict[str, str]] = []
    for date_html, direction, text_html in token_pattern.findall(conversation_html):
        if date_html:
            current_date = html_lib.unescape(re.sub(r"\s+", " ", date_html.replace("&nbsp;", " ")).strip())
            continue
        if not text_html or not direction:
            continue
        text_value = html_lib.unescape(re.sub(r"\s+", " ", text_html.replace("<br>", "\n").replace("<br/>", "\n")).strip())
        if not text_value:
            continue
        author = "them" if direction == "in" else "me"
        item = {"author": author, "text": text_value}
        if current_date:
            item["date"] = current_date
        messages.append(item)
    return messages


def _extract_chat_draft(page_html: str) -> str:
    match = re.search(
        r'<div class="textarea[^"]*" data-qa-role="chat-input">.*?<textarea class="textarea__input"[^>]*>(.*?)</textarea>',
        page_html,
        flags=re.S,
    )
    if not match:
        return ""
    draft_html = match.group(1)
    return html_lib.unescape(draft_html.replace("\r", "")).strip()


def _chat_send_enabled(page_html: str) -> bool:
    match = re.search(r'<button class="message-field__send"[^>]*>', page_html)
    if not match:
        return False
    button_html = match.group(0)
    return 'disabled=""' not in button_html and "is-disabled" not in button_html


def _tap_selector_center(selector: str) -> bool:
    bounds_resp = element_bounds(SESSION_ID, selector=selector)
    if bounds_resp.status_code != 200:
        return False
    try:
        box = bounds_resp.json()
        x = int(box["x"] + box["width"] / 2)
        y = int(box["y"] + box["height"] / 2)
    except Exception:
        return False
    for kind in ("tap", "click"):
        resp = action(SESSION_ID, kind=kind, x=x, y=y)
        if resp.status_code == 200:
            return True
    return False


def _profile_photo_bounds() -> Optional[dict[str, float]]:
    bounds_resp = element_bounds(SESSION_ID, selector=PROFILE_PHOTO_SELECTOR)
    if bounds_resp.status_code != 200:
        return None
    try:
        box = bounds_resp.json()
    except Exception:
        return None
    if not box.get("width") or not box.get("height"):
        return None
    return box


def _extract_profile_html(page_html: str) -> str:
    start = page_html.find('<aside class="page__profile')
    if start == -1:
        return ""
    end = page_html.find("</aside>", start)
    if end == -1:
        end = len(page_html)
    return page_html[start:end]


def _clean_html_text(value: str) -> str:
    text_value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    text_value = re.sub(r"<[^>]+>", "", text_value)
    text_value = html_lib.unescape(text_value)
    text_value = text_value.replace("\xa0", " ")
    text_value = re.sub(r"[ \t]+", " ", text_value)
    text_value = re.sub(r" *\n *", "\n", text_value)
    return text_value.strip()


def _badge_key_and_label(icon_src: str) -> tuple[str, str]:
    match = re.search(r'ic_badge_profileChips_[^_]+_([A-Za-z]+)v2\.png', icon_src, flags=re.I)
    if not match:
        return ("unknown", "Unknown")
    token = match.group(1)
    normalized = re.sub(r"[^a-z]", "", token.lower())
    label = BADGE_KEY_LABELS.get(normalized)
    if label:
        return (normalized, label)
    fallback = re.sub(r"(?<!^)([A-Z])", r" \1", token).replace("_", " ").strip().title()
    fallback = fallback or "Unknown"
    return (normalized or "unknown", fallback)


def _extract_profile_badges(profile_html: str) -> list[dict[str, str]]:
    badge_list_match = re.search(r'<ul class="profile__badges">(.*?)</ul>', profile_html, flags=re.S)
    if not badge_list_match:
        return []
    badge_list_html = badge_list_match.group(1)
    badge_pattern = re.compile(
        r'<li class="profile__badge">.*?<img class="pill__image" src="([^"]+)" alt="([^"]*)">.*?<div class="pill__title" dir="auto"><div class="p-3 text-ellipsis font-weight-medium">(.*?)</div>',
        flags=re.S,
    )
    badges: list[dict[str, str]] = []
    for icon_src_html, alt_html, title_html in badge_pattern.findall(badge_list_html):
        icon_src = html_lib.unescape(icon_src_html)
        title = _clean_html_text(title_html) or _clean_html_text(alt_html)
        if not title:
            continue
        key, label = _badge_key_and_label(icon_src)
        badges.append(
            {
                "key": key,
                "label": label,
                "value": title,
            }
        )
    return badges


def extract_profile_json_from_html(page_html: str) -> dict[str, Any]:
    """Extract structured Bumble profile data from the right-side profile pane."""
    profile_html = _extract_profile_html(page_html)
    if not profile_html:
        return {}

    result: dict[str, Any] = {}

    name_match = re.search(r'class="profile__name"[^>]* title="([^"]+)"', profile_html)
    if name_match:
        result["name"] = _clean_html_text(name_match.group(1))

    age_match = re.search(
        r'<div class="profile__age"><div class="header-1">.*?<span class="comma">,</span>\s*([^<]+)</div>',
        profile_html,
        flags=re.S,
    )
    if age_match:
        age_text = _clean_html_text(age_match.group(1))
        if age_text.isdigit():
            result["age"] = int(age_text)
        elif age_text:
            result["age"] = age_text

    result["verified"] = "badge-feature-verification" in profile_html

    education_match = re.search(r'<div class="profile__business[^"]*"[^>]*><div class="p-2 text-ellipsis">(.*?)</div>', profile_html, flags=re.S)
    if education_match:
        education = _clean_html_text(education_match.group(1))
        if education:
            result["education"] = education

    about_match = re.search(r'<div class="profile__about" dir="auto"><div class="p-1">(.*?)</div></div>', profile_html, flags=re.S)
    if about_match:
        about = _clean_html_text(about_match.group(1))
        if about:
            result["about"] = about

    badges = _extract_profile_badges(profile_html)
    if badges:
        result["badges"] = badges

    prompt_answers: list[dict[str, str]] = []
    answer_pattern = re.compile(
        r'<div class="profile__section profile__section--answer"><div class="profile-answer"><div class="profile-answer__title"><h3 class="p-2 font-weight-medium">(.*?)</h3></div><div class="profile-answer__text" dir="auto"><p class="header-2">(.*?)</p></div></div></div>',
        flags=re.S,
    )
    for question_html, answer_html in answer_pattern.findall(profile_html):
        question = _clean_html_text(question_html)
        answer = _clean_html_text(answer_html)
        if question and answer:
            prompt_answers.append({"question": question, "answer": answer})
    if prompt_answers:
        result["prompt_answers"] = prompt_answers

    location_match = re.search(
        r'<div class="profile__section profile__section--text profile__section--location">(.*?)</section></div></div>',
        profile_html,
        flags=re.S,
    )
    if location_match:
        location_html = location_match.group(1)
        location: dict[str, str] = {}
        title_match = re.search(r'<span>([^<]+’s location|[^<]+\'s location)</span>', location_html)
        town_match = re.search(r'<div class="location-widget__town"[^>]*><span class="header-2 text-color-black">(.*?)</span>', location_html, flags=re.S)
        distance_match = re.search(r'<div class="location-widget__distance"><span class="header-2 text-color-black">(.*?)</span>', location_html, flags=re.S)
        origin_match = re.search(r'<div class="p-3 text-ellipsis font-weight-medium">(.*?)</div>', location_html, flags=re.S)
        if title_match:
            location["title"] = _clean_html_text(title_match.group(1))
        if town_match:
            location["town"] = _clean_html_text(town_match.group(1))
        if distance_match:
            location["distance"] = _clean_html_text(distance_match.group(1))
        if origin_match:
            location["origin"] = _clean_html_text(origin_match.group(1))
        if location:
            result["location"] = location

    result["photo_count"] = len(re.findall(r'<img class="profile__photo" src="', profile_html))
    return result


def _extract_profile_photo_urls(page_html: str) -> list[str]:
    profile_html = _extract_profile_html(page_html)
    if not profile_html:
        return []
    matches = re.findall(r'<img class="profile__photo" src="([^"]+)"', profile_html)
    urls: list[str] = []
    seen: set[str] = set()
    for raw_url in matches:
        url = html_lib.unescape(raw_url)
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def _advance_profile_photo() -> bool:
    box = _profile_photo_bounds()
    if not box:
        return False
    x = int(box["x"] + box["width"] * 0.82)
    y = int(box["y"] + box["height"] * 0.5)
    for kind in ("tap", "click"):
        resp = action(SESSION_ID, kind=kind, x=x, y=y)
        if resp.status_code == 200:
            return True
    return False


def _reset_match_view(match_name: str) -> None:
    """Best-effort reset back to the normal match thread view."""
    try:
        open_match(match_name)
    except Exception:
        pass


def _download_photo(url: str, destination_dir: Path, stem: str, index: int) -> str:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    suffix = mimetypes.guess_extension(content_type) or ".jpg"
    if suffix == ".jpe":
        suffix = ".jpg"
    filename = f"{stem}_{index:02d}{suffix}"
    path = destination_dir / filename
    path.write_bytes(response.content)
    return str(path)


def save_profile_photos(match_name: str, output_dir: str) -> bool:
    """Save visible Bumble profile photos for a match into a directory."""
    destination_dir = Path(output_dir).expanduser()

    content = open_connections()
    if not content:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": "Failed to open Bumble connections.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not open_match(match_name):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": f"Failed to open Bumble match: {match_name}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    current = get_content()
    current_state = get_state(current)
    current_url = (current or {}).get("url", "")
    if current_state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": current_state,
                    "url": current_url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    photo_urls: list[str] = []
    seen_urls: set[str] = set()

    _tap_selector_center(PROFILE_PHOTO_SELECTOR)
    time.sleep(1)

    stagnant_rounds = 0
    for _ in range(8):
        page_html = _get_html()
        round_urls = _extract_profile_photo_urls(page_html)
        added = False
        for photo_url in round_urls:
            if photo_url in seen_urls:
                continue
            seen_urls.add(photo_url)
            photo_urls.append(photo_url)
            added = True
        if added:
            stagnant_rounds = 0
        else:
            stagnant_rounds += 1
        if stagnant_rounds >= 2 and photo_urls:
            break
        if not _advance_profile_photo():
            break
        time.sleep(1)

    if not photo_urls:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": get_state(get_content()),
                    "url": (get_content() or {}).get("url", ""),
                    "error": "No profile photos were detected for this match.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    destination_dir.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^a-z0-9]+", "_", match_name.lower()).strip("_") or "match"
    saved_paths: list[str] = []
    try:
        for index, photo_url in enumerate(photo_urls, start=1):
            saved_paths.append(_download_photo(photo_url, destination_dir, stem, index))
    except requests.RequestException as exc:
        _reset_match_view(match_name)
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": get_state(get_content()),
                    "url": (get_content() or {}).get("url", ""),
                    "directory": str(destination_dir),
                    "saved_paths": saved_paths,
                    "error": f"Failed to download Bumble photo: {exc}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    _reset_match_view(match_name)
    print(
        json.dumps(
            {
                "ok": True,
                "match": match_name,
                "state": get_state(get_content()),
                "url": (get_content() or {}).get("url", ""),
                "directory": str(destination_dir),
                "photos": saved_paths,
                "source_urls": photo_urls,
                "count": len(saved_paths),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def get_profile(match_name: str) -> bool:
    """Open a Bumble match and return structured profile JSON without image URLs."""
    content = open_connections()
    if not content:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": "Failed to open Bumble connections.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    # Verify the requested name is actually one of the current matches before
    # opening, so a stale right-side profile panel cannot be mistaken for a match.
    raw_content = get_page_content(SESSION_ID, mode="raw")
    raw_text = (raw_content or {}).get("text", "") or ""
    page_html = _get_html()
    match_names = [m["name"] for m in collect_all_match_entries(raw_text, page_html)]
    target = _normalize_space(match_name).casefold()
    if target not in {n.casefold() for n in match_names}:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": f"Match '{match_name}' is not in the current Bumble matches list.",
                    "available_matches": match_names,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not open_match(match_name):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": f"Failed to open Bumble match: {match_name}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    current = get_content()
    current_state = get_state(current)
    current_url = (current or {}).get("url", "")
    if current_state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": current_state,
                    "url": current_url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    profile = extract_profile_json_from_html(_get_html())
    active_name = _active_profile_name()
    if not profile or active_name.casefold() != _normalize_space(match_name).casefold():
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": current_state,
                    "url": current_url,
                    "error": "Failed to extract Bumble profile JSON for the requested match.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    print(
        json.dumps(
            {
                "ok": True,
                "match": match_name,
                "state": current_state,
                "url": current_url,
                "profile": profile,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def send_message(match_name: str, message: str) -> bool:
    """Open a Bumble match, send a message, and return JSON."""
    normalized_message = message.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized_message:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": "Message must not be empty.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    content = open_connections()
    if not content:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": "Failed to open Bumble connections.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not open_match(match_name):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": f"Failed to open Bumble match: {match_name}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    content = get_content()
    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    page_html = _get_html()
    existing_draft = _extract_chat_draft(page_html)

    if existing_draft != normalized_message:
        focus_resp = action(SESSION_ID, kind="click", selector=CHAT_INPUT_SELECTOR)
        if focus_resp.status_code != 200:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "match": match_name,
                        "state": state,
                        "url": url,
                        "error": "Failed to focus the Bumble chat input.",
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )
            return False
        if existing_draft:
            clear_resp = action(SESSION_ID, kind="fill", selector=CHAT_INPUT_SELECTOR, text="")
            if clear_resp.status_code != 200:
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "match": match_name,
                            "state": state,
                            "url": url,
                            "error": "Failed to clear the existing Bumble draft.",
                        },
                        ensure_ascii=True,
                        indent=2,
                    )
                )
                return False
        type_resp = action(SESSION_ID, kind="type", selector=CHAT_INPUT_SELECTOR, text=normalized_message)
        if type_resp.status_code != 200:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "match": match_name,
                        "state": state,
                        "url": url,
                        "error": "Failed to enter the Bumble message text.",
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )
            return False
        _pause()
        page_html = _get_html()
        existing_draft = _extract_chat_draft(page_html)

    if existing_draft != normalized_message or not _chat_send_enabled(page_html):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble did not accept the message draft for sending.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not _tap_selector_center(CHAT_SEND_SELECTOR):
        send_button = find_element_by_text(SESSION_ID, "Send", filter="interactive")
        if not send_button or not tap_ref(send_button.get("ref")):
            print(
                json.dumps(
                    {
                        "ok": False,
                        "match": match_name,
                        "state": state,
                        "url": url,
                        "error": "Failed to press the Bumble send button.",
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )
            return False

    _pause()

    updated_html = _get_html()
    messages = extract_message_objects_from_html(updated_html, match_name)
    sent = any(item.get("author") == "me" and item.get("text") == normalized_message for item in messages)
    if not sent:
        raw_content = get_page_content(SESSION_ID, mode="raw")
        raw_text = (raw_content or {}).get("text", "")
        sent = normalized_message in raw_text
    if not sent:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": get_state(get_content()),
                    "url": (get_content() or {}).get("url", ""),
                    "error": "Message send could not be verified from the visible chat.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    print(
        json.dumps(
            {
                "ok": True,
                "match": match_name,
                "state": get_state(get_content()),
                "url": (get_content() or {}).get("url", ""),
                "message": normalized_message,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def get_messages(match_name: str) -> bool:
    """Open a Bumble match and return visible messages as JSON."""
    if not open_match(match_name):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "error": f"Failed to open Bumble match: {match_name}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    content = get_content()
    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    messages = extract_message_objects_from_html(_get_html(), match_name)
    if not messages:
        raw_content = get_page_content(SESSION_ID, mode="raw")
        raw_messages = extract_messages_from_raw_text((raw_content or {}).get("text", ""), match_name)
        messages = [{"author": "unknown", "text": text} for text in raw_messages]
    if not messages:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": match_name,
                    "state": state,
                    "url": url,
                    "error": "No visible messages were found for this match.",
                    "messages": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    print(
        json.dumps(
            {
                "ok": True,
                "match": match_name,
                "state": state,
                "url": url,
                "messages": messages,
                "count": len(messages),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def debug_page() -> bool:
    """Print current Bumble state and save a screenshot for local debugging."""
    if not resume_existing_session():
        return False
    content = get_content()
    raw_content = get_page_content(SESSION_ID, mode="raw")
    state = get_state(content)
    print("State:", state)
    if content:
        print("URL:", content.get("url", ""))
        print("Title:", content.get("title", ""))
        print("Text (readability, first 1200 chars):")
        print((content.get("text") or "")[:1200])
    if raw_content:
        print("\nText (raw, first 1200 chars):")
        print((raw_content.get("text") or "")[:1200])

    nodes = _get_interactive_nodes()
    print("\nInteractive elements:")
    for node in nodes[:20]:
        print("-", (node.get("ref"), node.get("role"), node.get("name")))

    shot = screenshot(SESSION_ID, raw=True)
    if shot.status_code == 200 and hasattr(shot, "content"):
        DEBUG_SCREENSHOT_PATH.write_bytes(shot.content)
        print(f"\nScreenshot saved: {DEBUG_SCREENSHOT_PATH}")
    return True


def list_matches() -> bool:
    """Navigate to connections and print matches as JSON (name, source, expired, conversation_expired)."""
    content = open_connections()
    if not content:
        print(json.dumps({"ok": False, "error": "Failed to open Bumble connections"}, ensure_ascii=True, indent=2))
        return False

    state = get_state(content)
    url = content.get("url", "")
    if state == "logged_out":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is logged out; run auth first and enter the SMS code.",
                    "matches": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "awaiting_sms_code":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is waiting for the 6-digit SMS code; complete login first.",
                    "matches": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "captcha_challenge":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is waiting for a manual CAPTCHA challenge to be completed.",
                    "matches": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "passkey_prompt":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is on the passkey setup screen; tap 'Not Now' in the browser or retry after the client skips it.",
                    "matches": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    raw_content = get_page_content(SESSION_ID, mode="raw")
    raw_text = (raw_content or {}).get("text", "") or ""
    page_html = _get_html()
    matches: list[dict[str, Any]] = collect_all_match_entries(raw_text, page_html)
    if not matches:
        names = extract_visible_match_names(content)
        matches = [
            {
                "name": n,
                "expired": None,
                "conversation_expired": None,
                "source": "conversations",
            }
            for n in names
        ]
    if not matches:
        debug_page()
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "No visible matches detected from current page text.",
                    "matches": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    expired_count = sum(
        1
        for m in matches
        if m.get("conversation_expired") is True or m.get("expired") is True
    )
    active_count = sum(1 for m in matches if m.get("expired") is False)
    unknown_count = sum(1 for m in matches if m.get("expired") is None)
    queue_count = sum(1 for m in matches if m.get("source") == "queue")

    print(
        json.dumps(
            {
                "ok": True,
                "state": state,
                "url": url,
                "matches": matches,
                "count": len(matches),
                "expired_count": expired_count,
                "active_count": active_count,
                "unknown_expired_count": unknown_count,
                "queue_count": queue_count,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def list_likes() -> bool:
    """Navigate to Bumble Beeline and print admirer info as JSON."""
    content = open_beeline()
    if not content:
        print(json.dumps({"ok": False, "error": "Failed to open Bumble Beeline"}, ensure_ascii=True, indent=2))
        return False

    state = get_state(content)
    url = content.get("url", "")
    if state == "logged_out":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is logged out; run auth first and enter the SMS code.",
                    "likes": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "awaiting_sms_code":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is waiting for the 6-digit SMS code; complete login first.",
                    "likes": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "captcha_challenge":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is waiting for a manual CAPTCHA challenge to be completed.",
                    "likes": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state == "passkey_prompt":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is on the passkey setup screen; tap 'Not Now' in the browser or retry after the client skips it.",
                    "likes": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if "/app/beeline" not in url.lower():
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble did not stay on the Beeline / likes page.",
                    "likes": [],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    raw_content = get_page_content(SESSION_ID, mode="raw")
    raw_text = (raw_content or {}).get("text", "") or ""
    page_html = _get_html()
    likes = extract_likes_from_raw_text(raw_text)
    if not likes:
        likes = [{"name": n, "visible": True} for n in extract_visible_like_names(content)]

    total_like_count = extract_like_count(raw_text)
    premium_required = beeline_premium_required(raw_text, page_html)
    if total_like_count is None and premium_required and not likes:
        total_like_count = 0 if "no one has liked you yet" in raw_text.lower() else None

    print(
        json.dumps(
            {
                "ok": True,
                "state": state,
                "url": url,
                "likes": likes,
                "visible_count": len(likes),
                "total_like_count": total_like_count,
                "premium_required": premium_required,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return True


def enter_sms_code(code: str) -> bool:
    """Enter the 6-digit Bumble SMS code and continue."""
    normalized = re.sub(r"\D", "", code)
    if len(normalized) != 6:
        print(
            json.dumps(
                {"ok": False, "error": "SMS code must be exactly 6 digits."},
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not resume_existing_session():
        return False

    content = get_content()
    state = get_state(content)
    url = (content or {}).get("url", "")
    if state == "captcha_challenge":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is waiting for a manual CAPTCHA challenge, not an SMS code.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if state != "awaiting_sms_code":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "Bumble is not currently waiting for an SMS code.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    nodes = _get_interactive_nodes(limit=30)
    textboxes = [node for node in nodes if node.get("role") == "textbox"]
    if not textboxes:
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": state,
                    "url": url,
                    "error": "SMS code input fields were not found.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    def _entry_error(message: str) -> bool:
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": get_state(get_content()),
                    "url": (get_content() or {}).get("url", ""),
                    "error": message,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    def _short_pause() -> None:
        time.sleep(0.6)

    def _otp_inputs_empty() -> bool:
        page_html = _get_html()
        if not page_html:
            return False
        values = re.findall(r'<input type="text" class="text-field__input" autocomplete="digit" maxlength="1" size="5" data-qa-role="textfield-input" dir="auto" value="([^"]*)">', page_html)
        return bool(values) and all(value == "" for value in values[:6])

    def _try_selector_entry() -> None:
        for index, digit in enumerate(normalized, start=1):
            selector = OTP_INPUT_SELECTOR_TEMPLATE.format(index=index)
            action(SESSION_ID, kind="click", selector=selector)
            resp = action(SESSION_ID, kind="type", selector=selector, text=digit)
            if resp.status_code != 200:
                raise RuntimeError(f"Failed to type SMS digit into selector {selector}.")
            _short_pause()

    def _try_full_code_first_field() -> None:
        selector = OTP_INPUT_SELECTOR_TEMPLATE.format(index=1)
        action(SESSION_ID, kind="click", selector=selector)
        resp = action(SESSION_ID, kind="type", selector=selector, text=normalized)
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to type full SMS code into selector {selector}.")
        _short_pause()

    def _focus_first_otp_input() -> None:
        selector = OTP_INPUT_SELECTOR_TEMPLATE.format(index=1)
        resp = action(SESSION_ID, kind="click", selector=selector)
        if resp.status_code == 200:
            _short_pause()
            return
        ref = textboxes[0].get("ref")
        if not ref or not tap_ref(ref):
            raise RuntimeError("Failed to focus the first SMS input.")
        _short_pause()

    def _try_focused_type_entry() -> None:
        _focus_first_otp_input()
        resp = action(SESSION_ID, kind="type", text=normalized)
        if resp.status_code != 200:
            raise RuntimeError("Failed to type SMS code into the focused OTP input.")
        _short_pause()

    def _try_focused_press_entry() -> None:
        _focus_first_otp_input()
        for digit in normalized:
            resp = action(SESSION_ID, kind="press", key=digit)
            if resp.status_code != 200:
                raise RuntimeError(f"Failed to press SMS digit {digit} into the focused OTP input.")
            _short_pause()

    def _try_ref_entry() -> None:
        for digit, node in zip(normalized, textboxes[:6]):
            ref = node.get("ref")
            if not ref:
                continue
            action(SESSION_ID, kind="click", selector=str(ref))
            if not type_into(str(ref), digit):
                raise RuntimeError(f"Failed to type SMS digit into {ref}.")
            _short_pause()

    def _try_ref_full_code_first_field() -> None:
        ref = textboxes[0].get("ref")
        if not ref:
            raise RuntimeError("First SMS ref input was not found.")
        action(SESSION_ID, kind="click", selector=str(ref))
        if not type_into(str(ref), normalized):
            raise RuntimeError(f"Failed to type full SMS code into {ref}.")
        _short_pause()

    entry_errors: list[str] = []
    for strategy in (
        _try_focused_type_entry,
        _try_focused_press_entry,
        _try_full_code_first_field,
        _try_ref_full_code_first_field,
        _try_selector_entry,
        _try_ref_entry,
    ):
        if not _otp_inputs_empty() and not _otp_submit_enabled():
            return _entry_error("SMS inputs already contain a partial code; reset the page or request a fresh code before retrying.")
        try:
            strategy()
        except RuntimeError as exc:
            entry_errors.append(str(exc))
            continue

        _short_pause()
        if _otp_submit_enabled():
            break
    else:
        details = "; ".join(entry_errors) if entry_errors else "OTP inputs did not enable the Continue button."
        return _entry_error(
            "SMS code entry did not activate Bumble's Continue button. The code may be invalid/expired, or the page may require a different input event sequence. "
            + details
        )

    submit_resp = action(SESSION_ID, kind="click", selector=OTP_SUBMIT_SELECTOR)
    if submit_resp.status_code != 200:
        return _entry_error("Failed to click the SMS Continue button.")

    _pause()
    time.sleep(2)
    content = get_content()
    new_state = get_state(content)
    new_url = (content or {}).get("url", "")
    if new_state == "captcha_challenge":
        print(
            json.dumps(
                {
                    "ok": False,
                    "state": new_state,
                    "url": new_url,
                    "sms_code_accepted": True,
                    "error": "SMS code was accepted, but Bumble now requires a manual CAPTCHA challenge.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False
    if new_state == "awaiting_sms_code":
        return _entry_error("SMS code was submitted but Bumble is still on the confirm-phone page.")

    passkey_skipped = False
    if "/registration/passkey" in new_url.lower() or new_state == "passkey_prompt":
        for _ in range(3):
            if dismiss_passkey_prompt():
                _pause()
            time.sleep(2)
            content = get_content()
            new_state = get_state(content)
            new_url = (content or {}).get("url", "")
            if "/registration/passkey" not in new_url.lower() and new_state != "passkey_prompt":
                passkey_skipped = True
                break
        else:
            return _entry_error(
                "SMS code was accepted, but tapping 'Not Now' on the passkey screen failed; complete it manually in the browser."
            )

    payload: dict[str, Any] = {
        "ok": True,
        "state": new_state,
        "url": new_url,
        "message": "SMS code accepted.",
    }
    if passkey_skipped:
        payload["passkey_skipped"] = True
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return True


def ensure() -> bool:
    """Create/restore bumble session, navigate to app, set SF location."""
    return ensure_session(SESSION_ID, BUMBLE_APP_URL, latitude=SF_LAT, longitude=SF_LON)


def resume_existing_session() -> bool:
    """Resume stored Bumble session without creating a new auth path."""
    resp = create_session(SESSION_ID, from_stored=SESSION_ID)
    if resp.status_code not in (200, 201):
        print("No stored Bumble session available. Run auth separately.")
        return False
    set_location(SESSION_ID, SF_LAT, SF_LON)
    return True


def dismiss_passkey_prompt() -> bool:
    """
    On Bumble's /registration/passkey screen, tap the official 'Not Now' button so
    the user is not pressured into enrolling a passkey on this device.
    The script never creates or registers a passkey; it only declines the prompt.
    """
    def _still_on_passkey() -> bool:
        current = get_content()
        if not current:
            return False
        return "/registration/passkey" in ((current.get("url") or "").lower())

    if not _still_on_passkey():
        return False

    labels = ("Not Now", "Not now", "not now")
    for _ in range(3):
        for label in labels:
            if tap_text(label):
                time.sleep(1.0)
                if not _still_on_passkey():
                    return True
            el = find_element_by_text(SESSION_ID, label, filter="interactive")
            if el and tap_ref(el.get("ref")):
                time.sleep(1.0)
                if not _still_on_passkey():
                    return True
            el = find_element_by_text(SESSION_ID, label)
            if el and tap_ref(el.get("ref")):
                time.sleep(1.0)
                if not _still_on_passkey():
                    return True
        time.sleep(1.0)
        if not _still_on_passkey():
            return True
    return not _still_on_passkey()


def tap_text(text_to_find: str) -> bool:
    """Find element by text, tap at center or by ref. Returns True if OK."""
    result = get_bbox_by_text(SESSION_ID, text_to_find)
    if not result:
        return False
    if "x" in result and "width" in result:
        cx = int(result["x"] + result["width"] / 2)
        cy = int(result["y"] + result["height"] / 2)
        resp = action(SESSION_ID, kind="tap", x=cx, y=cy)
    else:
        ref = result.get("ref")
        if ref:
            resp = action(SESSION_ID, kind="tap", ref=ref)
            if resp.status_code != 200:
                resp = action(SESSION_ID, kind="tap", selector=ref)
        else:
            resp = action(SESSION_ID, kind="tap", selector=result.get("name", ""))
    return resp.status_code == 200


def tap_selector(selector: str) -> bool:
    """Tap by CSS selector, falling back to click if touch events fail."""
    for act_kind in ["tap", "click"]:
        resp = action(SESSION_ID, kind=act_kind, selector=selector)
        if resp.status_code == 200:
            return True
    return False


def tap_ref(ref: Optional[str]) -> bool:
    """Tap or click a known accessibility ref."""
    if not ref:
        return False
    for act_kind in ["click", "tap"]:
        resp = action(SESSION_ID, kind=act_kind, ref=ref)
        if resp.status_code == 200:
            return True
        resp = action(SESSION_ID, kind=act_kind, selector=ref)
        if resp.status_code == 200:
            return True
    return False


def _conversation_overflow_menu_seems_open() -> bool:
    resp = snapshot(SESSION_ID, filter="interactive")
    if resp.status_code == 200:
        try:
            for n in resp.json().get("nodes") or []:
                name = (n.get("name") or "").strip()
                if "unmatch" in name.casefold():
                    return True
        except Exception:
            pass
    for label in (
        "Unmatch",
        "Block & Report",
        "Block and Report",
        "Block",
        "Report",
        "Snooze",
        "Mute notifications",
    ):
        if find_element_by_text(SESSION_ID, label, filter="interactive"):
            return True
    return False


def _unmatch_dropdown_row_visible() -> bool:
    """True when the sandwich menu’s dropdown shows the Unmatch row (DOM has sensible size)."""
    for sel in CHAT_UNMATCH_OPTION_SELECTORS:
        bresp = element_bounds(SESSION_ID, selector=sel)
        if bresp.status_code != 200:
            continue
        try:
            box = bresp.json()
            if int(box.get("width") or 0) >= 8 and int(box.get("height") or 0) >= 8:
                return True
        except Exception:
            continue
    return False


def _tap_selector_at_center(selector: str) -> bool:
    bresp = element_bounds(SESSION_ID, selector=selector)
    if bresp.status_code != 200:
        return False
    try:
        box = bresp.json()
        x = int(box["x"] + box["width"] / 2)
        y = int(box["y"] + box["height"] / 2)
    except Exception:
        return False
    for kind in ("tap", "click"):
        if action(SESSION_ID, kind=kind, x=x, y=y).status_code == 200:
            return True
    return False


def _css_quoted_attr(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _button_selectors_for_aria_substrings(page_html: str, substrings: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"<button\b([^>]*?)>", page_html, flags=re.I | re.S):
        attrs = m.group(1)
        lab_m = re.search(r'aria-label\s*=\s*"([^"]*)"', attrs, flags=re.I)
        if not lab_m:
            lab_m = re.search(r"aria-label\s*=\s*'([^']*)'", attrs, flags=re.I)
        if not lab_m:
            continue
        label = html_lib.unescape(lab_m.group(1).strip())
        lower = label.casefold()
        if any(s.casefold() in lower for s in substrings):
            sel = f'button[aria-label="{_css_quoted_attr(label)}"]'
            if sel not in seen:
                seen.add(sel)
                out.append(sel)
    return out


def _open_conversation_overflow_menu() -> bool:
    page_html = _get_html()

    for sel in CHAT_OVERFLOW_MENU_SELECTORS:
        if tap_selector(sel):
            time.sleep(0.35)
            if _conversation_overflow_menu_seems_open() or _unmatch_dropdown_row_visible():
                return True

    aria_substrings: tuple[str, ...] = (
        "More options",
        "more options",
        "Open menu",
        "Conversation options",
        "Chat options",
        "Conversation actions",
    )
    for sel in _button_selectors_for_aria_substrings(page_html, aria_substrings):
        if tap_selector(sel):
            time.sleep(0.35)
            if _conversation_overflow_menu_seems_open() or _unmatch_dropdown_row_visible():
                return True

    for text_probe in ("More options", "Open menu", "Menu"):
        if tap_text(text_probe):
            time.sleep(0.35)
            if _conversation_overflow_menu_seems_open() or _unmatch_dropdown_row_visible():
                return True

    resp = snapshot(SESSION_ID, filter="interactive")
    if resp.status_code == 200:
        try:
            nodes = resp.json().get("nodes") or []
        except Exception:
            nodes = []
        for n in nodes:
            if (n.get("role") or "").lower() != "button":
                continue
            name = _normalize_space(str(n.get("name") or ""))
            if _OVERFLOW_MENU_BUTTON_NAME_RE.search(name):
                if tap_ref(n.get("ref")):
                    time.sleep(0.35)
                    if _conversation_overflow_menu_seems_open() or _unmatch_dropdown_row_visible():
                        return True
    return False


def _tap_unmatch_menu_item() -> bool:
    for sel in CHAT_UNMATCH_OPTION_SELECTORS:
        if tap_selector(sel):
            return True
        if _tap_selector_at_center(sel):
            return True
    resp = snapshot(SESSION_ID, filter="interactive")
    if resp.status_code == 200:
        try:
            nodes = resp.json().get("nodes") or []
        except Exception:
            nodes = []
        for n in nodes:
            name = (n.get("name") or "").strip()
            if "unmatch" in name.casefold() and "block" in name.casefold():
                if tap_ref(n.get("ref")):
                    return True
    for label in ("Unmatch",):
        if tap_text(label):
            return True
        el = find_element_by_text(SESSION_ID, label, filter="interactive")
        if el and tap_ref(el.get("ref")):
            return True
    combined = get_bbox_by_text(SESSION_ID, "Unmatch Block and report", filter="interactive")
    if combined and "x" in combined and "width" in combined:
        cx = int(combined["x"] + combined["width"] / 2)
        cy = int(combined["y"] + int(combined["height"]) * 0.22)
        for kind in ("tap", "click"):
            if action(SESSION_ID, kind=kind, x=cx, y=cy).status_code == 200:
                return True
    return False


def _confirm_unmatch_modals() -> None:
    time.sleep(0.8)
    for label in (
        "I'm just not interested",
        "I am just not interested",
        "It's not them, it's me",
        "Its not them, its me",
        "Not interested",
        "Just not interested",
    ):
        if tap_text(label):
            _pause()
            break
    for _ in range(4):
        tapped = False
        for label in ("Unmatch", "Yes, unmatch", "Yes, Unmatch", "Confirm", "Continue"):
            if tap_text(label):
                _pause()
                tapped = True
                time.sleep(0.8)
                break
        if not tapped:
            time.sleep(0.5)
        else:
            break


def _pick_unmatch_branch_in_first_modal() -> None:
    """
    After the header sandwich → Unmatch, Bumble shows a modal titled 'Unmatch this person'
    with two rows: 'Unmatch' and 'Block and report'. We must open the Unmatch branch first.
    """
    time.sleep(0.6)
    if "Unmatch this person" not in _get_html():
        return
    sel = 'div.dialog--m .choice-group__item:first-of-type label[data-qa-role="choice-field"]'
    if not tap_selector(sel):
        _tap_selector_at_center(sel)
    time.sleep(0.9)


def unmatch_match(match_name: str) -> bool:
    """Open a match chat, choose Unmatch from the overflow menu, confirm dialogs, and verify the list."""
    normalized = _normalize_space(match_name)
    if not normalized:
        print(
            json.dumps(
                {"ok": False, "error": "Match name is empty."},
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    content = open_connections()
    if not content:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "error": "Failed to open Bumble connections.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    state = get_state(content)
    url = (content or {}).get("url", "")
    if state in ("logged_out", "awaiting_sms_code", "captcha_challenge", "passkey_prompt"):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "state": state,
                    "url": url,
                    "error": "Bumble session is not in a logged-in state.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    raw_content = get_page_content(SESSION_ID, mode="raw")
    raw_text = (raw_content or {}).get("text", "") or ""
    page_html = _get_html()
    match_names = [m["name"] for m in collect_all_match_entries(raw_text, page_html)]
    target_cf = normalized.casefold()
    if target_cf not in {n.casefold() for n in match_names}:
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "state": state,
                    "url": url,
                    "error": f"Match '{normalized}' is not in the current Bumble matches list.",
                    "available_matches": match_names,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not open_match(normalized):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "error": f"Failed to open Bumble match: {normalized}",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not _wait_for_active_match(normalized):
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "error": "Active chat did not open for the requested match.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not _open_conversation_overflow_menu():
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "error": "Could not open the conversation overflow menu (More / ⋯).",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    if not _tap_unmatch_menu_item():
        print(
            json.dumps(
                {
                    "ok": False,
                    "match": normalized,
                    "error": "Unmatch was not found in the overflow menu.",
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return False

    _pick_unmatch_branch_in_first_modal()
    _pause()
    _confirm_unmatch_modals()
    _pause()

    open_connections()
    time.sleep(1.5)
    _pause()
    raw_content = get_page_content(SESSION_ID, mode="raw")
    raw_text = (raw_content or {}).get("text", "") or ""
    page_html = _get_html()
    match_names_after = [m["name"] for m in collect_all_match_entries(raw_text, page_html)]
    removed = target_cf not in {n.casefold() for n in match_names_after}

    if not removed:
        time.sleep(2.0)
        open_connections()
        _pause()
        raw_content = get_page_content(SESSION_ID, mode="raw")
        raw_text = (raw_content or {}).get("text", "") or ""
        page_html = _get_html()
        match_names_after = [m["name"] for m in collect_all_match_entries(raw_text, page_html)]
        removed = target_cf not in {n.casefold() for n in match_names_after}

    print(
        json.dumps(
            {
                "ok": removed,
                "match": normalized,
                "removed_from_list": removed,
                "matches_after": match_names_after,
                "note": None
                if removed
                else "Unmatch flow ran but the name still appears in the list; check the browser or retry.",
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return removed


def type_into(selector_or_ref: str, value: str) -> bool:
    """Type into element. Accepts ref (e.g. e15) or CSS selector."""
    resp = action(SESSION_ID, kind="type", selector=selector_or_ref, text=value)
    return resp.status_code == 200


def get_content() -> Optional[dict[str, str]]:
    """Get page url, title, text."""
    return get_page_content(SESSION_ID)


def is_auth_or_get_started() -> bool:
    """True if on get-started or auth page (needs login flow)."""
    content = get_content()
    if not content:
        return False
    url = (content.get("url") or "").lower()
    text_content = (content.get("text") or "").lower()
    return "get-started" in url or "auth" in url or "how do you want to get started" in text_content


def _check_page(step: str) -> None:
    """Print page content and key selectors after an action."""
    content = get_content()
    if content:
        print(f"\n--- After {step} ---")
        print("URL:", content.get("url", ""))
        print("Title:", content.get("title", ""))
        print("Text (first 800 chars):", (content.get("text") or "")[:800])
    nodes = _get_interactive_nodes(limit=15)
    if nodes:
        interactive = [(n.get("ref"), n.get("role"), n.get("name")) for n in nodes]
        print("Interactive elements:", interactive)


def run_auth_flow(phone: str) -> bool:
    """
    Run Bumble auth per AGENTS.md:
      1. Go to bumble.com/get-started
      2. Tap "Continue with another methods" -> tap "Use cell phone number" -> type phone digits
      3. Ask user to enter code from phone
    Checks page content and selectors after each action.
    """
    phone_digits = _normalize_phone_digits(phone)
    if not phone_digits:
        print("Auth failed: phone number is empty or has no digits.")
        return False
    if not ensure_session(SESSION_ID, BUMBLE_APP_URL, latitude=SF_LAT, longitude=SF_LON):
        return False
    _pause()

    # Navigate to get-started
    nav = navigate(SESSION_ID, BUMBLE_GET_STARTED, timeout=30)
    if nav.status_code != 200:
        print(f"Navigate to get-started failed: {nav.status_code}")
        return False
    set_location(SESSION_ID, SF_LAT, SF_LON)
    _pause()
    _check_page("navigate to get-started")

    # 1) Tap "Continue with another methods" or "Continue with other methods"
    #    Prefer the confirmed DOM selector before text/ref fallbacks.
    for selector in CONTINUE_METHODS_SELECTORS:
        print(f"\nTrying selector: {selector}")
        if tap_selector(selector):
            _pause()
            time.sleep(2)
            _check_page(f"tap selector '{selector}'")
            break
    else:
        # Do NOT tap "Quick sign in" — we use phone number flow per AGENTS.md
        for label in ["Continue with another methods", "Continue with other methods"]:
            el = find_element_by_text(SESSION_ID, label)
            if el:
                if "quick" in (el.get("name") or "").lower():
                    continue
                print(f"\nTapping: {label} (ref={el.get('ref')})")
                ref = el.get("ref")
                ok = tap_ref(ref)
                if not ok:
                    print("Tap/click failed")
                    return False
                _pause()
                time.sleep(2)  # Wait for modal/menu to appear
                _check_page(f"tap '{label}'")
                break
        else:
            print("'Continue with another/other methods' not found")
            _check_page("(no tap - element missing)")
            return False

    # 2) Tap "Use cell phone number" — prefer DOM selector (span.action.text-break-words)
    for sel in USE_CELL_PHONE_SELECTORS:
        print(f"\nTrying selector: {sel}")
        if tap_selector(sel):
            _pause()
            time.sleep(2)
            _check_page("tap 'Use cell phone number'")
            break
    else:
        # Fallback: find by text and tap by ref
        phone_options = [
            "Use cell phone number",
            "Use cell phone",
            "Use phone number",
            "Use phone",
            "cell phone number",
            "Phone number",
            "Sign in with phone",
            "Sign in with SMS",
            "Text me",
            "SMS",
            "mobile number",
            "Enter phone",
            "Enter your phone",
        ]
        el = None
        for wait_sec in [2, 3, 4]:
            for trial in phone_options:
                el = find_element_by_text(SESSION_ID, trial)
                if el and "quick" not in (el.get("name") or "").lower():
                    break
            if el:
                break
            time.sleep(wait_sec)
        if not el:
            resp = snapshot(SESSION_ID)
            if resp.status_code == 200:
                nodes = resp.json().get("nodes", [])
                print("All snapshot nodes:", [(n.get("ref"), n.get("role"), n.get("name")) for n in nodes[:45]])
            r = screenshot(SESSION_ID, raw=True)
            if r.status_code == 200 and hasattr(r, "content"):
                path = Path(__file__).resolve().parent / "bumble_after_continue.jpg"
                path.write_bytes(r.content)
                print(f"Screenshot saved: {path}")
            print("'Use cell phone number' (or variants) not found")
            _check_page("(before Use cell phone number)")
            return False
        print(f"\nTapping: {el.get('name')} (ref fallback)")
        if not tap_ref(el.get("ref")):
            return False
        _pause()
        _check_page("tap 'Use cell phone number'")

    # 3) Type phone number (national digits; country code is chosen in the UI)
    _pause()
    time.sleep(2)
    el = None
    for query in ["digits", "phone", "cell phone", "number", "Phone number", "mobile", "Mobile number", "Phone", "Enter your"]:
        el = find_element_by_text(SESSION_ID, query)
        if el and el.get("role") in ("textbox", "spinbutton", "searchbox", None):
            if el.get("role") == "searchbox" and "phone" not in (el.get("name") or "").lower():
                continue
            break
    if not el:
        print("Phone input not found")
        _check_page("(before type phone)")
        return False
    print(f"\nTyping {phone_digits} into {el.get('ref')} ({el.get('name')})")
    resp = action(SESSION_ID, kind="type", selector=el["ref"], text=phone_digits)
    if resp.status_code != 200:
        print("Type failed:", resp.status_code)
        return False
    _pause()
    _check_page("type phone number")

    # 4) Press Continue button
    for sel in CONTINUE_BUTTON_SELECTORS:
        if tap_selector(sel):
            _pause()
            time.sleep(2)
            _check_page("tap Continue")
            break
    else:
        el = find_element_by_text(SESSION_ID, "Continue")
        if el and tap_ref(el.get("ref")):
            _pause()
            _check_page("tap Continue")
        else:
            print("Continue button not found")

    # 5) Ask user to enter SMS code
    print("\n--- Enter SMS code from phone (code sent to your phone) ---")
    return True


def read_send_message_argv(argv: list[str]) -> tuple[str, str]:
    """
    Parse argv for send:
      send <match> <words...>
      send <match> - | --stdin   (read full message from stdin)
      send <match> --file <path> (read UTF-8 file)

    Trailing CR/LF on stdin/file is stripped so a single ``echo`` newline does not become an extra blank line in chat.
    """
    if len(argv) < 4:
        raise ValueError("missing match name or message source")
    match_name = argv[2]
    first = argv[3]
    if first in ("-", "--stdin"):
        text = sys.stdin.read().rstrip("\r\n")
        return match_name, text
    if first == "--file":
        if len(argv) < 5:
            raise ValueError("--file requires a path argument")
        path = Path(argv[4]).expanduser()
        text = path.read_text(encoding="utf-8").rstrip("\r\n")
        return match_name, text
    return match_name, " ".join(argv[3:])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python bumble_client.py ensure | content | auth <phone> | sms_code <code> | matches | likes | "
            "messages <name> | profile <name> | photos <name> <directory> | send <name> <message|-|--stdin|--file path> | "
            "unmatch <name> | debug | state | tap <text> | snapshot"
        )
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "ensure":
        ok = ensure()
        print("OK" if ok else "Failed")
        sys.exit(0 if ok else 1)

    if cmd == "content":
        if not resume_existing_session():
            sys.exit(1)
        c = get_content()
        if c:
            print("URL:", c.get("url"))
            print("Title:", c.get("title"))
            print("Text:", (c.get("text") or "")[:1000])
        else:
            print("Failed to get content")
            sys.exit(1)
        sys.exit(0)

    if cmd == "auth":
        if len(sys.argv) < 3:
            print("Usage: python bumble_client.py auth <phone>")
            print("  phone: digits only, or +country... (e.g. 4155550100 or +14155550100)")
            sys.exit(1)
        ok = run_auth_flow(sys.argv[2])
        print("Auth flow OK" if ok else "Auth flow failed or incomplete")
        sys.exit(0 if ok else 1)

    if cmd == "sms_code":
        if len(sys.argv) < 3:
            print("Usage: python bumble_client.py sms_code <6-digit-code>")
            sys.exit(1)
        ok = enter_sms_code(sys.argv[2])
        sys.exit(0 if ok else 1)

    if cmd == "matches":
        ok = list_matches()
        sys.exit(0 if ok else 1)

    if cmd == "likes":
        ok = list_likes()
        sys.exit(0 if ok else 1)

    if cmd == "messages":
        if len(sys.argv) < 3:
            print("Usage: python bumble_client.py messages <match-name>")
            sys.exit(1)
        ok = get_messages(" ".join(sys.argv[2:]))
        sys.exit(0 if ok else 1)

    if cmd == "profile":
        if len(sys.argv) < 3:
            print("Usage: python bumble_client.py profile <match-name>")
            sys.exit(1)
        ok = get_profile(" ".join(sys.argv[2:]))
        sys.exit(0 if ok else 1)

    if cmd == "photos":
        if len(sys.argv) < 4:
            print("Usage: python bumble_client.py photos <match-name> <directory>")
            sys.exit(1)
        ok = save_profile_photos(sys.argv[2], sys.argv[3])
        sys.exit(0 if ok else 1)

    if cmd == "send":
        try:
            match_for_send, message_payload = read_send_message_argv(sys.argv)
        except ValueError as exc:
            print("Usage: python bumble_client.py send <match-name> <message>")
            print("       python bumble_client.py send <match-name> -")
            print("            Read the message from stdin (use for URLs and multi-line text; avoids shell $'…' quoting bugs).")
            print("       python bumble_client.py send <match-name> --stdin   # same as -")
            print("       python bumble_client.py send <match-name> --file <path>")
            print("Error:", exc, file=sys.stderr)
            sys.exit(1)
        ok = send_message(match_for_send, message_payload)
        sys.exit(0 if ok else 1)

    if cmd == "unmatch":
        if len(sys.argv) < 3:
            print("Usage: python bumble_client.py unmatch <match-name>")
            sys.exit(1)
        ok = unmatch_match(" ".join(sys.argv[2:]))
        sys.exit(0 if ok else 1)

    if cmd == "debug":
        ok = debug_page()
        sys.exit(0 if ok else 1)

    if cmd == "state":
        if not resume_existing_session():
            sys.exit(1)
        content = get_content()
        print(json.dumps({"state": get_state(content), "content": content}, ensure_ascii=True, indent=2))
        sys.exit(0)

    if cmd == "tap":
        query = sys.argv[2] if len(sys.argv) > 2 else "Continue with another methods"
        if not resume_existing_session():
            sys.exit(1)
        _pause()
        ok = tap_text(query)
        print("Tap OK" if ok else "Tap failed")
        sys.exit(0 if ok else 1)

    if cmd == "snapshot":
        if not resume_existing_session():
            sys.exit(1)
        import json

        resp = snapshot(SESSION_ID)
        if resp.status_code == 200:
            print(json.dumps(resp.json(), indent=2)[:2000])
        else:
            print("Snapshot failed:", resp.status_code)
            sys.exit(1)
        sys.exit(0)

    print("Unknown command:", cmd)
    sys.exit(1)
