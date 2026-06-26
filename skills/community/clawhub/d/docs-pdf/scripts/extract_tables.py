#!/usr/bin/env python3
"""
extract_tables.py — Extract all tables from a PDF to an Excel workbook.

Usage:
    python scripts/extract_tables.py report.pdf
    python scripts/extract_tables.py report.pdf --output tables.xlsx
    python scripts/extract_tables.py report.pdf --strategy text   # for borderless tables
"""
import argparse
from pathlib import Path
import pdfplumber
import pandas as pd

STRATEGIES = {
    "lines":  {"vertical_strategy": "lines",  "horizontal_strategy": "lines"},
    "text":   {"vertical_strategy": "text",   "horizontal_strategy": "text"},
    "mixed":  {"vertical_strategy": "lines",  "horizontal_strategy": "text"},
}

def main():
    parser = argparse.ArgumentParser(description="Extract tables from PDF to Excel")
    parser.add_argument("input",                   help="Input PDF path")
    parser.add_argument("--output",    "-o",       help="Output .xlsx path")
    parser.add_argument("--strategy",  "-s",
                        choices=list(STRATEGIES),
                        default="lines",
                        help="Table detection strategy (default: lines)")
    parser.add_argument("--min-rows",  type=int, default=1,
                        help="Minimum rows for a table to be kept (default: 1)")
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output) if args.output else src.with_suffix(".xlsx")

    settings = {**STRATEGIES[args.strategy], "snap_tolerance": 3}
    all_dfs  = []

    with pdfplumber.open(src) as pdf:
        for p_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables(settings)
            for t_num, table in enumerate(tables, 1):
                if not table or len(table) < args.min_rows + 1:
                    continue
                # Use first row as header; sanitise None cells
                headers = [str(h or f"col_{i}") for i, h in enumerate(table[0])]
                rows    = [[str(c or "") for c in row] for row in table[1:]]
                df      = pd.DataFrame(rows, columns=headers)
                df.insert(0, "_page",  p_num)
                df.insert(1, "_table", t_num)
                all_dfs.append(df)
                print(f"  Page {p_num}, Table {t_num}: {len(df)} rows × {len(df.columns)-2} cols")

    if not all_dfs:
        print("No tables found. Try --strategy text or --strategy mixed.")
        return

    with pd.ExcelWriter(dst, engine="openpyxl") as writer:
        # All tables on one sheet (good for small results)
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.to_excel(writer, sheet_name="All Tables", index=False)
        # One sheet per table
        for i, df in enumerate(all_dfs):
            sheet = f"P{df['_page'].iloc[0]}_T{df['_table'].iloc[0]}"
            df.drop(columns=["_page","_table"]).to_excel(writer, sheet_name=sheet, index=False)

    print(f"\n✓ {len(all_dfs)} tables → {dst}")

if __name__ == "__main__":
    main()
