#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bibtex_to_json import filter_entries, parse_bibtex
from reference_styles import SUPPORTED_STYLES, format_reference


RIS_TYPE_MAP = {
    "JOUR": "article",
    "JFULL": "article",
    "MGZN": "article",
    "CONF": "inproceedings",
    "CPAPER": "inproceedings",
    "BOOK": "book",
    "THES": "thesis",
    "RPRT": "report",
    "ELEC": "online",
}

RIS_FIELD_MAP = {
    "TI": "title",
    "T1": "title",
    "JO": "journal",
    "JF": "journal",
    "JA": "journal",
    "T2": "journal",
    "PY": "year",
    "Y1": "year",
    "VL": "volume",
    "IS": "number",
    "SP": "start_page",
    "EP": "end_page",
    "DO": "doi",
    "UR": "url",
    "PB": "publisher",
    "CY": "address",
    "AB": "abstract",
    "KW": "keywords",
    "ID": "id",
}

CSV_ALIASES = {
    "key": ["key", "citekey", "citation key", "citation_key", "id"],
    "type": ["type", "item type", "entrytype", "entry_type"],
    "author": ["author", "authors", "creator", "creators"],
    "title": ["title", "publication title"],
    "journal": ["journal", "publication", "publicationtitle", "publication title", "journal title"],
    "booktitle": ["booktitle", "proceedings title", "conference name"],
    "year": ["year", "date", "publication year"],
    "volume": ["volume"],
    "number": ["number", "issue", "issue number"],
    "pages": ["pages", "page", "page range"],
    "publisher": ["publisher"],
    "address": ["address", "place", "location"],
    "doi": ["doi"],
    "url": ["url"],
    "abstract": ["abstract", "notes"],
}


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def normalize_year(value: str) -> str:
    match = re.search(r"\d{4}", value or "")
    return match.group(0) if match else (value or "")


def add_formatted_references(entries: list[dict[str, Any]], style: str) -> list[dict[str, Any]]:
    output = []
    for idx, entry in enumerate(entries, start=1):
        item = dict(entry)
        if not item.get("key"):
            item["key"] = f"ref{idx:03d}"
        formatted = format_reference(item, style)
        item["gbt"] = formatted
        item["formatted"] = formatted
        item["citation_style"] = style
        output.append(item)
    return output


def parse_ris(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    last_tag: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        match = re.match(r"^([A-Z0-9]{2})  -\s?(.*)$", line)
        if match:
            tag, value = match.group(1), match.group(2).strip()
            if tag == "TY":
                current = {"key": "", "type": RIS_TYPE_MAP.get(value, value.lower()), "fields": {}}
                last_tag = tag
                continue
            if current is None:
                continue
            if tag == "ER":
                finalize_ris_entry(current)
                entries.append(current)
                current = None
                last_tag = None
                continue
            append_ris_value(current, tag, value)
            last_tag = tag
        elif current is not None and last_tag:
            value = line.strip()
            if value:
                append_ris_value(current, last_tag, value, continuation=True)

    if current is not None:
        finalize_ris_entry(current)
        entries.append(current)
    return entries


def append_ris_value(entry: dict[str, Any], tag: str, value: str, continuation: bool = False):
    fields = entry["fields"]
    if tag in {"AU", "A1", "A2", "A3"}:
        existing = fields.get("author", "")
        if continuation and existing:
            fields["author"] = existing + " " + value
        else:
            fields["author"] = f"{existing} and {value}" if existing else value
        return
    mapped = RIS_FIELD_MAP.get(tag)
    if not mapped:
        return
    if mapped == "keywords":
        existing = fields.get(mapped, "")
        fields[mapped] = f"{existing}; {value}" if existing else value
        return
    if continuation and mapped in fields:
        fields[mapped] = fields[mapped] + " " + value
    else:
        fields[mapped] = value
    if tag == "ID":
        entry["key"] = value


def finalize_ris_entry(entry: dict[str, Any]):
    fields = entry["fields"]
    fields["year"] = normalize_year(fields.get("year", ""))
    if fields.get("start_page") and fields.get("end_page"):
        fields["pages"] = f"{fields['start_page']}-{fields['end_page']}"
    elif fields.get("start_page"):
        fields["pages"] = fields["start_page"]
    fields.pop("start_page", None)
    fields.pop("end_page", None)


def parse_csl_json(text: str) -> list[dict[str, Any]]:
    data = json.loads(text)
    if isinstance(data, dict):
        data = data.get("items") or data.get("references") or [data]
    if not isinstance(data, list):
        raise ValueError("CSL JSON must be an object or list.")
    entries = []
    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            continue
        fields = csl_fields(item)
        entries.append(
            {
                "key": str(item.get("id") or item.get("citation-key") or f"ref{idx:03d}"),
                "type": csl_type(item.get("type", "")),
                "fields": fields,
            }
        )
    return entries


def csl_type(raw: str) -> str:
    mapping = {
        "article-journal": "article",
        "paper-conference": "inproceedings",
        "book": "book",
        "chapter": "inbook",
        "thesis": "thesis",
        "report": "report",
        "webpage": "online",
    }
    return mapping.get(raw, raw or "misc")


def csl_fields(item: dict[str, Any]) -> dict[str, str]:
    issued = item.get("issued") or item.get("published") or {}
    fields = {
        "author": csl_people(item.get("author") or item.get("editor") or []),
        "title": str(item.get("title") or ""),
        "journal": str(item.get("container-title") or ""),
        "booktitle": str(item.get("event-title") or item.get("collection-title") or ""),
        "year": csl_year(issued),
        "volume": str(item.get("volume") or ""),
        "number": str(item.get("issue") or ""),
        "pages": str(item.get("page") or "").replace("--", "-"),
        "publisher": str(item.get("publisher") or ""),
        "address": str(item.get("publisher-place") or item.get("event-place") or ""),
        "doi": str(item.get("DOI") or item.get("doi") or ""),
        "url": str(item.get("URL") or item.get("url") or ""),
        "abstract": str(item.get("abstract") or ""),
    }
    return {key: value for key, value in fields.items() if value}


def csl_people(people: list[dict[str, Any]]) -> str:
    names = []
    for person in people:
        if not isinstance(person, dict):
            continue
        literal = person.get("literal")
        if literal:
            names.append(str(literal))
            continue
        family = str(person.get("family") or "").strip()
        given = str(person.get("given") or "").strip()
        names.append(" ".join(part for part in [family, given] if part))
    return " and ".join(name for name in names if name)


def csl_year(issued: Any) -> str:
    if isinstance(issued, dict):
        parts = issued.get("date-parts")
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            return str(parts[0][0])
        raw = issued.get("raw")
        return normalize_year(str(raw or ""))
    return normalize_year(str(issued or ""))


def parse_csv_like(path: Path, delimiter: str | None = None) -> list[dict[str, Any]]:
    text = read_text(path)
    if delimiter is None:
        sample = text[:4096]
        delimiter = "\t" if path.suffix.lower() == ".tsv" else csv.Sniffer().sniff(sample).delimiter
    rows = csv.DictReader(text.splitlines(), delimiter=delimiter)
    entries = []
    for idx, row in enumerate(rows, start=1):
        normalized = {normalize_header(k): (v or "").strip() for k, v in row.items() if k}
        fields = {}
        for field, aliases in CSV_ALIASES.items():
            value = first_present(normalized, aliases)
            if value:
                fields[field] = value
        entry_type = fields.pop("type", "") or "article"
        key = fields.pop("key", "") or f"ref{idx:03d}"
        if not fields.get("journal") and normalized.get("publication"):
            fields["journal"] = normalized["publication"]
        fields["year"] = normalize_year(fields.get("year", ""))
        entries.append({"key": key, "type": entry_type, "fields": fields})
    return entries


def normalize_header(value: str) -> str:
    return re.sub(r"[\s_-]+", " ", value.strip().lower())


def first_present(row: dict[str, str], aliases: list[str]) -> str:
    normalized_aliases = [normalize_header(alias) for alias in aliases]
    for alias in normalized_aliases:
        if row.get(alias):
            return row[alias]
    return ""


def parse_plain_references(text: str) -> list[dict[str, Any]]:
    lines = []
    buffer = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if buffer:
                lines.append(buffer.strip())
                buffer = ""
            continue
        match = re.match(r"^\s*(?:\[(\d+)\]|(\d+)[\.\、])\s*(.+)$", line)
        if match:
            if buffer:
                lines.append(buffer.strip())
            buffer = match.group(3).strip()
        else:
            buffer = f"{buffer} {line}".strip()
    if buffer:
        lines.append(buffer.strip())

    entries = []
    for idx, line in enumerate(lines, start=1):
        entries.append(
            {
                "key": f"ref{idx:03d}",
                "type": "preformatted",
                "fields": {"title": line},
                "gbt": line if line.endswith((".", "。")) else line + ".",
            }
        )
    return entries


def detect_format(path: Path, explicit: str = "auto") -> str:
    if explicit != "auto":
        return explicit
    suffix = path.suffix.lower()
    if suffix in {".bib", ".bibtex"}:
        return "bibtex"
    if suffix == ".ris":
        return "ris"
    if suffix in {".json", ".csljson"}:
        return "csl-json"
    if suffix == ".csv":
        return "csv"
    if suffix == ".tsv":
        return "tsv"
    if suffix in {".txt", ".md"}:
        return "plain"
    raise ValueError(f"Cannot infer source format from {path.name}. Use --format.")


def parse_source(path: Path, source_format: str) -> list[dict[str, Any]]:
    text = read_text(path)
    if source_format == "bibtex":
        return parse_bibtex(text)
    if source_format == "ris":
        return parse_ris(text)
    if source_format == "csl-json":
        return parse_csl_json(text)
    if source_format == "csv":
        return parse_csv_like(path, ",")
    if source_format == "tsv":
        return parse_csv_like(path, "\t")
    if source_format == "plain":
        return parse_plain_references(text)
    raise ValueError(f"Unsupported format: {source_format}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize literature source files to candidate JSON.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--format", choices=["auto", "bibtex", "ris", "csl-json", "csv", "tsv", "plain"], default="auto")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--style", choices=SUPPORTED_STYLES, default="gbt7714", help="Bibliography formatting style.")
    parser.add_argument("--contains", action="append", default=[], help="Filter entries containing text.")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    source_format = detect_format(args.source, args.format)
    entries = parse_source(args.source, source_format)
    entries = filter_entries(entries, args.contains)
    if args.limit:
        entries = entries[: args.limit]
    output = add_formatted_references(entries, args.style)
    text = json.dumps(output, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote={args.out}")
        print(f"format={source_format}")
        print(f"style={args.style}")
        print(f"entries={len(output)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
