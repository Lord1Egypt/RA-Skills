#!/usr/bin/env python3
"""File hashing and integrity verification toolkit.

Compute, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and more.
No external dependencies — uses Python's built-in hashlib.
"""

import argparse
import hashlib
import os
import sys
import json


ALGORITHMS = sorted(hashlib.algorithms_guaranteed)
DEFAULT_ALGO = "sha256"
BUFFER_SIZE = 65536  # 64KB chunks


def hash_file(filepath, algo=DEFAULT_ALGO):
    """Compute hash of a file."""
    try:
        h = hashlib.new(algo)
    except ValueError:
        print(f"Unknown algorithm: '{algo}'. Available: {', '.join(ALGORITHMS)}", file=sys.stderr)
        return None
    try:
        with open(filepath, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                h.update(data)
        return h.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        return None
    except PermissionError:
        print(f"Permission denied: {filepath}", file=sys.stderr)
        return None
    except IsADirectoryError:
        print(f"Is a directory: {filepath}", file=sys.stderr)
        return None


def hash_string(text, algo=DEFAULT_ALGO):
    """Compute hash of a string."""
    try:
        h = hashlib.new(algo)
    except ValueError:
        print(f"Unknown algorithm: '{algo}'. Available: {', '.join(ALGORITHMS)}", file=sys.stderr)
        return None
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def cmd_hash(args):
    """Compute hash(es) of file(s)."""
    algo = args.algorithm or DEFAULT_ALGO
    algos = [a.strip() for a in algo.split(",")] if "," in algo else [algo]

    for filepath in args.files:
        for a in algos:
            digest = hash_file(filepath, a)
            if digest is None:
                return 1
            if args.json_output:
                print(json.dumps({"file": filepath, "algorithm": a, "hash": digest}))
            elif args.bsd:
                print(f"{a.upper()} ({filepath}) = {digest}")
            else:
                print(f"{digest}  {filepath}")
    return 0


def cmd_verify(args):
    """Verify a file against an expected hash."""
    algo = args.algorithm or DEFAULT_ALGO
    filepath = args.file
    expected = args.expected.strip().lower()

    digest = hash_file(filepath, algo)
    if digest is None:
        return 1

    if digest == expected:
        print(f"✓ MATCH  {filepath}")
        print(f"  {algo}: {digest}")
        return 0
    else:
        print(f"✗ MISMATCH  {filepath}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {digest}")
        return 1


def cmd_check(args):
    """Verify files against a checksum file (sha256sum/md5sum format)."""
    algo = args.algorithm or None
    errors = 0
    checked = 0

    try:
        with open(args.checksum_file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Checksum file not found: {args.checksum_file}", file=sys.stderr)
        return 1

    base_dir = os.path.dirname(args.checksum_file) or "."

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # BSD format: ALGO (file) = hash
        if "(" in line and ") = " in line:
            algo_part = line.split("(")[0].strip()
            file_part = line.split("(")[1].split(")")[0]
            hash_part = line.split(" = ")[1].strip()
            use_algo = algo or algo_part.lower()
        else:
            # Standard format: hash  filename  (or hash *filename)
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            hash_part = parts[0]
            file_part = parts[1].lstrip("*").strip()
            # Infer algo from hash length
            if algo:
                use_algo = algo
            else:
                hash_len = len(hash_part)
                algo_map = {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}
                use_algo = algo_map.get(hash_len, DEFAULT_ALGO)

        # Resolve relative paths
        if not os.path.isabs(file_part):
            file_part = os.path.join(base_dir, file_part)

        digest = hash_file(file_part, use_algo)
        checked += 1
        if digest is None:
            errors += 1
            continue

        if digest == hash_part.lower():
            print(f"✓ {os.path.basename(file_part)}")
        else:
            print(f"✗ {os.path.basename(file_part)}  (MISMATCH)")
            errors += 1

    print(f"\n{checked} file(s) checked, {errors} error(s).")
    return 1 if errors > 0 else 0


def cmd_compare(args):
    """Compare hashes of two files."""
    algo = args.algorithm or DEFAULT_ALGO
    h1 = hash_file(args.file1, algo)
    h2 = hash_file(args.file2, algo)
    if h1 is None or h2 is None:
        return 1

    print(f"File 1: {args.file1}")
    print(f"  {algo}: {h1}")
    print(f"File 2: {args.file2}")
    print(f"  {algo}: {h2}")
    print()
    if h1 == h2:
        print("✓ Files are IDENTICAL")
        return 0
    else:
        print("✗ Files are DIFFERENT")
        return 1


def cmd_directory(args):
    """Hash all files in a directory."""
    algo = args.algorithm or DEFAULT_ALGO
    directory = args.directory
    recursive = args.recursive

    if not os.path.isdir(directory):
        print(f"Not a directory: {directory}", file=sys.stderr)
        return 1

    results = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            for fname in sorted(files):
                fpath = os.path.join(root, fname)
                digest = hash_file(fpath, algo)
                if digest:
                    rel = os.path.relpath(fpath, directory)
                    results.append((digest, rel))
    else:
        for fname in sorted(os.listdir(directory)):
            fpath = os.path.join(directory, fname)
            if os.path.isfile(fpath):
                digest = hash_file(fpath, algo)
                if digest:
                    results.append((digest, fname))

    for digest, name in results:
        if args.bsd:
            print(f"{algo.upper()} ({name}) = {digest}")
        else:
            print(f"{digest}  {name}")

    print(f"\n{len(results)} file(s) hashed with {algo}.", file=sys.stderr)
    return 0


def cmd_string(args):
    """Hash a string."""
    algo = args.algorithm or DEFAULT_ALGO
    algos = [a.strip() for a in algo.split(",")] if "," in algo else [algo]

    for a in algos:
        digest = hash_string(args.text, a)
        if digest is None:
            return 1
        print(f"{a:10s}  {digest}")
    return 0


def cmd_algorithms(args):
    """List available hash algorithms."""
    print("Available algorithms:")
    for a in ALGORITHMS:
        print(f"  {a}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="File hashing and integrity verification toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s hash file.txt                           # SHA-256 hash
  %(prog)s hash file.txt -a md5,sha1,sha256        # Multiple algos
  %(prog)s hash *.py --bsd                         # BSD format output
  %(prog)s verify file.txt -e abc123...            # Verify hash
  %(prog)s check SHA256SUMS                        # Check from file
  %(prog)s compare file1.txt file2.txt             # Compare two files
  %(prog)s directory ./src -r                      # Hash all files recursively
  %(prog)s string "hello world" -a sha256,md5      # Hash a string
  %(prog)s algorithms                              # List algorithms
""",
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # hash
    p_hash = sub.add_parser("hash", help="Compute file hash(es)")
    p_hash.add_argument("files", nargs="+", help="Files to hash")
    p_hash.add_argument("-a", "--algorithm", help=f"Algorithm(s), comma-separated (default: {DEFAULT_ALGO})")
    p_hash.add_argument("--bsd", action="store_true", help="BSD-style output")
    p_hash.add_argument("--json", dest="json_output", action="store_true", help="JSON output")

    # verify
    p_verify = sub.add_parser("verify", help="Verify file against expected hash")
    p_verify.add_argument("file", help="File to verify")
    p_verify.add_argument("-e", "--expected", required=True, help="Expected hash")
    p_verify.add_argument("-a", "--algorithm", help=f"Algorithm (default: {DEFAULT_ALGO})")

    # check
    p_check = sub.add_parser("check", help="Verify files from a checksum file")
    p_check.add_argument("checksum_file", help="Checksum file (sha256sum/md5sum format)")
    p_check.add_argument("-a", "--algorithm", help="Override algorithm detection")

    # compare
    p_comp = sub.add_parser("compare", help="Compare two files by hash")
    p_comp.add_argument("file1", help="First file")
    p_comp.add_argument("file2", help="Second file")
    p_comp.add_argument("-a", "--algorithm", help=f"Algorithm (default: {DEFAULT_ALGO})")

    # directory
    p_dir = sub.add_parser("directory", help="Hash all files in a directory")
    p_dir.add_argument("directory", help="Directory to hash")
    p_dir.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories")
    p_dir.add_argument("-a", "--algorithm", help=f"Algorithm (default: {DEFAULT_ALGO})")
    p_dir.add_argument("--bsd", action="store_true", help="BSD-style output")

    # string
    p_str = sub.add_parser("string", help="Hash a text string")
    p_str.add_argument("text", help="Text to hash")
    p_str.add_argument("-a", "--algorithm", help=f"Algorithm(s), comma-separated (default: {DEFAULT_ALGO})")

    # algorithms
    sub.add_parser("algorithms", help="List available hash algorithms")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    cmds = {
        "hash": cmd_hash,
        "verify": cmd_verify,
        "check": cmd_check,
        "compare": cmd_compare,
        "directory": cmd_directory,
        "string": cmd_string,
        "algorithms": cmd_algorithms,
    }
    return cmds[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
