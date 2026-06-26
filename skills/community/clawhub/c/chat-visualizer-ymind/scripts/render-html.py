#!/usr/bin/env python3
"""
Render a YMind graph JSON into a self-contained HTML visualization.

Usage:
  python3 render-html.py graph.json
  python3 render-html.py graph.json --out ymindmap-output.html

Input: graph.json produced by SKILL.md (agent mode) or extract-graph.py (script mode).
Output: A single HTML file with the graph data embedded inline.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "ymindmap.html"


def slugify(text: str, max_len: int = 40) -> str:
    """Turn a title into a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text[:max_len].rstrip("-")


def load_chat_messages(graph_input_path: Path) -> list | None:
    """Load and clean messages from raw_chat.json in the same directory, if present."""
    raw_chat_path = graph_input_path.parent / "raw_chat.json"
    if not raw_chat_path.exists():
        return None
    try:
        with open(raw_chat_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        items = raw.get("items") or []
        if not items:
            return None
        messages = items[0].get("messages") or []
        cleaned = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user" and content.startswith("You said\n\n"):
                content = content[len("You said\n\n"):]
            cleaned.append({"role": role, "content": content})
        return cleaned if cleaned else None
    except Exception:
        return None


def render(graph_json: dict, template: str, chat_messages: list | None = None) -> str:
    """Inject graph data (and optional chat messages) into the HTML template."""
    title = ""
    if "meta" in graph_json and graph_json["meta"]:
        title = graph_json["meta"].get("title", "")

    html = template.replace("{{TITLE}}", title or "Untitled")
    html = html.replace("{{GRAPH_JSON}}", json.dumps(graph_json, ensure_ascii=False))
    chat_json_str = json.dumps(chat_messages, ensure_ascii=False) if chat_messages is not None else "null"
    html = html.replace("{{CHAT_JSON}}", chat_json_str)
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description="Render YMind graph as HTML.")
    parser.add_argument("input", help="Path to graph.json")
    parser.add_argument("--out", "-o", default=None, help="Output HTML path (default: auto-named)")
    parser.add_argument("--template", "-t", default=None, help="Custom template path")
    parser.add_argument("--screenshot", "-s", action="store_true", help="Also capture a PNG screenshot (requires playwright)")
    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    # Read template
    tmpl_path = Path(args.template) if args.template else TEMPLATE_PATH
    if not tmpl_path.exists():
        print(f"Error: template not found at {tmpl_path}", file=sys.stderr)
        return 1

    template = tmpl_path.read_text(encoding="utf-8")

    # Load chat messages for split view (optional)
    chat_messages = load_chat_messages(input_path)

    # Render
    html = render(graph_data, template, chat_messages)

    # Output path
    if args.out:
        out_path = Path(args.out)
    else:
        title = ""
        if "meta" in graph_data and graph_data["meta"]:
            title = graph_data["meta"].get("title", "")
        slug = slugify(title) if title else input_path.stem
        out_path = input_path.parent / f"ymindmap-{slug}.html"

    out_path.write_text(html, encoding="utf-8")
    print(f"Rendered: {out_path}")

    if args.screenshot:
        shot_path = out_path.with_suffix(".png")
        _take_screenshot(out_path, shot_path)

    return 0


def _take_screenshot(html_path: Path, out_path: Path) -> None:
    """Start a temp HTTP server and use Playwright to screenshot the graph."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Warning: playwright not installed, skipping screenshot. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        return

    # Pick a free port
    import socket
    with socket.socket() as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    # Serve from the HTML file's directory
    serve_dir = html_path.parent

    class _QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(serve_dir), **kw)
        def log_message(self, *_):
            pass

    server = HTTPServer(("127.0.0.1", port), _QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}/{html_path.name}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
            page.goto(url, wait_until="networkidle")
            # Wait for D3 simulation to settle
            time.sleep(3)
            # Hide chat panel, re-fit graph, then screenshot
            page.evaluate("""
                document.body.classList.remove('split-mode');
                ['chatPanel','splitDivider'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.display = 'none';
                });
                if (typeof fitAll === 'function') fitAll(400);
            """)
            time.sleep(0.6)
            page.screenshot(path=str(out_path), full_page=False)
            browser.close()
        print(f"Screenshot: {out_path}")
    finally:
        server.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
