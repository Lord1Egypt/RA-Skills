#!/usr/bin/env python3
"""
File Organizer - automatically organizes files from a downloads directory
"""

import os
import sys
import json
import shutil
import argparse
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# Paths
SKILL_DIR = Path.home() / ".claude" / "skills" / "organize"
CONFIG_FILE = SKILL_DIR / "config.json"
LOGS_DIR = SKILL_DIR / "logs"
INDEX_FILE = SKILL_DIR / "index.md"

RULES = []

EXTENSION_FALLBACKS = []

IGNORED_FILENAMES = ["desktop.ini", "thumbs.db", ".ds_store"]
IGNORED_PREFIXES = [".", "$"]
SKIP_DIRS = [
    ".git", "venv", ".venv", "node_modules", "__pycache__",
    ".conda", ".idea", ".ipynb_checkpoints", "Replays",
]


# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────

def load_config() -> Optional[Dict]:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_config(config: Dict):
    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def setup_config():
    print("=== File Organizer Setup ===\n")

    target_root = input("Target root directory (default: ~/Documents): ").strip()
    target_root = str(Path(target_root or "~/Documents").expanduser())

    downloads_dir = input("Downloads directory (default: ~/Downloads): ").strip()
    downloads_dir = str(Path(downloads_dir or "~/Downloads").expanduser())

    config = {
        "target_root": target_root,
        "downloads_dir": downloads_dir,
        "rules": RULES,
        "extension_fallbacks": EXTENSION_FALLBACKS,
        "ignored_filenames": IGNORED_FILENAMES,
        "ignored_prefixes": IGNORED_PREFIXES,
        "skip_dirs": SKIP_DIRS,
    }
    save_config(config)
    print(f"\nConfig saved: {CONFIG_FILE}")
    return config


# ──────────────────────────────────────────────
# Classification
# ──────────────────────────────────────────────

def is_gibberish(name: str) -> bool:
    """Return True if the filename stem looks like random/meaningless characters."""
    stem = Path(name).stem
    if re.fullmatch(r'[0-9a-fA-F\-_]{6,}', stem):   # hex/uuid-like
        return True
    if re.fullmatch(r'[\d\-_\.]+', stem):             # all digits/dashes
        return True
    if len(stem) <= 3 and not re.search(r'[\u4e00-\u9fff]', stem):
        return True
    return False


def read_content_preview(filepath: Path, max_bytes: int = 2048) -> str:
    """Try to extract readable text from a file for classification."""
    ext = filepath.suffix.lower()
    try:
        if ext in {'.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm'}:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(max_bytes)

        # Use `strings` for binary/PDF files
        import subprocess
        result = subprocess.run(
            ['strings', str(filepath)],
            capture_output=True, text=True, timeout=5
        )
        readable = ' '.join(
            s for s in result.stdout.splitlines()
            if len(s) > 3 and re.search(r'[a-zA-Z\u4e00-\u9fff]', s)
        )
        return readable[:max_bytes]
    except Exception:
        return ""


def match_rules(text: str, rules: List[Dict]) -> Tuple[int, Optional[Dict]]:
    best_score, best_rule = 0, None
    text_lower = text.lower()
    for rule in rules:
        score = 0
        for kw in rule["keywords"]:
            kw_lower = kw.lower()
            if kw_lower not in text_lower:
                continue
            # Short keywords (<=4 chars) must match as whole word to avoid false positives
            # e.g. "ead" matching "readme", "visa" matching "revision"
            if len(kw_lower) <= 4:
                if not re.search(r'(?<![a-z])' + re.escape(kw_lower) + r'(?![a-z])', text_lower):
                    continue
            score += len(kw_lower)
        if score > best_score:
            best_score, best_rule = score, rule
    return best_score, best_rule


def classify_by_extension(ext: str, extension_fallbacks: List[Dict]) -> Tuple[str, str]:
    for entry in extension_fallbacks:
        if ext in entry["extensions"]:
            return entry["target"], entry["reason"]
    return "Others", "Uncategorized"


def classify_file(filepath: Path, config: Dict) -> Dict:
    rules = config.get("rules", RULES)
    extension_fallbacks = config.get("extension_fallbacks", EXTENSION_FALLBACKS)
    filename = filepath.name

    # Round 1: match against full filename
    score, rule = match_rules(filename, rules)

    # Round 2: if gibberish name and no match, try reading content
    if score == 0 and is_gibberish(filename):
        content = read_content_preview(filepath)
        if content:
            score, rule = match_rules(content, rules)

    if rule:
        target_subdir = rule["target"]
        reason = rule["reason"]
    else:
        target_subdir, reason = classify_by_extension(filepath.suffix.lower(), extension_fallbacks)

    target_root = Path(config["target_root"])
    target_dir = target_root / target_subdir

    return {
        "source": str(filepath),
        "filename": filename,
        "target_subdir": target_subdir,
        "target_dir": str(target_dir),
        "reason": reason,
    }


# ──────────────────────────────────────────────
# Conflict resolution
# ──────────────────────────────────────────────

def resolve_conflict(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path
    stem, suffix, parent = target_path.stem, target_path.suffix, target_path.parent
    for i in range(1, 1000):
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Too many conflicts for {target_path.name}")


# ──────────────────────────────────────────────
# Scan
# ──────────────────────────────────────────────

def scan_downloads(config: Dict) -> List[Dict]:
    downloads_dir = Path(config["downloads_dir"])
    if not downloads_dir.exists():
        return []

    ignored_filenames = {f.lower() for f in config.get("ignored_filenames", IGNORED_FILENAMES)}
    ignored_prefixes = tuple(config.get("ignored_prefixes", IGNORED_PREFIXES))

    plan = []
    for item in sorted(downloads_dir.iterdir()):
        if item.name.lower() in ignored_filenames or item.name.startswith(ignored_prefixes) or not item.is_file():
            continue
        info = classify_file(item, config)
        final_path = resolve_conflict(Path(info["target_dir"]) / item.name)
        info["final_target"] = str(final_path)
        info["renamed"] = final_path.name != item.name
        plan.append(info)
    return plan


# ──────────────────────────────────────────────
# Execute
# ──────────────────────────────────────────────

def execute_plan(plan: List[Dict]) -> Dict:
    results = {"moved": [], "errors": []}
    log_lines = [f"# Organize log {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]

    for item in plan:
        source = Path(item["source"])
        target = Path(item["final_target"])
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            results["moved"].append({"from": str(source), "to": str(target)})
            log_lines.append(f"[OK] {source.name}  →  {item['target_subdir']}/{target.name}")
        except Exception as e:
            results["errors"].append({"file": str(source), "error": str(e)})
            log_lines.append(f"[ERR] {source.name}  →  {e}")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n\n")

    return results


# ──────────────────────────────────────────────
# Index
# ──────────────────────────────────────────────

def update_index(config: Dict):
    target_root = Path(config["target_root"])
    skip_dirs = set(config.get("skip_dirs", SKIP_DIRS))
    lines = [
        "# File Directory Index",
        f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]

    for root, dirs, files in os.walk(target_root):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d not in skip_dirs)
        rel = Path(root).relative_to(target_root)
        depth = len(rel.parts)
        indent = "  " * depth
        folder_name = Path(root).name if depth > 0 else target_root.name
        lines.append(f"{indent}- **{folder_name}/**")
        for filename in sorted(files):
            if not filename.startswith('.'):
                lines.append(f"{'  ' * (depth + 1)}- {filename}")

    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Index updated: {INDEX_FILE}")


# ──────────────────────────────────────────────
# Watch mode
# ──────────────────────────────────────────────

def watch_mode(config: Dict):
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Please install watchdog first: pip install watchdog", file=sys.stderr)
        sys.exit(1)

    ignored_filenames = {f.lower() for f in config.get("ignored_filenames", IGNORED_FILENAMES)}
    ignored_prefixes = tuple(config.get("ignored_prefixes", IGNORED_PREFIXES))

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            filepath = Path(event.src_path)
            if filepath.name.lower() in ignored_filenames or filepath.name.startswith(ignored_prefixes):
                return
            time.sleep(2)  # wait for download to finish
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] New file: {filepath.name}")
            info = classify_file(filepath, config)
            final_path = resolve_conflict(Path(info["target_dir"]) / filepath.name)
            info["final_target"] = str(final_path)
            results = execute_plan([info])
            if results["moved"]:
                print(f"  Moved → {info['target_subdir']}/")
                update_index(config)
            elif results["errors"]:
                print(f"  Error: {results['errors'][0]['error']}")

    observer = Observer()
    observer.schedule(Handler(), config["downloads_dir"], recursive=False)
    observer.start()
    print(f"Watching: {config['downloads_dir']}\nPress Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped")
    observer.join()


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("--setup", action="store_true", help="Initialize configuration")
    parser.add_argument("--scan", action="store_true", help="Scan downloads directory, output JSON plan")
    parser.add_argument("--execute", type=str, metavar="JSON", help="Execute plan (pass JSON string)")
    parser.add_argument("--watch", action="store_true", help="Watch mode")
    parser.add_argument("--update-index", action="store_true", help="Update file index only")
    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    config = load_config()
    if config is None:
        print(json.dumps({"error": "config_missing"}))
        return

    if args.scan:
        plan = scan_downloads(config)
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    if args.execute:
        plan = json.loads(args.execute)
        results = execute_plan(plan)
        update_index(config)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args.watch:
        watch_mode(config)
        return

    if args.update_index:
        update_index(config)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
