"""Editing existing objects: set, set_params, delete, rename."""

from __future__ import annotations

import difflib
import json
import re
from typing import Any, Dict, List

import FreeCAD as App

from .. import errors, selectors, validate
from ..catalog import Param
from ..document import SEL_PROP, Context, apply_selector, topo_sorted, visible_objects
from ..errors import SkillError

VECTOR_PROPS = ("App::PropertyVector", "App::PropertyVectorDistance", "App::PropertyPosition", "App::PropertyDirection")
ALIAS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
CELL_RE = re.compile(r"^[A-Za-z]{1,2}[0-9]+$")
PARAMS_SHEET = "Params"


# Properties every object has; left out of "available properties" hints.
_GENERIC_PROPS = {
    "Label",
    "Label2",
    "Placement",
    "Shape",
    "Visibility",
    "ExpressionEngine",
    "AttacherEngine",
    "AttacherType",
    "AttachmentOffset",
    "AttachmentSupport",
    "MapMode",
    "MapPathParameter",
    "MapReversed",
    "Support",
    "ShapeMaterial",
    "_ElementMapVersion",
}


def _read_only(obj: Any, prop: str) -> bool:
    try:
        return "ReadOnly" in obj.getEditorMode(prop) or "ReadOnly" in obj.getPropertyStatus(prop)
    except Exception:
        return False


def _convert(ctx: Context, obj: Any, prop: str, value: Any) -> Any:
    ptype = obj.getTypeIdOfProperty(prop)
    if ptype in VECTOR_PROPS:
        if not validate._is_vector(value):
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}.{prop} expects [x, y, z] (three finite numbers)")
        return App.Vector(*value)
    if ptype == "App::PropertyVectorList":
        return [App.Vector(*(list(v) + [0] * (3 - len(v)))) for v in value]
    if ptype in ("App::PropertyLink", "App::PropertyLinkGlobal"):
        return ctx.get(value, need_shape=False)
    if ptype in ("App::PropertyLinkList", "App::PropertyLinkListGlobal"):
        return [ctx.get(v, need_shape=False) for v in value]
    if ptype == "App::PropertyPlacement":
        raise SkillError(
            errors.INVALID_PARAM,
            "Placement cannot be set directly",
            hint='Use "position": [x, y, z] and/or "rotation": {"axis": [...], "angle": deg} in properties.',
        )
    return value


def _offset_axis(sk: Any) -> str:
    """Which AttachmentOffset.Base component carries the plane offset (see partdesign.make_sketch)."""
    n = sk.AttachmentOffset.Rotation.multVec(App.Vector(0, 0, 1))
    return "xyz"[max(range(3), key=lambda k: abs((n.x, n.y, n.z)[k]))]


def _set_alias(ctx: Context, obj: Any, key: str, value: Any) -> bool:
    """Op-level aliases for features created by this skill. True if handled."""
    t = obj.TypeId
    if key in ("position", "rotation"):
        from .transforms import _placement_owner

        msg = validate._check_value(Param(key, "vector" if key == "position" else "rotation", ""), value)
        if msg:
            raise SkillError(
                errors.INVALID_PARAM,
                f"{obj.Name}: '{key}' {msg}",
                hint='Example: {"position": [10, 0, 5], "rotation": {"axis": [0, 0, 1], "angle": 90}}.',
            )
        owner = _placement_owner(obj)
        if owner is not obj:
            ctx.warn(
                "REDIRECTED", f"'{obj.Name}' follows the placement of '{owner.Name}'; changed '{owner.Name}' instead"
            )
        pl = owner.Placement
        if key == "position":
            owner.Placement = App.Placement(App.Vector(*value), pl.Rotation)
        else:
            owner.Placement = App.Placement(pl.Base, App.Rotation(App.Vector(*value["axis"]), value["angle"]))
        return True
    from .text import set_text

    if set_text(ctx, obj, key, value):
        return True
    if t in ("Part::Loft", "PartDesign::AdditiveLoft", "PartDesign::SubtractiveLoft") and key in (
        "sections",
        "ruled",
        "closed",
    ):
        if key != "sections":
            if not isinstance(value, bool):
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: '{key}' must be true or false")
            setattr(obj, key.capitalize(), value)
            return True
        from .sweeps import set_sections

        set_sections(ctx, obj, value)
        return True
    if key in ("path", "smooth", "corner_radius", "helix", "up", "shapes"):
        from .sweeps import set_sweep, sweep_parts

        parts = sweep_parts(ctx, obj)
        if parts is not None:
            set_sweep(ctx, obj, parts, key, value)
            return True
    if t in ("PartDesign::Fillet", "PartDesign::Chamfer", "PartDesign::Thickness") and key in (
        "radius",
        "size",
        "thickness",
        "edges",
        "open_faces",
    ):
        if key in ("edges", "open_faces"):
            selectors.check(value)
            apply_selector(obj, key, value, None)
            if selectors.is_dynamic(value):
                ctx.set_selector(obj, key, value)
            elif SEL_PROP in obj.PropertiesList:
                obj.removeProperty(SEL_PROP)
        else:
            if not validate._is_number(value) or value <= 0:
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: '{key}' must be a number > 0")
            prop = {"PartDesign::Fillet": "Radius", "PartDesign::Chamfer": "Size", "PartDesign::Thickness": "Value"}[t]
            setattr(obj, prop, float(value))
        return True
    if t in (
        "PartDesign::Pad",
        "PartDesign::Pocket",
        "PartDesign::Revolution",
        "PartDesign::Groove",
        "PartDesign::Hole",
    ) and key in ("shapes", "points", "offset", "at"):
        sk = obj.Profile[0]
        if key == "offset":
            axis = _offset_axis(sk)
            if isinstance(value, str):
                ctx.assign(sk, f".AttachmentOffset.Base.{axis}", value)
            elif validate._is_number(value):
                sk.setExpression(f".AttachmentOffset.Base.{axis}", None)
                base = sk.AttachmentOffset.Base
                setattr(base, axis, float(value))
                sk.AttachmentOffset = App.Placement(base, sk.AttachmentOffset.Rotation)
            else:
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'offset' must be a number or '=expression'")
            return True
        from .sketch import fill_sketch

        if key == "at":
            if t != "PartDesign::Hole":
                raise SkillError(errors.INVALID_PARAM, f"'at' applies to holes; set 'shapes' on '{obj.Name}'")
            msg = validate._check_value(Param("at", "centers", ""), value)
            if msg:
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'at' {msg}")
            r = obj.Diameter.Value / 2
            fill_sketch(sk, [{"circle": pt, "radius": r} for pt in value])
        else:
            if t == "PartDesign::Hole":
                raise SkillError(errors.INVALID_PARAM, f"set 'at' to move holes of '{obj.Name}'")
            shapes = value if key == "shapes" else [{"polygon": value}]
            fill_sketch(sk, shapes)
        return True
    if t in ("Part::Fillet", "Part::Chamfer") and key in ("radius", "size", "edges"):
        if key == "edges":
            selectors.check(value)
            apply_selector(obj, "edges", value, None)
            if selectors.is_dynamic(value):
                ctx.set_selector(obj, "edges", value)
            elif SEL_PROP in obj.PropertiesList:
                obj.removeProperty(SEL_PROP)
        else:
            if not validate._is_number(value) or value <= 0:
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: '{key}' must be a number > 0")
            r = float(value)
            obj.Edges = [(e[0], r, r) for e in obj.Edges]
        return True
    if t == "Part::Thickness" and key in ("thickness", "open_faces"):
        if key == "thickness":
            if not validate._is_number(value) or value <= 0:
                raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'thickness' must be a number > 0")
            v = float(value)
            obj.Value = v if obj.Value > 0 else -v
        else:
            selectors.check(value)
            apply_selector(obj, "open_faces", value, None)
            if selectors.is_dynamic(value):
                ctx.set_selector(obj, "open_faces", value)
            elif SEL_PROP in obj.PropertiesList:
                obj.removeProperty(SEL_PROP)  # explicit indices replace the stored selector
        return True
    if t in ("Part::Extrusion", "Part::Revolution") and key in ("points", "shapes"):
        prof = obj.Base if t == "Part::Extrusion" else obj.Source
        if key == "points":
            if prof.TypeId != "Part::Polygon":
                raise SkillError(errors.INVALID_PARAM, f"'{obj.Name}' was built from 'shapes'; set 'shapes' instead")
            prof.Nodes = [App.Vector(*(list(v) + [0] * (3 - len(v)))) for v in value]
        else:
            if prof.TypeId != "Sketcher::SketchObject":
                raise SkillError(errors.INVALID_PARAM, f"'{obj.Name}' was built from 'points'; set 'points' instead")
            from .sketch import fill_sketch

            fill_sketch(prof, value)
        return True
    return False


# Never writable through 'set', whatever their editor mode says.
PROTECTED_PROPS = ("Shape", "Proxy", "ExpressionEngine", "Label2", "Visibility", "PropertiesList")


def _set_label(ctx: Context, obj: Any, value: Any) -> None:
    msg = validate._check_value(Param("Label", "label", ""), value)
    if msg:
        raise SkillError(errors.INVALID_PARAM, f"'Label' {msg}")
    for o in visible_objects(ctx.doc):
        if o is not obj and (o.Name == value or o.Label == value):
            raise SkillError(
                errors.NAME_CONFLICT,
                f"'{value}' is already used by another object",
                hint="Labels must be unique; FreeCAD would silently rename it.",
            )
    obj.Label = value


def set_(ctx: Context, p: Dict[str, Any]) -> Any:
    obj = ctx.get(p["target"], need_shape=False)
    for key, value in p["properties"].items():
        if key == "Label":
            _set_label(ctx, obj, value)
            continue
        if key in PROTECTED_PROPS or key.startswith("FCSkill"):
            raise SkillError(
                errors.INVALID_PARAM,
                f"{obj.Name}.{key} cannot be set",
                hint="It is computed by FreeCAD or kept by the skill. Change the object's dimensions or inputs instead.",
            )
        try:
            if _set_alias(ctx, obj, key, value):
                continue
        except SkillError:
            raise
        except Exception as e:
            raise SkillError(errors.INVALID_PARAM, f"Cannot set {obj.Name}.{key}: {e}") from None
        if key not in obj.PropertiesList and key.split(".")[0] in ("Placement", ".Placement"):
            raise SkillError(
                errors.INVALID_PARAM,
                f"Placement cannot be set through '{key}'",
                hint='Use "position": [x, y, z] and/or "rotation": {"axis": [...], "angle": deg} in properties, '
                "or the move/rotate/place ops. Placement expressions are not supported.",
            )
        if key not in obj.PropertiesList:
            close = difflib.get_close_matches(key, obj.PropertiesList, n=3, cutoff=0.5)
            ci = [x for x in obj.PropertiesList if x.lower() == key.lower()]
            guess = ci or close
            own = [
                p
                for p in obj.PropertiesList
                if p not in _GENERIC_PROPS and not p.startswith("FCSkill") and not _read_only(obj, p)
            ][:12]
            start = (
                f"Did you mean {guess}? "
                if guess
                else (
                    f"{obj.TypeId} properties: {own}. "
                    if own
                    else f"{obj.TypeId} has no editable dimensions (not parametric). "
                )
            )
            raise SkillError(
                errors.INVALID_PARAM,
                f"'{obj.Name}' has no property '{key}'",
                hint=start + "Property names are case-sensitive; 'inspect' with target lists editable properties.",
            )
        if _read_only(obj, key):
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}.{key} is read-only")
        if value is None:
            obj.setExpression(key, None)
            continue
        if isinstance(value, str) and value.startswith("="):
            ctx.assign(obj, key, value)
            continue
        if any(prop == key for prop, _ in obj.ExpressionEngine):
            obj.setExpression(key, None)  # a literal value replaces an expression
        try:
            setattr(obj, key, _convert(ctx, obj, key, value))
        except SkillError:
            raise
        except Exception as e:
            raise SkillError(
                errors.INVALID_PARAM,
                f"Cannot set {obj.Name}.{key} = {json.dumps(value)}: {e}",
                hint=f"Property type is {obj.getTypeIdOfProperty(key)}.",
            ) from None
    ctx.mutated = True
    ctx.reselect()
    ctx.recompute()
    return obj


def set_params(ctx: Context, p: Dict[str, Any]) -> Any:
    sheet = ctx.doc.getObject(PARAMS_SHEET)
    if sheet is None:
        sheet = ctx.doc.addObject("Spreadsheet::Sheet", PARAMS_SHEET)
        sheet.Label = PARAMS_SHEET
    elif not sheet.TypeId.startswith("Spreadsheet::"):
        raise SkillError(errors.NAME_CONFLICT, f"'{PARAMS_SHEET}' exists but is not a spreadsheet")
    used_rows = [int(c[1:]) for c in sheet.getUsedCells() if c.startswith("A") and c[1:].isdigit()]
    next_row = max(used_rows, default=0) + 1
    for alias, value in p["values"].items():
        if not isinstance(alias, str) or not ALIAS_RE.match(alias) or CELL_RE.match(alias):
            raise SkillError(
                errors.INVALID_PARAM,
                f"Invalid parameter name '{alias}'",
                hint="Use identifiers like 'wall' or 'hole_d' (not cell addresses like 'A1').",
            )
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise SkillError(errors.INVALID_PARAM, f"Parameter '{alias}' must be a number or a string like '15 deg'")
        if isinstance(value, str):
            try:
                App.Units.Quantity(value.lstrip("="))
            except Exception:
                raise SkillError(
                    errors.INVALID_PARAM,
                    f"Parameter '{alias}': {value!r} is not a valid quantity",
                    hint="Use a number (millimetres) or a number with a FreeCAD unit, e.g. '15 deg', '2.5 mm', '1 in'.",
                ) from None
        content = repr(float(value)) if not isinstance(value, str) else ("=" + value.lstrip("="))
        cell = sheet.getCellFromAlias(alias)
        if not cell:
            cell = f"B{next_row}"
            sheet.set(f"A{next_row}", alias)
            sheet.set(cell, content)
            try:
                sheet.setAlias(cell, alias)
            except ValueError:
                raise SkillError(
                    errors.INVALID_PARAM,
                    f"FreeCAD rejects '{alias}' as a parameter name",
                    hint="Names must not be unit symbols (mm, m, t, s, g, h, in, ft, deg, ...) or cell addresses. Try a longer name such as 'thickness'.",
                ) from None
            next_row += 1
        else:
            sheet.set(cell, content)
    ctx.mutated = True
    ctx.recompute()
    ctx.reselect()
    ctx.recompute()
    return sheet


def _dependents(objs: List[Any]) -> List[Any]:
    out = {}
    for o in objs:
        for d in o.InListRecursive:
            out[d.Name] = d
    return list(out.values())


def delete(ctx: Context, p: Dict[str, Any]) -> Any:
    doc = ctx.doc
    if p.get("all"):
        victims = list(doc.Objects)
    else:
        targets = [ctx.get(t, need_shape=False) for t in p["targets"]]
        names = {t.Name for t in targets}
        deps = [d for d in _dependents(targets) if d.Name not in names]
        # helpers owned by a target die with it
        helpers = [doc.getObject(h) for t in targets for h in (getattr(t, "FCSkillHelpers", []) or [])]
        deps = [d for d in deps if d not in helpers]
        if deps and not p["with_dependents"]:
            raise SkillError(
                errors.DEPENDENCY,
                f"Cannot delete {sorted(names)}: other objects depend on them",
                hint="Delete the dependents too (with_dependents=true), or delete them first.",
                details={"dependents": sorted(d.Name for d in deps)},
            )
        victims = targets + deps + [h for h in helpers if h is not None]
    for obj in reversed(topo_sorted(list({o.Name: o for o in victims}.values()))):
        if doc.getObject(obj.Name) is not None:
            doc.removeObject(obj.Name)
    ctx.mutated = True
    ctx.recompute()
    return None


def rename(ctx: Context, p: Dict[str, Any]) -> Any:
    obj = ctx.get(p["target"], need_shape=False)
    new = p["label"]
    for o in visible_objects(ctx.doc):
        if o is not obj and (o.Name == new or o.Label == new):
            raise SkillError(
                errors.NAME_CONFLICT,
                f"'{new}' is already used by another object ('{o.Name}')",
                hint="Steps refer to objects by name or label, so both must be unique: choose another label "
                "(e.g. a suffix), or give the intermediate object a different name when creating it.",
            )
    obj.Label = new
    ctx.mutated = True
    return obj


HANDLERS = {"set": set_, "set_params": set_params, "delete": delete, "rename": rename}
