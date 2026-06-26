#!/usr/bin/env python3
"""
Remote Browser Service (RBS) HTTP client.
Follows workspace/skills/remote-browser-service/SKILL.md.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

import requests

DEFAULT_BASE = "https://rb.all-completed.com"


def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json"}
    key = os.environ.get("AC_API_KEY")
    if key:
        h["Authorization"] = f"Bearer {key}"
    return h


def _base_url() -> str:
    return os.environ.get("RBS_BASE_URL", DEFAULT_BASE)


def _post(session_id: str, path: str, data: Optional[dict[str, Any]] = None) -> requests.Response:
    base = _base_url()
    url = f"{base}/api/sessions/{session_id}{path}"
    return requests.post(url, headers=_headers(), json=data or {}, timeout=60)


def _get(session_id: str, path: str, params: Optional[dict[str, str]] = None) -> requests.Response:
    base = _base_url()
    url = f"{base}/api/sessions/{session_id}{path}"
    return requests.get(url, headers=_headers(), params=params or {}, timeout=60)


def action(session_id: str, *, kind: str, **kwargs: Any) -> requests.Response:
    """
    Act on the page. Kinds: tap, click, type, fill, press, focus, hover, select, scroll.
    Use tap for touch-capable pages (mobile viewports); click for mouse. Both support x,y or selector.
    Examples:
        action("bumble", kind="tap", x=960, y=620)
        action("bumble", kind="tap", selector="button.submit")
        action("bumble", kind="type", selector="#email", text="user@example.com")
        action("bumble", kind="fill", selector="#email", text="user@example.com")
        action("bumble", kind="press", key="Enter")
    """
    payload = {"kind": kind, **kwargs}
    return _post(session_id, "/action", payload)


def navigate(session_id: str, url: str, timeout: Optional[int] = None) -> requests.Response:
    payload = {"url": url}
    if timeout is not None:
        payload["timeout"] = timeout
    return _post(session_id, "/navigate", payload)


def snapshot(session_id: str, *, filter: Optional[str] = None, depth: Optional[int] = None) -> requests.Response:
    params = {}
    if filter:
        params["filter"] = filter
    if depth is not None:
        params["depth"] = str(depth)
    return _get(session_id, "/json", params if params else None)


def text(session_id: str, *, mode: str = "readability") -> requests.Response:
    return _get(session_id, "/text", {"mode": mode} if mode != "readability" else None)


def screenshot(session_id: str, *, raw: bool = False, quality: Optional[int] = None) -> requests.Response:
    params = {}
    if raw:
        params["raw"] = "true"
    if quality is not None:
        params["quality"] = str(quality)
    return _get(session_id, "/screenshot", params if params else None)


def html(session_id: str) -> requests.Response:
    """Fetch full page HTML snapshot with inlined CSS."""
    return _get(session_id, "/html")


def element_bounds(session_id: str, *, selector: Optional[str] = None, ref: Optional[str] = None) -> requests.Response:
    """
    Get element bounding box (x, y, width, height). Use selector (CSS) or ref (from snapshot).
    """
    params: dict[str, str] = {}
    if selector:
        params["selector"] = selector
    elif ref:
        params["ref"] = ref
    return _get(session_id, "/element-bounds", params if params else None)


def set_location(session_id: str, latitude: float, longitude: float, accuracy: Optional[int] = None) -> requests.Response:
    payload = {"latitude": latitude, "longitude": longitude}
    if accuracy is not None:
        payload["accuracy"] = accuracy
    return _post(session_id, "/location", payload)


def create_session(
    session_id: str,
    *,
    url: Optional[str] = None,
    from_stored: Optional[str] = None,
) -> requests.Response:
    """
    Create or restore a session. POST /api/sessions.
    Use url to navigate immediately; use from_stored to restore from stored session.
    """
    base = _base_url()
    url_path = f"{base}/api/sessions"
    payload: dict[str, Any] = {"session_id": session_id}
    if url:
        payload["url"] = url
    if from_stored:
        payload["from"] = from_stored
    return requests.post(url_path, headers=_headers(), json=payload, timeout=60)


def get_page_content(session_id: str, *, mode: str = "readability") -> Optional[dict[str, str]]:
    """Get page url, title, and text. Returns None on failure."""
    resp = text(session_id, mode=mode)
    if resp.status_code != 200:
        return None
    try:
        return resp.json()
    except Exception:
        return None


def find_element_by_text(
    session_id: str, text: str, *, filter: Optional[str] = None
) -> Optional[dict[str, Any]]:
    """
    Find element by accessible name in snapshot. Returns {ref, role, name} if found, else None.
    Does not call element-bounds.
    """
    resp = snapshot(session_id, filter=filter) if filter else snapshot(session_id)
    if resp.status_code != 200:
        return None
    try:
        data = resp.json()
        for n in data.get("nodes") or []:
            name = (n.get("name") or "").strip()
            if text.lower() in name.lower():
                ref = n.get("ref")
                if ref:
                    return {"ref": ref, "role": n.get("role"), "name": name}
    except Exception:
        pass
    return None


def get_bbox_by_text(
    session_id: str, text: str, *, filter: Optional[str] = None
) -> Optional[dict[str, Any]]:
    """
    Find element by accessible name. Returns bounding box {x, y, width, height} if element-bounds
    succeeds; otherwise returns {ref, role, name} for click-by-ref fallback.
    """
    resp = snapshot(session_id, filter=filter) if filter else snapshot(session_id)
    if resp.status_code != 200:
        return None
    try:
        data = resp.json()
        nodes = data.get("nodes") or []
        for n in nodes:
            name = (n.get("name") or "").strip()
            if text.lower() in name.lower():
                ref = n.get("ref")
                role = n.get("role")
                if not ref:
                    continue
                # Try element-bounds: ref, aria-label (RBS often 502 for these)
                for sel in [ref, f'[aria-label="{name}"]', f'[aria-label*="{text[:20]}"]']:
                    bresp = element_bounds(session_id, selector=sel)
                    if bresp.status_code == 200:
                        b = bresp.json()
                        if b.get("width", 0) > 0 and b.get("height", 0) > 0:
                            return b
                # Don't use [role=button] — it matches first of multiple, wrong element
                return {"ref": ref, "role": role, "name": name}
    except Exception:
        pass
    return None


def ensure_session(session_id: str, url: str, *, latitude: Optional[float] = None, longitude: Optional[float] = None) -> bool:
    """
    Create or restore session. Tries restore from stored first; if not found, creates with url.
    Sets location per AGENTS.md when provided. Returns True if OK.
    """
    resp = create_session(session_id, from_stored=session_id)
    if resp.status_code not in (200, 201):
        resp = create_session(session_id, url=url)
        if resp.status_code not in (200, 201):
            print(f"Create failed: {resp.status_code} {resp.text[:200]}")
            return False
    else:
        # Restored; navigate in case page is blank (AGENTS.md)
        nav = navigate(session_id, url, timeout=30)
        if nav.status_code != 200:
            print(f"Navigate failed: {nav.status_code} {nav.text[:200]}")
    if latitude is not None and longitude is not None:
        set_location(session_id, latitude, longitude)
    return True


if __name__ == "__main__":
    import sys
    import time

    args = sys.argv[1:]
    if args and args[0] == "click-text":
        # Usage: python rbs_client.py click-text [session] "text to find"
        session = args[1] if len(args) > 1 else "bumble"
        search_text = args[2] if len(args) > 2 else "Continue with other methods"
        if not ensure_session(session, "https://bumble.com/app" if session == "bumble" else "https://tinder.com/app",
                             latitude=37.78891962482936, longitude=-122.41778467794562):
            sys.exit(1)
        time.sleep(1)
        result = get_bbox_by_text(session, search_text)
        if not result:
            print("Element not found")
            sys.exit(1)
        if "x" in result and "width" in result:
            cx = int(result["x"] + result["width"] / 2)
            cy = int(result["y"] + result["height"] / 2)
            print(f"Bbox: {result}, center: ({cx}, {cy})")
            resp = action(session, kind="tap", x=cx, y=cy)
        else:
            print(f"Using ref: {result.get('ref')}")
            resp = action(session, kind="tap", selector=result["ref"])
        print(f"Tap: {resp.status_code} {resp.text}")
        sys.exit(0 if resp.status_code == 200 else 1)

    if args and args[0] == "bbox":
        # Usage: python rbs_client.py bbox [session] "text to find"
        session = args[1] if len(args) > 1 else "bumble"
        search_text = args[2] if len(args) > 2 else "Continue with other methods"
        if not ensure_session(session, "https://bumble.com/app" if session == "bumble" else "https://tinder.com/app",
                             latitude=37.78891962482936, longitude=-122.41778467794562):
            sys.exit(1)
        time.sleep(1)

        # Get page content
        content = get_page_content(session)
        if content:
            print("=== Page content ===")
            print(f"URL: {content.get('url', '')}")
            print(f"Title: {content.get('title', '')}")
            print(f"Text (first 1500 chars):\n{content.get('text', '')[:1500]}")
            print()

        # Verify selector exists before bbox
        el = find_element_by_text(session, search_text)
        if not el:
            print(f"Element '{search_text}' NOT FOUND in accessibility tree")
            sys.exit(1)
        print(f"Selector exists: {el}")

        result = get_bbox_by_text(session, search_text)
        if result:
            if "x" in result and "width" in result:
                cx = result["x"] + result["width"] / 2
                cy = result["y"] + result["height"] / 2
                print(json.dumps(result, indent=2))
                print(f"Center: x={cx:.0f}, y={cy:.0f}")
            else:
                print(json.dumps(result, indent=2))
                print(f"Click via: action({session!r}, kind=\"click\", selector={result.get('ref')!r})")
        else:
            print("Not found")
        sys.exit(0 if result else 1)

    session = args[0] if args else "bumble"
    x = int(args[1]) if len(args) > 1 else 960
    y = int(args[2]) if len(args) > 2 else 620

    # Per AGENTS.md: start session, navigate to bumble.com/app, set SF location
    bumble_url = "https://bumble.com/app"
    sf_lat, sf_lon = 37.78891962482936, -122.41778467794562
    if session == "bumble":
        if not ensure_session(session, bumble_url, latitude=sf_lat, longitude=sf_lon):
            sys.exit(1)
        time.sleep(2)  # small settle pause between page actions
    elif session == "tinder":
        if not ensure_session(session, "https://tinder.com/app", latitude=sf_lat, longitude=sf_lon):
            sys.exit(1)
        time.sleep(2)

    resp = action(session, kind="tap", x=x, y=y)
    print(f"Status: {resp.status_code}")
    if resp.text:
        print(resp.text[:500])
