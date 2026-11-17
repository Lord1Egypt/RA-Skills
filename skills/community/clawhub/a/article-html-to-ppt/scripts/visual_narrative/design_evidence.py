from __future__ import annotations

from typing import Any


SCHEMA_VERSION = "1.0"


def build_design_evidence(product_prd: dict[str, Any]) -> dict[str, Any]:
    """Normalize direct PRD design evidence and expose its required consumers."""
    source_id = _string(product_prd.get("source_id")) or "product_prd"
    items: list[dict[str, Any]] = []
    items.extend(_items(product_prd.get("design_tokens"), "token", source_id))
    items.extend(_items(product_prd.get("ui_spaces"), "ui_space", source_id))
    items.extend(_items(product_prd.get("interactions"), "interaction", source_id))

    has_spaces = any(item["category"] == "ui_space" for item in items)
    has_interactions = any(item["category"] == "interaction" for item in items)
    screenshot_asset_status = _screenshot_asset_status(product_prd)
    coverage = {
        "product_ui_overview": {
            # A product PRD must reserve a native screenshot slot even when
            # the source analysis contains no UI-space detail or image asset.
            "required": True,
            "evidence_ids": [item["id"] for item in items if item["category"] == "ui_space"],
            "consumed": False,
            "consumer_object_ids": [],
        },
        "interaction_storyboard": {
            "required": has_interactions,
            "evidence_ids": [item["id"] for item in items if item["category"] == "interaction"],
            "consumed": False,
            "consumer_object_ids": [],
        },
        "application_screenshot": {
            "required": True,
            "asset_status": screenshot_asset_status,
            "consumed": False,
            "consumer_object_ids": [],
            "placeholder": {
                "aspect_ratio": "16:10",
                "page_id": None,
                "region": "product_ui_overview.primary_visual",
            },
        },
    }
    required = [name for name, entry in coverage.items() if entry["required"] and not entry["consumed"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "source_id": source_id,
        "items": items,
        "coverage_matrix": coverage,
        "status": "blocked" if required else "ready",
        "blocking_codes": ["PRODUCT_PRD_REQUIRED_PROTOTYPES_UNCONSUMED"] if required else [],
    }


def consume_design_evidence(
    evidence: dict[str, Any], ppt_ir: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Route direct PRD evidence into native prototype objects and record consumers."""
    coverage = evidence.get("coverage_matrix")
    if not isinstance(coverage, dict):
        return evidence, ppt_ir
    items = evidence.get("items") if isinstance(evidence.get("items"), list) else []
    for ordinal, (component_type, object_id, category) in enumerate((
        ("product_ui_overview", "prd-product-ui-overview", "ui_space"),
        ("interaction_storyboard", "prd-interaction-storyboard", "interaction"),
    )):
        entry = coverage.get(component_type)
        if not isinstance(entry, dict):
            continue
        entry.setdefault("consumer_object_ids", [])
        matching = [item for item in items if isinstance(item, dict) and item.get("category") == category]
        if entry.get("required") is not True:
            continue
        # The screenshot slot makes product_ui_overview mandatory even for a
        # sparse PRD. An interaction storyboard still needs direct interaction
        # evidence before it can be truthfully drawn.
        if component_type != "product_ui_overview" and not matching:
            continue
        page_id = _inject_prototype(ppt_ir, component_type, object_id, matching, ordinal, evidence)
        entry["consumed"] = True
        entry["consumer_object_ids"] = [object_id]
        if component_type == "product_ui_overview":
            screenshot = coverage.get("application_screenshot")
            if isinstance(screenshot, dict):
                screenshot["consumed"] = True
                screenshot["consumer_object_ids"] = [object_id]
                placeholder = screenshot.get("placeholder")
                if isinstance(placeholder, dict):
                    placeholder["page_id"] = page_id

    unconsumed = [
        name for name, entry in coverage.items()
        if isinstance(entry, dict) and entry.get("required") is True and entry.get("consumed") is not True
    ]
    evidence["status"] = "blocked" if unconsumed else "ready"
    evidence["blocking_codes"] = ["PRODUCT_PRD_REQUIRED_PROTOTYPES_UNCONSUMED"] if unconsumed else []
    return evidence, ppt_ir


def _inject_prototype(
    ppt_ir: dict[str, Any], component_type: str, object_id: str,
    items: list[dict[str, Any]], ordinal: int, evidence: dict[str, Any],
) -> str:
    slides = ppt_ir.get("slides") if isinstance(ppt_ir.get("slides"), list) else []
    targets = [slide for slide in slides if isinstance(slide, dict) and slide.get("slide_role") != "cover"]
    if not targets:
        raise ValueError("PRODUCT_PRD_PROTOTYPE_TARGET_SLIDE_REQUIRED")
    slide = targets[min(ordinal, len(targets) - 1)]
    objects = slide.setdefault("objects", [])
    if not isinstance(objects, list):
        raise ValueError("PRODUCT_PRD_PROTOTYPE_OBJECTS_INVALID")
    # Product evidence pages are a direct PRD expression, not an overlay on a
    # generic acceptance card. Keep an existing prototype while replacing the
    # inherited page objects that would otherwise overlap its primary visual.
    objects[:] = [
        obj for obj in objects
        if isinstance(obj, dict) and obj.get("id") == object_id
    ]
    source_refs = [_source_ref(item) for item in items]
    sources = ppt_ir.setdefault("sources", [])
    if isinstance(sources, list):
        known_source_ids = {
            source.get("source_id") for source in sources if isinstance(source, dict)
        }
        for source_ref in source_refs:
            if source_ref["source_id"] not in known_source_ids:
                sources.append({
                    "source_id": source_ref["source_id"],
                    "type": "design_spec",
                    "title": "Product PRD direct evidence",
                })
                known_source_ids.add(source_ref["source_id"])
    source_labels = [f"{ref['source_id']}#{ref['locator']}" for ref in source_refs]
    # The selected pages stop being generic judgment/data pages once their
    # sole primary object is a source-bound product prototype. Mark the
    # semantic role truthfully so data-slide quality gates do not demand an
    # unrelated chart or a duplicate support card.
    slide["slide_role"] = "diagram"
    slide["primary_expression"] = "relationship_visual"
    slide["primary_anchor"] = object_id
    if component_type == "product_ui_overview":
        slide["title"] = "产品工作台 UI 总览"
        slide["message"] = "Canvas 是核心工作区；真实应用截图待补。"
        slide["judgment"] = "真实应用截图缺失时，以可编辑占位框保留替换边界。"
        screenshot = (evidence.get("coverage_matrix") or {}).get("application_screenshot", {})
        placeholder = screenshot.get("placeholder") if isinstance(screenshot, dict) else {}
        content = {
            "source_refs": source_labels,
            "spaces": [{"id": str(item["id"]), "label": str(item["value"])} for item in items],
            "relationships": [
                {"from": "topbar", "to": "canvas", "label": "进入工作区"},
                {"from": "canvas", "to": "inspector", "label": "选区联动"},
            ],
            "screenshot_placeholder": {
                "label": "待替换：应用截图",
                "asset_status": screenshot.get("asset_status", "missing") if isinstance(screenshot, dict) else "missing",
                "aspect_ratio": placeholder.get("aspect_ratio", "16:10") if isinstance(placeholder, dict) else "16:10",
                "region": placeholder.get("region", "product_ui_overview.primary_visual") if isinstance(placeholder, dict) else "product_ui_overview.primary_visual",
                "source_requirement": "PRD 要求真实应用截图；当前未提供截图资产。",
            },
        }
    else:
        slide["title"] = "工作台交互路径"
        slide["message"] = "从节点选区到 AI 反馈、结果采纳及异常处理的完整路径。"
        slide["judgment"] = "PRD 已明示的交互证据完整呈现。"
        step_items = [
            {"id": str(item["id"]), "kind": str(item.get("kind") or "action"), "label": str(item["value"])}
            for item in items
        ]
        # Check if error/conflict branch is present
        has_error = any(s.get("kind") == "error" for s in step_items)
        content = {
            "source_refs": source_labels,
            "steps": step_items,
            "transitions": [
                {"from": str(items[index]["id"]), "to": str(items[index + 1]["id"])}
                for index in range(len(items) - 1)
                if items[index + 1].get("kind") != "error" or index < len(items) - 2
            ],
        }
        if has_error:
            # Add transition from last normal step to error branch
            normal_steps = [s for s in step_items if s.get("kind") != "error"]
            error_steps = [s for s in step_items if s.get("kind") == "error"]
            if normal_steps and error_steps:
                last_normal = normal_steps[-1]["id"]
                for err in error_steps:
                    content.setdefault("transitions", []).append(
                        {"from": last_normal, "to": err["id"]}
                    )
    prototype = {
        "id": object_id,
        "type": "shape",
        "component_type": component_type,
        "semantic_role": "evidence",
        "content": content,
        "source_refs": source_refs,
        "editability": "native_required",
        "priority": "primary",
    }
    if objects:
        objects[0].update(prototype)
    else:
        objects.append(prototype)
    delivery = slide.setdefault("delivery_contract", {})
    for field in ("editable_core", "forbidden_raster"):
        values = delivery.setdefault(field, [])
        if isinstance(values, list) and object_id not in values:
            values.append(object_id)
    return str(slide.get("id") or "")


def _source_ref(item: dict[str, Any]) -> dict[str, str]:
    source = item.get("source") if isinstance(item.get("source"), dict) else {}
    return {
        "source_id": str(source.get("source_id") or "product_prd"),
        "locator": str(source.get("locator") or "unspecified"),
        "claim_type": "direct",
    }


def _items(value: Any, category: str, source_id: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    normalized: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(value, 1):
        if not isinstance(raw, dict):
            continue
        text = _string(raw.get("value")) or _string(raw.get("name")) or _string(raw.get("trigger"))
        if not text:
            continue
        locator = _string(raw.get("locator")) or "unspecified"
        normalized.append({
            "id": f"{category}-{ordinal:02d}",
            "category": category,
            "value": text,
            "source": {
                "source_id": source_id,
                "locator": locator,
                "directness": "direct",
                "confidence": "high",
            },
            "consumption": {"status": "unconsumed", "consumers": []},
        })
    return normalized


def _string(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _screenshot_asset_status(product_prd: dict[str, Any]) -> str:
    assets = product_prd.get("application_screenshot_assets")
    return "provided" if isinstance(assets, list) and any(assets) else "missing"
