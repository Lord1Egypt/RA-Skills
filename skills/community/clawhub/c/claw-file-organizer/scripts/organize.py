#!/usr/bin/env python3
"""
File Organizer — sorts files into categorized folders with rename, undo, and dry-run support.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_CONFIG = {
    "source_dirs": ["~/Downloads"],
    "target_base": "~/organized-files",
    "auto_sort": True,
    "rename_pattern": "{name}_{date}",
    "max_file_size_mb": 500,
    "exclude_patterns": ["*.tmp", "*.swp", ".DS_Store", "Thumbs.db"],
    "log_file": "ORGANIZE_LOG.json",
}

# File type to folder mapping
FILE_CATEGORIES = {
    "images": ["jpg", "jpeg", "png", "gif", "svg", "webp", "bmp", "tiff", "tif", "ico", "heic"],
    "documents": ["pdf", "doc", "docx", "txt", "rtf", "odt", "ppt", "pptx", "xls", "xlsx", "odp", "odg", "tex", "epub"],
    "audio": ["mp3", "wav", "flac", "ogg", "aac", "m4a", "wma", "aiff"],
    "video": ["mp4", "mkv", "avi", "mov", "webm", "flv", "wmv", "m4v", "3gp"],
    "archives": ["zip", "tar", "gz", "7z", "rar", "bz2", "xz", "tgz", "zst"],
    "code": ["py", "js", "ts", "jsx", "tsx", "html", "css", "scss", "md", "json", "yaml", "yml", "sh", "bat", "ps1", "rb", "go", "rs", "java", "c", "cpp", "h", "swift", "kt", "php", "sql"],
    "data": ["csv", "xml", "db", "sqlite", "sqlite3", "dat", "log"],
    "installers": ["exe", "msi", "dmg", "app", "pkg", "deb", "rpm", "apk", "iso", "img"],
    "fonts": ["ttf", "otf", "woff", "woff2", "fon", "eot"],
}

CATEGORIES = {v.lower(): k for k, vals in FILE_CATEGORIES.items() for v in vals}


def load_config(config_path="config.yaml"):
    """Load config from YAML or fall back to defaults."""
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f) or DEFAULT_CONFIG
    except ImportError:
        # Minimal YAML parser fallback
        pass
    except FileNotFoundError:
        pass

    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        # Simple key: value parsing for basic YAML
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    if val.startswith("[") and val.endswith("]"):
                        items = [i.strip().strip('"').strip("'") for i in val[1:-1].split(",") if i.strip()]
                        cfg[key] = items
                    elif val.startswith('"') and val.endswith('"'):
                        cfg[key] = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        cfg[key] = val[1:-1]
    return cfg


def expand_paths(paths):
    """Expand ~ and relative paths to absolute."""
    result = []
    for p in paths:
        p = os.path.expanduser(p)
        if not os.path.isabs(p):
            p = os.path.abspath(p)
        result.append(p)
    return result


def glob_match(pattern, filename):
    """Simple glob matching (supports *, ? patterns)."""
    regex = "^" + pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".") + "$"
    return bool(re.match(regex, filename, re.IGNORECASE))


def should_exclude(filename, exclude_patterns):
    """Check if file matches any exclude pattern."""
    for pat in exclude_patterns:
        if glob_match(pat, filename):
            return True
    return False


def extract_date(filename):
    """Extract YYYY-MM-DD date from filename. Returns tuple (y, m, d) or None."""
    matches = re.findall(r"(\d{4})[-_](\d{1,2})[-_](\d{1,2})", filename)
    if matches:
        y, m, d = matches[0]
        return (y, f"{int(m):02d}", f"{int(d):02d}")
    # Try month-day-year (validate: month <= 12, day <= 31)
    matches = re.findall(r"(\d{1,2})[-_](\d{1,2})[-_](\d{4})", filename)
    if matches:
        a, b, y = matches[0]
        a, b = int(a), int(b)
        if a > 12:
            # Likely day-first: swap
            a, b = b, a
        return (y, f"{a:02d}", f"{b:02d}")
    return None

def extract_date_str(filename):
    """Extract YYYY-MM-DD date string from filename."""
    d = extract_date(filename)
    return "-".join(d) if d else None

def strip_existing_date(filename):
    """Remove date patterns from the stem of a filename."""
    p = Path(filename)
    stem = p.stem
    # Remove YYYY-MM-DD or YYYY_MM_DD patterns
    stem = re.sub(r"\d{4}[_-]\d{1,2}[_-]\d{1,2}", "", stem)
    stem = re.sub(r"\d{1,2}[_-]\d{1,2}[_-]\d{4}", "", stem)
    # Clean up double underscores/dashes left behind
    stem = re.sub(r"_+", "_", stem)
    stem = re.sub(r"-+", "-", stem)
    stem = stem.strip("_-")
    return stem if stem else p.stem


def sanitize_name(name, date=None, pattern="{name}_{date}"):
    """Create a clean filename from source."""
    p = Path(name)
    ext = p.suffix.lower() if p.suffix else ""
    base = p.stem

    if date and pattern != "none":
        # Strip existing date from stem to avoid duplication
        base = strip_existing_date(name)

    # Remove spaces
    base = base.replace(" ", "_")
    # Remove special chars (keep hyphens, underscores, alphanumeric)
    base = re.sub(r"[^\w\-]", "", base)
    # Collapse multiple underscores/dashes
    base = re.sub(r"_+", "_", base).strip("_-")
    if not base:
        base = "unnamed"

    if pattern == "none":
        return f"{base}{ext}"

    if date:
        return f"{base}_{date}{ext}"
    return f"{base}{ext}"


def get_category(filename):
    """Determine file category based on extension."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return CATEGORIES.get(ext, "other")


def organize_directory(source_dir, target_base, config, dry_run=False):
    """Organize files in a directory."""
    source = os.path.abspath(source_dir)
    target = os.path.abspath(target_base)

    if not os.path.isdir(source):
        print(f"Error: Source directory not found: {source_dir}")
        return None

    exclude = config.get("exclude_patterns", ["*.tmp", "*.swp", ".DS_Store", "Thumbs.db"])
    max_size = config.get("max_file_size_mb", 500) * 1024 * 1024
    rename_pat = config.get("rename_pattern", "{name}_{date}")
    log_file = config.get("log_file", "ORGANIZE_LOG.json")

    moves = []
    errors = []
    counts = {}

    os.makedirs(target, exist_ok=True)

    for filename in os.listdir(source):
        filepath = os.path.join(source, filename)

        # Skip directories
        if not os.path.isfile(filepath):
            continue

        # Skip exclude patterns
        if should_exclude(filename, exclude):
            continue

        # Skip large files
        try:
            size = os.path.getsize(filepath)
            if size > max_size:
                errors.append({"file": filename, "reason": f"Too large ({size // 1024 // 1024}MB)"})
                continue
        except OSError as e:
            errors.append({"file": filename, "reason": str(e)})
            continue

        # Get category
        ext = Path(filename).suffix.lower()
        if not ext:
            continue  # No extension, skip

        category = get_category(filename)
        counts[category] = counts.get(category, 0) + 1

        # Build new path
        cat_dir = os.path.join(target, category)
        date_str = extract_date_str(filename)
        new_name = sanitize_name(filename, date_str, rename_pat)
        new_path = os.path.join(cat_dir, new_name)

        # Handle duplicates
        if os.path.exists(new_path):
            base = Path(new_name).stem
            suffix = Path(new_name).suffix
            counter = 2
            while os.path.exists(new_path := os.path.join(cat_dir, f"{base}_{counter}{suffix}")):
                counter += 1
            new_path = os.path.join(cat_dir, f"{base}_{counter}{suffix}")

        if dry_run:
            print(f"  [DRY RUN] {filename} → {category}/{new_name.lstrip('.')}")
        else:
            os.makedirs(cat_dir, exist_ok=True)
            try:
                shutil.move(filepath, new_path)
                moves.append({
                    "original": filepath,
                    "new": new_path,
                    "category": category,
                    "date": datetime.now().isoformat(),
                })
            except OSError as e:
                errors.append({"file": filename, "reason": str(e)})

    return {
        "moves": moves,
        "counts": counts,
        "errors": errors,
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "target": target,
        "dry_run": dry_run,
    }


def undo_operation(log_file_path, dry_run=False):
    """Undo the last organization operation from log."""
    if not os.path.exists(log_file_path):
        print(f"Error: No log file found: {log_file_path}")
        return

    with open(log_file_path) as f:
        log = json.load(f)

    # Get latest operation
    if isinstance(log, list):
        ops = log
    else:
        ops = [log]

    latest = ops[-1] if ops else None
    if not latest:
        print("No operations to undo.")
        return

    moves = latest.get("moves", [])
    if not moves:
        print("No moves to undo.")
        return

    restored = 0
    for move in moves:
        orig = move["original"]
        new = move["new"]
        if os.path.exists(new):
            if not dry_run:
                os.makedirs(os.path.dirname(orig), exist_ok=True)
                shutil.move(new, orig)
            restored += 1
            print(f"  Restored: {Path(new).name} → {Path(orig).name}")
        else:
            print(f"  Skipped (not found): {os.path.basename(new)}")

    if not dry_run:
        # Remove category dirs if empty
        cats = set(m.get("category", "") for m in moves)
        for cat in cats:
            cat_dir = os.path.join(latest.get("target", ""), cat)
            if os.path.isdir(cat_dir) and not os.listdir(cat_dir):
                os.rmdir(cat_dir)

    print(f"Restored {restored} file(s).")
    return {"restored": restored, "timestamp": datetime.now().isoformat()}


def main():
    parser = argparse.ArgumentParser(description="Organize files into categorized folders")
    parser.add_argument("source", nargs="?", default="~/Downloads", help="Source directory")
    parser.add_argument("--target", default="~/organized-files", help="Target directory")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    parser.add_argument("--undo", action="store_true", help="Undo last operation")
    parser.add_argument("--undo-log", default="ORGANIZE_LOG.json", help="Undo log file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    config = load_config(args.config)

    if args.undo:
        result = undo_operation(args.undo_log, args.dry_run)
        if result and args.json:
            print(json.dumps(result, indent=2))
        elif not args.json:
            pass  # undo prints its own output
        return

    source_dirs = config.get("source_dirs", [args.source])
    target_base = args.target or config.get("target_base", "~/organized-files")

    # Expand ~
    source_dirs = expand_paths(source_dirs)
    target_base = expand_paths([target_base])[0]

    all_counts = {}
    all_moves = []
    all_errors = []

    for source in source_dirs:
        result = organize_directory(source, target_base, config, args.dry_run)
        if result:
            all_counts.update(result["counts"])
            all_moves.extend(result["moves"])
            all_errors.extend(result["errors"])

    # Log the operation (unless dry-run)
    if not args.dry_run and all_moves:
        log_path = os.path.join(os.path.abspath(target_base), args.undo_log)
        log_dir = os.path.dirname(log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # Load existing log and append
        existing = []
        if os.path.exists(log_path):
            try:
                with open(log_path) as f:
                    existing = json.load(f)
                if isinstance(existing, dict):
                    existing = [existing]
            except json.JSONDecodeError:
                existing = []

        operation = {
            "timestamp": datetime.now().isoformat(),
            "source": source_dirs,
            "target": target_base,
            "moves": all_moves,
            "counts": all_counts,
        }
        existing.append(operation)
        with open(log_path, "w") as f:
            json.dump(existing, f, indent=2)

    # Output
    output = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "counts": all_counts,
        "total_moves": len(all_moves),
        "errors": all_errors,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'DRY RUN' if args.dry_run else 'DONE'} — {len(source_dirs)} source(s)")
        for cat, count in sorted(all_counts.items()):
            print(f"  {cat:15s} {count:4d} files")
        if all_errors:
            print(f"\n  Errors ({len(all_errors)}):")
            for e in all_errors[:5]:
                print(f"    - {e['file']}: {e['reason']}")
            if len(all_errors) > 5:
                print(f"    ... and {len(all_errors) - 5} more")
        if not args.dry_run and all_moves:
            print(f"\n  Logged to: {os.path.join(target_base, args.undo_log)}")


if __name__ == "__main__":
    main()
