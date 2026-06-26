#!/usr/bin/env python3
"""
Android resource scanner for project_scan.

Scans res/values/ XML files: colors.xml, strings.xml, dimens.xml,
styles.xml, themes.xml. Extracts name→value mappings.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path


def scan_colors(res_dir: Path) -> list[dict]:
    """
    Scan all colors*.xml files in res/values/.
    
    Returns list of {'name': str, 'value': str (hex)}.
    Also handles color references like @color/other.
    """
    colors = []
    values_dir = res_dir / "values"
    if not values_dir.is_dir():
        return colors
    
    for xml_file in sorted(values_dir.glob("colors*.xml")):
        colors.extend(_parse_value_items(xml_file, "color"))
    
    return colors


def scan_strings(res_dir: Path) -> list[dict]:
    """
    Scan strings.xml in res/values/.
    
    Returns list of {'name': str, 'value': str}.
    """
    strings = []
    values_dir = res_dir / "values"
    if not values_dir.is_dir():
        return strings
    
    for xml_file in sorted(values_dir.glob("strings*.xml")):
        strings.extend(_parse_value_items(xml_file, "string"))
    
    return strings


def scan_dimens(res_dir: Path) -> list[dict]:
    """
    Scan dimens.xml in res/values/.
    
    Returns list of {'name': str, 'value': str (e.g. '16dp')}.
    """
    dimens = []
    values_dir = res_dir / "values"
    if not values_dir.is_dir():
        return dimens
    
    for xml_file in sorted(values_dir.glob("dimens*.xml")):
        dimens.extend(_parse_value_items(xml_file, "dimen"))
    
    return dimens


def scan_styles(res_dir: Path) -> list[dict]:
    """
    Scan styles.xml and themes.xml in res/values/.
    
    Returns list of {'name': str, 'parent': str|None, 'items': dict}.
    """
    styles = []
    values_dir = res_dir / "values"
    if not values_dir.is_dir():
        return styles
    
    for pattern in ("styles*.xml", "themes*.xml"):
        for xml_file in sorted(values_dir.glob(pattern)):
            styles.extend(_parse_styles(xml_file))
    
    return styles


def scan_module_resources(module_dir: Path) -> dict:
    """
    Scan all resources in a module's res/ directory.
    
    Returns:
        {
            'module': str,
            'colors': [...],
            'strings': [...],
            'dimens': [...],
            'styles': [...],
        }
    """
    # Try both src/main/res and res
    res_dir = module_dir / "src" / "main" / "res"
    if not res_dir.is_dir():
        res_dir = module_dir / "res"
    
    return {
        "module": module_dir.name,
        "colors": scan_colors(res_dir),
        "strings": scan_strings(res_dir),
        "dimens": scan_dimens(res_dir),
        "styles": scan_styles(res_dir),
        "text_styles": scan_text_styles(res_dir),
    }


def build_color_index(all_resources: list[dict]) -> dict:
    """
    Build a hex→resource_name index for quick color matching.
    
    Input: list of module resource dicts from scan_module_resources.
    Returns: {'#FF0F0F0F': '@color/text_primary', ...}
    
    Normalizes hex to uppercase 8-char ARGB (#AARRGGBB).
    If duplicate hex values exist, first match wins (target module first).
    """
    index = {}
    for mod in all_resources:
        for color in mod["colors"]:
            normalized = _normalize_hex(color["value"])
            if normalized and normalized not in index:
                index[normalized] = f"@color/{color['name']}"
    return index


def scan_text_styles(res_dir: Path) -> list[dict]:
    """
    Scan styles*.xml and themes*.xml for TextAppearance-related styles.

    A style is considered text-related if any of:
    - name contains "TextAppearance" or "Text"
    - parent contains "TextAppearance"
    - it has an "android:textSize" item

    Returns list of dicts with keys:
        name, parent, text_size, text_color, font_family,
        text_style, line_height, letter_spacing
    """
    ANDROID_NS = "http://schemas.android.com/apk/res/android"
    ATTR_MAP = {
        f"{{{ANDROID_NS}}}textSize": "text_size",
        "android:textSize": "text_size",
        f"{{{ANDROID_NS}}}textColor": "text_color",
        "android:textColor": "text_color",
        f"{{{ANDROID_NS}}}fontFamily": "font_family",
        "android:fontFamily": "font_family",
        f"{{{ANDROID_NS}}}textStyle": "text_style",
        "android:textStyle": "text_style",
        f"{{{ANDROID_NS}}}lineHeight": "line_height",
        "android:lineHeight": "line_height",
        f"{{{ANDROID_NS}}}letterSpacing": "letter_spacing",
        "android:letterSpacing": "letter_spacing",
    }

    text_styles: list[dict] = []
    values_dir = res_dir / "values"
    if not values_dir.is_dir():
        return text_styles

    for pattern in ("styles*.xml", "themes*.xml"):
        for xml_file in sorted(values_dir.glob(pattern)):
            try:
                tree = ET.parse(xml_file)
            except ET.ParseError:
                continue

            for elem in tree.findall(".//style"):
                name = elem.get("name")
                if not name:
                    continue

                parent = elem.get("parent")

                # Collect item attributes (handle both namespace forms)
                items: dict[str, str] = {}
                for item in elem.findall("item"):
                    item_name = item.get("name", "")
                    if item_name:
                        items[item_name] = (item.text or "").strip()

                # Determine if this is a text-related style
                is_text_style = False
                name_upper = name.upper()
                if "TEXTAPPEARANCE" in name_upper or "TEXT" in name_upper:
                    is_text_style = True
                elif parent and "TEXTAPPEARANCE" in parent.upper():
                    is_text_style = True
                else:
                    # Check if it has android:textSize
                    for item_key in items:
                        if item_key in ("android:textSize",
                                        f"{{{ANDROID_NS}}}textSize"):
                            is_text_style = True
                            break

                if not is_text_style:
                    continue

                # Extract relevant attributes
                entry: dict[str, str | None] = {
                    "name": name,
                    "parent": parent,
                    "text_size": None,
                    "text_color": None,
                    "font_family": None,
                    "text_style": None,
                    "line_height": None,
                    "letter_spacing": None,
                }
                for item_key, item_val in items.items():
                    mapped = ATTR_MAP.get(item_key)
                    if mapped:
                        entry[mapped] = item_val

                text_styles.append(entry)

    return text_styles


def build_text_style_index(all_resources: list[dict]) -> dict:
    """
    Build a "{textSize}_{fontWeight}" → list[style_name] index.

    Key format: "16sp_bold", "14sp_normal", etc.

    fontWeight mapping (from textStyle or fontFamily hints):
    - "bold"     → "bold"
    - "medium"   → "medium"
    - "normal" / unset → "normal"
    """
    index: dict[str, list[str]] = {}
    for mod in all_resources:
        for ts in mod.get("text_styles", []):
            text_size = ts.get("text_size")
            if not text_size:
                continue

            # Normalize text size: keep as-is if already has unit, e.g. "16sp"
            size_str = text_size.strip().lower()
            # Remove non-sp suffixes for the key, but keep sp
            if not size_str.endswith("sp"):
                continue  # Only index sp-based sizes

            # Determine weight from textStyle
            raw_style = (ts.get("text_style") or "").lower().strip()
            font_family = (ts.get("font_family") or "").lower()

            if "bold" in raw_style:
                weight = "bold"
            elif "medium" in font_family:
                weight = "medium"
            elif "semibold" in font_family or "semi-bold" in font_family:
                weight = "semibold"
            else:
                weight = "normal"

            key = f"{size_str}_{weight}"
            if key not in index:
                index[key] = []
            style_ref = f"@style/{ts['name']}"
            if style_ref not in index[key]:
                index[key].append(style_ref)

    return index


def build_string_index(all_resources: list[dict]) -> dict:
    """
    Build a text→resource_name index for string matching.
    
    Returns: {'通知设置': '@string/notification_settings', ...}
    """
    index = {}
    for mod in all_resources:
        for s in mod["strings"]:
            if s["value"] and s["value"] not in index:
                index[s["value"]] = f"@string/{s['name']}"
    return index


# --- Internal helpers ---

def _parse_value_items(xml_file: Path, tag: str) -> list[dict]:
    """Parse <color>, <string>, or <dimen> items from a values XML file."""
    items = []
    try:
        tree = ET.parse(xml_file)
        for elem in tree.findall(f".//{tag}"):
            name = elem.get("name")
            value = (elem.text or "").strip()
            if name:
                items.append({"name": name, "value": value})
    except ET.ParseError:
        pass  # Skip malformed XML
    return items


def _parse_styles(xml_file: Path) -> list[dict]:
    """Parse <style> elements from styles/themes XML."""
    styles = []
    try:
        tree = ET.parse(xml_file)
        for elem in tree.findall(".//style"):
            name = elem.get("name")
            parent = elem.get("parent")
            items = {}
            for item in elem.findall("item"):
                item_name = item.get("name")
                if item_name:
                    items[item_name] = (item.text or "").strip()
            if name:
                styles.append({"name": name, "parent": parent, "items": items})
    except ET.ParseError:
        pass
    return styles


def _normalize_hex(value: str) -> str | None:
    """
    Normalize a color hex value to uppercase 8-char #AARRGGBB.
    
    #RGB     -> #FFRRGGBB (expand + add alpha)
    #RRGGBB  -> #FFRRGGBB (add alpha)
    #AARRGGBB -> as-is (uppercase)
    @color/x  -> None (reference, not a hex value)
    """
    value = value.strip()
    if not value.startswith("#"):
        return None
    
    hex_part = value[1:].upper()
    
    if len(hex_part) == 3:
        # #RGB -> #FFRRGGBB
        hex_part = "FF" + "".join(c * 2 for c in hex_part)
    elif len(hex_part) == 4:
        # #ARGB -> #AARRGGBB
        hex_part = "".join(c * 2 for c in hex_part)
    elif len(hex_part) == 6:
        # #RRGGBB -> #FFRRGGBB
        hex_part = "FF" + hex_part
    elif len(hex_part) == 8:
        pass  # Already #AARRGGBB
    else:
        return None
    
    return "#" + hex_part
