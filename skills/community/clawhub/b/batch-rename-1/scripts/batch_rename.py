"""
Batch File Rename Script

Provides powerful batch file renaming capabilities:
- Sequential numbering with customizable format
- Find and replace text in filenames
- Add prefix/suffix to filenames
- Regular expression pattern matching
- Extension filtering
- Recursive subfolder processing
"""

import os
import re
import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='Batch rename files with various patterns')
    parser.add_argument('--path', required=True, help='Target directory path')
    parser.add_argument('--pattern', required=True,
                        choices=['number', 'replace', 'prefix', 'suffix', 'regex'],
                        help='Rename pattern type')
    parser.add_argument('--format', help='Format string for numbering (e.g., "file_{n:03d}")')
    parser.add_argument('--find', help='Text to find for replacement')
    parser.add_argument('--replace', help='Replacement text')
    parser.add_argument('--prefix', help='Prefix to add')
    parser.add_argument('--suffix', help='Suffix to add')
    parser.add_argument('--regex', help='Regular expression pattern')
    parser.add_argument('--ext', default='*', help='File extension filter (default: *)')
    parser.add_argument('--recursive', action='store_true', help='Process subfolders recursively')
    return parser.parse_args()


def get_files(path, ext, recursive):
    """Get list of files matching the extension filter."""
    files = []
    ext_pattern = None

    if ext != '*':
        if ext.startswith('.'):
            ext_pattern = ext.lower()
        else:
            ext_pattern = f'.{ext.lower()}'

    if recursive:
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if ext_pattern:
                    if filename.lower().endswith(ext_pattern):
                        files.append((root, filename))
                else:
                    files.append((root, filename))
    else:
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                if ext_pattern:
                    if filename.lower().endswith(ext_pattern):
                        files.append((path, filename))
                else:
                    files.append((path, filename))

    return sorted(files)


def generate_new_name(filename, pattern, format_str, find, replace, prefix, suffix, regex_pattern, index):
    """Generate new filename based on the pattern."""
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    if pattern == 'number':
        if not format_str:
            format_str = 'file_{n}'
        try:
            new_name = format_str.format(n=index)
        except KeyError:
            # Handle format without n in braces
            new_name = format_str.replace('{n}', str(index)).replace('{n:03d}', f'{index:03d}')
        return new_name + ext

    elif pattern == 'replace':
        if find is None:
            print("Error: --find is required for replace pattern")
            return None
        new_name = name.replace(find, replace if replace is not None else '')
        return new_name + ext

    elif pattern == 'prefix':
        if prefix is None:
            print("Error: --prefix is required for prefix pattern")
            return None
        return f'{prefix}{name}{ext}'

    elif pattern == 'suffix':
        if suffix is None:
            print("Error: --suffix is required for suffix pattern")
            return None
        return f'{name}{suffix}{ext}'

    elif pattern == 'regex':
        if regex_pattern is None:
            print("Error: --regex is required for regex pattern")
            return None
        try:
            if replace is None:
                replace = ''
            new_name = re.sub(regex_pattern, replace, name)
            return new_name + ext
        except re.error as e:
            print(f"Error: Invalid regex pattern: {e}")
            return None

    return None


def batch_rename():
    """Main batch rename function."""
    args = parse_args()

    # Validate arguments
    if args.pattern == 'number' and not args.format:
        print("Warning: No format specified, using default 'file_{n}'")
        args.format = 'file_{n}'

    if args.pattern == 'replace' and not args.find:
        print("Error: --find is required for replace pattern")
        sys.exit(1)

    if args.pattern == 'prefix' and not args.prefix:
        print("Error: --prefix is required for prefix pattern")
        sys.exit(1)

    if args.pattern == 'suffix' and not args.suffix:
        print("Error: --suffix is required for suffix pattern")
        sys.exit(1)

    if args.pattern == 'regex' and not args.regex:
        print("Error: --regex is required for regex pattern")
        sys.exit(1)

    # Get files
    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(1)

    if not os.path.isdir(target_path):
        print(f"Error: Path is not a directory: {target_path}")
        sys.exit(1)

    files = get_files(target_path, args.ext, args.recursive)

    if not files:
        print(f"No files found matching criteria in: {target_path}")
        sys.exit(0)

    print(f"Found {len(files)} file(s) to rename")
    print("-" * 60)

    # Rename files
    success_count = 0
    error_count = 0
    skipped_count = 0
    results = []

    for index, (file_dir, filename) in enumerate(files, start=1):
        old_path = os.path.join(file_dir, filename)
        new_name = generate_new_name(
            filename, args.pattern, args.format,
            args.find, args.replace, args.prefix, args.suffix,
            args.regex, index
        )

        if new_name is None:
            error_count += 1
            continue

        new_path = os.path.join(file_dir, new_name)

        # Skip if name unchanged
        if new_name == filename:
            skipped_count += 1
            continue

        # Check if target already exists
        if os.path.exists(new_path):
            print(f"Skipped (exists): {filename} -> {new_name}")
            skipped_count += 1
            continue

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
            results.append((filename, new_name))
            success_count += 1
        except Exception as e:
            print(f"Error renaming {filename}: {e}")
            error_count += 1

    # Summary
    print("-" * 60)
    print(f"Summary:")
    print(f"  Successfully renamed: {success_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors: {error_count}")

    # Output JSON for programmatic use
    import json
    summary = {
        "success": success_count,
        "skipped": skipped_count,
        "errors": error_count,
        "results": results
    }
    print("\n[JSON_OUTPUT]")
    print(json.dumps(summary))


if __name__ == '__main__':
    batch_rename()
