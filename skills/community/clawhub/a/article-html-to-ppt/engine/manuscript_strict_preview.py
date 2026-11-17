"""Build a source-bound strict preview bundle for a complete manuscript."""
from __future__ import annotations

from copy import deepcopy


TITLE_SOURCE = {
    "source_slide_index": 34,
    "shape_names": ["文本框 10"],
}

PLACEHOLDER_SOURCE = {
    "source_slide_index": 1,
    "shape_names": ["矩形 144", "文本框 69", "文本框 70"],
    "title_shape_name": "文本框 69",
    "detail_shape_name": "文本框 70",
    "placement": {"x": 0.08, "y": 0.3, "w": 0.84, "h": 0.28},
}


def _indexed_item(items: list[dict], index: int) -> dict:
    while len(items) <= index:
        items.append({})
    return items[index]


def _add_component_binding(
    blocks: dict[str, dict],
    binding_name: str,
    text: str,
    purpose: str,
    *,
    source_ref: dict | None = None,
    source_refs: list[dict] | None = None,
    evidence_id: str | None = None,
) -> None:
    parts = binding_name.split(":")
    if (
        len(parts) != 6
        or parts[:2] != ["bind", "block"]
        or parts[2] != purpose
        or parts[4] not in {"item", "detail"}
    ):
        raise ValueError(f"unsupported manuscript component binding {binding_name!r}")
    try:
        item_index = int(parts[5])
    except ValueError as exc:
        raise ValueError(f"component binding index must be an integer: {binding_name!r}") from exc
    if item_index < 0:
        raise ValueError(f"component binding index must be non-negative: {binding_name!r}")
    block_id, field = parts[3], parts[4]
    block = blocks.setdefault(block_id, {"id": block_id, "role": "list", "items": []})
    item = _indexed_item(block["items"], item_index)
    target_field = "text" if field == "item" else "detail"
    existing = item.get(target_field)
    if existing is not None and existing != text:
        raise ValueError(f"conflicting component binding value for {binding_name!r}")
    item[target_field] = text
    for metadata_field, value in (
        ("source_ref", deepcopy(source_ref) if isinstance(source_ref, dict) else None),
        ("evidence_id", evidence_id if isinstance(evidence_id, str) else None),
    ):
        if value is None:
            continue
        existing_metadata = item.get(metadata_field)
        if existing_metadata is not None and existing_metadata != value:
            raise ValueError(
                f"conflicting {metadata_field} for component item {item_index}"
            )
        item[metadata_field] = value
    if isinstance(source_refs, list):
        merged = [
            ref for ref in item.get("source_refs", [])
            if isinstance(ref, dict)
        ]
        for ref in source_refs:
            if isinstance(ref, dict) and ref not in merged:
                merged.append(deepcopy(ref))
        if merged:
            item["source_refs"] = merged


def _component_bindings(operation: dict, blocks: dict[str, dict], purpose: str) -> None:
    elements = operation.get("elements")
    if not isinstance(elements, list) or not elements:
        raise ValueError("component operation requires non-empty elements")
    for element in elements:
        if not isinstance(element, dict):
            raise ValueError("component element must be an object")
        if "binding_name" in element:
            text = element.get("text")
            if not isinstance(text, str):
                raise ValueError("legacy component element requires text")
            _add_component_binding(
                blocks, element["binding_name"], text, purpose,
                source_ref=element.get("source_ref"),
                source_refs=element.get("source_refs"),
                evidence_id=element.get("evidence_id"),
            )
            continue
        labels = element.get("labels")
        if not isinstance(labels, dict) or not labels:
            raise ValueError("extended component element requires labels")
        for label in labels.values():
            if not isinstance(label, dict):
                raise ValueError("component label must be an object")
            text, binding_name = label.get("text"), label.get("binding_name")
            if not isinstance(text, str) or not isinstance(binding_name, str):
                raise ValueError("component label requires text and binding_name")
            _add_component_binding(
                blocks, binding_name, text, purpose,
                source_ref=label.get("source_ref"),
                source_refs=label.get("source_refs"),
                evidence_id=label.get("evidence_id"),
            )


def _text_bindings(operation: dict, blocks: dict[str, dict], purpose: str) -> None:
    text_bindings = operation.get("text_bindings")
    if not isinstance(text_bindings, list):
        raise ValueError(f"{operation.get('kind')} requires text_bindings")
    for text_binding in text_bindings:
        if not isinstance(text_binding, dict):
            raise ValueError("component text bindings must be objects")
        binding_name = text_binding.get("binding_name")
        text = text_binding.get("text")
        if not isinstance(binding_name, str) or not isinstance(text, str):
            raise ValueError("component text binding requires binding_name and text")
        _add_component_binding(
            blocks, binding_name, text, purpose,
            source_ref=text_binding.get("source_ref"),
            source_refs=text_binding.get("source_refs"),
            evidence_id=text_binding.get("evidence_id"),
        )


def _append_chart(ir_slide: dict, chart: dict) -> None:
    if not isinstance(chart, dict) or not isinstance(chart.get("id"), str):
        raise ValueError("component chart requires an id")
    if not isinstance(chart.get("data"), dict):
        raise ValueError("component chart requires data")
    ir_slide.setdefault("charts", []).append({
        "id": chart["id"],
        "data": deepcopy(chart["data"]),
    })


def expected_component_element_count(operation: dict) -> int:
    """Return semantic element capacity represented by one component operation."""
    kind = operation.get("kind") if isinstance(operation, dict) else None
    if kind == "chart_dashboard_clone":
        charts = operation.get("charts")
        if not isinstance(charts, list):
            raise ValueError("dashboard clone requires charts")
        return len(charts)
    if kind == "chart_component_clone":
        if not isinstance(operation.get("chart"), dict):
            raise ValueError("chart component clone requires chart")
        return 1
    if kind == "native_group_component_clone":
        requirement = operation.get("component_requirement")
        count = requirement.get("element_count") if isinstance(requirement, dict) else None
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ValueError("native group component requires a positive element_count")
        return count
    if kind == "component_clone":
        elements = operation.get("elements")
        if not isinstance(elements, list):
            raise ValueError("component clone requires elements")
        return len(elements)
    raise ValueError(f"unsupported component operation kind {kind!r}")


def rendered_component_element_count(operation: dict, shapes) -> int:
    """Count bound semantic elements for an already rendered component operation."""
    shape_list = list(shapes)
    shape_names = {getattr(shape, "name", None) for shape in shape_list}
    chart_names = {
        getattr(shape, "name", None)
        for shape in shape_list
        if getattr(shape, "has_chart", False)
    }
    kind = operation.get("kind") if isinstance(operation, dict) else None
    if kind == "chart_dashboard_clone":
        return sum(
            isinstance(chart, dict) and chart.get("binding_name") in chart_names
            for chart in operation.get("charts", [])
        )
    if kind == "chart_component_clone":
        chart = operation.get("chart")
        return int(isinstance(chart, dict) and chart.get("binding_name") in chart_names)
    if kind == "native_group_component_clone":
        bindings = operation.get("text_bindings")
        if not isinstance(bindings, list):
            return 0
        binding_names = [
            binding.get("binding_name")
            for binding in bindings
            if isinstance(binding, dict)
        ]
        if not binding_names or not all(name in shape_names for name in binding_names):
            return 0
        return expected_component_element_count(operation)
    if kind == "component_clone":
        instance_id = operation.get("component_instance_id")
        requirement = operation.get("component_requirement")
        family = requirement.get("family") if isinstance(requirement, dict) else None
        prefix = f"decoration:component:{family}:{instance_id}:segment:"
        return sum(
            isinstance(name, str) and name.startswith(prefix) and ":part:" not in name
            for name in shape_names
        )
    return 0


def _title_operation(*, purpose: str, title: str, destination_slide_index: int) -> dict:
    return {
        "kind": "native_group_clone",
        "source_slide_index": TITLE_SOURCE["source_slide_index"],
        "destination_slide_index": destination_slide_index,
        "shape_names": deepcopy(TITLE_SOURCE["shape_names"]),
        "placement": {"x": 0.03, "y": 0.03, "w": 0.8, "h": 0.08, "fit_mode": "stretch"},
        "text_bindings": [{
            "shape_name": TITLE_SOURCE["shape_names"][0],
            "binding_name": f"bind:slide:{purpose}:title",
            "text": title,
        }],
    }


def _placeholder_operation(
    *,
    purpose: str,
    destination_slide_index: int,
    detail: str,
) -> dict:
    return {
        "kind": "native_group_clone",
        "source_slide_index": PLACEHOLDER_SOURCE["source_slide_index"],
        "destination_slide_index": destination_slide_index,
        "shape_names": deepcopy(PLACEHOLDER_SOURCE["shape_names"]),
        "placement": deepcopy(PLACEHOLDER_SOURCE["placement"]),
        "text_bindings": [{
            "shape_name": PLACEHOLDER_SOURCE["title_shape_name"],
            "binding_name": f"bind:block:{purpose}:unsupported_status:item:0",
            "text": "组件待补充",
        }, {
            "shape_name": PLACEHOLDER_SOURCE["detail_shape_name"],
            "binding_name": f"bind:block:{purpose}:unsupported_status:detail:0",
            "text": detail,
        }],
    }


def build_manuscript_strict_preview_bundle(
    *,
    content_bindings: dict,
    storyboard: dict,
    composition: dict,
    component_plan: dict,
) -> dict:
    """Join component operations with titles, IR, and explicit gap disclosure."""
    content_slides = content_bindings.get("slides") if isinstance(content_bindings, dict) else None
    storyboard_slides = storyboard.get("slides") if isinstance(storyboard, dict) else None
    operations = component_plan.get("operations") if isinstance(component_plan, dict) else None
    if not isinstance(content_slides, list) or not content_slides:
        raise ValueError("content bindings require a non-empty slides list")
    if not isinstance(storyboard_slides, list) or not storyboard_slides:
        raise ValueError("storyboard requires a non-empty slides list")
    if not isinstance(operations, list):
        raise ValueError("component plan operations must be a list")
    if composition.get("source_page_count") != len(storyboard_slides):
        raise ValueError("composition source_page_count must match storyboard pages")
    template_slide_count = composition.get("template_slide_count")
    if isinstance(template_slide_count, bool) or not isinstance(template_slide_count, int):
        raise ValueError("composition requires template_slide_count")

    content_by_id = {
        slide.get("id"): slide
        for slide in content_slides
        if isinstance(slide, dict) and isinstance(slide.get("id"), str)
    }
    page_by_destination: dict[int, tuple[str, str]] = {}
    ir_slides: list[dict] = []
    ir_by_purpose: dict[str, dict] = {}
    title_operations: list[dict] = []
    blocks_by_purpose: dict[str, dict[str, dict]] = {}
    for page_index, storyboard_page in enumerate(storyboard_slides, 1):
        purpose = storyboard_page.get("purpose") if isinstance(storyboard_page, dict) else None
        content = content_by_id.get(purpose)
        if content is None:
            raise ValueError(f"storyboard purpose {purpose!r} has no content binding")
        title = content.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"content binding {purpose!r} requires a title")
        destination = template_slide_count + page_index
        page_by_destination[destination] = (purpose, title.strip())
        blocks_by_purpose[purpose] = {}
        ir_slide = {
            "id": purpose,
            "title": title.strip(),
            "slide_role": content.get("archetype", "body").replace("body", "content"),
            "blocks": [],
        }
        if isinstance(content.get("speaker_notes"), dict):
            ir_slide["speaker_notes"] = deepcopy(content["speaker_notes"])
        if isinstance(content.get("component_intent"), dict):
            ir_slide["component_intent"] = deepcopy(content["component_intent"])
        ir_slides.append(ir_slide)
        ir_by_purpose[purpose] = ir_slide
        title_operations.append(_title_operation(
            purpose=purpose,
            title=title.strip(),
            destination_slide_index=destination,
        ))

    for operation in operations:
        if not isinstance(operation, dict) or operation.get("kind") not in {
            "component_clone", "chart_component_clone", "chart_dashboard_clone",
            "native_group_component_clone",
        }:
            raise ValueError(
                "manuscript component plan may contain only reviewed component clone operations"
            )
        destination = operation.get("destination_slide_index")
        if destination not in page_by_destination:
            raise ValueError(f"component operation targets unknown destination slide {destination!r}")
        purpose, _title = page_by_destination[destination]
        if operation["kind"] == "component_clone":
            _component_bindings(operation, blocks_by_purpose[purpose], purpose)
            continue
        if operation["kind"] == "chart_component_clone":
            _append_chart(ir_by_purpose[purpose], operation.get("chart"))
            _text_bindings(operation, blocks_by_purpose[purpose], purpose)
            continue
        if operation["kind"] == "native_group_component_clone":
            _text_bindings(operation, blocks_by_purpose[purpose], purpose)
            continue
        charts = operation.get("charts")
        text_bindings = operation.get("text_bindings")
        if not isinstance(charts, list) or not charts or not isinstance(text_bindings, list):
            raise ValueError("dashboard clone requires charts and text_bindings")
        for chart in charts:
            _append_chart(ir_by_purpose[purpose], chart)
        _text_bindings(operation, blocks_by_purpose[purpose], purpose)

    unsupported_pages = composition.get("unsupported_pages")
    if not isinstance(unsupported_pages, list):
        raise ValueError("composition unsupported_pages must be a list")
    placeholder_operations: list[dict] = []
    for unsupported in unsupported_pages:
        page_index = unsupported.get("output_page_index") if isinstance(unsupported, dict) else None
        purpose = unsupported.get("purpose") if isinstance(unsupported, dict) else None
        destination = template_slide_count + page_index if isinstance(page_index, int) else None
        if destination not in page_by_destination or page_by_destination[destination][0] != purpose:
            raise ValueError("unsupported page does not align with the storyboard")
        layout_pattern = unsupported.get("layout_pattern") or "未声明布局"
        detail = (
            f"布局“{layout_pattern}”暂无 reviewed 组件；"
            "未使用不匹配组件。"
        )
        blocks_by_purpose[purpose]["unsupported_status"] = {
            "id": "unsupported_status",
            "role": "list",
            "items": [{"text": "组件待补充", "detail": detail}],
        }
        placeholder_operations.append(_placeholder_operation(
            purpose=purpose,
            destination_slide_index=destination,
            detail=detail,
        ))

    for ir_slide in ir_slides:
        ir_slide["blocks"] = list(blocks_by_purpose[ir_slide["id"]].values())

    combined_operations = title_operations + deepcopy(operations) + placeholder_operations
    evidence_ids: set[str] = set()
    source_references: set[tuple[str, str]] = set()
    for ir_slide in ir_slides:
        for block in ir_slide["blocks"]:
            for item in block.get("items", []):
                evidence_id = item.get("evidence_id")
                if isinstance(evidence_id, str):
                    evidence_ids.add(evidence_id)
                source_ref = item.get("source_ref")
                if (
                    isinstance(source_ref, dict)
                    and isinstance(source_ref.get("source_id"), str)
                    and isinstance(source_ref.get("loc"), str)
                ):
                    source_references.add((source_ref["source_id"], source_ref["loc"]))
                for multi_ref in item.get("source_refs", []) or []:
                    if (
                        isinstance(multi_ref, dict)
                        and isinstance(multi_ref.get("source_id"), str)
                        and isinstance(multi_ref.get("loc"), str)
                    ):
                        source_references.add((
                            multi_ref["source_id"], multi_ref["loc"],
                        ))
    return {
        "schema_version": "1.0.0",
        "ir": {"slides": ir_slides},
        "strict_plan": {
            "schema_version": "1.0.0",
            "operations": combined_operations,
        },
        "summary": {
            "output_pages": len(storyboard_slides),
            "component_operations": len(operations),
            "title_operations": len(title_operations),
            "placeholder_operations": len(placeholder_operations),
            "total_operations": len(combined_operations),
            "evidence_units": len(evidence_ids),
            "source_references": len(source_references),
        },
    }
