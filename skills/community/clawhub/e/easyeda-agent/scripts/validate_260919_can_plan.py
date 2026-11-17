#!/usr/bin/env python3
"""Validate a 260919 CAN routing candidate before it touches EasyEDA.

The candidate keeps the existing ``pcb.line.create`` payload unchanged.  The
small wrapper only says which action belongs to the ordered main path and which
belongs to the D1 protection branch.  This is deliberately an exam example
validator, not another routing language or autorouter.

Pass ``--components`` with the exact output of
``easyeda pcb list --include-bbox --include-pads`` when the integrated
``pcb dump`` omits source pad geometry.  The direct component response is
content-hashed separately and replaces only ``board.components``; outline and
rules still come from the board dump.  Without it, the validator remains
conservative with legacy pad data: when a pad has no source shape, the larger
reported width/height is used as a square obstacle.  That can reject a legal
route, but cannot turn an unknown rotated rectangle into a false clearance PASS.
Missing arc availability remains an explicit
limitation, so an otherwise clean legacy result is ``unknown`` rather than
``accepted``.  Board/track/via/pour/fill/region inputs are content-hashed without
transport timestamps and bound to one document UUID.  H/L absolute lengths and
segment counts may be retained as historical observations, but do not participate
in this validator's verdict and do not add an equal-length requirement to the exam.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


EPS = 0.05
MIN_SEGMENT_MIL = 1.0
SUPPORTED_SCHEMA = "260919-can-candidate/v1"
EXPECTED = {
    "CANH": {"ordered": ["U5.7", "R12.1", "CN1.2"], "branch": "D1.1"},
    "CANL": {"ordered": ["U5.6", "R12.2", "CN1.1"], "branch": "D1.2"},
}
@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    action_id: str
    net: str
    layer: int
    width: float
    a: Point
    b: Point
    role: str


def canonical_sha256(value: Any) -> str:
    """Hash design content, not transport metadata from a live readback."""
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


SNAPSHOT_RESPONSE_NAMES = ("tracks", "vias", "pours", "fills", "regions")


def snapshot_hashes(
    board: dict[str, Any],
    components: dict[str, Any] | None = None,
    **responses: dict[str, Any],
) -> dict[str, str]:
    # `pcb dump` stamps every read with capturedAt and copies the caller's
    # arbitrary --label into project.  The action response also gets a new
    # request id, timestamp and sequence.  None of those describe PCB state.
    board_content = {key: value for key, value in board.items() if key not in {"capturedAt", "project"}}
    digests = {"boardSha256": canonical_sha256(board_content)}
    if components is not None:
        digests["componentsSha256"] = canonical_sha256(components.get("result", components))
    for name in SNAPSHOT_RESPONSE_NAMES:
        response = responses[name]
        digests[f"{name}Sha256"] = canonical_sha256(response.get("result", response))
    return digests


def response_document_uuid(data: dict[str, Any]) -> str:
    context = data.get("context", {})
    return str(context.get("documentUuid", "")) if isinstance(context, dict) else ""


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def finite(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"expected a finite number, got {value!r}")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"expected a finite number, got {value!r}")
    return value


def same(a: Point, b: Point, tolerance: float = EPS) -> bool:
    return math.hypot(a.x - b.x, a.y - b.y) <= tolerance


def point_on_segment(p: Point, s: Segment, tolerance: float = EPS) -> bool:
    if seg_point_dist(s.a, s.b, p) > tolerance:
        return False
    return (
        min(s.a.x, s.b.x) - tolerance <= p.x <= max(s.a.x, s.b.x) + tolerance
        and min(s.a.y, s.b.y) - tolerance <= p.y <= max(s.a.y, s.b.y) + tolerance
    )


def seg_point_dist(a: Point, b: Point, p: Point) -> float:
    dx, dy = b.x - a.x, b.y - a.y
    if abs(dx) <= EPS and abs(dy) <= EPS:
        return math.hypot(p.x - a.x, p.y - a.y)
    t = max(0.0, min(1.0, ((p.x - a.x) * dx + (p.y - a.y) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p.x - (a.x + t * dx), p.y - (a.y + t * dy))


def orient(a: Point, b: Point, c: Point) -> float:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    def sign(v: float) -> int:
        return 1 if v > EPS else -1 if v < -EPS else 0

    o1, o2, o3, o4 = sign(orient(a, b, c)), sign(orient(a, b, d)), sign(orient(c, d, a)), sign(orient(c, d, b))
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    for p, x, y in ((c, a, b), (d, a, b), (a, c, d), (b, c, d)):
        if abs(orient(x, y, p)) <= EPS and min(x.x, y.x) - EPS <= p.x <= max(x.x, y.x) + EPS and min(x.y, y.y) - EPS <= p.y <= max(x.y, y.y) + EPS:
            return True
    return False


def seg_seg_dist(a: Point, b: Point, c: Point, d: Point) -> float:
    if segments_intersect(a, b, c, d):
        return 0.0
    return min(seg_point_dist(a, b, c), seg_point_dist(a, b, d), seg_point_dist(c, d, a), seg_point_dist(c, d, b))


def collinear_overlap(a: Point, b: Point, c: Point, d: Point) -> float:
    if abs(orient(a, b, c)) > EPS or abs(orient(a, b, d)) > EPS:
        return 0.0
    if abs(b.x - a.x) >= abs(b.y - a.y):
        return max(0.0, min(max(a.x, b.x), max(c.x, d.x)) - max(min(a.x, b.x), min(c.x, d.x)))
    return max(0.0, min(max(a.y, b.y), max(c.y, d.y)) - max(min(a.y, b.y), min(c.y, d.y)))


def point_in_rect(p: Point, rect: tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = rect
    return x1 - EPS <= p.x <= x2 + EPS and y1 - EPS <= p.y <= y2 + EPS


def rect_seg_dist(rect: tuple[float, float, float, float], a: Point, b: Point) -> float:
    x1, y1, x2, y2 = rect
    if point_in_rect(a, rect) or point_in_rect(b, rect):
        return 0.0
    corners = [Point(x1, y1), Point(x2, y1), Point(x2, y2), Point(x1, y2)]
    return min(seg_seg_dist(a, b, corners[i], corners[(i + 1) % 4]) for i in range(4))


def point_in_polygon(p: Point, points: list[Point]) -> bool:
    inside = False
    j = len(points) - 1
    for i, pi in enumerate(points):
        pj = points[j]
        if point_on_segment(p, Segment("outline", "", 0, 0, pj, pi, "outline"), 0.01):
            return True
        crosses = (pi.y > p.y) != (pj.y > p.y)
        if crosses and p.x < (pj.x - pi.x) * (p.y - pi.y) / (pj.y - pi.y) + pi.x:
            inside = not inside
        j = i
    return inside


def action_segment(action: dict[str, Any], role: str) -> Segment:
    if action.get("action") != "pcb.line.create":
        raise ValueError("route_contract_mismatch: only pcb.line.create actions are allowed")
    payload = action.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("route_contract_mismatch: action.payload must be an object")
    action_id = str(action.get("id", "")).strip()
    if not action_id:
        raise ValueError("route_contract_mismatch: every action needs a stable id")
    return Segment(
        action_id=action_id,
        net=str(payload.get("net", "")).strip(),
        layer=int(finite(payload.get("layer"))),
        width=finite(payload.get("lineWidth")),
        a=Point(finite(payload.get("startX")), finite(payload.get("startY"))),
        b=Point(finite(payload.get("endX")), finite(payload.get("endY"))),
        role=role,
    )


def normalized_chain(segments: list[Segment], start: Point) -> tuple[list[Point], list[Segment]] | None:
    points = [start]
    oriented: list[Segment] = []
    current = start
    for segment in segments:
        if same(segment.a, current):
            nxt = segment.b
            item = segment
        elif same(segment.b, current):
            nxt = segment.a
            item = Segment(segment.action_id, segment.net, segment.layer, segment.width, segment.b, segment.a, segment.role)
        else:
            return None
        points.append(nxt)
        oriented.append(item)
        current = nxt
    return points, oriented


def direction(segment: Segment) -> tuple[int, int] | None:
    dx, dy = segment.b.x - segment.a.x, segment.b.y - segment.a.y
    if math.hypot(dx, dy) <= EPS:
        return None
    sx, sy = (0 if abs(dx) <= EPS else (1 if dx > 0 else -1)), (0 if abs(dy) <= EPS else (1 if dy > 0 else -1))
    if sx and sy and not math.isclose(abs(dx), abs(dy), abs_tol=EPS):
        return (99, 99)
    return sx, sy


def turn_degrees(a: Segment, b: Segment) -> float:
    v1 = (a.b.x - a.a.x, a.b.y - a.a.y)
    v2 = (b.b.x - b.a.x, b.b.y - b.a.y)
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    n = math.hypot(*v1) * math.hypot(*v2)
    if n <= EPS:
        return 180.0
    return math.degrees(math.acos(max(-1.0, min(1.0, dot / n))))


def segment_length(segment: Segment) -> float:
    return math.hypot(segment.b.x - segment.a.x, segment.b.y - segment.a.y)


def board_pads(board: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    components: dict[str, dict[str, Any]] = {}
    pads: dict[str, dict[str, Any]] = {}
    for component in board.get("components", []):
        ref = str(component.get("designator", ""))
        components[ref] = component
        for pad in component.get("pads", []):
            pads[f"{ref}.{pad.get('padNumber')}"] = pad | {"reference": ref}
    return components, pads


def pad_center(pad: dict[str, Any]) -> Point:
    return Point(finite(pad.get("x")), finite(pad.get("y")))


def pad_rect(pad: dict[str, Any]) -> tuple[float, float, float, float] | None:
    width = pad.get("width")
    height = pad.get("height")
    if not isinstance(width, (int, float)) or not isinstance(height, (int, float)) or width <= 0 or height <= 0:
        return None
    shape = pad.get("shape")
    # New connector width/height are rendered AABB extents.  Legacy output has
    # no shape, so hypot(width,height) square is a safe rotation-independent
    # hull even for a square rotated 45 degrees.
    if shape is None:
        width = height = math.hypot(float(width), float(height))
    center = pad_center(pad)
    return center.x - width / 2, center.y - height / 2, center.x + width / 2, center.y + height / 2


def pad_external_entry(component: dict[str, Any], pad: dict[str, Any], previous: Point) -> tuple[bool, dict[str, Any]]:
    bbox = component.get("bbox", {})
    if not isinstance(bbox, dict):
        return False, {"reason": "component bbox unavailable"}
    center = Point(
        (finite(bbox.get("minX")) + finite(bbox.get("maxX"))) / 2,
        (finite(bbox.get("minY")) + finite(bbox.get("maxY"))) / 2,
    )
    target = pad_center(pad)
    sibling_centers = [pad_center(item) for item in component.get("pads", []) if isinstance(item, dict)]
    same_row = [item for item in sibling_centers if abs(item.y - target.y) <= 1.0]
    same_column = [item for item in sibling_centers if abs(item.x - target.x) <= 1.0]
    if len(same_row) >= 2 and sibling_centers:
        min_y, max_y = min(item.y for item in sibling_centers), max(item.y for item in sibling_centers)
        if max_y - min_y > 1.0 and abs(target.y - min_y) <= 1.0:
            return previous.y < target.y - EPS, {"outwardSide": "bottom", "previous": [previous.x, previous.y], "padCenter": [target.x, target.y]}
        if max_y - min_y > 1.0 and abs(target.y - max_y) <= 1.0:
            return previous.y > target.y + EPS, {"outwardSide": "top", "previous": [previous.x, previous.y], "padCenter": [target.x, target.y]}
    if len(same_column) >= 2 and sibling_centers:
        min_x, max_x = min(item.x for item in sibling_centers), max(item.x for item in sibling_centers)
        if max_x - min_x > 1.0 and abs(target.x - min_x) <= 1.0:
            return previous.x < target.x - EPS, {"outwardSide": "left", "previous": [previous.x, previous.y], "padCenter": [target.x, target.y]}
        if max_x - min_x > 1.0 and abs(target.x - max_x) <= 1.0:
            return previous.x > target.x + EPS, {"outwardSide": "right", "previous": [previous.x, previous.y], "padCenter": [target.x, target.y]}
    half_x = max(EPS, (finite(bbox.get("maxX")) - finite(bbox.get("minX"))) / 2)
    half_y = max(EPS, (finite(bbox.get("maxY")) - finite(bbox.get("minY"))) / 2)
    nx, ny = (target.x - center.x) / half_x, (target.y - center.y) / half_y
    if abs(nx) >= abs(ny):
        outward = "right" if nx >= 0 else "left"
        ok = previous.x > target.x + EPS if nx >= 0 else previous.x < target.x - EPS
    else:
        outward = "top" if ny >= 0 else "bottom"
        ok = previous.y > target.y + EPS if ny >= 0 else previous.y < target.y - EPS
    return ok, {
        "outwardSide": outward,
        "previous": [previous.x, previous.y],
        "padCenter": [target.x, target.y],
    }


def tracks_from_file(data: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    result = data.get("result", data)
    if not isinstance(result, dict):
        return [], False
    lines = result.get("lines", [])
    return (lines if isinstance(lines, list) else []), result.get("arcsAvailable") is True


def response_items(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    result = data.get("result", data)
    if not isinstance(result, dict):
        return []
    items = result.get(key, [])
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def finding(code: str, message: str, **evidence: Any) -> dict[str, Any]:
    item = {"code": code, "message": message}
    if evidence:
        item["evidence"] = evidence
    return item


def validate(
    plan: dict[str, Any],
    board: dict[str, Any],
    tracks_data: dict[str, Any],
    vias_data: dict[str, Any],
    pours_data: dict[str, Any],
    fills_data: dict[str, Any],
    regions_data: dict[str, Any],
    snapshot_digests: dict[str, str],
    components_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    limitations: list[str] = []
    if plan.get("schema") != SUPPORTED_SCHEMA:
        findings.append(finding("schema_mismatch", f"schema must be {SUPPORTED_SCHEMA}"))
    if plan.get("units") != "mil":
        findings.append(finding("route_contract_mismatch", "units must be mil"))
    source = plan.get("sourceSnapshot", {})
    expected_source = {"documentUuid", *snapshot_digests}
    if not isinstance(source, dict) or set(source) != expected_source or any(source.get(key) != value for key, value in snapshot_digests.items()):
        findings.append(finding("stale_source_snapshot", "candidate hashes do not match the supplied live readback"))
    document_inputs = [tracks_data, vias_data, pours_data, fills_data, regions_data]
    if components_data is not None:
        document_inputs.append(components_data)
    document_uuids = {
        response_document_uuid(data)
        for data in document_inputs
    }
    if "" in document_uuids or len(document_uuids) != 1 or source.get("documentUuid") not in document_uuids:
        findings.append(finding(
            "source_document_mismatch",
            "component/track/via/pour/fill/region snapshots must identify the same target document as the candidate",
            expected=source.get("documentUuid"),
            observed=sorted(document_uuids),
        ))

    board = copy.deepcopy(board)
    if components_data is not None:
        direct = components_data.get("result", components_data)
        direct_components = direct.get("components") if isinstance(direct, dict) else None
        if not isinstance(direct_components, list):
            findings.append(finding("component_snapshot_invalid", "direct component snapshot lacks result.components[]"))
        else:
            board["components"] = copy.deepcopy(direct_components)
    components, pads = board_pads(board)
    # Evaluate a proposed R12 translation against the real baseline without
    # moving the live board first.  Rotation changes are intentionally outside
    # v1; H-left/L-right rot0 is part of this exam example.
    placement = plan.get("placement", {})
    placement = placement.get("R12", {}) if isinstance(placement, dict) else {}
    r12 = components.get("R12", {})
    try:
        live_center = Point(finite(r12.get("x")), finite(r12.get("y")))
        raw_from = placement.get("fromCenter", [live_center.x, live_center.y])
        raw_target = placement.get("center", [])
        if not isinstance(raw_from, list) or len(raw_from) != 2 or not isinstance(raw_target, list) or len(raw_target) != 2:
            raise ValueError("placement.R12 fromCenter/center must be [x,y]")
        from_center = Point(finite(raw_from[0]), finite(raw_from[1]))
        target_center = Point(finite(raw_target[0]), finite(raw_target[1]))
        target_rotation = int(round(finite(placement.get("rotationDeg", 999)))) % 360
        live_rotation = int(round(finite(r12.get("rotation", 999)))) % 360
        if not same(from_center, live_center):
            findings.append(finding("placement_mismatch", "R12 fromCenter does not match the supplied live board snapshot", expected=[live_center.x, live_center.y], observed=[from_center.x, from_center.y]))
        if target_rotation != 0 or live_rotation != 0:
            findings.append(finding("main_pad_order_reversed", "R12 must remain rot0 for H-left/L-right in this example"))
        if target_rotation == 0 and live_rotation == 0:
            dx, dy = target_center.x - live_center.x, target_center.y - live_center.y
            r12["x"], r12["y"] = target_center.x, target_center.y
            bbox = r12.get("bbox")
            if isinstance(bbox, dict):
                for key in ("minX", "maxX"):
                    bbox[key] = finite(bbox[key]) + dx
                for key in ("minY", "maxY"):
                    bbox[key] = finite(bbox[key]) + dy
            for pad in r12.get("pads", []):
                pad["x"] = finite(pad.get("x")) + dx
                pad["y"] = finite(pad.get("y")) + dy
            components, pads = board_pads(board)
    except (ValueError, TypeError) as exc:
        findings.append(finding("placement_mismatch", str(exc)))

    missing = [key for spec in EXPECTED.values() for key in spec["ordered"] + [spec["branch"]] if key not in pads]
    if missing:
        findings.append(finding("missing_pad", "required pads are absent from the board snapshot", pads=sorted(set(missing))))
        return {"verdict": "rejected", "findings": findings, "limitations": limitations}

    contract = plan.get("contract", {})
    try:
        layer = int(finite(contract.get("layer")))
        width = finite(contract.get("widthMil"))
        clearance = finite(contract.get("minClearanceMil"))
        max_vias = int(finite(contract.get("maxVias")))
    except (ValueError, TypeError) as exc:
        findings.append(finding("route_contract_mismatch", str(exc)))
        return {"verdict": "rejected", "findings": findings, "limitations": limitations}
    if (layer, width, clearance, max_vias) != (1, 8.0, 6.0, 0):
        findings.append(finding("route_contract_mismatch", "260919 CAN requires TOP/8mil/6mil/0via", observed=[layer, width, clearance, max_vias]))
    if not (pad_center(pads["R12.1"]).x < pad_center(pads["R12.2"]).x and pads["R12.1"].get("net") == "CANH" and pads["R12.2"].get("net") == "CANL"):
        findings.append(finding("main_pad_order_reversed", "R12.1/H must remain left of R12.2/L"))

    actions = plan.get("actions", [])
    roles = plan.get("actionRoles", {})
    if not isinstance(actions, list) or not isinstance(roles, dict):
        findings.append(finding("route_contract_mismatch", "actions/actionRoles have invalid types"))
        return {"verdict": "rejected", "findings": findings, "limitations": limitations}
    by_id: dict[str, dict[str, Any]] = {}
    for action in actions:
        action_id = str(action.get("id", "")) if isinstance(action, dict) else ""
        if not action_id or action_id in by_id:
            findings.append(finding("route_contract_mismatch", "action ids must be present and unique", actionId=action_id))
            continue
        by_id[action_id] = action

    all_segments: list[Segment] = []
    net_segments: dict[str, list[Segment]] = {"CANH": [], "CANL": []}
    chains: dict[str, dict[str, Any]] = {}
    used_ids: list[str] = []
    for net, expected in EXPECTED.items():
        declared = contract.get("nets", {}).get(net, {})
        if declared.get("orderedMainPads") != expected["ordered"]:
            code = "branch_used_as_main_waypoint" if expected["branch"] in declared.get("orderedMainPads", []) else "ordered_through_missing"
            findings.append(finding(code, f"{net} orderedMainPads must be {expected['ordered']}"))
        if declared.get("branchPads") != [expected["branch"]]:
            findings.append(finding("branch_role_mismatch", f"{net} branchPads must be [{expected['branch']}]"))
        role = roles.get(net, {})
        main_ids = role.get("main", [])
        branch_map = role.get("branches", {})
        branch_ids = branch_map.get(expected["branch"], []) if isinstance(branch_map, dict) else []
        if not main_ids or not branch_ids:
            findings.append(finding("route_contract_mismatch", f"{net} needs non-empty main and {expected['branch']} branch action lists"))
            continue
        try:
            main = [action_segment(by_id[action_id], f"{net}:main") for action_id in main_ids]
            branch = [action_segment(by_id[action_id], f"{net}:branch:{expected['branch']}") for action_id in branch_ids]
        except (KeyError, ValueError) as exc:
            findings.append(finding("route_contract_mismatch", f"{net}: {exc}"))
            continue
        used_ids.extend(main_ids + branch_ids)
        for segment in main + branch:
            if segment.net != net or segment.layer != layer or not math.isclose(segment.width, width, abs_tol=EPS):
                findings.append(finding("route_contract_mismatch", "action net/layer/width differs from the contract", actionId=segment.action_id))
            d = direction(segment)
            if d is None or d == (99, 99):
                findings.append(finding("non_45_segment", "segment must be non-zero and horizontal, vertical, or 45-degree", actionId=segment.action_id))
            length = math.hypot(segment.b.x - segment.a.x, segment.b.y - segment.a.y)
            if length < MIN_SEGMENT_MIL - EPS:
                findings.append(finding("degenerate_segment", "segment is shorter than 1mil and is likely a rounding fragment", actionId=segment.action_id, lengthMil=round(length, 4)))
        main_start = pad_center(pads[expected["ordered"][0]])
        normalized = normalized_chain(main, main_start)
        if normalized is None:
            findings.append(finding("ordered_through_missing", f"{net} main action order is not one continuous chain from {expected['ordered'][0]}"))
            continue
        main_points, main_oriented = normalized
        ordered_points = [pad_center(pads[key]) for key in expected["ordered"]]
        indices: list[int] = []
        cursor = 0
        for key, target in zip(expected["ordered"], ordered_points):
            hit = next((i for i in range(cursor, len(main_points)) if same(main_points[i], target)), None)
            if hit is None:
                findings.append(finding("ordered_through_missing", f"{net} main chain does not visit {key} as an explicit vertex"))
                indices = []
                break
            indices.append(hit)
            cursor = hit + 1
        if indices and (indices[0] != 0 or indices[-1] != len(main_points) - 1):
            findings.append(finding("ordered_through_missing", f"{net} main chain has copper before/after its endpoint pads"))
        if len(indices) != 3:
            continue
        # Keep the pin escape mechanical and teachable.
        if len(main_oriented) and not (abs(main_oriented[0].b.x - main_oriented[0].a.x) <= EPS and main_oriented[0].b.y > main_oriented[0].a.y):
            findings.append(finding("pad_end_escape", f"{net} must leave the U5 top-row pad vertically upward first"))
        if len(main_oriented) and not (main_oriented[-1].b.y > main_oriented[-1].a.y):
            findings.append(finding("pad_end_escape", f"{net} must enter the CN1 pad from below"))
        for a, b in zip(main_oriented, main_oriented[1:]):
            if turn_degrees(a, b) > 45.0 + EPS:
                findings.append(finding("non_45_bend", "a direct 90-degree or sharper bend needs a 45-degree transition", actions=[a.action_id, b.action_id]))

        attach_candidates = main_points[indices[1] + 1 : indices[2]]
        branch_norm = None
        for attach in attach_candidates:
            candidate = normalized_chain(branch, attach)
            if candidate is not None and same(candidate[0][-1], pad_center(pads[expected["branch"]])):
                branch_norm = candidate
                break
        if branch_norm is None:
            findings.append(finding("branch_attach_order", f"{net} {expected['branch']} branch must tee at an explicit main vertex after R12 and before CN1"))
            continue
        branch_points, branch_oriented = branch_norm
        for a, b in zip(branch_oriented, branch_oriented[1:]):
            if turn_degrees(a, b) > 45.0 + EPS:
                findings.append(finding("non_45_bend", "branch contains a direct 90-degree or sharper bend", actions=[a.action_id, b.action_id]))
        d1 = components.get("D1", {})
        if branch_oriented:
            outward_ok, evidence = pad_external_entry(d1, pads[expected["branch"]], branch_oriented[-1].a)
            if not outward_ok:
                findings.append(finding(
                    "branch_pad_inner_entry",
                    f"{net} branch approaches {expected['branch']} from the component-body side instead of its external pad end",
                    actionId=branch_oriented[-1].action_id,
                    pad=expected["branch"],
                    **evidence,
                ))

        chains[net] = {
            "mainPoints": main_points,
            "main": main_oriented,
            "branchPoints": branch_points,
            "branch": branch_oriented,
            "orderedPads": expected["ordered"],
            "orderedVertexIndices": indices,
            "branchPad": expected["branch"],
        }
        net_segments[net] = main_oriented + branch_oriented
        all_segments.extend(main_oriented + branch_oriented)

    if sorted(used_ids) != sorted(by_id):
        findings.append(finding("unclassified_action", "every action must appear exactly once in actionRoles", unused=sorted(set(by_id) - set(used_ids))))
    if len(used_ids) != len(set(used_ids)):
        findings.append(finding("duplicate_action_role", "one action id is assigned to more than one role"))

    # Copper-to-copper spacing across H/L, including both branches.
    for hs in net_segments["CANH"]:
        for ls in net_segments["CANL"]:
            edge = seg_seg_dist(hs.a, hs.b, ls.a, ls.b) - hs.width / 2 - ls.width / 2
            if edge < clearance - EPS:
                code = "foreign_net_collinear_overlap" if abs(orient(hs.a, hs.b, ls.a)) <= EPS and abs(orient(hs.a, hs.b, ls.b)) <= EPS else "cross_net_intersection" if segments_intersect(hs.a, hs.b, ls.a, ls.b) else "track_clearance"
                findings.append(finding(code, "CANH/CANL planned copper violates the 6mil clearance", actions=[hs.action_id, ls.action_id], edgeGapMil=round(edge, 4)))

    # Same-net actions may meet only at the chain joints declared by main/branch
    # roles.  A tee at the first branch point is intentional; every other
    # non-adjacent crossing, loop-back, collinear duplicate, or copper-area
    # overlap is a planning bug.  The last case matters when a tiny chamfer is
    # shorter than the track width: centerlines look separate, but pcb net-path
    # correctly refuses the non-canonical physical copper union.
    for net, chain in chains.items():
        groups = [chain["main"], chain["branch"]]
        segments = groups[0] + groups[1]
        attach = chain["branchPoints"][0]
        for i, first in enumerate(segments):
            for second in segments[i + 1 :]:
                shared = [p for p in (first.a, first.b) if same(p, second.a) or same(p, second.b)]
                same_group_adjacent = any(
                    first in group and second in group and abs(group.index(first) - group.index(second)) == 1
                    for group in groups
                )
                tee = bool(shared) and all(same(p, attach) for p in shared) and (":main" in first.role) != (":main" in second.role)
                overlap = collinear_overlap(first.a, first.b, second.a, second.b)
                if overlap > EPS:
                    findings.append(finding("duplicate_segment", "same-net actions overlap collinearly", actions=[first.action_id, second.action_id], overlapMil=round(overlap, 4)))
                    continue
                center_gap = seg_seg_dist(first.a, first.b, second.a, second.b)
                copper_touch = center_gap < first.width / 2 + second.width / 2 - EPS
                if copper_touch and not same_group_adjacent and not tee:
                    findings.append(finding(
                        "same_net_copper_overlap",
                        "non-adjacent same-net track areas overlap without one declared endpoint/T junction",
                        actions=[first.action_id, second.action_id],
                        centerGapMil=round(center_gap, 4),
                    ))
                    continue
                if not segments_intersect(first.a, first.b, second.a, second.b):
                    continue
                if not same_group_adjacent and not tee:
                    findings.append(finding("same_net_self_intersection", "same-net actions intersect outside an adjacent chain joint or declared branch tee", actions=[first.action_id, second.action_id]))

    # Pads: foreign and NC are always obstacles.  Same-net pads are legal only
    # when their semantic role includes that pad.
    if any(pad.get("shape") is None for pad in pads.values()):
        limitations.append("pad source shapes are unavailable; conservative hypot(width,height) square hulls were used and special-pad presence is unproven")
    for segment in all_segments:
        net, role_type, *rest = segment.role.split(":")
        allowed = set(EXPECTED[net]["ordered"] if role_type == "main" else [EXPECTED[net]["branch"]])
        for key, pad in pads.items():
            pad_net = str(pad.get("net", ""))
            if key in allowed:
                continue
            rect = pad_rect(pad)
            if rect is None:
                limitations.append(f"pad {key} lacks usable width/height")
                continue
            edge = rect_seg_dist(rect, segment.a, segment.b) - segment.width / 2
            if edge < clearance - EPS:
                code = "foreign_pad_clearance" if pad_net != segment.net or not pad_net else "same_net_role_violation"
                findings.append(finding(code, "planned copper enters a pad outside this action role", actionId=segment.action_id, pad=key, padNet=pad_net or "NC", edgeGapMil=round(edge, 4)))

    # Existing routed copper from the exact track snapshot.
    existing, arcs_available = tracks_from_file(tracks_data)
    if not arcs_available:
        limitations.append("track snapshot lacks arcsAvailable:true; existing arc absence is unproven")
    for segment in all_segments:
        for line in existing:
            if int(line.get("layer", 0)) != segment.layer or str(line.get("net", "")) == segment.net:
                continue
            other = Segment("existing", str(line.get("net", "")), int(line.get("layer", 0)), finite(line.get("lineWidth")), Point(finite(line.get("startX")), finite(line.get("startY"))), Point(finite(line.get("endX")), finite(line.get("endY"))), "existing")
            edge = seg_seg_dist(segment.a, segment.b, other.a, other.b) - segment.width / 2 - other.width / 2
            if edge < clearance - EPS:
                findings.append(finding("existing_copper_clearance", "planned copper violates existing foreign-net copper clearance", actionId=segment.action_id, existingNet=other.net, edgeGapMil=round(edge, 4)))

    existing_can_vias = [via for via in response_items(vias_data, "vias") if str(via.get("net", "")) in EXPECTED]
    if max_vias == 0 and existing_can_vias:
        findings.append(finding(
            "route_contract_mismatch",
            "existing CANH/CANL vias violate the 0-via contract",
            primitiveIds=[str(via.get("primitiveId", "")) for via in existing_can_vias],
        ))
    for label, data, key in (
        ("pours", pours_data, "pours"),
        ("fills", fills_data, "fills"),
        ("regions", regions_data, "regions"),
    ):
        items = response_items(data, key)
        if items:
            limitations.append(f"existing {label} are present but this exam validator does not yet test their geometry")

    # Rounded board outline: sample each short route densely, so a segment cannot
    # cut outside a rounded/concave edge merely because its endpoints are inside.
    outline_raw = board.get("outline", {}).get("points", [])
    outline = [Point(finite(p[0]), finite(p[1])) for p in outline_raw if isinstance(p, list) and len(p) >= 2]
    if len(outline) < 3:
        limitations.append("board outline points are unavailable")
    else:
        for segment in all_segments:
            length = math.hypot(segment.b.x - segment.a.x, segment.b.y - segment.a.y)
            steps = max(1, math.ceil(length / 5))
            if any(not point_in_polygon(Point(segment.a.x + (segment.b.x - segment.a.x) * i / steps, segment.a.y + (segment.b.y - segment.a.y) * i / steps), outline) for i in range(steps + 1)):
                findings.append(finding("outside_outline", "planned copper leaves the real sampled board outline", actionId=segment.action_id))

    # The 10.056mil D1/CN1 body gap cannot carry an 8mil line plus clearance.
    d1_box, cn_box = components.get("D1", {}).get("bbox"), components.get("CN1", {}).get("bbox")
    if d1_box and cn_box and float(d1_box["maxY"]) < float(cn_box["minY"]):
        gap = (float(d1_box["minX"]), float(d1_box["maxY"]), float(d1_box["maxX"]), float(cn_box["minY"]))
        for segment in all_segments:
            if rect_seg_dist(gap, segment.a, segment.b) <= segment.width / 2 + EPS:
                findings.append(finding("forbidden_body_gap", "8mil copper uses the D1/CN1 10.056mil body gap", actionId=segment.action_id))

    # Stable order and no duplicate spam when one long segment hits a pad twice.
    unique: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in findings:
        ev = item.get("evidence", {})
        key = (item["code"], str(ev.get("actionId", ev.get("actions", ""))), str(ev.get("pad", "")))
        unique.setdefault(key, item)
    findings = sorted(unique.values(), key=lambda item: (item["code"], json.dumps(item.get("evidence", {}), sort_keys=True)))
    limitations = sorted(set(limitations))
    verdict = "rejected" if findings else "unknown" if limitations else "accepted"
    action_net = {segment.action_id: segment.net for segment in all_segments}
    topology: dict[str, Any] = {}
    for net, chain in sorted(chains.items()):
        main_length = sum(math.hypot(segment.b.x - segment.a.x, segment.b.y - segment.a.y) for segment in chain["main"])
        branch_length = sum(math.hypot(segment.b.x - segment.a.x, segment.b.y - segment.a.y) for segment in chain["branch"])
        attach = chain["branchPoints"][0]
        topology[net] = {
            "orderedMainPads": chain["orderedPads"],
            "orderedVertexIndices": chain["orderedVertexIndices"],
            "mainSegments": len(chain["main"]),
            "mainLengthMil": round(main_length, 4),
            "branchPad": chain["branchPad"],
            "branchSegments": len(chain["branch"]),
            "branchLengthMil": round(branch_length, 4),
            "branchTee": {"x": attach.x, "y": attach.y},
            "branchSharesOnlyDeclaredTee": not any(
                item["code"] in {"same_net_self_intersection", "duplicate_segment"}
                and any(action_net.get(str(action_id)) == net for action_id in item.get("evidence", {}).get("actions", []))
                for item in findings
            ),
        }
    return {
        "schema": "260919-can-plan-validation/v1",
        "verdict": verdict,
        "facts": {
            "actions": len(actions),
            "classifiedSegments": len(all_segments),
            "nets": sorted(chains),
            "layer": layer,
            "widthMil": width,
            "clearanceMil": clearance,
            "viaCount": 0,
            "sourceSnapshot": {
                **snapshot_digests,
                "documentUuid": source.get("documentUuid", ""),
            },
            "topology": topology,
            "existingCanViaCount": len(existing_can_vias),
        },
        "findings": findings,
        "limitations": limitations,
    }


def synthetic_fixture() -> tuple[dict[str, Any], ...]:
    def component(ref: str, x: float, y: float, pad_defs: list[tuple[str, str, float, float]]) -> dict[str, Any]:
        return {
            "designator": ref, "x": x, "y": y, "rotation": 0,
            "bbox": {"minX": x - 5, "minY": y - 5, "maxX": x + 5, "maxY": y + 5},
            "pads": [
                {"padNumber": num, "net": net, "layer": 1, "x": px, "y": py, "width": 4, "height": 4, "rotation": 0, "shape": ["RECT", 4, 4, 0]}
                for num, net, px, py in pad_defs
            ],
        }

    board = {
        "components": [
            component("U5", 40, 0, [("7", "CANH", 0, 0), ("6", "CANL", 80, 0), ("5", "", 100, 0)]),
            component("R12", 40, 100, [("1", "CANH", 0, 100), ("2", "CANL", 80, 100)]),
            component("D1", 40, 150, [("1", "CANH", 20, 150), ("2", "CANL", 60, 150)]),
            component("CN1", 40, 200, [("2", "CANH", 0, 200), ("1", "CANL", 80, 200)]),
        ],
        "outline": {"points": [[-50, -50], [130, -50], [130, 250], [-50, 250], [-50, -50]]},
    }
    actions = []
    roles: dict[str, Any] = {}
    for net, x, d1x, suffix in (("CANH", 0, 20, "H"), ("CANL", 80, 60, "L")):
        ids = []
        for n, (y1, y2) in enumerate(((0, 100), (100, 150), (150, 200)), 1):
            action_id = f"{suffix}-main-{n}"
            ids.append(action_id)
            actions.append({"id": action_id, "action": "pcb.line.create", "payload": {"net": net, "layer": 1, "lineWidth": 8, "startX": x, "startY": y1, "endX": x, "endY": y2}})
        branch_id = f"{suffix}-branch-1"
        actions.append({"id": branch_id, "action": "pcb.line.create", "payload": {"net": net, "layer": 1, "lineWidth": 8, "startX": x, "startY": 150, "endX": d1x, "endY": 150}})
        roles[net] = {"main": ids, "branches": {EXPECTED[net]["branch"]: [branch_id]}}
    plan = {
        "schema": SUPPORTED_SCHEMA, "status": "candidate-unverified", "units": "mil",
        "sourceSnapshot": {
            "documentUuid": "fixture",
            "boardSha256": "board",
            "tracksSha256": "tracks",
            "viasSha256": "vias",
            "poursSha256": "pours",
            "fillsSha256": "fills",
            "regionsSha256": "regions",
        },
        "placement": {"R12": {"fromCenter": [40, 100], "center": [40, 100], "rotationDeg": 0}},
        "contract": {
            "layer": 1, "widthMil": 8, "minClearanceMil": 6, "maxVias": 0,
            "nets": {net: {"orderedMainPads": spec["ordered"], "branchPads": [spec["branch"]]} for net, spec in EXPECTED.items()},
        },
        "actions": actions, "actionRoles": roles,
    }
    def response(result: dict[str, Any]) -> dict[str, Any]:
        return {"context": {"documentUuid": "fixture"}, "result": result}
    tracks = response({"lines": [], "arcs": [], "arcsAvailable": True})
    vias = response({"count": 0, "vias": []})
    pours = response({"count": 0, "pours": []})
    fills = response({"count": 0, "fills": []})
    regions = response({"count": 0, "regions": []})
    digests = {
        "boardSha256": "board", "tracksSha256": "tracks", "viasSha256": "vias",
        "poursSha256": "pours", "fillsSha256": "fills", "regionsSha256": "regions",
    }
    return board, tracks, vias, pours, fills, regions, plan, digests


def self_test() -> None:
    board, tracks, vias, pours, fills, regions, plan, digests = synthetic_fixture()
    report = validate(plan, board, tracks, vias, pours, fills, regions, digests)
    assert report["verdict"] == "accepted", report
    assert report["facts"]["topology"]["CANH"]["mainLengthMil"] == 200.0
    assert report["facts"]["topology"]["CANH"]["branchLengthMil"] == 20.0
    assert report["facts"]["topology"]["CANH"]["branchSharesOnlyDeclaredTee"] is True

    stamped_board = copy.deepcopy(board) | {"capturedAt": "later", "project": "different-label"}
    wrapped_tracks = {"id": "different-request", "seq": 99, "createdAt": "later", "context": tracks["context"], "result": tracks["result"]}
    original_hashes = snapshot_hashes(board, tracks=tracks, vias=vias, pours=pours, fills=fills, regions=regions)
    stamped_hashes = snapshot_hashes(stamped_board, tracks=wrapped_tracks, vias=vias, pours=pours, fills=fills, regions=regions)
    assert original_hashes == stamped_hashes

    bad = copy.deepcopy(plan)
    bad["contract"]["nets"]["CANH"]["orderedMainPads"] = ["U5.7", "D1.1", "CN1.2"]
    report = validate(bad, board, tracks, vias, pours, fills, regions, digests)
    assert "branch_used_as_main_waypoint" in {item["code"] for item in report["findings"]}

    bad = copy.deepcopy(plan)
    bad_board = copy.deepcopy(board)
    d1 = next(component for component in bad_board["components"] if component["designator"] == "D1")
    d1_h = next(pad for pad in d1["pads"] if pad["padNumber"] == "1")
    d1_h["x"] = 55
    by_id = {item["id"]: item for item in bad["actions"]}
    by_id["H-branch-1"]["payload"]["endX"] = 55
    report = validate(bad, bad_board, tracks, vias, pours, fills, regions, digests)
    assert {item["code"] for item in report["findings"]} & {"foreign_net_collinear_overlap", "cross_net_intersection", "track_clearance", "foreign_pad_clearance"}

    bad = copy.deepcopy(plan)
    by_id = {item["id"]: item for item in bad["actions"]}
    by_id["L-main-1"]["payload"].update({"endX": 100, "endY": 0})
    report = validate(bad, board, tracks, vias, pours, fills, regions, digests)
    assert {"foreign_pad_clearance", "ordered_through_missing"} & {item["code"] for item in report["findings"]}

    bad = copy.deepcopy(plan)
    by_id = {item["id"]: item for item in bad["actions"]}
    by_id["H-main-1"]["payload"].update({"endY": 0.5})
    bad["actions"].append({"id": "H-main-1b", "action": "pcb.line.create", "payload": {"net": "CANH", "layer": 1, "lineWidth": 8, "startX": 0, "startY": 0.5, "endX": 0, "endY": 100}})
    bad["actionRoles"]["CANH"]["main"] = ["H-main-1", "H-main-1b", "H-main-2", "H-main-3"]
    report = validate(bad, board, tracks, vias, pours, fills, regions, digests)
    assert "degenerate_segment" in {item["code"] for item in report["findings"]}

    bad_board = copy.deepcopy(board)
    d1 = next(component for component in bad_board["components"] if component["designator"] == "D1")
    d1["pads"].append({"padNumber": "3", "net": "GND", "layer": 1, "x": 40, "y": 160, "width": 4, "height": 4, "rotation": 0, "shape": ["RECT", 4, 4, 0]})
    report = validate(plan, bad_board, tracks, vias, pours, fills, regions, digests)
    assert "branch_pad_inner_entry" in {item["code"] for item in report["findings"]}

    bad_vias = copy.deepcopy(vias)
    bad_vias["result"] = {"count": 1, "vias": [{"primitiveId": "via-can", "net": "CANH"}]}
    report = validate(plan, board, tracks, bad_vias, pours, fills, regions, digests)
    assert "route_contract_mismatch" in {item["code"] for item in report["findings"]}

    bad = copy.deepcopy(plan)
    by_id = {item["id"]: item for item in bad["actions"]}
    by_id["H-main-2"]["payload"].update({"startX": 2, "endX": 2})
    bad["actions"].extend([
        {"id": "H-tiny-in", "action": "pcb.line.create", "payload": {"net": "CANH", "layer": 1, "lineWidth": 8, "startX": 0, "startY": 100, "endX": 2, "endY": 100}},
        {"id": "H-tiny-out", "action": "pcb.line.create", "payload": {"net": "CANH", "layer": 1, "lineWidth": 8, "startX": 2, "startY": 150, "endX": 0, "endY": 150}},
    ])
    bad["actionRoles"]["CANH"]["main"] = ["H-main-1", "H-tiny-in", "H-main-2", "H-tiny-out", "H-main-3"]
    report = validate(bad, board, tracks, vias, pours, fills, regions, digests)
    assert "same_net_copper_overlap" in {item["code"] for item in report["findings"]}

    print("validate_260919_can_plan self-test: ok (valid + 7 negative fixtures)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, help="candidate JSON")
    parser.add_argument("--board", type=Path, help="exact `easyeda pcb dump --out` JSON")
    parser.add_argument("--components", type=Path, help="optional exact `easyeda pcb list --include-bbox --include-pads` JSON; preferred when pcb dump omits pad shape")
    parser.add_argument("--tracks", type=Path, help="exact `easyeda pcb track-list` JSON")
    parser.add_argument("--vias", type=Path, help="exact `easyeda pcb via-list` JSON")
    parser.add_argument("--pours", type=Path, help="exact `easyeda pcb pour-list` JSON")
    parser.add_argument("--fills", type=Path, help="exact `easyeda pcb fill list` JSON")
    parser.add_argument("--regions", type=Path, help="exact `easyeda pcb region list` JSON")
    parser.add_argument("--out", type=Path, help="write the report instead of stdout")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0
    required = (args.plan, args.board, args.tracks, args.vias, args.pours, args.fills, args.regions)
    if not all(required):
        raise SystemExit("--plan, --board, --tracks, --vias, --pours, --fills, and --regions are required (or use --self-test)")
    board = load_json(args.board)
    components = load_json(args.components) if args.components else None
    tracks = load_json(args.tracks)
    vias = load_json(args.vias)
    pours = load_json(args.pours)
    fills = load_json(args.fills)
    regions = load_json(args.regions)
    digests = snapshot_hashes(board, components=components, tracks=tracks, vias=vias, pours=pours, fills=fills, regions=regions)
    report = validate(load_json(args.plan), board, tracks, vias, pours, fills, regions, digests, components)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if report["verdict"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
