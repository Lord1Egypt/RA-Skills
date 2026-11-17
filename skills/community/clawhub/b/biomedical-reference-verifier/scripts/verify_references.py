#!/usr/bin/env python3
"""Batch-check or format biomedical references.

Pipeline:
1. Normalize once: prefer machine-readable records.v1 JSON/JSONL, otherwise parse references.
2. For format-only requests, render the normalized records into the requested citation style.
3. For authenticity requests, batch lookup de-duplicated DOI/PMID/title queries.
4. Classify: short-circuit hijacked or shifted identifiers.
5. Recover: query titles only for problematic entries.
6. Write reports and an auto-fixed reference copy without touching the source.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import queue
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

from verifier_runtime import RuntimeMetrics, grace_for_mode
from verifier_network import RateLimiter, run_with_retry
from verifier_recovery import run_recovery_workers
from verifier_policy import (
    CROSSREF_POLITE_CONCURRENCY,
    CROSSREF_POLITE_RATE_PER_SECOND,
    CROSSREF_PUBLIC_CONCURRENCY,
    CROSSREF_PUBLIC_RATE_PER_SECOND,
    NCBI_API_KEY_RATE_PER_SECOND,
    NCBI_DEFAULT_RATE_PER_SECOND,
    OPENALEX_DEFAULT_CONCURRENCY,
    OPENALEX_DEFAULT_RATE_PER_SECOND,
    PROBLEM_STATUSES,
    SEVERE_STATUSES,
    TITLE_RECOVERY_STATUSES,
)
from verifier_prior_results import audit_result_from_dict, audit_to_index, load_prior_results, prior_result_for_entry, write_json_atomic
from verifier_models import AuditResult, CanonicalRecord, OutputPaths, ReferenceEntry
from generate_html_report import write_html_report


DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
PMID_RE = re.compile(r"\b(?:PMID|PubMed ID)[:\s]*(\d{6,9})\b", re.I)
URL_RE = re.compile(r"https?://[^\s<>)\]]+", re.I)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
REF_HEADING_RE = re.compile(r"^\s{0,3}#{0,6}\s*(references|bibliography|参考文献)\s*$", re.I)
WORKSHEET_REQUIRED_FIELDS = {"title", "doi"}
MACHINE_RECORD_SCHEMA = "biomedical-reference-verifier.records.v1"
VERSION = "1.2.1"
POLICY_VERSION = "2026-09-14.1"
WORKSHEET_HEADER_ALIASES = {
    "#": "index",
    "no": "index",
    "id": "index",
    "index": "index",
    "序号": "index",
    "original": "original",
    "originaltext": "original",
    "raw": "original",
    "reference": "original",
    "sourcetext": "original",
    "原文": "original",
    "title": "title",
    "sourcetitle": "title",
    "parsedtitle": "title",
    "articletitle": "title",
    "题名": "title",
    "标题": "title",
    "authors": "authors",
    "author": "authors",
    "sourceauthors": "authors",
    "parsedauthors": "authors",
    "作者": "authors",
    "year": "year",
    "sourceyear": "year",
    "publicationyear": "year",
    "年份": "year",
    "journal": "journal",
    "sourcejournal": "journal",
    "containertitle": "journal",
    "期刊": "journal",
    "doi": "doi",
    "sourcedoi": "doi",
    "pmid": "pmid",
    "sourcepmid": "pmid",
    "url": "url",
    "urls": "url",
    "sourceurl": "url",
    "line": "source_line",
    "sourceline": "source_line",
    "lines": "source_line",
    "context": "context",
    "note": "context",
    "notes": "context",
    "querykey": "query_key",
    "format": "citation_format",
    "citationformat": "citation_format",
}


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"doi\.org/", " ", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def title_similarity(a: str, b: str) -> float:
    na = normalize_text(a)
    nb = normalize_text(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return min(len(na), len(nb)) / max(len(na), len(nb))
    return SequenceMatcher(None, na, nb).ratio()


def clean_doi(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    return value.rstrip(".,;:)]}。；，").lower()


def first_year(value: str) -> str:
    match = YEAR_RE.search(value)
    return match.group(0) if match else ""


def compact(value: str, limit: int = 92) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "..."


def split_references(text: str, references_heading: str | None = None) -> list[str]:
    lines = text.splitlines()
    if references_heading:
        pattern = re.compile(rf"^\s{{0,3}}#{{0,6}}\s*{re.escape(references_heading)}\s*$", re.I)
    else:
        pattern = REF_HEADING_RE

    start = 0
    for i, line in enumerate(lines):
        if pattern.match(line):
            start = i + 1
            break

    block = "\n".join(lines[start:])
    raw_entries = re.split(r"\n\s*\n|(?=\n\s*(?:\[\d+\]|\d+[\).])\s+)", block)
    entries = []
    for entry in raw_entries:
        cleaned = " ".join(line.strip() for line in entry.splitlines()).strip()
        cleaned = re.sub(r"^\s*(?:[-*]\s*)", "", cleaned)
        if len(cleaned) < 20:
            continue
        if DOI_RE.search(cleaned) or PMID_RE.search(cleaned) or YEAR_RE.search(cleaned):
            entries.append(cleaned)
    return entries


def detect_format(reference: str) -> str:
    text = reference.strip()
    if re.match(r"^\[\d+\]", text) or re.search(r"\[[JMADEC]\]", text):
        return "gbt7714"
    if re.match(r"^\d+[\).]\s+", text):
        return "vancouver"
    if re.search(r"\([12][0-9]{3}[a-z]?\)\.?\s+", text):
        return "apa"
    if re.search(r"\b\d{4};\d", text) or re.search(r"\.\s+[A-Za-z].+\.\s+\d{4};", text):
        return "vancouver"
    return "free_text"


def extract_authors(reference: str, citation_format: str) -> list[str]:
    text = re.sub(r"^\s*(?:\[\d+\]|\d+[\).])\s*", "", reference).strip()
    if citation_format == "apa":
        head = re.split(r"\([12][0-9]{3}[a-z]?\)", text, maxsplit=1)[0]
    else:
        head = re.split(r"\.\s+", text, maxsplit=1)[0]
    head = re.sub(DOI_RE, "", head)
    parts = re.split(r"\s*(?:,?\s*&\s*|\s+and\s+|;\s*|，|、)\s*", head)
    authors = [p.strip(" .") for p in parts if p.strip(" .")]
    return authors[:12]


def guess_title(reference: str, citation_format: str) -> str:
    text = re.sub(DOI_RE, " ", reference)
    text = re.sub(URL_RE, " ", text)
    text = re.sub(r"^\s*(?:\[\d+\]|\d+[\).])\s*", "", text).strip()

    if citation_format == "apa":
        match = re.search(r"\([12][0-9]{3}[a-z]?\)\.?\s+(.+)", text)
        if match:
            return re.split(r"\.\s+", match.group(1), maxsplit=1)[0].strip(" .")

    if citation_format == "gbt7714":
        body = re.split(r"\.\s*", text, maxsplit=1)
        if len(body) > 1:
            title = re.split(r"\[[A-Z]\]|\.\s*", body[1], maxsplit=1)[0]
            return title.strip(" .")

    parts = [p.strip() for p in re.split(r"\.\s+", text) if p.strip()]
    candidates = []
    for part in parts:
        norm = normalize_text(part)
        word_count = len(norm.split())
        if 4 <= word_count <= 40 and not YEAR_RE.fullmatch(part):
            candidates.append(part)
    if candidates:
        return candidates[0].strip(" .")
    return text[:180].strip(" .")


def guess_journal(reference: str, title: str) -> str:
    after_title = reference
    if title and title in reference:
        after_title = reference.split(title, 1)[-1]
    after_title = re.sub(DOI_RE, "", after_title)
    after_title = re.sub(URL_RE, "", after_title)
    after_title = after_title.replace("[J]", "")
    parts = [p.strip(" .,:，") for p in re.split(r"\.\s+|,\s*", after_title) if p.strip(" .,:，")]
    for part in parts:
        if YEAR_RE.search(part) or PMID_RE.search(part):
            continue
        if 1 <= len(part.split()) <= 12:
            return part
    return ""


def parse_reference(reference: str, index: int, source_line: int | None = None, context: str = "") -> ReferenceEntry:
    citation_format = detect_format(reference)
    doi_match = DOI_RE.search(reference)
    pmid_match = PMID_RE.search(reference)
    urls = [url.rstrip(".,;)]}") for url in URL_RE.findall(reference)]
    doi = clean_doi(doi_match.group(0)) if doi_match else ""
    pmid = pmid_match.group(1) if pmid_match else ""
    title = html.unescape(guess_title(reference, citation_format))
    authors = extract_authors(reference, citation_format)
    year = first_year(reference)
    journal = html.unescape(guess_journal(reference, title))
    key = normalize_text(" ".join([title, year, authors[0] if authors else ""]))
    entry = ReferenceEntry(
        index=index,
        original=reference,
        citation_format=citation_format,
        title=title,
        authors=authors,
        journal=journal,
        year=year,
        doi=doi,
        pmid=pmid,
        urls=urls,
        normalized_key=key,
        source_lines=[source_line] if source_line is not None else [],
        context=context or reference,
    )
    return finalize_entry_quality(entry)


def build_entries(text: str, references_heading: str | None, input_mode: str) -> list[ReferenceEntry]:
    machine_entries = parse_machine_record_entries(text)
    worksheet_entries = parse_worksheet_entries(text)
    reference_entries = [parse_reference(ref, idx + 1) for idx, ref in enumerate(split_references(text, references_heading))]
    doi_entries = extract_doi_context_entries(text)
    if input_mode == "records":
        return machine_entries
    if input_mode == "worksheet":
        return worksheet_entries
    if input_mode == "references":
        return reference_entries
    if input_mode == "doi-context":
        return dedupe_doi_entries(doi_entries)
    if machine_entries:
        return machine_entries
    if worksheet_entries:
        return worksheet_entries
    if len(doi_entries) >= max(len(reference_entries) + 5, len(reference_entries) * 2, 10):
        return dedupe_doi_entries(doi_entries)
    return reference_entries


def parse_machine_record_entries(text: str) -> list[ReferenceEntry]:
    payload = parse_json_or_jsonl(text)
    if payload is None:
        return []
    records = machine_payload_records(payload)
    entries = []
    for idx, record in enumerate(records, 1):
        if isinstance(record, dict):
            entry = machine_record_to_entry(record, idx)
            if entry:
                entries.append(entry)
    validate_entry_indices(entries)
    return entries


def validate_entry_indices(entries: list[ReferenceEntry]) -> None:
    seen = set()
    for entry in entries:
        if entry.index in seen:
            raise ValueError(f"Duplicate reference index: {entry.index}. Give each reference a unique index.")
        seen.add(entry.index)


def parse_json_or_jsonl(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    records = []
    for line in stripped.splitlines():
        candidate = line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            return None
        records.append(value)
    return records if records else None


def machine_payload_records(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("records"), list):
        return payload["records"]
    if isinstance(payload.get("references"), list):
        return payload["references"]
    if isinstance(payload.get("items"), list):
        return payload["items"]
    if "source" in payload:
        return [payload]
    return []


def machine_record_to_entry(record: dict[str, Any], fallback_index: int) -> ReferenceEntry | None:
    source = record.get("source") if isinstance(record.get("source"), dict) else record
    identifiers = source.get("identifiers") if isinstance(source.get("identifiers"), dict) else {}
    raw_index = record.get("index", source.get("index", fallback_index))
    try:
        index = int(raw_index)
    except Exception:
        index = fallback_index
    title = scalar(source.get("title") or source.get("source_title"))
    authors = normalize_authors(source.get("authors") or source.get("source_authors"))
    year = first_year(str(source.get("year") or source.get("publication_year") or ""))
    journal = scalar(source.get("journal") or source.get("container_title") or source.get("source_journal"))
    doi = clean_doi(scalar(identifiers.get("doi") or source.get("doi") or source.get("source_doi")))
    pmid_match = re.search(r"\d{6,9}", scalar(identifiers.get("pmid") or source.get("pmid") or source.get("source_pmid")))
    pmid = pmid_match.group(0) if pmid_match else ""
    urls = normalize_urls(identifiers.get("urls") or source.get("urls") or source.get("url"))
    volume = scalar(source.get("volume"))
    issue = scalar(source.get("issue"))
    pages = scalar(source.get("pages") or source.get("page"))
    article_number = scalar(source.get("article_number") or source.get("article-number") or source.get("articleNumber"))
    original = scalar(source.get("original_text") or source.get("original") or source.get("raw") or title or doi or pmid)
    context = scalar(source.get("context") or source.get("note") or original)
    source_lines = [int(value) for value in re.findall(r"\d+", scalar(source.get("source_lines") or source.get("source_line") or source.get("line") or ""))]
    if not any([title, doi, pmid, original]):
        return None
    citation_format = scalar(source.get("citation_format") or record.get("citation_format")) or detect_format(original)
    entry = ReferenceEntry(
        index=index,
        original=original,
        citation_format=citation_format,
        title=html.unescape(title),
        authors=authors,
        journal=html.unescape(journal),
        year=year,
        doi=doi,
        pmid=pmid,
        urls=urls,
        normalized_key=normalize_text(" ".join([title, year, doi or pmid])),
        volume=volume,
        issue=issue,
        pages=pages,
        article_number=article_number,
        source_lines=source_lines,
        context=context,
        input_source="records.v1",
    )
    return finalize_entry_quality(entry)


def scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "; ".join(scalar(item) for item in value if scalar(item))
    if isinstance(value, dict):
        for key in ("value", "name", "title", "display_name", "text"):
            if key in value:
                return scalar(value[key])
    return str(value).strip()


def normalize_authors(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        authors = []
        for item in value:
            if isinstance(item, dict):
                name = scalar(item.get("name") or item.get("display_name") or item.get("full_name"))
                if not name:
                    given = scalar(item.get("given") or item.get("givenName"))
                    family = scalar(item.get("family") or item.get("familyName"))
                    name = f"{family}, {given}" if family and given else family or given
            else:
                name = scalar(item)
            if name:
                authors.append(name)
        return authors
    return parse_author_field(scalar(value))


def normalize_urls(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        values = [scalar(item) for item in value]
    else:
        values = [scalar(value)]
    urls = []
    for item in values:
        urls.extend(url.rstrip(".,;)]}") for url in URL_RE.findall(item))
    return urls


def parse_worksheet_entries(text: str) -> list[ReferenceEntry]:
    table = find_markdown_worksheet_table(text)
    if not table:
        return []
    header, rows = table
    aliases = [canonical_header(cell) for cell in header]
    if "doi" not in aliases and "title" not in aliases:
        return []
    entries = []
    for row_number, row in enumerate(rows, 1):
        mapped = {}
        for key, value in zip(aliases, row):
            if key:
                mapped[key] = value.strip()
        if not any(mapped.get(key) for key in ("title", "doi", "pmid", "original")):
            continue
        entries.append(worksheet_row_to_entry(mapped, len(entries) + 1, row_number))
    return entries


def find_markdown_worksheet_table(text: str) -> tuple[list[str], list[list[str]]] | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not is_markdown_table_row(line):
            continue
        if i + 1 >= len(lines) or not is_markdown_separator_row(lines[i + 1]):
            continue
        header = split_markdown_row(line)
        aliases = [canonical_header(cell) for cell in header]
        if not ({"doi", "title"} & set(aliases)):
            continue
        rows = []
        for raw in lines[i + 2 :]:
            if not is_markdown_table_row(raw):
                break
            rows.append(split_markdown_row(raw))
        if rows:
            return header, rows
    return None


def is_markdown_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def is_markdown_separator_row(line: str) -> bool:
    stripped = line.strip().strip("|")
    cells = [cell.strip() for cell in stripped.split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def split_markdown_row(line: str) -> list[str]:
    placeholder = "\u241f"
    stripped = line.strip().strip("|")
    stripped = stripped.replace(r"\|", placeholder)
    return [cell.strip().replace(placeholder, "|") for cell in stripped.split("|")]


def canonical_header(value: str) -> str:
    key = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "", value).lower()
    return WORKSHEET_HEADER_ALIASES.get(key, "")


def worksheet_row_to_entry(row: dict[str, str], fallback_index: int, row_number: int) -> ReferenceEntry:
    raw_index = row.get("index", "")
    try:
        index = int(re.search(r"\d+", raw_index).group(0)) if raw_index and re.search(r"\d+", raw_index) else fallback_index
    except Exception:
        index = fallback_index
    original = row.get("original") or row.get("context") or row.get("title") or row.get("doi") or ""
    doi = clean_doi(row.get("doi", ""))
    pmid_match = re.search(r"\d{6,9}", row.get("pmid", ""))
    pmid = pmid_match.group(0) if pmid_match else ""
    urls = [url.rstrip(".,;)]}") for url in URL_RE.findall(row.get("url", "") + " " + original)]
    title = html.unescape(row.get("title", "").strip())
    authors = parse_author_field(row.get("authors", ""))
    year = first_year(row.get("year", ""))
    journal = html.unescape(row.get("journal", "").strip())
    citation_format = row.get("citation_format") or detect_format(original)
    source_line_values = [int(value) for value in re.findall(r"\d+", row.get("source_line", ""))]
    entry = ReferenceEntry(
        index=index,
        original=original,
        citation_format=citation_format,
        title=title,
        authors=authors,
        journal=journal,
        year=year,
        doi=doi,
        pmid=pmid,
        urls=urls,
        normalized_key=normalize_text(row.get("query_key") or " ".join([title, year, doi or pmid])),
        source_lines=source_line_values or [row_number],
        context=row.get("context") or original,
        input_source="worksheet",
    )
    return finalize_entry_quality(entry)


def parse_author_field(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if ";" in value:
        parts = value.split(";")
    elif " and " in value.lower():
        parts = re.split(r"\s+and\s+", value, flags=re.I)
    else:
        parts = re.split(r"\s*(?:，|、)\s*", value)
    return [part.strip(" .") for part in parts if part.strip(" .")][:12]


def finalize_entry_quality(entry: ReferenceEntry) -> ReferenceEntry:
    warnings = list(entry.input_warnings)
    reliable = True
    title_norm = normalize_text(entry.title)
    if not entry.title:
        reliable = False
        warnings.append("source title is missing; DOI/PMID can be verified but title agreement cannot be judged")
    elif is_unreliable_source_title(entry.title, entry.authors, entry.original):
        reliable = False
        warnings.append("source title looks like an author/header/metadata line; skip identifier-hijacking judgment from this title")
    elif len(title_norm.split()) < 4 and not re.search(r"[\u4e00-\u9fff]", entry.title):
        reliable = False
        warnings.append("source title is too short for reliable title matching")
    entry.title_reliable = reliable
    entry.input_warnings = sorted(set(warnings))
    return entry


def is_unreliable_source_title(title: str, authors: list[str], original: str) -> bool:
    norm = normalize_text(title)
    if not norm:
        return True
    metadata_terms = {
        "author",
        "authors",
        "reference",
        "references",
        "candidate",
        "doi",
        "pmid",
        "title",
        "journal",
        "year",
        "编号",
        "作者",
        "候选",
        "题名",
        "标题",
        "期刊",
        "年份",
    }
    if norm in metadata_terms:
        return True
    if re.fullmatch(r"[\d\s#._-]+", title.strip()):
        return True
    if authors:
        authors_norm = normalize_text(" ".join(authors))
        if authors_norm and norm and (norm in authors_norm or authors_norm in norm):
            return True
    comma_like = title.count(",") + title.count(";") + title.count("，") + title.count("、")
    words = norm.split()
    chunks = re.split(r"[,;，、]", title)
    if comma_like >= 2 and all(re.fullmatch(r"[\w'’ -]+ [A-Z]{1,5}\.?", chunk.strip()) for chunk in chunks):
        return True
    if DOI_RE.search(title) or PMID_RE.search(title):
        return True
    if original and title.strip() == original.strip() and not (DOI_RE.search(original) or YEAR_RE.search(original)):
        return True
    return False


def extract_doi_context_entries(text: str) -> list[ReferenceEntry]:
    lines = text.splitlines()
    entries = []
    seen_on_line: set[tuple[int, str]] = set()
    for i, line in enumerate(lines):
        dois = [clean_doi(match.group(0)) for match in DOI_RE.finditer(line)]
        if not dois:
            continue
        previous_line = nearest_nonempty(lines, i, -1)
        next_line = nearest_nonempty(lines, i, 1)
        for doi in dois:
            key = (i + 1, doi)
            if key in seen_on_line:
                continue
            seen_on_line.add(key)
            line_without_ids = DOI_RE.sub(" ", line)
            line_without_ids = URL_RE.sub(" ", line_without_ids)
            line_has_context = len(normalize_text(line_without_ids)) > 8
            context_parts = [part for part in ([line] if line_has_context else [previous_line, line, next_line]) if part]
            context = " ".join(context_parts)
            entry_text = line if line_has_context else context
            entry = parse_reference(entry_text, len(entries) + 1, source_line=i + 1, context=context)
            entry.doi = doi
            entry.normalized_key = normalize_text(" ".join([entry.title, entry.year, entry.doi]))
            entries.append(entry)
    return entries


def nearest_nonempty(lines: list[str], start: int, direction: int, max_distance: int = 2) -> str:
    for step in range(1, max_distance + 1):
        idx = start + step * direction
        if 0 <= idx < len(lines) and lines[idx].strip():
            return lines[idx].strip()
    return ""


def dedupe_doi_entries(entries: list[ReferenceEntry]) -> list[ReferenceEntry]:
    by_doi: dict[str, ReferenceEntry] = {}
    for entry in entries:
        if not entry.doi:
            continue
        existing = by_doi.get(entry.doi)
        if not existing:
            by_doi[entry.doi] = entry
            continue
        existing.occurrence_count += 1
        existing.source_lines.extend(entry.source_lines)
        if len(entry.context) > len(existing.context):
            existing.context = entry.context
        if len(entry.title) > len(existing.title):
            existing.title = entry.title
            existing.title_reliable = entry.title_reliable
        if not existing.year and entry.year:
            existing.year = entry.year
        if not existing.authors and entry.authors:
            existing.authors = entry.authors
        existing.input_warnings = sorted(set(existing.input_warnings + entry.input_warnings))
        existing.title_reliable = existing.title_reliable or entry.title_reliable
    deduped = list(by_doi.values())
    for idx, entry in enumerate(deduped, 1):
        entry.index = idx
    return deduped


class ApiClient:
    def __init__(
        self,
        email: str = "",
        timeout: int = 8,
        crossref_workers: int = CROSSREF_POLITE_CONCURRENCY,
        pubmed_workers: int = 0,
        openalex_workers: int = OPENALEX_DEFAULT_CONCURRENCY,
        ncbi_api_key: str = "",
        openalex_api_key: str = "",
        metrics: RuntimeMetrics | None = None,
    ) -> None:
        self.email = email
        self.timeout = timeout
        self.ncbi_api_key = ncbi_api_key
        self.openalex_api_key = openalex_api_key
        self.metrics = metrics or RuntimeMetrics()
        crossref_concurrency = CROSSREF_POLITE_CONCURRENCY if email else CROSSREF_PUBLIC_CONCURRENCY
        crossref_rate = CROSSREF_POLITE_RATE_PER_SECOND if email else CROSSREF_PUBLIC_RATE_PER_SECOND
        pubmed_rate = NCBI_API_KEY_RATE_PER_SECOND if ncbi_api_key else NCBI_DEFAULT_RATE_PER_SECOND
        self.crossref_workers = min(max(1, crossref_workers), crossref_concurrency)
        self.pubmed_workers = max(1, pubmed_workers or int(pubmed_rate))
        self.openalex_workers = max(1, openalex_workers)
        self.crossref_limiter = RateLimiter(crossref_rate, crossref_concurrency)
        self.pubmed_limiter = RateLimiter(pubmed_rate, self.pubmed_workers)
        self.openalex_limiter = RateLimiter(OPENALEX_DEFAULT_RATE_PER_SECOND, self.openalex_workers)
        self.crossref_doi_cache: dict[str, CanonicalRecord | None] = {}
        self.search_failures: dict[tuple[str, str], str] = {}
        self.crossref_search_cache: dict[str, list[CanonicalRecord]] = {}
        self.pubmed_pmid_cache: dict[str, CanonicalRecord | None] = {}
        self.pubmed_search_cache: dict[str, list[CanonicalRecord]] = {}
        self.openalex_doi_cache: dict[str, CanonicalRecord | None] = {}
        self.openalex_pmid_cache: dict[str, CanonicalRecord | None] = {}
        self.openalex_search_cache: dict[str, list[CanonicalRecord]] = {}

    def get_json(self, url: str) -> dict[str, Any]:
        data = self.get_bytes(url)
        return json.loads(data.decode("utf-8"))

    def get_bytes(self, url: str) -> bytes:
        headers = {
            "User-Agent": f"biomedical-reference-verifier/{VERSION}" + (f" (mailto:{self.email})" if self.email else ""),
            "Accept": "application/json, text/xml;q=0.9, */*;q=0.8",
        }
        req = urllib.request.Request(url, headers=headers)
        limiter = self.limiter_for_url(url)
        provider = "crossref" if "crossref.org" in url else "pubmed" if "ncbi.nlm.nih.gov" in url else "openalex" if "openalex.org" in url else "other"
        started = time.monotonic()

        def request_once(timeout: float, attempt: int) -> bytes:
            attempt_started = time.monotonic()
            try:
                with limiter.slot():
                    with urllib.request.urlopen(req, timeout=timeout) as response:
                        body = response.read()
                self.metrics.record(provider, "success", time.monotonic() - attempt_started, attempt=attempt)
                return body
            except urllib.error.HTTPError as exc:
                status = "not_found" if exc.code == 404 else "rate_limited" if exc.code == 429 else "network_error"
                self.metrics.record(provider, status, time.monotonic() - attempt_started, attempt=attempt, detail=f"HTTP {exc.code}")
                raise
            except urllib.error.URLError as exc:
                reason = str(exc.reason)
                status = "timeout" if "timed out" in reason.lower() else "network_error"
                self.metrics.record(provider, status, time.monotonic() - attempt_started, attempt=attempt, detail=reason)
                raise
            except TimeoutError as exc:
                self.metrics.record(provider, "timeout", time.monotonic() - attempt_started, attempt=attempt, detail=str(exc))
                raise

        try:
            return run_with_retry(request_once, first_timeout=min(float(self.timeout), 2.5), retries=1)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.code} for {url}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network error for {url}: {exc.reason}") from exc
        except TimeoutError as exc:
            raise RuntimeError(f"Timeout for {url}") from exc

    def limiter_for_url(self, url: str) -> RateLimiter:
        host = urllib.parse.urlparse(url).netloc.lower()
        if "crossref.org" in host:
            return self.crossref_limiter
        if "ncbi.nlm.nih.gov" in host:
            return self.pubmed_limiter
        if "openalex.org" in host:
            return self.openalex_limiter
        return RateLimiter(1.0, 1)

    def crossref_by_doi(self, doi: str) -> CanonicalRecord | None:
        doi = clean_doi(doi)
        if doi in self.crossref_doi_cache:
            return self.crossref_doi_cache[doi]
        try:
            params = urllib.parse.urlencode({"mailto": self.email} if self.email else {})
            url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="") + "?" + params
            item = self.get_json(url).get("message", {})
            record = crossref_record(item, score=1.0)
        except Exception:
            record = None
        self.crossref_doi_cache[doi] = record
        return record

    def crossref_by_dois_parallel(self, dois: Iterable[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        unique = [doi for doi in sorted(set(clean_doi(doi) for doi in dois if doi)) if doi]
        missing = [doi for doi in unique if doi not in self.crossref_doi_cache]
        if missing:
            self.run_doi_workers(missing, self.crossref_workers, self.crossref_by_doi, stop_event)
        return {doi: self.crossref_doi_cache.get(doi) for doi in unique}

    def crossref_search(self, query: str, limit: int = 3) -> list[CanonicalRecord]:
        key = normalize_text(query)[:240]
        if key in self.crossref_search_cache:
            return self.crossref_search_cache[key]
        self.search_failures.pop(("crossref", key), None)
        try:
            params = {
                "query.title": query,
                "rows": str(limit),
                **({"mailto": self.email} if self.email else {}),
            }
            url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
            items = self.get_json(url)["message"]["items"]
            records = []
            for item in items:
                record = crossref_record(item, score=float(item.get("score") or 0.0))
                if record:
                    records.append(record)
        except Exception as exc:
            self.search_failures[("crossref", key)] = type(exc).__name__
            return []
        self.crossref_search_cache[key] = records
        return records

    def fetch_pubmed_pmids(self, pmids: Iterable[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        pmid_list = [pmid for pmid in pmids if pmid]
        missing = [pmid for pmid in sorted(set(pmid_list)) if pmid not in self.pubmed_pmid_cache]
        if missing:
            try:
                if stop_event and stop_event.is_set():
                    raise RuntimeError("PubMed lookup stopped by grace timer")
                params = {
                    "db": "pubmed",
                    "id": ",".join(missing),
                    "retmode": "xml",
                    "tool": "biomedical-reference-verifier",
                    **({"email": self.email} if self.email else {}),
                }
                if self.ncbi_api_key:
                    params["api_key"] = self.ncbi_api_key
                url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(params)
                root = ET.fromstring(self.get_bytes(url))
                found = {}
                for article in root.findall(".//PubmedArticle"):
                    record = pubmed_record(article)
                    if record.pmid:
                        found[record.pmid] = record
                for pmid in missing:
                    self.pubmed_pmid_cache[pmid] = found.get(pmid)
            except Exception:
                for pmid in missing:
                    self.pubmed_pmid_cache[pmid] = None
        return {pmid: self.pubmed_pmid_cache.get(pmid) for pmid in pmid_list}

    def pubmed_search(self, query: str, limit: int = 3) -> list[CanonicalRecord]:
        key = normalize_text(query)[:240]
        if key in self.pubmed_search_cache:
            return self.pubmed_search_cache[key]
        self.search_failures.pop(("pubmed", key), None)
        try:
            params = {
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": str(limit),
                "tool": "biomedical-reference-verifier",
                **({"email": self.email} if self.email else {}),
            }
            if self.ncbi_api_key:
                params["api_key"] = self.ncbi_api_key
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
            ids = self.get_json(url)["esearchresult"]["idlist"]
            pmid_map = self.fetch_pubmed_pmids(ids)
            missing = [pmid for pmid in ids if pmid_map.get(pmid) is None]
            if missing:
                for pmid in missing:
                    self.pubmed_pmid_cache.pop(pmid, None)
                raise RuntimeError("PubMed search matched IDs but record retrieval was incomplete")
            records = [record for record in pmid_map.values() if record]
        except Exception as exc:
            self.search_failures[("pubmed", key)] = type(exc).__name__
            return []
        self.pubmed_search_cache[key] = records
        return records

    def pubmed_by_doi(self, doi: str) -> CanonicalRecord | None:
        doi = clean_doi(doi)
        key = f"doi:{doi}"
        if key in self.pubmed_search_cache:
            records = self.pubmed_search_cache[key]
            return records[0] if records else None
        records = self.pubmed_search(f"{doi}[AID]", limit=1)
        self.pubmed_search_cache[key] = records
        return records[0] if records else None

    def pubmed_by_dois_parallel(self, dois: Iterable[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        unique = [doi for doi in sorted(set(clean_doi(doi) for doi in dois if doi)) if doi]
        results: dict[str, CanonicalRecord | None] = {doi: None for doi in unique}
        if not unique:
            return results
        batches = [unique[i : i + 20] for i in range(0, len(unique), 20)]
        work: queue.Queue[list[str]] = queue.Queue()
        lock = threading.Lock()
        for batch in batches:
            work.put(batch)

        def worker() -> None:
            while not (stop_event and stop_event.is_set()):
                try:
                    batch = work.get_nowait()
                except queue.Empty:
                    return
                try:
                    batch_result = self.pubmed_by_doi_batch(batch, stop_event)
                    with lock:
                        results.update(batch_result)
                except Exception:
                    pass
                finally:
                    work.task_done()

        threads = [threading.Thread(target=worker, daemon=True) for _ in range(min(self.pubmed_workers, len(batches)))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return results

    def pubmed_by_doi_batch(self, dois: list[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        try:
            return self._pubmed_by_doi_batch_once(dois, stop_event)
        except Exception:
            if len(dois) <= 1 or (stop_event and stop_event.is_set()):
                return {doi: None for doi in dois}
            midpoint = len(dois) // 2
            left = self.pubmed_by_doi_batch(dois[:midpoint], stop_event)
            right = self.pubmed_by_doi_batch(dois[midpoint:], stop_event)
            return {**left, **right}

    def _pubmed_by_doi_batch_once(self, dois: list[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        results: dict[str, CanonicalRecord | None] = {doi: None for doi in dois}
        if not dois:
            return results
        if stop_event and stop_event.is_set():
            return results
        term = " OR ".join(f'"{doi}"[AID]' for doi in dois)
        params = {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": str(max(len(dois) * 3, 20)),
            "tool": "biomedical-reference-verifier",
            **({"email": self.email} if self.email else {}),
        }
        if self.ncbi_api_key:
            params["api_key"] = self.ncbi_api_key
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
        ids = self.get_json(url).get("esearchresult", {}).get("idlist", [])
        if not ids:
            return results
        records = [record for record in self.fetch_pubmed_pmids(ids, stop_event).values() if record]
        for record in records:
            if record.doi:
                doi = clean_doi(record.doi)
                if doi in results:
                    results[doi] = record
        return results

    def openalex_params(self, params: dict[str, str]) -> dict[str, str]:
        if self.openalex_api_key:
            params["api_key"] = self.openalex_api_key
        if self.email:
            params["mailto"] = self.email
        return params

    def openalex_by_doi(self, doi: str) -> CanonicalRecord | None:
        doi = clean_doi(doi)
        if doi in self.openalex_doi_cache:
            return self.openalex_doi_cache[doi]
        try:
            identifier = urllib.parse.quote(f"doi:{doi}", safe=":")
            params = self.openalex_params(
                {
                    "select": "id,doi,title,display_name,publication_year,authorships,primary_location,ids",
                }
            )
            url = f"https://api.openalex.org/works/{identifier}?" + urllib.parse.urlencode(params)
            record = openalex_record(self.get_json(url), score=1.0)
        except Exception:
            record = None
        self.openalex_doi_cache[doi] = record
        return record

    def openalex_by_pmid(self, pmid: str) -> CanonicalRecord | None:
        pmid = pmid.strip()
        if pmid in self.openalex_pmid_cache:
            return self.openalex_pmid_cache[pmid]
        try:
            identifier = urllib.parse.quote(f"pmid:{pmid}", safe=":")
            params = self.openalex_params(
                {
                    "select": "id,doi,title,display_name,publication_year,authorships,primary_location,ids",
                }
            )
            url = f"https://api.openalex.org/works/{identifier}?" + urllib.parse.urlencode(params)
            record = openalex_record(self.get_json(url), score=1.0)
        except Exception:
            record = None
        self.openalex_pmid_cache[pmid] = record
        return record

    def openalex_by_dois_parallel(self, dois: Iterable[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        unique = [doi for doi in sorted(set(clean_doi(doi) for doi in dois if doi)) if doi]
        missing = [doi for doi in unique if doi not in self.openalex_doi_cache]
        if missing:
            self.run_doi_workers(missing, self.openalex_workers, self.openalex_by_doi, stop_event)
        return {doi: self.openalex_doi_cache.get(doi) for doi in unique}

    def openalex_by_pmids_parallel(self, pmids: Iterable[str], stop_event: threading.Event | None = None) -> dict[str, CanonicalRecord | None]:
        unique = [pmid for pmid in sorted(set(pmid.strip() for pmid in pmids if pmid.strip())) if pmid]
        missing = [pmid for pmid in unique if pmid not in self.openalex_pmid_cache]
        if missing:
            self.run_doi_workers(missing, self.openalex_workers, self.openalex_by_pmid, stop_event)
        return {pmid: self.openalex_pmid_cache.get(pmid) for pmid in unique}

    def openalex_search(self, query: str, limit: int = 3) -> list[CanonicalRecord]:
        key = normalize_text(query)[:240]
        if key in self.openalex_search_cache:
            return self.openalex_search_cache[key]
        self.search_failures.pop(("openalex", key), None)
        try:
            params = self.openalex_params(
                {
                    "search": query,
                    "per_page": str(limit),
                    "select": "id,doi,title,display_name,publication_year,authorships,primary_location,ids",
                }
            )
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            items = self.get_json(url)["results"]
            records = [record for item in items if (record := openalex_record(item, score=0.0))]
        except Exception as exc:
            self.search_failures[("openalex", key)] = type(exc).__name__
            return []
        self.openalex_search_cache[key] = records
        return records

    def run_doi_workers(
        self,
        items: list[str],
        worker_count: int,
        lookup: Any,
        stop_event: threading.Event | None = None,
    ) -> None:
        work: queue.Queue[str] = queue.Queue()
        for item in items:
            work.put(item)

        def worker() -> None:
            while not (stop_event and stop_event.is_set()):
                try:
                    item = work.get_nowait()
                except queue.Empty:
                    return
                try:
                    lookup(item)
                except Exception:
                    pass
                finally:
                    work.task_done()

        threads = [threading.Thread(target=worker, daemon=True) for _ in range(min(worker_count, len(items)))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def crossref_record(item: dict[str, Any], score: float) -> CanonicalRecord | None:
    title = html.unescape(first_value(item.get("title")))
    if not title:
        return None
    year = ""
    for key in ("published-print", "published-online", "issued"):
        parts = item.get(key, {}).get("date-parts") or []
        if parts and parts[0]:
            year = str(parts[0][0])
            break
    journal = html.unescape(first_value(item.get("container-title")))
    authors = []
    for author in item.get("author") or []:
        family = author.get("family", "")
        given = author.get("given", "")
        name = f"{family}, {given}" if family and given else family or given or author.get("name", "")
        if name:
            authors.append(name)
    doi = clean_doi(item.get("DOI", ""))
    return CanonicalRecord(
        source="Crossref",
        title=title,
        year=year,
        journal=journal,
        journal_abbreviation=html.unescape(first_value(item.get("short-container-title"))),
        publication_years=list(dict.fromkeys(str(parts[0][0]) for key in ("published-print", "published-online", "issued") if (parts := item.get(key, {}).get("date-parts")) and parts[0])),
        volume=scalar(item.get("volume")),
        issue=scalar(item.get("issue")),
        pages=scalar(item.get("page")),
        article_number=scalar(item.get("article-number") or item.get("article_number")),
        doi=doi,
        authors=authors,
        url=f"https://doi.org/{doi}" if doi else item.get("URL", ""),
        score=score,
    )


def pubmed_record(article: ET.Element) -> CanonicalRecord:
    pmid = article.findtext(".//PMID") or ""
    title_node = article.find(".//ArticleTitle")
    title = html.unescape("".join(title_node.itertext()).strip()) if title_node is not None else ""
    journal = html.unescape(article.findtext(".//Journal/Title") or article.findtext(".//Journal/ISOAbbreviation") or "")
    year = article.findtext(".//JournalIssue/PubDate/Year") or first_year(article.findtext(".//JournalIssue/PubDate/MedlineDate") or "")
    volume = article.findtext(".//JournalIssue/Volume") or ""
    issue = article.findtext(".//JournalIssue/Issue") or ""
    pages = article.findtext(".//Pagination/MedlinePgn") or article.findtext(".//ELocationID[@EIdType='pii']") or ""
    doi = ""
    for article_id in article.findall(".//ArticleId"):
        if article_id.attrib.get("IdType", "").lower() == "doi":
            doi = clean_doi(article_id.text or "")
            break
    authors = []
    for author in article.findall(".//Author"):
        last = author.findtext("LastName") or ""
        fore = author.findtext("ForeName") or author.findtext("Initials") or ""
        name = f"{last}, {fore}" if last and fore else last or fore or author.findtext("CollectiveName") or ""
        name = re.sub(r"\.?\s*Electronic address:.*$", "", name, flags=re.I).strip()
        if name:
            authors.append(name)
    return CanonicalRecord(
        source="PubMed",
        title=title,
        year=year,
        journal=journal,
        journal_abbreviation=article.findtext(".//Journal/ISOAbbreviation") or "",
        volume=volume,
        issue=issue,
        pages=pages,
        doi=doi,
        pmid=pmid,
        authors=authors,
        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        score=1.0,
    )


def openalex_record(item: dict[str, Any], score: float) -> CanonicalRecord | None:
    title = html.unescape(item.get("title") or item.get("display_name") or "")
    if not title:
        return None
    doi = clean_doi(item.get("doi") or "")
    ids = item.get("ids") or {}
    if not doi and ids.get("doi"):
        doi = clean_doi(str(ids.get("doi")))
    pmid = ""
    raw_pmid = ids.get("pmid") or ""
    match = re.search(r"(\d{6,9})", str(raw_pmid))
    if match:
        pmid = match.group(1)
    journal = ""
    primary_location = item.get("primary_location") or {}
    if isinstance(primary_location, dict):
        source = primary_location.get("source") or {}
        if isinstance(source, dict):
            journal = html.unescape(source.get("display_name") or "")
    authors = []
    for authorship in item.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name") or ""
        if name:
            authors.append(name)
    year = str(item.get("publication_year") or "")
    biblio = item.get("biblio") if isinstance(item.get("biblio"), dict) else {}
    pages = scalar(biblio.get("first_page"))
    if biblio.get("last_page"):
        pages = f"{pages}-{scalar(biblio.get('last_page'))}" if pages else scalar(biblio.get("last_page"))
    return CanonicalRecord(
        source="OpenAlex",
        title=title,
        year=year,
        journal=journal,
        volume=scalar(biblio.get("volume")),
        issue=scalar(biblio.get("issue")),
        pages=pages,
        doi=doi,
        pmid=pmid,
        authors=authors,
        url=item.get("id") or (f"https://doi.org/{doi}" if doi else ""),
        score=score,
    )


def europepmc_record(item: dict[str, Any], score: float = 1.0) -> CanonicalRecord | None:
    title = html.unescape(scalar(item.get("title")))
    if not title:
        return None
    authors = parse_author_field(scalar(item.get("authorString") or item.get("authorList")))
    doi = clean_doi(scalar(item.get("doi")))
    pmid = scalar(item.get("pmid"))
    pmcid = scalar(item.get("pmcid"))
    url = f"https://europepmc.org/article/MED/{pmid}" if pmid else scalar(item.get("fullTextUrlList") or item.get("url"))
    journal_info = item.get("journalInfo") if isinstance(item.get("journalInfo"), dict) else {}
    journal_meta = journal_info.get("journal") if isinstance(journal_info.get("journal"), dict) else {}
    journal_title = scalar(item.get("journalTitle")) or scalar(journal_meta.get("title"))
    return CanonicalRecord(
        source="EuropePMC",
        title=title,
        year=first_year(scalar(item.get("pubYear") or item.get("firstPublicationDate") or journal_info.get("printPublicationDate"))),
        journal=html.unescape(journal_title),
        volume=scalar(item.get("journalVolume") or journal_info.get("volume")),
        issue=scalar(item.get("issue") or journal_info.get("issue")),
        pages=scalar(item.get("pageInfo") or item.get("pages")),
        doi=doi,
        pmid=pmid,
        authors=authors,
        url=url or (f"https://europepmc.org/article/PMC/{pmcid}" if pmcid else ""),
        score=score,
    )


def semantic_scholar_record(item: dict[str, Any], score: float = 1.0) -> CanonicalRecord | None:
    title = html.unescape(scalar(item.get("title")))
    if not title:
        return None
    external_ids = item.get("externalIds") if isinstance(item.get("externalIds"), dict) else {}
    authors = []
    for author in item.get("authors") or []:
        name = scalar(author.get("name") if isinstance(author, dict) else author)
        if name:
            authors.append(name)
    journal_info = item.get("journal") if isinstance(item.get("journal"), dict) else {}
    return CanonicalRecord(
        source="SemanticScholar",
        title=title,
        year=scalar(item.get("year")),
        journal=html.unescape(scalar(item.get("venue") or item.get("journal"))),
        volume=scalar(journal_info.get("volume")),
        issue=scalar(journal_info.get("issue")),
        pages=scalar(item.get("pages") or journal_info.get("pages")),
        doi=clean_doi(scalar(external_ids.get("DOI") or external_ids.get("doi") or item.get("doi"))),
        pmid=scalar(external_ids.get("PubMed") or external_ids.get("PMID") or external_ids.get("pmid")),
        authors=authors[:12],
        url=scalar(item.get("url")) or (f"https://www.semanticscholar.org/paper/{item.get('paperId')}" if item.get("paperId") else ""),
        score=score,
    )


def datacite_record(item: dict[str, Any], score: float = 1.0) -> CanonicalRecord | None:
    data = item.get("data") if isinstance(item.get("data"), dict) else item
    attributes = data.get("attributes") if isinstance(data.get("attributes"), dict) else data
    titles = attributes.get("titles") or []
    title = ""
    if titles and isinstance(titles[0], dict):
        title = scalar(titles[0].get("title"))
    title = html.unescape(title or scalar(attributes.get("title")))
    if not title:
        return None
    creators = attributes.get("creators") or []
    authors = [scalar(creator.get("name") if isinstance(creator, dict) else creator) for creator in creators]
    container = attributes.get("container") if isinstance(attributes.get("container"), dict) else {}
    return CanonicalRecord(
        source="DataCite",
        title=title,
        year=first_year(scalar(attributes.get("publicationYear") or attributes.get("published"))),
        journal=html.unescape(scalar(container.get("title") or attributes.get("publisher", {}).get("name") if isinstance(attributes.get("publisher"), dict) else attributes.get("publisher"))),
        volume=scalar(container.get("volume")),
        issue=scalar(container.get("issue")),
        pages=scalar(container.get("firstPage") or container.get("first_page")),
        doi=clean_doi(scalar(attributes.get("doi") or data.get("id"))),
        authors=[author for author in authors if author][:12],
        url=scalar(attributes.get("url")) or (f"https://doi.org/{clean_doi(scalar(attributes.get('doi') or data.get('id')))}" if clean_doi(scalar(attributes.get("doi") or data.get("id"))) else ""),
        score=score,
    )


def biorxiv_record(item: dict[str, Any], score: float = 1.0) -> CanonicalRecord | None:
    title = html.unescape(scalar(item.get("title")))
    if not title:
        return None
    doi = clean_doi(scalar(item.get("doi")))
    published_doi = clean_doi(scalar(item.get("published_doi")))
    return CanonicalRecord(
        source="bioRxiv",
        title=title,
        year=first_year(scalar(item.get("date") or item.get("published_date"))),
        journal=html.unescape(scalar(item.get("server") or item.get("category"))),
        doi=published_doi or doi,
        authors=parse_author_field(scalar(item.get("authors"))),
        url=f"https://doi.org/{published_doi or doi}" if (published_doi or doi) else "",
        score=score,
    )


def first_value(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return ""


def choose_best(entry: ReferenceEntry, records: Iterable[CanonicalRecord]) -> CanonicalRecord | None:
    best = None
    best_score = -1.0
    source_priority = {"Crossref": 6, "PubMed": 4, "OpenAlex": 3}
    for record in records:
        sim = title_similarity(entry.title, record.title)
        record.score = sim
        score = sim * 100 + source_priority.get(record.source, 0)
        if entry.year and record.year and entry.year == record.year[:4]:
            score += 5
        if first_author_matches(entry.authors, record.authors):
            score += 3
        if score > best_score:
            best = record
            best_score = score
    return best


def first_author_matches(parsed: list[str], canonical: list[str]) -> bool:
    if not parsed or not canonical:
        return False
    def key(name: str) -> str:
        return normalize_text("".join(c for c in unicodedata.normalize("NFKD", author_parts(name)[0]) if not unicodedata.combining(c)))
    return key(parsed[0]) == key(canonical[0])


def author_parts(name: str) -> tuple[str, str]:
    """Prefer explicit family, given; preserve ambiguous and corporate names."""
    name = clean_terminal(re.sub(r"\.?\s*Electronic address:.*$", "", name, flags=re.I))
    if re.search(r"\b(group|consortium|collaboration|committee|team|organization)s?\b", name, re.I):
        return name, ""
    if "," in name:
        family, given = name.split(",", 1)
        return family.strip(), given.strip()
    parts = name.split()
    if len(parts) < 2:
        return name, ""
    if re.fullmatch(r"(?:[A-Z]\.?){1,6}", parts[-1]):
        return " ".join(parts[:-1]), parts[-1].replace(".", "")
    # A full given-name-first string is supported; uncertain forms are retained.
    if all(part[:1].isupper() and not part.isupper() for part in parts):
        return parts[-1], " ".join(parts[:-1])
    return name, ""


def author_initials(given: str) -> str:
    return "".join(p.replace(".", "") if p.replace(".", "").isupper() else p[0] for p in given.replace("-", " ").split() if p)


def metadata_differences(entry: ReferenceEntry, record: CanonicalRecord) -> list[dict]:
    differences = []
    for field in ("title", "authors", "journal", "year", "doi", "pmid", "volume", "issue", "pages"):
        old, new = getattr(entry, field), getattr(record, field)
        if not old or not new:
            continue
        if field == "authors":
            equivalent = authors_agree(old, new)
        elif field == "journal":
            equivalent = normalize_text(str(old)) in {normalize_text(value) for value in [record.journal, record.journal_abbreviation, *record.journal_aliases] if value}
        elif field == "year":
            equivalent = str(old) == str(new) or str(old) in record.publication_years
        elif field == "pages":
            equivalent = normalized_pages(str(old)) == normalized_pages(str(new))
        else:
            equivalent = normalize_text(str(old)) == normalize_text(str(new))
        if not equivalent:
            differences.append({"field": field, "before": old, "after": new, "source": record.source})
    return differences


def authors_agree(source: list[str], canonical: list[str]) -> bool:
    """An explicit et al. means a prefix, not an additional author or full list."""
    def key(name: str) -> str:
        value = unicodedata.normalize("NFKD", format_ama_author(name))
        return normalize_text("".join(c for c in value if not unicodedata.combining(c)))
    truncated = bool(source and normalize_text(source[-1]) in {"et al", "等"})
    named = source[:-1] if truncated else source
    return bool(named) and (len(canonical) >= len(named) if truncated else len(canonical) == len(named)) and all(key(a) == key(b) for a, b in zip(named, canonical))


def normalized_pages(value: str) -> str:
    value = value.strip().lower().replace("–", "-").replace("—", "-")
    match = re.fullmatch(r"([a-z]*)(\d+)-([a-z]*)(\d+)", value)
    if not match:
        return value
    prefix, start, end_prefix, end = match.groups()
    end_prefix = end_prefix or prefix
    if len(end) < len(start):
        end = start[:-len(end)] + end
    return prefix + start if prefix + start == end_prefix + end else f"{prefix}{start}-{end_prefix}{end}"


def year_agrees(parsed_year: str, canonical_year: str) -> bool:
    if not parsed_year or not canonical_year:
        return True
    try:
        return abs(int(parsed_year) - int(canonical_year[:4])) <= 1
    except ValueError:
        return False


def merge_equivalent(best: CanonicalRecord, records: Iterable[CanonicalRecord]) -> CanonicalRecord:
    for record in records:
        if record is best or not ((best.doi and record.doi and clean_doi(best.doi) == clean_doi(record.doi)) or (best.pmid and record.pmid and best.pmid == record.pmid)):
            continue
        best.journal_aliases = list(dict.fromkeys([*best.journal_aliases, record.journal, record.journal_abbreviation, *record.journal_aliases]))
        if record.source == "PubMed" and record.year and title_similarity(best.title, record.title) >= 0.90:
            best.publication_years = list(dict.fromkeys([*best.publication_years, record.year]))
        if not best.doi and record.doi:
            best.doi = record.doi
        if not best.pmid and record.pmid:
            best.pmid = record.pmid
        if not best.journal and record.journal:
            best.journal = record.journal
        if not best.year and record.year:
            best.year = record.year
        if not best.volume and record.volume:
            best.volume = record.volume
        if not best.issue and record.issue:
            best.issue = record.issue
        if not best.pages and record.pages:
            best.pages = record.pages
        if not best.article_number and record.article_number:
            best.article_number = record.article_number
        if not best.authors and record.authors:
            best.authors = record.authors
        if record.pubmed_corroborated:
            best.pubmed_corroborated = True
        if record.openalex_corroborated:
            best.openalex_corroborated = True
    return best


def likely_placeholder(entry: ReferenceEntry) -> bool:
    title = normalize_text(entry.title)
    generic_terms = ["review", "overview", "advances", "recent progress", "current status", "future perspectives"]
    if len(title.split()) < 4 and not entry.doi and not entry.pmid:
        return True
    if any(term in title for term in generic_terms) and not entry.journal:
        return True
    if entry.doi and re.search(r"/(?:xxxx|xxxxx|fake|placeholder|tbd)", entry.doi):
        return True
    return False


def evidence_links(record: CanonicalRecord | None, entry: ReferenceEntry) -> list[str]:
    links = []
    if record and record.pmid:
        links.append(f"https://pubmed.ncbi.nlm.nih.gov/{record.pmid}/")
    if record and record.doi:
        links.append(f"https://doi.org/{record.doi}")
    if record and record.url and record.url not in links:
        links.append(record.url)
    if not links:
        if entry.title:
            links.append("https://pubmed.ncbi.nlm.nih.gov/?term=" + urllib.parse.quote(entry.title))
            links.append("https://search.crossref.org/?q=" + urllib.parse.quote(entry.title))
        elif entry.doi:
            links.append(f"https://doi.org/{entry.doi}")
    return links


def build_fixed_reference(
    entry: ReferenceEntry,
    record: CanonicalRecord | None,
    status: str,
    majority_format: str,
    doi_output: str = "report-only",
    include_pmid: bool = False,
) -> str:
    if not record or status not in {"verified", "minor_fix", "minor_format_error", "formatted_only"}:
        if status in SEVERE_STATUSES:
            return f"{entry.original}  [不可用：{status}，未自动修复]"
        return entry.original
    target_format = majority_format if majority_format in {"ama", "apa", "gbt7714", "vancouver"} else entry.citation_format
    if target_format == "free_text":
        target_format = "ama"
    authors = record.authors or entry.authors
    author_text = format_authors(authors, target_format)
    year = entry.year if entry.year in record.publication_years else record.year or entry.year
    journal = entry.journal if normalize_text(entry.journal) in {normalize_text(value) for value in record.journal_aliases if value} else record.journal or entry.journal
    title = record.title or entry.title
    volume = record.volume or entry.volume
    issue = record.issue or entry.issue
    pages = record.pages or entry.pages or record.article_number or entry.article_number
    if target_format == "gbt7714":
        publication = join_comma_parts([journal, year, volume + (f"({issue})" if issue else "")])
        if pages:
            publication += f": {pages}"
        core = join_sentence_parts([author_text, f"{clean_terminal(title)}[J]" if title else "", publication])
        return append_identifiers(f"[{entry.index}] {core}", record, "append" if entry.doi and not entry.recovered_doi else doi_output, include_pmid)
    if target_format in {"vancouver", "ama"}:
        return format_ama_reference(entry.index, author_text, title, journal, year, volume, issue, pages, record, "append" if entry.doi and not entry.recovered_doi else doi_output, include_pmid)
    publication = join_comma_parts([journal, volume + (f"({issue})" if issue else ""), pages])
    core = join_sentence_parts([author_text, f"({year})" if year else "", title, publication])
    return append_identifiers(core, record, "append" if entry.doi and not entry.recovered_doi else doi_output, include_pmid)


def clean_terminal(value: str) -> str:
    return re.sub(r"[\s.。;:,]+$", "", html.unescape(value or "").strip())


def ensure_period(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    return value if value.endswith((".", "。", "?", "!")) else value + "."


def join_sentence_parts(parts: list[str]) -> str:
    cleaned = [clean_terminal(part) for part in parts if clean_terminal(part)]
    return " ".join(ensure_period(part) for part in cleaned).strip()


def join_comma_parts(parts: list[str]) -> str:
    cleaned = [clean_terminal(part) for part in parts if clean_terminal(part)]
    return ", ".join(cleaned)


def append_identifiers(text: str, record: CanonicalRecord, doi_output: str, include_pmid: bool) -> str:
    text = text.strip()
    extras = []
    if doi_output == "append" and record.doi:
        extras.append(f"doi:{record.doi}")
    if include_pmid and record.doi and record.pmid:
        extras.append(f"PMID: {record.pmid}")
    if extras:
        text = f"{text} {' '.join(extras)}"
    return text.strip()


def format_ama_reference(
    index: int,
    author_text: str,
    title: str,
    journal: str,
    year: str,
    volume: str,
    issue: str,
    pages: str,
    record: CanonicalRecord,
    doi_output: str,
    include_pmid: bool,
) -> str:
    lines = [f"{index}."]
    if author_text:
        lines.append(ensure_period(clean_terminal(author_text)))
    if title:
        lines.append(ensure_period(clean_terminal(title)))
    if journal:
        lines.append(ensure_period(clean_terminal(journal)))
    pub = format_ama_publication_detail(year, volume, issue, pages)
    if pub:
        lines.append(ensure_period(pub))
    return append_identifiers(" ".join(part for part in lines if part).strip(), record, doi_output, include_pmid)


def format_ama_publication_detail(year: str, volume: str, issue: str, pages: str) -> str:
    year = clean_terminal(year)
    volume = clean_terminal(volume)
    issue = clean_terminal(issue)
    pages = clean_terminal(pages)
    if not any([year, volume, issue, pages]):
        return ""
    detail = year
    if volume:
        detail += f";{volume}"
        if issue:
            detail += f"({issue})"
        if pages:
            detail += f":{pages}"
    elif pages:
        detail += f":{pages}" if detail else pages
    return detail


def format_authors(authors: list[str], citation_format: str) -> str:
    if not authors:
        return ""
    if citation_format == "apa":
        formatted = []
        for name in authors:
            family, given = author_parts(name)
            initials = " ".join(f"{letter}." for letter in author_initials(given))
            formatted.append(f"{family}, {initials}" if initials else family)
        if len(formatted) > 20:
            return ", ".join(formatted[:19]) + ", … " + formatted[-1]
        if len(formatted) == 1:
            return formatted[0]
        return ", ".join(formatted[:-1]) + ", & " + formatted[-1]
    if citation_format in {"ama", "vancouver"}:
        formatted = [format_ama_author(name) for name in authors if format_ama_author(name)]
        if len(formatted) > 6:
            return ", ".join(formatted[:(3 if citation_format == "ama" else 6)] + ["et al"])
        return ", ".join(formatted)
    return ", ".join(authors[:3] + (["et al"] if len(authors) > 3 else []))


def format_ama_author(name: str) -> str:
    family, given = author_parts(name)
    return f"{family} {author_initials(given)}".strip()


def classify_entries(
    entries: list[ReferenceEntry],
    client: ApiClient,
    pubmed_mode: str = "corroborate",
    openalex_mode: str = "corroborate",
    parallel_grace_seconds: float = 30.0,
    citation_style: str = "source-majority",
    doi_output: str = "report-only",
    include_pmid: bool = False,
) -> list[AuditResult]:
    doi_records, pmid_records, pubmed_doi_records, openalex_doi_records, openalex_pmid_records = run_identifier_queries(
        entries, client, pubmed_mode, openalex_mode, parallel_grace_seconds
    )
    majority_format = majority_citation_format(entries)
    output_format = majority_format if citation_style == "source-majority" else citation_style
    results = []

    for entry in entries:
        id_candidates = []
        if entry.doi and doi_records.get(entry.doi):
            id_candidates.append(doi_records[entry.doi])
        if entry.doi and pubmed_doi_records.get(entry.doi):
            pubmed_record_for_doi = pubmed_doi_records[entry.doi]
            pubmed_record_for_doi.pubmed_corroborated = True
            id_candidates.append(pubmed_record_for_doi)
        if entry.pmid and pmid_records.get(entry.pmid):
            id_candidates.append(pmid_records[entry.pmid])
        if entry.doi and openalex_doi_records.get(entry.doi):
            openalex_record_for_doi = openalex_doi_records[entry.doi]
            openalex_record_for_doi.openalex_corroborated = True
            id_candidates.append(openalex_record_for_doi)
        if entry.pmid and openalex_pmid_records.get(entry.pmid):
            openalex_record_for_pmid = openalex_pmid_records[entry.pmid]
            openalex_record_for_pmid.openalex_corroborated = True
            id_candidates.append(openalex_record_for_pmid)
        provider_records = [asdict(record) for record in id_candidates]
        id_best = doi_records.get(entry.doi) or choose_best(entry, id_candidates)
        placeholder_replaced = False
        if id_best and canonical_title_placeholder(id_best.title):
            alternatives = [record for record in id_candidates if record is not id_best and record.doi and clean_doi(record.doi) == clean_doi(entry.doi) and not canonical_title_placeholder(record.title)]
            replacement = choose_best(entry, alternatives)
            if replacement and title_similarity(entry.title, replacement.title) >= 0.86 and year_agrees(entry.year, replacement.year) and first_author_matches(entry.authors, replacement.authors):
                id_best = replacement
                placeholder_replaced = True
        if id_best:
            id_best = merge_equivalent(id_best, id_candidates)
        result = first_round_classification(entry, id_best, output_format, doi_output, include_pmid)
        result.provider_records = provider_records
        if placeholder_replaced:
            result.issues.append("Primary provider returned a placeholder title; used another enabled provider's record for the same DOI, without changing the identifier.")
        if entry.doi and entry.pmid and id_best and any(record.doi and clean_doi(record.doi) != clean_doi(entry.doi) for record in id_candidates):
            result.status = "identifier_hijacking"
            result.severity = "critical"
            result.issues.append("Supplied DOI and PMID resolve to conflicting records; do not merge them.")
            result.suggested_action = "Review both identifier records before any repair."
            result.fixed_reference = build_fixed_reference(entry, None, result.status, output_format, doi_output, include_pmid)
        results.append(result)

    detect_shifted_identifiers(entries, results)
    recover_by_title(entries, results, client, output_format, pubmed_mode, openalex_mode, doi_output, include_pmid)
    detect_possible_offset(results)
    return results


def recover_missing_dois_early(entries: list[ReferenceEntry], client: ApiClient, metrics: RuntimeMetrics, mode: str, pubmed_mode: str = "corroborate", openalex_mode: str = "corroborate") -> None:
    """Recover DOI candidates before identifier verification, without writing them to the source file."""
    targets = [entry for entry in entries if not entry.doi and entry.title_reliable and entry.title]
    def recover_one(entry: ReferenceEntry) -> None:
        candidates = client.crossref_search(entry.title, limit=3)
        best = choose_best(entry, candidates)
        strong = best and title_similarity(entry.title, best.title) >= 0.86 and year_agrees(entry.year, best.year)
        if not strong and mode != "fast" and openalex_mode != "off":
            candidates.extend(client.openalex_search(entry.title, limit=3))
            best = choose_best(entry, candidates)
            strong = best and title_similarity(entry.title, best.title) >= 0.86 and year_agrees(entry.year, best.year)
        if not strong and mode != "fast" and pubmed_mode != "off":
            candidates.extend(client.pubmed_search(f'"{entry.title}"', limit=3))
            best = choose_best(entry, candidates)
            strong = best and title_similarity(entry.title, best.title) >= 0.86 and year_agrees(entry.year, best.year)
        if strong and best and best.doi and entry.authors and best.authors and first_author_matches(entry.authors, best.authors):
            recovered = clean_doi(best.doi)
            source = best.source
            entry.recovered_doi = recovered
            entry.recovered_doi_source = source
            entry.doi = recovered
            entry.input_warnings.append(f"DOI recovered by {source} title search before identifier verification; source text was not modified.")
            metrics.doi_recovered += 1

    run_recovery_workers(targets, client.crossref_workers, recover_one)


def source_canonical_record(entry: ReferenceEntry) -> CanonicalRecord:
    return CanonicalRecord(
        source="source_record",
        title=entry.title,
        year=entry.year,
        journal=entry.journal,
        volume=entry.volume,
        issue=entry.issue,
        pages=entry.pages,
        article_number=entry.article_number,
        doi=entry.doi,
        pmid=entry.pmid,
        authors=entry.authors,
        url=entry.urls[0] if entry.urls else "",
    )


def format_only_results(
    entries: list[ReferenceEntry],
    citation_style: str = "source-majority",
    doi_output: str = "report-only",
    include_pmid: bool = False,
) -> list[AuditResult]:
    majority_format = majority_citation_format(entries)
    output_format = majority_format if citation_style == "source-majority" else citation_style
    results = []
    for entry in entries:
        source_record = source_canonical_record(entry)
        issues = list(entry.input_warnings)
        issues.append("Format-only pipeline: reference was normalized from source fields without external authenticity verification.")
        if not entry.title_reliable:
            issues.append("Parsed title is missing or unreliable; formatted output may need manual source cleanup.")
        fixed = build_fixed_reference(entry, source_record if entry.title_reliable else None, "formatted_only", output_format, doi_output, include_pmid)
        results.append(
            AuditResult(
                index=entry.index,
                status="formatted_only",
                severity="low",
                citation_format=entry.citation_format,
                original=entry.original,
                parsed_title=entry.title,
                parsed_authors=entry.authors,
                parsed_journal=entry.journal,
                parsed_year=entry.year,
                parsed_doi=entry.doi,
                parsed_pmid=entry.pmid,
                parsed_title_reliable=entry.title_reliable,
                input_warnings=entry.input_warnings,
                canonical=source_record,
                identifier_record=None,
                title_similarity=0.0,
                issues=issues,
                suggested_action="Use the formatted copy only for style normalization; run verification if authenticity matters.",
                fixed_reference=fixed,
                evidence_links=evidence_links(None, entry),
            )
        )
    return results


def describe_result(result: AuditResult, entry: ReferenceEntry, pipeline: str, mode: str, channels: list[str]) -> None:
    """Keep eligibility, evidence coverage and editing separate."""
    result.verification_level = (
        "not_checked" if pipeline == "format-only" else
        "identifier_only" if result.status == "verified_identifier_only" else
        "metadata_verified" if result.status in {"verified", "minor_fix"} else
        "conflict" if result.identifier_record or result.canonical else "unresolved"
    )
    result.usable = pipeline == "verify" and result.status in {"verified", "minor_fix"}
    result.repair_state = (
        "formatted" if pipeline == "format-only" and entry.title_reliable else
        "repaired" if result.usable and result.fixed_reference != result.original else
        "unchanged" if result.usable else "retained_for_review"
    )
    if not result.checked_at:
        result.checked_at = datetime.now(timezone.utc).isoformat()
        result.check_mode = mode
        result.check_channels = channels
    result.policy_version = POLICY_VERSION
    result.pipeline = pipeline
    result.source_fields = {field: getattr(entry, field) for field in ("title", "authors", "year", "journal", "doi", "pmid", "volume", "issue", "pages", "article_number", "urls")}
    if entry.recovered_doi:
        result.source_fields["doi"] = ""
        result.parsed_doi = ""
    if not result.usable and pipeline == "verify":
        result.suggested_action = "不可用：当前证据未通过核查。保留原文供复核，不纳入可用引用。 " + result.suggested_action



def run_identifier_queries(
    entries: list[ReferenceEntry],
    client: ApiClient,
    pubmed_mode: str,
    openalex_mode: str,
    parallel_grace_seconds: float | None,
) -> tuple[
    dict[str, CanonicalRecord | None],
    dict[str, CanonicalRecord | None],
    dict[str, CanonicalRecord | None],
    dict[str, CanonicalRecord | None],
    dict[str, CanonicalRecord | None],
]:
    dois = [e.doi for e in entries if e.doi]
    pmids = [e.pmid for e in entries if e.pmid]
    doi_records: dict[str, CanonicalRecord | None] = {}
    pmid_records: dict[str, CanonicalRecord | None] = {}
    pubmed_doi_records: dict[str, CanonicalRecord | None] = {}
    openalex_doi_records: dict[str, CanonicalRecord | None] = {}
    openalex_pmid_records: dict[str, CanonicalRecord | None] = {}

    if pubmed_mode == "off" and openalex_mode == "off":
        return client.crossref_by_dois_parallel(dois), {}, {}, {}, {}

    stop_events = {
        "crossref": threading.Event(),
        "pubmed": threading.Event(),
        "openalex": threading.Event(),
    }
    done_event = threading.Event()
    results_lock = threading.Lock()
    finished: set[str] = set()

    def run_crossref() -> dict[str, CanonicalRecord | None]:
        return client.crossref_by_dois_parallel(dois, stop_events["crossref"])

    def run_pubmed() -> tuple[dict[str, CanonicalRecord | None], dict[str, CanonicalRecord | None]]:
        by_pmid = client.fetch_pubmed_pmids(pmids, stop_events["pubmed"])
        by_doi = client.pubmed_by_dois_parallel(dois, stop_events["pubmed"]) if pubmed_mode == "corroborate" else {}
        return by_pmid, by_doi

    def run_openalex() -> tuple[dict[str, CanonicalRecord | None], dict[str, CanonicalRecord | None]]:
        by_doi = client.openalex_by_dois_parallel(dois, stop_events["openalex"]) if openalex_mode == "corroborate" else {}
        by_pmid = client.openalex_by_pmids_parallel(pmids, stop_events["openalex"])
        return by_doi, by_pmid

    def run_named(name: str, fn: Any) -> None:
        nonlocal doi_records, pmid_records, pubmed_doi_records, openalex_doi_records, openalex_pmid_records
        try:
            value = fn()
            with results_lock:
                if name == "crossref":
                    doi_records = value
                elif name == "pubmed":
                    pmid_records, pubmed_doi_records = value
                elif name == "openalex":
                    openalex_doi_records, openalex_pmid_records = value
        except Exception as exc:
            if getattr(client, "metrics", None):
                client.metrics.record(name, "query_failure", 0, detail=type(exc).__name__)
        finally:
            with results_lock:
                finished.add(name)
            done_event.set()

    tasks: list[tuple[str, Any]] = [("crossref", run_crossref)]
    if pubmed_mode != "off":
        tasks.append(("pubmed", run_pubmed))
    if openalex_mode != "off":
        tasks.append(("openalex", run_openalex))
    threads = [threading.Thread(target=run_named, args=task, daemon=True) for task in tasks]
    for thread in threads:
        thread.start()

    # Crossref is the primary DOI authority. Fast and Balanced may shorten only
    # auxiliary corroboration; they must never cancel the primary lookup merely
    # because PubMed or OpenAlex happened to finish first.
    while True:
        with results_lock:
            if "crossref" in finished and (not pmids or pubmed_mode == "off" or "pubmed" in finished):
                break
        done_event.wait(timeout=0.05)
        done_event.clear()
    if parallel_grace_seconds is None:
        for thread in threads:
            thread.join()
        return doi_records, pmid_records, pubmed_doi_records, openalex_doi_records, openalex_pmid_records
    deadline = time.monotonic() + max(0.0, parallel_grace_seconds)
    while time.monotonic() < deadline:
        with results_lock:
            if len(finished) == len(tasks):
                break
        time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))

    with results_lock:
        unfinished = {name for name, _ in tasks} - finished
    for name in unfinished:
        stop_events[name].set()
    for thread in threads:
        thread.join(timeout=0)

    return doi_records, pmid_records, pubmed_doi_records, openalex_doi_records, openalex_pmid_records


def canonical_title_placeholder(title: str) -> bool:
    return normalize_text(title) in {"oup accepted manuscript", "accepted manuscript", "untitled", "article", "journal pre proof", "corrected proof"}


def first_round_classification(
    entry: ReferenceEntry,
    id_best: CanonicalRecord | None,
    majority_format: str,
    doi_output: str,
    include_pmid: bool,
) -> AuditResult:
    issues = []
    status = "unresolved"
    severity = "high"
    suggested = "Use DOI verification result; ask before AI-assisted per-paper search." if entry.doi else "Run Crossref title recovery to find a DOI candidate."
    issues.extend(entry.input_warnings)
    sim = title_similarity(entry.title, id_best.title) if id_best and entry.title_reliable else 0.0

    if id_best:
        if not entry.title_reliable:
            status = "verified_identifier_only"
            severity = "low"
            issues.append("Identifier resolved to a canonical record, but source-title matching was skipped because the input title is missing or unreliable.")
            suggested = "Use canonical DOI metadata; fix the worksheet/source title before judging title agreement or DOI hijacking."
        elif canonical_title_placeholder(id_best.title):
            status = "unresolved"
            severity = "high"
            issues.append("Provider returned a placeholder title; this is insufficient evidence of identifier hijacking.")
            suggested = "Check the same identifier in another enabled channel; retain original until verified."
        elif sim < 0.70:
            status = "identifier_hijacking"
            severity = "critical"
            issues.append(f"Supplied DOI/PMID resolves to a different title (similarity {sim:.2f}).")
            suggested = "Do not trust this identifier; report the DOI conflict and ask before deeper manual recovery."
        elif sim >= 0.86 and entry.year and id_best.year and year_agrees(entry.year, id_best.year) and entry.authors and id_best.authors and first_author_matches(entry.authors, id_best.authors):
            conflicts = metadata_differences(entry, id_best)
            conflicts.extend({"field": field, "before": getattr(entry, field), "after": "未取得对应证据", "source": id_best.source} for field in ("journal", "doi", "pmid") if getattr(entry, field) and not getattr(id_best, field))
            # Only an explicit provider abbreviation establishes journal equivalence.
            conflicts = [d for d in conflicts if not (d["field"] == "journal" and id_best.journal_abbreviation and normalize_text(entry.journal) == normalize_text(id_best.journal_abbreviation))]
            # A one-year difference requires date provenance; never silently fix it.
            conflicts = [d for d in conflicts if d["field"] != "title" or sim < 0.98]
            if conflicts:
                status = "partial_attribute_corruption"
                severity = "medium"
                issues.extend(f"Field conflict ({d['field']}): {d['before']} → {d['after']} [{d['source']}]" for d in conflicts)
                suggested = "Metadata differ; retain original and review the field-level evidence before repair."
            elif has_minor_fix(entry, id_best):
                status = "minor_fix"
                severity = "low"
                issues.extend(minor_fix_issues(entry, id_best))
                suggested = "Auto-fix formatting and identifier fields in the fixed copy."
            else:
                status = "verified"
                severity = "none"
                suggested = "Keep."
        else:
            status = "partial_attribute_corruption"
            severity = "medium"
            issues.append(f"Canonical record found, but metadata only partially match (title similarity {sim:.2f}).")
            if not entry.authors or not id_best.authors or not first_author_matches(entry.authors, id_best.authors):
                issues.append("First-author evidence is missing or conflicting.")
            if not entry.year or not id_best.year:
                issues.append("Publication-year evidence is missing.")
            if not year_agrees(entry.year, id_best.year):
                issues.append(f"Year differs: parsed {entry.year or 'missing'}, canonical {id_best.year or 'missing'}.")
            suggested = "Use title recovery and canonical metadata before rewriting."
    elif not entry.title_reliable and not entry.doi and not entry.pmid:
        status = "parser_error"
        severity = "high"
        issues.append("Input row has no reliable title or identifier; automatic lookup would be guesswork.")
        suggested = "Stop and rebuild the standard worksheet row from source text before querying."
    elif likely_placeholder(entry):
        status = "placeholder_generation"
        severity = "high"
        issues.append("Entry has placeholder-like metadata and no reliable identifier hit.")
        suggested = "Stop automatic repair unless title recovery finds a strong canonical match."
    else:
        issues.append("No supplied DOI/PMID resolved to a canonical record.")

    canonical = id_best if status in {"verified", "minor_fix", "partial_attribute_corruption", "verified_identifier_only"} else None
    fixed = build_fixed_reference(entry, canonical, status, majority_format, doi_output, include_pmid)
    return AuditResult(
        index=entry.index,
        status=status,
        severity=severity,
        citation_format=entry.citation_format,
        original=entry.original,
        parsed_title=entry.title,
        parsed_authors=entry.authors,
        parsed_journal=entry.journal,
        parsed_year=entry.year,
        parsed_doi=entry.doi,
        parsed_pmid=entry.pmid,
        parsed_title_reliable=entry.title_reliable,
        input_warnings=entry.input_warnings,
        canonical=canonical,
        identifier_record=id_best,
        title_similarity=sim,
        issues=issues,
        suggested_action=suggested,
        fixed_reference=fixed,
        evidence_links=evidence_links(canonical or id_best, entry),
        field_differences=metadata_differences(entry, id_best) if id_best else [],
    )


def has_minor_fix(entry: ReferenceEntry, record: CanonicalRecord) -> bool:
    if entry.doi and record.doi and clean_doi(entry.doi) != clean_doi(record.doi):
        return True
    if not entry.doi and record.doi:
        return True
    if not entry.pmid and record.pmid:
        return True
    if entry.journal and record.journal and normalize_text(entry.journal) != normalize_text(record.journal):
        return True
    if entry.year and record.year and entry.year != record.year[:4] and year_agrees(entry.year, record.year):
        return True
    return False


def minor_fix_issues(entry: ReferenceEntry, record: CanonicalRecord) -> list[str]:
    issues = []
    if not entry.doi and record.doi:
        issues.append("DOI is available from canonical metadata; report it and ask before adding if DOI output is optional.")
    if not entry.pmid and record.pmid:
        issues.append("PMID is available as secondary metadata.")
    if entry.journal and record.journal and normalize_text(entry.journal) != normalize_text(record.journal):
        issues.append(f"Journal name can be normalized to {record.journal}.")
    if entry.year and record.year and entry.year != record.year[:4] and year_agrees(entry.year, record.year):
        issues.append(f"Year appears to be online-first/issue drift: {entry.year} vs {record.year}.")
    return issues or ["Minor formatting or identifier normalization needed."]


def detect_shifted_identifiers(entries: list[ReferenceEntry], results: list[AuditResult]) -> None:
    by_index = {entry.index: entry for entry in entries}
    for result in results:
        if result.status != "identifier_hijacking" or not result.identifier_record:
            continue
        best_neighbor = None
        best_sim = 0.0
        for offset in (-2, -1, 1, 2):
            neighbor = by_index.get(result.index + offset)
            if not neighbor or not neighbor.title_reliable:
                continue
            sim = title_similarity(neighbor.title, result.identifier_record.title)
            if sim > best_sim:
                best_sim = sim
                best_neighbor = neighbor
        if best_neighbor and best_sim >= 0.86:
            result.status = "shifted_identifier"
            result.severity = "critical"
            result.shifted_to_index = best_neighbor.index
            result.issues.append(f"Identifier appears to belong to reference #{best_neighbor.index} (neighbor title similarity {best_sim:.2f}).")
            result.suggested_action = "Treat as DOI/PMID shift; fix only in the auto-fixed copy or after user confirmation."
            result.fixed_reference = result.fixed_reference.replace("identifier_hijacking", "shifted_identifier")


def recover_by_title(
    entries: list[ReferenceEntry],
    results: list[AuditResult],
    client: ApiClient,
    majority_format: str,
    pubmed_mode: str,
    openalex_mode: str,
    doi_output: str,
    include_pmid: bool,
) -> None:
    entry_map = {entry.index: entry for entry in entries}
    for result in results:
        if result.status not in TITLE_RECOVERY_STATUSES:
            continue
        entry = entry_map[result.index]
        if entry.doi:
            result.issues.append("Title recovery skipped because this entry already has a DOI; DOI verification result is reported instead.")
            continue
        if not entry.title_reliable:
            result.status = "parser_error"
            result.severity = "high"
            result.issues.append("Title recovery skipped because the source title failed input quality checks.")
            result.suggested_action = "Rebuild the worksheet row from source text before title-based lookup."
            result.fixed_reference = build_fixed_reference(entry, None, result.status, majority_format, doi_output, include_pmid)
            result.evidence_links = evidence_links(None, entry)
            continue
        failed_searches = []
        def search(provider: str, query: str) -> list[CanonicalRecord]:
            records = getattr(client, provider + "_search")(query, limit=3)
            key = normalize_text(query)[:240]
            failure = getattr(client, "search_failures", {}).get((provider, key))
            if failure:
                failed_searches.append(f"{provider}: {failure}")
            return list(records)
        candidates = search("crossref", entry.title or entry.original)
        best_probe = choose_best(entry, candidates) if candidates else None
        if (not best_probe or title_similarity(entry.title, best_probe.title) < 0.86) and openalex_mode != "off":
            candidates.extend(search("openalex", entry.title or entry.original))
            best_probe = choose_best(entry, candidates) if candidates else None
        if (not best_probe or title_similarity(entry.title, best_probe.title) < 0.86) and pubmed_mode != "off":
            exact_query = f'"{entry.title}"' if entry.title else entry.original
            candidates.extend(search("pubmed", exact_query))
        best = choose_best(entry, candidates)
        if best:
            best = merge_equivalent(best, candidates)
        sim = title_similarity(entry.title, best.title) if best else 0.0
        if best and sim >= 0.86 and year_agrees(entry.year, best.year):
            previous = result.status
            author_ok = not entry.authors or not best.authors or first_author_matches(entry.authors, best.authors)
            result.status = "minor_fix" if previous in {"unresolved", "placeholder_generation"} and not entry.doi and not entry.pmid and author_ok else "partial_attribute_corruption"
            result.severity = "low" if result.status == "minor_fix" else "medium"
            result.canonical = best
            result.title_similarity = sim
            result.issues.append(f"Recovered canonical record by title search (similarity {sim:.2f}).")
            if not author_ok:
                result.issues.append(f"Parsed first author differs from canonical first author ({best.authors[0]}).")
            if previous in {"identifier_hijacking", "shifted_identifier"}:
                result.issues.append("Supplied identifier remains wrong; fixed copy uses title-recovered metadata.")
            result.suggested_action = "Use recovered canonical metadata; no AI-assisted manual search needed unless user wants extra confirmation."
            # Apply the same identity and field checks to recovered records.
            checked = first_round_classification(entry, best, majority_format, doi_output, include_pmid)
            if checked.status not in {"verified", "minor_fix"}:
                result.status = checked.status
                result.severity = checked.severity
                result.issues.extend(checked.issues)
                result.suggested_action = checked.suggested_action
            result.field_differences = checked.field_differences
            result.fixed_reference = build_fixed_reference(entry, best, result.status, majority_format, doi_output, include_pmid)
            result.evidence_links = evidence_links(best, entry)
        elif best and sim >= 0.78:
            result.status = "partial_attribute_corruption"
            result.severity = "medium"
            result.canonical = best
            result.title_similarity = sim
            result.issues.append(f"Title recovery found a possible but low-confidence match (similarity {sim:.2f}).")
            result.suggested_action = "Do not auto-fix; ask user before manual AI-assisted recovery."
            result.evidence_links = evidence_links(best, entry)
        elif failed_searches:
            result.status = "unresolved"
            result.severity = "high"
            result.issues.append("Title recovery incomplete due to failed queries: " + "; ".join(failed_searches))
            result.suggested_action = "Not eligible for use. Retry failed queries before concluding that no matching record exists."
            result.fixed_reference = build_fixed_reference(entry, None, result.status, majority_format, doi_output, include_pmid)
            result.evidence_links = evidence_links(None, entry)
        elif result.status == "unresolved":
            result.status = "total_fabrication" if entry.title and entry.authors and entry.year else "unresolved"
            result.severity = "critical" if result.status == "total_fabrication" else "high"
            result.issues.append("Exact and relaxed title recovery found no high-confidence canonical record.")
            result.suggested_action = "Stop automatic recovery; ask user whether to delete, keep flagged, or run AI-assisted manual search."
            result.fixed_reference = build_fixed_reference(entry, None, result.status, majority_format, doi_output, include_pmid)
            result.evidence_links = evidence_links(None, entry)


def detect_possible_offset(results: list[AuditResult]) -> None:
    shifted = [r for r in results if r.status == "shifted_identifier" and r.shifted_to_index]
    if len(shifted) < 2:
        return
    offsets = Counter(r.shifted_to_index - r.index for r in shifted if r.shifted_to_index is not None)
    offset, count = offsets.most_common(1)[0]
    if count >= 2:
        for result in shifted:
            if result.shifted_to_index and result.shifted_to_index - result.index == offset:
                result.issues.append(f"Multiple shifted identifiers suggest a consistent offset of {offset:+d}.")


def majority_citation_format(entries: list[ReferenceEntry]) -> str:
    counts = Counter(e.citation_format for e in entries if e.citation_format != "free_text")
    return counts.most_common(1)[0][0] if counts else "apa"


def format_consistency(entries: list[ReferenceEntry]) -> dict[str, Any]:
    counts = Counter(e.citation_format for e in entries)
    majority = counts.most_common(1)[0][0] if counts else "unknown"
    mixed = len([fmt for fmt, count in counts.items() if count]) > 1
    return {
        "majority_format": majority,
        "mixed": mixed,
        "counts": dict(counts),
        "recommendation": f"Offer to standardize to {majority} after authenticity cleanup." if mixed else "No format unification needed.",
    }


def build_output_paths(input_path: Path, output_dir: Path, detail_output: Path | None = None) -> OutputPaths:
    fixed_name = "document.auto-fixed.md" if looks_like_document(input_path) else "references.auto-fixed.md"
    return OutputPaths(
        normalized_input=output_dir / "reference-normalized-input.md",
        normalized_records=output_dir / "reference-normalized-records.json",
        extracted_references=output_dir / "references.extracted.md",
        summary=output_dir / "reference-audit-summary.md",
        detail=detail_output or output_dir / "reference-audit-detail.md",
        html_report=output_dir / "reference-audit-report.html",
        fixed=output_dir / fixed_name,
        audit_json=output_dir / "reference-audit.json",
    )


def validate_output_paths(input_path: Path, paths: OutputPaths, index_path: Path | None = None, prior_path: Path | None = None) -> None:
    targets = [Path(value) for value in asdict(paths).values()]
    if index_path is not None:
        targets.append(index_path)
    protected = [input_path] + ([prior_path] if prior_path is not None else [])
    def same(a: Path, b: Path) -> bool:
        return a.resolve() == b.resolve() or (a.exists() and b.exists() and a.samefile(b))
    for i, target in enumerate(targets):
        if any(same(target, source) for source in protected):
            raise ValueError(f"Output path would overwrite an input artifact: {target}. Choose a separate output directory.")
        if any(same(target, other) for other in targets[:i]):
            raise ValueError(f"Output paths collide: {target}. Choose distinct report paths.")


def result_file_map(paths: OutputPaths) -> dict[str, str]:
    return {
        "summary_report": str(paths.summary),
        "detail_report": str(paths.detail),
        "html_report": str(paths.html_report),
        "fixed_copy": str(paths.fixed),
    }


def process_file_map(paths: OutputPaths, keep_process_json: bool) -> dict[str, str]:
    files = {
        "machine_records": str(paths.normalized_records),
        "normalized_input_table": str(paths.normalized_input),
        "extracted_references": str(paths.extracted_references),
    }
    if keep_process_json:
        files["audit_json"] = str(paths.audit_json)
    return files


def parse_process_cleanup(value: str, process_files: dict[str, str]) -> set[str]:
    if not value or value == "none":
        return set()
    if value == "all":
        return set(process_files)
    aliases = {
        "normalized_input": "normalized_input_table",
        "normalized_input_table": "normalized_input_table",
        "machine_records": "machine_records",
        "records": "machine_records",
        "extracted": "extracted_references",
        "extracted_references": "extracted_references",
        "audit_json": "audit_json",
        "json": "audit_json",
    }
    selected = set()
    unknown = []
    for raw_item in value.split(","):
        item = raw_item.strip()
        if not item:
            continue
        label = aliases.get(item)
        if label and label in process_files:
            selected.add(label)
        else:
            unknown.append(item)
    if unknown:
        valid = ", ".join(sorted(process_files))
        raise ValueError(f"Unknown process file label(s): {', '.join(unknown)}. Valid labels: all, none, {valid}")
    return selected


def cleanup_generated_process_files(
    process_files: dict[str, str],
    selected_labels: set[str],
    stale_paths: list[Path],
) -> tuple[dict[str, str], list[str]]:
    retained = dict(process_files)
    removed: list[str] = []
    for path in stale_paths:
        removed.append(f"{path} (not written this run; any existing file is retained)")
    for label in selected_labels:
        path = Path(process_files[label])
        if path.exists():
            path.unlink()
            removed.append(str(path))
        else:
            removed.append(f"{path} (already absent)")
        retained.pop(label, None)
    return retained, removed


def write_outputs(
    input_path: Path,
    output_dir: Path,
    entries: list[ReferenceEntry],
    results: list[AuditResult],
    emit_json: bool,
    detail_output: Path | None = None,
    keep_process_json: bool = False,
    cleanup_process_files: str = "",
    metrics: RuntimeMetrics | None = None,
    write_index: bool = False,
    report_language: str = "zh",
) -> dict[str, str]:
    paths = build_output_paths(input_path, output_dir, detail_output)
    validate_output_paths(input_path, paths, output_dir / "reference-index.json" if write_index else None)
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = format_consistency(entries)
    detail = render_detail(results, fmt)
    fixed = render_fixed_references(results)
    result_files = result_file_map(paths)
    process_files = process_file_map(paths, keep_process_json)
    cleanup_labels = parse_process_cleanup(cleanup_process_files, process_files) if cleanup_process_files else {"normalized_input_table", "extracted_references"}
    stale_paths = [] if keep_process_json else [paths.audit_json]

    paths.normalized_input.write_text(render_normalized_input(entries), encoding="utf-8")
    paths.normalized_records.write_text(json.dumps(render_normalized_records(entries), ensure_ascii=False, indent=2), encoding="utf-8")
    paths.extracted_references.write_text(render_extracted_references(entries), encoding="utf-8")
    paths.detail.write_text(detail, encoding="utf-8")
    write_html_report(
        paths.html_report,
        input_path=str(input_path),
        results=results,
        format_consistency=fmt,
        runtime=metrics,
        language=report_language,
    )
    paths.fixed.write_text(fixed, encoding="utf-8")

    retained_process_files, removed_process_files = cleanup_generated_process_files(process_files, cleanup_labels, stale_paths)
    summary = render_summary(
        results,
        fmt,
        paths.normalized_input,
        paths.normalized_records,
        paths.extracted_references,
        paths.detail,
        paths.fixed,
        result_files,
        retained_process_files,
        removed_process_files,
    )
    if metrics:
        request_text = ", ".join(f"{k}={v}" for k, v in sorted(metrics.requests.items())) or "none"
        status_text = ", ".join(f"{k}={v}" for k, v in sorted(metrics.statuses.items())) or "none"
        summary += (
            "\n## Runtime performance\n\n"
            f"- Mode: `{metrics.mode}`\n"
            f"- Elapsed: `{metrics.elapsed_seconds:.2f}s`\n"
            f"- Reused prior results: `{metrics.reused}`\n"
            f"- DOI recovered before verification: `{metrics.doi_recovered}`\n"
            f"- Requests: {request_text}\n"
            f"- Query states: {status_text}\n"
        )
        if metrics.phases:
            summary += "- Phase timing: " + ", ".join(f"{name}={seconds:.3f}s" for name, seconds in metrics.phases.items()) + "\n"
    paths.summary.write_text(summary, encoding="utf-8")

    structured = {
        "input": str(input_path),
        "format_consistency": fmt,
        "outputs": {
            "normalized_input": str(paths.normalized_input) if "normalized_input_table" in retained_process_files else "",
            "normalized_records": str(paths.normalized_records) if "machine_records" in retained_process_files else "",
            "extracted_references": str(paths.extracted_references) if "extracted_references" in retained_process_files else "",
            "summary": str(paths.summary),
            "detail": str(paths.detail),
            "html_report": str(paths.html_report),
            "fixed": str(paths.fixed),
            "json": str(paths.audit_json) if keep_process_json and "audit_json" in retained_process_files else "",
        },
        "file_cleanup": {
            "result_files": result_files,
            "retained_process_files": retained_process_files,
            "removed_process_files": removed_process_files,
        },
        "runtime": {
            "mode": metrics.mode,
            "elapsed_seconds": round(metrics.elapsed_seconds, 3),
            "requests": dict(metrics.requests),
            "statuses": dict(metrics.statuses),
            "events": [asdict(event) for event in metrics.events],
            "phases": metrics.phases,
        } if metrics else {},
        "results": [asdict(result) for result in results],
    }
    if write_index:
        index_path = output_dir / "reference-index.json"
        structured["outputs"]["index"] = str(index_path)
        write_json_atomic(index_path, audit_to_index(structured))
    if keep_process_json and "audit_json" in retained_process_files:
        paths.audit_json.write_text(json.dumps(structured, ensure_ascii=False, indent=2), encoding="utf-8")
    if emit_json:
        print(json.dumps(structured, ensure_ascii=False, indent=2))
    else:
        print(summary)
    return structured["outputs"]


def looks_like_document(input_path: Path) -> bool:
    try:
        text = input_path.read_text(encoding="utf-8")
    except Exception:
        return False
    return bool(REF_HEADING_RE.search(text)) and len(text.splitlines()) > 80


def render_normalized_records(entries: list[ReferenceEntry]) -> dict[str, Any]:
    return {
        "schema": MACHINE_RECORD_SCHEMA,
        "records": [
            {
                "index": entry.index,
                "input_source": entry.input_source,
                "source": {
                    "original_text": entry.original,
                    "title": entry.title,
                    "authors": entry.authors,
                    "year": entry.year,
                    "journal": entry.journal,
                    "volume": entry.volume,
                    "issue": entry.issue,
                    "pages": entry.pages,
                    "article_number": entry.article_number,
                    "identifiers": {
                        "doi": "" if entry.recovered_doi else entry.doi,
                        "pmid": entry.pmid,
                        "urls": entry.urls,
                    },
                    "source_lines": entry.source_lines,
                    "context": entry.context,
                },
                "quality": {
                    "title_reliable": entry.title_reliable,
                    "warnings": entry.input_warnings,
                    "recovered_doi": entry.recovered_doi,
                    "recovered_doi_source": entry.recovered_doi_source,
                },
            }
            for entry in entries
        ],
    }


def render_extracted_references(entries: list[ReferenceEntry]) -> str:
    lines = [
        "# Extracted References",
        "",
        "These are the source reference entries extracted before verification or formatting. Use this file to manually inspect what the parser treated as references.",
        "",
    ]
    for entry in sorted(entries, key=lambda item: item.index):
        lines.append(f"{entry.index}. {entry.original}")
        details = []
        if entry.source_lines:
            details.append("lines " + ", ".join(str(line) for line in entry.source_lines))
        if entry.occurrence_count > 1:
            details.append(f"occurrences {entry.occurrence_count}")
        if details:
            lines.append(f"   - Source: {'; '.join(details)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_normalized_input(entries: list[ReferenceEntry]) -> str:
    lines = [
        "# Reference Normalized Input",
        "",
        "This file is generated before remote lookup. It is the canonical worksheet-style input for the audit pipeline.",
        "",
        "Required source fields are explicit columns. Remote database results are written only to reports, not back into source fields.",
        "",
        "| # | Input source | Occurrences | Lines | Format | Source DOI | Source PMID | Source title | Title reliable | Source authors | Source journal | Source year | Volume | Issue | Pages/article | Input warnings | Context |",
        "|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            f"| {entry.index} | {entry.input_source} | {entry.occurrence_count} | {escape_pipe(', '.join(map(str, entry.source_lines)))} | {entry.citation_format} | {escape_pipe(entry.doi)} | {escape_pipe(entry.pmid)} | {escape_pipe(compact(entry.title, 80))} | {str(entry.title_reliable).lower()} | {escape_pipe(compact('; '.join(entry.authors), 70))} | {escape_pipe(compact(entry.journal, 50))} | {entry.year} | {escape_pipe(entry.volume)} | {escape_pipe(entry.issue)} | {escape_pipe(entry.pages or entry.article_number)} | {escape_pipe(compact('; '.join(entry.input_warnings), 100))} | {escape_pipe(compact(entry.context, 120))} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_summary(
    results: list[AuditResult],
    fmt: dict[str, Any],
    normalized_path: Path,
    normalized_records_path: Path,
    extracted_path: Path,
    detail_path: Path,
    fixed_path: Path,
    result_files: dict[str, str],
    retained_process_files: dict[str, str],
    removed_process_files: list[str],
) -> str:
    counts = Counter(r.status for r in results)
    severe = [r for r in results if r.status in SEVERE_STATUSES]
    problems = [r for r in results if r.status in PROBLEM_STATUSES]
    lines = [
        "# Reference Verification Summary",
        "",
        f"- Total references: {len(results)}",
        f"- Verified: {counts.get('verified', 0)}",
        f"- DOI/PMID verified only: {counts.get('verified_identifier_only', 0)}",
        f"- Auto-fixable/minor: {counts.get('minor_fix', 0)}",
        f"- Format-only normalized (not verified): {counts.get('formatted_only', 0)}",
        f"- Eligible for use after verification: {sum(r.usable for r in results)}",
        f"- Not eligible / not verified: {sum(not r.usable for r in results)}",
        f"- Partial/corrupted: {counts.get('partial_attribute_corruption', 0)}",
        f"- Parser/input errors: {counts.get('parser_error', 0)}",
        f"- Severe/high-risk: {len(severe)}",
        f"- Format: majority `{fmt['majority_format']}`, mixed={fmt['mixed']}",
        f"- Normalized records: {normalized_records_path}",
        f"- Normalized input: {normalized_path} ({'retained' if 'normalized_input_table' in retained_process_files else 'cleaned'})",
        f"- Extracted references: {extracted_path} ({'retained' if 'extracted_references' in retained_process_files else 'cleaned'})",
        f"- Detail report: {detail_path}",
        f"- Auto-fixed copy: {fixed_path}",
        "- DOI handling: preserve source DOI; append newly recovered DOI only with `--doi-output append`.",
        "",
        "## Output Files",
        "",
        "Result files kept:",
    ]
    lines.extend(f"- {label}: {path}" for label, path in result_files.items())
    lines.extend(["", "Process files retained for manual inspection:"])
    lines.extend(f"- {label}: {path}" for label, path in retained_process_files.items())
    lines.extend(["", "Process files cleaned or skipped before reporting:"])
    if removed_process_files:
        lines.extend(f"- {path}" for path in removed_process_files)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "Cleanup question for the user:",
            "- A. Delete all retained process files listed above.",
            "- B. Keep selected process files, such as `machine_records`, `normalized_input_table`, or `extracted_references`.",
            "- C. Keep all retained process files for now.",
            "",
        "## Problem Items",
        "| # | Severity | Status | Short item | Suggested action |",
        "|---|---|---|---|---|",
        ]
    )
    if not problems:
        lines.append("| - | - | - | No problematic items detected. | - |")
    for result in problems:
        label = result.parsed_title or result.original
        if result.parsed_authors or result.parsed_year:
            label = f"{result.parsed_authors[0] if result.parsed_authors else 'Unknown'} {result.parsed_year}: {label}"
        lines.append(f"| {result.index} | {result.severity} | {result.status} | {escape_pipe(compact(label, 80))} | {escape_pipe(compact(result.suggested_action, 100))} |")
    lines.extend(
        [
            "",
            "## Next User Decision",
            "- If severe items exist, ask whether to continue AI-assisted per-paper recovery, delete them, keep with warning notes, or stop with the report.",
            "- If DOI candidates were recovered for DOI-missing entries, ask whether the user wants to append DOI links or keep AMA citations without DOI.",
            f"- If formats are mixed, ask whether to standardize to `{fmt['majority_format']}` or another user-specified style.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_detail(results: list[AuditResult], fmt: dict[str, Any]) -> str:
    groups = defaultdict(list)
    for result in results:
        groups[result.status].append(result)
    order = [
        "formatted_only",
        "parser_error",
        "identifier_hijacking",
        "shifted_identifier",
        "total_fabrication",
        "placeholder_generation",
        "unresolved",
        "partial_attribute_corruption",
        "minor_fix",
        "minor_format_error",
        "verified_identifier_only",
        "verified",
    ]
    lines = [
        "# Reference Authenticity Detail Report",
        "",
        "## Directory",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status in order:
        if groups.get(status):
            lines.append(f"| {status} | {len(groups[status])} |")
    lines.extend(
        [
            "",
            "## Format Consistency",
            f"- Majority format: `{fmt['majority_format']}`",
            f"- Mixed formats: {fmt['mixed']}",
            f"- Counts: {json.dumps(fmt['counts'], ensure_ascii=False)}",
            f"- Recommendation: {fmt['recommendation']}",
        ]
    )
    for status in order:
        items = groups.get(status, [])
        if not items:
            continue
        lines.extend(["", f"## {status}"])
        for result in items:
            lines.extend(
                [
                    "",
                    f"### {result.index}. {compact(result.parsed_title or result.original, 120)}",
                    "",
                    f"- Severity: {result.severity}",
                    f"- Original: {result.original}",
                    f"- Parsed: title=`{result.parsed_title}`, authors=`{'; '.join(result.parsed_authors)}`, journal=`{result.parsed_journal}`, year=`{result.parsed_year}`, DOI=`{result.parsed_doi}`, PMID=`{result.parsed_pmid}`",
                    f"- Input quality: title_reliable={str(result.parsed_title_reliable).lower()}, warnings=" + ("; ".join(result.input_warnings) if result.input_warnings else "None"),
                    f"- DOI result: {doi_result_text(result)}",
                    f"- PubMed corroboration: {pubmed_result_text(result)}",
                    f"- OpenAlex corroboration: {openalex_result_text(result)}",
                    f"- Similarity: {result.title_similarity:.2f}",
                    "- Issues: " + ("; ".join(result.issues) if result.issues else "None"),
                    f"- Suggested action: {result.suggested_action}",
                    f"- Fixed-copy entry: {result.fixed_reference}",
                ]
            )
            if result.canonical:
                lines.append(f"- Canonical: {result.canonical.title} ({result.canonical.year}). {result.canonical.journal}.")
            if result.identifier_record and result.identifier_record is not result.canonical:
                lines.append(f"- Identifier resolved to: {result.identifier_record.title} ({result.identifier_record.year}).")
            if result.evidence_links:
                lines.append("- Evidence links: " + ", ".join(f"[link]({link})" for link in result.evidence_links))
    return "\n".join(lines).rstrip() + "\n"


def doi_result_text(result: AuditResult) -> str:
    canonical_doi = result.canonical.doi if result.canonical and result.canonical.doi else ""
    identifier_doi = result.identifier_record.doi if result.identifier_record and result.identifier_record.doi else ""
    best_doi = canonical_doi or identifier_doi
    if result.status == "shifted_identifier" and result.parsed_doi and identifier_doi:
        return f"shifted DOI `{result.parsed_doi}` resolves, but appears to belong to reference #{result.shifted_to_index}"
    if result.status == "identifier_hijacking" and result.parsed_doi and identifier_doi:
        return f"hijacked/conflicting DOI `{result.parsed_doi}` resolves to a different work"
    if result.parsed_doi and best_doi and clean_doi(result.parsed_doi) == clean_doi(best_doi) and result.status not in {"identifier_hijacking", "shifted_identifier"}:
        return f"verified DOI `{best_doi}`"
    if result.parsed_doi and best_doi and clean_doi(result.parsed_doi) != clean_doi(best_doi):
        return f"conflict: parsed DOI `{result.parsed_doi}`, canonical/identifier DOI `{best_doi}`"
    if result.parsed_doi and not best_doi:
        return f"parsed DOI `{result.parsed_doi}` did not resolve in automatic checks"
    if not result.parsed_doi and best_doi:
        return f"DOI available for optional addition: `{best_doi}`"
    return "no DOI found"


def pubmed_result_text(result: AuditResult) -> str:
    record = result.canonical or result.identifier_record
    if record and record.pmid and record.doi:
        if record.pubmed_corroborated:
            return f"matched DOI-backed PubMed record PMID `{record.pmid}`"
        return f"PMID available from canonical DOI-backed record: `{record.pmid}`"
    if result.parsed_pmid:
        return f"parsed PMID `{result.parsed_pmid}` was not corroborated against a DOI-backed record"
    if result.parsed_doi:
        return "no DOI-backed PubMed corroboration returned within this run"
    return "not requested for DOI-missing record"


def openalex_result_text(result: AuditResult) -> str:
    record = result.canonical or result.identifier_record
    if record and record.openalex_corroborated and (record.doi or record.pmid):
        identifiers = []
        if record.doi:
            identifiers.append(f"DOI `{record.doi}`")
        if record.pmid:
            identifiers.append(f"PMID `{record.pmid}`")
        return "matched OpenAlex external-id record with " + ", ".join(identifiers)
    if record and record.source == "OpenAlex":
        return "canonical candidate came from OpenAlex"
    if result.parsed_doi or result.parsed_pmid:
        return "no OpenAlex corroboration returned within this run"
    return "not requested for DOI/PMID-missing record"


def render_fixed_references(results: list[AuditResult]) -> str:
    lines = ["# Auto-Fixed References", "", "<!-- Generated by biomedical-reference-verifier. Review severe items before reuse. -->", ""]
    for result in sorted(results, key=lambda r: r.index):
        lines.append(result.fixed_reference)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-verify or format biomedical references.")
    parser.add_argument("--report-language", choices=["zh", "en"], default="zh", help="HTML report language (default: zh)")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("input", help="Text, Markdown, or manuscript file containing references")
    parser.add_argument("--output-dir", help="Directory for summary/detail/fixed/json outputs. Defaults to a temp directory.")
    parser.add_argument("--output", help="Compatibility option: write detailed report to this path")
    parser.add_argument("--references-heading", help="Custom heading where references begin")
    parser.add_argument("--input-mode", choices=["auto", "records", "worksheet", "references", "doi-context"], default="auto", help="How to build normalized input records; records reads JSON/JSONL schema biomedical-reference-verifier.records.v1")
    parser.add_argument("--pipeline", choices=["verify", "format-only"], default="verify", help="verify runs external authenticity checks; format-only only normalizes citation style from source fields")
    parser.add_argument("--mode", choices=["fast", "balanced", "strict"], default="balanced", help="Execution mode: fast stops after primary evidence, balanced allows a short corroboration grace period, strict waits for all enabled evidence lines")
    parser.add_argument("--reuse-results", help="Explicit prior reference-audit.json to reuse for unchanged references; no hidden cache is created")
    parser.add_argument("--citation-style", choices=["source-majority", "ama", "apa", "gbt7714", "vancouver"], default="source-majority", help="Style for the auto-fixed reference copy")
    parser.add_argument("--doi-output", choices=["report-only", "append"], default="report-only", help="Whether recovered/verified DOI should stay in reports only or be appended to the fixed citation copy")
    parser.add_argument("--include-pmid", action="store_true", help="Append PMID to fixed citations only when the record also has a DOI")
    parser.add_argument("--pubmed-mode", choices=["off", "ids", "corroborate"], default="corroborate", help="PubMed corroboration mode; corroborate starts PubMed and Crossref together, while off runs Crossref only")
    parser.add_argument("--openalex-mode", choices=["off", "ids", "corroborate"], default="corroborate", help="OpenAlex corroboration mode; default is the third concurrent evidence line after Crossref and PubMed")
    parser.add_argument("--parallel-grace-seconds", type=float, default=None, help="Override mode grace period; defaults are fast=0, balanced=2.5, strict=wait for enabled evidence lines")
    parser.add_argument("--crossref-workers", type=int, default=CROSSREF_POLITE_CONCURRENCY, help="Concurrent Crossref DOI workers; capped to Crossref polite-pool concurrency")
    parser.add_argument("--pubmed-workers", type=int, default=0, help="Concurrent PubMed DOI corroboration workers; default is 3 without NCBI_API_KEY, 10 with NCBI_API_KEY")
    parser.add_argument("--openalex-workers", type=int, default=OPENALEX_DEFAULT_CONCURRENCY, help="Concurrent OpenAlex DOI/PMID corroboration workers")
    parser.add_argument("--request-timeout", type=int, default=8, help="Per-request network timeout in seconds")
    parser.add_argument("--ncbi-api-key", default=os.environ.get("NCBI_API_KEY") or "", help="Optional NCBI API key; raises PubMed E-utilities rate from 3 to 10 requests/second")
    parser.add_argument("--openalex-api-key", default=os.environ.get("OPENALEX_API_KEY") or "", help="Optional OpenAlex API key")
    parser.add_argument("--max-records", type=int, default=0, help="Limit records for testing")
    parser.add_argument("--email", default="", help="Optional contact email sent to bibliographic providers only when explicitly supplied")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of the chat summary")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Compatibility option for older usage")
    parser.add_argument("--keep-process-json", action="store_true", help="Keep reference-audit.json for debugging or continuation; default cleans/skips this process file")
    parser.add_argument("--write-index", action="store_true", help="Write optional reusable reference-index.json; disabled by default")
    parser.add_argument("--cleanup-process-files", default="", help="Delete generated process files after writing results. Use all, none, or comma labels such as machine_records,normalized_input,extracted_references,audit_json")
    args = parser.parse_args()

    metrics = RuntimeMetrics(mode=args.mode)
    phase_started = time.monotonic()
    input_path = Path(args.input)
    text = input_path.read_text(encoding="utf-8")
    try:
        entries = build_entries(text, args.references_heading, args.input_mode)
        validate_entry_indices(entries)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.max_records:
        entries = entries[: args.max_records]
    if not entries:
        print("No reference records found. Check the input file, --input-mode, or --references-heading.", file=sys.stderr)
        return 2
    metrics.finish_phase("parse", phase_started)
    output_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="reference-audit-"))
    detail_output = Path(args.output) if args.output else None
    if detail_output and not args.output_dir:
        output_dir = detail_output.parent

    try:
        validate_output_paths(input_path, build_output_paths(input_path, output_dir, detail_output),
                              output_dir / "reference-index.json" if args.write_index else None,
                              Path(args.reuse_results) if args.reuse_results else None)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    phase_started = time.monotonic()
    reuse_warnings: list[str] = []
    enabled_channels = ["Crossref"] if args.pipeline == "verify" else []
    if args.pipeline == "verify" and args.mode != "fast":
        enabled_channels.extend(name for name, setting in (("PubMed", args.pubmed_mode), ("OpenAlex", args.openalex_mode)) if setting != "off")
    try:
        prior_rows = load_prior_results(args.reuse_results, reuse_warnings, pipeline=args.pipeline, mode=args.mode, channels=enabled_channels, policy_version=POLICY_VERSION) if args.reuse_results else {}
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for warning in reuse_warnings:
        print(f"Prior artifact warning: {warning}", file=sys.stderr)
    metrics.finish_phase("prior_artifact", phase_started)
    reused_by_index: dict[int, AuditResult] = {}
    pending_entries = []
    for entry in entries:
        prior = prior_result_for_entry(prior_rows, entry)
        if prior:
            try:
                reused = audit_result_from_dict(prior)
                reused.index = entry.index
                reused.original = entry.original
                output_style = majority_citation_format(entries) if args.citation_style == "source-majority" else args.citation_style
                if args.pipeline == "format-only":
                    reused = format_only_results([entry], output_style, args.doi_output, args.include_pmid)[0]
                else:
                    reused.fixed_reference = build_fixed_reference(entry, reused.canonical, reused.status, output_style, args.doi_output, args.include_pmid)
                reused_by_index[entry.index] = reused
                metrics.reused += 1
                continue
            except (TypeError, ValueError):
                pass
        pending_entries.append(entry)
    if args.pipeline == "format-only":
        fresh_results = format_only_results(
            pending_entries,
            citation_style=args.citation_style,
            doi_output=args.doi_output,
            include_pmid=args.include_pmid,
        )
    else:
        client = ApiClient(
            email=args.email,
            timeout=args.request_timeout,
            crossref_workers=args.crossref_workers,
            pubmed_workers=args.pubmed_workers,
            openalex_workers=args.openalex_workers,
            ncbi_api_key=args.ncbi_api_key,
            openalex_api_key=args.openalex_api_key,
            metrics=metrics,
        )
        phase_started = time.monotonic()
        recover_missing_dois_early(pending_entries, client, metrics, args.mode, args.pubmed_mode, args.openalex_mode)
        metrics.finish_phase("doi_recovery", phase_started)
        effective_pubmed_mode = "off" if args.mode == "fast" else args.pubmed_mode
        effective_openalex_mode = "off" if args.mode == "fast" else args.openalex_mode
        phase_started = time.monotonic()
        fresh_results = classify_entries(
            pending_entries,
            client,
            pubmed_mode=effective_pubmed_mode,
            openalex_mode=effective_openalex_mode,
            parallel_grace_seconds=grace_for_mode(args.mode, args.parallel_grace_seconds),
            citation_style=args.citation_style,
            doi_output=args.doi_output,
            include_pmid=args.include_pmid,
        )
        metrics.finish_phase("verification", phase_started)
    fresh_by_index = {result.index: result for result in fresh_results}
    results = [reused_by_index.get(entry.index) or fresh_by_index[entry.index] for entry in entries]
    for entry, result in zip(entries, results):
        describe_result(result, entry, args.pipeline, args.mode, enabled_channels)
    try:
        write_outputs(
            input_path,
            output_dir,
            entries,
            results,
            emit_json=args.json or args.format == "json",
            detail_output=detail_output,
            keep_process_json=args.keep_process_json,
            cleanup_process_files=args.cleanup_process_files,
            metrics=metrics,
            write_index=args.write_index,
            report_language=args.report_language,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
