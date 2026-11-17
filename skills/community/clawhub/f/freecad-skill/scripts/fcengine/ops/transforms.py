"""Placement edits (move, rotate, place) and derived copies (mirror, copy, scale)."""

from __future__ import annotations

from typing import Any, Dict

import FreeCAD as App

from .. import errors
from ..document import Context
from ..errors import SkillError

# Features whose Placement is recomputed from their input: editing it has no
# lasting effect, so moves are redirected to the input chain.
DERIVED_PLACEMENT = {"Part::Fillet", "Part::Chamfer", "Part::Thickness"}


def _placement_owner(obj: Any) -> Any:
    parent = obj.getParentGeoFeatureGroup() if hasattr(obj, "getParentGeoFeatureGroup") else None
    if parent is not None and parent.TypeId == "PartDesign::Body":
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{obj.Name}' is a feature of body '{parent.Name}' and has no placement of its own",
            hint=f"Move/rotate the body '{parent.Name}', or change the feature's 'offset' or 'shapes' with 'set'.",
        )
    seen = 0
    while obj.TypeId in DERIVED_PLACEMENT and seen < 50:
        obj = obj.Base if obj.TypeId != "Part::Thickness" else obj.Faces[0]
        seen += 1
    return obj


def _check_no_expression(obj: Any) -> None:
    for prop, _expr in obj.ExpressionEngine:
        if prop.startswith("Placement") or prop.startswith(".Placement"):
            raise SkillError(
                errors.INVALID_PARAM,
                f"'{obj.Name}' has its Placement driven by an expression ({prop})",
                hint=f"Use 'set' on {obj.Name} with properties {{\"{prop}\": null}} to clear it first.",
            )


def _apply(ctx: Context, target: Any, placement_fn: Any) -> Any:
    owner = _placement_owner(target)
    if owner is not target:
        ctx.warn("REDIRECTED", f"'{target.Name}' follows the placement of '{owner.Name}'; moved '{owner.Name}' instead")
    _check_no_expression(owner)
    owner.Placement = placement_fn(owner.Placement)
    ctx.mutated = True
    ctx.reselect()
    ctx.recompute()
    return target


def move(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])
    off = App.Vector(*p["offset"])

    def fn(pl: Any) -> Any:
        return App.Placement(pl.Base + off, pl.Rotation)

    return _apply(ctx, target, fn)


def rotate(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])
    rot = App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(*p["axis"]), p["angle"]), App.Vector(*p["center"]))
    return _apply(ctx, target, lambda pl: rot.multiply(pl))


def place(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])

    def fn(pl: Any) -> Any:
        base = App.Vector(*p["position"]) if "position" in p else pl.Base
        rot = (
            App.Rotation(App.Vector(*p["rotation"]["axis"]), p["rotation"]["angle"]) if "rotation" in p else pl.Rotation
        )
        return App.Placement(base, rot)

    return _apply(ctx, target, fn)


def mirror(ctx: Context, p: Dict[str, Any]) -> Any:
    from .patterns import _pd_target

    feat = _pd_target(ctx, p)
    if feat is not None:  # a feature of a body: a native PartDesign::Mirrored inside the same body
        from .partdesign import pattern

        return pattern(ctx, p, "mirror", feat)
    target = ctx.get(p["target"])
    normal = p.get("normal") or {"XY": [0, 0, 1], "XZ": [0, 1, 0], "YZ": [1, 0, 0]}[p["plane"]]
    obj = ctx.add("Part::Mirroring", p.get("name"), "Mirror")
    obj.Source = target
    obj.Normal = App.Vector(*normal)
    obj.Base = App.Vector(*p["point"])
    ctx.recompute()
    ctx.verify_solid(obj, "Mirror")
    return obj


def _clone(ctx: Context, target: Any, name: Any, default: str) -> Any:
    from draftobjects.clone import Clone

    obj = ctx.add("Part::FeaturePython", name, default)
    Clone(obj)
    obj.Objects = [target]
    return obj


def copy(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])
    obj = _clone(ctx, target, p.get("name"), "Copy")
    obj.Placement = App.Placement(App.Vector(*p["offset"]), App.Rotation())
    ctx.recompute()
    ctx.verify_solid(obj, "Copy")
    return obj


def scale(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])
    f = p["factor"]
    obj = _clone(ctx, target, p.get("name"), "Scaled")
    obj.Scale = App.Vector(f, f, f) if not isinstance(f, list) else App.Vector(*f)
    ctx.mark_consumes(obj, target)
    ctx.recompute()
    ctx.verify_solid(obj, "Scale")
    return obj


HANDLERS = {"move": move, "rotate": rotate, "place": place, "mirror": mirror, "copy": copy, "scale": scale}
