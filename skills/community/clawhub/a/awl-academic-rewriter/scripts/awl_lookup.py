#!/usr/bin/env python3
"""Headword helper for the AWL/NAWL academic rewriter skill.

This script intentionally does not score semantic replacement candidates.
It lists, filters, and verifies first-column AWL/NAWL headwords, then retrieves
full CSV details for model-selected headwords.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_headwords_path() -> Path:
    return skill_root() / "references" / "awl-headwords.txt"


def default_csv_path() -> Path:
    return skill_root() / "references" / "awl.csv"


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def tokenize(text: str) -> list[str]:
    return [normalize(match.group(0)) for match in WORD_RE.finditer(text)]


def load_headwords(path: Path) -> list[str]:
    if path.exists():
        return [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    csv_path = default_csv_path()
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if "Word" not in (reader.fieldnames or []):
            raise SystemExit(f"CSV file lacks a Word column: {csv_path}")
        return [row["Word"].strip() for row in reader if row.get("Word", "").strip()]


def load_csv_details(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = ["Word", "Derivatives", "English Definition"]
        if reader.fieldnames != expected:
            raise SystemExit(f"Unexpected CSV columns in {path}: {reader.fieldnames!r}")
        return {
            normalize(row["Word"]): {
                "Word": row["Word"].strip(),
                "Derivatives": row["Derivatives"].strip(),
                "English Definition": row["English Definition"].strip(),
            }
            for row in reader
            if row.get("Word", "").strip()
        }


def filter_headwords(headwords: list[str], patterns: list[str]) -> list[str]:
    normalized_patterns = [normalize(pattern) for pattern in patterns if normalize(pattern)]
    if not normalized_patterns:
        return headwords

    filtered = []
    for word in headwords:
        word_norm = normalize(word)
        if any(pattern in word_norm for pattern in normalized_patterns):
            filtered.append(word)
    return filtered


def verify_words(headwords: list[str], words: list[str]) -> list[dict[str, object]]:
    index = {normalize(word): word for word in headwords}
    return [
        {
            "query": word,
            "found": normalize(word) in index,
            "headword": index.get(normalize(word), ""),
        }
        for word in words
    ]


def lookup_details(csv_path: Path, words: list[str]) -> list[dict[str, object]]:
    details = load_csv_details(csv_path)
    rows = []
    for word in words:
        key = normalize(word)
        row = details.get(key)
        if row:
            rows.append({"query": word, "found": True, **row})
        else:
            rows.append(
                {
                    "query": word,
                    "found": False,
                    "Word": "",
                    "Derivatives": "",
                    "English Definition": "",
                }
            )
    return rows


def detect_present_headwords(headwords: list[str], text: str) -> list[dict[str, object]]:
    index = {normalize(word): word for word in headwords}
    counts: Counter[str] = Counter()
    for token in tokenize(text):
        if token in index:
            counts[index[token]] += 1
    return [
        {"headword": word, "count": count}
        for word, count in counts.most_common()
    ]


def print_plain(headwords: list[str]) -> None:
    for word in headwords:
        print(word)


def print_markdown_headwords(headwords: list[str]) -> None:
    print("| # | AWL/NAWL headword |")
    print("|---|---|")
    for number, word in enumerate(headwords, start=1):
        escaped = word.replace("|", "\\|")
        print(f"| {number} | {escaped} |")


def print_markdown_verification(items: list[dict[str, object]]) -> None:
    print("| Query | In headword list | Matched headword |")
    print("|---|---|---|")
    for item in items:
        found = "yes" if item["found"] else "no"
        print(f"| {item['query']} | {found} | {item['headword']} |")


def print_markdown_details(items: list[dict[str, object]]) -> None:
    print("| Query | Found | Word | Derivatives | English Definition |")
    print("|---|---|---|---|---|")
    for item in items:
        found = "yes" if item["found"] else "no"
        cells = [
            str(item["query"]),
            found,
            str(item["Word"]),
            str(item["Derivatives"]),
            str(item["English Definition"]),
        ]
        escaped = [cell.replace("|", "\\|").replace("\n", " ") for cell in cells]
        print("| " + " | ".join(escaped) + " |")


def print_markdown_present(items: list[dict[str, object]]) -> None:
    print("| Headword present in text | Count |")
    print("|---|---|")
    for item in items:
        print(f"| {item['headword']} | {item['count']} |")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List, filter, and verify first-column AWL/NAWL headwords."
    )
    parser.add_argument("--headwords", type=Path, default=default_headwords_path())
    parser.add_argument("--csv", type=Path, default=default_csv_path())
    parser.add_argument("--all", action="store_true", help="Print all headwords.")
    parser.add_argument("--contains", action="append", default=[], help="Filter headwords by substring.")
    parser.add_argument("--word", action="append", default=[], help="Verify exact first-column headword membership.")
    parser.add_argument("--details", action="append", default=[], help="Return all CSV columns for a selected first-column headword.")
    parser.add_argument("--text-file", type=Path, help="Count exact headwords already present in an input text.")
    parser.add_argument("--limit", type=int, default=0, help="Limit listed or filtered headwords; 0 means no limit.")
    parser.add_argument("--format", choices=("markdown", "json", "plain"), default="markdown")
    args = parser.parse_args()

    headwords = load_headwords(args.headwords)
    filtered = filter_headwords(headwords, args.contains)
    if args.limit > 0:
        filtered = filtered[: args.limit]

    output: dict[str, object] = {}
    if args.all or args.contains:
        output["headwords"] = filtered
    if args.word:
        output["verification"] = verify_words(headwords, args.word)
    if args.details:
        output["details"] = lookup_details(args.csv, args.details)
    if args.text_file:
        output["present_in_text"] = detect_present_headwords(
            headwords,
            args.text_file.read_text(encoding="utf-8"),
        )

    if not output:
        parser.print_help()
        return 0

    if args.format == "json":
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0

    if args.format == "plain":
        if "headwords" in output:
            print_plain(output["headwords"])
        elif "verification" in output:
            for item in output["verification"]:
                status = "yes" if item["found"] else "no"
                print(f"{item['query']}\t{status}\t{item['headword']}")
        elif "details" in output:
            for item in output["details"]:
                status = "yes" if item["found"] else "no"
                print(
                    f"{item['query']}\t{status}\t{item['Word']}\t"
                    f"{item['Derivatives']}\t{item['English Definition']}"
                )
        elif "present_in_text" in output:
            for item in output["present_in_text"]:
                print(f"{item['headword']}\t{item['count']}")
        return 0

    if "headwords" in output:
        print("## AWL/NAWL Headwords")
        print_markdown_headwords(output["headwords"])
        print()
    if "verification" in output:
        print("## Headword Verification")
        print_markdown_verification(output["verification"])
        print()
    if "details" in output:
        print("## Selected Headword Details")
        print_markdown_details(output["details"])
        print()
    if "present_in_text" in output:
        print("## First-Column Headwords Already Present")
        print_markdown_present(output["present_in_text"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
