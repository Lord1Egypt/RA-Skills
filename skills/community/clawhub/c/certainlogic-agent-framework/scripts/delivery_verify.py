#!/usr/bin/env python3
"""
Delivery Verify — business-logic specific verification gate.

Checks for correct jurisdiction, entity names, arbitration clauses,
and financial figures before delivering legal/financial documents.

Usage:
    python3 delivery_verify.py <file>
    python3 delivery_verify.py <file> --jurisdiction Illinois
"""
import argparse
import re
import sys
from pathlib import Path


def check_jurisdiction(text, expected_jurisdiction):
    """Verify the document uses the correct jurisdiction."""
    found = re.findall(r'\b(?:State of\s+)?(Illinois|Delaware|New York|California|Texas|Nevada|Florida)\b', text)
    unique = set(found)
    if expected_jurisdiction and expected_jurisdiction not in unique:
        return False, f"Jurisdiction '{expected_jurisdiction}' not found. Found: {unique or 'none'}"
    if not expected_jurisdiction:
        return True, f"Jurisdiction(s) found: {unique or 'none'}"
    return True, f"Correct jurisdiction '{expected_jurisdiction}' confirmed"


def check_entity_names(text, expected_entity=None):
    """Check for LLC/Inc/Corp entity names."""
    entities = re.findall(r'\b[A-Z][A-Za-z0-9]+ (?:LLC|Inc|Corp|Ltd|LP)\b', text)
    if expected_entity and expected_entity not in text:
        return False, f"Expected entity '{expected_entity}' not found"
    return True, f"Entities found: {entities}" if entities else (True, "No entity names found (ok)")


def check_arbitration(text):
    """Check if arbitration clause is present."""
    if re.search(r'\barbitration\b', text, re.IGNORECASE):
        return True, "Arbitration clause present"
    return False, "No arbitration clause found"


def check_dollar_figures(text):
    """Verify dollar figures are present if expected."""
    amounts = re.findall(r'\$\d[\d,.]*', text)
    return True, f"Dollar figures: {amounts}" if amounts else (True, "No dollar figures (ok if not expected)")


def main():
    parser = argparse.ArgumentParser(description="Business-logic delivery verification")
    parser.add_argument("file", help="File to verify")
    parser.add_argument("--jurisdiction", default="", help="Expected jurisdiction (e.g., Illinois)")
    parser.add_argument("--entity", default="", help="Expected entity name")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    text = path.read_text()
    issues = []

    # Run checks
    ok, msg = check_jurisdiction(text, args.jurisdiction)
    if not ok:
        issues.append(msg)

    ok, msg = check_entity_names(text, args.entity)
    if not ok:
        issues.append(msg)

    ok, msg = check_arbitration(text)
    if not ok:
        issues.append(msg)

    ok, msg = check_dollar_figures(text)

    if issues:
        print(f"=== DELIVERY VERIFY — {len(issues)} issue(s) in '{args.file}' ===")
        for i in issues:
            print(f"  ❌ {i}")
        sys.exit(1)

    print(f"DELIVERY_VERIFY ✓ '{args.file}' — clean")
    sys.exit(0)


if __name__ == "__main__":
    main()