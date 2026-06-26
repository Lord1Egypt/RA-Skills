import argparse
import os
import re
import sys

def clean_filename(filename):
    """
    Cleans a filename by removing common clutter:
    - Timestamps (e.g., 20230101, 2023-01-01, 12-30-2023)
    - Hex strings (e.g., a1b2c3d, 8f3e4d)
    - UUIDs and hashes (e.g., 550e8400-e29b-41d4-a716-446655440000)
    - Extra dashes, underscores, or dots used as separators
    Preserves file extension.
    """
    name, ext = os.path.splitext(filename)

    # Remove UUIDs
    name = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '', name, flags=re.I)
    # Remove timestamps like 20230101, 2023-01-01, 01-01-2023, etc.
    name = re.sub(r'\b(?:\d{4}[-_]?\d{2}[-_]?\d{2}|\d{2}[-_]?\d{2}[-_]?\d{4})\b', '', name)
    # Remove hex strings (4+ chars)
    name = re.sub(r'\b[0-9a-f]{4,}\b', '', name, flags=re.I)
    # Remove multiple dashes/underscores/dots used as separators
    name = re.sub(r'[-_\.]{2,}', ' ', name)
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    # Re-capitalize first letters if too many uppercase
    name = name.capitalize() if name.lower() == name else name

    # Reassemble, prevent empty names
    if not name:
        name = "file"

    return name + ext

def main():
    parser = argparse.ArgumentParser(
        description="Cleans filenames by removing dates, hashes, and clutter."
    )
    parser.add_argument('paths', nargs='+', help='Files or directories to clean')
    parser.add_argument('-r', '--rename', action='store_true',
                        help='Rename files on disk (default: preview only)')
    parser.add_argument('-s', '--skip-ext', nargs='*', default=[],
                        help='File extensions to skip, e.g. pdf jpg')

    args = parser.parse_args()

    skip_exts = [f".{ext.lower().strip('.')}" for ext in args.skip_ext]

    files_to_process = []
    for path in args.paths:
        if os.path.isdir(path):
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath):
                    files_to_process.append(filepath)
        elif os.path.isfile(path):
            files_to_process.append(path)

    changes = []
    for filepath in files_to_process:
        directory, filename = os.path.split(filepath)
        ext_lower = os.path.splitext(filename)[1].lower()

        if ext_lower in skip_exts:
            continue

        cleaned = clean_filename(filename)
        if cleaned != filename:
            changes.append((filepath, os.path.join(directory, cleaned)))

    if not changes:
        print("No filename changes detected.")
        sys.exit(0)

    print("Planned changes:")
    for old, new in changes:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)}")

    if args.rename:
        print("\nRenaming files...")
        for old, new in changes:
            os.rename(old, new)
            print(f"Renamed: {os.path.basename(old)} -> {os.path.basename(new)}")
        print("Done.")
    else:
        print(f"\nUse --rename to apply these changes. {len(changes)} file(s) would be renamed.")

if __name__ == "__main__":
    main()
