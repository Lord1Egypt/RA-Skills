from __future__ import annotations

import json
import posixpath
import re
import unicodedata
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from bs4 import BeautifulSoup, Tag

HTML_TYPES = {
    "application/xhtml+xml",
    "text/html",
}

REMOVAL_TAGS = {
    "nav",
    "script",
    "style",
    "noscript",
    "template",
    "svg",
}

BLOCK_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "blockquote",
    "li",
}


def slugify(value: str, fallback: str = "item") -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return clean or fallback


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_zip_text(archive: zipfile.ZipFile, member_path: str) -> str:
    raw = archive.read(member_path)
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def resolve_href(base_path: str, href: str) -> str:
    clean_href = unquote((href or "").split("#", 1)[0])
    joined = posixpath.join(posixpath.dirname(base_path), clean_href)
    return posixpath.normpath(joined)


def relative_to(base_dir: Path, target: Path) -> str:
    return str(target.resolve().relative_to(base_dir.resolve()))


def _walk_block_tags(node: Tag) -> list[Tag]:
    blocks: list[Tag] = []
    for child in node.children:
        if not isinstance(child, Tag):
            continue
        if child.name in BLOCK_TAGS:
            blocks.append(child)
            continue
        blocks.extend(_walk_block_tags(child))
    return blocks


def extract_markdown_from_html(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all(REMOVAL_TAGS):
        tag.decompose()

    body = soup.body or soup
    links = body.find_all("a")
    total_text = normalize_whitespace(body.get_text(" ", strip=True))
    link_chars = sum(
        len(normalize_whitespace(link.get_text(" ", strip=True)))
        for link in links
    )

    title = ""
    title_tag = body.find(["h1", "h2", "h3", "title"]) or soup.title
    if title_tag:
        title = normalize_whitespace(title_tag.get_text(" ", strip=True))

    blocks: list[str] = []
    for tag in _walk_block_tags(body):
        text = normalize_whitespace(tag.get_text(" ", strip=True))
        if not text:
            continue

        if tag.name and re.fullmatch(r"h[1-6]", tag.name):
            level = int(tag.name[1])
            rendered = f"{'#' * level} {text}"
        elif tag.name == "blockquote":
            rendered = f"> {text}"
        elif tag.name == "li":
            rendered = f"- {text}"
        else:
            rendered = text

        if not blocks or blocks[-1] != rendered:
            blocks.append(rendered)

    markdown = "\n\n".join(blocks).strip()

    # 增强统计
    raw_text = body.get_text(" ", strip=True)
    paragraphs = re.split(r"\n\s*\n", raw_text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    headings = body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    images = body.find_all("img")
    tables = body.find_all("table")

    return {
        "title": title,
        "markdown": markdown,
        "stats": {
            "total_chars": len(total_text),
            "word_count": len(total_text.split()),
            "link_chars": link_chars,
            "anchor_count": len(links),
            "block_count": len(blocks),
            "paragraph_count": len(paragraphs),
            "heading_count": len(headings),
            "image_count": len(images),
            "table_count": len(tables),
        },
    }


def is_probably_noise_page(
    title: str,
    text: str,
    href: str,
    stats: dict[str, Any],
) -> bool:
    normalized_title = normalize_whitespace(title).lower()
    normalized_text = normalize_whitespace(text).lower()
    normalized_href = (href or "").lower()

    total_chars = int(stats.get("total_chars", 0))
    link_chars = int(stats.get("link_chars", 0))
    anchor_count = int(stats.get("anchor_count", 0))
    link_ratio = (link_chars / total_chars) if total_chars else 0.0

    if not normalized_text or total_chars < 40:
        return True

    nav_keywords = {
        "toc",
        "table of contents",
        "contents",
        "navigation",
        "目录",
        "导航",
    }
    copyright_keywords = {
        "copyright",
        "all rights reserved",
        "isbn",
        "publisher",
        "published by",
        "版权所有",
    }
    ad_keywords = {
        "also by",
        "other books",
        "more from",
        "coming soon",
        "advertisement",
        "advertising",
        "推荐",
        "更多作品",
    }

    if any(keyword in normalized_href for keyword in ("toc", "nav", "contents")):
        if link_ratio > 0.45 or total_chars < 2500:
            return True

    if any(keyword in normalized_title for keyword in nav_keywords):
        if link_ratio > 0.35 or anchor_count >= 4:
            return True

    if any(keyword in normalized_title for keyword in copyright_keywords):
        if total_chars < 2500:
            return True

    if any(keyword in normalized_text for keyword in copyright_keywords):
        if total_chars < 2200:
            return True

    if any(keyword in normalized_title for keyword in ad_keywords):
        if total_chars < 3000:
            return True

    if any(keyword in normalized_text for keyword in ad_keywords):
        if total_chars < 2500:
            return True

    if link_ratio > 0.7 and anchor_count >= 4:
        return True

    return False


def dump_frontmatter(data: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in data.items():
        if value is None:
            rendered = '""'
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            text = str(value).replace('"', '\\"')
            rendered = f'"{text}"'
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip())
    return "\n".join(lines).rstrip() + "\n"