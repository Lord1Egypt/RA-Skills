#!/usr/bin/env python3
"""
03_tabulate_and_rfi.py — Extract schedules from Excel/Word and generate RFIs.
Usage: python 03_tabulate_and_rfi.py <client_given_dir> <output_dir>
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def extract_excel_ref_errors(filepath: str) -> list:
    """Detect #REF! errors in CSV-exported Excel content (best-effort)."""
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row_idx, row in enumerate(reader, start=1):
                for col_idx, cell in enumerate(row, start=1):
                    if "#REF!" in cell:
                        errors.append({
                            "file": filepath,
                            "row": row_idx,
                            "col": col_idx,
                            "cell": cell,
                        })
    except Exception as e:
        errors.append({"file": filepath, "error": str(e)})
    return errors


def extract_word_data_gaps(filepath: str) -> list:
    """Scan DOCX/DOC text for placeholder keywords indicating missing data."""
    gaps = []
    placeholders = [
        r"to be provided",
        r"tbd",
        r"tbc",
        r"pending",
        r"awaiting",
        r"not available",
        r"supplier to confirm",
        r"missing",
    ]
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().lower()
            for ph in placeholders:
                matches = re.finditer(ph, text, re.IGNORECASE)
                for m in matches:
                    # Approximate line number by counting newlines before match
                    line = text[: m.start()].count("\n") + 1
                    gaps.append(
                        {
                            "file": filepath,
                            "placeholder": ph,
                            "line_approx": line,
                            "context": text[m.start() : m.start() + 80].replace("\n", " "),
                        }
                    )
    except Exception as e:
        gaps.append({"file": filepath, "error": str(e)})
    return gaps


def generate_rfi(gaps: list, missing_survey: bool, missing_crs: bool) -> dict:
    """Build a structured RFI document."""
    rfi_id = f"RFI-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    items = []
    if missing_survey:
        items.append(
            {
                "id": f"{rfi_id}-01",
                "discipline": "Civil / Survey",
                "issue": "Topographic survey data not found in client deliverables.",
                "request": "Provide certified topographic survey with control points, CRS/EPSG code, and elevation benchmark.",
                "priority": "Blocking",
            }
        )
    if missing_crs:
        items.append(
            {
                "id": f"{rfi_id}-02",
                "discipline": "Civil / Survey",
                "issue": "Coordinate reference system (CRS) not specified.",
                "request": "Confirm project CRS/EPSG code and datum for all CAD deliverables.",
                "priority": "Blocking",
            }
        )
    for idx, g in enumerate(gaps, start=3):
        items.append(
            {
                "id": f"{rfi_id}-{idx:02d}",
                "discipline": "General",
                "issue": f"Placeholder or missing data in {os.path.basename(g['file'])}.",
                "request": f"Replace placeholder '{g.get('placeholder', 'N/A')}' with confirmed data.",
                "priority": "Normal",
                "reference": g.get("context", ""),
            }
        )
    return {"rfi_id": rfi_id, "date": datetime.now(timezone.utc).isoformat(), "items": items}


def main():
    parser = argparse.ArgumentParser(description="Tabulate schedules and generate RFIs.")
    parser.add_argument("src", help="Path to client_given directory")
    parser.add_argument("out", help="Path to output directory")
    args = parser.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    tables_dir = out / "tables"
    rfi_dir = out / "rfi"
    tables_dir.mkdir(parents=True, exist_ok=True)
    rfi_dir.mkdir(parents=True, exist_ok=True)

    print("==========================================")
    print(" Tabulation & RFI Generation")
    print(f" Source: {src}")
    print(f" Output: {out}")
    print("==========================================")

    # 1. Excel/CSV extraction
    print("[1/3] Scanning Excel/CSV for #REF! and tabulation...")
    all_ref_errors = []
    excel_files = list(src.rglob("*.xlsx")) + list(src.rglob("*.xls")) + list(src.rglob("*.csv"))
    for ef in excel_files:
        errs = extract_excel_ref_errors(str(ef))
        all_ref_errors.extend(errs)
    print(f"  Excel/CSV files scanned: {len(excel_files)}")
    print(f"  #REF! errors found: {len(all_ref_errors)}")

    ref_report = tables_dir / "excel_ref_errors.json"
    with open(ref_report, "w", encoding="utf-8") as f:
        json.dump(all_ref_errors, f, indent=2, ensure_ascii=False)
    print(f"  Report: {ref_report}")

    # 2. Word/DOCX extraction
    print("[2/3] Scanning Word documents for data gaps...")
    all_gaps = []
    word_files = list(src.rglob("*.docx")) + list(src.rglob("*.doc"))
    for wf in word_files:
        gaps = extract_word_data_gaps(str(wf))
        all_gaps.extend(gaps)
    print(f"  Word files scanned: {len(word_files)}")
    print(f"  Placeholder gaps found: {len(all_gaps)}")

    gaps_report = tables_dir / "word_data_gaps.json"
    with open(gaps_report, "w", encoding="utf-8") as f:
        json.dump(all_gaps, f, indent=2, ensure_ascii=False)
    print(f"  Report: {gaps_report}")

    # 3. RFI generation
    print("[3/3] Generating RFI...")
    missing_survey = not any("survey" in str(p).lower() for p in src.rglob("*"))
    missing_crs = not any(re.search(r"epsg|crs|datum", str(p).lower()) for p in src.rglob("*"))
    rfi = generate_rfi(all_gaps, missing_survey, missing_crs)

    rfi_path = rfi_dir / f"{rfi['rfi_id']}.json"
    with open(rfi_path, "w", encoding="utf-8") as f:
        json.dump(rfi, f, indent=2, ensure_ascii=False)
    print(f"  RFI: {rfi_path}")
    print(f"  Items: {len(rfi['items'])}")

    # 4. Summary CSV
    summary_csv = tables_dir / "rfi_summary.csv"
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rfi_id", "item_id", "discipline", "priority", "issue"])
        for item in rfi["items"]:
            writer.writerow([rfi["rfi_id"], item["id"], item["discipline"], item["priority"], item["issue"]])
    print(f"  Summary CSV: {summary_csv}")

    print("==========================================")
    print("Tabulation & RFI complete.")


if __name__ == "__main__":
    main()
