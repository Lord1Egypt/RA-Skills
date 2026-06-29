#!/usr/bin/env python3
"""
extract_epub.py — Extract text from EPUB files using ebooklib + BeautifulSoup.
Usage: python3 extract_epub.py <input.epub> <output.txt>
"""

import sys
import os
from pathlib import Path


def extract_epub(input_path: str, output_path: str) -> None:
    try:
        from ebooklib import epub
        from bs4 import BeautifulSoup
    except ImportError:
        import subprocess
        python = str(Path.home() / ".workbuddy/binaries/python/envs/default/bin/python3")
        subprocess.run([python, "-m", "pip", "install", "ebooklib", "beautifulsoup4", "-q"], check=True)
        from ebooklib import epub
        from bs4 import BeautifulSoup

    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting text from: {input_path}")

    book = epub.read_epub(input_path)
    all_text = []
    item_count = 0

    for item in book.get_items():
        if item.get_type() == 9:  # ITEM_DOCUMENT
            soup = BeautifulSoup(item.get_content(), "html.parser")

            # Try to get chapter title from headings
            title = ""
            for tag in ["h1", "h2", "h3"]:
                h = soup.find(tag)
                if h:
                    title = h.get_text(strip=True)
                    break

            text = soup.get_text(separator="\n", strip=True)
            if text:
                header = f"\n{'='*60}\n{title or f'Section {item_count+1}'}\n{'='*60}\n"
                all_text.append(header + text)
                item_count += 1

    output = "\n".join(all_text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Done! Extracted {item_count} sections.")
    print(f"Output: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_epub.py <input.epub> <output.txt>")
        sys.exit(1)
    extract_epub(sys.argv[1], sys.argv[2])
