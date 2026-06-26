"""
Shared helpers for openclaw-csv-toolkit.

Pure standard library. No third-party imports.

Provides:
  - safe_path()        path validation against shell-metachar injection
  - sniff_dialect()    auto-detect delimiter, quote char, line terminator
  - sniff_encoding()   pick utf-8 / utf-8-sig / latin-1 by trial decode
  - open_table()       context-managed reader for csv/tsv/jsonl input
  - infer_column_type() classify a column's values into the most specific
                       type that fits (int, float, bool, date, datetime, string)
  - human_bytes()      pretty file-size formatter
"""

from __future__ import annotations

import csv
import json
import re
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    """Reject paths containing shell metacharacters."""
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def sniff_encoding(path: Path, byte_budget: int = 65536) -> str:
    """Pick a workable encoding by trial decode of the first chunk."""
    raw = path.read_bytes()[:byte_budget]
    # BOM first
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return "utf-16"
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return "latin-1"


def sniff_dialect(path: Path, encoding: str, byte_budget: int = 16384) -> Tuple[str, csv.Dialect]:
    """Return ('csv'|'tsv'|'jsonl', dialect-like object).

    Uses csv.Sniffer for CSV/TSV. JSON Lines is detected by checking the
    first non-empty line for a leading '{'.
    """
    with path.open("r", encoding=encoding, newline="", errors="replace") as fh:
        sample = fh.read(byte_budget)

    # JSON Lines?
    for line in sample.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("{") and line.endswith("}"):
            return "jsonl", csv.excel
        break

    # CSV / TSV
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        # Fall back: prefer tab if any line has more tabs than commas.
        first_line = sample.splitlines()[0] if sample else ""
        if first_line.count("\t") > first_line.count(","):
            dialect = csv.excel_tab
        else:
            dialect = csv.excel
    kind = "tsv" if getattr(dialect, "delimiter", ",") == "\t" else "csv"
    return kind, dialect


@contextmanager
def open_table(path: Path, encoding: Optional[str] = None):
    """Yield (kind, headers, row_iter) for csv/tsv/jsonl files.

    rows are always emitted as `dict[str, str]` with stringified values.
    Caller closes the underlying file via the contextmanager.
    """
    enc = encoding or sniff_encoding(path)
    kind, dialect = sniff_dialect(path, enc)

    fh = path.open("r", encoding=enc, newline="", errors="replace")
    try:
        if kind == "jsonl":
            # Read once to discover headers union over the first 1000 rows.
            sample_rows: List[Dict[str, str]] = []
            for i, line in enumerate(fh):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    sample_rows.append({k: ("" if v is None else str(v)) for k, v in obj.items()})
                if i >= 1000:
                    break
            headers: List[str] = []
            seen = set()
            for r in sample_rows:
                for k in r.keys():
                    if k not in seen:
                        seen.add(k)
                        headers.append(k)
            # Rewind and produce a fresh iterator over the entire file.
            fh.seek(0)

            def iter_rows():
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(obj, dict):
                        yield {k: ("" if obj.get(k) is None else str(obj.get(k))) for k in headers}

            yield kind, headers, iter_rows()
        else:
            reader = csv.reader(fh, dialect=dialect)
            try:
                headers = next(reader)
            except StopIteration:
                headers = []

            def iter_rows():
                for raw_row in reader:
                    # Pad / truncate to header count
                    if len(raw_row) < len(headers):
                        raw_row = raw_row + [""] * (len(headers) - len(raw_row))
                    elif len(raw_row) > len(headers):
                        raw_row = raw_row[: len(headers)]
                    yield dict(zip(headers, raw_row))

            yield kind, headers, iter_rows()
    finally:
        fh.close()


# ---- Type inference --------------------------------------------------------

_INT_RE = re.compile(r"^-?\d+$")
_FLOAT_RE = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")
_BOOL_VALUES = {"true", "false", "yes", "no", "y", "n", "0", "1", "t", "f"}
_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%m/%d/%Y",
)
_DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M:%S",
)


def _is_int(s: str) -> bool:
    return bool(_INT_RE.match(s))


def _is_float(s: str) -> bool:
    return bool(_FLOAT_RE.match(s)) and not _INT_RE.match(s)


def _is_bool(s: str) -> bool:
    return s.lower() in _BOOL_VALUES


def _is_date(s: str) -> bool:
    for fmt in _DATE_FORMATS:
        try:
            datetime.strptime(s, fmt)
            return True
        except ValueError:
            continue
    return False


def _is_datetime(s: str) -> bool:
    for fmt in _DATETIME_FORMATS:
        try:
            datetime.strptime(s, fmt)
            return True
        except ValueError:
            continue
    return False


def infer_column_type(values: Iterable[str], sample_size: int = 1000) -> str:
    """Return 'int' | 'float' | 'bool' | 'date' | 'datetime' | 'string' | 'empty'.

    Strategy: take up to sample_size non-empty values; if every value matches
    the same narrow type, return it; otherwise widen to 'string'.
    """
    sample: List[str] = []
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if not s:
            continue
        sample.append(s)
        if len(sample) >= sample_size:
            break

    if not sample:
        return "empty"

    candidates = ["int", "float", "bool", "date", "datetime"]
    matches: Dict[str, int] = {c: 0 for c in candidates}
    for s in sample:
        if _is_int(s):
            matches["int"] += 1
        if _is_float(s):
            matches["float"] += 1
        if _is_bool(s):
            matches["bool"] += 1
        if _is_date(s):
            matches["date"] += 1
        if _is_datetime(s):
            matches["datetime"] += 1

    n = len(sample)

    # Prefer the most specific type that matches every value.
    # int beats float (every int matches float regex too, but we only
    # set float when not int).
    if matches["int"] == n:
        return "int"
    # An integer-only column will also satisfy float; allow mixed int+float
    # to be reported as float.
    if matches["int"] + matches["float"] == n and matches["float"] > 0:
        return "float"
    if matches["bool"] == n:
        return "bool"
    if matches["datetime"] == n:
        return "datetime"
    if matches["date"] == n:
        return "date"
    return "string"


# ---- Misc ------------------------------------------------------------------

def human_bytes(n: int) -> str:
    """Format byte count as B/KB/MB/GB with one decimal."""
    if n < 1024:
        return f"{n} B"
    for unit in ("KB", "MB", "GB", "TB"):
        n /= 1024.0
        if n < 1024:
            return f"{n:.1f} {unit}"
    return f"{n:.1f} PB"


def print_error(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
