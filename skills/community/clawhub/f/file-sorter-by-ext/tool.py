#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path

def sort_files_by_extension(directory):
    """Sorts files in the given directory into subdirectories by file extension."""
    path = Path(directory)
    if not path.is_dir():
        print(f"Error: '{directory}' is not a valid directory.")
        return

    for file_path in path.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower().lstrip('.')
            if not ext:  # Handle files without extension
                ext = "no_extension"
            target_dir = path / ext
            target_dir.mkdir(exist_ok=True)
            try:
                shutil.move(str(file_path), str(target_dir / file_path.name))
                print(f"Moved: {file_path.name} -> {ext}/")
            except Exception as e:
                print(f"Failed to move {file_path.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sort files in a directory by their extension.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to sort (default: current directory)")
    args = parser.parse_args()
    sort_files_by_extension(args.directory)

if __name__ == "__main__":
    main()
