#!/usr/bin/env python3
"""
Smart File Organizer - Auto-classify files by type, date, and naming patterns.
"""
import argparse, json, shutil, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".json", ".xml", ".yaml", ".yml"},
    "Videos":    {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "Audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives":  {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"},
    "Code":      {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".h", ".rs", ".go", ".rb", ".php", ".sh", ".ps1", ".bat"},
    "Others":    set(),
}

def classify(ext: str) -> str:
    ext = ext.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"

def parse_patterns(s: str) -> dict:
    if not s:
        return {}
    result = {}
    for part in s.split(","):
        if ":" in part:
            folder, pattern = part.split(":", 1)
            result[pattern.strip().lower()] = folder.strip()
    return result

def get_date_dir(fp: Path, mode: str) -> str:
    dt = datetime.fromtimestamp(fp.stat().st_mtime)
    if mode == "year": return dt.strftime("%Y")
    elif mode == "month": return dt.strftime("%Y-%m")
    else: return dt.strftime("%Y-%m-%d")

def is_hidden(p: Path) -> bool:
    n = p.name
    return n.startswith(".") or n.startswith("~$") or n == "Thumbs.db"

def organize(target: Path, method: str, date_mode: str, patterns: dict, dry_run: bool, undo_log: Path) -> dict:
    if not target.exists():
        return {"error": f"Directory not found: {target}"}
    stats = {"moved": 0, "skipped": 0, "errors": 0, "details": []}
    files = [f for f in target.iterdir() if f.is_file() and not is_hidden(f)]
    for fp in files:
        try:
            if method == "type":
                folder = classify(fp.suffix)
            elif method == "date":
                folder = get_date_dir(fp, date_mode)
            elif method == "pattern":
                name_lower = fp.stem.lower()
                folder = "Unmatched"
                for pat, fld in patterns.items():
                    if pat in name_lower:
                        folder = fld
                        break
            else:
                stats["errors"] += 1
                continue
            dest_dir = target / folder
            dest_path = dest_dir / fp.name
            if dest_path.exists():
                stem, suffix = fp.stem, fp.suffix
                c = 1
                while dest_path.exists():
                    dest_path = dest_dir / f"{stem}_{c}{suffix}"
                    c += 1
            if dry_run:
                stats["details"].append(f"[DRY] {fp.name} -> {folder}/")
            else:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(fp), str(dest_path))
                stats["details"].append(f"{fp.name} -> {folder}/")
                stats["moved"] += 1
        except Exception as e:
            stats["errors"] += 1
            stats["details"].append(f"[ERR] {fp.name}: {e}")
    if not dry_run and undo_log:
        undo_log.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    return stats

def undo(target: Path, undo_log: Path):
    if not undo_log.exists():
        print("No undo log found.")
        return
    log = json.loads(undo_log.read_text(encoding="utf-8"))
    undone = 0
    for detail in log.get("details", []):
        if not detail.startswith("[ERR]") and not detail.startswith("[DRY]"):
            parts = detail.split(" -> ")
            if len(parts) == 2:
                fname, folder = parts[0], parts[1].rstrip("/")
                moved = target / folder / fname
                original = target / fname
                if moved.exists():
                    shutil.move(str(moved), str(original))
                    undone += 1
                    print(f"Restored: {fname}")
    for d in sorted(target.iterdir(), reverse=True):
        if d.is_dir() and d.name != "__pycache__":
            try: d.rmdir()
            except OSError: pass
    undo_log.unlink(missing_ok=True)
    print(f"Undone: {undone} files")

def main():
    p = argparse.ArgumentParser(description="Smart File Organizer")
    p.add_argument("--dir", "-d", required=True, help="Target directory")
    p.add_argument("--method", "-m", choices=["type","date","pattern"], default="type")
    p.add_argument("--date-mode", choices=["year","month","day"], default="month")
    p.add_argument("--patterns", "-p", help='Pattern rules: "keyword:folder,keyword2:folder2"')
    p.add_argument("--dry-run", action="store_true", help="Preview only")
    p.add_argument("--undo", action="store_true", help="Undo last operation")
    args = p.parse_args()
    target = Path(args.dir).resolve()
    if args.undo:
        undo(target, target / ".organizer_log.json")
        return 0
    patterns = parse_patterns(args.patterns)
    log = target / ".organizer_log.json"
    print(f"Organizing: {target}")
    print(f"Method: {args.method}" + (f" ({args.date_mode})" if args.method=="date" else ""))
    print(f"Dry-run: {args.dry_run}")
    print("-" * 40)
    stats = organize(target, args.method, args.date_mode, patterns, args.dry_run, log)
    for d in stats["details"]:
        print(f"  {d}")
    print("-" * 40)
    print(f"Moved: {stats['moved']}  |  Errors: {stats['errors']}")
    if args.dry_run:
        print("\nDry run. Remove --dry-run to execute.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
