#!/usr/bin/env python3
"""
epub_chapter_reader.py — Extract chapters from EPUB files.

Usage:
    python3 scripts/epub_chapter_reader.py <epub_path> --list
    python3 scripts/epub_chapter_reader.py <epub_path> --chapter 1
    python3 scripts/epub_chapter_reader.py <epub_path> --chapter 1 --max-chars 8000
"""

import argparse
import re
import sys
from pathlib import Path

from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


def extract_chapters(epub_path: str) -> list[dict]:
    """Parse an EPUB and return a list of chapters with title and text."""
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        name = item.get_name()
        # Skip non-content files (nav, toc, cover, copyright, etc.)
        if any(skip in name.lower() for skip in ['nav', 'toc', 'cover', 'cop', 'ded', 'ack', 'titl', 'half']):
            continue

        html = item.get_content()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text('\n', strip=True)
        text = re.sub(r'\n{3,}', '\n\n', text)

        if len(text.strip()) < 200:
            continue

        # Try to extract chapter title from first heading or first line
        title = None
        for tag in ['h1', 'h2', 'h3']:
            heading = soup.find(tag)
            if heading:
                title = heading.get_text(strip=True)
                break
        if not title:
            first_line = text.strip().split('\n')[0][:100]
            title = first_line

        chapters.append({
            'index': len(chapters) + 1,
            'file': name,
            'title': title,
            'text': text,
            'chars': len(text),
        })

    return chapters


def list_chapters(chapters: list[dict]) -> str:
    lines = []
    for ch in chapters:
        lines.append(f"  {ch['index']:2d}. {ch['title']} ({ch['chars']:,} chars)")
    return '\n'.join(lines)


def get_chapter(chapters: list[dict], num: int, max_chars: int = 0) -> str:
    if num < 1 or num > len(chapters):
        return f"Error: chapter {num} not found. Book has {len(chapters)} chapters."
    ch = chapters[num - 1]
    text = ch['text']
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[... truncated at {max_chars} chars, full chapter is {ch['chars']:,} chars ...]"
    return f"# {ch['title']}\n\n{text}"


def main():
    parser = argparse.ArgumentParser(description='Extract chapters from EPUB')
    parser.add_argument('epub', help='Path to EPUB file')
    parser.add_argument('--list', action='store_true', help='List all chapters')
    parser.add_argument('--chapter', '-c', type=int, help='Chapter number to extract')
    parser.add_argument('--max-chars', type=int, default=0, help='Max chars to output (0=unlimited)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    epub_path = args.epub
    if not Path(epub_path).exists():
        # Try common locations
        for candidate in [
            f'/root/.openclaw/media/inbound/{epub_path}',
            f'/data/workspace/obsidian-vault/Books/{epub_path}',
        ]:
            if Path(candidate).exists():
                epub_path = candidate
                break

    if not Path(epub_path).exists():
        print(f"Error: file not found: {epub_path}", file=sys.stderr)
        sys.exit(1)

    chapters = extract_chapters(epub_path)

    if args.list:
        print(f"Found {len(chapters)} chapters in: {Path(epub_path).name}\n")
        print(list_chapters(chapters))
    elif args.chapter:
        if args.json:
            import json
            ch = chapters[args.chapter - 1] if 0 < args.chapter <= len(chapters) else None
            if ch:
                text = ch['text']
                if args.max_chars and len(text) > args.max_chars:
                    text = text[:args.max_chars]
                print(json.dumps({'title': ch['title'], 'index': ch['index'], 'chars': ch['chars'], 'text': text}, ensure_ascii=False))
            else:
                print(json.dumps({'error': f'chapter {args.chapter} not found'}))
        else:
            print(get_chapter(chapters, args.chapter, args.max_chars))
    else:
        print("Use --list to see chapters, or --chapter N to extract one.")
        sys.exit(1)


if __name__ == '__main__':
    main()
