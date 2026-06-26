#!/usr/bin/env python3
"""
End-to-end article saver for ClawNoter Obsidian.
Fetches article content, downloads images, and writes an Obsidian note.
"""

import json
import os
import re
import sys
from datetime import datetime

from download_images import extract_title_from_html, process_article


INVALID_FILENAME_CHARS = r'[<>:"/\\|?*]'


def sanitize_filename(name):
    cleaned = re.sub(INVALID_FILENAME_CHARS, '', (name or '').strip())
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.rstrip('. ')
    return cleaned or f"article-{datetime.now().strftime('%Y-%m-%d')}"


def strip_reader_preamble(markdown):
    if not markdown:
        return ""

    text = markdown.replace('\r', '').strip()
    text = re.sub(r'^Title:\s.*?\n+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^URL Source:\s.*?\n+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^Published Time:\s.*?\n+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^Markdown Content:\s*\n?', '', text, flags=re.IGNORECASE)
    return text.strip()


def extract_title(markdown, html, url, preferred_title=""):
    markdown = strip_reader_preamble(markdown)

    if preferred_title:
        preferred_title = preferred_title.strip()

    heading_match = re.match(r'^#\s+(.+?)\s*$', markdown)
    if heading_match:
        title = heading_match.group(1).strip()
        remaining = markdown[heading_match.end():].lstrip()
        return title, remaining

    if preferred_title:
        return preferred_title, markdown

    html_title = extract_title_from_html(html)
    if html_title:
        return html_title, markdown

    return url, markdown


def build_callout(markdown):
    lines = markdown.splitlines()
    rendered = ["> [!note]- 📄 Full Article"]
    if not lines:
        return "\n".join(rendered)

    for line in lines:
        rendered.append(">" if not line else f"> {line}")
    return "\n".join(rendered)


def build_note_content(title, url, page_comment, article_markdown):
    created = datetime.now().strftime("%Y/%m/%d")
    frontmatter = "\n".join([
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f'url: "{url}"',
        f'created: "{created}"',
        f'pagecomment: "{(page_comment or "").replace(chr(34), chr(39))}"',
        "---",
        "",
    ])

    parts = [frontmatter, build_callout(article_markdown)]
    if page_comment:
        parts.extend(["", f"> {page_comment}", "^note-user"])
    return "\n".join(parts).rstrip() + "\n"


def save_article(url, output_dir, page_comment=""):
    result = process_article(url, output_dir)
    raw_markdown = result.get("markdown", "") or ""
    html = result.get("html", "") or ""
    preferred_title = result.get("title", "") or ""

    title, article_markdown = extract_title(raw_markdown, html, url, preferred_title)
    article_markdown = article_markdown.strip()

    filename = sanitize_filename(title) + ".md"
    output_path = os.path.join(output_dir, filename)
    note_content = build_note_content(title, url, page_comment, article_markdown)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(note_content)

    return {
        "title": title,
        "path": output_path,
        "images": result.get("images", []),
        "image_count": len(result.get("images", [])),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_article.py <url> <output_dir> [page_comment]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = os.path.abspath(os.path.expanduser(sys.argv[2]))
    page_comment = sys.argv[3] if len(sys.argv) > 3 else ""

    os.makedirs(output_dir, exist_ok=True)
    saved = save_article(url, output_dir, page_comment)
    print(json.dumps(saved, ensure_ascii=False))
