#!/usr/bin/env python3
"""Read-only Calibre metadata.db queries for OpenClaw skills."""

from __future__ import annotations

import argparse
import datetime
import html
import inspect
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any


DEFAULT_DB = None


def log_event(level: str, message: str, **params):
    """
    Register event in PDCL structured format (captures line automatically)
    
    Args:
        level: Log level (INFO, ALERT, ERROR, SUCCESS, DEBUG, START, END, DATA, TOOL, CACHE, SAVE)
        message: Event message
        **params: Additional parameters
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emoji_map = {
        'INFO': 'ℹ️',
        'ALERT': '⚠️',
        'ERROR': '❌',
        'SUCCESS': '✅',
        'DEBUG': '🔍',
        'START': '🚀',
        'END': '🏁',
        'DATA': '📊',
        'TOOL': '🔧',
        'CACHE': '📂',
        'SAVE': '💾'
    }
    emoji = emoji_map.get(level, 'ℹ️')
    
    # Automatically captures file, function, and line
    frame = inspect.currentframe().f_back
    file = inspect.getfile(frame)
    func = inspect.getframeinfo(frame).function
    line = inspect.getframeinfo(frame).lineno
    
    param_str = ''
    if params:
        param_str = ' - ' + ', '.join(f'{k}={v}' for k, v in params.items())
    
    print(f"[{timestamp}] [{file}:{func}:{line}] {emoji} {message}{param_str}", file=sys.stderr)


def connect(db_path: str) -> sqlite3.Connection:
    log_event('START', 'Connecting to Calibre database', db_path=db_path)
    if not db_path:
        raise SystemExit("metadata.db path is not configured. Use the calibre-ebooks Books API first, or pass --db / set CALIBRE_METADATA_DB for local fallback.")
    db = Path(db_path)
    if not db.exists():
        log_event('ERROR', 'Database not found', db_path=str(db))
        raise SystemExit(f"metadata.db not found: {db}")
    uri = f"file:{db}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    log_event('SUCCESS', 'Connection established successfully', db_path=db_path)
    return conn


def clean_html(value: str | None) -> str | None:
    if value is None:
        return None
    text = re.sub(r"<[^>]+>", " ", value)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part for part in value.split("||") if part]


def book_select(where: str = "", order_limit: str = "") -> str:
    return f"""
        SELECT
            b.id,
            b.title,
            b.author_sort,
            b.path,
            b.pubdate,
            b.timestamp,
            b.last_modified,
            b.uuid,
            (
                SELECT group_concat(a.name, '||')
                FROM books_authors_link bal
                JOIN authors a ON a.id = bal.author
                WHERE bal.book = b.id
                ORDER BY bal.id
            ) AS authors,
            (
                SELECT group_concat(d.format, '||')
                FROM data d
                WHERE d.book = b.id
                ORDER BY d.format
            ) AS formats,
            (
                SELECT group_concat(t.name, '||')
                FROM books_tags_link btl
                JOIN tags t ON t.id = btl.tag
                WHERE btl.book = b.id
                ORDER BY t.name
            ) AS tags,
            (
                SELECT group_concat(l.lang_code, '||')
                FROM books_languages_link bll
                JOIN languages l ON l.id = bll.lang_code
                WHERE bll.book = b.id
                ORDER BY l.lang_code
            ) AS languages,
            (
                SELECT group_concat(p.name, '||')
                FROM books_publishers_link bpl
                JOIN publishers p ON p.id = bpl.publisher
                WHERE bpl.book = b.id
                ORDER BY p.name
            ) AS publishers,
            (
                SELECT group_concat(i.type || ':' || i.val, '||')
                FROM identifiers i
                WHERE i.book = b.id
                ORDER BY i.type
            ) AS identifiers,
            (
                SELECT s.name
                FROM books_series_link bsl
                JOIN series s ON s.id = bsl.series
                WHERE bsl.book = b.id
                LIMIT 1
            ) AS series,
            (
                SELECT c.text
                FROM comments c
                WHERE c.book = b.id
                LIMIT 1
            ) AS comments
        FROM books b
        {where}
        {order_limit}
    """


def row_to_book(row: sqlite3.Row, include_comments: bool = False) -> dict[str, Any]:
    book = {
        "id": row["id"],
        "title": row["title"],
        "authors": split_csv(row["authors"]) or ([row["author_sort"]] if row["author_sort"] else []),
        "formats": split_csv(row["formats"]),
        "tags": split_csv(row["tags"]),
        "languages": split_csv(row["languages"]),
        "publishers": split_csv(row["publishers"]),
        "series": row["series"],
        "identifiers": split_csv(row["identifiers"]),
        "pubdate": row["pubdate"],
        "path": row["path"],
        "uuid": row["uuid"],
    }
    if include_comments:
        book["comments"] = clean_html(row["comments"])
    return book


def list_books(conn: sqlite3.Connection, limit: int, offset: int) -> list[dict[str, Any]]:
    log_event('START', 'Listing books', limit=limit, offset=offset)
    rows = conn.execute(
        book_select(order_limit="ORDER BY b.sort COLLATE NOCASE LIMIT ? OFFSET ?"),
        (limit, offset),
    ).fetchall()
    books = [row_to_book(row) for row in rows]
    log_event('DATA', 'Books listed', count=len(books))
    log_event('SUCCESS', 'Listing completed', count=len(books))
    return books


def random_book(conn: sqlite3.Connection, include_comments: bool = True) -> dict[str, Any]:
    log_event('START', 'Selecting random book')
    row = conn.execute(book_select(order_limit="ORDER BY RANDOM() LIMIT 1")).fetchone()
    if row is None:
        log_event('ERROR', 'No books found for random selection')
        raise SystemExit("no books found in Calibre database")
    book = row_to_book(row, include_comments=include_comments)
    log_event('SUCCESS', 'Random book selected', book_id=book["id"], title=book["title"])
    return book


def search_books(conn: sqlite3.Connection, query: str, limit: int) -> list[dict[str, Any]]:
    log_event('START', 'Searching books', query=query, limit=limit)
    pattern = f"%{query}%"
    rows = conn.execute(
        book_select(
            where="""
                WHERE b.title LIKE ? COLLATE NOCASE
                   OR b.author_sort LIKE ? COLLATE NOCASE
                   OR EXISTS (
                       SELECT 1
                       FROM books_authors_link bal
                       JOIN authors a ON a.id = bal.author
                       WHERE bal.book = b.id AND a.name LIKE ? COLLATE NOCASE
                   )
                   OR EXISTS (
                       SELECT 1
                       FROM books_tags_link btl
                       JOIN tags t ON t.id = btl.tag
                       WHERE btl.book = b.id AND t.name LIKE ? COLLATE NOCASE
                   )
            """,
            order_limit="ORDER BY b.sort COLLATE NOCASE LIMIT ?",
        ),
        (pattern, pattern, pattern, pattern, limit),
    ).fetchall()
    books = [row_to_book(row) for row in rows]
    log_event('DATA', 'Results found', count=len(books), query=query)
    log_event('SUCCESS', 'Search completed', count=len(books))
    return books


def metadata(conn: sqlite3.Connection, book_id: int) -> dict[str, Any]:
    log_event('START', 'Getting book metadata', book_id=book_id)
    row = conn.execute(book_select(where="WHERE b.id = ?"), (book_id,)).fetchone()
    if row is None:
        log_event('ERROR', 'Book not found', book_id=book_id)
        raise SystemExit(f"book id not found: {book_id}")
    book = row_to_book(row, include_comments=True)
    log_event('SUCCESS', 'Metadata obtained successfully', book_id=book_id)
    return book


def format_path(conn: sqlite3.Connection, db_path: str, book_id: int, fmt: str | None) -> dict[str, Any]:
    log_event('START', 'Getting file path', book_id=book_id, format=fmt)
    book = metadata(conn, book_id)
    library_dir = Path(db_path).resolve().parent

    query = "SELECT format, name FROM data WHERE book = ?"
    params: tuple[Any, ...] = (book_id,)
    if fmt:
        query += " AND upper(format) = upper(?)"
        params = (book_id, fmt)
    query += " ORDER BY format"

    rows = conn.execute(query, params).fetchall()
    formats = []
    for row in rows:
        extension = row["format"].lower()
        filename = f"{row['name']}.{extension}"
        file_path = library_dir / book["path"] / filename
        formats.append(
            {
                "format": row["format"],
                "path": str(file_path),
                "exists": file_path.exists(),
            }
        )

    log_event('DATA', 'Formats found', count=len(formats), book_id=book_id)
    log_event('SUCCESS', 'Paths obtained successfully', book_id=book_id)
    return {"book": book, "formats": formats}


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main(argv: list[str]) -> int:
    log_event('START', 'Starting calibre_query')
    parser = argparse.ArgumentParser(description="Read-only queries for a Calibre metadata.db")
    parser.add_argument("--db", default=os.environ.get("CALIBRE_METADATA_DB") or DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List books")
    list_parser.add_argument("--limit", type=int, default=20)
    list_parser.add_argument("--offset", type=int, default=0)

    random_parser = sub.add_parser("random", help="Show one random book")
    random_parser.add_argument("--no-comments", action="store_true", help="Do not include comments/synopsis")

    search_parser = sub.add_parser("search", help="Search by title, author, or tag")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=20)

    meta_parser = sub.add_parser("metadata", help="Show one book metadata")
    meta_parser.add_argument("book_id", type=int)

    path_parser = sub.add_parser("path", help="Show filesystem path for book formats")
    path_parser.add_argument("book_id", type=int)
    path_parser.add_argument("--format", dest="fmt")

    args = parser.parse_args(argv)
    log_event('INFO', 'Command received', command=args.command)
    conn = connect(args.db)

    if args.command == "list":
        print_json(list_books(conn, args.limit, args.offset))
    elif args.command == "random":
        print_json(random_book(conn, include_comments=not args.no_comments))
    elif args.command == "search":
        print_json(search_books(conn, args.query, args.limit))
    elif args.command == "metadata":
        print_json(metadata(conn, args.book_id))
    elif args.command == "path":
        print_json(format_path(conn, args.db, args.book_id, args.fmt))

    log_event('END', 'Command completed successfully', command=args.command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
