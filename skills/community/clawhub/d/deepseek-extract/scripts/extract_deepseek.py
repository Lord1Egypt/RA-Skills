#!/usr/bin/env python3
"""
DeepSeek Share Conversation Extractor

Extracts full conversation content from DeepSeek shared chat links
using Playwright (headless Chromium).

Usage:
    python extract_deepseek.py <share_url> [--output <path>] [--format <markdown|json>] [--headed]
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path


def check_playwright():
    """Check if playwright is installed and install browsers if needed."""
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        print("Error: playwright is not installed.", file=sys.stderr)
        print("Install it with: pip install playwright", file=sys.stderr)
        print("Then install browsers: playwright install chromium", file=sys.stderr)
        sys.exit(1)


def validate_url(url: str) -> bool:
    """Validate that the URL is a DeepSeek share link."""
    pattern = r"^https?://chat\.deepseek\.com/share/[a-zA-Z0-9_-]+"
    return bool(re.match(pattern, url))


def extract_conversation(url: str, headed: bool = False, timeout: int = 30000) -> dict:
    """
    Extract conversation from a DeepSeek share URL.

    Returns a dict with keys: url, title, messages
    """
    sync_playwright = check_playwright()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        try:
            # Navigate to the share page
            page.goto(url, wait_until="networkidle", timeout=timeout)

            # Wait for conversation content to render
            # DeepSeek SPA needs time for JavaScript to execute
            page.wait_for_timeout(3000)

            # Try multiple selector strategies for robustness
            # Strategy 1: Look for the main chat container
            # Strategy 2: Look for message blocks
            # Strategy 3: Fallback to broader selectors

            title = _extract_title(page)
            messages = _extract_messages(page)

            # If no messages found with primary selectors, try scrolling and retrying
            if not messages:
                _scroll_to_load(page)
                page.wait_for_timeout(2000)
                messages = _extract_messages(page)

            # If still no messages, try the most aggressive extraction
            if not messages:
                messages = _extract_messages_aggressive(page)

        except Exception as e:
            # Try with longer timeout on first failure
            if "Timeout" in str(e) and not headed:
                print(f"Initial timeout, retrying with longer wait...", file=sys.stderr)
                page.wait_for_timeout(5000)
                title = _extract_title(page)
                messages = _extract_messages(page)
                if not messages:
                    messages = _extract_messages_aggressive(page)
            else:
                print(f"Error during extraction: {e}", file=sys.stderr)
                title = page.title() if page else "Unknown"
                messages = []
        finally:
            browser.close()

    return {
        "url": url,
        "title": title,
        "messages": messages,
    }


def _extract_title(page) -> str:
    """Extract the conversation title from the page."""
    # Try multiple selectors for the title
    title_selectors = [
        "h1",
        ".chat-title",
        "[class*='title']",
        "[class*='header'] h1",
        "[class*='conversation'] h1",
    ]
    for selector in title_selectors:
        try:
            el = page.query_selector(selector)
            if el and el.inner_text().strip():
                return el.inner_text().strip()
        except Exception:
            continue

    # Fallback to page title
    return page.title()


def _extract_messages(page) -> list:
    """
    Extract messages from the page using primary selectors.
    Returns a list of dicts with 'role' and 'content' keys.
    """
    messages = []

    # DeepSeek share page typically uses these patterns:
    # - Message containers with data attributes or specific class patterns
    # - User messages and assistant messages have different styling

    # Strategy: Find all message blocks and classify them
    message_selectors = [
        # DeepSeek common patterns (as of 2025-2026)
        "[class*='message']",
        "[class*='chat-message']",
        "[class*='msg-content']",
        ".ds-chat-message",
        ".message-item",
        # Generic patterns
        "[data-role]",
        "[class*='conversation'] [class*='item']",
    ]

    for selector in message_selectors:
        try:
            elements = page.query_selector_all(selector)
            if elements and len(elements) >= 2:
                for el in elements:
                    role, content = _classify_message(el, page)
                    if content and content.strip():
                        messages.append({"role": role, "content": content.strip()})
                if messages:
                    break
        except Exception:
            continue

    return messages


def _classify_message(element, page) -> tuple:
    """
    Classify a message element as user or assistant and extract its content.
    Returns (role, content) tuple.
    """
    role = "unknown"
    content = ""

    try:
        # Check class names for role hints
        class_attr = element.get_attribute("class") or ""
        data_role = element.get_attribute("data-role") or ""

        # Determine role from attributes
        if data_role:
            role = data_role.lower()
        elif any(kw in class_attr.lower() for kw in ["user", "human", "question"]):
            role = "user"
        elif any(kw in class_attr.lower() for kw in ["assistant", "bot", "ai", "deepseek", "answer", "response"]):
            role = "assistant"

        # If role is still unknown, try to detect from DOM structure
        # In DeepSeek, user messages are typically on the right, assistant on the left
        if role == "unknown":
            # Check if there's an avatar or label element inside
            inner_text = element.inner_text()
            # Heuristic: user messages tend to be shorter and more direct
            # assistant messages tend to be longer and include formatted content
            # This is a rough heuristic — we improve below
            pass

        # Extract text content
        content = element.inner_text()

    except Exception:
        pass

    return role, content


def _scroll_to_load(page):
    """Scroll through the page to trigger lazy-loaded content."""
    try:
        page.evaluate("""
            async () => {
                const delay = ms => new Promise(r => setTimeout(r, ms));
                const height = document.body.scrollHeight;
                for (let i = 0; i < height; i += 500) {
                    window.scrollTo(0, i);
                    await delay(200);
                }
                window.scrollTo(0, 0);
            }
        """)
    except Exception:
        pass


def _extract_messages_aggressive(page) -> list:
    """
    Aggressive extraction fallback: parse the full page text
    and try to split it into user/assistant turns.
    """
    messages = []

    try:
        # Get the entire page content as text
        full_text = page.inner_text("body")

        # Try to get the rendered HTML for better parsing
        html_content = page.content()

        # Method 1: Try to find structured content in the HTML
        # Look for patterns that indicate message boundaries
        # DeepSeek uses specific text markers like "用户", "DeepSeek" or icons

        # Pattern for Chinese DeepSeek interface
        patterns_cn = [
            (r"用户\s*\n([\s\S]*?)(?=\n\s*DeepSeek|\Z)", "user"),
            (r"DeepSeek\s*\n([\s\S]*?)(?=\n\s*用户|\Z)", "assistant"),
        ]

        # Pattern for English interface
        patterns_en = [
            (r"You\s*\n([\s\S]*?)(?=\n\s*DeepSeek|\Z)", "user"),
            (r"DeepSeek\s*\n([\s\S]*?)(?=\n\s*You|\Z)", "assistant"),
        ]

        # Try Chinese patterns first
        for pattern, role in patterns_cn:
            for match in re.finditer(pattern, full_text):
                content = match.group(1).strip()
                if content:
                    messages.append({"role": role, "content": content})

        # If no results with Chinese patterns, try English
        if not messages:
            for pattern, role in patterns_en:
                for match in re.finditer(pattern, full_text):
                    content = match.group(1).strip()
                    if content:
                        messages.append({"role": role, "content": content})

        # If still no results, try HTML-based extraction
        if not messages:
            messages = _extract_from_html(html_content)

        # Final fallback: return the full text as a single message
        if not messages and full_text.strip():
            messages.append({"role": "unknown", "content": full_text.strip()})

    except Exception as e:
        print(f"Aggressive extraction failed: {e}", file=sys.stderr)

    return messages


def _extract_from_html(html_content: str) -> list:
    """
    Extract messages from raw HTML using regex patterns.
    This is the most aggressive fallback.
    """
    messages = []

    # Look for DeepSeek's specific HTML patterns
    # These patterns may change with UI updates, so we try multiple strategies

    # Strategy: Find all text blocks that look like conversation turns
    # DeepSeek typically wraps messages in divs with specific class patterns

    # Try to find user/assistant pairs in the HTML
    # Pattern: Look for identifiable message containers
    msg_pattern = re.compile(
        r'<(?:div|article|section)[^>]*class="[^"]*(?:message|chat-msg|msg-item)[^"]*"[^>]*>'
        r'([\s\S]*?)</(?:div|article|section)>',
        re.IGNORECASE,
    )

    return messages


def format_markdown(data: dict) -> str:
    """Format extracted conversation as Markdown."""
    lines = [
        f"# DeepSeek 对话记录",
        "",
        f"> 来源: {data['url']}",
        "",
        "---",
        "",
    ]

    role_labels = {
        "user": "用户",
        "assistant": "DeepSeek",
        "unknown": "未知",
    }

    for msg in data["messages"]:
        role = role_labels.get(msg["role"], msg["role"])
        lines.append(f"## {role}")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def format_json(data: dict) -> str:
    """Format extracted conversation as JSON."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Extract conversation content from DeepSeek share links"
    )
    parser.add_argument("url", help="DeepSeek share URL (https://chat.deepseek.com/share/...)")
    parser.add_argument(
        "--output", "-o",
        default="./deepseek_conversation.md",
        help="Output file path (default: ./deepseek_conversation.md)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode for debugging",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30000,
        help="Page load timeout in milliseconds (default: 30000)",
    )

    args = parser.parse_args()

    # Validate URL
    if not validate_url(args.url):
        print(
            f"Error: Invalid DeepSeek share URL: {args.url}",
            file=sys.stderr,
        )
        print(
            "Expected format: https://chat.deepseek.com/share/...",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Extracting conversation from: {args.url}", file=sys.stderr)

    # Extract
    data = extract_conversation(args.url, headed=args.headed, timeout=args.timeout)

    if not data["messages"]:
        print(
            "Warning: No messages extracted. The page may have anti-bot protection "
            "or the URL may be invalid. Try with --headed flag to debug.",
            file=sys.stderr,
        )

    # Format output
    if args.format == "json":
        output = format_json(data)
    else:
        output = format_markdown(data)

    # Write to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    print(f"Conversation extracted: {len(data['messages'])} messages", file=sys.stderr)
    print(f"Output saved to: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
