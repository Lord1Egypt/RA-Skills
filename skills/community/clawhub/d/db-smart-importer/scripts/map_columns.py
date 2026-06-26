#!/usr/bin/env python3
"""Suggest column mappings between source and destination columns."""

import sys
import json
import re


def normalize(s):
    """Normalize column name for matching."""
    s = s.lower().replace("_", " ").replace("-", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def tokens(s):
    """Get tokens from normalized string."""
    return set(normalize(s).split())


def similarity(col1, col2):
    """Calculate similarity between two column names."""
    n1, n2 = normalize(col1), normalize(col2)

    if n1 == n2:
        return 1.0

    t1, t2 = tokens(col1), tokens(col2)
    if not t1 or not t2:
        return 0.0

    intersection = len(t1 & t2)
    union = len(t1 | t2)

    if intersection > 0:
        jaccard = intersection / union

        if n1 in n2 or n2 in n1:
            return max(jaccard, 0.8)

        return jaccard

    return 0.0


def suggest_mappings(source_cols, dest_cols, sample_data=None):
    """Suggest column mappings based on similarity."""
    mappings = {}
    used_dest = set()

    source_cols = (
        json.loads(source_cols) if isinstance(source_cols, str) else source_cols
    )
    dest_cols = json.loads(dest_cols) if isinstance(dest_cols, str) else dest_cols

    for src in source_cols:
        best_match = None
        best_score = 0

        for dst in dest_cols:
            if dst in used_dest:
                continue

            score = similarity(src, dst)
            if score > best_score:
                best_score = score
                best_match = dst

        if best_match and best_score >= 0.3:
            mappings[src] = best_match
            used_dest.add(best_match)

    return mappings


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: map_columns.py <source_cols_json> <dest_cols_json> [sample_data_json]"
        )
        print('Example: map_columns.py \'["email", "name"]\' \'["email", "client"]\'')
        sys.exit(1)

    source_cols = sys.argv[1]
    dest_cols = sys.argv[2]
    sample_data = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        mappings = suggest_mappings(source_cols, dest_cols, sample_data)
        print(json.dumps(mappings, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
