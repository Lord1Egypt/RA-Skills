"""Geometry measurement, topology descriptors and expectation checks."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

import FreeCAD as App

from . import selectors

DIGITS = 4


def num(x: float, digits: int = DIGITS) -> float:
    v = round(float(x), digits)
    return 0.0 if v == 0 else v  # avoid -0.0


def vec(v: Any, digits: int = DIGITS) -> List[float]:
    return [num(v.x, digits), num(v.y, digits), num(v.z, digits)]


def tight_bbox(shape: Any) -> Any:
    """Exact bounding box. Shape.BoundBox can be loose on curved surfaces
    (a 92 mm torus reports ~99.6 mm), which would mislead dimension checks."""
    try:
        return shape.optimalBoundingBox(False, False)
    except Exception:
        return shape.BoundBox


def bbox(shape: Any) -> Optional[Dict[str, List[float]]]:
    if shape is None or shape.isNull():
        return None
    bb = tight_bbox(shape)
    if not bb.isValid():
        return None
    return {
        "min": [num(bb.XMin), num(bb.YMin), num(bb.ZMin)],
        "max": [num(bb.XMax), num(bb.YMax), num(bb.ZMax)],
        "size": [num(bb.XLength), num(bb.YLength), num(bb.ZLength)],
    }


_VALID: Dict[int, Tuple[Any, bool]] = {}
VALID_CACHE = 512


def is_valid(shape: Any) -> bool:
    """shape.isValid(), remembered per shape. The check takes seconds on large shapes (2-3 s for 20000 faces)
    and one request asks it several times about the same result. The cached shape is kept alive, so a new shape
    cannot reuse its identity, and isSame (same geometry and location) confirms the hit."""
    key = shape.hashCode()
    hit = _VALID.get(key)
    if hit is not None and hit[0].isSame(shape):
        return hit[1]
    valid = bool(shape.isValid())
    while len(_VALID) >= VALID_CACHE:
        _VALID.pop(next(iter(_VALID)))  # oldest entry first
    _VALID[key] = (shape, valid)
    return valid


# Self-intersection check (OCC's boolean-argument checker). isValid() does not see a solid that passes
# through itself, e.g. a spring whose wire is thicker than its pitch: such a solid has a wrong volume and
# breaks later booleans. The check is slower than isValid, so it is skipped above this face count.
SELF_CHECK_MAX_FACES = 3000
_SELF: Dict[int, Tuple[Any, Optional[bool], Optional[str]]] = {}


# FreeCAD reports the checker's findings as one exception text, one "BOPAlgo <kind>" per finding. These kinds
# come from the checker's other, independent tests (continuity, edge size, curve-on-surface fit): a report
# holding only these means the self-intersection test ran and found nothing. Any other text does not.
_BOP_REPORT = "BOP check found the following errors:"
_UNRELATED_FINDINGS = ("GeomAbs_C0", "TooSmallEdge", "InvalidCurveOnSurface")


def self_check(shape: Any) -> Tuple[Optional[bool], Optional[str]]:
    """(verdict, reason). The verdict is True (a solid passes through itself), False (every solid was
    checked and none does) or None: not established. ``reason`` then says why.

    A clean result is reported only when it was obtained: a solid the checker could not examine (FreeCAD
    runs the self-intersection test only on geometry that passes its validity test), an aborted run or an
    unrecognised checker error all leave the verdict open, for the whole shape.

    Solids are checked one by one: separate solids of a compound may overlap on purpose (parts of an
    assembly, unfused array instances), which is reported elsewhere."""
    if shape is None or shape.isNull():
        return None, "empty shape"
    key = shape.hashCode()
    hit = _SELF.get(key)
    if hit is not None and hit[0].isSame(shape):
        return hit[1], hit[2]
    verdict, reason = _self_check(shape)
    while len(_SELF) >= VALID_CACHE:
        _SELF.pop(next(iter(_SELF)))
    _SELF[key] = (shape, verdict, reason)
    return verdict, reason


def _self_check(shape: Any) -> Tuple[Optional[bool], Optional[str]]:
    solids = shape.Solids
    if not solids:
        return None, "no solid to check"
    if len(shape.Faces) > SELF_CHECK_MAX_FACES:
        return None, f"skipped: more than {SELF_CHECK_MAX_FACES} faces"
    open_reason: Optional[str] = None
    for solid in solids:
        try:
            solid.check(True)
            continue  # checked: clean
        except Exception as e:
            text = str(e)
        if "SelfIntersect" in text:
            return True, None  # confirmed, whatever happened on the other solids
        if _only_unrelated_findings(text):
            continue  # the test ran; the checker's other tests found something else
        if open_reason is None:
            open_reason = _open_reason(solid, text)
    return (None, open_reason) if open_reason else (False, None)


def _only_unrelated_findings(text: str) -> bool:
    head, sep, body = text.partition(_BOP_REPORT)
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if not sep or head.strip() or not lines:
        return False
    return all(ln.rpartition("BOPAlgo")[2].strip(" _") in _UNRELATED_FINDINGS for ln in lines)


def _open_reason(solid: Any, text: str) -> str:
    try:
        if not solid.isValid():
            return "the geometry is invalid, so the check cannot run"
    except Exception:
        pass
    return "the check did not complete: " + (" ".join(text.split())[:200] or "no details")


def self_intersects(shape: Any) -> Optional[bool]:
    """The verdict of self_check: True, False, or None when it is not established."""
    return self_check(shape)[0]


def summary(shape: Any, detailed: bool = False, validity: bool = True) -> Dict[str, Any]:
    """Compact geometric summary of a shape. ``validity=False`` leaves out the (slow) validity check."""
    if shape is None or shape.isNull():
        return {"empty": True}
    out: Dict[str, Any] = {
        "volume": num(shape.Volume, 3),
        "bbox": bbox(shape),
        "solids": len(shape.Solids),
    }
    if validity:
        out["valid"] = is_valid(shape)
    if detailed:
        out["area"] = num(shape.Area, 3)
        out["faces"] = len(shape.Faces)
        out["edges"] = len(shape.Edges)
        out.update(mass_properties(shape))
    return out


def center_of_mass(shape: Any) -> Optional[Any]:
    try:
        if not shape.Solids:
            return None
        return shape.Solids[0].CenterOfMass if len(shape.Solids) == 1 else _compound_com(shape)
    except Exception:
        return None


def mass_properties(shape: Any, density: Optional[float] = None) -> Dict[str, Any]:
    """Centre of mass and inertia of the solids of ``shape``.

    Without a density the inertia is geometric (volume-weighted, mm^5): multiply by the density to get
    a mass moment. With ``density`` (g/cm3) it is in g*mm2, and the mass in g. The inertia tensor is taken
    about the centre of mass, along the global X/Y/Z axes."""
    com = center_of_mass(shape)
    if com is None:
        return {}
    out: Dict[str, Any] = {"center_of_mass": vec(com)}
    k = 1.0 if density is None else density / 1000.0  # g/cm3 -> g/mm3
    try:
        m = shape.MatrixOfInertia
        key = "inertia_mm5" if density is None else "inertia_g_mm2"
        out[key] = {
            "ixx": num(m.A11 * k, 3),
            "iyy": num(m.A22 * k, 3),
            "izz": num(m.A33 * k, 3),
            "ixy": num(m.A12 * k, 3),
            "ixz": num(m.A13 * k, 3),
            "iyz": num(m.A23 * k, 3),
        }
        if len(shape.Solids) == 1:
            pp = shape.Solids[0].PrincipalProperties
            out["principal_" + key] = sorted(num(x * k, 3) for x in pp["Moments"])
    except Exception:
        pass
    if density is not None:
        out["mass_g"] = num(shape.Volume * k, 3)
    return out


def _compound_com(shape: Any) -> Any:
    total = App.Vector(0, 0, 0)
    vol = 0.0
    for s in shape.Solids:
        total = total + s.CenterOfMass * s.Volume
        vol += s.Volume
    return total * (1.0 / vol) if vol else total


# ------------------------------------------------------------------ descriptors

_SURFACES = {
    "Plane": "plane",
    "Cylinder": "cylinder",
    "Cone": "cone",
    "Sphere": "sphere",
    "Toroid": "torus",
    "BSplineSurface": "bspline",
    "BezierSurface": "bezier",
}
_CURVES = {
    "Line": "line",
    "LineSegment": "line",
    "Circle": "circle",
    "Ellipse": "ellipse",
    "BSplineCurve": "bspline",
    "BezierCurve": "bezier",
}


def _face_desc(i: int, f: Any) -> Dict[str, Any]:
    try:
        s = f.Surface
    except Exception:
        s = None
    t = _SURFACES.get(type(s).__name__, "other") if s is not None else "other"
    d: Dict[str, Any] = {"kind": "face", "index": i, "type": t, "area": num(f.Area, 3), "center": _center(f)}
    try:
        if t == "plane":
            u0, u1, v0, v1 = f.ParameterRange
            d["normal"] = vec(f.normalAt((u0 + u1) / 2, (v0 + v1) / 2), 6)
        elif t in ("cylinder", "cone"):
            d["axis"] = vec(s.Axis, 6)
            if t == "cylinder":
                d["radius"] = num(s.Radius)
        elif t == "sphere":
            d["radius"] = num(s.Radius)
    except Exception:
        pass
    return d


def _center(s: Any) -> List[float]:
    try:
        return vec(s.CenterOfMass)
    except Exception:  # degenerated edges have no mass properties
        pts = [v.Point for v in s.Vertexes]
        if not pts:
            return [0.0, 0.0, 0.0]
        acc = App.Vector(0, 0, 0)
        for p in pts:
            acc = acc + p
        return vec(acc * (1.0 / len(pts)))


def _edge_desc(i: int, e: Any) -> Dict[str, Any]:
    try:
        c = e.Curve
    except Exception:
        # Edges at a sphere's poles are degenerated: FreeCAD raises
        # TypeError ("undefined curve type") instead of returning a curve.
        c = None
    t = _CURVES.get(type(c).__name__, "other") if c is not None else "other"
    d: Dict[str, Any] = {"kind": "edge", "index": i, "type": t, "length": num(e.Length), "center": _center(e)}
    if c is None:
        d["degenerated"] = True
    try:
        if t == "line":
            p0, p1 = e.Vertexes[0].Point, e.Vertexes[-1].Point
            dv = p1 - p0
            if dv.Length > 0:
                d["direction"] = vec(dv.normalize(), 6)
        elif t == "circle":
            d["radius"] = num(c.Radius)
            d["axis"] = vec(c.Axis, 6)
            d["closed"] = bool(e.isClosed())
    except Exception:
        pass
    try:
        if getattr(e, "Degenerated", False):
            d["degenerated"] = True
    except Exception:
        pass
    return d


def describe_faces(shape: Any) -> List[Dict[str, Any]]:
    return [_face_desc(i + 1, f) for i, f in enumerate(shape.Faces)]


def describe_edges(shape: Any) -> List[Dict[str, Any]]:
    return [_edge_desc(i + 1, e) for i, e in enumerate(shape.Edges)]


def edge_face_map(shape: Any) -> Dict[int, List[int]]:
    """1-based edge index -> 1-based indices of faces that contain it."""
    faces = shape.Faces
    out: Dict[int, List[int]] = {}
    for ei, e in enumerate(shape.Edges, start=1):
        out[ei] = [fi for fi, f in enumerate(faces, start=1) if any(e.isSame(fe) for fe in f.Edges)]
    return out


def select_edges(shape: Any, value: Any, filletable: bool = False) -> List[int]:
    """Resolve an edge selector on ``shape``.

    With ``filletable`` the result skips seam and degenerated edges
    (e.g. the seam line of a cylinder), which fillets cannot round.
    """
    edges = describe_edges(shape)
    cache: Dict[str, Dict[int, List[int]]] = {}

    def lazy_map() -> Dict[int, List[int]]:
        if "m" not in cache:
            cache["m"] = edge_face_map(shape)
        return cache["m"]

    picked = selectors.select(value, edges, describe_faces(shape), lazy_map)
    if filletable and not isinstance(value, list) and not isinstance(value, int):
        mapping = lazy_map()
        picked = [i for i in picked if len(mapping.get(i, [])) == 2 and not edges[i - 1].get("degenerated")]
    return picked


def select_faces(shape: Any, value: Any) -> List[int]:
    return selectors.select(value, describe_faces(shape))


# ------------------------------------------------------------------ expectations


def check_expectations(shape: Any, exp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a list of failed expectations (empty if all hold)."""
    tol = float(exp.get("tolerance", 0.01))
    vtol = float(exp.get("volume_tolerance", 0.001))
    failures: List[Dict[str, Any]] = []
    if shape is None or shape.isNull():
        return [{"check": "shape", "expected": "non-empty", "actual": "empty"}]
    if "volume" in exp:
        want = float(exp["volume"])
        got = shape.Volume
        if abs(got - want) > vtol * max(abs(want), 1e-9) + 1e-6:
            failures.append({"check": "volume", "expected": want, "actual": num(got, 3)})
    bb = tight_bbox(shape)
    for key, actual in (
        ("bbox_size", [bb.XLength, bb.YLength, bb.ZLength]),
        ("bbox_min", [bb.XMin, bb.YMin, bb.ZMin]),
        ("bbox_max", [bb.XMax, bb.YMax, bb.ZMax]),
    ):
        if key in exp:
            want_v: Sequence[float] = exp[key]
            if any(abs(a - w) > tol for a, w in zip(actual, want_v)):
                failures.append({"check": key, "expected": list(want_v), "actual": [num(a) for a in actual]})
    if "solids" in exp and len(shape.Solids) != exp["solids"]:
        failures.append({"check": "solids", "expected": exp["solids"], "actual": len(shape.Solids)})
    if "valid" in exp and is_valid(shape) != exp["valid"]:
        failures.append({"check": "valid", "expected": exp["valid"], "actual": is_valid(shape)})
    if "self_intersecting" in exp:
        verdict, reason = self_check(shape)
        if verdict is not exp["self_intersecting"]:  # an unestablished verdict never satisfies the expectation
            failures.append(
                {
                    "check": "self_intersecting",
                    "expected": exp["self_intersecting"],
                    "actual": verdict if verdict is not None else f"not checked ({reason})",
                }
            )
    return failures


def rotation_to(direction: Sequence[float]) -> Any:
    """Rotation taking +Z onto ``direction``."""
    return App.Rotation(App.Vector(0, 0, 1), App.Vector(*direction))


def newell_normal(points: Sequence[Any]) -> Any:
    n = App.Vector(0, 0, 0)
    for i, p in enumerate(points):
        q = points[(i + 1) % len(points)]
        n.x += (p.y - q.y) * (p.z + q.z)
        n.y += (p.z - q.z) * (p.x + q.x)
        n.z += (p.x - q.x) * (p.y + q.y)
    return n


def is_part_shape(obj: Any) -> bool:
    if obj.TypeId == "Assembly::AssemblyObject":
        return True  # its Shape is the compound of its placed parts
    return obj.isDerivedFrom("Part::Feature") and hasattr(obj, "Shape")
