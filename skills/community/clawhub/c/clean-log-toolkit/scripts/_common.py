"""
Shared helpers for clean-log-toolkit.

Pure standard library. No third-party imports.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    """Reject paths containing shell metacharacters."""
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def iter_lines(path: Path, encoding: str = "utf-8") -> Iterator[str]:
    """Stream lines from a text file, falling back through several encodings."""
    for enc in (encoding, "utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open("r", encoding=enc, errors="replace") as f:
                for line in f:
                    yield line.rstrip("\n").rstrip("\r")
            return
        except UnicodeDecodeError:
            continue


# ---- Timestamp parsing ----------------------------------------------------

# Common formats found in log files (ordered: tries from most specific to least).
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f%z",        # ISO 8601 with TZ + microseconds
    "%Y-%m-%dT%H:%M:%S%z",            # ISO 8601 with TZ
    "%Y-%m-%dT%H:%M:%S.%fZ",         # ISO 8601 UTC Zulu + microseconds
    "%Y-%m-%dT%H:%M:%SZ",             # ISO 8601 UTC Zulu
    "%Y-%m-%dT%H:%M:%S.%f",           # ISO 8601 no TZ + microseconds
    "%Y-%m-%dT%H:%M:%S",              # ISO 8601 no TZ
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",                 # date + minute precision
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%d/%b/%Y:%H:%M:%S %z",          # Apache common log
    "%Y-%m-%d",                       # date only (useful for --since/--until)
    "%Y/%m/%d",                       # date only with slashes
    "%d/%m/%Y",                       # European date format
    "%b %d %H:%M:%S",                 # syslog (no year)
)


def parse_timestamp(s: str) -> Optional[datetime]:
    s = s.strip().strip("[]")
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


# Pre-compiled regex that grabs the FIRST timestamp-shaped token in a line
TIMESTAMP_PROBE_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?)"
    r"|"
    r"(\d{2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})"
    r"|"
    r"([A-Z][a-z]{2} {1,2}\d{1,2} \d{2}:\d{2}:\d{2})"
)


def extract_timestamp(line: str) -> Optional[datetime]:
    """Best-effort find-and-parse of the first timestamp-shaped token in a line."""
    m = TIMESTAMP_PROBE_RE.search(line)
    if not m:
        return None
    raw = next((g for g in m.groups() if g), None)
    if raw is None:
        return None
    return parse_timestamp(raw)


# ---- Level detection ------------------------------------------------------

LEVEL_RE = re.compile(
    r"\b(TRACE|DEBUG|INFO|NOTICE|WARN(?:ING)?|ERROR|ERR|FATAL|CRITICAL|CRIT|EMERG(?:ENCY)?)\b",
    re.IGNORECASE,
)

LEVEL_CANONICAL = {
    "TRACE": "TRACE", "DEBUG": "DEBUG",
    "INFO": "INFO", "NOTICE": "NOTICE",
    "WARN": "WARN", "WARNING": "WARN",
    "ERROR": "ERROR", "ERR": "ERROR",
    "FATAL": "FATAL", "CRITICAL": "FATAL", "CRIT": "FATAL",
    "EMERG": "FATAL", "EMERGENCY": "FATAL",
}


def extract_level(line: str) -> Optional[str]:
    m = LEVEL_RE.search(line)
    if not m:
        return None
    return LEVEL_CANONICAL.get(m.group(1).upper())
