"""
DeckCraft v6 — WeChat Article → Markdown Importer

Fetches WeChat public account (微信公众号) articles and converts to Markdown.

Usage (via CLI):
    python3 scripts/import_source.py wechat https://mp.weixin.qq.com/s/xxx -o output.md

WeChat articles have specific requirements:
- Custom User-Agent (WeChat browser UA)
- Referer header
- Need to extract article body from #js_content div
"""
import subprocess
import sys
import os
import re
import json
from typing import Optional


# WeChat in-app browser User-Agent
WECHAT_UA = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro Build/UQ1A.240205.004) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
    "Chrome/122.0.6261.119 Mobile Safari/537.36 "
    "MicroMessenger/8.0.47.2544(0x28002F38) NetType/WIFI Language/zh_CN"
)

WECHAT_REFERER = "https://mp.weixin.qq.com/"


def _is_wechat_url(url: str) -> bool:
    """Check if URL is a WeChat article."""
    return "mp.weixin.qq.com" in url


def _fetch_wechat_html(url: str) -> Optional[str]:
    """Fetch WeChat article HTML with proper headers."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "30",
             "-A", WECHAT_UA,
             "-e", WECHAT_REFERER,
             "-H", "Accept: text/html,application/xhtml+xml",
             "-H", "Accept-Language: zh-CN,zh;q=0.9",
             url],
            capture_output=True, text=True, timeout=35,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _extract_wechat_content(html: str) -> str:
    """Extract article content from WeChat HTML.

    WeChat articles store the main content in:
    - <div id="js_content">...</div> (main article body)
    - Title in <h1 id="activity-name"> or <meta property="og:title">
    - Author in <span id="js_author_name"> or similar
    """
    # Extract title
    title = ""
    title_match = re.search(
        r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>',
        html, re.DOTALL | re.IGNORECASE,
    )
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    if not title:
        og_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html, re.IGNORECASE)
        if og_match:
            title = og_match.group(1).strip()

    # Extract author
    author = ""
    author_match = re.search(
        r'<span[^>]*id="js_author_name"[^>]*>(.*?)</span>',
        html, re.DOTALL | re.IGNORECASE,
    )
    if author_match:
        author = re.sub(r'<[^>]+>', '', author_match.group(1)).strip()

    # Extract main content
    content_match = re.search(
        r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*(?:<script|<div\s+class="rich_media_tool)',
        html, re.DOTALL | re.IGNORECASE,
    )
    if not content_match:
        # Fallback: try to get everything between js_content and the next major div
        content_match = re.search(
            r'<div[^>]*id="js_content"[^>]*>(.*)',
            html, re.DOTALL | re.IGNORECASE,
        )

    content_html = content_match.group(1) if content_match else html

    # Convert to Markdown
    md = _wechat_html_to_md(content_html)

    # Prepend title and author
    parts = []
    if title:
        parts.append(f"# {title}")
    if author:
        parts.append(f"*{author}*\n")
    if md:
        parts.append(md)

    return "\n\n".join(parts)


def _wechat_html_to_md(html: str) -> str:
    """Convert WeChat article HTML to Markdown."""
    text = html

    # Remove scripts and styles
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert headings
    for i in range(1, 7):
        text = re.sub(
            rf'<h{i}[^>]*>(.*?)</h{i}>',
            '#' * min(i + 1, 6) + r' \1',
            text, flags=re.DOTALL | re.IGNORECASE,
        )

    # Convert <section> tags (WeChat uses lots of these) → pass through
    text = re.sub(r'</?section[^>]*>', '\n', text, flags=re.IGNORECASE)

    # Convert paragraphs
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL | re.IGNORECASE)

    # Convert <br>
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Bold/strong
    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.DOTALL | re.IGNORECASE)

    # Italic/em
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.DOTALL | re.IGNORECASE)

    # Images — WeChat uses data-src for lazy loading
    def img_replace(m):
        src = m.group(1) or m.group(2) or ""
        if src:
            return f"![image]({src})"
        return ""
    text = re.sub(
        r'<img[^>]*(?:data-src|src)=["\']([^"\']*)["\'][^>]*>',
        img_replace, text, flags=re.IGNORECASE,
    )

    # Links
    text = re.sub(
        r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>',
        r'[\2](\1)', text, flags=re.DOTALL | re.IGNORECASE,
    )

    # List items
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')

    # Clean up
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def wechat_to_markdown(url: str, output_path: Optional[str] = None) -> str:
    """Fetch a WeChat article and convert to Markdown.

    Args:
        url: WeChat article URL (mp.weixin.qq.com).
        output_path: Optional file path to save.

    Returns:
        Markdown string.

    Raises:
        ValueError: If URL is not a WeChat article.
        RuntimeError: If fetch fails.
    """
    if not _is_wechat_url(url):
        raise ValueError(
            f"Not a WeChat article URL: {url}\n"
            "Expected URL containing 'mp.weixin.qq.com'"
        )

    html = _fetch_wechat_html(url)
    if not html:
        raise RuntimeError(
            f"Failed to fetch WeChat article: {url}\n"
            "Tips:\n"
            "  - The article may have been deleted\n"
            "  - Network may be blocked\n"
            "  - Try opening the URL in a browser first"
        )

    md_content = _extract_wechat_content(html)

    if not md_content.strip():
        raise RuntimeError(
            f"Fetched WeChat page but extracted no content from: {url}\n"
            "The page structure may have changed or the article may be empty."
        )

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
                    exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✓ Saved WeChat article → {output_path} ({len(md_content)} chars)")

    return md_content
