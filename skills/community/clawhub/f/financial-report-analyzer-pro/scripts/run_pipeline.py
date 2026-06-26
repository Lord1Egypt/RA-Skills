#!/usr/bin/env python3
"""Financial Report Analyzer · end-to-end pipeline (demo)."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from compute_ratios import compute_ratios
from detect_red_flags import detect_red_flags


def _load_input(path: str) -> dict:
    """Read normalized financial statement JSON.

    For the bundled demo we accept either:
      - a pre-normalized JSON (recommended for testing), or
      - a placeholder PDF path (returns a stub so the pipeline shape can be
        verified end-to-end without bundling pdfplumber / camelot).
    """
    p = Path(path)
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    return {
        "company": {"name": p.stem, "ticker": "UNKNOWN", "industry": "n/a"},
        "period": {"fiscal_year": 0, "reporting_basis": "unknown"},
        "income_statement": {},
        "balance_sheet": {},
        "cash_flow": {},
        "_note": "Bundled demo did not parse PDFs; supply a normalized JSON for full analysis.",
    }


def run(financials: dict, mode: str) -> dict:
    out: dict = {"company": financials.get("company"), "period": financials.get("period")}
    if mode in ("full", "ratios"):
        out["ratios"] = compute_ratios(financials)
    if mode in ("full", "red-flag-only"):
        out["red_flags"] = detect_red_flags(financials)
    out["executive_summary"] = _summarize(financials, out)
    return out


def _summarize(fin: dict, computed: dict) -> str:
    name = (fin.get("company") or {}).get("name", "Company")
    period = (fin.get("period") or {}).get("fiscal_year", "?")
    flags = computed.get("red_flags", [])
    flag_count = sum(1 for f in flags if f.get("severity") in ("🟡", "🔴"))
    return f"{name} FY{period}: ratios computed, {flag_count} elevated red flag(s)."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True)
    ap.add_argument("--mode", choices=["full", "ratios", "red-flag-only"], default="full")
    ap.add_argument("--output", "-o", default="-")
    args = ap.parse_args()
    fin = _load_input(args.input)
    result = run(fin, args.mode)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(text)
    else:
        Path(args.output).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
