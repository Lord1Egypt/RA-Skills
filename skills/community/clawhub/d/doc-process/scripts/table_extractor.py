#!/usr/bin/env python3
"""
table_extractor.py — Extract tables from PDFs to CSV or JSON.

Requires: pdfplumber

Usage:
  python table_extractor.py --file document.pdf --output data.csv
  python table_extractor.py --file document.pdf --output data.json --format json
  python table_extractor.py --file document.pdf --output data.csv --pages 2-5
  python table_extractor.py --file document.pdf --output data.csv --table 1
  python table_extractor.py --file document.pdf --list
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path


def _require_pdfplumber():
    try:
        import pdfplumber
        return pdfplumber
    except ImportError:
        print(
            "Error: pdfplumber is not installed.\n"
            "Install it with:  pip install pdfplumber",
            file=sys.stderr,
        )
        sys.exit(1)


def _parse_pages(pages_arg: str | None, total_pages: int) -> list[int]:
    """Parse '2-5' or '3' or '1,3,5' into a list of 0-based page indices."""
    if not pages_arg:
        return list(range(total_pages))
    indices = []
    for part in pages_arg.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            indices.extend(range(int(lo) - 1, int(hi)))
        else:
            indices.append(int(part) - 1)
    return [i for i in indices if 0 <= i < total_pages]


def _clean_cell(value) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def _extract_tables(pdf_path: Path, page_indices: list[int]) -> list[dict]:
    pdfplumber = _require_pdfplumber()
    results = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_idx in page_indices:
            if page_idx >= len(pdf.pages):
                continue
            page = pdf.pages[page_idx]
            tables = page.extract_tables()
            for tbl_idx, table in enumerate(tables):
                if not table:
                    continue
                # First row as headers
                raw_headers = [_clean_cell(c) for c in table[0]]
                # Deduplicate blank headers
                headers = []
                seen: dict[str, int] = {}
                for h in raw_headers:
                    if not h:
                        h = f"Column{len(headers)+1}"
                    if h in seen:
                        seen[h] += 1
                        h = f"{h}_{seen[h]}"
                    else:
                        seen[h] = 0
                    headers.append(h)

                rows = []
                for row in table[1:]:
                    cleaned = [_clean_cell(c) for c in row]
                    # Pad or trim to match header count
                    while len(cleaned) < len(headers):
                        cleaned.append("")
                    cleaned = cleaned[: len(headers)]
                    rows.append(dict(zip(headers, cleaned)))

                results.append({
                    "page": page_idx + 1,
                    "table_index": tbl_idx + 1,
                    "table_title": f"Page {page_idx+1}, Table {tbl_idx+1}",
                    "source": pdf_path.name,
                    "headers": headers,
                    "rows": rows,
                    "row_count": len(rows),
                    "notes": [],
                })
    return results


def _tables_to_csv(tables: list[dict], single_table: int | None = None) -> str:
    """Return CSV string. If multiple tables, separate with blank line + comment."""
    output = io.StringIO()

    target = tables
    if single_table is not None:
        idx = single_table - 1
        if 0 <= idx < len(tables):
            target = [tables[idx]]
        else:
            print(f"Error: Table {single_table} not found (found {len(tables)}).", file=sys.stderr)
            return ""

    for i, tbl in enumerate(target):
        if i > 0:
            output.write("\n")
        output.write(f"# Table {tbl['table_index']}: {tbl['table_title']}\n")
        writer = csv.DictWriter(output, fieldnames=tbl["headers"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(tbl["rows"])

    return output.getvalue()


def _tables_to_json(tables: list[dict], single_table: int | None = None) -> str:
    target = tables
    if single_table is not None:
        idx = single_table - 1
        if 0 <= idx < len(tables):
            target = [tables[idx]]
    if len(target) == 1:
        return json.dumps(target[0], indent=2, ensure_ascii=False)
    return json.dumps(target, indent=2, ensure_ascii=False)


def cmd_list(pdf_path: Path, page_indices: list[int]) -> int:
    tables = _extract_tables(pdf_path, page_indices)
    if not tables:
        print("No tables found in the specified pages.")
        return 0
    print(f"Found {len(tables)} table(s):\n")
    print(f"| # | Page | Rows | Columns | Sample Headers |")
    print("|---|---|---|---|---|")
    for tbl in tables:
        sample_headers = ", ".join(tbl["headers"][:4])
        if len(tbl["headers"]) > 4:
            sample_headers += f", … ({len(tbl['headers'])} total)"
        print(
            f"| {tbl['table_index']} "
            f"| {tbl['page']} "
            f"| {tbl['row_count']} "
            f"| {len(tbl['headers'])} "
            f"| {sample_headers} |"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="table_extractor",
        description="Extract tables from PDFs to CSV or JSON.",
    )
    parser.add_argument("--file", required=True, help="Path to PDF file")
    parser.add_argument("--output", help="Output file path (.csv or .json)")
    parser.add_argument(
        "--format", choices=["csv", "json"], default="csv",
        help="Output format (default: csv; inferred from --output extension if not set)"
    )
    parser.add_argument("--pages", help="Page range, e.g. '2-5' or '1,3,5'")
    parser.add_argument("--table", type=int, help="Extract only table N (1-based)")
    parser.add_argument("--list", action="store_true", help="List all tables without extracting")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    pdf_path = Path(args.file).expanduser()
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Warning: File does not have .pdf extension: {pdf_path}", file=sys.stderr)

    pdfplumber = _require_pdfplumber()
    with pdfplumber.open(str(pdf_path)) as pdf:
        total_pages = len(pdf.pages)

    page_indices = _parse_pages(getattr(args, "pages", None), total_pages)

    if args.list:
        return cmd_list(pdf_path, page_indices)

    if not args.output:
        print("Error: --output is required when not using --list.", file=sys.stderr)
        return 1

    tables = _extract_tables(pdf_path, page_indices)
    if not tables:
        print("No tables found.", file=sys.stderr)
        return 1

    print(f"Extracted {len(tables)} table(s), {sum(t['row_count'] for t in tables)} total rows.", file=sys.stderr)

    # Infer format from extension
    out_fmt = args.format
    out_path = Path(args.output).expanduser()
    if out_path.suffix.lower() == ".json":
        out_fmt = "json"
    elif out_path.suffix.lower() == ".csv":
        out_fmt = "csv"

    if out_fmt == "json":
        content = _tables_to_json(tables, getattr(args, "table", None))
    else:
        content = _tables_to_csv(tables, getattr(args, "table", None))

    if not content:
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"Output written to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
