#!/usr/bin/env python3
"""
Single-pass Swift file scanner for iOS projects.

Reads each .swift file once and extracts colors, NSLocalizedString calls,
and class/struct definitions in a single pass. This replaces the separate
traversals in ios_resources.scan_swift_colors, ios_resources.scan_ns_localized,
and ios_views.scan_views.
"""

from __future__ import annotations

import re
from pathlib import Path

from .ios_resources import (
    _RE_DYNAMIC, _RE_UICOLOR_HEX, _RE_SWIFTUI_COLOR,
    _RE_COLOR_PROP, _RE_NS_LOCALIZED,
)
from .ios_views import _RE_CLASS, _RE_SWIFTUI_VIEW, _infer_package

# Directories to skip
_SKIP_SEGMENTS = frozenset(("Pods", "Tests", "UITests", "build",
                            ".build", "DerivedData", "Carthage"))


def scan_swift_single_pass(
    root: Path,
    *,
    colors: bool = True,
    strings: bool = True,
    views: bool = True,
) -> dict:
    """
    Scan all .swift files under root in a single traversal.

    Args:
        root: Directory to scan (typically the module source dir).
        colors: Extract UIColor/Color hex definitions.
        strings: Extract NSLocalizedString calls.
        views: Extract class/struct View definitions.

    Returns:
        {
            "colors": [{"name", "value", "source"}, ...],
            "strings": [{"key", "value", "source"}, ...],
            "views": [{"name", "parent", "package", "file"}, ...],
        }
    """
    result_colors: list[dict] = []
    result_strings: list[dict] = []
    result_views: list[dict] = []

    color_seen: set[str] = set()
    string_seen: set[str] = set()
    view_seen: set[str] = set()

    for sf in root.rglob("*.swift"):
        # Skip excluded directories
        if _SKIP_SEGMENTS & set(sf.parts):
            continue

        try:
            text = sf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        sf_str = str(sf)

        if colors:
            _extract_colors(text, sf, sf_str, result_colors, color_seen)

        if strings:
            _extract_ns_localized(text, sf_str, result_strings, string_seen)

        if views:
            _extract_views(text, sf, sf_str, root, result_views, view_seen)

    return {
        "colors": result_colors,
        "strings": result_strings,
        "views": result_views,
    }


def _extract_colors(
    text: str, sf: Path, sf_str: str,
    out: list[dict], seen: set[str],
) -> None:
    """Extract color definitions from file text."""
    for line_no, line in enumerate(text.splitlines(), 1):
        # Dynamic colors first
        for m in _RE_DYNAMIC.finditer(line):
            prop_m = _RE_COLOR_PROP.search(line)
            name = prop_m.group(1) if prop_m else f"color_L{line_no}"
            key = f"{name}@{sf_str}"
            if key not in seen:
                seen.add(key)
                out.append({
                    "name": name,
                    "value": f"light:{m.group(1)} dark:{m.group(2)}",
                    "source": sf_str,
                })

        if _RE_DYNAMIC.search(line):
            continue

        for pat in (_RE_UICOLOR_HEX, _RE_SWIFTUI_COLOR):
            for m in pat.finditer(line):
                prop_m = _RE_COLOR_PROP.search(line)
                name = prop_m.group(1) if prop_m else f"color_L{line_no}"
                key = f"{name}@{sf_str}"
                if key not in seen:
                    seen.add(key)
                    out.append({
                        "name": name,
                        "value": m.group(1),
                        "source": sf_str,
                    })


def _extract_ns_localized(
    text: str, sf_str: str,
    out: list[dict], seen: set[str],
) -> None:
    """Extract NSLocalizedString keys from file text."""
    for m in _RE_NS_LOCALIZED.finditer(text):
        key = m.group(1)
        if key not in seen:
            seen.add(key)
            out.append({"key": key, "value": "", "source": sf_str})


def _extract_views(
    text: str, sf: Path, sf_str: str, root: Path,
    out: list[dict], seen: set[str],
) -> None:
    """Extract class/struct View definitions from file text."""
    for m in _RE_CLASS.finditer(text):
        cls_name, parent = m.group(1), m.group(2)
        if cls_name not in seen:
            seen.add(cls_name)
            out.append({
                "name": cls_name,
                "parent": parent,
                "package": _infer_package(sf, root),
                "file": sf_str,
            })

    for m in _RE_SWIFTUI_VIEW.finditer(text):
        name = m.group(1)
        if name not in seen:
            seen.add(name)
            out.append({
                "name": name,
                "parent": "View",
                "package": _infer_package(sf, root),
                "file": sf_str,
            })
