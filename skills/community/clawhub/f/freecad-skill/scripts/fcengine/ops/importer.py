"""Import solids from files: STEP/IGES/BREP, meshes (STL/OBJ/3MF/PLY/OFF), or another FreeCAD document.

Meshes become solids with one planar face per triangle (coplanar triangles merged when 'refine' is on).
Probed on FreeCAD 1.1: booleans on the result work but are slow, because FreeCAD tracks every face. A request
that imports, cuts and exports a mesh took 20 s for 7400 triangles and 77 s for 20000, so meshes are capped at
MAX_TRIANGLES, and 'refine' (quadratic) is skipped above REFINE_MAX. Only closed, manifold,
non-self-intersecting meshes are accepted: anything else would give a solid that booleans silently break.

Library parts (see ``library``) are downloaded by the launcher into the
workspace before the engine runs; here they are plain workspace files plus an
attribution sidecar. Imported geometry is a fixed shape (Part::Feature): it can
be placed, cut, fused, measured, given a material and used in assemblies, but
its dimensions are not parametric.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import FreeCAD as App

from .. import errors, geometry, library, workspace
from ..document import Context
from ..errors import SkillError

SOURCE_PROP = "FCSkillSource"
EXTS = {
    "step": "step",
    "stp": "step",
    "iges": "iges",
    "igs": "iges",
    "brep": "brep",
    "brp": "brep",
    "fcstd": "fcstd",
    **{ext: "mesh" for ext in ("stl", "obj", "3mf", "ply", "off")},
}
MAX_TRIANGLES = 20000
REFINE_MAX = 10000  # merging coplanar triangles grows quadratically: 5.5 s for 10000, 21 s for 20000
SEW_TOLERANCE = 0.01  # mm
# A mesh outside this size range was probably not modelled in millimetres (STL carries no units).
PLAUSIBLE_MM = (1.0, 3000.0)


def _library_file(ctx: Context, ref: str) -> Path:
    """The downloaded copy of a library part (exact file, or the best format of a part path)."""
    base = ctx.root / library.CACHE_DIR / "parts"
    ref = library._safe_rel(ref.strip().strip("/"))
    exact = base / ref
    if exact.is_file() and library._ext(ref) in library.FORMATS:
        return workspace.resolve(ctx.root, str(exact.relative_to(ctx.root)))  # no symlink escapes
    stem = ref.rsplit(".", 1)[0] if library._ext(ref) in library.LISTED else ref
    folder, name = (base / stem).parent, (base / stem).name
    if folder.is_dir():
        found = {
            library._ext(f.name): f
            for f in folder.iterdir()
            if f.is_file() and f.name.rsplit(".", 1)[0] == name and library._ext(f.name) in library.FORMATS
        }
        for fmt in library.FORMATS:
            if fmt in found:
                return workspace.resolve(ctx.root, str(found[fmt].relative_to(ctx.root)))
    raise SkillError(
        errors.LIBRARY_UNAVAILABLE,
        f"Library part '{ref}' has not been downloaded",
        hint="Library parts are fetched by the launcher: run the request with 'python3 fcskill.py run ...' "
        "(not through FreeCAD directly), and use the 'part' value from 'fcskill.py library <keywords>'.",
    )


def _shape_from_fcstd(path: Path) -> Any:
    """Compound of the finished solids of another document (objects no other object uses)."""
    import Part

    before = set(App.listDocuments())
    doc = App.openDocument(str(path), hidden=True)
    try:
        solids = []
        for o in doc.Objects:
            if not (hasattr(o, "Shape") and o.isDerivedFrom("Part::Feature")) or o.Shape.isNull() or not o.Shape.Solids:
                continue
            users = [u for u in o.InList if hasattr(u, "Shape") and u.isDerivedFrom("Part::Feature")]
            parent = o.getParentGeoFeatureGroup() if hasattr(o, "getParentGeoFeatureGroup") else None
            if users or (parent is not None and parent.TypeId == "PartDesign::Body"):
                continue  # consumed by another feature, or a feature inside a body (the body itself counts)
            solids.append(o.Shape.copy())
        if not solids:
            raise SkillError(errors.EMPTY_RESULT, f"'{path.name}' contains no solid parts to import")
        return solids[0] if len(solids) == 1 else Part.makeCompound(solids)
    finally:
        for name in set(App.listDocuments()) - before:
            App.closeDocument(name)


def _mesh_solid(path: Path, refine: bool, info: Dict[str, Any]) -> Any:
    """A solid from a closed triangle mesh; 'info' receives the mesh statistics."""
    import Mesh
    import Part

    try:
        mesh = Mesh.Mesh(str(path))
    except Exception as e:
        raise SkillError(errors.INVALID_PARAM, f"Cannot read '{path.name}': {e}") from None
    n = mesh.CountFacets
    if n == 0:
        # FreeCAD also reads 0 triangles from a damaged file, or from an ASCII STL with only a triangle or two.
        raise SkillError(
            errors.GEOMETRY_INVALID,
            f"FreeCAD read no triangles from '{path.name}': it is not a closed solid mesh",
            hint="The file is empty, damaged, or too small to enclose a volume (a closed mesh needs at least 4 "
            "triangles). Export the part again as a closed mesh, or as STEP.",
        )
    if n > MAX_TRIANGLES:
        raise SkillError(
            errors.UNSUPPORTED,
            f"'{path.name}' has {n} triangles; meshes are imported as solids up to {MAX_TRIANGLES}",
            hint="Reduce it first (e.g. 'Decimate' in Blender or MeshLab), or ask for the part as STEP.",
        )
    # Harmless clean-ups that exporters often need; nothing that changes the shape.
    mesh.removeDuplicatedPoints()
    mesh.removeDuplicatedFacets()
    mesh.harmonizeNormals()
    problems = []
    if not mesh.isSolid():
        problems.append("it is not closed (it has holes or open edges)")
    if mesh.hasNonManifolds():
        problems.append("it has non-manifold edges")
    if mesh.hasSelfIntersections():
        problems.append("it intersects itself")
    if problems:
        raise SkillError(
            errors.GEOMETRY_INVALID,
            f"'{path.name}' can't become a solid: {'; '.join(problems)}",
            hint="Repair the mesh first (e.g. Meshmixer, MeshLab, or a slicer's repair function), then import it again.",
            details={"triangles": n},
        )
    if mesh.Volume < 0:
        mesh.flipNormals()
    solids = []
    for comp in mesh.getSeparateComponents() if mesh.countComponents() > 1 else [mesh]:
        faces = Part.Shape()
        faces.makeShapeFromMesh(comp.Topology, SEW_TOLERANCE, False)
        solid = Part.Solid(Part.Shell(faces.Faces))
        if solid.Volume < 0:
            solid.reverse()
        solids.append(solid.removeSplitter() if refine and n <= REFINE_MAX else solid)
    shape = solids[0] if len(solids) == 1 else Part.makeCompound(solids)
    if not geometry.is_valid(shape):
        raise SkillError(errors.GEOMETRY_INVALID, f"'{path.name}' gave an invalid solid", details={"triangles": n})
    info.update(
        {"triangles": n, "faces": len(shape.Faces), "pieces": len(solids), "refined": refine and n <= REFINE_MAX}
    )
    if refine and n > REFINE_MAX:
        info["note"] = f"not refined: merging faces is too slow above {REFINE_MAX} triangles"
    return shape


def _read(path: Path, refine: bool = True, info: Optional[Dict[str, Any]] = None) -> Any:
    import Part

    kind = EXTS.get(path.suffix.lower().lstrip("."))
    if kind is None:
        raise SkillError(
            errors.UNSUPPORTED,
            f"Cannot import '{path.name}'",
            hint="Supported: .step/.stp, .iges/.igs, .brep/.brp, .FCStd, and meshes: .stl, .obj, .3mf, .ply, .off.",
        )
    if kind == "fcstd":
        return _shape_from_fcstd(path)
    if kind == "mesh":
        return _mesh_solid(path, refine, info if info is not None else {})
    shape = Part.Shape()
    try:
        shape.read(str(path))
    except Exception as e:
        raise SkillError(errors.INVALID_PARAM, f"Cannot read '{path.name}': {e}") from None
    return shape


def _anchor(shape: Any, anchor: str) -> Any:
    """Offset that puts the chosen point of the bounding box at the origin."""
    bb = shape.optimalBoundingBox() if hasattr(shape, "optimalBoundingBox") else shape.BoundBox
    c = bb.Center
    return {
        "origin": App.Vector(0, 0, 0),
        "center": -c,
        "bottom_center": App.Vector(-c.x, -c.y, -bb.ZMin),
        "min_corner": App.Vector(-bb.XMin, -bb.YMin, -bb.ZMin),
    }[anchor]


def _bake(shape: Any) -> Any:
    """Move the shape's placement into its geometry. Assigning a placed shape to an object makes the shape's
    placement the object's, and setting the object's placement afterwards would silently drop it (probed)."""
    m = shape.Placement.toMatrix()
    c = shape.copy()
    c.Placement = App.Placement()
    return c.transformed(m, True)


def import_(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    meta: Optional[Dict[str, Any]] = None
    if p.get("library"):
        path = _library_file(ctx, p["library"])
        side = path.with_name(path.name + ".json")
        meta = json.loads(side.read_text(encoding="utf-8")) if side.is_file() else library.attribution(p["library"])
    else:
        path = workspace.resolve(ctx.root, p["file"])
        if not path.is_file():
            raise SkillError(errors.INVALID_PARAM, f"File '{p['file']}' not found in the workspace")
    mesh_info: Dict[str, Any] = {}
    shape = _read(path, bool(p.get("refine", True)), mesh_info)
    if shape.isNull() or not shape.Faces:
        raise SkillError(errors.EMPTY_RESULT, f"'{path.name}' contains no geometry")
    default = "".join(c if c.isalnum() else "_" for c in path.stem)[:40] or "Imported"
    if not default[0].isalpha():
        default = "P" + default
    obj = ctx.add("Part::Feature", p.get("name"), default)
    shape.translate(_anchor(shape, p.get("anchor", "origin")))
    obj.Shape = _bake(shape)
    rot = (
        App.Rotation(App.Vector(*p["rotation"]["axis"]), p["rotation"]["angle"])
        if p.get("rotation")
        else App.Rotation()
    )
    obj.Placement = App.Placement(App.Vector(*p.get("position", [0, 0, 0])), rot)
    source = {"file": workspace.relative(ctx.root, path)}
    if meta:
        source.update(meta)
    obj.addProperty(
        "App::PropertyString", SOURCE_PROP, "FCSkill", "Where this imported shape came from (and its licence)"
    )
    obj.setEditorMode(SOURCE_PROP, 1)
    setattr(obj, SOURCE_PROP, json.dumps(source))
    if meta:
        obj.Label2 = meta["text"][:500]
    ctx.recompute()
    data: Dict[str, Any] = {"source": source["file"], "solids": len(obj.Shape.Solids)}
    if mesh_info:
        data["mesh"] = mesh_info
        size = max(obj.Shape.BoundBox.XLength, obj.Shape.BoundBox.YLength, obj.Shape.BoundBox.ZLength)
        if not PLAUSIBLE_MM[0] <= size <= PLAUSIBLE_MM[1]:
            ctx.warn(
                "CHECK_UNITS",
                f"'{obj.Name}' is {size:.4g} mm across. Mesh files carry no units: if it was made in inches "
                "(x25.4) or metres (x1000), resize it with 'scale'",
            )
    if meta:
        data["attribution"] = meta["text"]
        data["license"] = meta["license"]
    if not obj.Shape.Solids:
        ctx.warn(
            "NOT_SOLID", f"'{obj.Name}' has no closed solid (surfaces only): booleans, volume and FEM won't work on it"
        )
    elif not geometry.is_valid(obj.Shape):
        ctx.warn("INVALID_GEOMETRY", f"'{obj.Name}' has invalid geometry from the file; booleans with it may fail")
    return {"object": obj, "data": data}


HANDLERS = {"import": import_}
