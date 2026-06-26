"""Rewind markers: embed/extract hash references in compressed text.

Part of claw-compactor. License: MIT.
"""
from __future__ import annotations
import re
from dataclasses import dataclass


MARKER_PATTERN = re.compile(
    r'\[(\d+) items? compressed to (\d+)\. Retrieve: hash=([a-f0-9]{24})\]'
)


@dataclass(frozen=True)
class MarkerInfo:
    original_count: int
    compressed_count: int
    hash_id: str
    span: tuple[int, int]  # (start, end) in text


def embed_marker(text: str, original_count: int, compressed_count: int, hash_id: str) -> str:
    """Append a Rewind retrieval marker to compressed text."""
    item_word = "item" if original_count == 1 else "items"
    marker = f"[{original_count} {item_word} compressed to {compressed_count}. Retrieve: hash={hash_id}]"
    return f"{text}\n{marker}"


def extract_markers(text: str) -> list[MarkerInfo]:
    """Extract all Rewind markers from text."""
    markers = []
    for match in MARKER_PATTERN.finditer(text):
        markers.append(MarkerInfo(
            original_count=int(match.group(1)),
            compressed_count=int(match.group(2)),
            hash_id=match.group(3),
            span=(match.start(), match.end()),
        ))
    return markers


def has_markers(text: str) -> bool:
    """Return True if text contains any Rewind markers."""
    return bool(MARKER_PATTERN.search(text))


def strip_markers(text: str) -> str:
    """Remove all Rewind markers from text."""
    return MARKER_PATTERN.sub("", text).rstrip()
