#!/usr/bin/env python3
"""
Purple highlight keywords on a webpage and take a screenshot.
Uses Playwright to open URL, inject purple highlights, then screenshot.

Usage:
    python3 purple_highlight_screenshot.py <url> <output.png> <keyword1> [keyword2] ...

Example:
    python3 purple_highlight_screenshot.py https://example.com out.png "alpha testing" "defects"
"""

import sys
import json
import re
import subprocess
from playwright.sync_api import sync_playwright


def smart_keyword_match(page, keywords: list[str], timeout_sec: int = 20) -> list[str]:
    """Extract page text, use LLM to find exact matching substrings.

    Opens the current page, extracts visible text, sends it to LLM with the
    original keywords, and returns only substrings that exist verbatim in the
    page. Falls back to original keywords on any error.
    """
    if not keywords:
        return []

    # Extract visible page text
    try:
        page_text = page.evaluate('() => document.body.innerText')
    except Exception:
        return keywords

    if not page_text or not page_text.strip():
        return keywords

    prompt = (
        'You are given text extracted from a web page and a list of search keywords.\n'
        'For each keyword, find the EXACT substring(s) from the page text that best match it semantically.\n'
        'CRITICAL RULES:\n'
        '1. Only return substrings that appear VERBATIM in the page text below.\n'
        '2. If a keyword has no good match in the text, skip it silently.\n'
        '3. Prefer shorter, more precise matches (1-4 words each).\n'
        '4. Consider synonyms and rewordings when matching (e.g. "improved" matches "enhanced").\n'
        '5. For numeric keywords, prefer matches that appear near the numbers.\n'
        f'--- PAGE TEXT ---\n{page_text}\n--- END ---\n\n'
        f'Keywords: {json.dumps(keywords)}\n\n'
        'Return ONLY a JSON array of exact matching substrings found in the page text, nothing else.'
    )

    try:
        proc = subprocess.run(
            ['openclaw', 'infer', 'model', 'run', '--prompt', prompt, '--json'],
            capture_output=True, text=True, timeout=timeout_sec
        )
        if proc.returncode != 0:
            return keywords
        result = json.loads(proc.stdout)
        outputs = result.get('outputs', [])
        if not outputs:
            return keywords
        text = outputs[0].get('text', '')
        text = re.sub(r'^```(?:json)?\s*\n?', '', text.strip())
        text = re.sub(r'\n?```\s*$', '', text)
        matches = json.loads(text)
        if isinstance(matches, list) and len(matches) > 0:
            # Verify each match exists in page text (safety check)
            page_lower = page_text.lower()
            verified = [m for m in matches if isinstance(m, str) and m.lower() in page_lower]
            if verified:
                return verified
    except Exception:
        pass

    return keywords


def load_keywords_for_url(keywords_file: str, url: str) -> list[str]:
    """Load keywords from verification_keywords.json for the given URL.

    Reads the JSON file, finds all entries whose URL matches (normalized),
    merges their keywords deduplicating while preserving order.
    Returns list of keyword strings, or empty list if no match.
    """
    try:
        with open(keywords_file) as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading keywords file: {e}", file=sys.stderr)
        return []

    footnotes = data.get("footnotes", [])
    matched_keywords = []
    seen = set()
    url_normalized = url.rstrip('/').lower()

    for entry in footnotes:
        entry_url = entry.get("url", "").rstrip('/').lower()
        if entry_url == url_normalized:
            for kw in entry.get("keywords", []):
                kw_text = kw.get("text", kw) if isinstance(kw, dict) else kw
                if kw_text not in seen:
                    seen.add(kw_text)
                    matched_keywords.append(kw_text)

    return matched_keywords


def highlight_and_screenshot(url: str, output: str, keywords: list[str], timeout_ms: int = 30000, smart_mode: bool = False):
    """Open URL, highlight keywords with purple, take screenshot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            locale="en-US",
        )
        page = context.new_page()

        # Navigate: prefer networkidle; fallback to load for noisy sites
        try:
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
        except Exception:
            # Sites with persistent analytics/WebSocket never reach networkidle
            try:
                page.goto(url, wait_until="load", timeout=min(timeout_ms, 60000))
            except Exception as e2:
                print(json.dumps({"ok": False, "url": url, "error": f"goto: {e2}"}))
                browser.close()
                return False

        # Extra wait for dynamic content (SPA / React / delayed rendering)
        page.wait_for_timeout(5000)
        # Poll until body text populates (SPA rendering can lag far behind load events)
        try:
            page.wait_for_function(
                """() => {
                    const text = document.body.innerText.trim();
                    return text.length > 100;
                }""",
                timeout=30000
            )
        except Exception:
            pass  # Proceed even if body text never grows (static pages may have < 100 chars)

        # Inject CSS for purple highlight style
        page.evaluate("""
            () => {
                const style = document.createElement('style');
                style.textContent = `
                    .skill-purple-highlight {
                        background-color: rgba(128, 0, 128, 0.25) !important;
                        outline: 2px solid rgba(128, 0, 128, 0.6) !important;
                        outline-offset: 1px !important;
                        border-radius: 2px !important;
                    }
                `;
                document.head.appendChild(style);
            }
        """)

        # --- Smart mode: page-aware LLM keyword matching ---
        if smart_mode and keywords:
            print(f"[smart] Extracting page text and matching keywords via LLM...", file=sys.stderr)
            keywords = smart_keyword_match(page, keywords)
            print(f"[smart] LLM returned {len(keywords)} matched keywords: {keywords}", file=sys.stderr)

        # Highlight each keyword
        highlight_count = 0
        for kw in keywords:
            count = page.evaluate("""
                (keyword) => {
                    const walker = document.createTreeWalker(
                        document.body,
                        NodeFilter.SHOW_TEXT,
                        null,
                        false
                    );
                    const textNodes = [];
                    let node;
                    while (node = walker.nextNode()) {
                        if (node.textContent.toLowerCase().includes(keyword.toLowerCase())) {
                            textNodes.push(node);
                        }
                    }
                    let highlighted = 0;
                    for (const textNode of textNodes) {
                        const text = textNode.textContent;
                        const idx = text.toLowerCase().indexOf(keyword.toLowerCase());
                        if (idx === -1) continue;
                        const before = text.substring(0, idx);
                        const match = text.substring(idx, idx + keyword.length);
                        const after = text.substring(idx + keyword.length);
                        const span = document.createElement('span');
                        span.className = 'skill-purple-highlight';
                        span.textContent = match;
                        const parent = textNode.parentNode;
                        if (before) parent.insertBefore(document.createTextNode(before), textNode);
                        parent.insertBefore(span, textNode);
                        if (after) parent.insertBefore(document.createTextNode(after), textNode);
                        parent.removeChild(textNode);
                        highlighted++;
                        // Only highlight first 5 occurrences per keyword
                        if (highlighted >= 5) break;
                    }
                    return highlighted;
                }
            """, kw)
            highlight_count += count

        # Count highlights visible in viewport
        visible_count = page.evaluate("""
            () => {
                const els = document.querySelectorAll('.skill-purple-highlight');
                const vw = window.innerWidth;
                const vh = window.innerHeight;
                let visible = 0;
                for (const el of els) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 &&
                        r.right > 0 && r.left < vw &&
                        r.bottom > 0 && r.top < vh) {
                        visible++;
                    }
                }
                return visible;
            }
        """)

        # Extract page text for grade assessment and claim alignment
        try:
            page_body_text = page.evaluate('() => document.body.innerText')
        except Exception:
            page_body_text = ""

        # Take full-page screenshot so all highlights are visible
        page.screenshot(path=output, full_page=True)
        browser.close()

        result = {
            "ok": True,
            "url": url,
            "output": output,
            "keywords": keywords,
            "highlighted_count": highlight_count,
            "visible_highlighted_count": highlight_count,  # all highlights visible in full-page
            "body_text": page_body_text,
        }
        print(json.dumps(result))
        return True


def main():
    smart_mode = False
    keywords_file = None
    args = sys.argv[1:]

    if '--smart' in args:
        smart_mode = True
        args.remove('--smart')

    if '--keywords-file' in args:
        idx = args.index('--keywords-file')
        if idx + 1 >= len(args):
            print("Error: --keywords-file requires a file path argument", file=sys.stderr)
            sys.exit(1)
        keywords_file = args[idx + 1]
        # Remove --keywords-file and its value from args
        args = args[:idx] + args[idx+2:]

    if len(args) < 2:
        print("Usage: python3 purple_highlight_screenshot.py [--smart] [--keywords-file <path>] <url> <output.png> [keyword1 keyword2 ...]")
        sys.exit(1)

    url = args[0]
    output = args[1]

    if keywords_file:
        keywords = load_keywords_for_url(keywords_file, url)
        if not keywords:
            print(f"Warning: No keywords found for URL {url} in {keywords_file}", file=sys.stderr)
    else:
        if len(args) < 3:
            print("Usage: python3 purple_highlight_screenshot.py [--smart] [--keywords-file <path>] <url> <output.png> [keyword1 keyword2 ...]")
            sys.exit(1)
        keywords = args[2:]

    success = highlight_and_screenshot(url, output, keywords, smart_mode=smart_mode)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
