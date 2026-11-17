"""Static request validation against the catalog (pure Python).

Validation happens before the document is touched, and reports *all*
problems at once so the agent can fix a request in one round trip.
"""

from __future__ import annotations

import difflib
import math
import re
from typing import Any, Dict, List, Optional

from . import catalog, errors, profiles, selectors
from .catalog import Op, Param

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,59}$")
NONZERO_VECTORS = ("direction", "axis", "normal")
MIN_SIZE = 1e-6  # mm; OCC's confusion tolerance is 1e-7
MAX_INSTANCES = 5000  # array instances per op: beyond this FreeCAD takes minutes
CELL_ADDRESS = re.compile(r"^[A-Za-z]{1,2}[0-9]+$")

# Names FreeCAD rejects as spreadsheet aliases (unit symbols, constants, keywords),
# measured with FreeCAD 1.1 (see tests). Checked statically so all are reported at once.
RESERVED_PARAM_NAMES = frozenset(
    {
        "A",
        "AS",
        "C",
        "CV",
        "F",
        "False",
        "G",
        "GHz",
        "GPa",
        "H",
        "Hz",
        "J",
        "K",
        "M",
        "MA",
        "MHz",
        "MN",
        "MOhm",
        "MPa",
        "MS",
        "MeV",
        "N",
        "Nm",
        "None",
        "Ohm",
        "Pa",
        "S",
        "T",
        "True",
        "V",
        "VA",
        "W",
        "Wb",
        "Ws",
        "cal",
        "cd",
        "cm",
        "cwt",
        "deg",
        "dm",
        "e",
        "eV",
        "ft",
        "g",
        "gon",
        "h",
        "in",
        "kA",
        "kHz",
        "kJ",
        "kN",
        "kOhm",
        "kPa",
        "kS",
        "kV",
        "kW",
        "kcal",
        "keV",
        "kg",
        "km",
        "ksi",
        "l",
        "lb",
        "lbf",
        "m",
        "mA",
        "mF",
        "mH",
        "mJ",
        "mK",
        "mN",
        "mS",
        "mV",
        "mW",
        "mg",
        "mi",
        "mil",
        "min",
        "ml",
        "mm",
        "mmol",
        "mol",
        "mph",
        "nF",
        "nH",
        "nm",
        "oz",
        "pF",
        "pi",
        "psi",
        "rad",
        "s",
        "st",
        "t",
        "thou",
        "uF",
        "uH",
        "uK",
        "uS",
        "ug",
        "um",
        "yd",
    }
)
PARAM_SUGGESTIONS = {
    "W": "width",
    "H": "height",
    "h": "height",
    "l": "length",
    "t": "thickness",
    "d": "diameter",
    "m": "mass",
    "s": "spacing",
    "g": "gap",
    "e": "edge_dist",
    "A": "area",
    "C": "clearance",
    "in": "inner",
}


class Problems:
    def __init__(self) -> None:
        self.items: List[Dict[str, Any]] = []

    def add(
        self, message: str, step: Optional[int] = None, op: Optional[str] = None, param: Optional[str] = None
    ) -> None:
        item: Dict[str, Any] = {"message": message}
        if step is not None:
            item["step"] = step
        if op:
            item["op"] = op
        if param:
            item["param"] = param
        self.items.append(item)


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _is_vector(v: Any) -> bool:
    return isinstance(v, list) and len(v) == 3 and all(_is_number(c) for c in v)


def _suggest(word: str, options: List[str]) -> str:
    close = difflib.get_close_matches(word, options, n=1, cutoff=0.6)
    return f" Did you mean '{close[0]}'?" if close else ""


def _check_value(p: Param, v: Any) -> Optional[str]:
    """Return an error message, or None if ``v`` is valid for ``p``.

    May normalise enums in place by returning None after the caller
    re-reads ``normalised`` - handled in ``_normalise``.
    """
    t = p.type
    if t == "number":
        if isinstance(v, str) and p.expr:
            if not v.startswith("=") or len(v.strip()) < 2:
                return "expression strings must start with '=' (e.g. \"=Params.width * 2\")"
            return None
        if not _is_number(v):
            return "must be a number" + (" or an '=expression' string" if p.expr else "")
        if p.gt is not None and not v > p.gt:
            return f"must be > {p.gt}"
        if p.gt == 0 and v < MIN_SIZE:
            return f"is below FreeCAD's modelling precision ({MIN_SIZE} mm); sizes are in millimetres"
        if p.ge is not None and not v >= p.ge:
            return f"must be >= {p.ge}"
        if p.le is not None and not v <= p.le:
            return f"must be <= {p.le}"
        return None
    if t == "integer":
        if isinstance(v, bool) or not isinstance(v, int):
            return "must be an integer"
        if p.ge is not None and v < p.ge:
            return f"must be >= {int(p.ge)}"
        if p.le is not None and v > p.le:
            return f"must be <= {int(p.le)}"
        return None
    if t in ("string", "path"):
        if not isinstance(v, str) or not v.strip():
            return "must be a non-empty string"
        return None
    if t == "bool":
        return None if isinstance(v, bool) else "must be true or false"
    if t == "name":
        return None if isinstance(v, str) and v.strip() else "must be an object name"
    if t == "names":
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
            return "must be a non-empty list of object names"
        if p.min_items and len(v) < p.min_items:
            return f"needs at least {p.min_items} objects"
        if len(set(v)) != len(v):
            return "contains duplicates"
        return None
    if t == "newname":
        if not isinstance(v, str) or not IDENTIFIER.match(v):
            return "must be an identifier: letters, digits and '_', starting with a letter or '_' (max 60 chars)"
        return None
    if t == "label":
        if not isinstance(v, str) or not v.strip():
            return "must be non-empty text"
        if v != v.strip() or len(v) > 100 or any(ord(c) < 32 for c in v):
            return "must have no leading/trailing spaces or control characters, max 100 characters"
        return None
    if t == "vector":
        if not _is_vector(v):
            return "must be [x, y, z] numbers"
        if p.name in NONZERO_VECTORS and all(c == 0 for c in v):
            return "must not be the zero vector"
        return None
    if t == "points":
        if not isinstance(v, list) or len(v) < 3:
            return "needs at least 3 points"
        dims = set()
        for pt in v:
            if not isinstance(pt, list) or len(pt) not in (2, 3) or not all(_is_number(c) for c in pt):
                return "each point must be [a, b] or [x, y, z] numbers"
            dims.add(len(pt))
        if len(dims) > 1:
            return "mix of 2D and 3D points; use one form"
        if len({tuple(pt) for pt in v}) != len(v):
            return "contains duplicate points (the polygon is closed automatically; do not repeat the first point)"
        return None
    if t == "color":
        if isinstance(v, str):
            return None if re.fullmatch(r"#?[0-9a-fA-F]{6}", v) else "must be '#RRGGBB' or [r, g, b] with 0..1 values"
        if isinstance(v, list) and len(v) == 3 and all(_is_number(c) and 0 <= c <= 1 for c in v):
            return None
        return "must be '#RRGGBB' or [r, g, b] with 0..1 values"
    if t == "sections":
        if not isinstance(v, list) or len(v) < 2:
            return "needs at least 2 sections"
        if len(v) > 50:
            return "at most 50 sections"
        for k, sec in enumerate(v):
            if not isinstance(sec, dict) or "shape" not in sec:
                return f'sections[{k}] must be {{"shape": {{...}}, "plane": "XY", "offset": 0}}'
            extra = set(sec) - {"shape", "plane", "offset"}
            if extra:
                return f"sections[{k}]: unknown keys {sorted(extra)}; allowed: shape, plane, offset"
            if sec.get("plane", "XY") not in ("XY", "XZ", "YZ"):
                return f"sections[{k}].plane must be XY, XZ or YZ"
            off = sec.get("offset", 0)
            if not (_is_number(off) or (isinstance(off, str) and off.startswith("=") and len(off) > 1)):
                return f"sections[{k}].offset must be a number or an '=expression'"
            try:
                profiles.shape_segments(sec["shape"], 0)
            except profiles.ProfileError as e:
                return f"sections[{k}]: {str(e).replace('shapes[0]', 'shape')}"
        return None
    if t == "path3d":
        if not isinstance(v, list) or len(v) < 2 or len(v) > 500:
            return "needs 2 to 500 [x, y, z] points"
        if not all(_is_vector(pt) for pt in v):
            return "each point must be [x, y, z]"
        return None
    if t == "helix":
        if not isinstance(v, dict):
            return 'must be {"radius": r, "pitch": p, "height": h}'
        extra = set(v) - {"radius", "pitch", "height", "left_handed", "center", "axis"}
        if extra:
            return f"unknown keys {sorted(extra)}; allowed: radius, pitch, height, left_handed, center, axis"
        for key in ("radius", "pitch", "height"):
            if not _is_number(v.get(key)) or v[key] <= 0:
                return f"'{key}' must be a number > 0"
        if v["height"] / v["pitch"] > 500:
            return "more than 500 turns"
        if "left_handed" in v and not isinstance(v["left_handed"], bool):
            return "'left_handed' must be true or false"
        for key in ("center", "axis"):
            if key in v and not _is_vector(v[key]):
                return f"'{key}' must be [x, y, z]"
        if "axis" in v and all(c == 0 for c in v["axis"]):
            return "'axis' must not be [0, 0, 0]"
        return None
    if t == "centers":
        if not isinstance(v, list) or not v:
            return "needs at least one [a, b] point"
        if not all(isinstance(pt, list) and len(pt) == 2 and all(_is_number(c) for c in pt) for pt in v):
            return "each point must be [a, b] numbers in the plane"
        if len({tuple(pt) for pt in v}) != len(v):
            return "contains duplicate points"
        return None
    if t == "enum":
        if not isinstance(v, str) or v.upper() not in {c.upper() for c in p.choices}:
            return f"must be one of {list(p.choices)}"
        return None
    if t == "selector":
        try:
            selectors.check(v)
        except selectors.SelectorError as e:
            return f"invalid selector: {e}"
        return None
    if t == "rotation":
        if not isinstance(v, dict) or set(v) != {"axis", "angle"}:
            return 'must be {"axis": [x, y, z], "angle": degrees}'
        if not _is_vector(v["axis"]) or all(c == 0 for c in v["axis"]):
            return "rotation axis must be a non-zero [x, y, z]"
        if not _is_number(v["angle"]):
            return "rotation angle must be a number (degrees)"
        return None
    if t == "number_or_vector":
        if _is_number(v):
            return None if v != 0 else "must not be 0"
        if _is_vector(v):
            return None if all(c != 0 for c in v) else "components must not be 0"
        return "must be a number or [x, y, z]"
    if t == "shapes":
        try:
            if profiles.has_expressions(v):
                profiles.check_expressions(v)
                return None
            profiles.all_segments(v)
        except profiles.ProfileError as e:
            return f"invalid: {e}"
        return None
    if t == "views":
        allowed = ("iso", "front", "back", "left", "right", "top", "bottom")
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x in allowed for x in v):
            return f"must be a non-empty list of {list(allowed)}"
        if len(v) > 8:
            return "at most 8 views"
        return None
    if t == "expect":
        msgs = expect_problems(v)
        return "; ".join(m.replace("'expect' ", "") for m in msgs) if msgs else None
    if t == "parts":
        if not isinstance(v, list) or not v:
            return "must be a non-empty list of parts"
        names = []
        for k, part in enumerate(v):
            if not isinstance(part, dict) or not isinstance(part.get("object"), str):
                return f"parts[{k}] must be an object with 'object' (the solid to add)"
            extra = set(part) - {"object", "name", "position", "rotation", "ground"}
            if extra:
                return f"parts[{k}]: unknown keys {sorted(extra)}"
            if "name" in part and not (isinstance(part["name"], str) and IDENTIFIER.match(part["name"])):
                return f"parts[{k}].name must be an identifier"
            if "position" in part and not _is_vector(part["position"]):
                return f"parts[{k}].position must be [x, y, z]"
            if "rotation" in part and _check_value(catalog.Param("rotation", "rotation", ""), part["rotation"]):
                return f'parts[{k}].rotation must be {{"axis": [x, y, z], "angle": deg}}'
            if "ground" in part and not isinstance(part["ground"], bool):
                return f"parts[{k}].ground must be true or false"
            names.append(part.get("name") or f"{part['object']}_Part")
        if len(set(names)) != len(names):
            return "two parts get the same name: give 'name' to repeated objects"
        return None
    if t == "jointref":
        if not isinstance(v, dict) or not isinstance(v.get("part"), str):
            return 'must be {"part": name, "face": selector} or {"part": name, "edge": selector}'
        kinds = [k for k in ("face", "edge") if k in v]
        if len(kinds) != 1 or set(v) - {"part", "face", "edge"}:
            return "give 'part' and exactly one of 'face' or 'edge'"
        try:
            selectors.check(v[kinds[0]])
        except selectors.SelectorError as e:
            return f"invalid {kinds[0]} selector: {e}"
        return None
    if t == "loads":
        if not isinstance(v, list) or not v:
            return "must be a non-empty list of loads"
        for k, ld in enumerate(v):
            if not isinstance(ld, dict) or "faces" not in ld or (("force" in ld) == ("pressure" in ld)):
                return f"loads[{k}] must have 'faces' and exactly one of 'force' or 'pressure'"
            extra = set(ld) - {"faces", "force", "pressure", "direction"}
            if extra:
                return f"loads[{k}]: unknown keys {sorted(extra)}"
            try:
                selectors.check(ld["faces"])
            except selectors.SelectorError as e:
                return f"loads[{k}].faces: {e}"
            key = "force" if "force" in ld else "pressure"
            if not isinstance(ld[key], str) or not ld[key].strip():
                unit = "N" if key == "force" else "MPa"
                return f"loads[{k}].{key} must be a string with units, e.g. '500 {unit}' (bare numbers are ambiguous)"
            if key == "force":
                if not _is_vector(ld.get("direction")) or all(c == 0 for c in ld["direction"]):
                    return f"loads[{k}] with a force needs 'direction': a non-zero [x, y, z]"
            elif "direction" in ld:
                return f"loads[{k}]: a pressure acts along the face normal; remove 'direction'"
        return None
    if t == "object":
        return None if isinstance(v, dict) and v else "must be a non-empty JSON object"
    return f"unknown parameter type {t}"


def _normalise(p: Param, v: Any) -> Any:
    if p.type == "enum":
        for c in p.choices:
            if c.upper() == v.upper():
                return c
    return v


def expect_problems(exp: Any) -> List[str]:
    """Problems with an expectations object (shared by step 'expect' and op 'check')."""
    if not isinstance(exp, dict) or not exp:
        return ["'expect' must be a non-empty object"]
    out: List[str] = []
    for k, v in exp.items():
        if k not in catalog.EXPECT_KEYS:
            out.append(
                f"unknown expectation '{k}'.{_suggest(k, list(catalog.EXPECT_KEYS))} Known: {list(catalog.EXPECT_KEYS)}"
            )
        elif k in ("bbox_size", "bbox_min", "bbox_max") and not _is_vector(v):
            out.append(f"expect.{k} must be [x, y, z] (three numbers)")
        elif k in ("volume", "tolerance", "volume_tolerance") and not (_is_number(v) and v >= 0):
            out.append(f"expect.{k} must be a non-negative number")
        elif k == "solids" and (isinstance(v, bool) or not isinstance(v, int) or v < 0):
            out.append("expect.solids must be a non-negative integer")
        elif k in ("valid", "self_intersecting") and not isinstance(v, bool):
            out.append(f"expect.{k} must be true or false")
    if exp and set(exp) <= {"tolerance", "volume_tolerance"}:
        out.append(
            "expect has only tolerances; add something to check (volume, bbox_size, bbox_min, bbox_max, solids, valid, self_intersecting)"
        )
    return out


def _check_expect(exp: Any, i: int, op: str, probs: Problems) -> None:
    for msg in expect_problems(exp):
        probs.add(msg, i, op, "expect")


def _static_op_checks(op: Op, params: Dict[str, Any], i: int, probs: Problems) -> None:
    """Cross-parameter checks that need no document."""
    n = op.name
    if n == "torus":
        r1, r2 = params.get("radius1"), params.get("radius2")
        if _is_number(r1) and _is_number(r2) and r2 >= r1:
            probs.add("radius2 (tube) must be smaller than radius1 (ring)", i, n, "radius2")
    if n == "cone":
        r1, r2 = params.get("radius1"), params.get("radius2")
        if _is_number(r1) and _is_number(r2):
            if r1 == 0 and r2 == 0:
                probs.add("radius1 and radius2 cannot both be 0", i, n, "radius1")
            elif r1 == r2:
                probs.add("radius1 equals radius2: use 'cylinder' instead", i, n, "radius2")
    if n in ("cylinder", "cone", "torus", "prism") and "direction" in params and "rotation" in params:
        probs.add("give either 'direction' or 'rotation', not both", i, n, "direction")
    if n == "delete":
        if params.get("all") and params.get("targets"):
            probs.add("give either 'targets' or all=true, not both", i, n, "targets")
        if not params.get("all") and not params.get("targets"):
            probs.add("give 'targets' or all=true", i, n, "targets")
    if n == "place" and "position" not in params and "rotation" not in params:
        probs.add("give 'position' and/or 'rotation'", i, n)
    if n in ("extrude", "revolve") and "points" in params and "offset" in params:
        probs.add("'offset' applies to 'shapes'; with 'points' give 3D points instead", i, n, "offset")
    if n == "sweep" and profiles.has_expressions(params.get("shapes")):
        probs.add("'=expression' values are not supported in sweep profiles; give numbers", i, n, "shapes")
    if n == "set_params" and isinstance(params.get("values"), dict):
        for alias, value in params["values"].items():
            if not isinstance(alias, str) or not IDENTIFIER.match(alias) or CELL_ADDRESS.match(alias):
                probs.add(
                    f"parameter name '{alias}' must be an identifier and not a cell address like 'A1'", i, n, "values"
                )
            elif alias in RESERVED_PARAM_NAMES:
                probs.add(
                    f"parameter name '{alias}' is reserved by FreeCAD (unit symbol, constant or keyword); "
                    f"use e.g. '{PARAM_SUGGESTIONS.get(alias, alias + '_val')}'",
                    i,
                    n,
                    "values",
                )
            if isinstance(value, str):
                if not value.strip().lstrip("="):
                    probs.add(f"parameter '{alias}' is an empty string", i, n, "values")
            elif not _is_number(value):
                probs.add(
                    f"parameter '{alias}' must be a finite number, or a string with a unit such as '15 deg'",
                    i,
                    n,
                    "values",
                )
    if n in ("extrude", "revolve"):
        in_body = "body" in params
        mode = params.get("mode", "add")
        if not in_body:
            if mode == "remove":
                probs.add("mode 'remove' needs a 'body'; outside a body, cut with op 'cut'", i, n, "mode")
            for k in ("through_all", "reversed"):
                if params.get(k):
                    probs.add(f"'{k}' only applies inside a body", i, n, k)
            if isinstance(params.get("offset"), str):
                probs.add("'offset' expressions need a body; outside a body give a number", i, n, "offset")
        elif "points" in params and params["points"] and len(params["points"][0]) == 3:
            probs.add(
                "inside a body give 2D 'points' (with 'plane'/'offset') or 'shapes', not 3D points", i, n, "points"
            )
    if n == "extrude":
        if "body" in params:
            if "direction" in params:
                probs.add(
                    "'direction' is not available inside a body; use 'plane', 'offset' and 'reversed'",
                    i,
                    n,
                    "direction",
                )
            through = bool(params.get("through_all"))
            if through and params.get("mode", "add") != "remove":
                probs.add("'through_all' only applies with mode 'remove'", i, n, "through_all")
            if through == ("height" in params):
                probs.add("give exactly one of 'height' or through_all=true", i, n, "height")
        elif ("height" in params) == ("direction" in params):
            probs.add("give exactly one of ['height', 'direction']", i, n, "height")
    if n == "fem_static" and params.get("require") is not None:
        for k, val in params["require"].items():
            if k not in ("min_safety_factor", "max_displacement"):
                probs.add(
                    f"unknown requirement '{k}'. Known: ['min_safety_factor', 'max_displacement']", i, n, "require"
                )
            elif not (_is_number(val) and val > 0):
                probs.add(f"require.{k} must be a positive number", i, n, "require")
    if n == "measure":
        if "material" in params and "density" in params:
            probs.add("give 'material' or 'density', not both", i, n, "density")
        req = params.get("require")
        if req is not None:
            for k, v in req.items():
                if k == "min_clearance":
                    if not (_is_number(v) and v >= 0):
                        probs.add("require.min_clearance must be a non-negative number (mm)", i, n, "require")
                elif k == "no_interference":
                    if not isinstance(v, bool):
                        probs.add("require.no_interference must be true or false", i, n, "require")
                else:
                    probs.add(
                        f"unknown requirement '{k}'.{_suggest(k, ['min_clearance', 'no_interference'])} Known: ['min_clearance', 'no_interference']",
                        i,
                        n,
                        "require",
                    )
    if n == "hole":
        kind = params.get("type", "simple")
        if "cut_depth" in params and kind != "counterbore":
            probs.add("'cut_depth' only applies to type 'counterbore'", i, n, "cut_depth")
        if "cut_diameter" in params and kind == "simple":
            probs.add("'cut_diameter' needs type 'counterbore' or 'countersink'", i, n, "cut_diameter")
        if "diameter" in params and kind != "simple":
            need = ["cut_diameter"] + (["cut_depth"] if kind == "counterbore" else [])
            missing = [k for k in need if k not in params]
            if missing:
                probs.add(
                    f"with an explicit 'diameter', a {kind} needs {missing} (or use 'size' for standard values)",
                    i,
                    n,
                    missing[0],
                )
        if "fit" in params and "size" not in params:
            probs.add("'fit' applies with 'size'", i, n, "fit")
    if n == "linear_array" and _is_vector(params.get("step")) and all(c == 0 for c in params["step"]):
        probs.add("'step' must not be [0, 0, 0]: every copy would sit on the original", i, n, "step")
    if n == "grid_array":
        counts = [params.get(f"count_{a}", 1) for a in ("x", "y", "z")]
        if all(isinstance(c, int) and not isinstance(c, bool) for c in counts):
            total = counts[0] * counts[1] * counts[2]
            if total > MAX_INSTANCES:
                probs.add(f"{total} instances; a grid can have at most {MAX_INSTANCES}", i, n, "count_x")
        for axis in ("x", "y", "z"):
            count, step = params.get(f"count_{axis}", 1), params.get(f"step_{axis}", 0)
            if isinstance(count, int) and count > 1 and _is_number(step) and step == 0:
                probs.add(
                    f"'step_{axis}' must not be 0 when count_{axis} > 1: the copies would overlap exactly",
                    i,
                    n,
                    f"step_{axis}",
                )
    # L1: 'Params' is the parameter spreadsheet's name
    if n not in ("set_params",) and params.get("name") == "Params":
        probs.add("'Params' is reserved for the parameter spreadsheet (set_params); choose another name", i, n, "name")
    if n == "rename" and params.get("label") == params.get("target"):
        probs.add("label is unchanged", i, n, "label")


def validate_step(raw: Any, i: int, probs: Problems) -> Optional[Dict[str, Any]]:
    if not isinstance(raw, dict):
        probs.add("each step must be a JSON object with an 'op' key", i)
        return None
    name = raw.get("op")
    if not isinstance(name, str):
        probs.add("missing 'op'", i)
        return None
    op = catalog.OPS_BY_NAME.get(name)
    if op is None:
        probs.add(
            f"unknown op '{name}'.{_suggest(name, list(catalog.OPS_BY_NAME))} Run 'describe' to list operations.",
            i,
            name,
        )
        return None

    known = [p.name for p in op.params]
    params: Dict[str, Any] = {}
    for key, value in raw.items():
        p = op.param(key)
        if p is None and key in catalog.STEP_KEYS:
            continue
        if p is None:
            probs.add(f"unknown parameter '{key}'.{_suggest(key, known)} Valid: {known}", i, name, key)
            continue
        if value is None:
            continue  # explicit null == omitted
        msg = _check_value(p, value)
        if msg:
            probs.add(f"'{key}' {msg}", i, name, key)
            continue
        params[key] = _normalise(p, value)

    for p in op.params:
        if p.required and p.name not in params and not any(p.name in g for g in op.one_of):
            if p.name not in raw:
                probs.add(f"missing required parameter '{p.name}' ({p.doc})", i, name, p.name)
    for group in op.one_of:
        given = [g for g in group if g in params or raw.get(g) is not None]
        if len(given) != 1:
            probs.add(f"give exactly one of {list(group)}", i, name, group[0])

    _static_op_checks(op, params, i, probs)

    # Defaults last so cross-checks only see what the agent wrote.
    for p in op.params:
        if p.name not in params and p.default is not None:
            params[p.name] = p.default

    step: Dict[str, Any] = {"index": i, "op": name, "params": params}
    if "expect" in raw and op.param("expect") is None:
        _check_expect(raw["expect"], i, name, probs)
        step["expect"] = raw["expect"]
    return step


def validate_request(req: Any) -> Dict[str, Any]:
    """Validate and normalise a request. Raises SkillError."""
    if isinstance(req, dict) and "operation" in req:
        raise errors.SkillError(
            errors.INVALID_REQUEST,
            'The v1 request format ({"operation": ..., "parameters": ...}) is no longer supported',
            hint='Use {"doc": "model.FCStd", "steps": [{"op": "box", "length": 10, ...}]}; run \'describe\' for the operations.',
        )
    if not isinstance(req, dict):
        raise errors.SkillError(
            errors.INVALID_REQUEST,
            "Request must be a JSON object",
            hint='Send {"doc": "model.FCStd", "steps": [{"op": "box", ...}]}',
        )

    # Single-step shorthand: {"op": "inspect", "doc": "x.FCStd"}
    if "op" in req and "steps" not in req:
        step = {k: v for k, v in req.items() if k not in catalog.REQUEST_KEYS}
        req = {k: v for k, v in req.items() if k in catalog.REQUEST_KEYS}
        req["steps"] = [step]

    probs = Problems()
    for key in req:
        if key not in catalog.REQUEST_KEYS:
            probs.add(
                f"unknown request key '{key}'.{_suggest(key, list(catalog.REQUEST_KEYS))} Valid: {list(catalog.REQUEST_KEYS)}"
            )
    doc = req.get("doc", "model.FCStd")
    if not isinstance(doc, str) or not doc.lower().endswith(".fcstd"):
        probs.add("'doc' must be a path ending in .FCStd")
    for flag in ("new", "dry_run", "brief"):
        if flag in req and not isinstance(req[flag], bool):
            probs.add(f"'{flag}' must be true or false")
    steps_raw = req.get("steps")
    steps: List[Dict[str, Any]] = []
    if not isinstance(steps_raw, list) or not steps_raw:
        probs.add("'steps' must be a non-empty list of operations")
    else:
        for i, raw in enumerate(steps_raw):
            s = validate_step(raw, i, probs)
            if s is not None:
                steps.append(s)

    if probs.items:
        n = len(probs.items)
        raise errors.SkillError(
            errors.INVALID_REQUEST,
            f"{n} problem{'s' if n > 1 else ''} in request; nothing was executed",
            hint="Fix every listed problem and resend. Run 'describe <op>' for parameter details.",
            details={"problems": probs.items},
        )
    return {
        "doc": doc,
        "new": bool(req.get("new", False)),
        "dry_run": bool(req.get("dry_run", False)),
        "brief": bool(req.get("brief", False)),
        "steps": steps,
    }
