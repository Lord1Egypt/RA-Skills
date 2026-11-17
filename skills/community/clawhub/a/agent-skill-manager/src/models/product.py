"""Typed shape of a supported product's registry entry."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict


class ProductSpec(TypedDict, total=False):
    """Static description of one supported AI agent product.

    Declared ``total=False`` because some products (e.g. DuMate) omit the
    platform-specific path keys or the optional ``settings_file`` /
    ``extra_dirs_*`` keys.
    """

    name: str
    short: str
    macos_path: Optional[Path]
    windows_path: Optional[Path]
    sync_method: str  # "symlink" | "native" | "pack"
    note: str
    extra_dirs_macos: list[Path]
    extra_dirs_windows: list[Path]
    settings_file: Path
