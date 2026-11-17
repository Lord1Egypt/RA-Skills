"""Primitive solids and profile-based solids (extrude, revolve)."""

from __future__ import annotations

from typing import Any, Dict, List

import FreeCAD as App

from .. import errors, geometry
from ..document import Context
from ..errors import SkillError

PLANE_MAP = {
    "XY": (lambda a, b: App.Vector(a, b, 0), App.Vector(0, 0, 1)),
    "XZ": (lambda a, b: App.Vector(a, 0, b), App.Vector(0, 1, 0)),
    "YZ": (lambda a, b: App.Vector(0, a, b), App.Vector(1, 0, 0)),
}


def _placement(obj: Any, p: Dict[str, Any]) -> None:
    pos = App.Vector(*p.get("position", [0, 0, 0]))
    if p.get("rotation"):
        rot = App.Rotation(App.Vector(*p["rotation"]["axis"]), p["rotation"]["angle"])
    elif p.get("direction"):
        rot = geometry.rotation_to(p["direction"])
    else:
        rot = App.Rotation()
    obj.Placement = App.Placement(pos, rot)


def _primitive(ctx: Context, type_id: str, default: str, p: Dict[str, Any], props: Dict[str, str]) -> Any:
    obj = ctx.add(type_id, p.get("name"), default)
    for param, prop in props.items():
        ctx.assign(obj, prop, p[param])
    _placement(obj, p)
    ctx.recompute()
    ctx.verify_solid(obj, default)
    return obj


def box(ctx: Context, p: Dict[str, Any]) -> Any:
    return _primitive(ctx, "Part::Box", "Box", p, {"length": "Length", "width": "Width", "height": "Height"})


def cylinder(ctx: Context, p: Dict[str, Any]) -> Any:
    return _primitive(ctx, "Part::Cylinder", "Cylinder", p, {"radius": "Radius", "height": "Height"})


def sphere(ctx: Context, p: Dict[str, Any]) -> Any:
    return _primitive(ctx, "Part::Sphere", "Sphere", p, {"radius": "Radius"})


def cone(ctx: Context, p: Dict[str, Any]) -> Any:
    return _primitive(ctx, "Part::Cone", "Cone", p, {"radius1": "Radius1", "radius2": "Radius2", "height": "Height"})


def torus(ctx: Context, p: Dict[str, Any]) -> Any:
    return _primitive(ctx, "Part::Torus", "Torus", p, {"radius1": "Radius1", "radius2": "Radius2"})


def prism(ctx: Context, p: Dict[str, Any]) -> Any:
    obj = ctx.add("Part::Prism", p.get("name"), "Prism")
    obj.Polygon = p["sides"]
    ctx.assign(obj, "Circumradius", p["circumradius"])
    ctx.assign(obj, "Height", p["height"])
    _placement(obj, p)
    ctx.recompute()
    ctx.verify_solid(obj, "Prism")
    return obj


# ------------------------------------------------------------------ profiles


def _profile_points(p: Dict[str, Any]) -> List[Any]:
    pts = p["points"]
    if len(pts[0]) == 3:
        vecs = [App.Vector(*pt) for pt in pts]
    else:
        to3d = PLANE_MAP[p.get("plane", "XY")][0]
        vecs = [to3d(a, b) for a, b in pts]
    normal = geometry.newell_normal(vecs)
    if normal.Length < 1e-9:
        raise SkillError(
            errors.INVALID_PARAM,
            "Profile points are collinear or the polygon has zero area",
            hint="Give at least 3 non-collinear corners in perimeter order.",
        )
    n = App.Vector(normal).normalize()
    off = [abs((v - vecs[0]).dot(n)) for v in vecs]
    if max(off) > 1e-6:
        raise SkillError(
            errors.INVALID_PARAM,
            f"Profile points are not coplanar (max deviation {geometry.num(max(off))} mm)",
            hint="All points must lie in one plane; use 2D points with 'plane' when possible.",
        )
    crossing = _first_crossing(vecs, n)
    if crossing:
        i, j = crossing
        raise SkillError(
            errors.INVALID_PARAM,
            f"Profile edges {i}-{i + 1} and {j}-{j + 1 if j + 1 < len(vecs) else 0} cross (points are 0-based)",
            hint="List the corners in order around the perimeter so that no two edges cross.",
        )
    return vecs


def _first_crossing(vecs: List[Any], n: Any) -> Any:
    """First pair of non-adjacent polygon edges that intersect, or None."""
    drop = max(range(3), key=lambda k: abs((n.x, n.y, n.z)[k]))
    keep = [k for k in range(3) if k != drop]
    pts = [((v.x, v.y, v.z)[keep[0]], (v.x, v.y, v.z)[keep[1]]) for v in vecs]
    m = len(pts)

    def orient(a: Any, b: Any, c: Any) -> float:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def on_seg(a: Any, b: Any, c: Any) -> bool:
        return (
            min(a[0], b[0]) - 1e-9 <= c[0] <= max(a[0], b[0]) + 1e-9
            and min(a[1], b[1]) - 1e-9 <= c[1] <= max(a[1], b[1]) + 1e-9
        )

    for i in range(m):
        a, b = pts[i], pts[(i + 1) % m]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1:
                continue  # adjacent through the closing edge
            c, d = pts[j], pts[(j + 1) % m]
            o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
            if (
                (o1 * o2 < 0 and o3 * o4 < 0)
                or (abs(o1) < 1e-12 and on_seg(a, b, c))
                or (abs(o2) < 1e-12 and on_seg(a, b, d))
                or (abs(o3) < 1e-12 and on_seg(c, d, a))
                or (abs(o4) < 1e-12 and on_seg(c, d, b))
            ):
                return i, j
    return None


def _make_polygon(ctx: Context, owner_name: str, vecs: List[Any]) -> Any:
    poly = ctx.doc.addObject("Part::Polygon", f"{owner_name}_Profile")
    poly.Label = poly.Name
    poly.Nodes = vecs
    poly.Close = True
    return poly


def _profile(ctx: Context, obj: Any, p: Dict[str, Any]) -> Any:
    """Create the profile helper (sketch for 'shapes', polygon for 'points')."""
    if "shapes" in p:
        from .sketch import make_sketch

        helper = make_sketch(ctx, obj.Name, p)
    else:
        helper = _make_polygon(ctx, obj.Name, _profile_points(p))
    ctx.own_helper(obj, helper)
    return helper


def _profile_normal(p: Dict[str, Any], helper: Any) -> Any:
    if "points" in p and len(p["points"][0]) == 3:
        return geometry.newell_normal(list(helper.Nodes)).normalize()
    return PLANE_MAP[p.get("plane", "XY")][1]


def extrude(ctx: Context, p: Dict[str, Any]) -> Any:
    if p.get("body"):
        from . import partdesign

        return partdesign.extrude(ctx, p)
    obj = ctx.add("Part::Extrusion", p.get("name"), "Extrude")
    poly = _profile(ctx, obj, p)
    obj.Base = poly
    obj.Solid = True
    obj.DirMode = "Custom"
    if "direction" in p:
        d = App.Vector(*p["direction"])
        obj.Dir = App.Vector(d).normalize()
        obj.LengthFwd = d.Length
    else:
        obj.Dir = _profile_normal(p, poly)
        ctx.assign(obj, "LengthFwd", p["height"])
    obj.Symmetric = bool(p.get("symmetric", False))
    ctx.recompute()
    ctx.verify_solid(obj, "Extrusion")
    return obj


def _check_axis_side(pts: List[Any], axis: Any, center: Any, n: Any) -> None:
    if abs(App.Vector(axis).normalize().dot(n)) >= 1e-6:
        return  # axis not in the profile plane
    side = [App.Vector(axis).cross(v - center).dot(n) for v in pts]
    tol = 1e-7 * max(1.0, max(abs(s) for s in side))
    if any(s > tol for s in side) and any(s < -tol for s in side):
        raise SkillError(
            errors.INVALID_PARAM,
            "The profile crosses the revolution axis",
            hint="Keep the whole profile on one side of the axis (touching the axis is fine).",
        )


def revolve(ctx: Context, p: Dict[str, Any]) -> Any:
    if p.get("body"):
        from . import partdesign

        return partdesign.revolve(ctx, p)
    axis = App.Vector(*p["axis"])
    center = App.Vector(*p["center"])
    if "points" in p:
        vecs = _profile_points(p)
        _check_axis_side(vecs, axis, center, geometry.newell_normal(vecs).normalize())
    obj = ctx.add("Part::Revolution", p.get("name"), "Revolve")
    poly = _profile(ctx, obj, p)
    if "shapes" in p:
        from .sketch import normal_of, sketch_points

        _check_axis_side(sketch_points(poly), axis, center, normal_of(p.get("plane", "XY")))
    obj.Source = poly
    obj.Axis = axis
    obj.Base = center
    ctx.assign(obj, "Angle", p["angle"])
    obj.Solid = True
    ctx.recompute()
    ctx.verify_solid(obj, "Revolution")
    return obj


HANDLERS = {
    "box": box,
    "cylinder": cylinder,
    "sphere": sphere,
    "cone": cone,
    "torus": torus,
    "prism": prism,
    "extrude": extrude,
    "revolve": revolve,
}
