#!/usr/bin/env python3
"""CSV to JSON converter (stdlib only)."""
import csv, json, sys, argparse

def coerce(v):
    v = v.strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("-o", "--output")
    ap.add_argument("--delimiter", default=",")
    ap.add_argument("--compact", action="store_true")
    args = ap.parse_args()
    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=args.delimiter)
        rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        print("⚠️ 文件为空")
        return
    header = rows[0]
    out = []
    for r in rows[1:]:
        obj = {header[i]: coerce(r[i]) if i < len(r) else None for i in range(len(header))}
        out.append(obj)
    text = json.dumps(out, ensure_ascii=False, indent=None if args.compact else 2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ 已转换 {len(out)} 行 -> {args.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
