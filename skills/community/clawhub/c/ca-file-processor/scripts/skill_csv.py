"""
OpenClaw Skill: CSV Processor (Open-Source Path)
=================================================
Reads CSV files and normalises them for LLM consumption.
Specifically tuned for Indian bank statement formats and
CA firm data exports.

Auto-detects:
  - Encoding (UTF-8, latin-1, cp1252 — common in Indian bank exports)
  - Delimiter (, or | or tab — HDFC uses | sometimes)
  - Header row location (some bank CSVs have metadata rows on top)
  - Column types: date, amount, description, balance

Dependencies:
    pip install pandas chardet

Usage in OpenClaw skill config:
    skill_name: csv_processor
    trigger: "*.csv uploaded"
    entry: process_csv(file_path)
"""

import json
import re
import io
from pathlib import Path
from datetime import datetime

import pandas as pd


# ── CONFIG ────────────────────────────────────────────────────────────────────

MAX_ROWS = 5000
PREVIEW_ROWS = 20
ENCODINGS_TO_TRY = ["utf-8", "latin-1", "cp1252", "utf-8-sig"]

# Common Indian bank statement column name patterns
DATE_COLS     = ["date", "txn date", "transaction date", "value date",
                 "posting date", "tran date", "dt"]
DEBIT_COLS    = ["debit", "withdrawal", "dr", "debit amount",
                 "withdrawal amt", "chq/ref no"]
CREDIT_COLS   = ["credit", "deposit", "cr", "credit amount",
                 "deposit amt"]
BALANCE_COLS  = ["balance", "closing balance", "running balance",
                 "available balance", "bal"]
DESC_COLS     = ["description", "narration", "particulars", "remarks",
                 "transaction details", "details", "chq/ref details"]


# ── MAIN ENTRY POINT ─────────────────────────────────────────────────────────

def process_csv(file_path: str) -> dict:
    """
    Main entry point called by OpenClaw when a CSV is received.

    Returns:
        {
          "file":         str,
          "rows":         int,
          "columns":      list[str],
          "doc_type":     str,          # "bank_statement" | "gst_export" | "generic"
          "column_map":   dict,         # standardised column name mapping
          "data":         list[dict],   # normalised rows
          "summary":      dict,         # totals, date range, etc.
          "preview_text": str,          # first N rows as text
        }
    """
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    raw_text, encoding = _read_with_encoding(path)
    if raw_text is None:
        return {"error": "Could not decode file. Unsupported encoding."}

    df, delimiter, header_row = _smart_parse(raw_text)
    if df is None:
        return {"error": "Could not parse CSV structure."}

    df = _clean_dataframe(df)
    col_map = _detect_column_map(df.columns.tolist())
    doc_type = _detect_doc_type(df.columns.tolist(), raw_text[:500])
    data = _to_records(df)
    summary = _build_summary(df, col_map, doc_type)

    return {
        "file": path.name,
        "encoding": encoding,
        "delimiter": repr(delimiter),
        "rows": len(df),
        "columns": df.columns.tolist(),
        "doc_type": doc_type,
        "column_map": col_map,
        "data": data[:MAX_ROWS],
        "truncated": len(df) > MAX_ROWS,
        "summary": summary,
        "preview_text": _preview_text(df, col_map),
    }


# ── ENCODING DETECTION ────────────────────────────────────────────────────────

def _read_with_encoding(path: Path):
    """Try multiple encodings common in Indian bank exports."""
    for enc in ENCODINGS_TO_TRY:
        try:
            text = path.read_text(encoding=enc)
            return text, enc
        except (UnicodeDecodeError, LookupError):
            continue

    # Last resort: chardet
    try:
        import chardet
        raw_bytes = path.read_bytes()
        detected = chardet.detect(raw_bytes)
        enc = detected.get("encoding", "utf-8")
        return raw_bytes.decode(enc, errors="replace"), enc
    except Exception:
        return None, None


# ── SMART PARSING ─────────────────────────────────────────────────────────────

def _smart_parse(raw_text: str):
    """
    Detect delimiter and header row location.
    Some bank CSVs (HDFC, Kotak) have 10-15 metadata rows before the actual table.
    """
    lines = raw_text.strip().split("\n")

    # Detect delimiter: count occurrences in first 5 non-empty lines
    delimiters = [",", "|", "\t", ";"]
    counts = {d: 0 for d in delimiters}
    sample_lines = [l for l in lines if l.strip()][:5]
    for line in sample_lines:
        for d in delimiters:
            counts[d] += line.count(d)
    delimiter = max(counts, key=counts.get)
    if counts[delimiter] == 0:
        delimiter = ","

    # Find header row: first row with 3+ non-empty delimited fields
    header_row_idx = 0
    for i, line in enumerate(lines):
        fields = [f.strip() for f in line.split(delimiter)]
        non_empty = [f for f in fields if f]
        if len(non_empty) >= 3:
            header_row_idx = i
            break

    # Skip metadata rows, parse from header
    data_text = "\n".join(lines[header_row_idx:])
    try:
        df = pd.read_csv(
            io.StringIO(data_text),
            sep=delimiter,
            dtype=str,
            skipinitialspace=True,
            on_bad_lines="skip",
            nrows=MAX_ROWS + 1,
        )
        return df, delimiter, header_row_idx
    except Exception:
        return None, delimiter, 0


# ── DATA CLEANING ─────────────────────────────────────────────────────────────

def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise column names and clean values."""
    # Normalise column names
    df.columns = [
        str(c).strip().lower()
                    .replace("\n", " ")
                    .replace("  ", " ")
        for c in df.columns
    ]

    # Drop fully empty columns and rows
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")

    # Strip whitespace from all string values
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": "", "None": "", "NaN": ""})

    return df.reset_index(drop=True)


# ── COLUMN MAP DETECTION ──────────────────────────────────────────────────────

def _detect_column_map(columns: list) -> dict:
    """
    Map actual column names to standardised CA field names.
    Returns e.g. {"date": "txn date", "debit": "withdrawal amt", ...}
    """
    col_lower = [c.lower() for c in columns]
    mapping = {}

    def find_col(candidates):
        for candidate in candidates:
            for col in col_lower:
                if candidate in col:
                    return columns[col_lower.index(col)]
        return None

    for field, candidates in [
        ("date",    DATE_COLS),
        ("debit",   DEBIT_COLS),
        ("credit",  CREDIT_COLS),
        ("balance", BALANCE_COLS),
        ("description", DESC_COLS),
    ]:
        found = find_col(candidates)
        if found:
            mapping[field] = found

    return mapping


# ── DOCUMENT TYPE DETECTION ───────────────────────────────────────────────────

def _detect_doc_type(columns: list, header_text: str) -> str:
    combined = " ".join(columns).lower() + " " + header_text.lower()

    if any(kw in combined for kw in ["gstin", "hsn", "igst", "cgst", "sgst"]):
        return "gst_export"
    if any(kw in combined for kw in ["debit", "credit", "withdrawal", "deposit", "balance"]):
        return "bank_statement"
    if any(kw in combined for kw in ["salary", "employee", "payroll", "pf", "esic"]):
        return "payroll_export"
    if any(kw in combined for kw in ["ledger", "narration", "voucher"]):
        return "tally_export"
    return "generic"


# ── RECORDS & SUMMARY ─────────────────────────────────────────────────────────

def _to_records(df: pd.DataFrame) -> list:
    """Convert DataFrame to list of dicts, preserving all columns."""
    return df.to_dict(orient="records")


def _build_summary(df: pd.DataFrame, col_map: dict, doc_type: str) -> dict:
    """Build numeric summary for bank statements and payroll CSVs."""
    summary = {
        "doc_type": doc_type,
        "total_rows": len(df),
    }

    def parse_amount(series):
        """Strip commas and currency symbols, convert to float."""
        cleaned = series.str.replace(r"[₹,\s]", "", regex=True)
        return pd.to_numeric(cleaned, errors="coerce").fillna(0)

    if doc_type == "bank_statement":
        if "debit" in col_map:
            summary["total_debits"] = round(
                parse_amount(df[col_map["debit"]]).sum(), 2)
        if "credit" in col_map:
            summary["total_credits"] = round(
                parse_amount(df[col_map["credit"]]).sum(), 2)
        if "date" in col_map:
            dates = df[col_map["date"]].dropna()
            if not dates.empty:
                summary["date_range"] = f"{dates.iloc[0]} → {dates.iloc[-1]}"

    return summary


def _preview_text(df: pd.DataFrame, col_map: dict) -> str:
    """First N rows as readable text for LLM context."""
    lines = [" | ".join(df.columns.tolist())]
    for _, row in df.head(PREVIEW_ROWS).iterrows():
        lines.append(" | ".join(str(v) for v in row.values))
    return "\n".join(lines)


# ── OPENCLAW SKILL METADATA ───────────────────────────────────────────────────

SKILL_METADATA = {
    "name": "csv_processor",
    "version": "1.0.0",
    "description": "Parses CSV files with auto-encoding and delimiter detection. Tuned for Indian bank exports.",
    "triggers": ["*.csv", "process csv", "bank statement"],
    "entry_function": "process_csv",
    "output_format": "dict → passed to LLM context",
    "ca_use_cases": [
        "HDFC / ICICI / SBI bank statement exports",
        "GSTR-2B reconciliation downloads",
        "Tally CSV exports",
        "Payroll CSV registers",
        "GST portal data exports",
    ]
}


# ── QUICK TEST ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python skill_csv.py <path_to_csv>")
        sys.exit(1)
    result = process_csv(sys.argv[1])
    print(json.dumps({k: v for k, v in result.items() if k != "data"}, indent=2))
