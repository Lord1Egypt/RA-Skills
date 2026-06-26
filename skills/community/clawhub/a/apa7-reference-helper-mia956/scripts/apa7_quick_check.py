#!/usr/bin/env python3
"""Quick APA 7 reference-list triage.

This script reads a UTF-8 text file with one reference per line and reports
common structural issues. It intentionally uses only Python's standard library.
It is not a complete APA parser; it is a fast checklist helper for students.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

YEAR_RE = re.compile(r"\((?:19|20)\d{2}(?:,\s*[A-Za-z]+\s+\d{1,2})?\)")
DOI_RAW_RE = re.compile(r"10\.\d{4,9}/\S+", re.IGNORECASE)
DOI_URL_RE = re.compile(r"https://doi\.org/10\.\d{4,9}/\S+", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
INITIAL_RE = re.compile(r"^[A-Z][A-Za-z'\-]+,\s*(?:[A-Z]\.\s*)+")


def check_reference(ref: str) -> Dict[str, object]:
    issues: List[str] = []
    suggestions: List[str] = []
    stripped = ref.strip()

    if not stripped:
        return {"reference": ref, "issues": ["empty line"], "suggestions": ["Remove empty lines."], "score": 0}

    if not YEAR_RE.search(stripped):
        issues.append("missing or nonstandard year in parentheses")
        suggestions.append("Add year after authors, e.g., (2024).")

    if DOI_RAW_RE.search(stripped) and not DOI_URL_RE.search(stripped):
        issues.append("DOI is not formatted as a URL")
        suggestions.append("Use https://doi.org/xxxxx rather than doi: or raw DOI.")

    if "doi:" in stripped.lower():
        issues.append("uses old DOI prefix")
        suggestions.append("Replace doi: with https://doi.org/.")

    if "retrieved from" in stripped.lower():
        issues.append("possibly unnecessary 'Retrieved from'")
        suggestions.append("APA 7 usually omits 'Retrieved from' for stable sources.")

    if not INITIAL_RE.search(stripped):
        issues.append("author format may be nonstandard")
        suggestions.append("Check author format: Surname, A. A., & Surname, B. B.")

    # Light heuristic: a journal article should often contain a volume-like comma after the title.
    if URL_RE.search(stripped) and "doi.org" not in stripped.lower() and not any(ch.isdigit() for ch in stripped):
        issues.append("web source may be missing date")
        suggestions.append("Add publication date if available, or (n.d.) if no date exists.")

    if stripped.endswith(";") or stripped.endswith(","):
        issues.append("reference ends with unusual punctuation")
        suggestions.append("End the reference with a period, DOI, or URL as appropriate.")

    score = max(0, 100 - 15 * len(issues))
    return {"reference": stripped, "issues": issues or ["no obvious structural issue"], "suggestions": suggestions or ["Review manually for APA 7 details."], "score": score}


def main() -> int:
    parser = argparse.ArgumentParser(description="Quick APA 7 reference-list checker")
    parser.add_argument("file", help="UTF-8 text file, one reference per line")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of a readable report")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    refs = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    results = [check_reference(ref) for ref in refs]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"Checked {len(results)} reference(s).")
        print("=" * 72)
        for idx, result in enumerate(results, 1):
            print(f"[{idx}] Score: {result['score']}/100")
            print(result["reference"])
            print("Issues:")
            for issue in result["issues"]:
                print(f"  - {issue}")
            print("Suggestions:")
            for suggestion in result["suggestions"]:
                print(f"  - {suggestion}")
            print("-" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
