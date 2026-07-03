#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_wechat_html.py — Convert Markdown to WeChat-compatible inline-style HTML.

Generates clean, styled HTML from Markdown with Clockless design tokens,
ready for WeChat Official Account publishing.

Usage:
    python md_to_wechat_html.py --input article.md --output wechat.html --title "Article Title"

Dependencies: markdown (auto-installed if missing)
"""

import argparse
import re
import sys
from pathlib import Path

# Fix Windows console encoding (GBK → UTF-8)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    print("[INFO] Installing markdown...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.toc import TocExtension


# ── Clockless Design Tokens (resolved, no CSS variables) ──
COLORS = {
    "primary": "#a03b00",
    "primary_container": "#c94c00",
    "bg": "#ffffff",
    "surface": "#fafafa",
    "surface_low": "#f5f5f5",
    "fg": "#1e1b19",
    "fg_secondary": "#594138",
    "fg_muted": "#8d7166",
    "border": "rgba(0,0,0,0.06)",
    "border_strong": "rgba(0,0,0,0.12)",
}

FONTS = {
    "headline": "-apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    "body": "-apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
    "mono": "'SF Mono', 'Menlo', 'Courier New', monospace",
}


def build_header(title: str) -> str:
    """Build the article masthead."""
    return f'''<div style="padding:40px 24px 32px;margin:0 0 24px;background:linear-gradient(135deg,{COLORS["primary"]} 0%,{COLORS["primary_container"]} 100%);border-radius:14px;text-align:center;">
  <div style="font-size:26px;font-weight:700;color:#ffffff;letter-spacing:-0.3px;line-height:1.3;">{title}</div>
</div>'''


def style_html(html_content: str) -> str:
    """Apply WeChat-safe inline styles to converted HTML."""

    # Style headings
    html_content = re.sub(
        r'<h1([^>]*)>(.*?)</h1>',
        lambda m: f'<h1 style="font-size:24px;font-weight:700;color:{COLORS["fg"]};margin:32px 0 16px;padding-bottom:10px;border-bottom:2px solid {COLORS["primary"]};letter-spacing:-0.3px;font-family:{FONTS["headline"]};">{m.group(2)}</h1>',
        html_content,
    )
    html_content = re.sub(
        r'<h2([^>]*)>(.*?)</h2>',
        lambda m: f'<h2 style="font-size:20px;font-weight:700;color:{COLORS["fg"]};margin:28px 0 14px;padding-bottom:8px;border-bottom:1px solid {COLORS["border_strong"]};font-family:{FONTS["headline"]};">{m.group(2)}</h2>',
        html_content,
    )
    html_content = re.sub(
        r'<h3([^>]*)>(.*?)</h3>',
        lambda m: f'<h3 style="font-size:17px;font-weight:600;color:{COLORS["primary_container"]};margin:24px 0 12px;font-family:{FONTS["headline"]};">{m.group(2)}</h3>',
        html_content,
    )
    html_content = re.sub(
        r'<h4([^>]*)>(.*?)</h4>',
        lambda m: f'<h4 style="font-size:15px;font-weight:600;color:{COLORS["fg_secondary"]};margin:20px 0 10px;font-family:{FONTS["headline"]};">{m.group(2)}</h4>',
        html_content,
    )

    # Style paragraphs
    html_content = re.sub(
        r'<p>',
        f'<p style="font-size:15px;color:{COLORS["fg"]};line-height:1.8;margin:0 0 16px;font-family:{FONTS["body"]};">',
        html_content,
    )

    # Style strong / bold
    html_content = re.sub(
        r'<strong>(.*?)</strong>',
        lambda m: f'<strong style="color:{COLORS["fg"]};font-weight:700;">{m.group(1)}</strong>',
        html_content,
    )

    # Style emphasis
    html_content = re.sub(
        r'<em>(.*?)</em>',
        lambda m: f'<em style="color:{COLORS["primary"]};">{m.group(1)}</em>',
        html_content,
    )

    # Style links
    html_content = re.sub(
        r'<a([^>]*)href="([^"]*)"([^>]*)>(.*?)</a>',
        lambda m: f'<a href="{m.group(2)}" style="color:{COLORS["primary"]};text-decoration:underline;font-weight:500;">{m.group(4)}</a>',
        html_content,
    )

    # Style lists
    html_content = re.sub(
        r'<ul>',
        '<ul style="margin:8px 0 16px 0;padding-left:24px;">',
        html_content,
    )
    html_content = re.sub(
        r'<ol>',
        '<ol style="margin:8px 0 16px 0;padding-left:24px;">',
        html_content,
    )
    html_content = re.sub(
        r'<li>',
        f'<li style="font-size:15px;color:{COLORS["fg"]};line-height:1.8;margin-bottom:6px;font-family:{FONTS["body"]};">',
        html_content,
    )

    # Style blockquotes
    html_content = re.sub(
        r'<blockquote>',
        f'<blockquote style="margin:16px 0;padding:14px 20px;background:{COLORS["surface"]};border-left:4px solid {COLORS["primary"]};border-radius:0 10px 10px 0;">',
        html_content,
    )

    # Style tables
    html_content = re.sub(
        r'<table>',
        f'<table style="width:100%;border-collapse:collapse;font-size:14px;margin:16px 0;background:#ffffff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(30,27,25,0.06);">',
        html_content,
    )
    html_content = re.sub(
        r'<thead>',
        '<thead>',
        html_content,
    )
    html_content = re.sub(
        r'<th>',
        f'<th style="padding:11px 14px;text-align:left;color:#ffffff;font-weight:600;font-size:13px;border:none;background:{COLORS["primary"]};">',
        html_content,
    )
    html_content = re.sub(
        r'<td>',
        f'<td style="padding:10px 14px;border-bottom:1px solid {COLORS["border"]};color:{COLORS["fg_secondary"]};font-size:14px;">',
        html_content,
    )
    html_content = re.sub(
        r'<tr>',
        '<tr style="background:#ffffff;">',
        html_content,
    )

    # Style code blocks
    html_content = re.sub(
        r'<pre><code([^>]*)>',
        f'<pre style="margin:16px 0;padding:14px 18px;background:{COLORS["surface_low"]};border-radius:8px;overflow-x:auto;"><code style="font-family:{FONTS["mono"]};font-size:13px;color:{COLORS["fg"]};line-height:1.6;">',
        html_content,
    )
    html_content = re.sub(
        r'<code>',
        f'<code style="font-family:{FONTS["mono"]};font-size:13px;color:{COLORS["primary"]};background:{COLORS["surface"]};padding:2px 6px;border-radius:4px;">',
        html_content,
    )

    # Style images
    html_content = re.sub(
        r'<img([^>]*)src="([^"]*)"([^>]*)alt="([^"]*)"([^>]*)>',
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(4)}" style="max-width:100%;height:auto;border-radius:8px;margin:12px 0;display:block;">',
        html_content,
    )
    html_content = re.sub(
        r'<img([^>]*)src="([^"]*)"([^>]*)>',
        lambda m: f'<img src="{m.group(2)}" style="max-width:100%;height:auto;border-radius:8px;margin:12px 0;display:block;">'
        if 'style=' not in m.group(0)
        else m.group(0),
        html_content,
    )

    # Style horizontal rules
    html_content = re.sub(
        r'<hr\s*/?>',
        f'<hr style="border:none;border-top:1px solid {COLORS["border_strong"]};margin:32px 0;">',
        html_content,
    )

    return html_content


def convert_md_to_wechat(input_path: str, output_path: str, title: str = ""):
    """Convert Markdown file to WeChat-compatible HTML."""
    print(f"[READ] Reading: {input_path}")
    md_text = Path(input_path).read_text(encoding="utf-8")

    # Extract title from first H1 if not provided
    if not title:
        h1_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
            md_text = re.sub(r'^#\s+.+$', '', md_text, count=1, flags=re.MULTILINE)
        else:
            title = Path(input_path).stem

    # Convert Markdown to HTML
    md = markdown.Markdown(
        extensions=[
            TableExtension(),
            FencedCodeExtension(),
            TocExtension(),
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
        ]
    )
    raw_html = md.convert(md_text)

    # Apply WeChat styles
    styled_html = style_html(raw_html)

    # Build final document
    header = build_header(title)

    # Wrap in section (WeChat prefers <section> over <div>)
    final_html = f'''<section style="max-width:680px;margin:0 auto;padding:20px 16px;font-family:{FONTS["body"]};color:{COLORS["fg"]};line-height:1.8;background-color:{COLORS["bg"]};">
{header}
{styled_html}
</section>'''

    # Write output
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(final_html, encoding="utf-8")

    size = len(final_html.encode("utf-8"))
    print(f"[DONE] WeChat-ready HTML: {output_path}")
    print(f"[INFO] Title: {title}")
    print(f"[INFO] Output size: {size} bytes ({size / 1024:.1f} KB)")

    if size > 2 * 1024 * 1024:
        print("[WARN] Output exceeds WeChat's 2MB limit!")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to WeChat-compatible inline-style HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md_to_wechat_html.py --input article.md --output wechat.html
  python md_to_wechat_html.py --input article.md --output wechat.html --title "My Article"
        """,
    )
    parser.add_argument("--input", required=True, help="Input Markdown file path")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--title", default="", help="Article title (auto-detected from H1 if omitted)")

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    convert_md_to_wechat(str(input_file), args.output, args.title)


if __name__ == "__main__":
    main()
