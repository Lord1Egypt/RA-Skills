"""Build real Sketcher sketches from profile shapes (see ``profiles``)."""

from __future__ import annotations

from typing import Any, Dict, List

import FreeCAD as App

from .. import errors, profiles
from ..document import Context
from ..errors import SkillError

# Plane -> (local X image, local Y image, our extrusion normal)
PLANES = {
    "XY": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    "XZ": ((1, 0, 0), (0, 0, 1), (0, 1, 0)),
    "YZ": ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
}
SHAPES_PROP = "FCSkillShapes"


def plane_placement(plane: str, offset: float) -> Any:
    a, b, n = PLANES[plane]
    c = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])  # a x b
    m = App.Matrix(
        a[0], b[0], c[0], n[0] * offset, a[1], b[1], c[1], n[1] * offset, a[2], b[2], c[2], n[2] * offset, 0, 0, 0, 1
    )
    return App.Placement(m)


def normal_of(plane: str) -> Any:
    return App.Vector(*PLANES[plane][2])


def _dist(a: Any, b: Any) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _geom(seg: Any) -> Any:
    import Part

    V = App.Vector
    if seg[0] == "line":
        return Part.LineSegment(V(*seg[1], 0), V(*seg[2], 0))
    if seg[0] == "arc":
        return Part.Arc(V(*seg[1], 0), V(*seg[2], 0), V(*seg[3], 0))
    if seg[0] == "spline":
        _, pts, periodic, t0, t1 = seg
        curve = Part.BSplineCurve()
        if t0 or t1:
            # OCC needs both tangents; a missing one follows the chord at that end. Unit tangents with
            # Scale=False match the chord-length parameterisation; the default Scale=True bends a
            # symmetric input into an asymmetric curve (probed on FreeCAD 1.1).
            a = V(*t0, 0) if t0 else V(*pts[1], 0) - V(*pts[0], 0)
            b = V(*t1, 0) if t1 else V(*pts[-1], 0) - V(*pts[-2], 0)
            curve.interpolate(
                Points=[V(*q, 0) for q in pts], InitialTangent=a.normalize(), FinalTangent=b.normalize(), Scale=False
            )
        elif periodic:
            params, ders = profiles.closed_spline_derivatives(pts)
            curve.interpolate(
                Points=[V(*q, 0) for q in pts],
                PeriodicFlag=True,
                Parameters=params + [params[-1] + _dist(pts[-1], pts[0])],
                Tangents=[V(*t, 0) for t in ders],
                TangentFlags=[True] * len(pts),
                Scale=False,
            )
        else:
            curve.interpolate(Points=[V(*q, 0) for q in pts])
        return curve
    return Part.Circle(V(*seg[1], 0), V(0, 0, 1), seg[2])


def _loop_face(loop: List[Any]) -> Any:
    import Part

    edges = [_geom(s).toShape() for s in loop]
    return Part.Face(Part.Wire(edges))


def _check_overlaps(loops: List[List[Any]]) -> None:
    faces = []
    for i, loop in enumerate(loops):
        try:
            f = _loop_face(loop)
        except Exception:
            raise SkillError(errors.INVALID_PARAM, f"shapes[{i}] does not form a closed loop") from None
        if not f.isValid() or f.Area < 1e-9:
            raise SkillError(
                errors.INVALID_PARAM,
                f"shapes[{i}] is self-intersecting or has zero area",
                hint="List path points in order around the outline so that no edges cross.",
            )
        faces.append(f)
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            inter = faces[i].common(faces[j]).Area
            smaller = min(faces[i].Area, faces[j].Area)
            if inter > 1e-6 * smaller and abs(inter - smaller) > 1e-6 * smaller:
                raise SkillError(
                    errors.INVALID_PARAM,
                    f"shapes[{i}] and shapes[{j}] partially overlap",
                    hint="Shapes must be disjoint (separate regions) or fully nested (holes). Merge overlapping outlines into one 'path'.",
                )


def _evaluate(sk: Any, expr: str) -> float:
    """Current value of an '=expression' used as a profile number, in mm."""
    try:
        v = sk.evalExpression(expr[1:].strip())
    except Exception as e:
        raise SkillError(
            errors.INVALID_EXPRESSION,
            f"Invalid expression in shapes: {expr!r}: {e}",
            hint="Expressions use FreeCAD syntax, e.g. '=Params.width' or '=Params.width / 2 - 5'. "
            "Parameters are created with set_params.",
        ) from None
    unit = getattr(v, "Unit", None)
    if unit is not None and unit != App.Units.Unit() and unit != App.Units.Length:
        raise SkillError(
            errors.INVALID_EXPRESSION,
            f"{expr!r} gives {v}, but profile coordinates are lengths",
            hint="Use a parameter in mm (a plain number means mm).",
        )
    try:
        return float(v.Value if hasattr(v, "Value") else v)
    except (TypeError, ValueError):
        raise SkillError(errors.INVALID_EXPRESSION, f"{expr!r} does not give a number") from None


def _clear(sk: Any) -> None:
    for prop, _expr in list(sk.ExpressionEngine):
        if prop.lstrip(".").startswith("Constraints."):
            sk.setExpression(prop, None)
    if sk.GeometryCount:
        sk.deleteAllGeometry()


def _dimensions(shape: Any, numeric: Any, loop: List[Any], ids: List[int]) -> Any:
    """Named dimensions that pin a rect, circle or slot completely: [(name, constraint, source value)].

    Each number the agent wrote gets exactly one dimension, so a sketch made only of these shapes is fully
    constrained, and an '=expression' number becomes an expression on its dimension. Returns None for
    other shapes, and for degenerate layouts (a rect whose rounding swallows a whole side)."""
    import Sketcher

    C = Sketcher.Constraint
    lines = [g for seg, g in zip(loop, ids) if seg[0] == "line"]
    arcs = [g for seg, g in zip(loop, ids) if seg[0] == "arc"]
    out: List[Any] = []
    if "circle" in shape:
        g = ids[0]
        cx, cy = numeric["circle"]
        out += [("r", C("Radius", g, numeric["radius"]), shape["radius"])]
        out += [("cx", C("DistanceX", -1, 1, g, 3, cx), shape["circle"][0])]
        out += [("cy", C("DistanceY", -1, 1, g, 3, cy), shape["circle"][1])]
        return out
    if "rect" in shape:
        r = float(numeric.get("corner_radius", 0) or 0)
        if len(lines) != 4 or len(arcs) != (4 if r > 0 else 0):
            return None
        x0, y0, x1, y1 = numeric["rect"]
        src = shape["rect"]
        out += [(None, C("Horizontal", lines[0]), None), (None, C("Horizontal", lines[2]), None)]
        out += [(None, C("Vertical", lines[1]), None), (None, C("Vertical", lines[3]), None)]
        if r > 0:
            out += [(None, C("Equal", arcs[0], a), None) for a in arcs[1:]]
            out += [("r", C("Radius", arcs[0], r), shape.get("corner_radius"))]
        # line order (see profiles._rounded_polygon): bottom, right, top, left
        out += [("y0", C("DistanceY", -1, 1, lines[0], 1, y0), src[1])]
        out += [("x1", C("DistanceX", -1, 1, lines[1], 1, x1), src[2])]
        out += [("y1", C("DistanceY", -1, 1, lines[2], 1, y1), src[3])]
        out += [("x0", C("DistanceX", -1, 1, lines[3], 1, x0), src[0])]
        return out
    if "slot" in shape:
        if len(lines) != 2 or len(arcs) != 2:
            return None
        (ax, ay), (bx, by) = numeric["slot"]
        end2, end1 = arcs  # segment order: line, arc around the second centre, line, arc around the first
        out += [(None, C("Equal", end2, end1), None), ("r", C("Radius", end2, numeric["radius"]), shape["radius"])]
        out += [("x1", C("DistanceX", -1, 1, end1, 3, ax), shape["slot"][0][0])]
        out += [("y1", C("DistanceY", -1, 1, end1, 3, ay), shape["slot"][0][1])]
        out += [("x2", C("DistanceX", -1, 1, end2, 3, bx), shape["slot"][1][0])]
        out += [("y2", C("DistanceY", -1, 1, end2, 3, by), shape["slot"][1][1])]
        return out
    return None


def _build(sk: Any, shapes: Any, numeric: Any, loops: List[List[Any]], dimension: bool) -> bool:
    """Add geometry and constraints; False if the dimensioned sketch does not solve."""
    import Sketcher

    driven = []
    for index, (shape, num, loop) in enumerate(zip(shapes, numeric, loops)):
        ids = [sk.addGeometry(_geom(s), False) for s in loop]
        dims = _dimensions(shape, num, loop, ids) if dimension and isinstance(shape, dict) else None
        if not (loop[0][0] == "circle" or (loop[0][0] == "spline" and loop[0][2])):  # not a single closed curve
            for k, seg in enumerate(loop):
                nxt = (k + 1) % len(loop)
                joint = App.Vector(*(seg[1][-1] if seg[0] == "spline" else seg[-1]), 0)
                pk = _pos_at(sk, ids[k], joint)
                pn = _pos_at(sk, ids[nxt], joint)
                if pk and pn:
                    # Coincident keeps the outline connected when edited in the GUI; where a dimensioned
                    # shape's line meets its arc the join is also tangent (a rounded corner, a slot end).
                    smooth = dims is not None and {seg[0], loop[nxt][0]} == {"line", "arc"}
                    kind = "Tangent" if smooth else "Coincident"
                    sk.addConstraint(Sketcher.Constraint(kind, ids[k], pk, ids[nxt], pn))
        for name, constraint, source in dims or []:
            i = sk.addConstraint(constraint)
            if name is not None:
                sk.renameConstraint(i, f"s{index}_{name}")
                if profiles.is_expr(source):
                    driven.append((f"s{index}_{name}", source))
    for name, source in driven:
        sk.setExpression(f"Constraints.{name}", source[1:].strip())
    return not dimension or sk.solve() == 0


def fill_sketch(sk: Any, shapes: Any) -> None:
    """(Re)build the geometry of ``sk`` from profile shapes."""
    try:
        numeric = shapes
        if profiles.has_expressions(shapes):
            profiles.check_expressions(shapes)
            numeric = profiles.resolve(shapes, lambda e: _evaluate(sk, e))
        loops = profiles.all_segments(numeric)
    except profiles.ProfileError as e:
        raise SkillError(errors.INVALID_PARAM, str(e)) from None
    _check_overlaps(loops)
    _clear(sk)
    try:
        solved = _build(sk, shapes, numeric, loops, dimension=True)
    except SkillError:
        raise
    except Exception:
        solved = False
    if not solved:
        if profiles.has_expressions(shapes):
            raise SkillError(
                errors.RECOMPUTE_FAILED,
                f"The profile of '{sk.Name}' could not be dimensioned with its expressions",
                hint="Check that the expressions give a valid shape (x_max > x_min, radii that fit), or use numbers.",
            )
        _clear(sk)  # plain geometry, as drawn: still a valid profile, without dimensions
        _build(sk, shapes, numeric, loops, dimension=False)
    setattr_json(sk, shapes)


def _pos_at(sk: Any, gid: int, p: Any) -> int:
    for pos in (1, 2):
        if (sk.getPoint(gid, pos) - p).Length < 1e-6:
            return pos
    return 0


def setattr_json(sk: Any, shapes: Any) -> None:
    import json

    if SHAPES_PROP not in sk.PropertiesList:
        sk.addProperty("App::PropertyString", SHAPES_PROP, "FCSkill", "Profile shapes this sketch was built from")
        sk.setEditorMode(SHAPES_PROP, 2)
    setattr(sk, SHAPES_PROP, json.dumps(shapes))


def make_sketch(ctx: Context, owner_name: str, p: Dict[str, Any]) -> Any:
    sk = ctx.doc.addObject("Sketcher::SketchObject", f"{owner_name}_Sketch")
    sk.Label = sk.Name
    sk.Placement = plane_placement(p.get("plane", "XY"), float(p.get("offset", 0)))
    fill_sketch(sk, p["shapes"])
    sk.recompute()
    if sk.solve() != 0:
        raise SkillError(errors.INTERNAL, f"Sketch {sk.Name} did not solve")
    return sk


def sketch_points(sk: Any) -> List[Any]:
    """Points along the sketch outline, in global coordinates."""
    pts: List[Any] = []
    for e in sk.Shape.Edges:
        pts.extend(e.discretize(24))
    return pts
