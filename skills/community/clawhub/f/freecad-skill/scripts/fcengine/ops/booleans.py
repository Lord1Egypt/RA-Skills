"""Parametric booleans with result verification."""

from __future__ import annotations

import json
from typing import Any, Dict

from .. import errors, geometry
from ..document import Context
from ..errors import SkillError


def _overlaps(a: Any, b: Any) -> bool:
    return a.Shape.BoundBox.intersect(b.Shape.BoundBox)


BOOLEAN_TYPES = ("Part::Cut", "Part::MultiFuse", "Part::MultiCommon")
DEEP_CHAIN = 12


def _chain_depth(obj: Any) -> int:
    """How many booleans are stacked under ``obj`` along its deepest input."""
    depth, level, seen = 0, [obj], set()
    while level and depth < 200:
        nxt = []
        for o in level:
            for i in o.OutList:
                if i.TypeId in BOOLEAN_TYPES and i.Name not in seen:
                    seen.add(i.Name)
                    nxt.append(i)
        if not nxt:
            break
        depth, level = depth + 1, nxt
    return depth


def _warn_deep_chain(ctx: Context, obj: Any) -> None:
    """One warning per request: FreeCAD recomputes a boolean much more slowly when it sits on a long chain
    of earlier booleans (measured on 1.1: 50 holes cut one by one take 21 s, as one cut 1.3 s)."""
    if any(w["code"] == "DEEP_CHAIN" for w in ctx.warnings):
        return
    depth = _chain_depth(obj)
    if depth >= DEEP_CHAIN:
        ctx.warn(
            "DEEP_CHAIN",
            f"'{obj.Name}' sits on a chain of {depth} booleans; each further one gets slower to compute. "
            "Combine repeated features in one step: one 'cut' with all the 'tools', an array of the tool, "
            "or (in a body) one 'hole' with all its centres.",
        )


def cut(ctx: Context, p: Dict[str, Any]) -> Any:
    base = ctx.get(p["base"])
    tool_refs = p["tools"] if "tools" in p else [p["tool"]]
    tools = [ctx.get(t) for t in tool_refs]
    if base in tools:
        raise SkillError(errors.INVALID_PARAM, "An object cannot cut itself")
    base_volume = base.Shape.Volume
    obj = ctx.add("Part::Cut", p.get("name"), "Cut")
    if len(tools) == 1:
        tool = tools[0]
    else:
        tool = ctx.doc.addObject("Part::MultiFuse", f"{obj.Name}_Tools")
        tool.Label = tool.Name
        tool.Shapes = tools
        ctx.own_helper(obj, tool)
    obj.Base = base
    obj.Tool = tool
    obj.Refine = p["refine"]
    ctx.recompute()

    if obj.Shape.isNull() or obj.Shape.Volume <= 1e-9:
        raise SkillError(
            errors.EMPTY_RESULT,
            f"Cut '{obj.Name}' removed all material from '{base.Name}'",
            hint="The tool fully contains the base. Check tool sizes and positions.",
        )
    ctx.verify_solid(obj, "Cut")
    removed = base_volume - obj.Shape.Volume
    if removed <= 1e-6 * max(base_volume, 1.0):
        missed = [t.Name for t in tools if not _overlaps(base, t)]
        ctx.warn(
            "NO_EFFECT",
            f"cut removed no material from '{base.Name}'"
            + (f"; {missed} do not overlap it" if missed else "; the tools touch but do not penetrate it")
            + f". Base bbox {json.dumps(geometry.bbox(base.Shape))}, tool bbox {json.dumps(geometry.bbox(tool.Shape))}",
        )
    else:
        for t in tools:
            if not _overlaps(base, t):
                ctx.warn("NO_EFFECT", f"tool '{t.Name}' does not overlap '{base.Name}' and removed nothing")
    _warn_deep_chain(ctx, obj)
    return obj


def fuse(ctx: Context, p: Dict[str, Any]) -> Any:
    objs = [ctx.get(n) for n in p["objects"]]
    obj = ctx.add("Part::MultiFuse", p.get("name"), "Fusion")
    obj.Shapes = objs
    obj.Refine = p["refine"]
    ctx.recompute()
    ctx.verify_solid(obj, "Fusion")
    n = len(obj.Shape.Solids)
    if n > 1:
        ctx.warn(
            "DISJOINT",
            f"fusion result has {n} separate solids: some objects do not touch. "
            "Move them to overlap if one connected part is intended.",
        )
    _warn_deep_chain(ctx, obj)
    return obj


def common(ctx: Context, p: Dict[str, Any]) -> Any:
    objs = [ctx.get(n) for n in p["objects"]]
    obj = ctx.add("Part::MultiCommon", p.get("name"), "Common")
    obj.Shapes = objs
    obj.Refine = p["refine"]
    ctx.recompute()
    if obj.Shape.isNull() or not obj.Shape.Solids or obj.Shape.Volume <= 1e-9:
        raise SkillError(
            errors.EMPTY_RESULT,
            f"Common '{obj.Name}' is empty: the objects do not overlap",
            details={o.Name: geometry.bbox(o.Shape) for o in objs},
        )
    ctx.verify_solid(obj, "Common")
    return obj


HANDLERS = {"cut": cut, "fuse": fuse, "common": common}
