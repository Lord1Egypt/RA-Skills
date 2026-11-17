"""Plan reviewed template components for a complete manuscript.

The planner joins evidence-bound content with a confirmed storyboard, routes
only explicit layout patterns, and reports every unsupported page. It never
forces a page into an unrelated component merely to increase coverage.
"""
from __future__ import annotations

from copy import deepcopy

from .component_atlas import resolve_component_binding, select_component
from .content_integrity_gate import evaluate_template_content_integrity
from .deck_diversity import evaluate_family_diversity
from .topology import infer_topology


ROUTES = {
    "three-keyword cover": ("cover keywords", "icon_card_grid"),
    "three conclusion cards": ("icon capability cards", "icon_card_grid"),
    "two-sided contrast": ("experimentation scale contrast", "two_sided_contrast"),
    "four-stage timeline": ("maturity journey", "timeline"),
    "process comparison": ("phased rollout", "timeline"),
    "multi-node comparison": ("icon capability cards", "icon_card_grid"),
    "chapter insight": ("chapter insight", "dual_panel"),
    "cycle relationship": ("closed-loop adoption relationship", "cycle_pair"),
    "dual metric": ("industry adoption contrast", "dual_panel"),
    "large-small comparison": ("capability cards", "card_grid"),
    "native chart dashboard": ("research impact evidence", "chart_dashboard"),
    "parallel function panels": ("capability cards", "card_grid"),
    "funnel conclusion": ("prioritization", "funnel"),
    "objective comparison": ("capability cards", "card_grid"),
    "progression": ("workflow redesign progression", "two_stage_progression"),
    "parallel comparison": ("capability cards", "card_grid"),
    "parallel leadership evidence": ("capability cards", "card_grid"),
    "multi-node practice map": ("icon capability cards", "icon_card_grid"),
    "workflow capability map": ("capability stack", "pyramid"),
    "layered workforce view": ("hierarchy", "pyramid"),
    "three-way comparison": ("icon capability cards", "icon_card_grid"),
    "outcome cards": ("capability cards", "card_grid"),
    "signal-uncertainty-action": ("capability cards", "card_grid"),
    "risk and mitigation": ("capability cards", "card_grid"),
    "pyramid": ("hierarchy", "pyramid"),
    "method relationship map": ("capability cards", "card_grid"),
    "funnel priorities": ("prioritization", "funnel"),
    "capability radar": ("management action dimensions", "icon_card_grid"),
    "closing statement": ("closing source note", "statement_card"),
}


# Content bindings may make these information structures explicit.  This is
# deliberately narrower than ``ROUTES``: statement pages still use their
# reviewed page archetype during migration, while relational/data structures
# must not be silently flattened into generic cards.
TOPOLOGY_ROUTES = {
    "comparison": ("experimentation scale contrast", "two_sided_contrast"),
    "sequence": ("maturity journey", "timeline"),
    "causal": ("closed-loop adoption relationship", "cycle_pair"),
    "hierarchy": ("hierarchy", "pyramid"),
    "dashboard": ("research impact evidence", "chart_dashboard"),
}


PLACEMENTS = {
    "funnel": {"x": 0.12, "y": 0.1, "w": 0.76, "h": 0.82},
    "pyramid": {"x": 0.12, "y": 0.1, "w": 0.76, "h": 0.82},
    "timeline": {"x": 0.05, "y": 0.08, "w": 0.9, "h": 0.84},
    "card_grid": {"x": 0.08, "y": 0.12, "w": 0.84, "h": 0.76},
    "icon_card_grid": {"x": 0.07, "y": 0.1, "w": 0.86, "h": 0.8},
    "dual_panel": {"x": 0.08, "y": 0.25, "w": 0.84, "h": 0.55},
    "statement_card": {"x": 0.28, "y": 0.24, "w": 0.44, "h": 0.54},
    "two_sided_contrast": {"x": 0.04, "y": 0.18, "w": 0.92, "h": 0.7},
    "cycle_pair": {"x": 0.16, "y": 0.16, "w": 0.68, "h": 0.7},
    "two_stage_progression": {"x": 0.06, "y": 0.18, "w": 0.88, "h": 0.68},
    "chart_dashboard": {"x": 0.0, "y": 0.0, "w": 1.0, "h": 1.0},
}


def _unsupported(
    *,
    output_page_index: int,
    purpose: str,
    layout_pattern: str,
    reason_code: str,
    reason: str,
) -> dict:
    return {
        "output_page_index": output_page_index,
        "purpose": purpose,
        "layout_pattern": layout_pattern,
        "reason_code": reason_code,
        "reason": reason,
    }


def _item_text(item: object, *, purpose: str, index: int) -> tuple[str, dict]:
    if isinstance(item, str) and item.strip():
        return item.strip(), {}
    if isinstance(item, dict):
        text = item.get("text") or item.get("title")
        if isinstance(text, str) and text.strip():
            return text.strip(), item
    raise ValueError(f"content binding {purpose!r} item {index} requires text")


def _binding_name(purpose: str, field: str, index: int) -> str:
    block = {
        "title": "component_items",
        "detail": "component_items",
        "badge": "component_badges",
        "metric_label": "component_metric_labels",
        "metric_value": "component_metric_values",
    }.get(field, f"component_{field}")
    suffix = "detail" if field == "detail" else "item"
    return f"bind:block:{purpose}:{block}:{suffix}:{index}"


def _page_items(content_page: dict, layout_pattern: str) -> list | None:
    items = content_page.get("items")
    if isinstance(items, list) and items:
        return items
    subtitle = content_page.get("subtitle")
    if layout_pattern == "closing statement" and isinstance(subtitle, str) and subtitle.strip():
        return [{"title": subtitle.strip()}]
    return None


def _metric_card_placements(count: int) -> list[dict]:
    if count < 2 or count > 5:
        raise ValueError("metric comparisons require between two and five items")
    if count <= 4:
        gap = 0.02
        width = (0.92 - gap * (count - 1)) / count
        return [
            {"x": round(0.04 + index * (width + gap), 4), "y": 0.18, "w": round(width, 4), "h": 0.66}
            for index in range(count)
        ]
    return [
        {"x": 0.04, "y": 0.16, "w": 0.29, "h": 0.31},
        {"x": 0.355, "y": 0.16, "w": 0.29, "h": 0.31},
        {"x": 0.67, "y": 0.16, "w": 0.29, "h": 0.31},
        {"x": 0.195, "y": 0.53, "w": 0.29, "h": 0.31},
        {"x": 0.515, "y": 0.53, "w": 0.29, "h": 0.31},
    ]


def _metric_card_components(content_page: dict, purpose: str) -> list[dict] | None:
    metrics = content_page.get("metric_comparisons")
    if metrics is None:
        return None
    if not isinstance(metrics, list):
        raise ValueError("metric_comparisons must be a list")
    placements = _metric_card_placements(len(metrics))
    components: list[dict] = []
    for index, metric in enumerate(metrics):
        if not isinstance(metric, dict):
            raise ValueError(f"metric comparison {index} must be an object")
        title, metric_text = metric.get("title"), metric.get("metric")
        categories, values = metric.get("categories"), metric.get("values")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"metric comparison {index} requires a title")
        if not isinstance(metric_text, str) or not metric_text.strip():
            raise ValueError(f"metric comparison {index} requires display text")
        if (
            not isinstance(categories, list)
            or len(categories) < 2
            or any(not isinstance(item, str) or not item.strip() for item in categories)
        ):
            raise ValueError(f"metric comparison {index} requires named categories")
        if (
            not isinstance(values, list)
            or len(values) != len(categories)
            or any(isinstance(item, bool) or not isinstance(item, (int, float)) for item in values)
        ):
            raise ValueError(f"metric comparison {index} values must match categories")
        metadata = {
            **({"source_ref": deepcopy(metric["source_ref"])}
               if isinstance(metric.get("source_ref"), dict) else {}),
            **({"source_refs": deepcopy(metric["source_refs"])}
               if isinstance(metric.get("source_refs"), list) else {}),
            **({"evidence_id": metric["evidence_id"]}
               if isinstance(metric.get("evidence_id"), str) else {}),
        }
        components.append({
            "semantic_use": "single KPI comparison",
            "family": "kpi_chart_card",
            "element_count": 1,
            "required_slots": ["chart", "title", "metric"],
            "chart": {
                "id": f"metric_{index + 1}",
                "binding_name": f"bind:chart:{purpose}:metric_{index + 1}",
                "data": {
                    "categories": [item.strip() for item in categories],
                    "series": [{
                        "name": metric.get("series_name", "Share"),
                        "values": values,
                    }],
                },
            },
            "text_bindings": [{
                "field": "title",
                "binding_name": f"bind:block:{purpose}:metric_titles:item:{index}",
                "text": title.strip(),
                **metadata,
            }, {
                "field": "metric",
                "binding_name": f"bind:block:{purpose}:metric_values:item:{index}",
                "text": metric_text.strip(),
                **metadata,
            }],
            "placement": placements[index],
        })
    return components


def _label_text(
    *,
    field: str,
    item_text: str,
    item_data: dict,
    index: int,
    fields: set[str],
) -> str:
    labels = item_data.get("labels") if isinstance(item_data.get("labels"), dict) else {}
    explicit = labels.get(field, item_data.get(field))
    if field == "title" and fields == {"title"}:
        title = explicit if isinstance(explicit, str) and explicit.strip() else item_text
        if item_data.get("compact_label") is True:
            return title.strip()
        detail = labels.get("detail", item_data.get("detail"))
        if isinstance(detail, str) and detail.strip() and detail.strip() not in title:
            return f"{title.strip()}\n{detail.strip()}"
        return title.strip()
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    if field == "detail":
        return item_text
    if field == "title" and fields == {"title"}:
        return item_text
    raise ValueError(
        f"content item {index} requires explicit label field {field!r}"
    )


def _elements(*, purpose: str, items: list, resolved: dict) -> list[dict]:
    normalized = [
        _item_text(item, purpose=purpose, index=index)
        for index, item in enumerate(items)
    ]
    if resolved.get("binding_schema_version") != "2.0.0":
        return [{
            "text": text,
            "value": (
                data.get("value")
                if isinstance(data.get("value"), (int, float))
                and not isinstance(data.get("value"), bool)
                else len(items) - index
            ),
            "binding_name": f"bind:block:{purpose}:component_items:item:{index}",
            **({"source_ref": deepcopy(data["source_ref"])}
               if isinstance(data.get("source_ref"), dict) else {}),
            **({"source_refs": deepcopy(data["source_refs"])}
               if isinstance(data.get("source_refs"), list) else {}),
            **({"evidence_id": data["evidence_id"]}
               if isinstance(data.get("evidence_id"), str) else {}),
        } for index, (text, data) in enumerate(normalized)]

    item_groups = resolved.get("item_groups")
    if not isinstance(item_groups, list) or not item_groups:
        raise ValueError("resolved extended component has no item_groups")
    fields = set(item_groups[0].get("label_fields", {}))
    if not fields:
        raise ValueError("resolved extended component has no label fields")
    if any(set(group.get("label_fields", {})) != fields for group in item_groups):
        raise ValueError("resolved extended component label fields do not align")
    return [{
        "value": (
            data.get("value")
            if isinstance(data.get("value"), (int, float))
            and not isinstance(data.get("value"), bool)
            else None
        ),
        "labels": {
            field: {
                "text": _label_text(
                    field=field,
                    item_text=text,
                    item_data=data,
                    index=index,
                    fields=fields,
                ),
                "binding_name": _binding_name(purpose, field, index),
                **({"source_ref": deepcopy(data["source_ref"])}
                   if isinstance(data.get("source_ref"), dict) else {}),
                **({"source_refs": deepcopy(data["source_refs"])}
                   if isinstance(data.get("source_refs"), list) else {}),
                **({"evidence_id": data["evidence_id"]}
                   if isinstance(data.get("evidence_id"), str) else {}),
            }
            for field in sorted(fields)
        },
    } for index, (text, data) in enumerate(normalized)]


def build_manuscript_component_composition(
    atlas: dict,
    content_bindings: dict,
    storyboard: dict,
    *,
    evidence_ledger: dict | None = None,
    enforce_content_integrity: bool = False,
) -> dict:
    if not isinstance(atlas, dict) or atlas.get("status") != "reviewed":
        raise ValueError("manuscript component planning requires a reviewed atlas")
    template_slide_count = atlas.get("source", {}).get("slide_count")
    if (
        isinstance(template_slide_count, bool)
        or not isinstance(template_slide_count, int)
        or template_slide_count < 1
    ):
        raise ValueError("reviewed atlas requires a positive source slide_count")
    binding_slides = content_bindings.get("slides") if isinstance(content_bindings, dict) else None
    if not isinstance(binding_slides, list) or not binding_slides:
        raise ValueError("content bindings require a non-empty slides list")
    storyboard_slides = storyboard.get("slides") if isinstance(storyboard, dict) else None
    if not isinstance(storyboard_slides, list) or not storyboard_slides:
        raise ValueError("storyboard requires a non-empty slides list")

    content_integrity = {"status": "not_enforced"}
    if enforce_content_integrity:
        if evidence_ledger is None:
            raise ValueError("CONTENT_INTEGRITY_LEDGER_REQUIRED")
        content_integrity = evaluate_template_content_integrity(
            content_bindings, evidence_ledger,
        )
        if content_integrity["status"] != "pass":
            codes = sorted({issue["code"] for issue in content_integrity["issues"]})
            raise ValueError(f"CONTENT_INTEGRITY_FAILED: {','.join(codes)}")

    by_id = {
        slide.get("id"): slide
        for slide in binding_slides
        if isinstance(slide, dict) and isinstance(slide.get("id"), str)
    }
    pages: list[dict] = []
    unsupported_pages: list[dict] = []
    for page_offset, storyboard_page in enumerate(storyboard_slides):
        output_page_index = page_offset + 1
        if not isinstance(storyboard_page, dict):
            raise ValueError(f"storyboard page {output_page_index} must be an object")
        purpose = storyboard_page.get("purpose")
        if not isinstance(purpose, str) or not purpose:
            raise ValueError(f"storyboard page {output_page_index} requires purpose")
        rationale = storyboard_page.get("layout_rationale", {})
        layout_pattern = rationale.get("layout_pattern", "") if isinstance(rationale, dict) else ""
        if not isinstance(layout_pattern, str):
            layout_pattern = ""
        content_page = by_id.get(purpose)
        if content_page is None:
            unsupported_pages.append(_unsupported(
                output_page_index=output_page_index,
                purpose=purpose,
                layout_pattern=layout_pattern,
                reason_code="missing_content_binding",
                reason=f"no content binding found for purpose {purpose!r}",
            ))
            continue
        topology = infer_topology(content_page, storyboard_page)
        try:
            metric_components = _metric_card_components(content_page, purpose)
        except ValueError as exc:
            unsupported_pages.append(_unsupported(
                output_page_index=output_page_index,
                purpose=purpose,
                layout_pattern=layout_pattern,
                reason_code="invalid_metric_comparisons",
                reason=str(exc),
            ))
            continue
        if metric_components is not None:
            pages.append({
                "output_page_index": output_page_index,
                "purpose": purpose,
                "topology": topology,
                "destination_slide_index": template_slide_count + output_page_index,
                "components": metric_components,
            })
            continue
        if topology["source"] == "content_binding":
            route = TOPOLOGY_ROUTES.get(topology["topology"])
            if route is None:
                unsupported_pages.append(_unsupported(
                    output_page_index=output_page_index,
                    purpose=purpose,
                    layout_pattern=layout_pattern,
                    reason_code="topology_route_unavailable",
                    reason=(
                        "no reviewed component route for explicit topology "
                        f"{topology['topology']!r}"
                    ),
                ))
                continue
        else:
            route = ROUTES.get(layout_pattern)
            if route is None:
                unsupported_pages.append(_unsupported(
                    output_page_index=output_page_index,
                    purpose=purpose,
                    layout_pattern=layout_pattern,
                    reason_code="no_component_route",
                    reason=f"no reviewed component route for layout pattern {layout_pattern!r}",
                ))
                continue
        semantic_use, family = route
        if family == "chart_dashboard":
            dashboard = content_page.get("dashboard")
            charts = dashboard.get("charts") if isinstance(dashboard, dict) else None
            text_bindings = dashboard.get("text_bindings") if isinstance(dashboard, dict) else None
            clear_text_names = dashboard.get("clear_text_names") if isinstance(dashboard, dict) else None
            if (
                not isinstance(charts, list)
                or not charts
                or not isinstance(text_bindings, list)
                or not isinstance(clear_text_names, list)
            ):
                unsupported_pages.append(_unsupported(
                    output_page_index=output_page_index,
                    purpose=purpose,
                    layout_pattern=layout_pattern,
                    reason_code="missing_dashboard_binding",
                    reason=f"content binding {purpose!r} requires structured dashboard data",
                ))
                continue
            requirement = {
                "semantic_use": semantic_use,
                "family": family,
                "element_count": len(charts),
                "topology": topology["topology"] if topology["source"] == "content_binding" else None,
                "required_slots": content_page.get("required_slots", []),
            }
            selection = select_component(atlas, requirement)
            if selection.get("status") != "selected":
                unsupported_pages.append(_unsupported(
                    output_page_index=output_page_index,
                    purpose=purpose,
                    layout_pattern=layout_pattern,
                    reason_code="no_component_match",
                    reason=selection.get("reason", "no reviewed dashboard satisfies the chart count"),
                ))
                continue
            pages.append({
                "output_page_index": output_page_index,
                "purpose": purpose,
                "destination_slide_index": template_slide_count + output_page_index,
                "components": [{
                    "component_id": selection["component_id"],
                    "semantic_use": semantic_use,
                    "family": family,
                    "element_count": len(charts),
                    "charts": deepcopy(charts),
                    "text_bindings": deepcopy(text_bindings),
                    "clear_text_names": deepcopy(clear_text_names),
                    "placement": deepcopy(PLACEMENTS[family]),
                }],
            })
            continue
        items = _page_items(content_page, layout_pattern)
        if not isinstance(items, list) or not items:
            unsupported_pages.append(_unsupported(
                output_page_index=output_page_index,
                purpose=purpose,
                layout_pattern=layout_pattern,
                reason_code="missing_component_items",
                reason=f"content binding {purpose!r} has no component items",
            ))
            continue

        requirement = {
            "semantic_use": semantic_use,
            "family": family,
            "element_count": len(items),
            "topology": topology["topology"] if topology["source"] == "content_binding" else None,
            "required_slots": content_page.get("required_slots", []),
        }
        selection = select_component(atlas, requirement)
        if selection.get("status") != "selected":
            unsupported_pages.append(_unsupported(
                output_page_index=output_page_index,
                purpose=purpose,
                layout_pattern=layout_pattern,
                reason_code="no_component_match",
                reason=selection.get(
                    "reason",
                    "no reviewed component satisfies semantic use and element capacity",
                ),
            ))
            continue
        try:
            resolved = resolve_component_binding(atlas, requirement)
            elements = _elements(purpose=purpose, items=items, resolved=resolved)
        except ValueError as exc:
            unsupported_pages.append(_unsupported(
                output_page_index=output_page_index,
                purpose=purpose,
                layout_pattern=layout_pattern,
                reason_code="component_binding_unavailable",
                reason=str(exc),
            ))
            continue

        pages.append({
            "output_page_index": output_page_index,
            "purpose": purpose,
            "topology": topology,
            "destination_slide_index": template_slide_count + output_page_index,
            "components": [{
                "semantic_use": semantic_use,
                "family": family,
                "elements": elements,
                "placement": deepcopy(PLACEMENTS[family]),
            }],
        })

    total_pages = len(storyboard_slides)
    planned_pages = len(pages)
    coverage_status = (
        "complete" if planned_pages == total_pages
        else "none" if planned_pages == 0
        else "partial"
    )
    diversity = evaluate_family_diversity([
        {
            "families": [
                component.get("family")
                for component in page.get("components", [])
            ],
            "archetype": by_id.get(page.get("purpose"), {}).get("archetype", "body"),
        }
        for page in pages
    ])
    if enforce_content_integrity and diversity["status"] != "pass":
        codes = sorted({issue["code"] for issue in diversity["issues"]})
        raise ValueError(f"COMPONENT_DIVERSITY_FAILED: {','.join(codes)}")
    return {
        "schema_version": "1.0.0",
        "source_page_count": total_pages,
        "template_slide_count": template_slide_count,
        "pages": pages,
        "unsupported_pages": unsupported_pages,
        "content_integrity": content_integrity,
        "family_diversity": diversity,
        "coverage": {
            "status": coverage_status,
            "total_pages": total_pages,
            "planned_pages": planned_pages,
            "unsupported_pages": len(unsupported_pages),
            "coverage_ratio": round(planned_pages / total_pages, 4),
        },
    }
