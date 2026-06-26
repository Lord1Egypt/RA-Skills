#!/usr/bin/env python3
"""
标准化 Cookie 提取脚本
从浏览器通过 CDP 提取指定域名的 Cookie，缓存到 /tmp 避免重复提取

用法：
  python3 extract_cookies.py <target_url>         # 提取并缓存
  python3 extract_cookies.py <target_url> --force  # 强制刷新
  python3 extract_cookies.py <target_url> --check  # 只检查缓存是否有效
"""

import json
import os
import sys
import time
import hashlib
import urllib.request

CACHE_DIR = "/tmp/form_api_cookies"
CACHE_MAX_AGE = 3600  # 1小时过期


def get_cache_path(domain: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    domain_hash = hashlib.md5(domain.encode()).hexdigest()[:8]
    safe_domain = domain.replace(".", "_").replace(":", "_")
    return os.path.join(CACHE_DIR, f"{safe_domain}_{domain_hash}.txt")


def is_cache_valid(cache_path: str) -> bool:
    if not os.path.exists(cache_path):
        return False
    age = time.time() - os.path.getmtime(cache_path)
    if age > CACHE_MAX_AGE:
        return False
    with open(cache_path) as f:
        content = f.read().strip()
    return bool(content)


def extract_from_browser(target_url: str) -> str:
    """通过 CDP WebSocket 从浏览器提取 Cookie"""
    try:
        import websocket
    except ImportError:
        print("ERROR: websocket-client not installed. Run: pip3 install websocket-client", file=sys.stderr)
        sys.exit(1)

    cdp_url = "http://127.0.0.1:9222/json"
    try:
        tabs_raw = urllib.request.urlopen(cdp_url, timeout=5).read()
    except Exception as e:
        print(f"ERROR: Cannot connect to Chrome CDP at {cdp_url}\n{e}", file=sys.stderr)
        print("Make sure Chrome is running with: --remote-debugging-port=9222", file=sys.stderr)
        sys.exit(1)

    tabs = json.loads(tabs_raw)
    domain = target_url.split("/")[2] if "://" in target_url else target_url

    # 优先找目标域名的 tab，否则用第一个 http tab
    tab = None
    for t in tabs:
        if domain in t.get("url", ""):
            tab = t
            break
    if not tab:
        for t in tabs:
            if t.get("url", "").startswith("http"):
                tab = t
                break

    if not tab:
        print("ERROR: No valid browser tab found", file=sys.stderr)
        sys.exit(1)

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        print(f"ERROR: Tab has no webSocketDebuggerUrl: {tab.get('url')}", file=sys.stderr)
        sys.exit(1)

    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({
        "id": 1,
        "method": "Network.getCookies",
        "params": {"urls": [target_url]}
    }))
    result = json.loads(ws.recv())
    ws.close()

    cookies = result.get("result", {}).get("cookies", [])
    if not cookies:
        print(f"WARNING: No cookies found for {target_url}", file=sys.stderr)
        return ""

    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    return cookie_str


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_cookies.py <target_url> [--force] [--check]")
        sys.exit(1)

    target_url = sys.argv[1]
    force = "--force" in sys.argv
    check_only = "--check" in sys.argv

    domain = target_url.split("/")[2] if "://" in target_url else target_url
    cache_path = get_cache_path(domain)

    if check_only:
        valid = is_cache_valid(cache_path)
        print("valid" if valid else "expired")
        sys.exit(0 if valid else 1)

    if not force and is_cache_valid(cache_path):
        print(f"# Using cached cookies (cache: {cache_path})", file=sys.stderr)
        with open(cache_path) as f:
            print(f.read().strip())
        return

    print(f"# Extracting cookies from browser for: {target_url}", file=sys.stderr)
    cookie_str = extract_from_browser(target_url)

    if cookie_str:
        with open(cache_path, "w") as f:
            f.write(cookie_str)
        print(f"# Saved to: {cache_path}", file=sys.stderr)
        print(cookie_str)
    else:
        print("ERROR: Failed to extract cookies", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
