#!/usr/bin/env python3
"""ISBN parsing, normalization, and validation helpers."""

from __future__ import annotations

import re
from typing import Iterable, List, Optional

ISBN_TOKEN_RE = re.compile(r"(?:97[89][\d\-\s]{10,20}|[\dXx][\d\-\s]{8,20})")


def _clean_token(token: str) -> str:
    return re.sub(r"[^0-9Xx]", "", token).upper()


def is_valid_isbn10(isbn10: str) -> bool:
    if not re.fullmatch(r"\d{9}[\dX]", isbn10):
        return False
    total = 0
    for idx, char in enumerate(isbn10):
        value = 10 if char == "X" else int(char)
        total += value * (10 - idx)
    return total % 11 == 0


def is_valid_isbn13(isbn13: str) -> bool:
    if not re.fullmatch(r"\d{13}", isbn13):
        return False
    total = 0
    for idx, ch in enumerate(isbn13[:12]):
        factor = 1 if idx % 2 == 0 else 3
        total += int(ch) * factor
    checksum = (10 - (total % 10)) % 10
    return checksum == int(isbn13[-1])


def isbn10_to_isbn13(isbn10: str) -> Optional[str]:
    if not is_valid_isbn10(isbn10):
        return None
    core = "978" + isbn10[:9]
    total = 0
    for idx, ch in enumerate(core):
        total += int(ch) * (1 if idx % 2 == 0 else 3)
    check = (10 - (total % 10)) % 10
    isbn13 = core + str(check)
    return isbn13 if is_valid_isbn13(isbn13) else None


def isbn13_to_isbn10(isbn13: str) -> Optional[str]:
    if not (is_valid_isbn13(isbn13) and isbn13.startswith("978")):
        return None
    core = isbn13[3:12]
    total = 0
    for idx, ch in enumerate(core):
        total += int(ch) * (10 - idx)
    remainder = 11 - (total % 11)
    if remainder == 10:
        check = "X"
    elif remainder == 11:
        check = "0"
    else:
        check = str(remainder)
    isbn10 = core + check
    return isbn10 if is_valid_isbn10(isbn10) else None


def normalize_isbn(value: str) -> Optional[str]:
    """Normalize a token to canonical ISBN-13 when possible."""
    token = _clean_token(value)
    if len(token) == 13 and is_valid_isbn13(token):
        return token
    if len(token) == 10 and is_valid_isbn10(token):
        return isbn10_to_isbn13(token)
    if len(token) == 13 and token.startswith("979") and is_valid_isbn13(token):
        return token
    return None


def extract_isbn_candidates_from_text(text: str) -> List[str]:
    """Extract and normalize valid ISBN-13 candidates from free text."""
    raw_tokens = ISBN_TOKEN_RE.findall(text or "")
    found: List[str] = []
    seen = set()
    for token in raw_tokens:
        normalized = normalize_isbn(token)
        if normalized and normalized not in seen:
            seen.add(normalized)
            found.append(normalized)
    return found


def to_unique_isbn13(tokens: Iterable[str]) -> List[str]:
    """Normalize arbitrary tokens to unique valid ISBN-13 values."""
    out: List[str] = []
    seen = set()
    for token in tokens:
        norm = normalize_isbn(token)
        if norm and norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out
