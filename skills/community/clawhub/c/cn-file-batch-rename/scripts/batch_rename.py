#!/usr/bin/env python3
"""Batch file renamer (stdlib only)."""
import os, re, sys, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--replace", help="old:new")
    ap.add_argument("--sequence", action="store_true")
    ap.add_argument("--ext", help="只处理该扩展名，如 .jpg")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = [f for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f))]
    if args.ext:
        files = [f for f in files if f.lower().endswith(args.ext.lower())]
    files.sort()
    repl = args.replace.split(":", 1) if args.replace else None
    plan = []
    for idx, f in enumerate(files, 1):
        base, ext = os.path.splitext(f)
        new = base
        if repl:
            new = new.replace(repl[0], repl[1])
        if args.sequence:
            new = f"{idx:03d}_{new}"
        new = f"{args.prefix}{new}{args.suffix}{ext}"
        if new != f:
            plan.append((f, new))
    if not plan:
        print("ℹ️ 没有需要改名的文件")
        return
    for old, new in plan:
        print(f"{'🔄' if not args.dry_run else '👁'}  {old}  ->  {new}")
        if not args.dry_run:
            os.rename(os.path.join(args.dir, old), os.path.join(args.dir, new))
    print(f"\n{'预览' if args.dry_run else '已执行'}: {len(plan)} 个文件" + ("（去掉 --dry-run 实际执行）" if args.dry_run else ""))

if __name__ == "__main__":
    main()
