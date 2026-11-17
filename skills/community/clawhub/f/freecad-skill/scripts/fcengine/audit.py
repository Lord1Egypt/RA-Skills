"""Document-wide integrity audit, run around every edit.

Creation-time checks (cut removed nothing, fusion fell apart, empty
result) only see the feature being created. Later edits to its inputs
(set, move, rotate, place, set_params, delete) can break it silently, so the
runner audits all features before and after each edit. Conditions that
are *new* after the edit are reported: an empty result is an error (the
request rolls back), and no-effect or disjoint booleans are warnings.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from . import errors, geometry
from .document import role, type_name
from .errors import SkillError

# Ops that change existing objects and so need the audit.
EDIT_OPS = ("set", "set_params", "move", "rotate", "place", "delete")

State = Dict[str, Tuple[bool, bool, int]]  # name -> (empty, no_effect, solids)


def _volume(obj: Any) -> float:
    try:
        return obj.Shape.Volume if not obj.Shape.isNull() else 0.0
    except Exception:
        return 0.0


def snapshot(doc: Any) -> State:
    out: State = {}
    for o in doc.Objects:
        if not geometry.is_part_shape(o) or o.TypeId.startswith("Spreadsheet::"):
            continue
        if role(o) != "result" and o.TypeId not in ("Part::Cut", "Part::MultiFuse", "Part::MultiCommon"):
            continue
        shape = o.Shape
        empty = (
            o.TypeId != "Part::Polygon"
            and not (o.TypeId == "PartDesign::Body" and o.Tip is None)
            and (shape.isNull() or not shape.Faces)
        )
        no_effect = False
        if o.TypeId == "Part::Cut" and o.Base is not None and not empty:
            base_v = _volume(o.Base)
            no_effect = base_v - _volume(o) <= 1e-6 * max(base_v, 1.0)
        solids = len(shape.Solids) if not shape.isNull() else 0
        out[o.Name] = (empty, no_effect, solids)
    return out


def compare(ctx: Any, before: State) -> None:
    """Raise for newly empty results; warn for newly no-effect or disjoint booleans."""
    after = snapshot(ctx.doc)
    for name, (empty, no_effect, solids) in after.items():
        was = before.get(name)
        obj = ctx.doc.getObject(name)
        if empty and (was is None or not was[0]) and role(obj) == "result":
            if was is None:
                raise SkillError(
                    errors.EMPTY_RESULT,
                    f"'{name}' ({type_name(obj)}) was created without geometry",
                    hint="Give it a shape or don't create it. Nothing was saved.",
                    details={"object": name},
                )
            raise SkillError(
                errors.EMPTY_RESULT,
                f"This edit left '{name}' ({type_name(obj)}) with no solid geometry",
                hint="The change makes a tool swallow its base, or moves objects apart. Nothing was saved; "
                "check the new sizes and positions (inspect the inputs of this object).",
                details={"object": name, "inputs": [i.Name for i in obj.OutList]},
            )
        if was is None:
            continue
        if no_effect and not was[1]:
            ctx.warn(
                "NO_EFFECT",
                f"after this edit, cut '{name}' no longer removes any material: its tool does not "
                "overlap the base any more",
            )
        if obj.TypeId == "Part::MultiFuse" and solids > 1 and was[2] <= 1:
            ctx.warn("DISJOINT", f"after this edit, fusion '{name}' falls apart into {solids} separate solids")


def final_check(doc: Any) -> None:
    """Every result must have geometry (catches empty objects left by edits)."""
    for o in doc.Objects:
        if geometry.is_part_shape(o) and role(o) == "result" and (o.Shape.isNull() or not o.Shape.Faces):
            if o.TypeId == "Part::Polygon" or (o.TypeId == "PartDesign::Body" and o.Tip is None):
                continue  # a stand-alone profile is a wire by design; a new body is empty until its first feature
            raise SkillError(
                errors.EMPTY_RESULT,
                f"'{o.Name}' ({type_name(o)}) has no geometry",
                hint="Delete it, or give it a shape. Nothing was saved.",
            )


MAX_OVERLAP_RESULTS = 25
OVERLAP_BUDGET_S = 10.0
OVERLAP_MIN_FRACTION = 1e-3


def _fingerprint(o: Any) -> Any:
    try:
        b = o.Shape.BoundBox
        return (
            round(o.Shape.Volume, 6),
            round(b.XMin, 6),
            round(b.YMin, 6),
            round(b.ZMin, 6),
            round(b.XMax, 6),
            round(b.YMax, 6),
            round(b.ZMax, 6),
        )
    except Exception:
        return None


def _same(a: Any, b: Any) -> bool:
    """Fingerprints equal up to recompute noise (a reopened document recomputes to the last few digits)."""
    if a is None or b is None:
        return a is b
    return all(abs(x - y) <= 1e-7 * max(1.0, abs(x)) for x, y in zip(a, b))


def fingerprints(doc: Any) -> Dict[str, Any]:
    """Shape fingerprints at the start of a request, to tell which objects the request created or changed."""
    return {o.Name: _fingerprint(o) for o in doc.Objects if geometry.is_part_shape(o) and not o.Shape.isNull()}


def overlap_pairs(objs: Any, changed: Any = None, limit: int = 5) -> Any:
    """(a, b, overlap volume, smaller object) for solids that overlap by more than a tiny fraction.
    With ``changed``, only pairs involving one of those names are tested. Time-bounded."""
    import time

    start, out = time.monotonic(), []
    for i, a in enumerate(objs):
        for b in objs[i + 1 :]:
            if time.monotonic() - start > OVERLAP_BUDGET_S or len(out) >= limit:
                return out
            if changed is not None and a.Name not in changed and b.Name not in changed:
                continue
            sa, sb = a.Shape, b.Shape
            if not sa.Solids or not sb.Solids or not sa.BoundBox.intersect(sb.BoundBox):
                continue
            try:
                v = sa.common(sb).Volume
            except Exception:
                continue
            if v > OVERLAP_MIN_FRACTION * min(sa.Volume, sb.Volume):
                out.append((a, b, v, a if sa.Volume <= sb.Volume else b))
    return out


def overlapping_results(ctx: Any, before: Dict[str, Any]) -> None:
    """Warn when separate results overlap: usually a leftover helper (e.g. an unused cutter) that would be
    rendered and exported with the model, hiding or corrupting it. Only pairs involving an object this request
    created or changed are checked, so a model is not re-warned on every request, and objects already reported
    as ORPHANED are skipped. Assemblies report their own interferences."""
    from .document import visible_objects

    orphaned = {w["message"].split("'")[1] for w in ctx.warnings if w["code"] == "ORPHANED" and "'" in w["message"]}
    objs = [
        o
        for o in visible_objects(ctx.doc)
        if role(o) == "result"
        and geometry.is_part_shape(o)
        and o.TypeId != "Assembly::AssemblyObject"
        and not o.Shape.isNull()
        and o.Shape.Solids
        and o.Name not in orphaned
    ]
    if not 2 <= len(objs) <= MAX_OVERLAP_RESULTS:
        return
    changed = {o.Name for o in objs if o.Name not in before or not _same(before[o.Name], _fingerprint(o))}
    exported = [w["message"] for w in ctx.warnings if w["code"] == "OVERLAPPING_SOLIDS"]
    for a, b, v, small in overlap_pairs(objs, changed):
        if any(f"'{a.Name}'" in m and f"'{b.Name}'" in m for m in exported):
            continue  # already reported by the export that wrote them
        ctx.warn(
            "OVERLAPPING_RESULTS",
            f"results '{a.Name}' and '{b.Name}' overlap ({geometry.num(v, 1)} mm3, "
            f"{geometry.num(100 * v / small.Shape.Volume, 1)}% of '{small.Name}'). Both are shown, rendered and "
            f"exported. If one is a leftover tool, delete it or use it in a cut/common; to join them, fuse them.",
        )
