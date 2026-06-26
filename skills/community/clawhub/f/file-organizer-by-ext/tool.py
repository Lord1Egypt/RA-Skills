#!/usr/bin/env python3
"""
Simple CLI tool to organize files by their extension.
Moves files into subdirectories named by file extension.
"""
import os
import shutil
import argparse
from pathlib import Path

def organize_by_extension(directory):
    """Organize files in the given directory by file extension."""
    target_dir = Path(directory).resolve()
    if not target_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not target_dir.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    # Track moved files
    moved_files = []

    for item in target_dir.iterdir():
        if item.is_file():
            # Create subdirectory using lowercase extension
            ext = item.suffix[1:].lower() or 'no_ext'
            ext_dir = target_dir / ext
            ext_dir.mkdir(exist_ok=True)

            # Move file
            dest = ext_dir / item.name
            shutil.move(str(item), str(dest))
            moved_files.append(f"{item.name} -> {ext}/")

    return moved_files

def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their extension."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Path to the directory to organize (default: current directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show files that were moved"
    )

    args = parser.parse_args()

    try:
        moved = organize_by_extension(args.directory)
        if moved:
            print(f"Organized {len(moved)} files in '{args.directory}'.")
            if args.verbose:
                for move in moved:
                    print(f"  Moved: {move}")
        else:
            print(f"No files to organize in '{args.directory}'.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
