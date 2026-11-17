#!/usr/bin/env python3
"""Compare canonical local book trees with a full remote export.

The comparison intentionally includes text and parent structure, not only counts.
It prints one TSV row per book and exits non-zero for missing or mismatched books.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def normalize_title(value: Any) -> str:
    return "" if value is None else str(value).strip()


def exact_content(value: Any) -> str:
    return "" if value is None else str(value)


def natural_key(path: Path) -> list[Any]:
    return [int(piece) if piece.isdigit() else piece for piece in re.split(r"(\d+)", path.name)]


def canonical_nodes(nodes: list[dict[str, Any]], remote: bool) -> list[dict[str, Any]]:
    id_field = "chapter_id" if remote else "key"
    parent_field = "parent_id" if remote else "parent_key"
    id_to_index: dict[str, int] = {}
    for index, node in enumerate(nodes):
        node_id = node.get(id_field)
        if not isinstance(node_id, str) or not node_id:
            raise ValueError(f"node {index + 1}: missing {id_field}")
        if node_id in id_to_index:
            raise ValueError(f"duplicate {id_field}: {node_id}")
        id_to_index[node_id] = index

    result: list[dict[str, Any]] = []
    for index, node in enumerate(nodes):
        parent = node.get(parent_field)
        if parent is None or parent == "":
            parent_index = None
        elif parent not in id_to_index:
            raise ValueError(f"node {index + 1}: missing parent {parent!r}")
        else:
            parent_index = id_to_index[parent]
        result.append(
            {
                "title": normalize_title(node.get("title", node.get("chapter_title", ""))),
                "content": exact_content(node.get("content", "")),
                "level": int(node.get("level", 0)),
                "sort": int(node.get("sort", index + 1)),
                "parent_index": parent_index,
            }
        )
    return result


def fingerprint(nodes: list[dict[str, Any]]) -> str:
    payload = json.dumps(nodes, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_local(directory: Path) -> dict[str, dict[str, Any]]:
    books: dict[str, dict[str, Any]] = {}
    paths = sorted(directory.glob("*_tree.json"), key=natural_key)
    if not paths:
        raise ValueError(f"no *_tree.json files in {directory}")
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        book_id = data.get("book_id")
        if not isinstance(book_id, str) or not book_id:
            raise ValueError(f"{path}: missing book_id")
        if book_id in books:
            raise ValueError(f"duplicate local book_id: {book_id}")
        nodes = data.get("nodes")
        if not isinstance(nodes, list):
            raise ValueError(f"{path}: nodes must be a list")
        canonical = canonical_nodes(nodes, remote=False)
        books[book_id] = {
            "title": normalize_title(data.get("title", "")),
            "nodes": canonical,
            "sha256": fingerprint(canonical),
            "path": str(path),
        }
    return books


def load_remote(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_books = data.get("books")
    if not isinstance(raw_books, list):
        raise ValueError(f"{path}: books must be a list")
    books: dict[str, dict[str, Any]] = {}
    for data_book in raw_books:
        book_id = data_book.get("book_id")
        if not isinstance(book_id, str) or not book_id:
            raise ValueError("remote book missing book_id")
        if book_id in books:
            raise ValueError(f"duplicate remote book_id: {book_id}")
        chapters = data_book.get("chapters")
        if not isinstance(chapters, list):
            raise ValueError(f"remote {book_id}: chapters must be a list")
        canonical = canonical_nodes(chapters, remote=True)
        books[book_id] = {
            "title": normalize_title(data_book.get("title", "")),
            "nodes": canonical,
            "sha256": fingerprint(canonical),
        }
    return books


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-dir", required=True, type=Path)
    parser.add_argument("--remote-export", required=True, type=Path)
    args = parser.parse_args()

    try:
        local = load_local(args.local_dir)
        remote = load_remote(args.remote_export)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        return 2

    print("book_id\tlocal_nodes\tremote_nodes\ttitle\tstructure_content\tsha256")
    failed = False
    for book_id in sorted(set(local) | set(remote)):
        local_book = local.get(book_id)
        remote_book = remote.get(book_id)
        if local_book is None:
            print(f"{book_id}\t-\t{len(remote_book['nodes'])}\tMISSING_LOCAL\tFAIL\t-")
            failed = True
            continue
        if remote_book is None:
            print(f"{book_id}\t{len(local_book['nodes'])}\t-\tMISSING_REMOTE\tFAIL\t{local_book['sha256']}")
            failed = True
            continue
        title_ok = local_book["title"] == remote_book["title"]
        body_ok = local_book["nodes"] == remote_book["nodes"]
        hash_ok = local_book["sha256"] == remote_book["sha256"]
        ok = title_ok and body_ok and hash_ok
        failed = failed or not ok
        print(
            f"{book_id}\t{len(local_book['nodes'])}\t{len(remote_book['nodes'])}"
            f"\t{'OK' if title_ok else 'FAIL'}\t{'OK' if body_ok else 'FAIL'}"
            f"\t{local_book['sha256'] if hash_ok else local_book['sha256'] + ' != ' + remote_book['sha256']}"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
