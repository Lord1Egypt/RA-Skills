#!/usr/bin/env python3
"""Convert an EPUB file into a structured directory of Markdown files.

Usage:
    uv run scripts/convert.py <file.epub> [output_dir]
    uv run scripts/convert.py <file.epub> [output_dir] --overwrite
"""
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "ebooklib>=0.18",
#   "beautifulsoup4>=4.12",
#   "markdownify>=0.11",
# ]
# ///

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import unquote

import ebooklib
from bs4 import BeautifulSoup, Comment
from ebooklib import epub
from markdownify import markdownify as md


@dataclass
class ChapterInfo:
    index: int
    title: str
    slug: str
    filename: str
    word_count: int = 0


@dataclass
class BookMeta:
    title: str
    language: str
    authors: List[str] = field(default_factory=list)
    description: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[str] = None
    subjects: List[str] = field(default_factory=list)
    identifiers: List[str] = field(default_factory=list)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:60].strip("-") or "chapter"


_CJK_RANGES = (
    (0x3400, 0x4DBF),   # CJK Unified Ideographs Extension A
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x3040, 0x309F),   # Hiragana
    (0x30A0, 0x30FF),   # Katakana
    (0x31F0, 0x31FF),   # Katakana Phonetic Extensions
    (0xAC00, 0xD7AF),   # Hangul Syllables
    (0x1100, 0x11FF),   # Hangul Jamo
    (0x3130, 0x318F),   # Hangul Compatibility Jamo
)


def is_cjk(char: str) -> bool:
    code = ord(char)
    return any(start <= code <= end for start, end in _CJK_RANGES)


def word_count(text: str) -> int:
    meaningful = [c for c in text if not c.isspace()]
    if not meaningful:
        return 0

    cjk_count = sum(1 for c in meaningful if is_cjk(c))
    if cjk_count / len(meaningful) > 0.2:
        return cjk_count

    return len(text.split())


def extract_metadata(book: epub.EpubBook) -> BookMeta:
    def get_list(key: str) -> List[str]:
        data = book.get_metadata("DC", key)
        return [x[0] for x in data if x and x[0]] if data else []

    def get_one(key: str) -> Optional[str]:
        data = book.get_metadata("DC", key)
        return data[0][0] if data and data[0] and data[0][0] else None

    return BookMeta(
        title=get_one("title") or "Untitled",
        language=get_one("language") or "en",
        authors=get_list("creator"),
        description=get_one("description"),
        publisher=get_one("publisher"),
        date=get_one("date"),
        subjects=get_list("subject"),
        identifiers=get_list("identifier"),
    )


def parse_toc(toc_list) -> List[tuple[str, str]]:
    result: List[tuple[str, str]] = []
    for item in toc_list:
        if isinstance(item, tuple):
            section, children = item
            href = getattr(section, "href", "") or ""
            title = getattr(section, "title", None) or "Untitled"
            result.append((title, href.split("#")[0]))
            result.extend(parse_toc(children))
        elif isinstance(item, epub.Link):
            href = item.href or ""
            result.append(((item.title or "Untitled"), href.split("#")[0]))
        elif isinstance(item, epub.Section):
            href = getattr(item, "href", "") or ""
            result.append(((item.title or "Untitled"), href.split("#")[0]))
    return result


def clean_soup(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup(["script", "style", "iframe", "nav", "form", "button", "input"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()
    return soup


def rewrite_image_srcs(soup: BeautifulSoup, image_map: dict[str, str]) -> BeautifulSoup:
    for img in soup.find_all("img"):
        src = unquote(img.get("src", ""))
        fname = os.path.basename(src)
        if src in image_map:
            img["src"] = f"../images/{image_map[src]}"
        elif fname in image_map:
            img["src"] = f"../images/{image_map[fname]}"
    return soup


def html_to_markdown(html: str) -> str:
    return md(html, heading_style="ATX", bullets="-", newline_style="backslash")


def ensure_output_dir(output_dir: Path, overwrite: bool) -> None:
    if not output_dir.exists():
        return
    if not output_dir.is_dir():
        raise ValueError(f"Output path exists and is not a directory: {output_dir}")
    if not overwrite:
        raise ValueError(
            f"Output directory already exists: {output_dir}\\n"
            "Choose a different output directory or pass --overwrite to replace it."
        )
    shutil.rmtree(output_dir)


def sanitize_filename(name: str, fallback: str) -> str:
    cleaned = re.sub(r"[^\w.\-]", "_", name).strip("._")
    return cleaned or fallback


def escape_table_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def yaml_scalar(value: Optional[str]) -> str:
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def yaml_list(values: List[str]) -> str:
    return json.dumps([str(v) for v in values], ensure_ascii=False)


def convert(epub_path: Path, output_dir: Path, overwrite: bool = False) -> dict:
    print(f"Loading {epub_path} ...")
    book = epub.read_epub(str(epub_path))
    meta = extract_metadata(book)

    ensure_output_dir(output_dir, overwrite=overwrite)

    chapters_dir = output_dir / "chapters"
    images_dir = output_dir / "images"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting images ...")
    image_map: dict[str, str] = {}
    used_image_names: dict[str, int] = {}

    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_IMAGE:
            continue

        original = os.path.basename(item.get_name())
        base, ext = os.path.splitext(original)
        safe_base = sanitize_filename(base, "image")
        safe_ext = ext if ext else ".bin"

        count = used_image_names.get(f"{safe_base}{safe_ext}", 0)
        safe_name = f"{safe_base}{safe_ext}" if count == 0 else f"{safe_base}-{count + 1}{safe_ext}"
        used_image_names[f"{safe_base}{safe_ext}"] = count + 1

        dest = images_dir / safe_name
        dest.write_bytes(item.get_content())
        image_map[item.get_name()] = safe_name
        image_map[original] = safe_name

    toc_entries = parse_toc(book.toc)
    href_to_title: dict[str, str] = {}
    for title, file_href in toc_entries:
        key = os.path.basename(file_href) if file_href else ""
        if key and key not in href_to_title:
            href_to_title[key] = title

    print("Converting chapters ...")
    chapters: List[ChapterInfo] = []
    seen_slugs: dict[str, int] = {}

    for item_id, _linear in book.spine:
        item = book.get_item_with_id(item_id)
        if not item or item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        item_href_base = os.path.basename(item.get_name())
        title = (
            href_to_title.get(item_href_base)
            or href_to_title.get(item.get_name())
            or item_href_base.replace(".html", "").replace(".xhtml", "").replace("_", " ").title()
            or "Untitled"
        )

        base_slug = slugify(title)
        seen_slugs[base_slug] = seen_slugs.get(base_slug, 0) + 1
        slug = base_slug if seen_slugs[base_slug] == 1 else f"{base_slug}-{seen_slugs[base_slug]}"

        index = len(chapters) + 1
        filename = f"{index:03d}_{slug}.md"

        raw = item.get_content().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(raw, "html.parser")
        soup = clean_soup(soup)
        soup = rewrite_image_srcs(soup, image_map)

        body = soup.find("body")
        inner_html = "".join(str(x) for x in body.contents) if body else str(soup)

        markdown_body = html_to_markdown(inner_html).strip()
        cleaned_text = re.sub(r"[#*`\[\]()>-]", "", markdown_body)
        wc = word_count(cleaned_text)

        chapter_md = f"# {title}\n\n{markdown_body}\n"
        (chapters_dir / filename).write_text(chapter_md, encoding="utf-8")

        chapters.append(
            ChapterInfo(
                index=index,
                title=title,
                slug=slug,
                filename=filename,
                word_count=wc,
            )
        )

    print("Writing META.md ...")
    _write_meta(output_dir, meta, chapters, epub_path)

    summary = {
        "title": meta.title,
        "authors": meta.authors,
        "total_chapters": len(chapters),
        "total_words": sum(c.word_count for c in chapters),
        "output_dir": str(output_dir),
        "images": len({*image_map.values()}),
    }

    print(f"\nDone. Output: {output_dir}/")
    print(f"  Chapters : {summary['total_chapters']}")
    print(f"  Images   : {summary['images']}")
    return summary


def _write_meta(output_dir: Path, meta: BookMeta, chapters: List[ChapterInfo], source: Path) -> None:
    total_words = sum(c.word_count for c in chapters)

    lines = [
        "---",
        f"title: {yaml_scalar(meta.title)}",
        f"authors: {yaml_list(meta.authors)}",
        f"language: {yaml_scalar(meta.language)}",
    ]
    if meta.publisher:
        lines.append(f"publisher: {yaml_scalar(meta.publisher)}")
    if meta.date:
        lines.append(f"date: {yaml_scalar(meta.date)}")
    if meta.subjects:
        lines.append(f"subjects: {yaml_list(meta.subjects)}")
    if meta.identifiers:
        lines.append(f"identifiers: {yaml_list(meta.identifiers)}")
    lines.extend(
        [
            f"source: {yaml_scalar(source.name)}",
            f"processed_at: {yaml_scalar(datetime.now().isoformat(timespec='seconds'))}",
            f"total_chapters: {len(chapters)}",
            f"total_words: {total_words}",
            "---",
            "",
            f"# {meta.title}",
            "",
        ]
    )

    if meta.description:
        lines.extend(["## Description", "", meta.description.strip(), ""])

    lines.extend([
        "## Table of Contents",
        "",
        "| # | Title | File | Words |",
        "|---|-------|------|-------|",
    ])
    for chapter in chapters:
        lines.append(
            f"| {chapter.index} | {escape_table_cell(chapter.title)} | "
            f"chapters/{chapter.filename} | {chapter.word_count} |"
        )

    lines.extend(
        [
            "",
            "## Structure",
            "",
            "- `META.md` — read this first for metadata and navigation",
            "- `chapters/` — one Markdown file per chapter",
            "- `images/` — extracted image assets referenced by chapters",
            f"- Total words (approx): {total_words:,}",
            "",
        ]
    )

    (output_dir / "META.md").write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert an EPUB file into an AI-friendly Markdown library."
    )
    parser.add_argument("epub_file", help="Path to the EPUB file")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Output directory (default: beside the EPUB, named after the file stem)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing output directory",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    epub_file = Path(args.epub_file).expanduser().resolve()
    if not epub_file.exists():
        print(f"Error: file not found: {epub_file}", file=sys.stderr)
        return 1
    if epub_file.suffix.lower() != ".epub":
        print(f"Error: expected an .epub file, got: {epub_file.name}", file=sys.stderr)
        return 1

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else epub_file.with_suffix("")
    )

    try:
        summary = convert(epub_file, output_dir, overwrite=args.overwrite)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    authors = ", ".join(summary["authors"]) if summary["authors"] else "Unknown"
    print("\nSuggested agent reply:\n")
    print("✅ Conversion complete\n")
    print(f"Title   : {summary['title']}")
    print(f"Authors : {authors}")
    print(f"Chapters: {summary['total_chapters']}")
    print(f"Words   : {summary['total_words']}")
    print(f"Output  : {summary['output_dir']}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
