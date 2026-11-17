"""Fail-closed content-expression gates for model-authored final decks."""

from __future__ import annotations

import re


_ELLIPSIS_RE = re.compile(r"…|\.\.\.")
_FORBIDDEN_VISIBLE_RE = re.compile(
    r"(?i)(?:\b(?:undefined|null|nan|tbd|todo)\b|\[object\s+object\]|"
    r"lorem\s+ipsum|待补充|待完善|待定|待替换|占位(?:符|文本)?)"
)


def _visible_strings(slide: dict) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []

    def add(path: str, value: object) -> None:
        if isinstance(value, str) and value.strip():
            values.append((path, value.strip()))

    add("title", slide.get("title"))
    add("message", slide.get("message"))
    for block_index, block in enumerate(slide.get("blocks", [])):
        if not isinstance(block, dict):
            continue
        prefix = f"blocks/{block_index}"
        for field in ("text", "label", "value", "unit", "baseline", "delta", "caption"):
            add(f"{prefix}/{field}", block.get(field))
        for item_index, item in enumerate(block.get("items", []) or []):
            if not isinstance(item, dict):
                continue
            add(f"{prefix}/items/{item_index}/text", item.get("text"))
            add(f"{prefix}/items/{item_index}/detail", item.get("detail"))
            for action_index, action in enumerate(item.get("action_items", []) or []):
                add(f"{prefix}/items/{item_index}/action_items/{action_index}", action)
    for chart_name in ("chart",):
        chart = slide.get(chart_name)
        if isinstance(chart, dict):
            for index, category in enumerate(chart.get("data", {}).get("categories", [])):
                add(f"{chart_name}/categories/{index}", category)
            for index, series in enumerate(chart.get("data", {}).get("series", [])):
                if isinstance(series, dict):
                    add(f"{chart_name}/series/{index}/name", series.get("name"))
    for chart_index, chart in enumerate(slide.get("charts", []) or []):
        if not isinstance(chart, dict):
            continue
        for index, category in enumerate(chart.get("data", {}).get("categories", [])):
            add(f"charts/{chart_index}/categories/{index}", category)
        for index, series in enumerate(chart.get("data", {}).get("series", [])):
            if isinstance(series, dict):
                add(f"charts/{chart_index}/series/{index}/name", series.get("name"))
    diagram = slide.get("diagram_ir")
    if isinstance(diagram, dict):
        for index, node in enumerate(diagram.get("nodes", []) or []):
            if isinstance(node, dict):
                add(f"diagram_ir/nodes/{index}/label", node.get("label"))
                add(f"diagram_ir/nodes/{index}/detail", node.get("detail"))
        for index, edge in enumerate(diagram.get("edges", []) or []):
            if isinstance(edge, dict):
                add(f"diagram_ir/edges/{index}/label", edge.get("label"))
    return values


def evaluate_model_authored_quality(
    ir: dict,
    *,
    require_assertions: bool = True,
) -> dict:
    """Reject source-page substitution, truncated copy, and empty expression."""
    issues: list[dict] = []
    per_slide: list[dict] = []
    for index, slide in enumerate(ir.get("slides", []), 1):
        if not isinstance(slide, dict):
            continue
        slide_id = str(slide.get("id") or index)
        role = slide.get("slide_role", "content")
        visible = _visible_strings(slide)
        visible_chars = sum(len(text) for _, text in visible)
        for path, text in visible:
            if _FORBIDDEN_VISIBLE_RE.search(text):
                issues.append({
                    "code": "MODEL_AUTHORED_PLACEHOLDER_TEXT",
                    "slide_id": slide_id,
                    "path": path,
                    "text": text[:160],
                })
        if role not in {"cover", "section", "closing"}:
            message = slide.get("message")
            if require_assertions and (
                not isinstance(message, str) or len(message.strip()) < 12
            ):
                issues.append({"code": "SLIDE_ASSERTION_MISSING", "slide_id": slide_id})
            has_visual = bool(
                slide.get("chart") or slide.get("charts") or slide.get("diagram_ir")
                or any(
                    isinstance(block, dict) and block.get("role") in {"image", "table"}
                    for block in slide.get("blocks", [])
                )
            )
            if visible_chars < 60 and not has_visual:
                issues.append({
                    "code": "VISIBLE_CONTENT_TOO_SPARSE",
                    "slide_id": slide_id,
                    "visible_characters": visible_chars,
                })
        for path, text in visible:
            if _ELLIPSIS_RE.search(text):
                issues.append({
                    "code": "VISIBLE_CONTENT_ELLIPSIS",
                    "slide_id": slide_id,
                    "path": path,
                    "text": text,
                })
        for block_index, block in enumerate(slide.get("blocks", [])):
            if not isinstance(block, dict) or block.get("role") != "image":
                continue
            asset_kind = block.get("asset_kind")
            crop = block.get("crop_audit")
            if asset_kind == "page_screenshot":
                issues.append({
                    "code": "SOURCE_PAGE_SCREENSHOT_FORBIDDEN",
                    "slide_id": slide_id,
                    "block_index": block_index,
                })
            if asset_kind is None or not isinstance(crop, dict):
                issues.append({
                    "code": "IMAGE_AUTHORING_AUDIT_REQUIRED",
                    "slide_id": slide_id,
                    "block_index": block_index,
                })
                continue
            contaminated = [
                field for field in (
                    "includes_page_header", "includes_page_footer",
                    "includes_navigation", "includes_body_prose",
                )
                if crop.get(field) is True
            ]
            if contaminated:
                issues.append({
                    "code": "SOURCE_ILLUSTRATION_CROP_CONTAMINATED",
                    "slide_id": slide_id,
                    "block_index": block_index,
                    "contaminated_fields": contaminated,
                })
            if asset_kind in {"data_figure"} and block.get("reconstructable") is not False:
                issues.append({
                    "code": "NATIVE_DATA_VISUAL_REQUIRED",
                    "slide_id": slide_id,
                    "block_index": block_index,
                })
        per_slide.append({
            "slide_id": slide_id,
            "visible_character_count": visible_chars,
            "visible_string_count": len(visible),
        })
    return {
        "status": "pass" if not issues else "fail",
        "slides": per_slide,
        "issues": issues,
    }
