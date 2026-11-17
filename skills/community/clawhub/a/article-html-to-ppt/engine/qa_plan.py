"""Plan-level QA: fail-closed checks on the Render Plan, before any pptx
exists. Blank-page detection is an *error*, not a warning (D9) — the
pipeline may only ship a deck whose plan passes.

Codes:
  SLIDE_EMPTY            content zone essentially unpopulated
  ELEMENT_OUT_OF_BOUNDS  frame exceeds the canvas
  TEXT_OVERFLOW_RISK     estimated text height exceeds its frame
  CONTRAST_LOW           text vs background contrast under 3.0
  FONT_BELOW_FLOOR       run below the 8pt absolute floor
"""

from __future__ import annotations

from .textfit import paragraphs_height_emu

CONTRAST_FLOOR = 3.0
FONT_FLOOR_CPT = 800
MIN_CONTENT_COVERAGE = 0.05


def _luminance(hex_color: str) -> float:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = sorted((_luminance(fg), _luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def _issue(code: str, slide_id: str, element_id: str | None, message: str) -> dict:
    return {"code": code, "slide_id": slide_id, "element_id": element_id,
            "message": message}


def _element_runs(element: dict):
    for para in element.get("paragraphs", []) or []:
        yield para, element.get("fill")
    for row in element.get("rows", []) or []:
        for cell in row.get("cells", []):
            for para in cell.get("paragraphs", []):
                yield para, cell.get("fill") or element.get("fill")


def check_plan(plan: dict) -> dict:
    errors: list[dict] = []
    warnings: list[dict] = []
    canvas = plan["canvas"]
    cw, ch = canvas["width_emu"], canvas["height_emu"]

    for slide in plan["slides"]:
        sid = slide["slide_id"]
        bg = slide.get("background", {}).get("color", "#FFFFFF")
        content_area = 0

        for element in slide["elements"]:
            eid = element["element_id"]
            role = element.get("semantic_role", "")
            is_footer = role.startswith("footer")
            frame = element.get("frame")
            if frame:
                if frame["x"] < 0 or frame["y"] < 0 or \
                        frame["x"] + frame["w"] > cw or frame["y"] + frame["h"] > ch:
                    errors.append(_issue("ELEMENT_OUT_OF_BOUNDS", sid, eid,
                                         f"frame {frame} exceeds canvas"))
                if role != "title" and not is_footer:
                    content_area += frame["w"] * frame["h"]

            if element.get("type") in ("textbox", "shape") and frame:
                pad = 304800 if element["type"] == "shape" else 182880
                total_h = paragraphs_height_emu(element.get("paragraphs", []) or [],
                                                max(frame["w"] - pad, 1))
                if total_h > frame["h"] * 1.08:
                    errors.append(_issue("TEXT_OVERFLOW_RISK", sid, eid,
                                         f"estimated text {total_h} EMU vs frame {frame['h']}"))

            if is_footer:
                continue  # footer text sits on the primary bar, not the bg
            for para, fill in _element_runs(element):
                back = (fill or {}).get("color", bg)
                for run in para["runs"]:
                    if run["size_cpt"] < FONT_FLOOR_CPT:
                        errors.append(_issue("FONT_BELOW_FLOOR", sid, eid,
                                             f"{run['size_cpt']} cpt"))
                    ratio = contrast_ratio(run["color"], back)
                    if ratio < CONTRAST_FLOOR:
                        errors.append(_issue("CONTRAST_LOW", sid, eid,
                                             f"{ratio:.2f} for {run['color']} on {back}"))

        title_only = all(e.get("semantic_role") in ("title", "footer")
                         for e in slide["elements"])
        coverage = content_area / (cw * ch)
        if sid != "cover" and (title_only or coverage < MIN_CONTENT_COVERAGE):
            errors.append(_issue("SLIDE_EMPTY", sid, None,
                                 f"content coverage {coverage:.3f}"))

    return {"status": "pass" if not errors else "fail",
            "error_count": len(errors), "errors": errors, "warnings": warnings}
