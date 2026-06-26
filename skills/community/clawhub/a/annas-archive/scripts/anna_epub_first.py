#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RUNNER = Path(os.environ.get("ANNAS_RUNNER_PATH", str(SCRIPT_DIR / "run-annas-mcp.sh")))


@dataclass
class Book:
    title: str
    authors: str
    format: str
    hash: str
    raw: dict[str, str]


def _norm(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokens(text: str) -> set[str]:
    stop = {
        "the",
        "a",
        "an",
        "of",
        "to",
        "and",
        "for",
        "with",
        "on",
        "in",
    }
    return {t for t in _norm(text).split() if t and t not in stop}


def parse_books(output: str) -> list[Book]:
    books: list[Book] = []
    current: dict[str, str] | None = None

    for line in output.splitlines():
        line = line.rstrip("\n")
        if line.startswith("Book ") and line.endswith(":"):
            if current:
                books.append(
                    Book(
                        title=current.get("title", ""),
                        authors=current.get("authors", ""),
                        format=current.get("format", ""),
                        hash=current.get("hash", ""),
                        raw=current,
                    )
                )
            current = {}
            continue

        if current is None or ":" not in line:
            continue

        key, value = line.split(":", 1)
        current[key.strip().lower()] = value.strip()

    if current:
        books.append(
            Book(
                title=current.get("title", ""),
                authors=current.get("authors", ""),
                format=current.get("format", ""),
                hash=current.get("hash", ""),
                raw=current,
            )
        )

    return [b for b in books if b.hash]


def book_score(query: str, book: Book) -> float:
    q_norm = _norm(query)
    t_norm = _norm(book.title)
    if not q_norm or not t_norm:
        return 0.0

    seq = SequenceMatcher(None, q_norm, t_norm).ratio()

    q_tokens = _tokens(query)
    t_tokens = _tokens(book.title)
    jac = (len(q_tokens & t_tokens) / len(q_tokens | t_tokens)) if (q_tokens | t_tokens) else 0.0

    fmt = _norm(book.format)
    if fmt == "epub":
        fmt_bonus = 0.25
    elif fmt == "pdf":
        fmt_bonus = 0.1
    else:
        fmt_bonus = 0.0

    return (0.55 * seq) + (0.45 * jac) + fmt_bonus


def resolve_runner() -> Path:
    runner = RUNNER.expanduser()
    if not runner.is_absolute():
        runner = (SCRIPT_DIR / runner).resolve()
    if not runner.exists():
        raise RuntimeError(f"Runner script not found: {runner}")
    if not os.access(runner, os.X_OK):
        raise RuntimeError(f"Runner script is not executable: {runner}")
    return runner


def run_search(query: str) -> list[Book]:
    runner = resolve_runner()
    cmd = [str(runner), "book-search", query]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "book-search failed")
    books = parse_books(proc.stdout)
    return books


def run_download(book: Book, preferred_format: str) -> subprocess.CompletedProcess[str]:
    runner = resolve_runner()
    fmt = preferred_format if preferred_format else book.format
    cmd = [
        str(runner),
        "book-download",
        "--hash",
        book.hash,
        "--title",
        book.title,
        "--format",
        fmt,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Anna's Archive and choose EPUB first.")
    parser.add_argument("--query", required=True, help="Book query")
    parser.add_argument("--download", action="store_true", help="Download selected result")
    parser.add_argument("--epub-only", action="store_true", help="Fail unless selected format is EPUB")
    parser.add_argument("--max-results", type=int, default=20, help="Top N parsed candidates to rank")
    args = parser.parse_args()

    books = run_search(args.query)
    if not books:
        print(json.dumps({"ok": False, "reason": "no-results", "query": args.query}, ensure_ascii=False))
        return 2

    ranked = sorted(
        books[: max(1, args.max_results)],
        key=lambda b: book_score(args.query, b),
        reverse=True,
    )

    selected = ranked[0]
    selected_format = _norm(selected.format)

    if args.epub_only and selected_format != "epub":
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "no-epub-match",
                    "query": args.query,
                    "selected": {
                        "title": selected.title,
                        "authors": selected.authors,
                        "format": selected.format,
                        "hash": selected.hash,
                    },
                },
                ensure_ascii=False,
            )
        )
        return 3

    response = {
        "ok": True,
        "query": args.query,
        "selected": {
            "title": selected.title,
            "authors": selected.authors,
            "format": selected.format,
            "hash": selected.hash,
            "score": round(book_score(args.query, selected), 3),
        },
    }

    if args.download:
        preferred = "epub" if selected_format == "epub" else selected.format
        proc = run_download(selected, preferred)
        runner = resolve_runner()
        response["download"] = {
            "command": " ".join(shlex.quote(part) for part in [str(runner), "book-download", "--hash", selected.hash, "--title", selected.title, "--format", preferred]),
            "return_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "download_path": "/tmp/annas-archive-downloads",
        }
        if proc.returncode != 0:
            response["ok"] = False
            print(json.dumps(response, ensure_ascii=False))
            return 4

    print(json.dumps(response, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
