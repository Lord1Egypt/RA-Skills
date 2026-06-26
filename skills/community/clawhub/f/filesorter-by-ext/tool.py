#!/usr/bin/env python3
"""
Sorts files in a directory into subdirectories grouped by file extension.
"""
import os
import shutil
import argparse
from pathlib import Path

def sort_files_by_extension(directory: Path):
    """Organize files in the given directory into subfolders by extension."""
    directory = directory.resolve()
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a valid directory.")
    
    # Track moved files and created folders
    moved_files = 0
    extensions = set()

    for item in directory.iterdir():
        if item.is_file():
            ext = item.suffix[1:].lower() or "no_ext"
            extensions.add(ext)
            target_dir = directory / ext
            target_dir.mkdir(exist_ok=True)
            target_path = target_dir / item.name

            # Handle filename conflicts
            counter = 1
            while target_path.exists():
                name_stem = item.stem
                name_suffix = item.suffix
                target_path = target_dir / f"{name_stem}_{counter}{name_suffix}"
                counter += 1

            shutil.move(str(item), str(target_path))
            moved_files += 1

    return moved_files, len(extensions)

def main():
    parser = argparse.ArgumentParser(
        description="Organize files into folders by their extension."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory path to organize (default: current directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed summary after sorting"
    )

    args = parser.parse_args()
    target_path = Path(args.path)

    try:
        moved, folders = sort_files_by_extension(target_path)
        print(f"✓ Organized {moved} file(s) into {folders} extension-based folder(s).")
        if args.verbose:
            print(f"📁 Target location: {target_path.resolve()}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
