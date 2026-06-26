#!/usr/bin/env python3
"""build_xlsx.py  –  Generate formatted .xlsx workbooks from structured JSON.

Part of the excel-export skill (v1).  Produces polished Excel workbooks
with tables, filters, frozen headers, and French / Morocco formatting
defaults.  Write-only – does not read or edit existing workbooks.

Usage
-----
    python build_xlsx.py --input workbook.json --output report.xlsx
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import xlsxwriter
except ImportError:
    print(
        "FATAL  xlsxwriter is not installed – "
        "run:  pip install xlsxwriter",
        file=sys.stderr,
    )
    sys.exit(3)

# ━━ Excel limits ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAX_ROWS = 1_048_576
MAX_COLS = 16_384
MAX_SHEET_NAME = 31
SHEET_NAME_BAD = set("[]:*?/\\")

# ━━ Type → default number format (French / Morocco) ━━━━━━━━━━━━━━━━━
DEFAULT_FORMATS: dict[str, str | None] = {
    "text":     None,
    "integer":  "#,##0",
    "number":   "#,##0.00",
    "percent":  "0.0%",
    "currency": '#,##0.00 "MAD"',
    "date":     "dd/mm/yyyy",
    "datetime": "dd/mm/yyyy hh:mm",
    "boolean":  None,               # rendered as Oui / Non text
}
VALID_TYPES  = frozenset(DEFAULT_FORMATS)
VALID_TOTALS = frozenset(("sum", "average", "count"))

# ━━ Column-width estimation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WIDTH_MIN = 8
WIDTH_MAX = 50
WIDTH_PAD = 2


# ─── helpers ──────────────────────────────────────────────────────────

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR  {msg}", file=sys.stderr)
    sys.exit(code)


def _validate_sheet_name(name: str) -> None:
    """Fail fast if a sheet name violates Excel rules."""
    if not name or not name.strip():
        die(f"sheet name is empty or blank")
    if len(name) > MAX_SHEET_NAME:
        die(f"sheet name '{name}' exceeds {MAX_SHEET_NAME}-character Excel limit")
    bad_chars = set(name) & SHEET_NAME_BAD
    if bad_chars:
        die(f"sheet name '{name}' contains illegal characters: {sorted(bad_chars)}")
    if name.startswith("'") or name.endswith("'"):
        die(f"sheet name '{name}' must not start or end with an apostrophe")


def _check_duplicate_sheet_names(sheets: list[dict]) -> None:
    """Fail fast on duplicate sheet names (case-insensitive, matching Excel)."""
    seen: dict[str, str] = {}
    for sh in sheets:
        name = sh["name"]
        lower = name.lower()
        if lower in seen:
            die(f"duplicate sheet name '{name}' (conflicts with '{seen[lower]}')")
        seen[lower] = name


def _table_name(sheet_name: str, idx: int) -> str:
    base = "".join(c if c.isalnum() else "_" for c in sheet_name)
    if not base or base[0].isdigit():
        base = f"T_{base}"
    return f"{base}_{idx + 1}"


# ─── validation ───────────────────────────────────────────────────────

def validate(spec: dict) -> None:
    if not isinstance(spec.get("sheets"), list) or not spec["sheets"]:
        die("JSON root must contain a non-empty 'sheets' array")

    for i, sh in enumerate(spec["sheets"]):
        _validate_sheet(sh, i)


def _validate_sheet(sh: dict, i: int) -> None:
    tag = f"sheets[{i}]"
    if not isinstance(sh, dict):
        die(f"{tag}: must be an object")
    if not sh.get("name") or not isinstance(sh["name"], str):
        die(f"{tag}: 'name' is required (string)")
    _validate_sheet_name(sh["name"])

    if sh.get("subtitle") and not sh.get("title"):
        die(f"{tag}: 'subtitle' requires 'title' — cannot use subtitle alone")

    cols = sh.get("columns")
    if not isinstance(cols, list) or not cols:
        die(f"{tag}: 'columns' must be a non-empty array")
    if len(cols) > MAX_COLS:
        die(f"{tag}: {len(cols)} columns exceeds Excel limit ({MAX_COLS:,})")

    keys: set[str] = set()
    for j, c in enumerate(cols):
        _validate_col(c, j, tag, keys)

    rows = sh.get("rows", [])
    if not isinstance(rows, list):
        die(f"{tag}: 'rows' must be an array")
    if len(rows) > MAX_ROWS - 10:      # header + possible title rows + totals
        die(f"{tag}: {len(rows):,} rows exceeds Excel limit")
    for r, row in enumerate(rows):
        if not isinstance(row, dict):
            die(f"{tag}.rows[{r}]: must be an object")
        bad = set(row) - keys
        if bad:
            die(f"{tag}.rows[{r}]: unknown keys {sorted(bad)}")


def _validate_col(c: dict, j: int, parent: str, keys: set[str]) -> None:
    tag = f"{parent}.columns[{j}]"
    if not isinstance(c, dict):
        die(f"{tag}: must be an object")

    key = c.get("key")
    if not key or not isinstance(key, str):
        die(f"{tag}: 'key' is required (string)")
    if key in keys:
        die(f"{tag}: duplicate key '{key}'")
    keys.add(key)

    if not c.get("header") or not isinstance(c["header"], str):
        die(f"{tag}: 'header' is required (string)")

    ctype = c.get("type", "text")
    if ctype not in VALID_TYPES:
        die(f"{tag}: unknown type '{ctype}' – valid: {sorted(VALID_TYPES)}")

    total = c.get("total")
    if total and total not in VALID_TOTALS:
        die(f"{tag}: invalid total '{total}' – valid: {sorted(VALID_TOTALS)}")

    if c.get("formula") is not None and not isinstance(c["formula"], str):
        die(f"{tag}: 'formula' must be a string")


# ─── value coercion ───────────────────────────────────────────────────

def _must_stay_text(val: object) -> bool:
    """True when a string value must be stored as text to prevent
    Excel data-loss (leading zeros, phone numbers, >15-digit IDs)."""
    if not isinstance(val, str):
        return False
    s = val.strip()
    if not s:
        return False
    if s.startswith("+"):                                   # phone
        return True
    if len(s) > 1 and s[0] == "0" and s.isdigit():         # leading zero
        return True
    digits = s.replace(".", "").replace("-", "").replace(",", "")
    if digits.isdigit() and len(digits) > 15:               # precision
        return True
    return False


_DT_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
)


def coerce(val: object, ctype: str, col_key: str, row_idx: int):
    """Return a Python value that xlsxwriter can write directly.

    Raises ValueError for typed columns when the value cannot be
    converted to the declared type (fail-fast contract).
    """
    if val is None:
        return None

    # ── boolean → Oui / Non ──────────────────────────────────────
    if ctype == "boolean":
        if isinstance(val, bool):
            return "Oui" if val else "Non"
        if isinstance(val, (int, float)) and val in (0, 1, 0.0, 1.0):
            return "Oui" if val else "Non"
        if isinstance(val, str):
            low = val.strip().lower()
            if low in ("true", "1", "yes", "oui"):
                return "Oui"
            if low in ("false", "0", "no", "non"):
                return "Non"
        raise ValueError(
            f"column '{col_key}' row {row_idx}: "
            f"unrecognized boolean value {val!r}"
        )

    # ── forced text ──────────────────────────────────────────────
    if ctype == "text" or _must_stay_text(val):
        return str(val)

    # ── date ─────────────────────────────────────────────────────
    if ctype == "date":
        if isinstance(val, date) and not isinstance(val, datetime):
            return val
        if isinstance(val, str):
            try:
                return datetime.strptime(val[:10], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"column '{col_key}' row {row_idx}: "
                    f"cannot parse '{val}' as date (expected YYYY-MM-DD)"
                )
        raise ValueError(
            f"column '{col_key}' row {row_idx}: "
            f"expected date string or date object, got {type(val).__name__}"
        )

    # ── datetime ─────────────────────────────────────────────────
    if ctype == "datetime":
        if isinstance(val, datetime):
            return val
        if isinstance(val, date):
            return datetime(val.year, val.month, val.day)
        if isinstance(val, str):
            for fmt in _DT_FORMATS:
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    pass
            # last resort: date only
            try:
                return datetime.strptime(val[:10], "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"column '{col_key}' row {row_idx}: "
                    f"cannot parse '{val}' as datetime"
                )
        raise ValueError(
            f"column '{col_key}' row {row_idx}: "
            f"expected datetime/date string or object, got {type(val).__name__}"
        )

    # ── numeric ──────────────────────────────────────────────────
    if ctype in ("integer", "number", "percent", "currency"):
        # bool is a subclass of int in Python — reject it explicitly
        if isinstance(val, bool):
            raise ValueError(
                f"column '{col_key}' row {row_idx}: "
                f"expected numeric value, got boolean"
            )
        if isinstance(val, (int, float)):
            # Guard: integers beyond 15 digits lose precision in Excel
            if isinstance(val, int) and len(str(abs(val))) > 15:
                return str(val)
            if isinstance(val, float) and val.is_integer() and len(str(int(abs(val)))) > 15:
                return str(val)
            if ctype == "integer" and isinstance(val, float) and not val.is_integer():
                raise ValueError(
                    f"column '{col_key}' row {row_idx}: "
                    f"expected integer, got float {val!r} (would truncate)"
                )
            return int(val) if ctype == "integer" and isinstance(val, float) else val
        if isinstance(val, str):
            try:
                clean = val.strip().replace("\u00a0", "").replace(" ", "")
                if ctype == "integer":
                    parsed = float(clean)
                    if not parsed.is_integer():
                        raise ValueError(
                            f"column '{col_key}' row {row_idx}: "
                            f"expected integer, got '{val}' (would truncate)"
                        )
                    return int(parsed)
                return float(clean)
            except (ValueError, OverflowError):
                raise ValueError(
                    f"column '{col_key}' row {row_idx}: "
                    f"cannot parse '{val}' as {ctype}"
                )
        raise ValueError(
            f"column '{col_key}' row {row_idx}: "
            f"expected numeric value or string, got {type(val).__name__}"
        )

    return val


# ─── column-width estimation ─────────────────────────────────────────

_TYPE_DISPLAY_LEN = {
    "date": 10,       # dd/mm/yyyy
    "datetime": 16,   # dd/mm/yyyy hh:mm
    "boolean": 3,     # Oui
}


def _display_len(val: object, ctype: str) -> int:
    if val is None:
        return 0
    fixed = _TYPE_DISPLAY_LEN.get(ctype)
    if fixed is not None:
        return fixed
    return len(str(val))


def _estimate_widths(cols: list[dict], rows: list[dict]) -> list[float]:
    sample = rows[:200]
    widths: list[float] = []
    for col in cols:
        key   = col["key"]
        ctype = col.get("type", "text")
        best  = len(col["header"])
        for row in sample:
            best = max(best, _display_len(row.get(key), ctype))
        auto = min(max(best + WIDTH_PAD, WIDTH_MIN), WIDTH_MAX)
        widths.append(col.get("width") or auto)
    return widths


# ─── cell writer ──────────────────────────────────────────────────────

def _write_cell(ws, row: int, col: int, val, fmt) -> None:
    if val is None:
        ws.write_blank(row, col, None, fmt)
    elif isinstance(val, datetime):
        ws.write_datetime(row, col, val, fmt)
    elif isinstance(val, date):
        ws.write_datetime(row, col, val, fmt)
    elif isinstance(val, (int, float)):
        ws.write_number(row, col, val, fmt)
    elif isinstance(val, str):
        ws.write_string(row, col, val, fmt)
    else:
        ws.write(row, col, val, fmt)


# ─── sheet renderer ──────────────────────────────────────────────────

def _render_sheet(
    wb: xlsxwriter.Workbook,
    sh: dict,
    idx: int,
    title_fmt,
    subtitle_fmt,
) -> int:
    """Render one sheet into the workbook.  Returns data-row count."""
    ws   = wb.add_worksheet(sh["name"])
    cols = sh["columns"]
    rows = sh.get("rows", [])
    n_c  = len(cols)
    n_r  = len(rows)

    title    = sh.get("title")
    subtitle = sh.get("subtitle")
    has_tot  = any(c.get("total") for c in cols)

    # ── layout offset ────────────────────────────────────────────
    if title and subtitle:
        hdr_row = 3
    elif title:
        hdr_row = 2
    else:
        hdr_row = 0

    # ── title / subtitle ─────────────────────────────────────────
    if title:
        if n_c > 1:
            ws.merge_range(0, 0, 0, n_c - 1, title, title_fmt)
        else:
            ws.write_string(0, 0, title, title_fmt)
    if subtitle:
        row_s = 1
        if n_c > 1:
            ws.merge_range(row_s, 0, row_s, n_c - 1, subtitle, subtitle_fmt)
        else:
            ws.write_string(row_s, 0, subtitle, subtitle_fmt)

    # ── freeze pane at first data row ────────────────────────────
    ws.freeze_panes(hdr_row + 1, 0)

    # ── column formats ───────────────────────────────────────────
    col_fmts = []
    for c in cols:
        ctype  = c.get("type", "text")
        numfmt = c.get("numfmt") or DEFAULT_FORMATS.get(ctype)
        col_fmts.append(wb.add_format({"num_format": numfmt}) if numfmt else None)

    # ── column widths ────────────────────────────────────────────
    for ci, w in enumerate(_estimate_widths(cols, rows)):
        ws.set_column(ci, ci, w)

    # ── write data cells (skip formula columns) ──────────────────
    for ri, row in enumerate(rows):
        xl_row = hdr_row + 1 + ri
        for ci, col in enumerate(cols):
            if col.get("formula"):
                continue                    # table API writes these
            key   = col["key"]
            ctype = col.get("type", "text")
            try:
                val = coerce(row.get(key), ctype, key, ri)
            except ValueError as exc:
                die(f"sheet '{sh['name']}': {exc}")
            _write_cell(ws, xl_row, ci, val, col_fmts[ci])

    # ── table range ──────────────────────────────────────────────
    body   = max(n_r, 1)                    # Excel table needs >= 1 data row
    last_r = hdr_row + body + (1 if has_tot else 0)

    # ── table column definitions ─────────────────────────────────
    tbl_cols: list[dict] = []
    for ci, col in enumerate(cols):
        td: dict = {"header": col["header"]}
        if col_fmts[ci]:
            td["format"] = col_fmts[ci]
        if col.get("formula"):
            td["formula"] = col["formula"]
        tot = col.get("total")
        if tot:
            td["total_function"] = tot
        elif has_tot and ci == 0:
            td["total_string"] = "Total"
        tbl_cols.append(td)

    ws.add_table(hdr_row, 0, last_r, n_c - 1, {
        "name":        _table_name(sh["name"], idx),
        "style":       "Table Style Medium 9",
        "columns":     tbl_cols,
        "autofilter":  True,
        "banded_rows": True,
        "total_row":   has_tot,
    })

    return n_r


# ─── workbook builder ────────────────────────────────────────────────

def build(spec: dict, output: str) -> list[dict]:
    out_dir = os.path.dirname(os.path.abspath(output))
    os.makedirs(out_dir, exist_ok=True)

    wb = xlsxwriter.Workbook(output, {
        "default_date_format": "dd/mm/yyyy",
        "strings_to_numbers":  False,
        "strings_to_urls":     False,
    })

    title_fmt = wb.add_format({
        "bold": True,
        "font_size": 14,
        "font_color": "#1F2937",
    })
    subtitle_fmt = wb.add_format({
        "italic": True,
        "font_size": 11,
        "font_color": "#6B7280",
    })

    summary: list[dict] = []
    for i, sh in enumerate(spec["sheets"]):
        count = _render_sheet(wb, sh, i, title_fmt, subtitle_fmt)
        summary.append({"sheet": sh["name"], "rows": count})

    wb.close()
    return summary


# ─── CLI entry point ─────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate a formatted .xlsx workbook from a JSON spec",
    )
    ap.add_argument("--input",  required=True, help="Path to workbook JSON")
    ap.add_argument("--output", required=True, help="Output .xlsx path")
    args = ap.parse_args()

    # ── read input ───────────────────────────────────────────────
    if not os.path.isfile(args.input):
        die(f"input file not found: {args.input}")
    try:
        with open(args.input, encoding="utf-8") as fh:
            spec = json.load(fh)
    except json.JSONDecodeError as exc:
        die(f"invalid JSON: {exc}")

    # ── validate ─────────────────────────────────────────────────
    validate(spec)
    _check_duplicate_sheet_names(spec["sheets"])

    # ── build ────────────────────────────────────────────────────
    summary = build(spec, args.output)

    # ── deterministic stdout summary ─────────────────────────────
    result = {
        "success": True,
        "output":  os.path.abspath(args.output),
        "sheets":  summary,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
