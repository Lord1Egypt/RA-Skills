#!/usr/bin/env python3
"""
Drawable scanner for project_scan.

Scans res/drawable/ directories, extracts visual characteristics of
shape drawables and vector drawables for matching against Figma designs.

Also provides DrawableShapeEntry dataclass and dedicated shape scanning
for structured shape-drawable matching (fill color, corners, stroke, gradient).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


# Android XML namespaces
NS_ANDROID = "http://schemas.android.com/apk/res/android"


# ── DrawableShapeEntry dataclass ──

@dataclass
class DrawableShapeEntry:
    """Structured representation of a shape drawable's visual properties."""
    name: str                          # filename without .xml
    fill_color: str = ""               # hex e.g. "#FFFFFF", empty if none
    corner_radius: float = 0.0         # uniform corner radius, 0 if none
    corner_radii: list[float] | None = None  # [tl, tr, br, bl] when non-uniform
    stroke_color: str = ""             # stroke color hex
    stroke_width: float = 0.0          # stroke width in dp
    has_gradient: bool = False         # whether gradient is present
    source: str = ""                   # file path relative to res/

    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "fill_color": self.fill_color,
            "corner_radius": self.corner_radius,
            "stroke_color": self.stroke_color,
            "stroke_width": self.stroke_width,
            "has_gradient": self.has_gradient,
            "source": self.source,
        }
        if self.corner_radii is not None:
            d["corner_radii"] = self.corner_radii
        return d


# ── Shape-specific scanning ──

def scan_shape_drawables(res_dir: Path) -> list[DrawableShapeEntry]:
    """
    Scan drawable directories for shape drawables and extract visual properties.

    Parses res/drawable/*.xml and res/drawable-*/*.xml.
    Only processes <shape> root elements and <selector> containing <shape> items.
    Skips vector, layer-list, ripple, and other non-shape drawables.

    Returns list of DrawableShapeEntry.
    """
    entries: list[DrawableShapeEntry] = []
    if not res_dir.is_dir():
        return entries

    seen_names: set[str] = set()

    for drawable_dir in sorted(res_dir.glob("drawable*")):
        if not drawable_dir.is_dir():
            continue
        for xml_file in sorted(drawable_dir.glob("*.xml")):
            name = xml_file.stem
            if name in seen_names:
                continue
            seen_names.add(name)

            entry = _parse_shape_entry(xml_file, name, res_dir)
            if entry is not None:
                entries.append(entry)

    return entries


def build_shape_index(entries: list[DrawableShapeEntry]) -> dict[str, list[dict]]:
    """
    Build a color-keyed index for quick shape lookup.

    Returns: {"#ff5722": [entry.to_dict(), ...], ...}
    Keys are lowercase hex fill colors. Entries without a fill color
    are indexed under the empty string key "".
    """
    index: dict[str, list[dict]] = {}
    for entry in entries:
        key = entry.fill_color.lower() if entry.fill_color else ""
        index.setdefault(key, []).append(entry.to_dict())
    return index


def _parse_shape_entry(
    xml_file: Path, name: str, res_dir: Path,
) -> DrawableShapeEntry | None:
    """Parse an XML file and return DrawableShapeEntry if it's a shape drawable."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except (ET.ParseError, OSError):
        return None

    tag = _strip_ns(root.tag)
    source = str(xml_file.relative_to(res_dir))

    if tag == "shape":
        return _extract_shape_props(root, name, source)
    elif tag == "selector":
        # Look for the default (no state attrs) or first <item> containing a <shape>
        return _extract_selector_shape(root, name, source)
    else:
        return None  # skip vector, layer-list, ripple, etc.


def _extract_shape_props(
    shape_elem, name: str, source: str,
) -> DrawableShapeEntry:
    """Extract visual properties from a <shape> element."""
    fill_color = ""
    corner_radius = 0.0
    corner_radii: list[float] | None = None
    stroke_color = ""
    stroke_width = 0.0
    has_gradient = False

    # Solid fill color
    solid = shape_elem.find("solid")
    if solid is not None:
        fill_color = solid.get(f"{{{NS_ANDROID}}}color", "")

    # Gradient
    gradient = shape_elem.find("gradient")
    if gradient is not None:
        has_gradient = True

    # Corner radius
    corners = shape_elem.find("corners")
    if corners is not None:
        uniform = corners.get(f"{{{NS_ANDROID}}}radius", "")
        if uniform:
            corner_radius = _parse_dp(uniform)
        else:
            tl = _parse_dp(corners.get(f"{{{NS_ANDROID}}}topLeftRadius", "0dp"))
            tr = _parse_dp(corners.get(f"{{{NS_ANDROID}}}topRightRadius", "0dp"))
            br = _parse_dp(corners.get(f"{{{NS_ANDROID}}}bottomRightRadius", "0dp"))
            bl = _parse_dp(corners.get(f"{{{NS_ANDROID}}}bottomLeftRadius", "0dp"))
            if tl == tr == br == bl:
                corner_radius = tl
            else:
                corner_radii = [tl, tr, br, bl]

    # Stroke
    stroke = shape_elem.find("stroke")
    if stroke is not None:
        stroke_color = stroke.get(f"{{{NS_ANDROID}}}color", "")
        stroke_width = _parse_dp(stroke.get(f"{{{NS_ANDROID}}}width", "0dp"))

    return DrawableShapeEntry(
        name=name,
        fill_color=fill_color,
        corner_radius=corner_radius,
        corner_radii=corner_radii,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        has_gradient=has_gradient,
        source=source,
    )


def _extract_selector_shape(
    selector_elem, name: str, source: str,
) -> DrawableShapeEntry | None:
    """
    Extract shape properties from a <selector> that contains <shape> items.

    Prefers the default item (no state_* attributes); falls back to the first
    item that contains an inline <shape> child.
    """
    first_match: DrawableShapeEntry | None = None

    for item in selector_elem:
        if _strip_ns(item.tag) != "item":
            continue
        shape_child = item.find("shape")
        if shape_child is not None:
            # Check if this is a "default" item (no state attrs)
            has_state = any("state_" in attr for attr in item.attrib)
            entry = _extract_shape_props(shape_child, name, source)
            if not has_state:
                return entry
            # Remember first match as fallback
            if first_match is None:
                first_match = entry

    # Return first stateful match if no default found
    if first_match is not None:
        return first_match

    return None


# ── Original drawable scanning (preserved for backward compatibility) ──

def scan_drawables(res_dir: Path) -> list[dict]:
    """
    Scan all drawable directories under res/.

    Looks at res/drawable/, res/drawable-*dpi/ etc.
    Only parses XML drawables (shapes, vectors, selectors).

    Returns list of drawable info dicts.
    """
    drawables = []
    if not res_dir.is_dir():
        return drawables

    seen_names: set[str] = set()

    # Scan drawable dirs (prefer drawable/ over qualified dirs)
    for drawable_dir in sorted(res_dir.glob("drawable*")):
        if not drawable_dir.is_dir():
            continue
        for xml_file in sorted(drawable_dir.glob("*.xml")):
            name = xml_file.stem
            if name in seen_names:
                continue
            seen_names.add(name)

            info = _parse_drawable(xml_file)
            if info:
                info["name"] = name
                info["file"] = str(xml_file.relative_to(res_dir))
                drawables.append(info)

    return drawables


def _parse_drawable(xml_file: Path) -> dict | None:
    """Parse an XML drawable and extract visual characteristics."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError:
        return None

    tag = _strip_ns(root.tag)

    if tag == "shape":
        return _parse_shape(root)
    elif tag == "vector":
        return _parse_vector(root)
    elif tag == "selector":
        return _parse_selector(root)
    elif tag == "layer-list":
        return {"type": "layer-list", "layers": _count_children(root)}
    elif tag == "ripple":
        return {"type": "ripple"}
    else:
        return {"type": tag}


def _parse_shape(root) -> dict:
    """Extract shape drawable characteristics."""
    info: dict = {"type": "shape"}

    # Shape type (rectangle, oval, etc.)
    shape_type = root.get(f"{{{NS_ANDROID}}}shape", "rectangle")
    info["shape"] = shape_type

    # Solid color
    solid = root.find("solid")
    if solid is not None:
        info["color"] = solid.get(f"{{{NS_ANDROID}}}color", "")

    # Gradient
    gradient = root.find("gradient")
    if gradient is not None:
        info["gradient"] = {
            "type": gradient.get(f"{{{NS_ANDROID}}}type", "linear"),
            "startColor": gradient.get(f"{{{NS_ANDROID}}}startColor", ""),
            "endColor": gradient.get(f"{{{NS_ANDROID}}}endColor", ""),
            "angle": gradient.get(f"{{{NS_ANDROID}}}angle", ""),
        }

    # Corner radius
    corners = root.find("corners")
    if corners is not None:
        radius = corners.get(f"{{{NS_ANDROID}}}radius", "")
        if radius:
            info["cornerRadius"] = radius
        else:
            # Per-corner radii
            info["corners"] = {
                "topLeft": corners.get(f"{{{NS_ANDROID}}}topLeftRadius", "0dp"),
                "topRight": corners.get(f"{{{NS_ANDROID}}}topRightRadius", "0dp"),
                "bottomLeft": corners.get(f"{{{NS_ANDROID}}}bottomLeftRadius", "0dp"),
                "bottomRight": corners.get(f"{{{NS_ANDROID}}}bottomRightRadius", "0dp"),
            }

    # Stroke
    stroke = root.find("stroke")
    if stroke is not None:
        info["stroke"] = {
            "color": stroke.get(f"{{{NS_ANDROID}}}color", ""),
            "width": stroke.get(f"{{{NS_ANDROID}}}width", ""),
        }

    # Size
    size = root.find("size")
    if size is not None:
        info["size"] = {
            "width": size.get(f"{{{NS_ANDROID}}}width", ""),
            "height": size.get(f"{{{NS_ANDROID}}}height", ""),
        }

    return info


def _parse_vector(root) -> dict:
    """Extract vector drawable characteristics."""
    info: dict = {"type": "vector"}

    width = root.get(f"{{{NS_ANDROID}}}width", "")
    height = root.get(f"{{{NS_ANDROID}}}height", "")
    if width:
        info["width"] = width
    if height:
        info["height"] = height

    # Count paths for complexity estimate
    path_count = len(list(root.iter("path")))
    info["pathCount"] = path_count

    # Tint
    tint = root.get(f"{{{NS_ANDROID}}}tint", "")
    if tint:
        info["tint"] = tint

    return info


def _parse_selector(root) -> dict:
    """Extract selector drawable info."""
    items = list(root)
    states = []
    for item in items:
        state: dict = {}
        for attr_name, attr_val in item.attrib.items():
            if "state_" in attr_name:
                state_name = attr_name.split("}")[-1] if "}" in attr_name else attr_name
                state[state_name] = attr_val
        drawable = item.get(f"{{{NS_ANDROID}}}drawable", "")
        if drawable:
            state["drawable"] = drawable
        if state:
            states.append(state)

    return {"type": "selector", "stateCount": len(states), "states": states}


def build_drawable_index(drawables: list[dict]) -> dict:
    """
    Build a searchable index of shape drawables by visual features.

    Returns: {
        'shapes': [{'name': ..., 'color': ..., 'cornerRadius': ..., 'stroke': ...}, ...],
        'vectors': [{'name': ..., 'width': ..., 'height': ...}, ...],
        'selectors': [{'name': ..., 'stateCount': ...}, ...],
    }
    """
    index: dict = {"shapes": [], "vectors": [], "selectors": [], "other": []}

    for d in drawables:
        dtype = d.get("type", "")
        if dtype == "shape":
            index["shapes"].append(d)
        elif dtype == "vector":
            index["vectors"].append(d)
        elif dtype == "selector":
            index["selectors"].append(d)
        else:
            index["other"].append(d)

    return index


# ── Helpers ──

def _parse_dp(value: str) -> float:
    """Parse a dimension string like '8dp', '12.5dp', '0' into a float dp value."""
    if not value:
        return 0.0
    # Strip dp/dip/px/sp suffix, take the numeric part
    match = re.match(r"([+-]?\d+(?:\.\d+)?)", value.strip())
    if match:
        return float(match.group(1))
    return 0.0


def _strip_ns(tag: str) -> str:
    """Strip XML namespace from tag name."""
    if "}" in tag:
        return tag.split("}")[-1]
    return tag


def _count_children(root) -> int:
    """Count direct children of an XML element."""
    return len(list(root))
