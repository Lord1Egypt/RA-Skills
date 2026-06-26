#!/usr/bin/env python3
"""Execute JavaScript in a Brave/Chrome tab via CDP WebSocket.

Usage:
    python3 cdp_exec.py <tab_id> "<js_expression>"
    python3 cdp_exec.py --list
    python3 cdp_exec.py --open "<url>"
    python3 cdp_exec.py --close <tab_id>
    python3 cdp_exec.py --screenshot <tab_id> [output.png]
    python3 cdp_exec.py --eval <tab_id> "<js_code>" [--await-promise] [--timeout-ms 10000]

Environment:
    CDP_PORT  - CDP debugging port (default: 9222, the user's daily Brave)
"""

import argparse
import base64
import json
import sys
import urllib.request

try:
    import asyncio
    import websockets
except ImportError:
    print("Error: websockets not installed. Run: pip3 install websockets", file=sys.stderr)
    sys.exit(1)

DEFAULT_PORT = 9222
DEFAULT_TIMEOUT = 30  # 增加默认超时到30秒
MAX_RETRIES = 3  # 最大重试次数


def get_port():
    import os
    return int(os.environ.get("CDP_PORT", DEFAULT_PORT))


def cdp_request(path):
    """Make a request to the CDP HTTP API."""
    port = get_port()
    url = f"http://localhost:{port}{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"CDP HTTP error: {e}", file=sys.stderr)
        return None


def list_tabs():
    """List all open tabs."""
    tabs = cdp_request("/json/list")
    if tabs is None:
        return
    for t in tabs:
        print(f"  {t.get('id', '?'):20s}  {t.get('type', '?'):8s}  {t.get('title', '?')[:60]}  {t.get('url', '')[:80]}")
    return tabs


def open_tab(url):
    """Open a new tab with the given URL."""
    import urllib.parse
    port = get_port()
    encoded_url = urllib.parse.quote(url, safe=':/?#[]@!$&\'()*+,;=-._~%')
    endpoint = f"http://localhost:{port}/json/new?{encoded_url}"
    try:
        with urllib.request.urlopen(endpoint, timeout=10) as resp:
            tab = json.loads(resp.read().decode("utf-8"))
        print(f"Opened: {tab.get('id', '?')}  {tab.get('url', '')}")
        return tab
    except Exception as e:
        print(f"Failed to open tab: {e}", file=sys.stderr)
        return None


def close_tab(tab_id):
    """Close a tab by ID."""
    port = get_port()
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json/close/{tab_id}", timeout=5) as resp:
            result = resp.read().decode("utf-8")
        print(f"Closed: {tab_id}  {result}")
    except Exception as e:
        print(f"Failed to close tab: {e}", file=sys.stderr)


async def _exec_js(ws_url, js_code, await_promise=False, timeout_ms=10000):
    """Execute JS code on a tab via CDP WebSocket with improved timeout handling."""
    try:
        async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
            # Enable Runtime and drain initial events
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            # Drain events until we get the id:1 response
            while True:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=DEFAULT_TIMEOUT))
                if msg.get("id") == 1:
                    break

            msg = {
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": js_code,
                    "returnByValue": True,
                    "awaitPromise": await_promise,
                    "timeout": timeout_ms,
                },
            }
            await ws.send(json.dumps(msg))

            # Read until we get our response (id:2)
            while True:
                resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout_ms / 1000 + DEFAULT_TIMEOUT))
                if resp.get("id") == 2:
                    break

            if "result" in resp:
                result = resp["result"]
                if "result" in result:
                    value = result["result"].get("value")
                    subtype = result["result"].get("subtype")
                    if subtype == "error":
                        description = result["result"].get("description", "Unknown error")
                        print(f"JS Error: {description}", file=sys.stderr)
                        return None
                    return value
                elif "exceptionDetails" in result:
                    exc = result["exceptionDetails"]
                    text = exc.get("text", "Unknown exception")
                    print(f"Exception: {text}", file=sys.stderr)
                    return None
            elif "error" in resp:
                print(f"CDP Error: {resp['error']}", file=sys.stderr)
                return None
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
        print(f"Connection error: {type(e).__name__}", file=sys.stderr)
        raise
    return None


async def _screenshot(ws_url, output_path):
    """Take a screenshot of the current page with improved timeout handling."""
    try:
        async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
            # Set viewport
            await ws.send(json.dumps({
                "id": 1,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {"width": 1280, "height": 900, "deviceScaleFactor": 1, "mobile": False}
            }))
            # Drain events until we get the id:1 response
            while True:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=DEFAULT_TIMEOUT))
                if msg.get("id") == 1:
                    break

            await ws.send(json.dumps({
                "id": 2,
                "method": "Page.captureScreenshot",
                "params": {"format": "png", "quality": 90}
            }))
            while True:
                resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=DEFAULT_TIMEOUT))
                if resp.get("id") == 2:
                    break

            if "result" in resp and "data" in resp["result"]:
                img_data = base64.b64decode(resp["result"]["data"])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Screenshot saved: {output_path} ({len(img_data)} bytes)")
            else:
                print(f"Screenshot failed: {resp}", file=sys.stderr)
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
        print(f"Screenshot connection error: {type(e).__name__}", file=sys.stderr)
        raise


def exec_js(tab_id, js_code, await_promise=False, timeout_ms=10000):
    """Execute JS in a tab with automatic retry on connection failure."""
    import time
    for attempt in range(MAX_RETRIES):
        try:
            tabs = cdp_request("/json/list")
            if not tabs:
                print("No tabs found. Is Brave running?", file=sys.stderr)
                return

            ws_url = None
            for t in tabs:
                if t.get("id") == tab_id:
                    ws_url = t.get("webSocketDebuggerUrl")
                    break

            if not ws_url:
                print(f"Tab {tab_id} not found.", file=sys.stderr)
                print("Available tabs:", file=sys.stderr)
                for t in tabs:
                    print(f"  {t.get('id')}  {t.get('title', '')[:60]}", file=sys.stderr)
                return

            result = asyncio.run(
                _exec_js(ws_url, js_code, await_promise, timeout_ms)
            )
            if result is not None:
                if isinstance(result, (dict, list)):
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    print(result)
            return result

        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Connection lost (attempt {attempt + 1}/{MAX_RETRIES}), retrying...", file=sys.stderr)
                time.sleep(2)  # 等待2秒后重试
                continue
            else:
                print(f"Failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                return None


def screenshot(tab_id, output_path="screenshot.png"):
    """Take a screenshot of a tab with automatic retry on connection failure."""
    import time
    for attempt in range(MAX_RETRIES):
        try:
            tabs = cdp_request("/json/list")
            if not tabs:
                print("No tabs found.", file=sys.stderr)
                return

            ws_url = None
            for t in tabs:
                if t.get("id") == tab_id:
                    ws_url = t.get("webSocketDebuggerUrl")
                    break

            if not ws_url:
                print(f"Tab {tab_id} not found.", file=sys.stderr)
                return

            asyncio.run(_screenshot(ws_url, output_path))
            return

        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Connection lost (attempt {attempt + 1}/{MAX_RETRIES}), retrying...", file=sys.stderr)
                time.sleep(2)
                continue
            else:
                print(f"Screenshot failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                return


def main():
    parser = argparse.ArgumentParser(description="CDP browser automation helper")
    parser.add_argument("--port", type=int, default=None, help="CDP port (default: 9222)")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List open tabs")
    sub.add_parser("status", help="Check if browser is running")

    p_open = sub.add_parser("open", help="Open URL in new tab")
    p_open.add_argument("url", help="URL to open")

    p_close = sub.add_parser("close", help="Close tab")
    p_close.add_argument("tab_id", help="Tab ID to close")

    p_eval = sub.add_parser("eval", help="Execute JS in tab")
    p_eval.add_argument("tab_id", help="Tab ID")
    p_eval.add_argument("js", help="JavaScript code")
    p_eval.add_argument("--await-promise", action="store_true", help="Await promises")
    p_eval.add_argument("--timeout-ms", type=int, default=10000, help="Timeout in ms")

    p_shot = sub.add_parser("screenshot", help="Take screenshot")
    p_shot.add_argument("tab_id", help="Tab ID")
    p_shot.add_argument("output", nargs="?", default="screenshot.png", help="Output path")

    # --- Smart interaction subcommands (delegates to smart_interact.py) ---

    p_interact = sub.add_parser("interact", help="Click element via CDP native mouse events (anti-detection)")
    p_interact.add_argument("tab_id", help="Tab ID")
    p_interact.add_argument("--selector", "-s", help="CSS selector")
    p_interact.add_argument("--text", "-t", help="Find element containing this text")
    p_interact.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")
    p_interact.add_argument("--x", type=int, default=None, help="X coordinate")
    p_interact.add_argument("--y", type=int, default=None, help="Y coordinate")
    p_interact.add_argument("--delay", type=int, default=50, help="Press-release delay ms (default: 50)")

    p_wait = sub.add_parser("wait", help="Wait for page load, selector, or network idle")
    p_wait.add_argument("tab_id", help="Tab ID")
    p_wait.add_argument("--page-load", action="store_true", help="Wait for document.readyState=complete")
    p_wait.add_argument("--selector", "-s", help="Wait for this CSS selector to appear")
    p_wait.add_argument("--network-idle", action="store_true", help="Wait for network idle")
    p_wait.add_argument("--timeout", type=int, default=15, help="Timeout in seconds (default: 15)")

    p_elements = sub.add_parser("elements", help="List interactive elements on page")
    p_elements.add_argument("tab_id", help="Tab ID")
    p_elements.add_argument("--selector", "-s", help="CSS selector filter")
    p_elements.add_argument("--limit", "-l", type=int, default=30, help="Max elements (default: 30)")

    p_scroll = sub.add_parser("scroll", help="Smooth scroll via CDP mouse wheel")
    p_scroll.add_argument("tab_id", help="Tab ID")
    p_scroll.add_argument("--direction", "-d", default="down", choices=["down", "up", "left", "right"])
    p_scroll.add_argument("--amount", "-a", type=int, default=300, help="Scroll amount per step (default: 300)")
    p_scroll.add_argument("--steps", type=int, default=3, help="Number of scroll steps (default: 3)")
    p_scroll.add_argument("--interval", type=float, default=0.3, help="Interval between steps")

    p_type = sub.add_parser("type", help="Type text into focused element")
    p_type.add_argument("tab_id", help="Tab ID")
    p_type.add_argument("text", help="Text to type")
    p_type.add_argument("--human", action="store_true", help="Type char by char (human-like)")
    p_type.add_argument("--char-delay", type=int, default=30, help="Delay between chars ms")

    p_key = sub.add_parser("key", help="Press a keyboard key")
    p_key.add_argument("tab_id", help="Tab ID")
    p_key.add_argument("key", help="Key name (Enter, Tab, Escape, etc.)")

    p_highlight = sub.add_parser("highlight", help="Highlight element with colored outline")
    p_highlight.add_argument("tab_id", help="Tab ID")
    p_highlight.add_argument("--selector", "-s", required=True, help="CSS selector")
    p_highlight.add_argument("--index", "-i", type=int, default=0, help="Element index")
    p_highlight.add_argument("--color", default="red", help="Outline color")

    p_paginate = sub.add_parser("pagination", help="Detect pagination buttons on page")
    p_paginate.add_argument("tab_id", help="Tab ID")

    p_snapshot = sub.add_parser("snapshot", help="Lightweight DOM snapshot")
    p_snapshot.add_argument("tab_id", help="Tab ID")
    p_snapshot.add_argument("--max-depth", type=int, default=5, help="Max DOM depth (default: 5)")
    p_snapshot.add_argument("--max-chars", type=int, default=5000, help="Max output chars (default: 5000)")

    p_status = sub.add_parser("page-status", help="Page load status (readyState, resources, scroll)")
    p_status.add_argument("tab_id", help="Tab ID")

    p_count = sub.add_parser("count", help="Count elements matching a selector")
    p_count.add_argument("tab_id", help="Tab ID")
    p_count.add_argument("--selector", "-s", required=True, help="CSS selector")

    p_locate = sub.add_parser("locate", help="Get element bounding rect coordinates")
    p_locate.add_argument("tab_id", help="Tab ID")
    p_locate.add_argument("--selector", "-s", help="CSS selector")
    p_locate.add_argument("--text", "-t", help="Find element containing this text")
    p_locate.add_argument("--index", "-i", type=int, default=0, help="Element index")

    # --- Framework-aware click commands (delegates to framework_click.py) ---

    p_smart = sub.add_parser("click-smart", help="Multi-strategy click (auto: CDP→React→Vue→dispatchEvent→Enter)")
    p_smart.add_argument("tab_id", help="Tab ID")
    p_smart.add_argument("--selector", "-s", help="CSS selector")
    p_smart.add_argument("--text", "-t", help="Find element containing this text")
    p_smart.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")

    p_df = sub.add_parser("detect-framework", help="Detect JS framework (React/Vue/Angular)")
    p_df.add_argument("tab_id", help="Tab ID")

    p_ab = sub.add_parser("analyze-button", help="Deep analyze a button (for debugging failed clicks)")
    p_ab.add_argument("tab_id", help="Tab ID")
    p_ab.add_argument("--selector", "-s", required=True, help="CSS selector")
    p_ab.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")

    # Legacy positional args support
    parser.add_argument("tab_id_pos", nargs="?", help="Tab ID (positional, legacy)")
    parser.add_argument("js_pos", nargs="?", help="JS code (positional, legacy)")

    args = parser.parse_args()

    if args.port:
        import os
        os.environ["CDP_PORT"] = str(args.port)

    if args.command == "list":
        list_tabs()
    elif args.command == "status":
        info = cdp_request("/json/version")
        if info:
            print(f"Browser: {info.get('Browser', '?')}")
            print(f"WebSocket: {info.get('webSocketDebuggerUrl', '?')}")
            tabs = cdp_request("/json/list")
            print(f"Open tabs: {len(tabs) if tabs else 0}")
        else:
            print("Browser not running or CDP not available.")
    elif args.command == "open":
        open_tab(args.url)
    elif args.command == "close":
        close_tab(args.tab_id)
    elif args.command == "eval":
        exec_js(args.tab_id, args.js, args.await_promise, args.timeout_ms)
    elif args.command == "screenshot":
        screenshot(args.tab_id, args.output)
    elif args.command in ("interact", "wait", "scroll", "type", "key",
                           "highlight", "locate"):
        # Delegate to smart_interact.py
        import subprocess, os
        si = os.path.join(os.path.dirname(__file__), "smart_interact.py")
        cmd = ["python3", si, args.command]
        if args.command == "interact":
            cmd += [args.tab_id]
            if args.selector:
                cmd += ["--selector", args.selector]
            if args.text:
                cmd += ["--text", args.text]
            if args.x is not None:
                cmd += ["--x", str(args.x)]
            if args.y is not None:
                cmd += ["--y", str(args.y)]
            cmd += ["--index", str(args.index), "--delay", str(args.delay)]
        elif args.command == "wait":
            cmd += [args.tab_id]
            if args.page_load:
                cmd += ["--page-load"]
            if args.selector:
                cmd += ["--selector", args.selector]
            if args.network_idle:
                cmd += ["--network-idle"]
            cmd += ["--timeout", str(args.timeout)]
        elif args.command == "scroll":
            cmd += [args.tab_id, "--direction", args.direction,
                    "--amount", str(args.amount),
                    "--steps", str(args.steps),
                    "--interval", str(args.interval)]
        elif args.command == "type":
            cmd += [args.tab_id, args.text]
            if args.human:
                cmd += ["--human"]
            cmd += ["--char-delay", str(args.char_delay)]
        elif args.command == "key":
            cmd += [args.tab_id, args.key]
        elif args.command == "highlight":
            cmd += [args.tab_id, "--selector", args.selector,
                    "--index", str(args.index), "--color", args.color]
        elif args.command == "locate":
            cmd += [args.tab_id]
            if args.selector:
                cmd += ["--selector", args.selector]
            if args.text:
                cmd += ["--text", args.text]
            cmd += ["--index", str(args.index)]
        subprocess.run(cmd)
    elif args.command in ("elements", "pagination", "snapshot", "page-status", "count"):
        # Delegate to page_state.py
        import subprocess, os
        ps = os.path.join(os.path.dirname(__file__), "page_state.py")
        subcmd = "status" if args.command == "page-status" else args.command
        cmd = ["python3", ps, subcmd, args.tab_id]
        if args.command == "elements":
            if args.selector:
                cmd += ["--selector", args.selector]
            cmd += ["--limit", str(args.limit)]
        elif args.command == "snapshot":
            cmd += ["--max-depth", str(args.max_depth),
                    "--max-chars", str(args.max_chars)]
        elif args.command == "count":
            cmd += ["--selector", args.selector]
        subprocess.run(cmd)
    elif args.command in ("click-smart", "detect-framework", "analyze-button"):
        # Delegate to framework_click.py
        import subprocess, os
        fc = os.path.join(os.path.dirname(__file__), "framework_click.py")
        if args.command == "click-smart":
            cmd = ["python3", fc, "smart-click", args.tab_id]
            if getattr(args, 'selector', None):
                cmd += ["--selector", args.selector]
            if getattr(args, 'text', None):
                cmd += ["--text", args.text]
            cmd += ["--index", str(args.index or 0)]
        elif args.command == "detect-framework":
            cmd = ["python3", fc, "detect-framework", args.tab_id]
        elif args.command == "analyze-button":
            cmd = ["python3", fc, "analyze-button", args.tab_id,
                   "--selector", args.selector]
            if getattr(args, 'index', None):
                cmd += ["--index", str(args.index)]
        subprocess.run(cmd)
    elif args.tab_id_pos and args.js_pos:
        # Legacy: python3 cdp_exec.py <tab_id> "<js>"
        exec_js(args.tab_id_pos, args.js_pos)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
