#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("%"):
            continue
        lines.append(line)
    return "\n".join(lines)


def find_matching(text: str, start: int, open_char: str, close_char: str) -> int:
    depth = 0
    quote = False
    escaped = False
    for idx in range(start, len(text)):
        ch = text[idx]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"' and depth == 0:
            quote = not quote
            continue
        if quote:
            continue
        if ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return idx
    raise ValueError(f"No matching {close_char!r} found from offset {start}.")


def parse_bibtex(text: str) -> list[dict[str, Any]]:
    text = strip_comments(text)
    entries: list[dict[str, Any]] = []
    pos = 0
    while True:
        at = text.find("@", pos)
        if at == -1:
            break
        match = re.match(r"@([A-Za-z]+)\s*([\{\(])", text[at:])
        if not match:
            pos = at + 1
            continue
        entry_type = match.group(1).lower()
        open_char = match.group(2)
        close_char = "}" if open_char == "{" else ")"
        body_start = at + match.end() - 1
        body_end = find_matching(text, body_start, open_char, close_char)
        body = text[body_start + 1 : body_end]
        key, fields_text = split_key_and_fields(body)
        entries.append(
            {
                "key": key.strip(),
                "type": entry_type,
                "fields": parse_fields(fields_text),
            }
        )
        pos = body_end + 1
    return entries


def split_key_and_fields(body: str) -> tuple[str, str]:
    depth = 0
    quote = False
    escaped = False
    for idx, ch in enumerate(body):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"':
            quote = not quote
            continue
        if quote:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == "," and depth == 0:
            return body[:idx], body[idx + 1 :]
    return body, ""


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos] in " \t\r\n,":
            pos += 1
        match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", text[pos:])
        if not match:
            break
        name = match.group(1).lower()
        pos += match.end()
        while pos < len(text) and text[pos].isspace():
            pos += 1
        value, pos = parse_value(text, pos)
        fields[name] = clean_value(value)
        while pos < len(text) and text[pos] not in ",":
            pos += 1
        if pos < len(text) and text[pos] == ",":
            pos += 1
    return fields


def parse_value(text: str, pos: int) -> tuple[str, int]:
    if pos >= len(text):
        return "", pos
    if text[pos] == "{":
        end = find_matching(text, pos, "{", "}")
        return text[pos + 1 : end], end + 1
    if text[pos] == '"':
        escaped = False
        out = []
        idx = pos + 1
        while idx < len(text):
            ch = text[idx]
            if escaped:
                out.append(ch)
                escaped = False
            elif ch == "\\":
                escaped = True
                out.append(ch)
            elif ch == '"':
                return "".join(out), idx + 1
            else:
                out.append(ch)
            idx += 1
        return "".join(out), idx
    start = pos
    while pos < len(text) and text[pos] not in ",\r\n":
        pos += 1
    return text[start:pos], pos


def clean_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    value = value.replace("--", "-")
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def year_from_fields(fields: dict[str, str]) -> str:
    year = fields.get("year") or fields.get("date") or ""
    match = re.search(r"\d{4}", year)
    return match.group(0) if match else year


def authors_for_display(fields: dict[str, str]) -> str:
    raw = fields.get("author") or fields.get("editor") or ""
    if not raw:
        return ""
    parts = [part.strip() for part in re.split(r"\s+and\s+", raw) if part.strip()]
    return ", ".join(parts) if parts else raw


def append_period(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    return text if text.endswith((".", "。")) else text + "."


def join_year_volume_issue_pages(year: str, volume: str, issue: str, pages: str) -> str:
    left = year
    if volume and issue:
        left = f"{year}, {volume}({issue})" if year else f"{volume}({issue})"
    elif volume:
        left = f"{year}, {volume}" if year else volume
    elif issue:
        left = f"{year}({issue})" if year else f"({issue})"
    if pages:
        return f"{left}: {pages}" if left else pages
    return left


def gbt_from_entry(entry: dict[str, Any]) -> str:
    fields = entry["fields"]
    entry_type = entry["type"]
    authors = authors_for_display(fields)
    title = fields.get("title", "")
    year = year_from_fields(fields)
    volume = fields.get("volume", "")
    issue = fields.get("number") or fields.get("issue") or ""
    pages = fields.get("pages", "")

    if entry_type == "article":
        journal = fields.get("journal") or fields.get("journaltitle") or ""
        tail = join_year_volume_issue_pages(year, volume, issue, pages)
        chunks = [authors, f"{title}[J]"]
        if journal and tail:
            chunks.append(f"{journal}, {tail}")
        elif journal:
            chunks.append(journal)
        elif tail:
            chunks.append(tail)
        return append_period(". ".join(chunk for chunk in chunks if chunk))

    if entry_type in {"book", "monograph"}:
        publisher = fields.get("publisher", "")
        place = fields.get("address") or fields.get("location") or ""
        pub = ": ".join(part for part in [place, publisher] if part)
        tail = ", ".join(part for part in [pub, year] if part)
        chunks = [authors, f"{title}[M]"]
        if tail:
            chunks.append(tail)
        return append_period(". ".join(chunk for chunk in chunks if chunk))

    if entry_type in {"inproceedings", "conference"}:
        booktitle = fields.get("booktitle", "")
        tail = join_year_volume_issue_pages(year, "", "", pages)
        chunks = [authors, f"{title}[C]"]
        if booktitle and tail:
            chunks.append(f"{booktitle}, {tail}")
        elif booktitle:
            chunks.append(booktitle)
        elif tail:
            chunks.append(tail)
        return append_period(". ".join(chunk for chunk in chunks if chunk))

    if entry_type in {"phdthesis", "mastersthesis", "thesis"}:
        school = fields.get("school") or fields.get("institution") or ""
        place = fields.get("address") or fields.get("location") or ""
        org = ": ".join(part for part in [place, school] if part)
        tail = ", ".join(part for part in [org, year] if part)
        chunks = [authors, f"{title}[D]"]
        if tail:
            chunks.append(tail)
        return append_period(". ".join(chunk for chunk in chunks if chunk))

    chunks = [authors, title]
    source = fields.get("howpublished") or fields.get("publisher") or fields.get("institution") or ""
    if source:
        chunks.append(source)
    if year:
        chunks.append(year)
    return append_period(". ".join(chunk for chunk in chunks if chunk))


def filter_entries(entries: list[dict[str, Any]], contains: list[str]) -> list[dict[str, Any]]:
    if not contains:
        return entries
    needles = [item.lower() for item in contains]
    selected = []
    for entry in entries:
        haystack = json.dumps(entry, ensure_ascii=False).lower()
        if any(needle in haystack for needle in needles):
            selected.append(entry)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse BibTeX and emit JSON candidates with rough GB/T strings.")
    parser.add_argument("bibtex", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--contains", action="append", default=[], help="Filter entries containing text.")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    entries = parse_bibtex(args.bibtex.read_text(encoding="utf-8"))
    entries = filter_entries(entries, args.contains)
    if args.limit:
        entries = entries[: args.limit]

    output = []
    for entry in entries:
        item = dict(entry)
        item["gbt"] = gbt_from_entry(entry)
        output.append(item)

    text = json.dumps(output, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote={args.out}")
        print(f"entries={len(output)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
