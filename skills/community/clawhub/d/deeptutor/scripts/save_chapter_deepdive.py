#!/usr/bin/env python3
"""
save_chapter_deepdive.py — Save a chapter deepdive to Obsidian and maintain navigation links.

Usage:
    python3 scripts/save_chapter_deepdive.py \
        --book "Supercommunicators" \
        --chapter 1 \
        --title "The Matching Principle" \
        --content-file /tmp/ch1_deepdive.md

    # Or pipe content:
    echo "# Chapter 1 deepdive..." | python3 scripts/save_chapter_deepdive.py \
        --book "Supercommunicators" \
        --chapter 1 \
        --title "The Matching Principle"
"""

import argparse
import sys
import re
from pathlib import Path

VAULT = Path('/data/workspace/obsidian-vault/Books')


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def save_deepdive(book: str, chapter: int, title: str, content: str) -> Path:
    book_dir = VAULT / slugify(book)
    book_dir.mkdir(parents=True, exist_ok=True)

    filename = f"chapter-{chapter}-{slugify(title)}.md"
    filepath = book_dir / filename
    filepath.write_text(content, encoding='utf-8')
    print(f"Saved: {filepath}")

    # Update navigation index
    update_index(book_dir, book)
    return filepath


def update_index(book_dir: Path, book_name: str):
    """Regenerate the book's index.md with links to all chapters."""
    chapters = sorted(book_dir.glob('chapter-*.md'))
    if not chapters:
        return

    lines = [f'# {book_name} — Reading Notes\n']
    lines.append(f'Total chapters read: {len(chapters)}\n')

    for ch_path in chapters:
        # Extract chapter number and title from filename
        match = re.match(r'chapter-(\d+)-(.+)\.md', ch_path.name)
        if match:
            num = match.group(1)
            title_slug = match.group(2).replace('-', ' ').title()
            lines.append(f'- [[{ch_path.stem}|Chapter {num}: {title_slug}]]')

    index_path = book_dir / 'index.md'
    index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Updated index: {index_path}")

    # Add prev/next nav links to each chapter file
    for i, ch_path in enumerate(chapters):
        text = ch_path.read_text(encoding='utf-8')

        # Remove old nav block if exists
        text = re.sub(r'\n---\n\n## 章节导航\n.*$', '', text, flags=re.DOTALL)

        nav = ['\n---\n\n## 章节导航\n']
        if i > 0:
            prev = chapters[i - 1]
            nav.append(f'← [[{prev.stem}|上一章]]')
        if i < len(chapters) - 1:
            nxt = chapters[i + 1]
            nav.append(f'→ [[{nxt.stem}|下一章]]')
        nav.append(f'📚 [[index|返回目录]]')

        text += '\n'.join(nav) + '\n'
        ch_path.write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', required=True)
    parser.add_argument('--chapter', type=int, required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--content-file', help='Read content from file')
    args = parser.parse_args()

    if args.content_file:
        content = Path(args.content_file).read_text(encoding='utf-8')
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("Error: provide --content-file or pipe content via stdin", file=sys.stderr)
        sys.exit(1)

    save_deepdive(args.book, args.chapter, args.title, content)


if __name__ == '__main__':
    main()
