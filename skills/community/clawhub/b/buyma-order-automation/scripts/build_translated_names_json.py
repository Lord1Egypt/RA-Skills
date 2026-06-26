#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ORDER_RE = re.compile(r'(\d{6})')

def main() -> None:
    parser = argparse.ArgumentParser(description="Build translated_names.json from line-based text input")
    parser.add_argument("--input", required=True, help="Input text file path")
    parser.add_argument("--out", required=True, help="Output json path")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    result = []
    i = 0
    while i < len(lines) - 1:
        memo_line = lines[i]
        product_line = lines[i + 1]

        m = ORDER_RE.search(memo_line)
        if m:
            result.append({
                "order_no": m.group(1),
                "product_name_ko": product_line
            })
            i += 2
        else:
            i += 1

    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "count": len(result),
        "output": str(out_path)
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
