#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ORDER_RE = re.compile(r'(\d{6})')

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert BUYMA raw text into structured JSON")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) % 2 != 0:
        raise SystemExit("Input line count must be even (2 lines per block).")

    rows = []
    for i in range(0, len(lines), 2):
        memo_line = lines[i]
        product_name_ja = lines[i + 1]
        m = ORDER_RE.search(memo_line)
        order_no = m.group(1) if m else ""
        rows.append({
            "order_no": order_no,
            "memo_line": memo_line,
            "product_name_ja": product_name_ja,
        })

    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(rows), "output": str(out_path)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
