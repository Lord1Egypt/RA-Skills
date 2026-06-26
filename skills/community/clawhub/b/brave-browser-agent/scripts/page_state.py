#!/usr/bin/env python3
"""Page state analysis via CDP — interactive elements, page load status, pagination detection, DOM snapshots.

Usage:
    # List interactive elements
    python3 page_state.py elements <tab_id> [--selector "a, button"] [--limit 30]

    # Check page load status
    python3 page_state.py status <tab_id>

    # Detect pagination buttons
    python3 page_state.py pagination <tab_id>

    # Lightweight DOM snapshot (text content structure)
    python3 page_state.py snapshot <tab_id> [--max-depth 5] [--max-chars 5000]

    # Get element count
    python3 page_state.py count <tab_id> --selector ".note-item"
"""

import argparse
import asyncio
import json
import sys
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
    try:
        tabs = json.loads(urllib.request.urlopen(
            f"http://localhost:{port}/json/list", timeout=5
        ).read())
    except Exception as e:
        print(f"CDP error: {e}", file=sys.stderr)
        return None
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    return None


async def _eval_js(ws_url, js, timeout_ms=10000):
    """Execute JS and return result value."""
    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        mid = 1
        await ws.send(json.dumps({"id": mid, "method": "Runtime.enable"}))
        while True:
            m = json.loads(await ws.recv())
            if m.get("id") == 1:
                break

        await ws.send(json.dumps({
            "id": mid + 1, "method": "Runtime.evaluate",
            "params": {"expression": js, "returnByValue": True, "timeout": timeout_ms}
        }))
        while True:
            resp = json.loads(await ws.recv())
            if resp.get("id") == mid + 1:
                result = resp.get("result", {}).get("result", {})
                if result.get("subtype") == "error":
                    return {"error": result.get("description", "Unknown error")}
                return result.get("value")


JS_INTERACTIVE_ELEMENTS = '''(function() {
    const selector = arguments[0] || 'a, button, input, select, textarea, [role="button"], [onclick], [tabindex]';
    const limit = arguments[1] || 30;
    const els = document.querySelectorAll(selector);
    const results = [];
    const viewportH = window.innerHeight;
    const viewportW = window.innerWidth;

    els.forEach((el, i) => {
        if (i >= limit) return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return; // hidden

        const tag = el.tagName.toLowerCase();
        const type = el.type || '';
        const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().substring(0, 80);
        const href = el.href || '';
        const placeholder = el.placeholder || '';
        const inViewport = r.top >= 0 && r.top <= viewportH && r.left >= 0 && r.left <= viewportW;

        results.push({
            index: results.length,
            tag: tag,
            type: type,
            text: text,
            href: href ? href.substring(0, 120) : '',
            placeholder: placeholder,
            x: Math.round(r.left + r.width / 2),
            y: Math.round(r.top + r.height / 2),
            width: Math.round(r.width),
            height: Math.round(r.height),
            visible: inViewport,
            id: el.id || '',
            classes: (el.className && typeof el.className === 'string') ? el.className.substring(0, 100) : ''
        });
    });

    return JSON.stringify({
        total: els.length,
        shown: results.length,
        viewport: {width: viewportW, height: viewportH},
        scroll: {x: window.scrollX, y: window.scrollY},
        elements: results
    }, null, 2);
})()'''


JS_PAGE_STATUS = '''(function() {
    const perf = performance.getEntriesByType('navigation')[0] || {};
    const resources = performance.getEntriesByType('resource');
    const pending = resources.filter(r => !r.responseEnd).length;
    return JSON.stringify({
        url: location.href,
        title: document.title,
        readyState: document.readyState,
        domContentLoaded: perf.domContentLoadedEventEnd || 0,
        loadComplete: perf.loadEventEnd || 0,
        totalResources: resources.length,
        pendingResources: pending,
        scrollPosition: {x: window.scrollX, y: window.scrollY},
        documentHeight: document.documentElement.scrollHeight,
        viewportHeight: window.innerHeight,
        urlFragment: location.hash || ''
    }, null, 2);
})()'''


JS_PAGINATION = '''(function() {
    const results = [];
    const keywords = ['next', '下一页', 'next page', 'load more', '加载更多', 'more', 'show more',
                       '查看更多', '翻页', '后一页', '›', '»', '›', '→', '下页', '下一个'];
    const antonyms = ['prev', '上一页', 'previous', '前页'];

    // Check common pagination elements
    const selectors = [
        'a[rel="next"]', 'button[rel="next"]',
        'a.next', 'button.next', '.next a', '.next button',
        '.pagination a', '.pagination button',
        '.pager a', '.pager button',
        '[class*="next"]', '[class*="page-next"]',
        '[class*="load-more"]', '[class*="loadmore"]',
        '[class*="more-btn"]', '[class*="show-more"]',
        'li.next a', 'li.next button'
    ];

    for (const sel of selectors) {
        document.querySelectorAll(sel).forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            const text = (el.innerText || '').trim().toLowerCase();
            // Skip if it matches antonyms
            if (antonyms.some(a => text.includes(a))) return;
            results.push({
                selector: sel,
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || '').trim().substring(0, 60),
                x: Math.round(r.left + r.width / 2),
                y: Math.round(r.top + r.height / 2),
                href: el.href || '',
                disabled: el.disabled || false
            });
        });
    }

    // Also check all buttons/links with keyword text
    document.querySelectorAll('a, button, [role="button"]').forEach(el => {
        const text = (el.innerText || el.getAttribute('aria-label') || '').trim().toLowerCase();
        if (keywords.some(k => text.includes(k))) {
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            // Avoid duplicates
            const already = results.some(r2 => r2.x === Math.round(r.left + r.width/2) && r2.y === Math.round(r.top + r.height/2));
            if (!already) {
                results.push({
                    selector: 'keyword-match',
                    tag: el.tagName.toLowerCase(),
                    text: (el.innerText || '').trim().substring(0, 60),
                    x: Math.round(r.left + r.width / 2),
                    y: Math.round(r.top + r.height / 2),
                    href: el.href || '',
                    disabled: el.disabled || false
                });
            }
        }
    });

    // Check for infinite scroll indicators
    const sentinel = document.querySelector('[class*="infinite"], [class*="loading"], [class*="sentinel"]');
    const hasInfiniteScroll = sentinel && sentinel.getBoundingClientRect().height > 0;

    return JSON.stringify({
        paginationButtons: results,
        hasInfiniteScroll: hasInfiniteScroll,
        documentHeight: document.documentElement.scrollHeight,
        scrollPosition: window.scrollY,
        distanceToBottom: document.documentElement.scrollHeight - window.scrollY - window.innerHeight
    }, null, 2);
})()'''


JS_DOM_SNAPSHOT = '''(function() {
    const maxDepth = arguments[0] || 5;
    const maxChars = arguments[1] || 5000;

    function snapshotNode(el, depth) {
        if (depth > maxDepth) return null;
        const tag = el.tagName?.toLowerCase();
        if (!tag) return null;
        // Skip script, style, svg, noscript
        if (['script', 'style', 'svg', 'noscript', 'meta', 'link', 'head'].includes(tag)) return null;

        const result = {tag: tag};
        if (el.id) result.id = el.id;
        const cls = el.className;
        if (cls && typeof cls === 'string' && cls.length > 0 && cls.length < 100) {
            result.class = cls;
        }

        const children = el.children;
        if (children.length === 0 || depth === maxDepth) {
            const text = (el.innerText || '').trim();
            if (text.length > 0) {
                result.text = text.substring(0, 200);
            }
            return result;
        }

        result.children = [];
        for (const child of children) {
            const snap = snapshotNode(child, depth + 1);
            if (snap) result.children.push(snap);
        }
        return result;
    }

    const body = document.body;
    const result = snapshotNode(body, 0);
    const json = JSON.stringify(result, null, 2);
    return json.substring(0, maxChars);
})()'''


JS_ELEMENT_COUNT = '''(function() {
    const selector = arguments[0];
    const els = document.querySelectorAll(selector);
    const viewportH = window.innerHeight;
    let visible = 0;
    els.forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.top >= 0 && r.top <= viewportH) visible++;
    });
    return JSON.stringify({
        selector: selector,
        total: els.length,
        visible: visible,
        scrollY: window.scrollY,
        documentHeight: document.documentElement.scrollHeight
    }, null, 2);
})()'''


async def cmd_elements(args):
    """List interactive elements on the page."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    # We pass selector and limit via a wrapper that injects arguments
    selector = args.selector or 'a, button, input, select, textarea, [role="button"], [onclick], [tabindex]'
    limit = args.limit or 30
    js = f'''(function() {{
        const selector = '{selector}';
        const limit = {limit};
        {JS_INTERACTIVE_ELEMENTS.replace("(function() {", "").rstrip(")")}
        const els = document.querySelectorAll(selector);
        const results = [];
        const viewportH = window.innerHeight;
        const viewportW = window.innerWidth;
        els.forEach((el, i) => {{
            if (i >= limit) return;
            const r = el.getBoundingClientRect();
            if (r.width === 0 && r.height === 0) return;
            const tag = el.tagName.toLowerCase();
            const type = el.type || '';
            const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().substring(0, 80);
            const href = el.href || '';
            const placeholder = el.placeholder || '';
            const inViewport = r.top >= 0 && r.top <= viewportH && r.left >= 0 && r.left <= viewportW;
            results.push({{
                index: results.length, tag: tag, type: type, text: text,
                href: href ? href.substring(0, 120) : '',
                placeholder: placeholder,
                x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
                width: Math.round(r.width), height: Math.round(r.height),
                visible: inViewport, id: el.id || '',
                classes: (el.className && typeof el.className === 'string') ? el.className.substring(0, 100) : ''
            }});
        }});
        return JSON.stringify({{total: els.length, shown: results.length,
            viewport: {{width: viewportW, height: viewportH}},
            scroll: {{x: window.scrollX, y: window.scrollY}},
            elements: results}}, null, 2);
    }})()'''

    result = await _eval_js(ws_url, js)
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
    if result:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2))


async def cmd_status(args):
    """Check page load status."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    result = await _eval_js(ws_url, JS_PAGE_STATUS)
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
    if result:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2))


async def cmd_pagination(args):
    """Detect pagination buttons."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    result = await _eval_js(ws_url, JS_PAGINATION)
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
    if result:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2))


async def cmd_snapshot(args):
    """Lightweight DOM snapshot."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    max_depth = args.max_depth or 5
    max_chars = args.max_chars or 5000
    js = f'''(function() {{
        const maxDepth = {max_depth};
        const maxChars = {max_chars};
        function snapshotNode(el, depth) {{
            if (depth > maxDepth) return null;
            const tag = el.tagName?.toLowerCase();
            if (!tag) return null;
            if (['script','style','svg','noscript','meta','link','head'].includes(tag)) return null;
            const result = {{tag: tag}};
            if (el.id) result.id = el.id;
            const cls = el.className;
            if (cls && typeof cls === 'string' && cls.length > 0 && cls.length < 100) result.class = cls;
            const children = el.children;
            if (children.length === 0 || depth === maxDepth) {{
                const text = (el.innerText || '').trim();
                if (text.length > 0) result.text = text.substring(0, 200);
                return result;
            }}
            result.children = [];
            for (const child of children) {{
                const snap = snapshotNode(child, depth + 1);
                if (snap) result.children.push(snap);
            }}
            return result;
        }}
        const result = snapshotNode(document.body, 0);
        const json = JSON.stringify(result, null, 2);
        return json.substring(0, maxChars);
    }})()'''

    result = await _eval_js(ws_url, js, timeout_ms=15000)
    if result:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2))


async def cmd_count(args):
    """Count elements matching a selector."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(f"Tab {args.tab_id} not found", file=sys.stderr)
        return

    js = f'''(function() {{
        const els = document.querySelectorAll('{args.selector}');
        const viewportH = window.innerHeight;
        let visible = 0;
        els.forEach(el => {{
            const r = el.getBoundingClientRect();
            if (r.top >= 0 && r.top <= viewportH) visible++;
        }});
        return JSON.stringify({{
            selector: '{args.selector}',
            total: els.length,
            visible: visible,
            scrollY: window.scrollY,
            documentHeight: document.documentElement.scrollHeight
        }}, null, 2);
    }})()'''

    result = await _eval_js(ws_url, js)
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
    if result:
        print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Page state analysis via CDP")
    parser.add_argument("--port", type=int, default=None, help="CDP port (default: 9222)")
    sub = parser.add_subparsers(dest="command")

    p_el = sub.add_parser("elements", help="List interactive elements")
    p_el.add_argument("tab_id", help="Tab ID")
    p_el.add_argument("--selector", "-s", help="CSS selector (default: interactive elements)")
    p_el.add_argument("--limit", "-l", type=int, default=30, help="Max elements (default: 30)")

    p_st = sub.add_parser("status", help="Page load status")
    p_st.add_argument("tab_id", help="Tab ID")

    p_pg = sub.add_parser("pagination", help="Detect pagination buttons")
    p_pg.add_argument("tab_id", help="Tab ID")

    p_snap = sub.add_parser("snapshot", help="Lightweight DOM snapshot")
    p_snap.add_argument("tab_id", help="Tab ID")
    p_snap.add_argument("--max-depth", type=int, default=5, help="Max DOM depth (default: 5)")
    p_snap.add_argument("--max-chars", type=int, default=5000, help="Max output chars (default: 5000)")

    p_cnt = sub.add_parser("count", help="Count elements by selector")
    p_cnt.add_argument("tab_id", help="Tab ID")
    p_cnt.add_argument("--selector", "-s", required=True, help="CSS selector")

    args = parser.parse_args()

    if args.port:
        import os
        os.environ["CDP_PORT"] = str(args.port)

    commands = {
        "elements": cmd_elements,
        "status": cmd_status,
        "pagination": cmd_pagination,
        "snapshot": cmd_snapshot,
        "count": cmd_count,
    }

    if args.command in commands:
        asyncio.run(commands[args.command](args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
