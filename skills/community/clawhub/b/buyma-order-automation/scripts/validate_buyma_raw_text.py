#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ORDER_RE = re.compile(r'(\d{6})')


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate BUYMA raw translated text format")
    parser.add_argument("--input", required=True, help="Path to buyma_translated_raw.txt")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    result = {
        "input": str(input_path),
        "nonempty_line_count": len(lines),
        "is_even_line_count": len(lines) % 2 == 0,
        "pair_count": len(lines) // 2,
        "valid_order_count": 0,
        "missing_order_count": 0,
        "duplicate_order_count": 0,
        "duplicate_orders": {},
        "preview": [],
        "warnings": [],
    }

    if len(lines) % 2 != 0:
        result["warnings"].append("Line count is odd. Expected 2 lines per order block.")

    extracted_orders = []

    for i in range(0, len(lines) - 1, 2):
        memo_line = lines[i]
        product_line = lines[i + 1]

        m = ORDER_RE.search(memo_line)
        order_no = m.group(1) if m else ""

        if order_no:
            result["valid_order_count"] += 1
            extracted_orders.append(order_no)
        else:
            result["missing_order_count"] += 1

        if len(result["preview"]) < 10:
            result["preview"].append({
                "block_index": (i // 2) + 1,
                "memo_line": memo_line,
                "order_no": order_no,
                "product_name_ko": product_line,
            })

    counter = Counter(extracted_orders)
    dupes = {k: v for k, v in counter.items() if v > 1}
    result["duplicate_order_count"] = len(dupes)
    result["duplicate_orders"] = dupes

    if result["missing_order_count"] > 0:
        result["warnings"].append(f"{result['missing_order_count']} block(s) have no 6-digit order number.")

    if result["duplicate_order_count"] > 0:
        result["warnings"].append(f"{result['duplicate_order_count']} duplicate order number(s) found.")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
