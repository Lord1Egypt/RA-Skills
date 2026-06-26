#!/usr/bin/env python3
"""Preview a downloads organization plan."""
import argparse, json, os, shutil
from pathlib import Path

def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_group(ext, groups):
    ext = ext.lower()
    for name, exts in groups.items():
        if ext in exts:
            return name
    return "other"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="Downloads folder")
    ap.add_argument("--rules", default="resources/rules.sample.json")
    ap.add_argument("--apply", action="store_true", help="Actually move files")
    args = ap.parse_args()
    rules = load_rules(args.rules)
    folder = Path(args.folder)
    moves = []
    for item in folder.iterdir():
        if item.is_file():
            group = detect_group(item.suffix, rules["groups"])
            target_dir = folder / group / item.stat().st_mtime_ns.__str__()[:7]
            target = target_dir / item.name
            moves.append({"source": str(item), "target": str(target), "group": group})
            if args.apply:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(target))
    print(json.dumps({"preview_only": not args.apply, "moves": moves}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
