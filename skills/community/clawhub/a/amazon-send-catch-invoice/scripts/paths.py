#!/usr/bin/env python3
"""Cross-platform paths. Windows, macOS and Linux all work.

Do NOT use /tmp. It does not exist on Windows, and even on Unix it is wiped on
reboot, so a cache there silently re-downloads every image. Use the per-user
cache directory the OS actually provides:

    Windows   %LOCALAPPDATA%\\catch-invoice\\images
    macOS     ~/Library/Caches/catch-invoice/images
    Linux     $XDG_CACHE_HOME/catch-invoice/images  (default ~/.cache/…)

Override any of these with the CATCH_INVOICE_HOME environment variable.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP = "catch-invoice"


def _base() -> Path:
    override = os.environ.get("CATCH_INVOICE_HOME")
    if override:
        return Path(override).expanduser()
    if sys.platform == "win32":
        root = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        return Path(root or Path.home()) / APP
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / APP
    xdg = os.environ.get("XDG_CACHE_HOME")
    return Path(xdg).expanduser() / APP if xdg else Path.home() / ".cache" / APP


def cache_dir(name: str = "images") -> Path:
    """Per-user cache directory, created on demand."""
    p = _base() / name
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_dir() -> Path:
    """Per-user config directory (portal token lives here), created on demand."""
    if sys.platform == "win32":
        p = _base() / "config"
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        p = (Path(xdg).expanduser() if xdg else Path.home() / ".config") / APP
    p.mkdir(parents=True, exist_ok=True)
    return p


def records_dir() -> Path:
    """Where generated invoices are written. Override with CATCH_INVOICE_RECORDS."""
    override = os.environ.get("CATCH_INVOICE_RECORDS")
    p = Path(override).expanduser() if override else Path.cwd() / "catch_invoice_records"
    p.mkdir(parents=True, exist_ok=True)
    return p


if __name__ == "__main__":
    print(f"platform  {sys.platform}")
    print(f"cache     {cache_dir()}")
    print(f"config    {config_dir()}")
    print(f"records   {records_dir()}")
