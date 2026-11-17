"""Text as a solid: a Draft ShapeString (letters from a font) extruded along the plane normal.

Probed on FreeCAD 1.1 (headless):
- ShapeString works without the GUI. Each glyph becomes one or more faces (with holes for 'o', 'e', ...), so
  the extrusion is a compound of one solid per glyph part; fused onto or cut from a part it is ordinary geometry.
- A missing font file or a blank string does not fail the recompute: ShapeString keeps its previous shape and
  only prints a message. Both are checked here before any recompute.
- FontFile is an absolute path. FreeCAD's own font lives inside the installation, whose path changes with
  updates (snap revisions), so the default font is re-located on every edit instead of trusting the stored path.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import FreeCAD as App

from .. import errors, workspace
from ..document import Context
from ..errors import SkillError
from .sketch import PLANES, plane_placement

FONT_PROP = "FCSkillFont"  # "default" or the workspace-relative font path
DEFAULT_FONT = "osifont-lgpl3fe.ttf"  # ships with FreeCAD (TechDraw), LGPL
FONT_EXTS = (".ttf", ".otf", ".ttc", ".pfb")
JUSTIFY = {
    "bottom_left": "Bottom-Left",
    "bottom_center": "Bottom-Center",
    "bottom_right": "Bottom-Right",
    "middle_left": "Middle-Left",
    "center": "Middle-Center",
    "middle_right": "Middle-Right",
    "top_left": "Top-Left",
    "top_center": "Top-Center",
    "top_right": "Top-Right",
}
TEXT_KEYS = ("text", "size", "font", "align", "height")


def _default_font() -> str:
    rel = os.path.join("Mod", "TechDraw", "Resources", "fonts", DEFAULT_FONT)
    for base in (App.getResourceDir(), os.path.join(App.getHomePath(), "data"), App.getHomePath()):
        path = os.path.join(base, rel)
        if os.path.isfile(path):
            return path
    raise SkillError(
        errors.UNSUPPORTED,
        f"FreeCAD's bundled font ({DEFAULT_FONT}) was not found in this installation",
        hint="Put a .ttf or .otf font file in the workspace and give it as 'font'.",
    )


def _font(ctx: Context, ref: str) -> str:
    if ref == "default":
        return _default_font()
    path = workspace.resolve(ctx.root, ref)
    if not path.is_file():
        raise SkillError(errors.INVALID_PARAM, f"Font file '{ref}' not found in the workspace")
    if path.suffix.lower() not in FONT_EXTS:
        raise SkillError(errors.INVALID_PARAM, f"'{ref}' is not a font file ({', '.join(FONT_EXTS)})")
    return str(path)


def _check_text(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SkillError(errors.INVALID_PARAM, "'text' must contain at least one visible character")
    return value


def _shape_string(obj: Any) -> Optional[Any]:
    """The ShapeString behind a text solid made by this op, else None."""
    if obj.TypeId != "Part::Extrusion":
        return None
    base = obj.Base
    proxy = getattr(base, "Proxy", None) if base is not None else None
    return base if proxy is not None and type(proxy).__name__ == "ShapeString" else None


def _verify(ctx: Context, obj: Any) -> None:
    ss = obj.Base
    if ss.Shape.isNull() or not ss.Shape.Faces:
        raise SkillError(
            errors.EMPTY_RESULT,
            f"Text '{obj.Name}' produced no letters",
            hint="The font may lack these characters; try another 'font'.",
        )
    ctx.verify_solid(obj, "Text")


def text(ctx: Context, p: Dict[str, Any]) -> Any:
    from draftobjects.shapestring import ShapeString  # needs FreeCAD 1.1 headless (see compat.py)

    content = _check_text(p["text"])
    font_ref = p.get("font") or "default"
    font = _font(ctx, font_ref)
    plane = p.get("plane", "XY")
    obj = ctx.add("Part::Extrusion", p.get("name"), "Text")
    ss = ctx.doc.addObject("Part::Part2DObjectPython", f"{obj.Name}_String")
    ShapeString(ss)
    ss.Label = ss.Name
    ss.String = content
    ss.FontFile = font
    ss.Size = float(p["size"])
    ss.Justification = JUSTIFY[p.get("align", "bottom_left")]
    ss.JustificationReference = "Cap Height"
    # The plane's local axes (text reads along local X, upright along local Y), turned by 'angle' in the plane.
    base = plane_placement(plane, 0)
    turn = App.Rotation(App.Vector(0, 0, 1), float(p.get("angle", 0)))
    ss.Placement = App.Placement(App.Vector(*p.get("position", [0, 0, 0])), base.Rotation.multiply(turn))
    ss.addProperty("App::PropertyString", FONT_PROP, "FCSkill", "Font as requested: 'default' or a workspace file")
    ss.setEditorMode(FONT_PROP, 2)
    setattr(ss, FONT_PROP, font_ref)
    ctx.own_helper(obj, ss)
    obj.Base = ss
    obj.Solid = True
    obj.DirMode = "Custom"
    n = App.Vector(*PLANES[plane][2])
    obj.Dir = n * (-1.0 if p.get("reversed") else 1.0)
    ctx.assign(obj, "LengthFwd", p["height"])
    ctx.recompute()
    _verify(ctx, obj)
    font_name = DEFAULT_FONT if font_ref == "default" else font_ref
    return {"object": obj, "data": {"text": content, "font": font_name, "solids": len(obj.Shape.Solids)}}


def set_text(ctx: Context, obj: Any, key: str, value: Any) -> bool:
    """'set' aliases for a text solid: text, size, font, align, height. True if handled."""
    ss = _shape_string(obj)
    if ss is None or key not in TEXT_KEYS:
        return False
    if key == "height":
        if isinstance(value, str) and value.startswith("="):
            ctx.assign(obj, "LengthFwd", value)
        elif isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0:
            obj.setExpression("LengthFwd", None)
            obj.LengthFwd = float(value)
        else:
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'height' must be a number > 0 or '=expression'")
        return True
    ref = getattr(ss, FONT_PROP, "default") if FONT_PROP in ss.PropertiesList else "default"
    if key == "text":
        ss.String = _check_text(value)
    elif key == "size":
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'size' must be a number > 0")
        ss.Size = float(value)
    elif key == "align":
        if value not in JUSTIFY:
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'align' must be one of {list(JUSTIFY)}")
        ss.Justification = JUSTIFY[value]
    else:
        if not isinstance(value, str) or not value:
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'font' must be 'default' or a font file path")
        ref = value
        if FONT_PROP in ss.PropertiesList:
            setattr(ss, FONT_PROP, ref)
    ss.FontFile = _font(ctx, ref)  # re-located every time: a stale path would silently keep the old letters
    ctx.recompute()
    _verify(ctx, obj)
    return True


HANDLERS = {"text": text}
