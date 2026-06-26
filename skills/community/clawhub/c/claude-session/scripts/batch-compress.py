#!/usr/bin/env python3
"""Batch dedup script for JSONL files at arbitrary paths to reduce session file sizes

Usage:
    python batch-compress.py <path>                    # Recursively find *.jsonl in path + dedup
    python batch-compress.py <path> --dry-run          # Print expected results without making changes
    python batch-compress.py <path> --clean-orig       # Also clean up .orig.jsonl files
    python batch-compress.py <path> --clean-proj       # Also clean up .proj.jsonl files
"""

import os
import sys
import importlib.util
from pathlib import Path


def load_dedup_session():
    """Import dedup_session function from dedup-session.py in the same directory"""
    script_dir = Path(__file__).parent
    dedup_path = script_dir / 'dedup-session.py'

    if not dedup_path.exists():
        print(f"Error: {dedup_path} not found", file=sys.stderr)
        sys.exit(1)

    spec = importlib.util.spec_from_file_location('dedup_session_mod', dedup_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.dedup_session


def format_size(size_bytes: int) -> str:
    """Convert bytes to a human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f}MB"


def collect_jsonl_files(root: Path) -> list[Path]:
    """Recursively find all .jsonl files in path (excluding .orig.jsonl, .proj.jsonl, .dedup)"""
    files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.jsonl') and not (
                fname.endswith('.orig.jsonl') or fname.endswith('.proj.jsonl')
            ):
                files.append(Path(dirpath) / fname)
    return files


def clean_orig_files(root: Path, dry_run: bool) -> tuple[int, int]:
    """
    Clean up .orig.jsonl files:
    - Delete if corresponding .jsonl exists
    - Rename to .jsonl if no corresponding .jsonl exists (.orig.jsonl -> .jsonl)

    Returns: (deleted, renamed)
    """
    deleted = 0
    renamed = 0

    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith('.orig.jsonl'):
                continue
            orig_path = Path(dirpath) / fname
            # Compute corresponding .jsonl path from .orig.jsonl
            base_name = fname[: -len('.orig.jsonl')] + '.jsonl'
            jsonl_path = Path(dirpath) / base_name

            if jsonl_path.exists():
                print(f"  [orig] delete: {orig_path}")
                if not dry_run:
                    orig_path.unlink()
                deleted += 1
            else:
                print(f"  [orig] rename: {orig_path} -> {jsonl_path}")
                if not dry_run:
                    orig_path.rename(jsonl_path)
                renamed += 1

    return deleted, renamed


def clean_proj_files(root: Path, dry_run: bool) -> int:
    """
    Clean up .proj.jsonl files:
    - Delete if corresponding .jsonl exists

    Returns: deleted count
    """
    deleted = 0

    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith('.proj.jsonl'):
                continue
            proj_path = Path(dirpath) / fname
            base_name = fname[: -len('.proj.jsonl')] + '.jsonl'
            jsonl_path = Path(dirpath) / base_name

            if jsonl_path.exists():
                print(f"  [proj] delete: {proj_path}")
                if not dry_run:
                    proj_path.unlink()
                deleted += 1

    return deleted


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    root = Path(sys.argv[1])
    if not root.exists():
        print(f"Error: {root} path does not exist", file=sys.stderr)
        sys.exit(1)

    dry_run = '--dry-run' in sys.argv
    clean_orig = '--clean-orig' in sys.argv
    clean_proj = '--clean-proj' in sys.argv

    if dry_run:
        print("=== DRY RUN mode (no file changes) ===\n")

    dedup_session = load_dedup_session()

    # Step 1: clean up .orig.jsonl
    if clean_orig:
        print("--- cleaning .orig.jsonl ---")
        orig_deleted, orig_renamed = clean_orig_files(root, dry_run)
        print(f"  deleted: {orig_deleted}, renamed: {orig_renamed}\n")

    # Step 2: clean up .proj.jsonl
    if clean_proj:
        print("--- cleaning .proj.jsonl ---")
        proj_deleted = clean_proj_files(root, dry_run)
        print(f"  deleted: {proj_deleted}\n")

    # Step 3: collect .jsonl files and sort by size descending (largest first)
    jsonl_files = collect_jsonl_files(root)
    jsonl_files.sort(key=lambda p: p.stat().st_size, reverse=True)

    total = len(jsonl_files)
    if total == 0:
        print("No .jsonl files to process.")
        return

    print(f"--- dedup processing: {total} files ---")

    changed = 0
    errors = 0
    total_before = 0
    total_after = 0

    for i, jsonl_path in enumerate(jsonl_files, 1):
        if i % 50 == 0:
            print(f"  progress: {i}/{total} ({changed} changed, {errors} errors)")

        file_size = jsonl_path.stat().st_size
        total_before += file_size

        try:
            result = dedup_session(jsonl_path, dry_run=dry_run)

            orig_lines = result['original_lines']
            unique_lines = result['unique_lines']
            removed = orig_lines - unique_lines

            if not dry_run and 'output_file' in result:
                dedup_path = Path(result['output_file'])
                after_size = dedup_path.stat().st_size
                total_after += after_size

                if removed > 0:
                    os.replace(dedup_path, jsonl_path)
                    changed += 1
                    print(
                        f"  changed: {jsonl_path.name}"
                        f" ({orig_lines}->{unique_lines} lines,"
                        f" {format_size(file_size)}->{format_size(after_size)})"
                    )
                else:
                    dedup_path.unlink()
                    total_after = total_after - after_size + file_size
            else:
                # dry-run: estimate savings by line ratio
                if removed > 0 and orig_lines > 0:
                    estimated_after = int(file_size * unique_lines / orig_lines)
                    changed += 1
                    print(
                        f"  [estimated change] {jsonl_path.name}"
                        f" ({orig_lines}->{unique_lines} lines, -{removed} lines,"
                        f" ~{format_size(file_size - estimated_after)} estimated savings)"
                    )
                else:
                    estimated_after = file_size
                total_after += estimated_after

        except Exception as e:
            errors += 1
            total_after += file_size
            print(f"  error: {jsonl_path.name} -- {e}", file=sys.stderr)

    # Summary
    saved = total_before - total_after
    ratio = (saved / total_before * 100) if total_before > 0 else 0.0

    print(f"\n{'=== Summary (DRY RUN) ===' if dry_run else '=== Summary ==='}")
    print(f"  total files:   {total}")
    print(f"  changed files: {changed}")
    print(f"  errors:        {errors}")
    print(f"  before:        {format_size(total_before)}")
    print(f"  after:         {format_size(total_after)}")
    print(f"  saved:         {format_size(saved)} ({ratio:.1f}%)")


if __name__ == '__main__':
    main()
