#!/usr/bin/env python3
"""
Android layout XML scanner.

Analyzes layout files to extract View usage patterns, attribute
combinations, and constraint styles for pattern learning.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

NS_ANDROID = "http://schemas.android.com/apk/res/android"
NS_APP = "http://schemas.android.com/apk/res-auto"


def scan_layouts(res_dir: Path) -> dict:
    """
    Scan layout XML files and extract usage statistics.

    Returns dict with view_usage, root_views, parent_child combos,
    text_styles, image_patterns, constraint_patterns.
    """
    layout_dir = res_dir / "layout"
    if not layout_dir.is_dir():
        return _empty_result()

    view_usage: Counter = Counter()
    root_views: Counter = Counter()
    parent_child: Counter = Counter()
    text_styles: Counter = Counter()
    image_patterns: Counter = Counter()
    dimension_modes: Counter = Counter()
    total_files = 0

    for xml_file in sorted(layout_dir.glob("*.xml")):
        total_files += 1
        try:
            tree = ET.parse(xml_file)
        except ET.ParseError:
            continue
        _walk(tree.getroot(), None, view_usage, root_views,
              parent_child, text_styles, image_patterns,
              dimension_modes)

    return {
        "total_layouts": total_files,
        "view_usage": dict(view_usage.most_common(30)),
        "root_views": dict(root_views.most_common(10)),
        "parent_child": dict(parent_child.most_common(30)),
        "text_styles": dict(text_styles.most_common(20)),
        "image_patterns": dict(image_patterns.most_common(10)),
        "dimension_modes": dict(dimension_modes.most_common(15)),
    }


def _walk(elem, parent_tag, view_usage, root_views,
          parent_child, text_styles, image_patterns,
          dimension_modes):
    """Recursively walk XML tree and collect stats."""
    tag = _short_tag(elem.tag)
    if tag in ("merge", "include", "layout"):
        for child in elem:
            _walk(child, parent_tag, view_usage, root_views,
                  parent_child, text_styles, image_patterns,
                  dimension_modes)
        return

    view_usage[tag] += 1

    if parent_tag is None:
        root_views[tag] += 1
    else:
        parent_child[f"{parent_tag} > {tag}"] += 1

    attrs = _short_attrs(elem.attrib)

    # Text styles
    if "TextView" in tag or "FontTextView" in tag:
        _extract_text_style(attrs, text_styles)

    # Image patterns
    if "ImageView" in tag:
        _extract_image_pattern(attrs, image_patterns)

    # Dimension modes in ConstraintLayout children
    if parent_tag and "ConstraintLayout" in parent_tag:
        _extract_dimension_mode(attrs, dimension_modes)

    for child in elem:
        _walk(child, tag, view_usage, root_views,
              parent_child, text_styles, image_patterns,
              dimension_modes)


def _extract_text_style(attrs: dict, counter: Counter) -> None:
    parts = []
    size = attrs.get("android:textSize", "")
    if size:
        parts.append(f"size:{size}")
    color = attrs.get("android:textColor", "")
    if color.startswith("@color"):
        parts.append(f"color:{color}")
    elif color:
        parts.append("color:hardcoded")
    style = attrs.get("android:textStyle", "")
    if style:
        parts.append(f"style:{style}")
    if parts:
        counter[" | ".join(parts)] += 1


def _extract_image_pattern(attrs: dict, counter: Counter) -> None:
    parts = []
    if "android:src" in attrs or "app:srcCompat" in attrs:
        parts.append("src")
    if "android:background" in attrs:
        parts.append("bg")
    if "app:tint" in attrs or "android:tint" in attrs:
        parts.append("tint")
    if parts:
        counter["+".join(sorted(parts))] += 1


def _extract_dimension_mode(attrs: dict, counter: Counter) -> None:
    w = attrs.get("android:layout_width", "")
    h = attrs.get("android:layout_height", "")
    if w and h:
        counter[f"w={w} h={h}"] += 1


def _short_tag(tag: str) -> str:
    if "}" in tag:
        tag = tag.split("}")[-1]
    # Shorten common prefixes
    tag = tag.replace("androidx.constraintlayout.widget.", "")
    tag = tag.replace("androidx.recyclerview.widget.", "")
    tag = tag.replace("com.google.android.material.", "material.")
    return tag


def _short_attrs(attrib: dict) -> dict:
    result = {}
    for k, v in attrib.items():
        short = k.replace(f"{{{NS_ANDROID}}}", "android:")
        short = short.replace(f"{{{NS_APP}}}", "app:")
        result[short] = v
    return result


def _empty_result() -> dict:
    return {
        "total_layouts": 0,
        "view_usage": {},
        "root_views": {},
        "parent_child": {},
        "text_styles": {},
        "image_patterns": {},
        "dimension_modes": {},
    }
