#!/usr/bin/env python3
"""Utilities for handling secret material with restrictive permissions."""

import base64
import os
import sys
import tempfile


def secure_zero(buf: bytearray) -> None:
    """Best-effort in-place zeroing for mutable secret buffers."""
    for index in range(len(buf)):
        buf[index] = 0


def to_secure_buffer(data: bytes | str) -> bytearray:
    """Copy bytes or text into a mutable buffer that can be zeroed later."""
    raw = data.encode() if isinstance(data, str) else bytes(data)
    return bytearray(raw)


def atomic_write(path: str, content: bytes | str, mode: int = 0o600) -> None:
    """Atomically write content by replacing destination with a temp file."""
    data = content.encode() if isinstance(content, str) else content
    directory = os.path.dirname(path) or "."
    dir_fd = os.open(directory, os.O_RDONLY)
    fd = None
    temp_path = None
    try:
        fd, temp_path = tempfile.mkstemp(prefix=".tmp-", dir=directory)
        os.fchmod(fd, mode)
        total_written = 0
        while total_written < len(data):
            written = os.write(fd, data[total_written:])
            if written == 0:
                raise OSError(f"Short write while writing file: {path}")
            total_written += written
        os.fsync(fd)
        os.replace(temp_path, path)
        os.fsync(dir_fd)
    except Exception:
        if fd is not None:
            os.close(fd)
            fd = None
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
    finally:
        if fd is not None:
            os.close(fd)
        os.close(dir_fd)


def atomic_write_new(path: str, content: bytes | str, mode: int = 0o600) -> None:
    """Create a new file atomically; fail with FileExistsError if destination exists."""
    data = content.encode() if isinstance(content, str) else content
    directory = os.path.dirname(path) or "."
    dir_fd = os.open(directory, os.O_RDONLY)
    fd = None
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(path, flags, mode)
        total_written = 0
        while total_written < len(data):
            written = os.write(fd, data[total_written:])
            if written == 0:
                raise OSError(f"Short write while creating file: {path}")
            total_written += written
        os.fsync(fd)
        os.fsync(dir_fd)
    finally:
        if fd is not None:
            os.close(fd)
        os.close(dir_fd)


def write_secret_file(path: str, content: str | bytes, mode: int = 0o600) -> None:
    """Write secret content to a file with restrictive permissions."""
    atomic_write(path, content, mode=mode)


def validate_challenge(challenge: str) -> None:
    """Validate that challenge is a well-formed base64url-encoded value.

    Accepts standard base64url with or without padding.
    Decoded length must be 16–128 bytes.

    Raises SystemExit with a descriptive error on failure.
    """
    try:
        # Add padding if missing
        padded = challenge + "=" * (-len(challenge) % 4)
        decoded = base64.urlsafe_b64decode(padded)
    except Exception:
        print(f"Error: challenge is not valid base64url: {challenge!r}", file=sys.stderr)
        sys.exit(1)
    if len(decoded) < 16:
        print(
            f"Error: challenge too short ({len(decoded)} bytes decoded, minimum 16)",
            file=sys.stderr,
        )
        sys.exit(1)
    if len(decoded) > 128:
        print(
            f"Error: challenge too long ({len(decoded)} bytes decoded, maximum 128)",
            file=sys.stderr,
        )
        sys.exit(1)


def resolve_api_base(default: str = "https://agent-id.io/v1") -> str:
    """Resolve the API base URL, enforcing HTTPS.

    Reads AGENT_ID_API environment variable. Rejects non-HTTPS URLs with
    a clear error message to prevent TLS downgrade attacks.
    """
    url = os.environ.get("AGENT_ID_API", default).rstrip("/")
    if not url.startswith("https://"):
        print(
            f"Error: AGENT_ID_API must use https:// (got {url!r}). "
            "HTTP connections expose credentials in transit.",
            file=sys.stderr,
        )
        sys.exit(1)
    return url
