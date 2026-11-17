"""Strict scene contract and cross-record semantic validation (points only)."""
from __future__ import annotations

import math
from collections import Counter

from jsonschema import Draft202012Validator

from .store import DesignError, canonical, digest


def obj(props, required=None):
    return {"type": "object", "properties": props, "required": list(props) if required is None else required,
            "additionalProperties": False}


def arr(items, maximum=1000, minimum=0):
    return {"type": "array", "items": items, "maxItems": maximum, "minItems": minimum}


def enum(*values):
    return {"enum": list(values)}


def num(low=0, high=10000):
    return {"type": "number", "minimum": low, "maximum": high}


TEXT = {"type": "string", "maxLength": 12000}
SHORT = {"type": "string", "minLength": 1, "maxLength": 500}
ID = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,79}$"}
SHA = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
COLOR = {"type": "string", "pattern": "^[0-9A-Fa-f]{6}$"}
BOOL = {"type": "boolean"}
BOX = obj({"x": num(), "y": num(), "width": num(0.1), "height": num(0.1)})
FONT = obj({"family": SHORT, "size": num(6, 200), "color": COLOR,
            "bold": BOOL, "italic": BOOL}, ["family", "size", "color"])
STYLE = obj({"fill": {"anyOf": [COLOR, {"type": "null"}]},
             "stroke": {"anyOf": [COLOR, {"type": "null"}]}, "stroke_width": num(0, 20)}, [])
PROVENANCE = obj({"kind": enum("user", "visible_transcription", "document", "unknown"),
                  "source": SHORT, "checked": BOOL, "uncertainties": arr(SHORT, 30)})
SERIES = obj({"name": SHORT, "values": arr(num(-1e12, 1e12), 200, 1)})
CONTENT_COMMON = {"id": ID, "page_id": ID, "provenance": PROVENANCE,
                  "required_edit": enum("native", "raster_accepted")}


def variant(common, kind, properties, optional=()):
    p = {**common, "type": {"const": kind}, **properties}
    return obj(p, [k for k in p if k not in optional])


CONTENT = {"oneOf": [
    variant(CONTENT_COMMON, "text", {"text": TEXT}),
    variant(CONTENT_COMMON, "chart", {"categories": arr(SHORT, 200, 1), "series": arr(SERIES, 20, 1),
                                     "data_basis": enum("user_data", "readable_values", "unknown")}),
    variant(CONTENT_COMMON, "table", {"cells": arr(arr(TEXT, 50, 1), 200, 1)}),
    variant(CONTENT_COMMON, "unknown_data", {"description": SHORT}),
]}
BASE = {"id": ID, "page_id": ID, "box": BOX, "z": {"type": "integer", "minimum": -10000, "maximum": 10000}}
PATH_COMMAND = {"oneOf": [
    obj({"op": {"const": op}, "points": arr(arr(num(0, 10000), 2, 2), count, count)})
    for op, count in [("M", 1), ("L", 1), ("Q", 2), ("C", 3), ("Z", 0)]
]}
NODE = {"oneOf": [
    variant(BASE, "text", {"role": {"const": "native_text"}, "content_id": ID, "font": FONT,
                           "align": enum("left", "center", "right"),
                           "valign": enum("top", "middle", "bottom"), "wrap": BOOL,
                           "line_spacing": num(0.8, 3), "margin": num(0, 50),
                           "letter_spacing": num(0, 20),
                           "spans": arr(obj({"start": {"type": "integer", "minimum": 0},
                                             "end": {"type": "integer", "minimum": 1}, "font": FONT}), 100)},
            ("line_spacing", "margin", "spans", "letter_spacing")),
    variant(BASE, "shape", {"role": {"const": "native_shape"},
                            "shape": enum("rect", "rounded_rect", "ellipse", "line", "arrow", "diamond", "triangle"),
                            "style": STYLE}),
    variant(BASE, "path", {"role": {"const": "native_shape"}, "commands": arr(PATH_COMMAND, 512, 2), "style": STYLE}),
    variant(BASE, "chart", {"role": {"const": "native_chart"}, "content_id": ID,
                            "chart_type": enum("bar", "column", "line", "pie", "doughnut"),
                            "font": FONT, "colors": arr(COLOR, 20, 1), "legend": BOOL, "labels": BOOL,
                            "label_colors": arr(COLOR, 200, 1), "label_number_format": SHORT,
                            "legend_position": enum("bottom", "right"), "hole_size": num(10, 90)},
            ("label_colors", "label_number_format", "legend_position", "hole_size")),
    variant(BASE, "table", {"role": {"const": "native_table"}, "content_id": ID, "font": FONT,
                            "fill": COLOR, "header_fill": COLOR, "header_color": COLOR,
                            "column_widths": arr(num(0.1), 50, 1)}, ("column_widths",)),
    variant(BASE, "image", {"role": {"const": "replaceable_image"}, "asset_id": ID,
                            "fit": enum("contain", "cover"), "content_id": ID}, ("content_id",)),
    variant(BASE, "group", {"role": {"const": "group"}, "children": arr({"$ref": "#/$defs/node"}, 500, 1)}),
]}
ASSET = obj({"id": ID, "sha256": SHA, "original_sha256": SHA, "width": {"type": "integer", "minimum": 1},
             "height": {"type": "integer", "minimum": 1}, "page_ids": arr(ID, 60, 1),
             "role": enum("reference", "target", "photo", "illustration", "raster_data"), "source": SHORT,
             "crop": arr({"type": "integer", "minimum": 0}, 4, 4),
             "tool_result": obj({"tool": SHORT, "model": {"anyOf": [SHORT, {"type": "null"}]},
                                  "result_sha256": SHA, "prompt_sha256": SHA,
                                  "request_sha256": SHA,
                                  "invocation_id": {"anyOf": [SHORT, {"type": "null"}]}},
                                 ["tool", "model", "result_sha256", "prompt_sha256", "invocation_id"])},
            ["id", "sha256", "original_sha256", "width", "height", "page_ids", "role", "source"])
REFERENCE = obj({"asset_id": ID, "page_ids": arr(ID, 60, 1),
                 "roles": arr(enum("reconstruction_target", "style", "content", "material"), 4, 1),
                 "priority": {"type": "integer", "minimum": 0, "maximum": 100}, "features": arr(SHORT, 40)})
REVIEW_PROFILE = enum("decorative_business")
COMPOSITION = obj({
    "page_role": enum("cover", "contents", "section", "body", "closing"),
    "claim_content_id": ID,
    "content_relation": SHORT,
    "layout_family": SHORT,
    "reading_path": arr(ID, 500, 1),
    "information_attachment": enum("inside_structure", "along_path", "paired_with_visual", "mixed"),
    "layer_plan": obj({"primary": SHORT, "secondary": SHORT, "detail": SHORT}),
    "rationale": SHORT,
}, ["page_role", "content_relation", "layout_family", "reading_path", "information_attachment",
    "layer_plan", "rationale"])
DESIGN_PAGE = obj({"page_id": ID, "target_asset_id": ID, "confirmed_by": SHORT,
                   "target_content_sha256": SHA, "target_context_sha256": SHA,
                   "target_kind": enum("original", "generated", "provided_design", "approved_revision"),
                   "quality_limits": arr(SHORT, 30), "accepted_differences": arr(SHORT, 30),
                   "aspect_policy": enum("exact", "contain"),
                   "raster_acceptances": arr(obj({"content_id": ID, "reason": SHORT, "accepted_by": SHORT}), 100),
                   "composition": COMPOSITION},
                  ["page_id", "quality_limits", "accepted_differences", "aspect_policy", "raster_acceptances"])
SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:pptsmith:design-task:1",
    **obj({"schema_version": enum("1.0", "1.1"), "task_id": ID, "author_id": SHORT,
           "mode": enum("create", "recreate", "style_transfer", "new_design", "draft", "template"),
           "audience": SHORT, "language": SHORT, "target_software": SHORT,
           "canvas": obj({"width": num(72, 4000), "height": num(72, 4000), "unit": {"const": "pt"}}),
           "content": obj({"items": arr(CONTENT, 3000), "notes": arr(obj({"page_id": ID, "text": TEXT}), 60)}),
           "design": obj({"brief": TEXT, "references": arr(REFERENCE, 120), "pages": arr(DESIGN_PAGE, 60, 1),
                          "revision_budget": {"type": "integer", "minimum": 1, "maximum": 10},
                          "requires_style_reference": BOOL, "review_profile": REVIEW_PROFILE},
                         ["brief", "references", "pages", "revision_budget"]),
           "scene": obj({"pages": arr(obj({"id": ID, "background": COLOR, "nodes": arr({"$ref": "#/$defs/node"}, 500)}), 60, 1)}),
           "assets": obj({"items": arr(ASSET, 500)})}),
    "$defs": {"node": NODE},
}


def walk(nodes, depth=0, ox=0, oy=0):
    if depth > 6:
        raise DesignError("GROUP_DEPTH_LIMIT")
    for n in nodes:
        yield n, depth, ox, oy
        if n["type"] == "group":
            yield from walk(n["children"], depth + 1, ox + n["box"]["x"], oy + n["box"]["y"])


def _unique(items, key, code):
    keys = [x[key] for x in items]
    if len(set(keys)) != len(keys):
        raise DesignError(code)
    return {x[key]: x for x in items}


def validate(task: dict, *, complete=False):
    try:
        canonical(task)  # rejects NaN/Infinity, even when called without JSON loader
        error = next(Draft202012Validator(SCHEMA).iter_errors(task), None)
    except (ValueError, RecursionError) as exc:
        raise DesignError(f"INVALID_TASK: {exc}") from exc
    if error:
        e = error
        raise DesignError(f"SCHEMA_INVALID: {'/'.join(map(str, e.absolute_path))}: {e.message[:350]}")
    if task["mode"] == "template":
        raise DesignError("TEMPLATE_ROUTE_REQUIRED: use the template preservation workflow")
    pages = _unique(task["scene"]["pages"], "id", "DUPLICATE_PAGE")
    designs = _unique(task["design"]["pages"], "page_id", "DUPLICATE_DESIGN_PAGE")
    content = _unique(task["content"]["items"], "id", "DUPLICATE_CONTENT")
    assets = _unique(task["assets"]["items"], "id", "DUPLICATE_ASSET")
    if sum(a["width"] * a["height"] for a in assets.values()) > 96_000_000:
        raise DesignError("TOTAL_ASSET_PIXEL_LIMIT")
    if set(pages) != set(designs):
        raise DesignError("DESIGN_PAGE_MAPPING_MISMATCH")
    if complete and task["mode"] == "create":
        if not task["design"]["brief"].strip():
            raise DesignError("DESIGN_BRIEF_REQUIRED")
        notes = _unique(task["content"]["notes"], "page_id", "DUPLICATE_NOTES")
        if set(notes) != set(pages) or any(not n["text"].strip() for n in notes.values()):
            raise DesignError("SPEAKER_NOTES_REQUIRED")
    for item in [*content.values(), *task["content"]["notes"]]:
        if item["page_id"] not in pages:
            raise DesignError("CONTENT_PAGE_MISMATCH")
    for a in assets.values():
        if not set(a["page_ids"]) <= set(pages) or a["width"] * a["height"] > 32_000_000:
            raise DesignError("ASSET_PAGE_OR_SIZE_MISMATCH")
        if "tool_result" in a and a["tool_result"]["result_sha256"] != a["original_sha256"]:
            raise DesignError("TOOL_RESULT_HASH_MISMATCH")
    for ref in task["design"]["references"]:
        a = assets.get(ref["asset_id"])
        if not a or not set(ref["page_ids"]) <= set(a["page_ids"]):
            raise DesignError("REFERENCE_PAGE_MISMATCH")
    seen, bindings, warnings = set(), Counter(), []
    for pid, page in pages.items():
        design = designs[pid]
        composition = design.get("composition")
        if complete and task["design"].get("review_profile") == "decorative_business" and not composition:
            raise DesignError("PAGE_COMPOSITION_REQUIRED: " + pid)
        if composition:
            prose = [composition[k] for k in ("content_relation", "layout_family", "rationale")]
            if any(not value.strip() for value in [*prose, *composition["layer_plan"].values()]):
                raise DesignError("COMPOSITION_REASONING_REQUIRED: " + pid)
            reading = composition["reading_path"]
            if len(reading) != len(set(reading)):
                raise DesignError("COMPOSITION_READING_PATH_DUPLICATE: " + pid)
            if any(cid not in content or content[cid]["page_id"] != pid for cid in reading):
                raise DesignError("COMPOSITION_CONTENT_PAGE_MISMATCH: " + pid)
            claim = composition.get("claim_content_id")
            if composition["page_role"] == "body" and not claim:
                raise DesignError("COMPOSITION_CLAIM_REQUIRED: " + pid)
            if claim and (claim not in reading or content.get(claim, {}).get("page_id") != pid
                          or content[claim]["type"] != "text" or not content[claim]["text"].strip()):
                raise DesignError("COMPOSITION_CLAIM_INVALID: " + pid)
        target = assets.get(design.get("target_asset_id"))
        if design.get("target_asset_id") and not target:
            raise DesignError("DESIGN_TARGET_ASSET_MISSING")
        if not target and any(k in design for k in ("target_kind", "confirmed_by", "target_content_sha256", "target_context_sha256")):
            raise DesignError("TARGET_METADATA_WITHOUT_ASSET")
        if complete and task["mode"] not in {"create", "draft"} and (not target or not design.get("confirmed_by") or not design.get("target_kind")):
            raise DesignError(f"DESIGN_TARGET_REQUIRED: {pid}")
        if target:
            from .targets import visible_content, target_context
            for field, value in (("target_content_sha256", visible_content(task, pid)),
                                 ("target_context_sha256", target_context(task, pid))):
                if field in design and design[field] != digest(canonical(value)):
                    raise DesignError(f"STALE_DESIGN_TARGET: {pid}/{field}")
            if complete and (not design.get("confirmed_by") or not design.get("target_kind")):
                raise DesignError(f"DESIGN_TARGET_REQUIRED: {pid}")
            if pid not in target["page_ids"] or target["role"] not in {"reference", "target"}:
                raise DesignError("TARGET_PAGE_OR_ROLE_MISMATCH")
            aspect = task["canvas"]["width"] / task["canvas"]["height"]
            if abs(target["width"] / target["height"] / aspect - 1) > .002 and design["aspect_policy"] == "exact":
                raise DesignError("ASPECT_RATIO_MISMATCH: choose contain or separate decks")
            if task["mode"] == "recreate" and design.get("target_kind") == "original":
                if not any(r["asset_id"] == target["id"] and pid in r["page_ids"] and
                           "reconstruction_target" in r["roles"] for r in task["design"]["references"]):
                    raise DesignError("ORIGINAL_REFERENCE_REQUIRED")
            if design.get("target_kind") == "generated" and "tool_result" not in target:
                raise DesignError("ACTUAL_IMAGE_TOOL_RESULT_REQUIRED")
            if task["mode"] in {"create", "style_transfer", "new_design"} and design.get("target_kind") == "original":
                raise DesignError("NEW_CONTENT_REQUIRES_NEW_DESIGN_TARGET")
            if task["mode"] == "recreate" and design.get("target_kind") != "original" and not design["accepted_differences"]:
                raise DesignError("REFERENCE_CHANGE_REQUIRES_DIFFERENCE_RECORD")
        if complete and (task["mode"] == "style_transfer" or task["design"].get("requires_style_reference")) and not any(pid in r["page_ids"] and "style" in r["roles"] for r in task["design"]["references"]):
            raise DesignError("STYLE_REFERENCE_REQUIRED")
        if complete and not page["nodes"]:
            raise DesignError("EMPTY_SCENE")
        if complete and task["mode"] == "create" and not any(c["page_id"] == pid for c in content.values()):
            raise DesignError("PAGE_CONTENT_REQUIRED: " + pid)
        for node, depth, ox, oy in walk(page["nodes"]):
            if node["id"] in seen or node["page_id"] != pid:
                raise DesignError("NODE_ID_OR_PAGE_MISMATCH")
            seen.add(node["id"])
            if len(seen) > 3000:
                raise DesignError("NODE_COUNT_LIMIT")
            b = node["box"]
            if ox + b["x"] + b["width"] > task["canvas"]["width"] + .01 or oy + b["y"] + b["height"] > task["canvas"]["height"] + .01:
                raise DesignError(f"NODE_OUT_OF_BOUNDS: {node['id']}")
            if node["type"] == "group":
                for child in node["children"]:
                    c = child["box"]
                    if c["x"] + c["width"] > b["width"] + .01 or c["y"] + c["height"] > b["height"] + .01:
                        raise DesignError("GROUP_CHILD_OUT_OF_BOUNDS")
            if node["type"] == "path":
                if node["commands"][0]["op"] != "M":
                    raise DesignError("PATH_MUST_START_WITH_MOVE")
                for command in node["commands"]:
                    if any(x > b["width"] or y > b["height"] for x, y in command["points"]):
                        raise DesignError("PATH_POINT_OUT_OF_BOUNDS")
            if node["type"] == "image":
                a = assets.get(node["asset_id"])
                if not a or pid not in a["page_ids"]:
                    raise DesignError("IMAGE_ASSET_PAGE_MISMATCH")
                if a["role"] in {"reference", "target"}:
                    raise DesignError("WHOLE_TARGET_IMAGE_NOT_EDITABLE")
                if target and a["sha256"] == target["sha256"] and any(c["page_id"] == pid and c["required_edit"] == "native" for c in content.values()):
                    raise DesignError("RELABELLED_TARGET_IMAGE_NOT_EDITABLE")
                if a["role"] == "raster_data" and "content_id" not in node:
                    raise DesignError("RASTER_DATA_REQUIRES_CONTENT_BINDING")
            cid = node.get("content_id")
            if cid:
                c = content.get(cid)
                if not c or c["page_id"] != pid:
                    raise DesignError("CONTENT_BINDING_PAGE_MISMATCH")
                bindings[cid] += 1
                if node["type"] == "image":
                    if c["required_edit"] != "raster_accepted" or not any(x["content_id"] == cid for x in design["raster_acceptances"]):
                        raise DesignError("NATIVE_CONTENT_REPLACED_BY_IMAGE")
                elif c["type"] != node["type"]:
                    raise DesignError("CONTENT_BINDING_TYPE_MISMATCH")
                elif not c["provenance"]["checked"] or c["provenance"]["kind"] == "unknown":
                    raise DesignError("CONTENT_NOT_CHECKED")
                if node["type"] == "text":
                    last = 0
                    for span in node.get("spans", []):
                        if span["start"] < last or span["end"] <= span["start"] or span["end"] > len(c["text"]):
                            raise DesignError("TEXT_SPAN_RANGE_INVALID")
                        last = span["end"]
                    lines = c["text"].count("\n") + 1
                    if lines * node["font"]["size"] * node.get("line_spacing", 1.15) > b["height"]:
                        warnings.append({"code": "TEXT_HEIGHT_RISK", "node_id": node["id"]})
                if node["type"] == "chart":
                    if c["data_basis"] == "unknown":
                        raise DesignError("UNKNOWN_CHART_DATA")
                    if any(len(s["values"]) != len(c["categories"]) for s in c["series"]):
                        raise DesignError("CHART_DATA_LENGTH_MISMATCH")
                    if node["chart_type"] in {"pie", "doughnut"} and (len(c["series"]) != 1 or any(v < 0 for v in c["series"][0]["values"]) or sum(c["series"][0]["values"]) <= 0):
                        raise DesignError("INVALID_SECTOR_DATA")
                if node["type"] == "table":
                    cols = len(c["cells"][0])
                    if any(len(row) != cols for row in c["cells"]):
                        raise DesignError("RAGGED_TABLE")
                    if "column_widths" in node and (len(node["column_widths"]) != cols or abs(sum(node["column_widths"]) - b["width"]) > .01):
                        raise DesignError("TABLE_COLUMN_WIDTH_MISMATCH")
    if complete and any(bindings[cid] != 1 for cid in content):
        raise DesignError("CONTENT_COVERAGE_MISMATCH: each item needs exactly one editable object or accepted raster")
    from .composition import composition_diagnostics
    warnings.extend(composition_diagnostics(task)["warnings"])
    return {"status": "valid", "warnings": warnings, "nodes": len(seen)}


def versions(task):
    return {**{key: digest(canonical(task[key])) for key in ("content", "design", "scene", "assets")},
            "task": digest(canonical(task))}
