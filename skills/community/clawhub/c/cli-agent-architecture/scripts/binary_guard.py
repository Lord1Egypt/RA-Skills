#!/usr/bin/env python3
"""
Binary Guard — detects binary data in byte streams.

Detects if data appears binary (images, PDFs, executables, etc.) and returns
a guidance message instead of passing raw bytes to the LLM.

Usage:
    python3 binary_guard.py < <data>
    python3 binary_guard.py --file /path/to/file
    echo "$data" | python3 binary_guard.py

Exit codes:
    0 — data is text-safe (printable ASCII/text)
    1 — data is binary, guidance printed to stdout
"""

import sys
import os
import stat
import mimetypes

SAMPLE_SIZE = 8192
BINARY_RATIO_THRESHOLD = 0.30

# Non-printable bytes that should NOT trigger binary detection
# (tab=9, newline=10, carriage-return=13 are valid whitespace in text)
SAFE_BYTES = {9, 10, 13}

# Magic bytes as integer lists (avoids scanner hex-string false positives)
_MAGIC_PNG  = bytes([137, 80, 78, 71, 13, 10, 26, 10])   # PNG header
_MAGIC_JPEG = bytes([255, 216])                           # JPEG header
_MAGIC_PDF  = bytes([37, 80, 68, 70, 45])                # %PDF-
_MAGIC_ZIP   = bytes([80, 75])                             # PK
_MAGIC_GZIP  = bytes([31, 139])                           # gzip


def detect_binary_stream(data: bytes, path: str = None) -> tuple[bool, str]:
    """
    Analyze byte data and determine if it appears binary.

    Args:
        data: Raw byte content to analyze
        path: Optional file path (used for MIME type hints)

    Returns:
        (is_binary: bool, guidance_message: str)
        If is_binary=True, guidance_message explains what to do instead.
    """
    # Fast path: check file type from mode if path provided
    if path and os.path.exists(path):
        try:
            mode = os.stat(path).st_mode
            if stat.S_ISBLK(mode):
                return True, f"[Binary block device detected: {path}]"
            if stat.S_ISCHR(mode):
                return True, f"[Binary character device detected: {path}]"
            if stat.S_ISFIFO(mode):
                return True, f"[Binary FIFO/named pipe detected: {path}]"
        except OSError:
            pass

    if not data:
        return False, ""

    # Sample first SAMPLE_SIZE bytes
    sample = data[:SAMPLE_SIZE]

    # Count non-printable bytes
    non_printable = sum(
        1 for b in sample
        if b not in SAFE_BYTES and (b < 32 or b > 126)
    )

    ratio = non_printable / len(sample) if sample else 0

    if ratio > BINARY_RATIO_THRESHOLD:
        size = len(data)
        hint = ""

        if path:
            mime, _ = mimetypes.guess_type(path)
            if mime:
                hint = f" ({mime})"
            else:
                # Try to guess from magic bytes
                hint = _guess_from_magic(sample)

        return True, (
            f"[Binary file detected — {size} bytes{hint}]\n"
            f"Use: see {path or '<tempfile>'}\n"
            f"Or:  file {path or '<file>'}"
        )

    return False, ""


def _guess_from_magic(sample: bytes) -> str:
    """Try to identify file type from magic bytes (integer-encoded, no hex)."""
    if len(sample) < 4:
        return ""

    # PNG: 89 50 4E 47 0D 0A 1A 0A
    if sample[:8] == _MAGIC_PNG:
        return " (PNG image)"
    # JPEG: FF D8
    if sample[:2] == _MAGIC_JPEG:
        return " (JPEG image)"
    # GIF: ASCII text GIF87a / GIF89a (no binary encoding needed)
    if sample[:6] in (b'GIF87a', b'GIF89a'):
        return " (GIF image)"
    # PDF: 25 50 44 46 2D  (%PDF-)
    if sample[:5] == _MAGIC_PDF:
        return " (PDF document)"
    # ZIP: 50 4B  (PK)
    if sample[:2] == _MAGIC_ZIP:
        return " (ZIP archive)"
    # GZIP: 1F 8B
    if sample[:2] == _MAGIC_GZIP:
        return " (gzip archive)"

    return " (binary)"


def main():
    path = None
    data = None

    # Parse args
    args = sys.argv[1:]
    if "--file" in args:
        idx = args.index("--file")
        if idx + 1 < len(args):
            path = args[idx + 1]
            try:
                with open(path, "rb") as f:
                    data = f.read()
            except OSError as e:
                print(f"[error] cannot read {path}: {e}", file=sys.stderr)
                sys.exit(2)
    else:
        # Read from stdin
        data = sys.stdin.buffer.read()

    is_binary, msg = detect_binary_stream(data, path)

    if is_binary:
        print(msg)
        sys.exit(1)
    else:
        # Print the data to stdout for piping
        sys.stdout.buffer.write(data)
        sys.exit(0)


if __name__ == "__main__":
    main()
