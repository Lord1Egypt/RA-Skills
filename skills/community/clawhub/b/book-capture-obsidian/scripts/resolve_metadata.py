#!/usr/bin/env python3
"""Resolve book metadata from an ISBN (or title and author) using public APIs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_isbn import normalize_isbn
from common_json import fail_and_print, make_result, print_json, read_json_file
from metadata_resolver import MetadataResolver

STAGE = "resolve_metadata"


MetadataDict = Dict[str, Any]


def resolve_book_metadata(
    isbn: Optional[str] = None,
    *,
    title: str = "",
    author: str = "",
    resolver: Optional[MetadataResolver] = None,
) -> dict:
    """Resolve metadata by ISBN, or by title and author when no ISBN is known."""
    isbn13 = normalize_isbn(isbn or "") if isbn else None
    if isbn and not isbn13:
        return make_result(STAGE, ok=False, error=f"invalid ISBN value: {isbn}", isbn13=None, metadata=None, warnings=[])
    if not isbn13 and not title.strip():
        return make_result(STAGE, ok=False, error="an ISBN or a title is required", isbn13=None, metadata=None, warnings=[])

    resolver = resolver or MetadataResolver.from_env()
    metadata, found_isbn, warnings = resolver.lookup(isbn13=isbn13, title=title.strip(), author=author.strip())
    if metadata:
        return make_result(
            STAGE,
            ok=True,
            error=None,
            isbn13=found_isbn or isbn13,
            metadata=metadata,
            warnings=warnings,
        )
    return make_result(
        STAGE,
        ok=False,
        error="metadata not found in configured providers",
        isbn13=isbn13,
        metadata=None,
        warnings=warnings,
    )


def _isbn_from_extract_json(path: str) -> str:
    payload = read_json_file(path)
    isbn13 = payload.get("isbn13")
    if not isinstance(isbn13, str) or not isbn13.strip():
        raise ValueError(f"extract JSON does not include isbn13: {path}")
    return isbn13


def _self_check() -> dict:
    isbn13 = normalize_isbn("0-201-63361-2")
    ok = isbn13 == "9780201633610"
    return make_result(
        STAGE,
        ok=ok,
        error=None if ok else "isbn normalization self-check failed",
        checks={
            "normalized_isbn13": isbn13,
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--isbn", help="ISBN-10 or ISBN-13")
    parser.add_argument("--extract-json", help="Path to extract_isbn JSON output")
    parser.add_argument("--title", default="", help="Book title, used when no ISBN is known")
    parser.add_argument("--author", default="", help="Author name, narrows a title lookup")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    isbn_value = args.isbn
    if args.extract_json:
        try:
            isbn_value = _isbn_from_extract_json(args.extract_json)
        except Exception as exc:
            return fail_and_print(STAGE, f"failed to read --extract-json: {exc}", isbn13=None, metadata=None)

    if not isbn_value and not args.title.strip():
        return fail_and_print(STAGE, "--isbn, --extract-json or --title is required", isbn13=None, metadata=None)

    result = resolve_book_metadata(isbn_value, title=args.title, author=args.author)
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
