from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .constants import CSV_ROLE_DEFAULTS
from .shared import normalize_author_key, normalize_space, normalized_key, parse_float, parse_rating, strip_html


def resolve_csv_headers(headers: list[str], overrides: dict[str, str] | None = None) -> dict[str, str]:
    overrides = overrides or {}
    mapping: dict[str, str] = {}
    header_lookup = {header.casefold(): header for header in headers}
    for role, names in CSV_ROLE_DEFAULTS.items():
        if role in overrides:
            override_header = str(overrides[role]).strip()
            existing = header_lookup.get(override_header.casefold())
            if not existing:
                detected = ", ".join(headers)
                raise ValueError(
                    f"CSV override for {role} references missing header '{override_header}'. "
                    f"Detected headers: {detected}."
                )
            mapping[role] = existing
            continue
        for candidate in names:
            existing = header_lookup.get(candidate.casefold())
            if existing:
                mapping[role] = existing
                break
    required_roles = ("title", "author", "shelf")
    missing = [role for role in required_roles if role not in mapping]
    if missing:
        detected = ", ".join(headers)
        wanted = " ".join(f"--csv-column {role}=..." for role in required_roles)
        raise ValueError(
            "Could not identify the Goodreads export columns for title, author, and shelf. "
            f"Detected headers: {detected}. Use {wanted}"
        )
    return mapping


def canonicalize_bookshelves(raw_shelf: str, raw_bookshelves: str) -> tuple[str, list[str]]:
    values = [normalize_space(raw_shelf)]
    values.extend(normalize_space(item) for item in str(raw_bookshelves or "").split(","))
    shelves: list[str] = []
    for value in values:
        if value and value not in shelves:
            shelves.append(value)
    exclusive = shelves[0] if shelves else ""
    return exclusive, shelves


def effective_shelf(entry: dict[str, Any]) -> str:
    exclusive = normalize_space(str(entry.get("exclusiveShelf") or "")).casefold()
    shelves = [normalize_space(str(item)).casefold() for item in entry.get("bookshelves") or []]
    if "read" in shelves or exclusive == "read":
        return "read"
    if "currently-reading" in shelves or exclusive == "currently-reading":
        return "currently-reading"
    if "to-read" in shelves or exclusive == "to-read":
        return "to-read"
    return ""


def load_goodreads_csv(export_path: Path, csv_columns: dict[str, str] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with export_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        mapping = resolve_csv_headers(headers, csv_columns)
        rows: list[dict[str, Any]] = []
        for raw in reader:
            title = normalize_space(raw.get(mapping["title"]) or "")
            author = normalize_space(raw.get(mapping["author"]) or "")
            average_rating = parse_float(raw.get(mapping.get("average_rating", "")))
            exclusive, shelves = canonicalize_bookshelves(
                raw.get(mapping["shelf"]) or "",
                raw.get(mapping.get("bookshelves", "")) or "",
            )
            row = {
                "bookId": normalize_space(raw.get(mapping.get("book_id", "")) or ""),
                "title": title,
                "author": author,
                "exclusiveShelf": exclusive,
                "bookshelves": shelves,
                "myRating": parse_rating(raw.get(mapping.get("rating", ""))),
                "myReview": normalize_space(strip_html(raw.get(mapping.get("review", "")) or "")),
                "averageRating": average_rating,
                "averageRatingSource": "csv_average_rating" if average_rating is not None else None,
                "dateRead": normalize_space(raw.get(mapping.get("date_read", "")) or ""),
                "dateAdded": normalize_space(raw.get(mapping.get("date_added", "")) or ""),
                "isbn": normalize_space(raw.get(mapping.get("isbn", "")) or ""),
                "isbn13": normalize_space(raw.get(mapping.get("isbn13", "")) or ""),
            }
            rows.append(row)
    stats = {
        "headers": headers,
        "columnMap": mapping,
        "totalRows": len(rows),
        "ratedOrReviewedRows": sum(1 for row in rows if row["myRating"] > 0 or row["myReview"]),
        "missingAuthorRows": sum(1 for row in rows if row["title"] and not row["author"]),
    }
    return rows, stats


def strong_personal_matches(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    candidate_isbns = {normalize_space(str(candidate.get("isbn") or "")), normalize_space(str(candidate.get("isbn13") or ""))}
    candidate_isbns.discard("")
    normalized_title = normalized_key(candidate.get("title") or "", ascii_only=True)
    normalized_author = normalize_author_key(candidate.get("author") or "", ascii_only=True)
    for row in rows:
        row_title = normalized_key(str(row.get("title") or ""), ascii_only=True)
        row_author = normalize_author_key(str(row.get("author") or ""), ascii_only=True)
        row_isbns = {normalize_space(str(row.get("isbn") or "")), normalize_space(str(row.get("isbn13") or ""))}
        row_isbns.discard("")
        if candidate_isbns and row_isbns and candidate_isbns & row_isbns:
            matches.append(row)
            continue
        if row_title and row_author and row_title == normalized_title and row_author == normalized_author:
            matches.append(row)
    return matches


def classify_personal_match(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    matches = strong_personal_matches(candidate, rows)
    if not matches:
        return {"matched": False, "effectiveShelf": "", "matches": []}
    effective_states = {state for state in (effective_shelf(item) for item in matches) if state in {"read", "currently-reading", "to-read"}}
    if len(effective_states) > 1:
        return {"matched": True, "ambiguous": True, "effectiveShelf": "", "matches": matches}
    state = next(iter(effective_states), "")
    return {"matched": True, "ambiguous": False, "effectiveShelf": state, "matches": matches}
