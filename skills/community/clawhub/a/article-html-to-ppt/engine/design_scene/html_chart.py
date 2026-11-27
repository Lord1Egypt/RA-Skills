"""Validate a data-chart specification and translate its display options to native chart fields."""
import json
import math

from jsonschema import Draft202012Validator

from .contract import AXIS, BOOL, SHORT, arr, enum, num, obj
from .store import DesignError

HEX = {"type": "string", "pattern": "^#?[0-9a-fA-F]{6}$"}
PALETTE = ["4B4FD6", "F2804F", "2BB9A9", "A473D9", "E0B23F", "688DC4"]
VALUE = num(-1e12, 1e12)
CHART = Draft202012Validator(obj({
    "type": enum("line", "column", "bar", "stacked_column", "stacked_bar", "pie", "doughnut"),
    "categories": arr(SHORT, 200, 1),
    "series": arr(obj({"name": SHORT, "values": arr(VALUE, 200, 1),
                       "color": HEX, "area": BOOL}, ["name", "values"]), 20, 1),
    "font": SHORT, "font_size": num(6, 200), "min": VALUE, "max": VALUE, "major": AXIS["properties"]["major"],
    "colors": arr(HEX, 20, 1), "labels": BOOL, "legend": BOOL, "legend_position": enum("bottom", "right"),
    "label_number_format": SHORT, "axis_number_format": SHORT, "label_colors": arr(HEX, 200, 1), "hole_size": num(10, 90),
    "axis": AXIS, "markers": BOOL, "gap_width": {"type": "integer", "minimum": 0, "maximum": 500},
}, ["categories", "series"]))


def parse_chart(raw):
    def reject_constant(_):
        raise ValueError("non-finite JSON number")

    try:
        spec = json.loads(raw, parse_constant=reject_constant)
    except (ValueError, RecursionError) as exc:
        raise DesignError("HTML_CHART_DATA_INVALID: invalid chart JSON") from exc
    return validate_chart(spec)


def _label(value):
    if type(value) not in (int, float):
        return value
    # JSON.parse uses binary64. An unquoted long ID would change before layout extraction.
    if not -9_007_199_254_740_991 <= value <= 9_007_199_254_740_991:
        raise DesignError("HTML_CHART_DATA_INVALID: use a quoted string for long numeric category or series labels")
    return str(value)


def validate_chart(spec):
    # Previous releases accepted numeric category labels and numeric strings as data values.
    if isinstance(spec, dict) and isinstance(spec.get("categories"), list) and isinstance(spec.get("series"), list):
        spec = dict(spec)
        spec["categories"] = [_label(c) for c in spec["categories"]]
        series = []
        for s in spec["series"]:
            if isinstance(s, dict) and isinstance(s.get("values"), list):
                try:
                    values = [float(v) if isinstance(v, str) else v for v in s["values"]]
                except (ValueError, OverflowError) as exc:
                    raise DesignError("HTML_CHART_DATA_INVALID: series values must be finite numbers") from exc
                if any(isinstance(v, float) and not math.isfinite(v) for v in values):
                    raise DesignError("HTML_CHART_DATA_INVALID: series values must be finite numbers")
                s = {**s, "values": values, "name": _label(s.get("name"))}
            series.append(s)
        spec["series"] = series
    error = next(CHART.iter_errors(spec), None)
    if error:
        path = ".".join(map(str, error.absolute_path)) or "data-chart"
        if path == "type":
            raise DesignError(f"HTML_CHART_TYPE_UNSUPPORTED: {spec['type']}")
        raise DesignError(f"HTML_CHART_DATA_INVALID: {path} ({error.validator})")
    categories, series = spec["categories"], spec["series"]
    if any(len(s["values"]) != len(categories) for s in series):
        raise DesignError("HTML_CHART_DATA_INVALID: each series needs one value per category")
    kind = spec.get("type", "line")
    sector = kind in {"pie", "doughnut"}
    if sector and (len(series) != 1 or min(series[0]["values"]) < 0 or sum(series[0]["values"]) <= 0):
        raise DesignError("HTML_CHART_DATA_INVALID: pie and doughnut require one nonnegative series with a positive total")
    if (("hole_size" in spec and kind != "doughnut") or ("label_colors" in spec and not sector)
            or (sector and any(key in spec for key in ("axis", "min", "max", "major", "axis_number_format")))
            or ("gap_width" in spec and kind not in {"column", "bar", "stacked_column", "stacked_bar"})
            or (kind != "line" and ("markers" in spec or any(s.get("area") for s in series)))):
        raise DesignError("HTML_CHART_DATA_INVALID: display option does not apply to the selected chart type")
    axis = {**{k: spec[k] for k in ("min", "max", "major") if k in spec}, **spec.get("axis", {})}
    if "min" in axis and "max" in axis and axis["min"] >= axis["max"]:
        raise DesignError("HTML_CHART_DATA_INVALID: axis max must exceed min")
    if "major" in axis:
        if kind in {"stacked_column", "stacked_bar"}:
            pos = [sum(max(0, s["values"][i]) for s in series) for i in range(len(categories))]
            neg = [sum(min(0, s["values"][i]) for s in series) for i in range(len(categories))]
            lo, hi = axis.get("min", min(0, *neg)), axis.get("max", max(0, *pos))
        else:
            values = [v for s in series for v in s["values"]]
            lo, hi = axis.get("min", min(0, min(values))), axis.get("max", max(0, max(values)))
        if hi - lo > 200 * axis["major"]:
            raise DesignError("HTML_CHART_DATA_INVALID: choose a major unit with at most 200 intervals")
    return spec


def native_chart_options(spec):
    kind = spec.get("type", "line")
    series = spec["series"]
    colors = spec.get("colors") or [s.get("color", PALETTE[0]) for s in series]
    sector = kind in {"pie", "doughnut"}
    if sector and "colors" not in spec and "color" not in series[0]:
        colors = PALETTE
    axis = {"gridline_color": "EDEFF5", "line_color": "E6E8F0", "label_color": "A0A4B8", "label_size": 8,
            "category_padding": True, **{k: spec[k] for k in ("min", "max", "major") if k in spec},
            **({"number_format": spec["axis_number_format"]} if "axis_number_format" in spec else {}),
            **spec.get("axis", {})}
    options = {"chart_type": kind, "colors": [c.lstrip("#").upper() for c in colors],
               "font": {"family": spec.get("font", "__page__"), "size": spec.get("font_size", 8.5),
                        "color": axis["label_color"]},
               "legend": spec.get("legend", False), "labels": spec.get("labels", True),
               **{k: spec[k] for k in ("hole_size", "legend_position", "label_number_format") if k in spec}}
    if "label_colors" in spec:
        options["label_colors"] = [c.lstrip("#").upper() for c in spec["label_colors"]]
    if not sector:
        default_pos = "above" if kind == "line" else "center" if kind in {"stacked_column", "stacked_bar"} else "outside_end"
        options.update(axis=axis, label_position=default_pos)
    if kind == "line":
        options["markers"] = spec.get("markers", True)
        area = [i for i, s in enumerate(series) if s.get("area")]
        if area:
            options["area_series"] = area
    if kind in {"column", "bar", "stacked_column", "stacked_bar"}:
        options["gap_width"] = spec.get("gap_width", 100)
    return options
