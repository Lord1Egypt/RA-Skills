"""Export with read-back verification.

Files are written to a temporary name next to the destination and only
moved into place when the whole request succeeds (see runner).
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Dict, List

from .. import audit, errors, geometry, workspace
from ..document import Context, role, visible_objects
from ..errors import SkillError

EXTENSIONS = {
    ".step": "step",
    ".stp": "step",
    ".iges": "iges",
    ".igs": "iges",
    ".brep": "brep",
    ".brp": "brep",
    ".stl": "stl",
    ".obj": "obj",
    ".3mf": "3mf",
    ".dxf": "dxf",
    ".svg": "svg",
}
MESH_FORMATS = {"stl", "obj", "3mf"}
FLAT_FORMATS = {"dxf", "svg"}
# view -> rotation rows taking model coordinates to (drawing x, drawing y, towards viewer).
# Projecting the rotated shape from +Z gives standard orientations: front shows X across and Z up.
FLAT_VIEWS = {
    "top": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    "bottom": ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    "front": ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    "back": ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    "right": ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    "left": ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
}


def view_shape(shape: Any, view: str) -> Any:
    """Copy of ``shape`` rotated so that ``view`` is seen from +Z with standard drawing axes."""
    import FreeCAD as App

    r = FLAT_VIEWS[view]
    m = App.Matrix(r[0][0], r[0][1], r[0][2], 0, r[1][0], r[1][1], r[1][2], 0, r[2][0], r[2][1], r[2][2], 0, 0, 0, 0, 1)
    out = shape.copy()
    out.transformShape(m)
    return out


def dxf_entities(text: str) -> List[Any]:
    """(type, {group code: [values]}) for each entity in a DXF ENTITIES fragment."""
    lines = [ln.strip() for ln in text.splitlines()]
    pairs = list(zip(lines[0::2], lines[1::2]))
    out: List[Any] = []
    for code, value in pairs:
        if code == "0":
            out.append((value, {}))
        elif out:
            out[-1][1].setdefault(code, []).append(value)
    return [e for e in out if e[0] not in ("SECTION", "ENDSEC", "EOF")]


def dxf_file_entities(text: str) -> List[Any]:
    """Entities of the ENTITIES section of a complete DXF file."""
    lines = [ln.strip() for ln in text.splitlines()]
    pairs = list(zip(lines[0::2], lines[1::2]))
    out: List[Any] = []
    inside = False
    for (code, value), nxt in zip(pairs, pairs[1:] + [("", "")]):
        if code == "0" and value == "SECTION" and nxt == ("2", "ENTITIES"):
            inside = True
            continue
        if inside and code == "0" and value == "ENDSEC":
            break
        if inside:
            if code == "0":
                out.append((value, {}))
            elif out:
                out[-1][1].setdefault(code, []).append(value)
    return out


def dxf_extents(ents: List[Any]) -> Any:
    xs: List[float] = []
    ys: List[float] = []
    for kind, g in ents:
        f = lambda c, i=0, g=g: float(g[c][i])  # noqa: E731
        try:
            if kind == "LINE":
                xs += [f("10"), f("11")]
                ys += [f("20"), f("21")]
            elif kind == "CIRCLE":
                cx, cy, r = f("10"), f("20"), f("40")
                xs += [cx - r, cx + r]
                ys += [cy - r, cy + r]
            elif kind == "ARC":
                cx, cy, r, a0, a1 = f("10"), f("20"), f("40"), f("50"), f("51")
                sweep = (a1 - a0) % 360 or 360
                angles = [a0, a0 + sweep] + [a for a in (0, 90, 180, 270, 360, 450, 540, 630) if a0 < a < a0 + sweep]
                xs += [cx + r * math.cos(math.radians(a)) for a in angles]
                ys += [cy + r * math.sin(math.radians(a)) for a in angles]
            else:
                xs += [float(v) for v in g.get("10", [])]
                ys += [float(v) for v in g.get("20", [])]
        except (KeyError, ValueError, IndexError):
            continue
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def _write_flat(fmt: str, objs: List[Any], path: Path, view: str, shown: str) -> Dict[str, Any]:
    import FreeCAD as App
    import Part
    import TechDraw

    shape = view_shape(Part.makeCompound([o.Shape for o in objs]), view)
    up = App.Vector(0, 0, 1)
    frag = TechDraw.projectToDXF(shape, up)
    ents = dxf_entities(frag)
    ext = dxf_extents(ents)
    if not ents or ext is None:
        raise SkillError(errors.EXPORT_FAILED, f"The {view} projection of {[o.Name for o in objs]} is empty")
    bb = geometry.tight_bbox(shape)
    want = [bb.XLength, bb.YLength]
    got = [ext[2] - ext[0], ext[3] - ext[1]]
    if any(abs(g - w) > 1e-3 + 1e-6 * w for g, w in zip(got, want)):
        raise SkillError(
            errors.EXPORT_FAILED,
            f"The {view} projection in {shown} does not match the model",
            details={"expected_size": [geometry.num(x) for x in want], "actual_size": [geometry.num(x) for x in got]},
        )
    if fmt == "dxf":
        body = frag if frag.startswith("0") else frag.lstrip()
        path.write_text("0\nSECTION\n2\nENTITIES\n" + body.rstrip("\n") + "\n0\nENDSEC\n0\nEOF\n", encoding="utf-8")
    else:
        g = TechDraw.projectToSVG(shape, up).replace('stroke-width="1.0"', 'stroke-width="0.25"')
        m = 2.0
        x0, y0, x1, y1 = ext
        w, h = x1 - x0 + 2 * m, y1 - y0 + 2 * m
        path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.4f}mm" height="{h:.4f}mm" '
            f'viewBox="{x0 - m:.4f} {-(y1 + m):.4f} {w:.4f} {h:.4f}">\n{g}\n</svg>\n',
            encoding="utf-8",
        )
    from collections import Counter

    counts = dict(Counter(k for k, _ in ents))
    return {
        "view": view,
        "units": "mm",
        "size": [geometry.num(x) for x in (ext[2] - ext[0], ext[3] - ext[1])],
        "entities": counts,
    }


def _targets(ctx: Context, p: Dict[str, Any]) -> List[Any]:
    if p.get("targets"):
        return [ctx.get(t) for t in p["targets"]]
    objs = [o for o in visible_objects(ctx.doc) if role(o) == "result" and not o.Shape.isNull() and o.Shape.Solids]
    if not objs:
        raise SkillError(
            errors.EXPORT_FAILED,
            "Nothing to export: the document has no solid result objects",
            hint="Create geometry first, or name objects explicitly with 'targets'.",
        )
    return objs


def _readback(objs: List[Any], path: Path, fmt: str) -> Any:
    """Read the file back and compare it with the model: (checks, mismatch); checks is None if it is empty."""
    import Part

    back = Part.read(str(path))
    if back.isNull() or not back.Faces:
        return None, True
    want_bb = geometry.bbox(Part.makeCompound([o.Shape for o in objs]))
    got_bb = geometry.bbox(back)
    checks: Dict[str, Any] = {"faces": len(back.Faces), "bbox_size": got_bb["size"] if got_bb else None}
    mismatch = got_bb is None or any(
        abs(a - b) > 1e-3 + 1e-6 * abs(b)
        for a, b in zip(got_bb["min"] + got_bb["max"], want_bb["min"] + want_bb["max"])
    )
    if fmt != "iges":  # IGES commonly comes back as faces/shells, not solids
        want_vol = sum(o.Shape.Volume for o in objs)
        want_solids = sum(len(o.Shape.Solids) for o in objs)
        checks.update(solids=len(back.Solids), volume=geometry.num(back.Volume, 3))
        mismatch = (
            mismatch or len(back.Solids) != want_solids or abs(back.Volume - want_vol) > 1e-3 * max(want_vol, 1.0)
        )
    return checks, mismatch


def _step_names(path: Path) -> List[str]:
    """Product names written to a STEP file, in file order."""
    import re

    text = path.read_text(encoding="utf-8", errors="replace")
    return list(dict.fromkeys(re.findall(r"PRODUCT\(\s*'((?:[^']|'')*)'", text)))


def _write_step(objs: List[Any], path: Path) -> bool:
    """STEP with one named product per part, and assemblies as a product structure (each part once,
    placed as often as it is used). Returns False if only the plain writer worked (anonymous shapes)."""
    import Part

    try:
        import Import

        # legacy=False, keepPlacement=True: without the second flag a single part is written at the origin.
        Import.export(objs, str(path), False, True)
        if path.exists() and path.stat().st_size > 0 and not _readback(objs, path, "step")[1]:
            return True
    except Exception:
        pass
    if all(o.isDerivedFrom("Part::Feature") for o in objs):
        Part.export(objs, str(path))
    else:
        Part.makeCompound([o.Shape for o in objs]).exportStep(str(path))
    return False


def _write_brep_like(fmt: str, objs: List[Any], path: Path, shown: str, ctx: Context) -> Dict[str, Any]:
    import Part

    structured = None
    if fmt == "step":
        structured = _write_step(objs, path)
    elif all(o.isDerivedFrom("Part::Feature") for o in objs):
        Part.export(objs, str(path))
    else:  # assemblies: Part.export writes nothing; export their placed compound
        compound = Part.makeCompound([o.Shape for o in objs])
        {"iges": compound.exportIges, "brep": compound.exportBrep}[fmt](str(path))
    if not path.exists() or path.stat().st_size == 0:
        raise SkillError(errors.EXPORT_FAILED, f"FreeCAD wrote no data to {shown}")
    checks, mismatch = _readback(objs, path, fmt)
    if checks is None:
        raise SkillError(errors.EXPORT_FAILED, f"{shown} reads back as an empty shape")
    want_bb = geometry.bbox(Part.makeCompound([o.Shape for o in objs]))
    if mismatch:
        raise SkillError(
            errors.EXPORT_FAILED,
            f"Read-back of {shown} does not match the model",
            details={"expected_bbox": want_bb, "actual": checks},
        )
    if structured is not None:
        names = _step_names(path)
        wanted = [o.Label for o in objs]
        checks["part_names"] = bool(structured) and all(w in names for w in wanted)
        if not checks["part_names"]:
            ctx.warn(
                "STEP_NAMES",
                f"{shown} was written without part names or assembly structure (this FreeCAD build's structured "
                "STEP writer failed); the geometry is complete and verified",
            )
    bad: List[str] = []
    unchecked: Dict[str, str] = {}
    for o in objs:
        if o.Shape.isNull() or not o.Shape.Solids:
            continue  # wires, faces and shells have no solid to check
        verdict, reason = geometry.self_check(o.Shape)
        if verdict:
            bad.append(o.Name)
        elif verdict is None:
            unchecked[o.Name] = str(reason)
    if bad:
        checks["self_intersecting"] = bad
        ctx.warn(
            "SELF_INTERSECTION",
            f"{shown}: {', '.join(repr(n) for n in bad)} pass through themselves; other CAD systems may reject "
            "the file or compute wrong volumes. Fix the geometry before handing it over.",
        )
    if unchecked:  # not established is recorded as such, never as a clean result
        checks["self_intersection_unchecked"] = unchecked
        ctx.warn(
            "SELF_INTERSECTION_UNCHECKED",
            f"{shown}: {', '.join(f'{n!r} ({why})' for n, why in unchecked.items())} could not be checked for "
            "passing through themselves; the file is written, but this property is unconfirmed.",
        )
    return checks


def _write_mesh(objs: List[Any], path: Path, tol: float, ang_deg: float, ctx: Context, shown: str) -> Dict[str, Any]:
    import Mesh
    import MeshPart

    mesh = Mesh.Mesh()
    for o in objs:
        mesh.addMesh(
            MeshPart.meshFromShape(
                Shape=o.Shape, LinearDeflection=tol, AngularDeflection=math.radians(ang_deg), Relative=False
            )
        )
    mesh.write(str(path))
    if not path.exists() or path.stat().st_size == 0:
        raise SkillError(errors.EXPORT_FAILED, f"FreeCAD wrote no data to {shown}")
    back = Mesh.Mesh(str(path))
    want = sum(o.Shape.Volume for o in objs)
    checks = {
        "facets": back.CountFacets,
        "closed": bool(back.isSolid()),
        "non_manifold": bool(back.hasNonManifolds()),
        "volume": geometry.num(back.Volume, 3),
    }
    if back.CountFacets == 0:
        raise SkillError(errors.EXPORT_FAILED, f"{shown} contains no triangles")
    try:
        checks["self_intersections"] = bool(back.hasSelfIntersections())
    except Exception:
        pass
    if checks.get("self_intersections"):
        ctx.warn(
            "MESH_SELF_INTERSECTION",
            f"{shown} has triangles that cut through each other (the model overlaps itself, or separate "
            "exported solids overlap); slicers may print it wrongly. Fix the model, or fuse the overlapping parts.",
        )
    if not checks["closed"] or checks["non_manifold"]:
        ctx.warn("MESH_NOT_WATERTIGHT", f"{shown} is not a closed manifold mesh; slicers may reject it")
    if want > 0 and abs(back.Volume - want) > 0.02 * want:
        ctx.warn(
            "MESH_VOLUME",
            f"mesh volume {checks['volume']} differs from model volume {geometry.num(want, 3)} by more than 2%; lower 'tolerance'",
        )
    return checks


def export(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    dest = workspace.resolve(ctx.root, p["filename"])
    if dest.suffix.lower() == ".fcstd" or dest == ctx.doc_path:
        raise SkillError(
            errors.PATH_NOT_ALLOWED,
            "export writes exchange formats, not FreeCAD documents",
            hint="The model document is saved automatically. To save a copy under another name, "
            "send a request with that 'doc' path instead.",
        )
    ext = dest.suffix.lower()
    fmt = EXTENSIONS.get(ext)
    if fmt is None:
        raise SkillError(
            errors.INVALID_PARAM,
            f"Cannot export to '{dest.name}': unknown extension '{ext}'",
            hint=f"The extension sets the format. Use one of {sorted(EXTENSIONS)}.",
        )
    if any(pe["dest"] == dest for pe in ctx.pending_exports):
        raise SkillError(errors.INVALID_PARAM, f"'{p['filename']}' is already exported earlier in this request")
    objs = _targets(ctx, p)
    for o in objs:
        if o.Shape.isNull():
            raise SkillError(errors.EXPORT_FAILED, f"'{o.Name}' has an empty shape")
        if not o.Shape.Faces:
            raise SkillError(
                errors.EXPORT_FAILED,
                f"'{o.Name}' has no faces (it is a {o.TypeId} wire/profile)",
                hint="Export solids. Profiles are helpers; export the extrusion or revolution built from them.",
            )
    if fmt not in FLAT_FORMATS and 2 <= len(objs) <= audit.MAX_OVERLAP_RESULTS:
        for a, b, v, small in audit.overlap_pairs(objs):
            ctx.warn(
                "OVERLAPPING_SOLIDS",
                f"{dest.name}: '{a.Name}' and '{b.Name}' overlap ({geometry.num(v, 1)} mm3, "
                f"{geometry.num(100 * v / small.Shape.Volume, 1)}% of '{small.Name}'); the file holds interpenetrating "
                "solids. Fix the sizes or positions, fuse them, or export one object at a time.",
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.stem}.fcskill-tmp{dest.suffix}")
    try:
        if fmt in MESH_FORMATS:
            checks = _write_mesh(objs, tmp, p["tolerance"], p["angular_tolerance"], ctx, dest.name)
        elif fmt in FLAT_FORMATS:
            checks = _write_flat(fmt, objs, tmp, p.get("view", "top"), dest.name)
        else:
            checks = _write_brep_like(fmt, objs, tmp, dest.name, ctx)
    except SkillError:
        if tmp.exists():
            os.remove(tmp)
        raise
    except Exception as e:
        if tmp.exists():
            os.remove(tmp)
        raise SkillError(errors.EXPORT_FAILED, f"Export to {dest.name} failed: {e}") from None
    record = {
        "file": workspace.relative(ctx.root, dest),
        "format": fmt,
        "objects": [o.Name for o in objs],
        "bytes": tmp.stat().st_size,
        "verified": checks,
    }
    ctx.pending_exports.append({"tmp": tmp, "dest": dest, "record": record})
    return {"data": record}


HANDLERS = {"export": export}
