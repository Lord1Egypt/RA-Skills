#!/usr/bin/env python3
"""Line sorter (stdlib only)."""
import sys, argparse, random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("-o", "--output")
    ap.add_argument("--sort", action="store_true")
    ap.add_argument("--unique", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--numeric", action="store_true")
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--by-length", action="store_true")
    args = ap.parse_args()
    with open(args.file, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    if args.unique:
        seen, uniq = set(), []
        for l in lines:
            if l not in seen:
                seen.add(l); uniq.append(l)
        lines = uniq
    if args.numeric:
        lines.sort(key=lambda x: float(x) if x.replace('.','',1).lstrip('-').isdigit() else float('inf'), reverse=args.reverse)
    elif args.by_length:
        lines.sort(key=len, reverse=args.reverse)
    elif args.shuffle:
        random.shuffle(lines)
    elif args.reverse:
        lines.reverse()
    elif args.sort:
        lines.sort(reverse=args.reverse)
    out = "\n".join(lines) + ("\n" if lines else "")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"✅ 已处理 {len(lines)} 行 -> {args.output}")
    else:
        print(out, end="")

if __name__ == "__main__":
    main()
