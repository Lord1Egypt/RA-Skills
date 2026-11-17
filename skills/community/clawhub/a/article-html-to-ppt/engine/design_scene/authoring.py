"""Compact author input and atomic object patches; no task-authored code."""
from __future__ import annotations

import copy
import re
from collections import Counter

from jsonschema import Draft202012Validator

from .contract import PROVENANCE, validate, versions, walk
from .store import DesignError, canonical, digest

FORMAT = "pptsmith-author/1"
ROLES = {"text": "native_text", "shape": "native_shape", "path": "native_shape",
         "chart": "native_chart", "table": "native_table", "image": "replaceable_image", "group": "group"}
STYLE_KEYS = {"font", "style", "align", "valign", "wrap", "line_spacing", "margin",
              "letter_spacing", "colors", "legend", "labels", "fill", "header_fill", "header_color"}
AUTHOR_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["format", "task"],
    "properties": {
        "format": {"const": FORMAT}, "task": {"type": "object"},
        "tokens": {"type": "object", "maxProperties": 200},
        "styles": {"type": "object", "maxProperties": 300},
        "sources": {"type": "object", "maxProperties": 3000, "additionalProperties": PROVENANCE},
        "symbols": {"type": "object", "maxProperties": 100},
    },
}


def merge(base, changes):
    result = copy.deepcopy(base)
    for key, value in changes.items():
        result[key] = merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else copy.deepcopy(value)
    return result


def _checked_keys(value, allowed, code):
    if not isinstance(value, dict) or set(value) - set(allowed):
        raise DesignError(code)


def expand(document):
    error = next(Draft202012Validator(AUTHOR_SCHEMA).iter_errors(document), None)
    if error:
        raise DesignError("AUTHOR_SCHEMA_INVALID: " + error.message[:240])
    canonical(document)
    tokens = document.get("tokens", {})
    if any(not re.fullmatch(r"[A-Za-z][\w.-]{0,79}", k) or
           not isinstance(v, (str, int, float, bool)) or isinstance(v, str) and v.startswith("$")
           for k, v in tokens.items()):
        raise DesignError("INVALID_DESIGN_TOKEN")

    def resolve(value, depth=0):
        if depth > 30:
            raise DesignError("AUTHOR_DEPTH_LIMIT")
        if isinstance(value, str) and value.startswith("$"):
            if value[1:] not in tokens:
                raise DesignError("UNKNOWN_DESIGN_TOKEN: " + value[:80])
            return tokens[value[1:]]
        if isinstance(value, dict):
            return {k: resolve(v, depth + 1) for k, v in value.items()}
        if isinstance(value, list):
            return [resolve(v, depth + 1) for v in value]
        return value

    # Tokens apply to design properties only, never business text or provenance.
    styles = resolve(document.get("styles", {}))
    for value in styles.values():
        _checked_keys(value, STYLE_KEYS, "INVALID_STYLE_FIELDS")
    symbols = document.get("symbols", {})
    count = [0]

    def node(spec, page_id, index, depth=0):
        if depth > 6:
            raise DesignError("AUTHOR_GROUP_DEPTH_LIMIT")
        count[0] += 1
        if count[0] > 3000:
            raise DesignError("NODE_COUNT_LIMIT")
        value = copy.deepcopy(spec)
        style_id = value.pop("style_ref", None)
        if style_id is not None:
            if style_id not in styles:
                raise DesignError("UNKNOWN_STYLE: " + str(style_id)[:80])
            value = merge(styles[style_id], value)
        symbol_id = value.pop("symbol_ref", None)
        if symbol_id is not None:
            _checked_keys(value, {"id", "page_id", "box", "z"}, "INVALID_SYMBOL_INSTANCE")
            symbol = symbols.get(symbol_id)
            _checked_keys(symbol, {"width", "height", "nodes"}, "INVALID_SYMBOL")
            if set(symbol) != {"width", "height", "nodes"} or not isinstance(symbol["nodes"], list):
                raise DesignError("INVALID_SYMBOL")
            geometry = resolve(value["box"])
            if (not isinstance(geometry, dict) or set(geometry) != {"x", "y", "width", "height"} or
                    any(not isinstance(v, (int, float)) or isinstance(v, bool) for v in geometry.values()) or
                    not 0 < geometry["width"] <= 10000 or not 0 < geometry["height"] <= 10000):
                raise DesignError("INVALID_SYMBOL_INSTANCE_GEOMETRY")
            width, height = symbol["width"], symbol["height"]
            if not isinstance(width, (int, float)) or not isinstance(height, (int, float)) or min(width, height) <= 0:
                raise DesignError("INVALID_SYMBOL_SIZE")
            sx, sy = geometry["width"] / width, geometry["height"] / height
            if abs(sx / sy - 1) > 0.002:
                raise DesignError("SYMBOL_ASPECT_MISMATCH")
            children = [node(n, page_id, i, depth + 1) for i, n in enumerate(symbol["nodes"])]
            for child, *_ in walk(children):
                if child["type"] not in {"shape", "path", "group"}:
                    raise DesignError("SYMBOL_DECORATION_ONLY")
                child["id"] = value["id"] + "_" + child["id"]
                child["box"] = {k: v * (sx if k in {"x", "width"} else sy) for k, v in child["box"].items()}
                if "style" in child and "stroke_width" in child["style"]:
                    child["style"]["stroke_width"] *= sx
                for command in child.get("commands", []):
                    command["points"] = [[x * sx, y * sy] for x, y in command["points"]]
            value.update(type="group", role="group", box=geometry, children=children)
        else:
            value = resolve(value)
            if value.get("type") == "group":
                value["children"] = [node(n, page_id, i, depth + 1) for i, n in enumerate(value["children"])]
        value.setdefault("page_id", page_id)
        value.setdefault("role", ROLES.get(value.get("type")))
        value.setdefault("z", index)
        if value.get("type") == "text":
            for k, v in {"align": "left", "valign": "top", "wrap": True}.items():
                value.setdefault(k, v)
        return value

    task = copy.deepcopy(document["task"])
    for item in task["content"]["items"]:
        source_id = item.pop("source_ref", None)
        if source_id is not None:
            if "provenance" in item or source_id not in document.get("sources", {}):
                raise DesignError("AMBIGUOUS_OR_UNKNOWN_SOURCE")
            item["provenance"] = copy.deepcopy(document["sources"][source_id])
    for page in task["scene"]["pages"]:
        page["background"] = resolve(page["background"])
        page["nodes"] = [node(n, page["id"], i) for i, n in enumerate(page["nodes"])]
    validate(task, complete=True)
    return task


def compact(task):
    """Lossless projection of a strict task; never asks a model to rewrite it."""
    validate(task, complete=True)
    result = {"format": FORMAT, "task": copy.deepcopy(task), "sources": {}, "styles": {}}
    sources = {canonical(c["provenance"]) for c in task["content"]["items"]}
    source_ids = {s: "source-" + str(i + 1) for i, s in enumerate(sorted(sources))}
    for item in result["task"]["content"]["items"]:
        ident = source_ids[canonical(item["provenance"])]
        result["sources"][ident] = item.pop("provenance")
        item["source_ref"] = ident
    fonts = Counter(canonical(n["font"]) for p in task["scene"]["pages"] for n, *_ in walk(p["nodes"]) if "font" in n)
    style_ids = {s: "font-" + str(i + 1) for i, s in enumerate(sorted(k for k, v in fonts.items() if v > 1))}

    def shrink(nodes, page_id):
        for i, n in enumerate(nodes):
            if n.get("page_id") == page_id:
                n.pop("page_id")
            if n.get("role") == ROLES[n["type"]]:
                n.pop("role")
            if n.get("z") == i:
                n.pop("z")
            if "font" in n and canonical(n["font"]) in style_ids:
                ident = style_ids[canonical(n["font"])]
                result["styles"][ident] = {"font": n.pop("font")}
                n["style_ref"] = ident
            if n["type"] == "text":
                for k, v in {"align": "left", "valign": "top", "wrap": True}.items():
                    if n.get(k) == v:
                        n.pop(k)
            if n["type"] == "group":
                shrink(n["children"], page_id)

    for page in result["task"]["scene"]["pages"]:
        shrink(page["nodes"], page["id"])
    if canonical(expand(result)) != canonical(task):
        raise DesignError("COMPACT_ROUNDTRIP_FAILED")
    return result


def apply_updates(task, patch):
    _checked_keys(patch, {"base_task_sha256", "updates"}, "INVALID_PATCH")
    if patch.get("base_task_sha256") != versions(task)["task"]:
        raise DesignError("PATCH_STALE_INPUT")
    updates = patch.get("updates")
    if not isinstance(updates, list) or not 1 <= len(updates) <= 3000:
        raise DesignError("INVALID_PATCH_UPDATES")
    candidate = copy.deepcopy(task)
    indexes = {
        "node": {n["id"]: n for p in candidate["scene"]["pages"] for n, *_ in walk(p["nodes"])},
        "content": {c["id"]: c for c in candidate["content"]["items"]},
        "notes": {n["page_id"]: n for n in candidate["content"]["notes"]},
        "design": {p["page_id"]: p for p in candidate["design"]["pages"]},
        "page": {p["id"]: p for p in candidate["scene"]["pages"]},
    }
    affected = set()
    for update in updates:
        _checked_keys(update, {"target", "id", "changes"}, "INVALID_PATCH_UPDATE")
        kind, ident, changes = update.get("target"), update.get("id"), update.get("changes")
        if kind not in indexes or ident not in indexes[kind]:
            raise DesignError("PATCH_TARGET_NOT_FOUND")
        if not isinstance(changes, dict) or not changes or set(changes) & {"id", "page_id", "type", "role", "children", "nodes"}:
            raise DesignError("PATCH_IMMUTABLE_OR_EMPTY_FIELDS")
        if kind == "page" and set(changes) != {"background"}:
            raise DesignError("PATCH_PAGE_BACKGROUND_ONLY")
        target = indexes[kind][ident]
        affected.add(target.get("page_id", target.get("id")))
        replacement = merge(target, changes)
        target.clear()
        target.update(replacement)
    validate(candidate, complete=True)
    return candidate, sorted(affected)
