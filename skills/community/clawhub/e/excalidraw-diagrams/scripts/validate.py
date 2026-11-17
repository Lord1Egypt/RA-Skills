#!/usr/bin/env python3
"""Check an Excalidraw file (.excalidraw or Obsidian .md) before handing it over.

Read-only and stdlib only. Prints one JSON object with ok, errors, warnings and
stats. Errors mean the file will not open or will render broken; warnings are
readability problems.

Usage:
    validate.py "Diagrams/flow.excalidraw.md"
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

KNOWN_TYPES = {"rectangle", "ellipse", "diamond", "text", "arrow", "line", "freedraw", "image", "frame", "magicframe", "embeddable", "iframe"}
KNOWN_FONTS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
SHAPES = {"rectangle", "ellipse", "diamond"}
REQUIRED = ("id", "type", "x", "y", "width", "height")
DRAWING_RE = re.compile(r"## Drawing\s*\n```(json|compressed-json)\n(.*?)\n```", re.S)


def extract_scene(path: Path) -> Tuple[Optional[Dict[str, Any]], List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, [f"cannot read UTF-8 file: {exc}"], warnings
    if path.suffix == ".md":
        frontmatter = re.match(r"\A---[^\S\n]*\n(.*?)\n---(?:\n|$)", text, re.S)
        if not frontmatter or not re.search(r"^excalidraw-plugin:[ \t]*\S+", frontmatter.group(1), re.M):
            errors.append("frontmatter is missing 'excalidraw-plugin: parsed'")
        match = DRAWING_RE.search(text)
        if not match:
            errors.append("no '## Drawing' section with a ```json block")
            return None, errors, warnings
        if match.group(1) == "compressed-json":
            warnings.append("drawing is compressed; only the frontmatter was checked")
            return None, errors, warnings
        if "## Text Elements" not in text:
            warnings.append("no '## Text Elements' section; Obsidian search will not see the labels")
        body = match.group(2)
    else:
        body = text
    try:
        data = json.loads(body)
    except ValueError as exc:
        errors.append(f"drawing JSON does not parse: {exc}")
        return None, errors, warnings
    if not isinstance(data, dict) or data.get("type") != "excalidraw":
        errors.append("top-level object must have type 'excalidraw'")
        return None, errors, warnings
    if not isinstance(data.get("elements"), list):
        errors.append("'elements' must be a list")
        return None, errors, warnings
    return data, errors, warnings


def _overlap(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return (a["x"] < b["x"] + b["width"] and b["x"] < a["x"] + a["width"]
            and a["y"] < b["y"] + b["height"] and b["y"] < a["y"] + a["height"])


def check_elements(elements: List[Any]) -> Tuple[List[str], List[str], Dict[str, int]]:
    errors: List[str] = []
    warnings: List[str] = []
    by_id: Dict[str, Dict[str, Any]] = {}
    live = []
    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            errors.append(f"element {i} is not an object")
            continue
        missing = [k for k in REQUIRED if k not in el]
        if missing:
            errors.append(f"element {i} is missing {', '.join(missing)}")
            continue
        if not isinstance(el["id"], str) or not el["id"]:
            errors.append(f"element {i}: id must be a non-empty string")
            continue
        if not isinstance(el["type"], str):
            errors.append(f"{el['id']}: type must be a string")
            continue
        if el["id"] in by_id:
            errors.append(f"duplicate id {el['id']}")
        by_id[el["id"]] = el
        if el["type"] not in KNOWN_TYPES:
            errors.append(f"{el['id']}: unknown type {el['type']!r}")
        if el.get("isDeleted"):
            continue
        live.append(el)
        for key in ("x", "y", "width", "height", "opacity", "fontSize", "fontFamily"):
            if key in el and (type(el[key]) not in (int, float) or not math.isfinite(el[key])):
                errors.append(f"{el['id']}: {key} must be a finite number")
        if el.get("containerId") is not None and not isinstance(el["containerId"], str):
            errors.append(f"{el['id']}: containerId must be a string or null")
        bounds = el.get("boundElements")
        if bounds is not None and (not isinstance(bounds, list) or any(
            not isinstance(b, dict) or not isinstance(b.get("id"), str)
            or b.get("type") not in ("text", "arrow") for b in bounds
        )):
            errors.append(f"{el['id']}: boundElements must contain text/arrow references or be null")
        for side in ("startBinding", "endBinding"):
            binding = el.get(side)
            if binding is not None and (not isinstance(binding, dict) or not isinstance(binding.get("elementId"), str)):
                errors.append(f"{el['id']}: {side} must reference an element or be null")
        if el["type"] in {"arrow", "line"}:
            points = el.get("points")
            if not isinstance(points, list) or len(points) < 2 or any(
                not isinstance(pt, list) or len(pt) != 2 or any(
                    type(n) not in (int, float) or not math.isfinite(n) for n in pt
                ) for pt in points
            ):
                errors.append(f"{el['id']}: points must contain at least two finite coordinate pairs")

    # Structural errors must not reach geometry or binding checks.
    if errors:
        return errors, warnings, {}

    for el in live:
        eid = el["id"]
        if el["type"] == "text":
            if not isinstance(el.get("text"), str):
                errors.append(f"{eid}: text element without text")
            if el.get("fontFamily") not in KNOWN_FONTS:
                warnings.append(f"{eid}: unknown fontFamily {el.get('fontFamily')!r}")
            if isinstance(el.get("fontSize"), (int, float)) and el["fontSize"] < 14:
                warnings.append(f"{eid}: font size {el['fontSize']} is hard to read; use 14 or more")
            cid = el.get("containerId")
            if cid:
                container = by_id.get(cid)
                if container is None:
                    errors.append(f"{eid}: containerId {cid} does not exist")
                elif not any(b.get("id") == eid for b in (container.get("boundElements") or [])):
                    errors.append(f"{eid}: container {cid} does not list this text in boundElements")
        if el["type"] in {"arrow", "line"}:
            points = el.get("points")
            if not isinstance(points, list) or len(points) < 2:
                errors.append(f"{eid}: arrow or line needs at least two points")
            for side in ("startBinding", "endBinding"):
                binding = el.get(side)
                if not binding:
                    continue
                target = by_id.get(binding.get("elementId"))
                if target is None:
                    errors.append(f"{eid}: {side} points to missing element {binding.get('elementId')}")
                elif not any(b.get("id") == eid for b in (target.get("boundElements") or [])):
                    errors.append(f"{eid}: {target['id']} does not list this arrow in boundElements")
        for bound in el.get("boundElements") or []:
            other = by_id.get(bound.get("id"))
            if other is None:
                errors.append(f"{eid}: boundElements lists missing element {bound.get('id')}")
            elif bound.get("type") == "text" and other.get("containerId") != eid:
                errors.append(f"{eid}: bound text {other['id']} has containerId {other.get('containerId')!r}")
            elif bound.get("type") == "arrow" and not any(
                (other.get(side) or {}).get("elementId") == eid for side in ("startBinding", "endBinding")
            ):
                errors.append(f"{eid}: bound arrow {other['id']} does not bind back to this element")

    shapes = [el for el in live if el["type"] in SHAPES and el.get("opacity", 100) >= 60]
    for i, a in enumerate(shapes):
        for b in shapes[i + 1:]:
            if _overlap(a, b):
                warnings.append(f"shapes {a['id']} and {b['id']} overlap")

    stats = {
        "elements": len(live),
        "shapes": sum(1 for el in live if el["type"] in SHAPES),
        "arrows": sum(1 for el in live if el["type"] == "arrow"),
        "texts": sum(1 for el in live if el["type"] == "text"),
    }
    return errors, warnings, stats


def validate(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {"ok": False, "errors": [f"file not found: {path}"], "warnings": []}
    data, errors, warnings = extract_scene(path)
    stats: Dict[str, int] = {}
    if data is not None:
        e2, w2, stats = check_elements(data["elements"])
        errors += e2
        warnings += w2
    return {"ok": not errors, "path": str(path), "errors": errors, "warnings": warnings, "stats": stats}


def main(argv: Optional[List[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] in {"-h", "--help"}:
        print(__doc__.strip())
        return 2
    result = validate(Path(args[0]).expanduser())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
