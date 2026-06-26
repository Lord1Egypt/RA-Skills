"""
Shared row-writer used by head.py, tail.py, and sample.py.

Pure standard library. No third-party imports.

Provides:
  - ALLOWED_AS     tuple of valid --as values
  - select_columns subset / validate a header list against an optional
                   user-supplied column list
  - write_rows     emit rows to stdout or a file in csv|tsv|jsonl|md|aligned
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional


ALLOWED_AS = {"csv", "tsv", "jsonl", "md", "aligned"}


def select_columns(headers: List[str],
                   selected: Optional[List[str]]) -> List[str]:
    """Return headers, optionally filtered to `selected`.

    Raises KeyError with a clear message if any selected name is not in headers.
    Empty / None `selected` means "keep every header".
    """
    if not selected:
        return list(headers)
    missing = [c for c in selected if c not in headers]
    if missing:
        raise KeyError(
            f"column(s) not found in header: {', '.join(missing)}. "
            f"Available: {', '.join(headers)}"
        )
    # Preserve the user-supplied order, not the original header order.
    return list(selected)


def _md_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("\r", "")


def _aligned_lines(rows: List[Dict[str, str]], headers: List[str],
                   include_header: bool) -> List[str]:
    """Render rows as a fixed-width text table sized to the actual data."""
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            v = str(r.get(h, ""))
            if "\n" in v:
                v = v.replace("\n", " ").replace("\r", "")
            widths[h] = max(widths[h], len(v))

    def fmt_row(values: List[str]) -> str:
        return "  ".join(v.ljust(widths[headers[i]]) for i, v in enumerate(values))

    lines: List[str] = []
    if include_header:
        lines.append(fmt_row(headers))
        lines.append("  ".join("-" * widths[h] for h in headers))
    for r in rows:
        lines.append(fmt_row([str(r.get(h, "")) for h in headers]))
    return lines


def _csv_string(rows: List[Dict[str, str]], headers: List[str],
                delimiter: str, include_header: bool) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers,
                            delimiter=delimiter, lineterminator="\n")
    if include_header:
        writer.writeheader()
    for r in rows:
        writer.writerow({h: r.get(h, "") for h in headers})
    return buf.getvalue()


def _md_string(rows: List[Dict[str, str]], headers: List[str],
               include_header: bool) -> str:
    lines: List[str] = []
    if include_header:
        lines.append("| " + " | ".join(_md_escape(h) for h in headers) + " |")
        lines.append("|" + "|".join(" --- " for _ in headers) + "|")
    for r in rows:
        cells = [_md_escape(str(r.get(h, ""))) for h in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + ("\n" if lines else "")


def _jsonl_string(rows: List[Dict[str, str]], headers: List[str]) -> str:
    out = io.StringIO()
    for r in rows:
        out.write(json.dumps({h: r.get(h, "") for h in headers},
                             ensure_ascii=False))
        out.write("\n")
    return out.getvalue()


def write_rows(rows: List[Dict[str, str]], headers: List[str], as_fmt: str,
               out_path: Optional[Path] = None,
               include_header: bool = True) -> None:
    """Render rows to stdout (or out_path) in the chosen format.

    JSON Lines mode ignores include_header because JSONL has no header concept.
    """
    if as_fmt == "csv":
        text = _csv_string(rows, headers, ",", include_header)
    elif as_fmt == "tsv":
        text = _csv_string(rows, headers, "\t", include_header)
    elif as_fmt == "jsonl":
        text = _jsonl_string(rows, headers)
    elif as_fmt == "md":
        text = _md_string(rows, headers, include_header)
    elif as_fmt == "aligned":
        lines = _aligned_lines(rows, headers, include_header)
        text = "\n".join(lines) + ("\n" if lines else "")
    else:
        raise ValueError(f"unknown --as value: {as_fmt!r}")

    if out_path is None:
        sys.stdout.write(text)
        sys.stdout.flush()
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
