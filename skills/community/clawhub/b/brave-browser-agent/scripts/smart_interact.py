#!/usr/bin/env python3
"""Smart browser interaction via CDP — human-like mouse events, element targeting, smooth scrolling.

Incorporates lessons from browser-use and xiaohongshu-search skills:
- CDP Input.dispatchMouseEvent for real mouse events (anti-detection)
- Element location via CSS selector or text content
- Human-like interaction: mouse move → pause → click
- Smooth scrolling via CDP mouseWheel events
- Smart wait: readyState, selector appearance, network idle

Usage:
    # Click element by CSS selector
    python3 smart_interact.py click <tab_id> --selector "button.submit"

    # Click element by text content
    python3 smart_interact.py click <tab_id> --text "搜索"

    # Click at coordinates
    python3 smart_interact.py click <tab_id> --x 400 --y 300

    # Type into focused element
    python3 smart_interact.py type <tab_id> "hello world"

    # Scroll down
    python3 smart_interact.py scroll <tab_id> --direction down --amount 500 --steps 3

    # Wait for selector
    python3 smart_interact.py wait <tab_id> --selector ".result-item" --timeout 10

    # Wait for page load
    python3 smart_interact.py wait <tab_id> --page-load --timeout 15

    # Highlight element
    python3 smart_interact.py highlight <tab_id> --selector ".note-item"

    # Get element bounding rect
    python3 smart_interact.py locate <tab_id> --selector ".note-item" --index 0
"""

import argparse
import asyncio
import json
import random
import sys
import time
import urllib.request

try:
    import websockets
except ImportError:
    print("Error: websockets not installed. Run: pip3 install websockets", file=sys.stderr)
    sys.exit(1)

DEFAULT_PORT = 9222
MAX_WS_SIZE = 50 * 1024 * 1024


def get_port():
    import os
    return int(os.environ.get("CDP_PORT", DEFAULT_PORT))


def get_ws_url(tab_id):
    """Get WebSocket URL for a tab."""
    port = get_port()
    tabs = json.loads(urllib.request.urlopen(
        f"http://localhost:{port}/json/list", timeout=5
    ).read())
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    return None


class CDPConnection:
    """Manage a CDP WebSocket connection with message ID tracking."""

    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 0

    async def send_cdp(self, method, params=None):
        """Send a CDP command and wait for its response."""
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method}
        if params:
            msg["params"] = params
        await self.ws.send(json.dumps(msg))
        target_id = self.msg_id
        while True:
            resp = json.loads(await self.ws.recv())
            if resp.get("id") == target_id:
                return resp
        # unreachable

    async def eval_js(self, js, return_by_value=True, timeout_ms=10000):
        """Execute JS and return the result value."""
        resp = await self.send_cdp("Runtime.evaluate", {
            "expression": js,
            "returnByValue": return_by_value,
            "timeout": timeout_ms,
        })
        result = resp.get("result", {}).get("result", {})
        if result.get("subtype") == "error":
            return {"error": result.get("description", "Unknown error")}
        return result.get("value")

    async def enable_runtime(self):
        """Enable Runtime domain and drain initial events."""
        await self.send_cdp("Runtime.enable")

    async def mouse_move(self, x, y):
        """Move mouse to coordinates."""
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mouseMoved", "x": x, "y": y
        })

    async def mouse_press(self, x, y, button="left"):
        """Press mouse button."""
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": button, "clickCount": 1
        })

    async def mouse_release(self, x, y, button="left"):
        """Release mouse button."""
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": button, "clickCount": 1
        })

    async def mouse_click(self, x, y, button="left", delay_ms=50):
        """Human-like click: move → press → delay → release."""
        # Add tiny random offset for realism
        rx = x + random.uniform(-2, 2)
        ry = y + random.uniform(-2, 2)
        await self.mouse_move(rx, ry)
        await asyncio.sleep(random.uniform(0.02, 0.06))
        await self.mouse_press(rx, ry, button)
        await asyncio.sleep(delay_ms / 1000.0)
        await self.mouse_release(rx, ry, button)
        return {"success": True, "x": round(rx), "y": round(ry)}

    async def mouse_wheel(self, x, y, delta_x=0, delta_y=300):
        """Send mouse wheel event for scrolling."""
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mouseWheel", "x": x, "y": y,
            "deltaX": delta_x, "deltaY": delta_y
        })

    async def smooth_scroll(self, x=500, y=400, delta_y=300, steps=3, interval=0.3):
        """Perform smooth scrolling in steps (triggers lazy loading)."""
        for _ in range(steps):
            await self.mouse_wheel(x, y, delta_y=delta_y)
            await asyncio.sleep(interval)
        return {"scrolled": True, "steps": steps, "total_delta": delta_y * steps}

    async def type_text(self, text, char_delay_ms=30):
        """Type text character by character via CDP Input events."""
        for ch in text:
            # Dispatch keyDown + keyUp for each character
            await self.send_cdp("Input.dispatchKeyEvent", {
                "type": "keyDown",
                "text": ch,
            })
            await asyncio.sleep(char_delay_ms / 1000.0)
            await self.send_cdp("Input.dispatchKeyEvent", {
                "type": "keyUp",
                "text": ch,
            })
        return {"typed": True, "length": len(text)}

    async def insert_text(self, text):
        """Insert text at once via Input.insertText (faster, less human-like)."""
        await self.send_cdp("Input.insertText", {"text": text})
        return {"inserted": True, "length": len(text)}

    async def key_press(self, key, code=None, modifiers=0):
        """Press and release a key (e.g., Enter, Tab, Escape)."""
        params_down = {
            "type": "keyDown",
            "key": key,
            "code": code or f"Key{key.upper()}",
            "modifiers": modifiers,
        }
        params_up = {
            "type": "keyUp",
            "key": key,
            "code": code or f"Key{key.upper()}",
            "modifiers": modifiers,
        }
        # Special key mappings
        key_map = {
            "Enter": "Enter", "Return": "Enter",
            "Tab": "Tab", "Escape": "Escape", "Esc": "Escape",
            "Backspace": "Backspace", "Delete": "Delete",
            "ArrowDown": "ArrowDown", "ArrowUp": "ArrowUp",
            "ArrowLeft": "ArrowLeft", "ArrowRight": "ArrowRight",
        }
        if key in key_map:
            params_down["key"] = key_map[key]
            params_down["code"] = key_map[key]
            params_up["key"] = key_map[key]
            params_up["code"] = key_map[key]
        await self.send_cdp("Input.dispatchKeyEvent", params_down)
        await asyncio.sleep(0.03)
        await self.send_cdp("Input.dispatchKeyEvent", params_up)
        return {"pressed": key}


def _build_locate_js(selector, index=None, text=None):
    """Build JS to locate an element and return its bounding rect."""
    if text:
        # Find element by text content
        return f'''(function() {{
            const targets = document.querySelectorAll('{selector}');
            for (const el of targets) {{
                if (el.innerText.includes('{text}')) {{
                    const r = el.getBoundingClientRect();
                    return JSON.stringify({{
                        x: Math.round(r.left + r.width/2),
                        y: Math.round(r.top + r.height/2),
                        width: Math.round(r.width),
                        height: Math.round(r.height),
                        text: el.innerText.substring(0, 80)
                    }});
                }}
            }}
            return JSON.stringify({{error: "no element matching text '{text}' in '{selector}'"}});
        }})()'''
    else:
        idx = index or 0
        return f'''(function() {{
            const els = document.querySelectorAll('{selector}');
            const el = els[{idx}];
            if (!el) return JSON.stringify({{error: "no element at index {idx}", total: els.length}});
            const r = el.getBoundingClientRect();
            return JSON.stringify({{
                x: Math.round(r.left + r.width/2),
                y: Math.round(r.top + r.height/2),
                width: Math.round(r.width),
                height: Math.round(r.height),
                text: el.innerText.substring(0, 80),
                total: els.length
            }});
        }})()'''


async def cmd_click(args):
    """Click an element using CDP native mouse events."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        # Determine click target
        if args.x is not None and args.y is not None:
            x, y = args.x, args.y
        elif args.selector:
            js = _build_locate_js(args.selector, index=args.index, text=args.text)
            coords = await cdp.eval_js(js)
            if isinstance(coords, dict) and "error" in coords:
                print(json.dumps(coords), file=sys.stderr)
                return
            if isinstance(coords, str):
                coords = json.loads(coords)
            if "error" in coords:
                print(json.dumps(coords), file=sys.stderr)
                return
            x, y = coords["x"], coords["y"]
        else:
            print("Must specify --selector, --text, or --x/--y", file=sys.stderr)
            return

        result = await cdp.mouse_click(x, y, delay_ms=args.delay)
        print(json.dumps({"success": True, "x": result["x"], "y": result["y"]}))


async def cmd_type(args):
    """Type text into the focused element."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        if args.human:
            result = await cdp.type_text(args.text, char_delay_ms=args.char_delay)
        else:
            result = await cdp.insert_text(args.text)
        print(json.dumps(result))


async def cmd_scroll(args):
    """Smooth scroll via CDP mouse wheel events."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    direction_map = {"down": 1, "up": -1, "right": 1, "left": -1}
    sign = direction_map.get(args.direction, 1)

    delta_y = args.amount * sign if args.direction in ("down", "up") else 0
    delta_x = args.amount * sign if args.direction in ("right", "left") else 0

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()
        result = await cdp.smooth_scroll(
            x=args.x, y=args.y,
            delta_x=delta_x, delta_y=delta_y,
            steps=args.steps, interval=args.interval
        )
        print(json.dumps(result))


async def cmd_wait(args):
    """Wait for a condition (page load, selector, network idle)."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        if args.page_load:
            # Wait for document.readyState === 'complete'
            js = '''document.readyState'''
            deadline = time.time() + args.timeout
            while time.time() < deadline:
                state = await cdp.eval_js(js)
                if state == "complete":
                    print(json.dumps({"ready": True, "readyState": state}))
                    return
                await asyncio.sleep(0.5)
            print(json.dumps({"ready": False, "timeout": args.timeout}), file=sys.stderr)

        elif args.selector:
            # Wait for selector to appear
            js = f'''document.querySelector('{args.selector}') !== null'''
            deadline = time.time() + args.timeout
            while time.time() < deadline:
                found = await cdp.eval_js(js)
                if found:
                    print(json.dumps({"found": True, "selector": args.selector}))
                    return
                await asyncio.sleep(0.5)
            print(json.dumps({"found": False, "selector": args.selector, "timeout": args.timeout}), file=sys.stderr)

        elif args.network_idle:
            # Wait for network to be idle (no pending requests for 1 second)
            # Enable Network domain and count requests
            await cdp.send_cdp("Network.enable")
            pending = 0
            last_change = time.time()
            deadline = time.time() + args.timeout

            async def consume_events():
                nonlocal pending, last_change
                while time.time() < deadline:
                    try:
                        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=1.0))
                        method = msg.get("method", "")
                        if method == "Network.requestWillBeSent":
                            pending += 1
                            last_change = time.time()
                        elif method in ("Network.loadingFinished", "Network.loadingFailed",
                                        "Network.responseReceived"):
                            pending = max(0, pending - 1)
                            last_change = time.time()
                    except asyncio.TimeoutError:
                        pass

            while time.time() < deadline:
                await consume_events()
                if pending == 0 and (time.time() - last_change) > 1.0:
                    print(json.dumps({"idle": True, "pending": pending}))
                    return
                await asyncio.sleep(0.3)

            print(json.dumps({"idle": False, "pending": pending, "timeout": args.timeout}), file=sys.stderr)
        else:
            print("Must specify --page-load, --selector, or --network-idle", file=sys.stderr)


async def cmd_highlight(args):
    """Highlight an element with a colored outline for screenshot confirmation."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        color = args.color or "red"
        js = f'''(function() {{
            const els = document.querySelectorAll('{args.selector}');
            if (els.length === 0) return JSON.stringify({{error: "no elements found"}});
            const idx = {args.index or 0};
            if (idx >= els.length) return JSON.stringify({{error: "index out of range", total: els.length}});
            // Remove previous highlights
            document.querySelectorAll('[data-cdp-highlight]').forEach(el => {{
                el.style.outline = el.getAttribute('data-cdp-highlight');
                el.removeAttribute('data-cdp-highlight');
            }});
            const el = els[idx];
            el.setAttribute('data-cdp-highlight', el.style.outline || '');
            el.style.outline = '3px solid {color}';
            return JSON.stringify({{highlighted: true, index: idx, total: els.length}});
        }})()'''
        result = await cdp.eval_js(js)
        if isinstance(result, str):
            result = json.loads(result)
        print(json.dumps(result))


async def cmd_locate(args):
    """Get bounding rect of an element."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        js = _build_locate_js(args.selector, index=args.index, text=args.text)
        result = await cdp.eval_js(js)
        if isinstance(result, str):
            result = json.loads(result)
        print(json.dumps(result, ensure_ascii=False))


async def cmd_key(args):
    """Press a keyboard key."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()
        result = await cdp.key_press(args.key)
        print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description="Smart CDP browser interaction")
    parser.add_argument("--port", type=int, default=None, help="CDP port (default: 9222)")
    sub = parser.add_subparsers(dest="command")

    # click
    p_click = sub.add_parser("click", help="Click element via CDP native mouse events")
    p_click.add_argument("tab_id", help="Tab ID")
    p_click.add_argument("--selector", "-s", help="CSS selector")
    p_click.add_argument("--text", "-t", help="Find element containing this text")
    p_click.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")
    p_click.add_argument("--x", type=int, default=None, help="X coordinate")
    p_click.add_argument("--y", type=int, default=None, help="Y coordinate")
    p_click.add_argument("--delay", type=int, default=50, help="Press-release delay in ms (default: 50)")

    # type
    p_type = sub.add_parser("type", help="Type text into focused element")
    p_type.add_argument("tab_id", help="Tab ID")
    p_type.add_argument("text", help="Text to type")
    p_type.add_argument("--human", action="store_true", help="Type char by char (slower but human-like)")
    p_type.add_argument("--char-delay", type=int, default=30, help="Delay between chars in ms (default: 30)")

    # scroll
    p_scroll = sub.add_parser("scroll", help="Smooth scroll via CDP mouse wheel")
    p_scroll.add_argument("tab_id", help="Tab ID")
    p_scroll.add_argument("--direction", "-d", default="down", choices=["down", "up", "left", "right"])
    p_scroll.add_argument("--amount", "-a", type=int, default=300, help="Scroll amount per step (default: 300)")
    p_scroll.add_argument("--steps", type=int, default=3, help="Number of scroll steps (default: 3)")
    p_scroll.add_argument("--interval", type=float, default=0.3, help="Interval between steps (default: 0.3)")
    p_scroll.add_argument("--x", type=int, default=500, help="Mouse X for wheel event")
    p_scroll.add_argument("--y", type=int, default=400, help="Mouse Y for wheel event")

    # wait
    p_wait = sub.add_parser("wait", help="Wait for page load, selector, or network idle")
    p_wait.add_argument("tab_id", help="Tab ID")
    p_wait.add_argument("--page-load", action="store_true", help="Wait for document.readyState=complete")
    p_wait.add_argument("--selector", "-s", help="Wait for this CSS selector to appear")
    p_wait.add_argument("--network-idle", action="store_true", help="Wait for network idle")
    p_wait.add_argument("--timeout", type=int, default=15, help="Timeout in seconds (default: 15)")

    # highlight
    p_hi = sub.add_parser("highlight", help="Highlight element with colored outline")
    p_hi.add_argument("tab_id", help="Tab ID")
    p_hi.add_argument("--selector", "-s", required=True, help="CSS selector")
    p_hi.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")
    p_hi.add_argument("--color", default="red", help="Outline color (default: red)")

    # locate
    p_loc = sub.add_parser("locate", help="Get element bounding rect")
    p_loc.add_argument("tab_id", help="Tab ID")
    p_loc.add_argument("--selector", "-s", help="CSS selector")
    p_loc.add_argument("--text", "-t", help="Find element containing this text")
    p_loc.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")

    # key
    p_key = sub.add_parser("key", help="Press a keyboard key (Enter, Tab, Escape, etc.)")
    p_key.add_argument("tab_id", help="Tab ID")
    p_key.add_argument("key", help="Key name (Enter, Tab, Escape, ArrowDown, etc.)")

    args = parser.parse_args()

    if args.port:
        import os
        os.environ["CDP_PORT"] = str(args.port)

    commands = {
        "click": cmd_click,
        "type": cmd_type,
        "scroll": cmd_scroll,
        "wait": cmd_wait,
        "highlight": cmd_highlight,
        "locate": cmd_locate,
        "key": cmd_key,
    }

    if args.command in commands:
        asyncio.run(commands[args.command](args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
