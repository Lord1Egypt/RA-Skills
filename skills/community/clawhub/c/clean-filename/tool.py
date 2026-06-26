#!/usr/bin/env python3
import argparse
import os
import re
import sys

def clean_name(filename):
    """Clean a filename by removing or replacing invalid characters."""
    # Remove invalid characters for most filesystems (including Windows, macOS, Linux)
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', filename)
    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Strip leading/trailing spaces and dots
    cleaned = cleaned.strip('. ')
    # Prevent common reserved names on Windows
    reserved = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    name, ext = os.path.splitext(cleaned)
    if name.upper() in reserved:
        name = f"{name}_file"
    cleaned = f"{name}{ext}"
    # If name becomes empty, use placeholder
    if not cleaned:
        cleaned = "unnamed_file.txt"
    return cleaned

def rename_file(old_path, new_name):
    """Rename a file, handling conflicts by adding a number."""
    dir_name = os.path.dirname(old_path)
    new_path = os.path.join(dir_name, new_name)
    base, ext = os.path.splitext(new_name)
    counter = 1
    while os.path.exists(new_path) and new_path != old_path:
        new_name = f"{base}_{counter}{ext}"
        new_path = os.path.join(dir_name, new_name)
        counter += 1
    os.rename(old_path, new_path)
    return new_path

def main():
    parser = argparse.ArgumentParser(
        description="Clean filenames by removing invalid characters and normalizing format."
    )
    parser.add_argument('paths', nargs='+', help="File or directory paths to clean")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be renamed without changing files")
    parser.add_argument('--recursive', '-r', action='store_true', help="Process directories recursively")
    
    args = parser.parse_args()

    for path in args.paths:
        if not os.path.exists(path):
            print(f"Error: Path not found: {path}", file=sys.stderr)
            continue

        items = []
        if os.path.isdir(path) and args.recursive:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]  # Skip hidden dirs
                for file in files:
                    if not file.startswith('.'):  # Skip hidden files
                        items.append(os.path.join(root, file))
        elif os.path.isdir(path):
            for file in os.listdir(path):
                if file.startswith('.'):
                    continue
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    items.append(full_path)
        else:
            items.append(path)

        for item in items:
            old_name = os.path.basename(item)
            new_name = clean_name(old_name)
            if old_name == new_name:
                continue
            if args.dry_run:
                print(f"{item} -> {os.path.join(os.path.dirname(item), new_name)} (dry run)")
            else:
                new_path = rename_file(item, new_name)
                print(f"Renamed: {old_name} -> {os.path.basename(new_path)}")

if __name__ == '__main__':
    main()
