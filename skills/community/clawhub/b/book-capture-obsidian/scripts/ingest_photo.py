#!/usr/bin/env python3
"""Orchestrate end-to-end ingestion: photo -> ISBN -> metadata -> Obsidian note."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_config import get_env_str
from common_json import fail_and_print, make_result, print_json
from extract_isbn import extract_isbn_from_image
from resolve_metadata import resolve_book_metadata
from upsert_obsidian_note import upsert_note

STAGE = "ingest_photo"


def ingest_book_photo(image_path: str, vault_path: str, notes_dir: str, target_note: str | None = None) -> Dict[str, Any]:
    warnings: List[str] = []

    extract_result = extract_isbn_from_image(image_path)
    warnings.extend(extract_result.get("warnings") or [])
    if not extract_result.get("ok"):
        return make_result(
            STAGE,
            ok=False,
            error="isbn extraction failed",
            image_path=image_path,
            extract=extract_result,
            metadata=None,
            upsert=None,
            warnings=sorted(set(warnings)),
        )

    isbn13 = extract_result.get("isbn13")
    metadata_result = resolve_book_metadata(str(isbn13 or ""))
    warnings.extend(metadata_result.get("warnings") or [])
    if not metadata_result.get("ok"):
        return make_result(
            STAGE,
            ok=False,
            error="metadata resolution failed",
            image_path=image_path,
            extract=extract_result,
            metadata=metadata_result,
            upsert=None,
            warnings=sorted(set(warnings)),
        )

    upsert_payload = {
        "isbn13": metadata_result.get("isbn13"),
        "metadata": metadata_result.get("metadata"),
    }
    upsert_result = upsert_note(
        payload=upsert_payload,
        vault_path=vault_path,
        notes_dir=notes_dir,
        target_note=target_note,
    )

    if not upsert_result.get("ok"):
        return make_result(
            STAGE,
            ok=False,
            error="note upsert failed",
            image_path=image_path,
            extract=extract_result,
            metadata=metadata_result,
            upsert=upsert_result,
            warnings=sorted(set(warnings)),
        )

    return make_result(
        STAGE,
        ok=True,
        error=None,
        image_path=image_path,
        isbn13=metadata_result.get("isbn13"),
        note_path=upsert_result.get("note_path"),
        extract=extract_result,
        metadata=metadata_result,
        upsert=upsert_result,
        warnings=sorted(set(warnings)),
    )


def _self_check() -> Dict[str, Any]:
    ok = callable(extract_isbn_from_image) and callable(resolve_book_metadata) and callable(upsert_note)
    return make_result(
        STAGE,
        ok=ok,
        error=None if ok else "pipeline imports are not callable",
        checks={
            "extract_callable": callable(extract_isbn_from_image),
            "resolve_callable": callable(resolve_book_metadata),
            "upsert_callable": callable(upsert_note),
        },
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", help="Path to book photo")
    parser.add_argument("--vault-path", default=get_env_str("BOOK_CAPTURE_VAULT_PATH", "."), help="Obsidian vault root")
    parser.add_argument("--notes-dir", default=get_env_str("BOOK_CAPTURE_NOTES_DIR", "Books"), help="Notes directory inside vault")
    parser.add_argument("--target-note", default=get_env_str("BOOK_CAPTURE_TARGET_NOTE", ""), help="Optional explicit note path")
    parser.add_argument("--self-check", action="store_true", help="Run internal quick checks")
    args = parser.parse_args(argv)

    if args.self_check:
        result = _self_check()
        print_json(result)
        return 0 if result.get("ok") else 1

    if not args.image:
        return fail_and_print(STAGE, "--image is required", image_path=None)

    result = ingest_book_photo(
        image_path=args.image,
        vault_path=args.vault_path,
        notes_dir=args.notes_dir,
        target_note=args.target_note or None,
    )
    print_json(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
