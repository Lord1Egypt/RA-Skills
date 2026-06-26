#!/usr/bin/env python3
"""Shared redaction helpers for Artifact Redactor."""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

TEXT_SUFFIXES = {
    ".cfg",
    ".conf",
    ".csv",
    ".env",
    ".html",
    ".ini",
    ".json",
    ".log",
    ".markdown",
    ".md",
    ".py",
    ".sh",
    ".sql",
    ".text",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

URL_PATTERN = re.compile(r"https?://[^\s<>()\"']+")
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\w)\+?[\d][\d().\s-]{8,}\d(?!\w)")
UNIX_PATH_PATTERN = re.compile(
    r"(?:(?<=\s)|(?<=^)|(?<=[\"'`]))"
    r"(?:"
    r"~\/[^\s\"'`]+"
    r"|\/(?:Users|home|var|etc|tmp|private|opt|workspace|mnt|srv|run|data)\/[^\s\"'`]+"
    r"|\/(?:[^/\s\"'`]+\/)+[^/\s\"'`]+\.[A-Za-z0-9._-]+"
    r")"
)
WINDOWS_PATH_PATTERN = re.compile(r"(?:(?<=\s)|(?<=^)|(?<=[\"'`]))[A-Za-z]:\\[^\s\"'`]+")
UNC_PATH_PATTERN = re.compile(r"(?:(?<=\s)|(?<=^)|(?<=[\"'`]))\\\\[^\s\"'`\\]+\\[^\s\"'`\\]+(?:\\[^\s\"'`\\]+)+")
FILE_URL_PATTERN = re.compile(r"file://[^\s\"'`]+", re.IGNORECASE)

SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.IGNORECASE),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{10,}", re.IGNORECASE),
]

PATH_PATTERNS = [FILE_URL_PATTERN, UNIX_PATH_PATTERN, WINDOWS_PATH_PATTERN, UNC_PATH_PATTERN]


def iter_candidate_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return [path for path in sorted(root.rglob("*")) if path.is_file()]


def is_text_candidate(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    return path.name.lower() in {"license", "readme", ".gitignore"}


def read_text_if_supported(path: Path) -> Optional[str]:
    if not is_text_candidate(path):
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def is_private_host(host: str) -> bool:
    normalized = (host or "").strip().lower()
    if not normalized:
        return True
    if normalized == "localhost" or normalized.endswith((".local", ".internal", ".corp", ".lan")):
        return True
    if normalized in {"0.0.0.0", "127.0.0.1"}:
        return True
    if "." not in normalized and not any(char.isdigit() for char in normalized):
        return True
    try:
        ip = ipaddress.ip_address(normalized)
    except ValueError:
        return False
    return bool(ip.is_private or ip.is_loopback or ip.is_link_local)


def sanitize_url(url: str) -> str:
    value = url.strip()
    if not value:
        return value
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[redacted-private-url]"
    if parts.scheme not in {"http", "https"}:
        return "[redacted-private-url]"
    if parts.username or parts.password:
        return "[redacted-private-url]"
    if is_private_host(parts.hostname or ""):
        return "[redacted-private-url]"
    netloc = parts.hostname or ""
    if parts.port:
        netloc = f"{netloc}:{parts.port}"
    return urlunsplit((parts.scheme, netloc, parts.path, "", ""))


def sanitize_snippet(text: str) -> str:
    redacted, _ = redact_text(text)
    collapsed = " ".join(redacted.strip().split())
    return collapsed[:160]


def _apply_regex_replacement(pattern: re.Pattern[str], text: str, replacement: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return replacement

    return pattern.sub(replace, text), count


def _replace_urls(text: str) -> tuple[str, dict[str, int]]:
    counters = {"private_url": 0, "public_url_query": 0}

    def replace(match: re.Match[str]) -> str:
        raw = match.group(0)
        sanitized = sanitize_url(raw)
        if sanitized == "[redacted-private-url]":
            counters["private_url"] += 1
            return sanitized
        if sanitized != raw:
            counters["public_url_query"] += 1
        return sanitized

    return URL_PATTERN.sub(replace, text), counters


def _replace_phones(text: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        raw = match.group(0)
        digits = sum(char.isdigit() for char in raw)
        if digits < 10:
            return raw
        count += 1
        return "[redacted-phone]"

    return PHONE_PATTERN.sub(replace, text), count


def redact_text(text: str) -> tuple[str, dict[str, int]]:
    output = text
    counts = {
        "private_url": 0,
        "public_url_query": 0,
        "private_path": 0,
        "secret_like": 0,
        "email": 0,
        "phone": 0,
    }

    output, url_counts = _replace_urls(output)
    counts["private_url"] += url_counts["private_url"]
    counts["public_url_query"] += url_counts["public_url_query"]

    for pattern in PATH_PATTERNS:
        output, path_hits = _apply_regex_replacement(pattern, output, "[redacted-private-path]")
        counts["private_path"] += path_hits

    for pattern in SECRET_PATTERNS:
        output, secret_hits = _apply_regex_replacement(pattern, output, "[redacted-secret]")
        counts["secret_like"] += secret_hits

    output, email_hits = _apply_regex_replacement(EMAIL_PATTERN, output, "[redacted-email]")
    counts["email"] += email_hits

    output, phone_hits = _replace_phones(output)
    counts["phone"] += phone_hits
    return output, counts


def find_line_findings(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for index, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        if any(pattern.search(raw_line) for pattern in SECRET_PATTERNS):
            findings.append({"line": index, "code": "secret-like", "severity": "error", "snippet": sanitize_snippet(raw_line)})

        for match in URL_PATTERN.finditer(raw_line):
            raw_url = match.group(0)
            sanitized = sanitize_url(raw_url)
            if sanitized == "[redacted-private-url]":
                findings.append({"line": index, "code": "private-url", "severity": "error", "snippet": sanitize_snippet(raw_line)})
            elif sanitized != raw_url:
                findings.append({"line": index, "code": "public-url-query", "severity": "warning", "snippet": sanitize_snippet(raw_line)})

        if any(pattern.search(raw_line) for pattern in PATH_PATTERNS):
            findings.append({"line": index, "code": "private-path", "severity": "error", "snippet": sanitize_snippet(raw_line)})

        if EMAIL_PATTERN.search(raw_line):
            findings.append({"line": index, "code": "email", "severity": "warning", "snippet": sanitize_snippet(raw_line)})

        phone_match = PHONE_PATTERN.search(raw_line)
        if phone_match and sum(char.isdigit() for char in phone_match.group(0)) >= 10:
            findings.append({"line": index, "code": "phone", "severity": "warning", "snippet": sanitize_snippet(raw_line)})

    return findings
