#!/usr/bin/env python3
import json
import sys


def score(source_level: int, freshness: int, cross_check: int, page_type: int):
    total = source_level + freshness + cross_check + page_type
    if total >= 17:
        band = "high"
    elif total >= 12:
        band = "medium"
    else:
        band = "low"
    return total, band


def main():
    if len(sys.argv) != 5:
        print("Usage: score_result.py <source_level 1-5> <freshness 1-5> <cross_check 1-5> <page_type 1-5>", file=sys.stderr)
        sys.exit(1)
    vals = list(map(int, sys.argv[1:5]))
    total, band = score(*vals)
    print(json.dumps({
        "sourceLevel": vals[0],
        "freshness": vals[1],
        "crossCheck": vals[2],
        "pageType": vals[3],
        "total": total,
        "reliability": band
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
