#!/usr/bin/env python3
import argparse
import os
import re
import sys

def clean_name(name):
    """Cleans a single filename by removing invalid chars and normalizing whitespace."""
    # Remove any characters not allowed in most filesystems
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)
    # Replace multiple spaces/tab with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Strip leading/trailing spaces and dots (avoid names ending with . or spaces)
    cleaned = cleaned.strip(' .')
    # Ensure at least one character remains
    if not cleaned:
        cleaned = "unnamed"
    return cleaned

def rename_file(path, new_name):
    """Renames a file safely, avoiding overwrites."""
    dir_name = os.path.dirname(path)
    new_path = os.path.join(dir_name, new_name) if dir_name else new_name

    if new_path == path:
        return False  # No change needed

    if os.path.exists(new_path):
        print(f"Conflict: {new_path} already exists. Skipping '{os.path.basename(path)}'.", file=sys.stderr)
        return False

    try:
        os.rename(path, new_path)
        print(f"Renamed: '{os.path.basename(path)}' → '{new_name}'")
        return True
    except OSError as e:
        print(f"Error renaming '{os.path.basename(path)}': {e}", file=sys.stderr)
        return False

def process_directory(directory, recursive=False):
    """Processes all files in the given directory."""
    count = 0
    for root, dirs, files in os.walk(directory):
        # Skip renaming directories for safety
        for file in files:
            orig_path = os.path.join(root, file)
            clean = clean_name(file)
            if clean != file:
                if rename_file(orig_path, clean):
                    count += 1
        if not recursive:
            break  # Only process top directory
    return count

def main():
    parser = argparse.ArgumentParser(
        description="Clean and sanitize filenames by removing invalid characters and normalizing formatting."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to process (default: current directory)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process directories recursively"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="clean-filenames 1.0.0"
    )

    args = parser.parse_args()

    if os.path.isfile(args.path):
        # Single file handling
        base = os.path.basename(args.path)
        clean = clean_name(base)
        if clean != base:
            rename_file(args.path, clean)
        else:
            print(f"No change needed: '{base}'")
    elif os.path.isdir(args.path):
        # Directory handling
        count = process_directory(args.path, recursive=args.recursive)
        print(f"Done. Cleaned {count} file name(s).", file=sys.stderr)
    else:
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
