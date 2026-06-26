#!/usr/bin/env python3
"""Scan iOS project for custom UIView/SwiftUI View definitions."""

from __future__ import annotations

import re
from pathlib import Path

# UIKit class inheritance patterns
_UIKIT_BASES = (
    "UIView", "UIViewController", "UITableViewCell",
    "UICollectionViewCell", "UITableViewController",
    "UICollectionViewController", "UINavigationController",
    "UITabBarController", "UIControl", "UIScrollView",
    "UITableViewHeaderFooterView", "UICollectionReusableView",
)
_BASES_PATTERN = "|".join(_UIKIT_BASES)

# class ClassName: UIView {  or  class ClassName: SomeCustomView, Protocol {
_RE_CLASS = re.compile(
    rf'^\s*(?:(?:public|internal|private|open|final)\s+)*'
    rf'class\s+(\w+)\s*(?:<[^>]*>)?\s*:\s*(\w+)',
    re.MULTILINE,
)

# struct ClassName: View {
_RE_SWIFTUI_VIEW = re.compile(
    r'^\s*(?:(?:public|internal|private)\s+)?'
    r'struct\s+(\w+)\s*(?:<[^>]*>)?\s*:\s*(?:\w+,\s*)*View\b',
    re.MULTILINE,
)

# Skip extensions and protocols
_RE_EXTENSION = re.compile(r'^\s*extension\s+', re.MULTILINE)
_RE_PROTOCOL = re.compile(r'^\s*protocol\s+', re.MULTILINE)


def _infer_package(filepath: Path, project_root: Path) -> str:
    """Infer a module/package name from the file path."""
    try:
        rel = filepath.relative_to(project_root)
        parts = rel.parts
        # Skip the first part if it's the main target dir, use 2nd level
        if len(parts) >= 3:
            return parts[1] if parts[1] != "src" else parts[2]
        elif len(parts) >= 2:
            return parts[0]
    except ValueError:
        pass
    return ""


def scan_views(root: Path) -> list[dict]:
    """
    Scan Swift files for UIView subclasses and SwiftUI Views.

    Returns list of dicts with name, parent, package, file.
    """
    views: list[dict] = []
    seen: set[str] = set()

    for sf in root.rglob("*.swift"):
        fstr = str(sf)
        # Skip Pods, tests, extensions-only files
        if any(skip in fstr for skip in ("/Pods/", "/Tests/", "Test/", "UITests/")):
            continue

        try:
            text = sf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        # UIKit classes
        for m in _RE_CLASS.finditer(text):
            cls_name, parent = m.group(1), m.group(2)
            if cls_name in seen:
                continue
            # Check if parent is a known UIKit base or custom (include all)
            seen.add(cls_name)
            views.append({
                "name": cls_name,
                "parent": parent,
                "package": _infer_package(sf, root),
                "file": fstr,
            })

        # SwiftUI Views
        for m in _RE_SWIFTUI_VIEW.finditer(text):
            name = m.group(1)
            if name in seen:
                continue
            seen.add(name)
            views.append({
                "name": name,
                "parent": "View",
                "package": _infer_package(sf, root),
                "file": fstr,
            })

    return views
