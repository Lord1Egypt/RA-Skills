"""Bounded, versioned JSON plus binary IPC for the PDFium worker."""

from __future__ import annotations

import json
import os
import select
import struct
import time
from typing import Any, BinaryIO


PROTOCOL_VERSION = 1
MAX_HEADER_BYTES = 64 * 1024
_LENGTH = struct.Struct(">I")


class IPCError(RuntimeError):
    pass


def canonical_header(value: dict[str, Any]) -> bytes:
    data = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")
    if len(data) > MAX_HEADER_BYTES:
        raise IPCError("IPC header exceeds configured limit")
    return _LENGTH.pack(len(data)) + data


def write_frame(stream: BinaryIO, value: dict[str, Any], payload: bytes = b"") -> None:
    stream.write(canonical_header(value))
    if payload:
        stream.write(payload)
    stream.flush()


def read_frame(stream: BinaryIO, *, max_payload: int) -> tuple[dict[str, Any], bytes]:
    prefix = stream.read(_LENGTH.size)
    if len(prefix) != _LENGTH.size:
        raise IPCError("truncated IPC header length")
    header_length = _LENGTH.unpack(prefix)[0]
    if header_length > MAX_HEADER_BYTES:
        raise IPCError("IPC header exceeds configured limit")
    header_bytes = stream.read(header_length)
    if len(header_bytes) != header_length:
        raise IPCError("truncated IPC header")
    try:
        header = json.loads(header_bytes.decode("ascii"))
    except (UnicodeDecodeError, ValueError, TypeError) as exc:
        raise IPCError("invalid IPC JSON header") from exc
    if not isinstance(header, dict) or header.get("protocol_version") != PROTOCOL_VERSION:
        raise IPCError("unsupported IPC protocol")
    payload_length = header.get("payload_length", 0)
    if isinstance(payload_length, bool) or not isinstance(payload_length, int) or payload_length < 0:
        raise IPCError("invalid IPC payload length")
    if payload_length > max_payload:
        raise IPCError("IPC payload exceeds configured limit")
    payload = stream.read(payload_length)
    if len(payload) != payload_length:
        raise IPCError("truncated IPC payload")
    return header, payload


def _wait(fd: int, *, write: bool, deadline: float) -> None:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("PDFium worker watchdog expired")
    readable, writable, _ = select.select([] if write else [fd], [fd] if write else [], [], remaining)
    if not (writable if write else readable):
        raise TimeoutError("PDFium worker watchdog expired")


def write_deadline(fd: int, data: bytes, deadline: float) -> None:
    """Write bounded bytes to a worker pipe under a monotonic deadline."""

    offset = 0
    while offset < len(data):
        _wait(fd, write=True, deadline=deadline)
        written = os.write(fd, data[offset : offset + 64 * 1024])
        if written <= 0:
            raise IPCError("worker request pipe closed")
        offset += written


def read_exact_deadline(fd: int, length: int, deadline: float) -> bytes:
    """Read exactly a bounded number of bytes under a monotonic deadline."""

    result = bytearray()
    while len(result) < length:
        _wait(fd, write=False, deadline=deadline)
        chunk = os.read(fd, min(64 * 1024, length - len(result)))
        if not chunk:
            raise IPCError("worker response pipe closed")
        result.extend(chunk)
    return bytes(result)


def read_frame_deadline(fd: int, *, max_payload: int, deadline: float) -> tuple[dict[str, Any], bytes]:
    prefix = read_exact_deadline(fd, _LENGTH.size, deadline)
    header_length = _LENGTH.unpack(prefix)[0]
    if header_length > MAX_HEADER_BYTES:
        raise IPCError("IPC header exceeds configured limit")
    header_bytes = read_exact_deadline(fd, header_length, deadline)
    try:
        header = json.loads(header_bytes.decode("ascii"))
    except (UnicodeDecodeError, ValueError, TypeError) as exc:
        raise IPCError("invalid IPC JSON header") from exc
    if not isinstance(header, dict) or header.get("protocol_version") != PROTOCOL_VERSION:
        raise IPCError("unsupported IPC protocol")
    payload_length = header.get("payload_length", 0)
    if isinstance(payload_length, bool) or not isinstance(payload_length, int) or payload_length < 0:
        raise IPCError("invalid IPC payload length")
    if payload_length > max_payload:
        raise IPCError("IPC payload exceeds configured limit")
    return header, read_exact_deadline(fd, payload_length, deadline)
