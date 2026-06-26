#!/usr/bin/env python3
"""Download and cache the ebook database from jbiaojerry.github.io."""

import json
import os
import sys
import time
import urllib.request
import ssl
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "ebook-search"
CACHE_FILE = CACHE_DIR / "all-books.json"
CACHE_MAX_AGE = 86400  # 24 hours

DATABASE_URL = "https://jbiaojerry.github.io/ebook-treasure-chest/all-books.json"


def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def is_cache_valid():
    if not CACHE_FILE.exists():
        return False
    age = time.time() - CACHE_FILE.stat().st_mtime
    return age < CACHE_MAX_AGE


def download_database():
    """Download the all-books.json database."""
    ensure_cache_dir()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(DATABASE_URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    print(f"Downloading database from {DATABASE_URL}...", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            data = resp.read()
            # Write to temp file first, then rename for atomicity
            tmp_file = CACHE_FILE.with_suffix(".tmp")
            tmp_file.write_bytes(data)
            tmp_file.rename(CACHE_FILE)
            print(f"Downloaded {len(data)} bytes, saved to {CACHE_FILE}", file=sys.stderr)
            return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        return False


def load_books():
    """Load books from cache, downloading if needed."""
    if not is_cache_valid():
        if not download_database():
            if CACHE_FILE.exists():
                print("Using stale cache", file=sys.stderr)
            else:
                print("No cache available", file=sys.stderr)
                return []

    return extract_complete_books(CACHE_FILE)


def extract_complete_books(filepath):
    """Extract complete book objects from a potentially truncated JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Fallback: extract complete objects manually
    books = []
    depth = 0
    in_string = False
    escape = False
    obj_start = -1

    for i, c in enumerate(content):
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
            if depth == 1:
                obj_start = i
        elif c == '}':
            depth -= 1
            if depth == 0 and obj_start >= 0:
                try:
                    obj = json.loads(content[obj_start:i+1])
                    books.append(obj)
                except json.JSONDecodeError:
                    pass
                obj_start = -1

    return books


def search(keyword, books=None):
    """Search books by title, author, or category."""
    if books is None:
        books = load_books()

    if not keyword or not keyword.strip():
        return []

    k = keyword.lower().strip()
    keywords = k.split()

    results = []
    for b in books:
        title = (b.get("title") or "").lower()
        author = (b.get("author") or "").lower()
        category = (b.get("category") or "").lower()
        text = f"{title} {author} {category}"

        if all(kw in text for kw in keywords):
            results.append(b)

    return results


def format_book(book, index=None):
    """Format a book for display."""
    title = book.get("title", "Unknown")
    author = book.get("author", "Unknown")
    category = book.get("category", "Unknown")
    formats = ", ".join(book.get("formats", []))
    link = book.get("link", "")

    prefix = f"{index}. " if index else ""
    result = f"{prefix}《{title}》— {author} [{category}] ({formats})"
    if link:
        result += f"\n   下载: {link}"
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ebook search tool")
    subparsers = parser.add_subparsers(dest="command")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for books")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("-l", "--limit", type=int, default=20, help="Max results")
    search_parser.add_argument("--category", help="Filter by category")

    # Update command
    subparsers.add_parser("update", help="Update the database cache")

    # Stats command
    subparsers.add_parser("stats", help="Show database statistics")

    # Categories command
    subparsers.add_parser("categories", help="List all categories")

    args = parser.parse_args()

    if args.command == "update":
        download_database()

    elif args.command == "stats":
        books = load_books()
        print(f"Total books: {len(books)}")
        cats = {}
        for b in books:
            cat = b.get("category", "Unknown")
            cats[cat] = cats.get(cat, 0) + 1
        print(f"Categories: {len(cats)}")
        print("Top 10 categories:")
        for cat, count in sorted(cats.items(), key=lambda x: -x[1])[:10]:
            print(f"  {cat}: {count}")

    elif args.command == "categories":
        books = load_books()
        cats = {}
        for b in books:
            cat = b.get("category", "Unknown")
            cats[cat] = cats.get(cat, 0) + 1
        for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"{cat}: {count}")

    elif args.command == "search":
        books = load_books()
        results = search(args.keyword, books)

        if args.category:
            results = [b for b in results if args.category.lower() in (b.get("category") or "").lower()]

        print(f"Found {len(results)} results for '{args.keyword}'")
        print("---")
        for i, book in enumerate(results[:args.limit], 1):
            print(format_book(book, i))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
