#!/usr/bin/env python3
"""Search architecture patterns from the patterns CSV database.

Usage:
    python search.py "microservices"           # keyword search
    python search.py --category "Resilience"   # by category (partial match)
    python search.py --complexity low           # by complexity level
    python search.py --scale enterprise         # by scale
    python search.py --list-categories          # show all categories
    python search.py --all                      # show all patterns
"""

import argparse
import csv
import os
import sys
from typing import List, Dict

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "patterns.csv")

VALID_COMPLEXITY = {"low", "medium", "high"}
VALID_SCALE = {"small", "medium", "large", "enterprise"}

HEADER_ID = "ID"
HEADER_NAME = "Name"
HEADER_CATEGORY = "Category"
HEADER_COMPLEXITY = "Cplx"
HEADER_SCALE = "Scale"


def load_patterns() -> List[Dict[str, str]]:
    """Load patterns from the CSV file."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}", file=sys.stderr)
        sys.exit(1)

    patterns = []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            patterns.append(row)
    return patterns


def search_keyword(patterns: List[Dict[str, str]], keyword: str) -> List[Dict[str, str]]:
    """Search patterns by keyword across all text fields."""
    keyword_lower = keyword.lower()
    results = []
    searchable_fields = ["name", "category", "description", "use_case", "tradeoffs"]
    for p in patterns:
        for field in searchable_fields:
            if keyword_lower in p.get(field, "").lower():
                results.append(p)
                break
    return results


def filter_by_field(patterns: List[Dict[str, str]], field: str, value: str) -> List[Dict[str, str]]:
    """Filter patterns by exact or partial match on a field."""
    value_lower = value.lower()
    return [p for p in patterns if value_lower in p.get(field, "").lower()]


def get_categories(patterns: List[Dict[str, str]]) -> List[str]:
    """Get sorted unique categories."""
    categories = sorted(set(p["category"] for p in patterns))
    return categories


def format_table(patterns: List[Dict[str, str]]) -> str:
    """Format patterns as an aligned table."""
    if not patterns:
        return "  No patterns found."

    col_id = max(len(HEADER_ID), max(len(p["id"]) for p in patterns))
    col_name = max(len(HEADER_NAME), max(len(p["name"]) for p in patterns))
    col_cat = max(len(HEADER_CATEGORY), max(len(p["category"]) for p in patterns))
    col_cplx = max(len(HEADER_COMPLEXITY), max(len(p["complexity"]) for p in patterns))
    col_scale = max(len(HEADER_SCALE), max(len(p["scale"]) for p in patterns))

    header = (
        f"  {HEADER_ID:>{col_id}}  {HEADER_NAME:<{col_name}}  "
        f"{HEADER_CATEGORY:<{col_cat}}  {HEADER_COMPLEXITY:<{col_cplx}}  {HEADER_SCALE:<{col_scale}}"
    )
    sep = "  " + "-" * (col_id + col_name + col_cat + col_cplx + col_scale + 8)

    lines = [header, sep]
    for p in patterns:
        line = (
            f"  {p['id']:>{col_id}}  {p['name']:<{col_name}}  "
            f"{p['category']:<{col_cat}}  {p['complexity']:<{col_cplx}}  {p['scale']:<{col_scale}}"
        )
        lines.append(line)

    return "\n".join(lines)


def print_detail(pattern: Dict[str, str]) -> None:
    """Print detailed view of a single pattern."""
    print(f"\n  [{pattern['id']}] {pattern['name']}")
    print(f"  Category:   {pattern['category']}")
    print(f"  Complexity: {pattern['complexity']}")
    print(f"  Scale:      {pattern['scale']}")
    print(f"  Description: {pattern['description']}")
    print(f"  Use case:    {pattern['use_case']}")
    print(f"  Tradeoffs:   {pattern['tradeoffs']}")


def print_results(patterns: List[Dict[str, str]], detail: bool = False) -> None:
    """Print search results."""
    count = len(patterns)
    label = "pattern" if count == 1 else "patterns"
    print(f"\n  Found {count} {label}:\n")

    if detail and count <= 5:
        for p in patterns:
            print_detail(p)
        print()
    else:
        print(format_table(patterns))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search architecture patterns database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("keyword", nargs="?", help="Keyword to search across all fields")
    parser.add_argument("--category", "-c", help="Filter by category (partial match)")
    parser.add_argument(
        "--complexity", "-x",
        choices=sorted(VALID_COMPLEXITY),
        help="Filter by complexity level",
    )
    parser.add_argument(
        "--scale", "-s",
        choices=sorted(VALID_SCALE),
        help="Filter by scale",
    )
    parser.add_argument("--list-categories", "-l", action="store_true", help="List all categories")
    parser.add_argument("--detail", "-d", action="store_true", help="Show detailed output (auto for <=5 results)")
    parser.add_argument("--all", "-a", action="store_true", help="Show all patterns")

    args = parser.parse_args()

    if not any([args.keyword, args.category, args.complexity, args.scale, args.list_categories, args.all]):
        parser.print_help()
        sys.exit(0)

    patterns = load_patterns()

    if args.list_categories:
        categories = get_categories(patterns)
        print("\n  Categories:\n")
        for cat in categories:
            count = sum(1 for p in patterns if p["category"] == cat)
            print(f"    - {cat} ({count} patterns)")
        print()
        return

    results = patterns

    if args.keyword:
        results = search_keyword(results, args.keyword)
    if args.category:
        results = filter_by_field(results, "category", args.category)
    if args.complexity:
        results = filter_by_field(results, "complexity", args.complexity)
    if args.scale:
        results = filter_by_field(results, "scale", args.scale)

    show_detail = args.detail or len(results) <= 3
    print_results(results, detail=show_detail)


if __name__ == "__main__":
    main()
