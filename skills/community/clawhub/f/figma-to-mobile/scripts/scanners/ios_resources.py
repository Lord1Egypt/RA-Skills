#!/usr/bin/env python3
"""Scan iOS project for color definitions and localized strings."""

from __future__ import annotations

import json
import re
from pathlib import Path

# ── Color scanning ──

# Matches: UIColor(hex: "#RRGGBB") or UIColor(hex: "#RRGGBBAA")
_RE_UICOLOR_HEX = re.compile(
    r'UIColor\(\s*hex:\s*"(#[0-9A-Fa-f]{6,8})"\s*\)'
)

# Matches: Color(hex: "...")
_RE_SWIFTUI_COLOR = re.compile(
    r'Color\(\s*hex:\s*"(#[0-9A-Fa-f]{6,8})"\s*\)'
)

# Matches: let/var propertyName = UIColor(... or Color(...
_RE_COLOR_PROP = re.compile(
    r'(?:let|var)\s+(\w+)\s*=\s*(?:UIColor|Color)\b'
)

# Dynamic color: UIColor.dynamic(light: UIColor(hex: "X"), dark: UIColor(hex: "Y"))
_RE_DYNAMIC = re.compile(
    r'UIColor\.dynamic\(\s*light:\s*UIColor\(\s*hex:\s*"(#[0-9A-Fa-f]{6,8})"\s*\)'
    r'\s*,\s*dark:\s*UIColor\(\s*hex:\s*"(#[0-9A-Fa-f]{6,8})"\s*\)\s*\)'
)


def scan_colorset_assets(root: Path) -> list[dict]:
    """Scan *.xcassets for *.colorset/Contents.json."""
    colors: list[dict] = []
    for cset in root.rglob("*.colorset"):
        contents = cset / "Contents.json"
        if not contents.is_file():
            continue
        try:
            data = json.loads(contents.read_text(encoding="utf-8"))
            for entry in data.get("colors", []):
                comp = entry.get("color", {}).get("components", {})
                r = comp.get("red", "0")
                g = comp.get("green", "0")
                b = comp.get("blue", "0")
                colors.append({
                    "name": cset.stem,
                    "value": f"rgb({r},{g},{b})",
                    "source": str(cset),
                })
        except (json.JSONDecodeError, KeyError):
            pass
    return colors


def scan_swift_colors(root: Path) -> list[dict]:
    """Scan .swift files for UIColor/Color hex definitions."""
    colors: list[dict] = []
    seen: set[str] = set()
    for sf in root.rglob("*.swift"):
        if "/Pods/" in str(sf) or "/Tests/" in str(sf):
            continue
        try:
            text = sf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            # Dynamic colors (light+dark pair)
            for m in _RE_DYNAMIC.finditer(line):
                prop_m = _RE_COLOR_PROP.search(line)
                name = prop_m.group(1) if prop_m else f"color_L{line_no}"
                light, dark = m.group(1), m.group(2)
                key = f"{name}@{sf}"
                if key not in seen:
                    seen.add(key)
                    colors.append({
                        "name": name,
                        "value": f"light:{light} dark:{dark}",
                        "source": str(sf),
                    })
            # Plain UIColor(hex:) / Color(hex:)
            if _RE_DYNAMIC.search(line):
                continue  # already handled
            for pat in (_RE_UICOLOR_HEX, _RE_SWIFTUI_COLOR):
                for m in pat.finditer(line):
                    prop_m = _RE_COLOR_PROP.search(line)
                    name = prop_m.group(1) if prop_m else f"color_L{line_no}"
                    key = f"{name}@{sf}"
                    if key not in seen:
                        seen.add(key)
                        colors.append({
                            "name": name,
                            "value": m.group(1),
                            "source": str(sf),
                        })
    return colors


# ── String scanning ──

_RE_DOTSTRINGS = re.compile(r'^\s*"(.+?)"\s*=\s*"(.+?)"\s*;', re.MULTILINE)
_RE_NS_LOCALIZED = re.compile(
    r'NSLocalizedString\(\s*"(.+?)"'
)


def scan_strings_files(root: Path) -> list[dict]:
    """Scan .strings files for key=value pairs."""
    strings: list[dict] = []
    for sf in root.rglob("*.strings"):
        if "/Pods/" in str(sf):
            continue
        try:
            text = sf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in _RE_DOTSTRINGS.finditer(text):
            strings.append({"key": m.group(1), "value": m.group(2), "source": str(sf)})
    return strings


def scan_json_strings(root: Path) -> list[dict]:
    """Scan JSON i18n files (e.g. i18n_en.json)."""
    strings: list[dict] = []
    for jf in root.rglob("*.json"):
        if "/Pods/" in str(jf):
            continue
        if not ("i18n" in jf.stem.lower() or "locale" in jf.stem.lower()
                or "string" in jf.stem.lower()
                or jf.parent.name.lower() in ("i18n", "locales", "resources")):
            continue
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    strings.append({"key": k, "value": v, "source": str(jf)})
    return strings


def scan_ns_localized(root: Path) -> list[dict]:
    """Scan Swift files for NSLocalizedString calls."""
    strings: list[dict] = []
    seen: set[str] = set()
    for sf in root.rglob("*.swift"):
        if "/Pods/" in str(sf) or "/Tests/" in str(sf):
            continue
        try:
            text = sf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in _RE_NS_LOCALIZED.finditer(text):
            key = m.group(1)
            if key not in seen:
                seen.add(key)
                strings.append({"key": key, "value": "", "source": str(sf)})
    return strings
