#!/usr/bin/env python3

import argparse, json, sys, os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    parser.add_argument("--prefix", default="")
    parser.add_argument("--suffix", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    files = sorted(os.listdir(args.dir))
    result = []
    for i, f in enumerate(files, 1):
        ext = os.path.splitext(f)[1]
        new = f"{args.prefix}{i:03d}{args.suffix}{ext}"
        old_path = os.path.join(args.dir, f)
        new_path = os.path.join(args.dir, new)
        result.append({"old": f, "new": new, "exists": os.path.exists(new_path)})
        if not args.dry_run and not os.path.exists(new_path):
            os.rename(old_path, new_path)
    print(json.dumps({"renamed": len([r for r in result if not r["exists"]]), "dry_run": args.dry_run, "files": result}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
