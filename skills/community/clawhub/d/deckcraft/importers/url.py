"""
DeckCraft v6 — URL → Markdown Importer

Fetches a URL and converts to Markdown for use as a DeckCraft outline source.

Usage (via CLI):
    python3 scripts/import_source.py url https://example.com -o output.md
    python3 scripts/import_source.py url https://example.com -o outline.json --to-outline
"""
import subprocess
import sys
import os
import re
import json
from typing import Optional


def _fetch_via_openclaw(url: str) -> Optional[str]:
    """Try fetching via openclaw CLI's web_fetch."""
    try:
        result = subprocess.run(
            ["openclaw", "web-fetch", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _fetch_via_curl(url: str) -> Optional[str]:
    """Fetch raw HTML via curl."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "20",
             "-A", "Mozilla/5.0 (compatible; DeckCraft/6.0)",
             url],
            capture_output=True, text=True, timeout=25,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _html_to_markdown(html: str) -> str:
    """Convert HTML to Markdown using basic heuristics.

    Tries html2text first (if installed), then falls back to a simple regex-based extractor.
    """
    # Try html2text
    try:
        import html2text
        h = html2text.HTML2HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # no wrapping
        return h.handle(html)
    except ImportError:
        pass

    # Fallback: simple regex-based extraction
    text = html

    # Remove scripts and styles
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert headings
    for i in range(1, 7):
        text = re.sub(
            rf'<h{i}[^>]*>(.*?)</h{i}>',
            '#' * i + r' \1',
            text, flags=re.DOTALL | re.IGNORECASE,
        )

    # Convert paragraphs → double newline
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert line breaks
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Convert bold/strong
    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert italic/em
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert links
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # Convert list items
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def url_to_markdown(url: str, output_path: Optional[str] = None) -> str:
    """Fetch a URL and convert to Markdown.

    Args:
        url: The URL to fetch.
        output_path: Optional file path to save the Markdown.

    Returns:
        Markdown string.

    Raises:
        RuntimeError: If the URL cannot be fetched.
    """
    # Try openclaw CLI first (handles JS rendering)
    md_content = _fetch_via_openclaw(url)

    # Fallback: curl + html2text
    if not md_content:
        html = _fetch_via_curl(url)
        if html:
            md_content = _html_to_markdown(html)

    if not md_content:
        raise RuntimeError(
            f"Failed to fetch URL: {url}\n"
            "Tips:\n"
            "  - Check your network connection\n"
            "  - The site may require JavaScript (try installing html2text: pip install html2text)\n"
            "  - The URL may be invalid or the server may be down"
        )

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                    exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✓ Saved Markdown from {url} → {output_path} ({len(md_content)} chars)")

    return md_content
