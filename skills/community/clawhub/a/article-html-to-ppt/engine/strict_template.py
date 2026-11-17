"""Fail-closed Path C entry for native reuse of a hash-locked template."""
from __future__ import annotations

import shutil
import hashlib
import posixpath
from pathlib import Path
import zipfile
import json
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from pptx import Presentation

from .authored_page import verify_authored_page
from .component_atlas import (
    resolve_chart_component_binding,
    resolve_chart_dashboard_binding,
    resolve_component_binding,
    resolve_native_group_binding,
)
from .production_request import prepare_template_context
from .presentation_subset import write_slide_subset
from .template_native import (
    bind_chart_data,
    bind_chart_shape,
    bind_template_component,
    bind_text_shape,
    fit_text_background,
    fit_text_to_container,
    bind_table_data,
    clear_text_shape,
    clone_chart_shape,
    clone_native_shape_trees,
    clone_native_shapes,
    clone_table_shape,
    mark_native_shapes_as_decorations,
    place_native_shapes,
)


ASSET_PREFIXES = ("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/theme/", "ppt/media/")


def _asset_preservation(template_pptx: Path, output_pptx: Path) -> dict:
    with zipfile.ZipFile(template_pptx) as source, zipfile.ZipFile(output_pptx) as output:
        source_names = set(source.namelist())
        output_names = set(output.namelist())
        output_assets = sorted(
            name for name in output_names if name.startswith(ASSET_PREFIXES)
        )
        changed = [
            name for name in output_assets
            if name not in source_names or source.read(name) != output.read(name)
        ]
        broken_relationships: list[dict] = []
        for relationship_part in sorted(
            name for name in output_names if name.endswith(".rels")
        ):
            root = ElementTree.fromstring(output.read(relationship_part))
            relationship_name = posixpath.basename(relationship_part)[:-5]
            owner_directory = posixpath.dirname(
                posixpath.dirname(relationship_part)
            )
            owner_part = posixpath.join(owner_directory, relationship_name)
            target_base = posixpath.dirname(owner_part)
            for relationship in root:
                if not relationship.tag.endswith("Relationship"):
                    continue
                if relationship.get("TargetMode") == "External":
                    continue
                raw_target = relationship.get("Target", "")
                if raw_target.startswith("/"):
                    target = posixpath.normpath(raw_target.lstrip("/"))
                else:
                    target = posixpath.normpath(
                        posixpath.join(target_base, raw_target)
                    )
                if target.startswith(ASSET_PREFIXES) and target not in output_names:
                    broken_relationships.append({
                        "relationship_part": relationship_part,
                        "relationship_id": relationship.get("Id"),
                        "target": target,
                    })
    return {
        "status": "pass" if not changed and not broken_relationships else "fail",
        "verified_parts": len(output_assets),
        "changed_parts": changed,
        "broken_relationships": broken_relationships,
    }


def _operation_error(message: str) -> ValueError:
    return ValueError(f"STRICT_TEMPLATE_PLAN_INVALID: {message}")


def _ensure_destination_slides(pptx_path: Path, strict_plan: dict) -> dict:
    """Append native blank canvases when a model plan extends the template.

    Component plans address delivery canvases after the template's reviewed
    source pages.  Appending with a layout already owned by the presentation
    preserves its master/theme relationship instead of fabricating a foreign
    blank deck.
    """
    operations = strict_plan.get("operations") if isinstance(strict_plan, dict) else None
    if not isinstance(operations, list) or not operations:
        raise _operation_error("operations must be a non-empty list")
    destinations = [
        operation.get("destination_slide_index")
        for operation in operations
        if isinstance(operation, dict)
    ]
    if any(
        isinstance(index, bool) or not isinstance(index, int) or index < 1
        for index in destinations
    ):
        raise _operation_error("every operation requires a positive destination slide index")
    presentation = Presentation(str(pptx_path))
    before = len(presentation.slides)
    required = max(destinations)
    if required <= before:
        return {"status": "unchanged", "before": before, "after": before, "appended": 0}
    layout_candidates = list(enumerate(presentation.slide_layouts))
    if not layout_candidates:
        raise _operation_error("template contains no slide layouts")
    layout_index, layout = min(
        layout_candidates,
        key=lambda item: (len(item[1].placeholders), -item[0]),
    )
    for _ in range(required - before):
        presentation.slides.add_slide(layout)
    presentation.save(str(pptx_path))
    return {
        "status": "expanded",
        "before": before,
        "after": required,
        "appended": required - before,
        "layout_index": layout_index,
        "layout_name": str(getattr(layout, "name", "") or ""),
    }


def _issue_signature(issue: dict) -> str:
    """Create a stable identity for a structural finding across template copies."""
    return json.dumps({
        "code": issue.get("issue_code"),
        "severity": issue.get("severity"),
        "slide_id": issue.get("slide_id"),
        "object_id": issue.get("object_id"),
        "ppt_shape_id": issue.get("ppt_shape_id"),
        "evidence": issue.get("evidence", {}),
    }, ensure_ascii=False, sort_keys=True)


def _inspection_delta(baseline: dict, candidate: dict) -> dict:
    """Fail only on structural findings introduced by declared strict edits.

    User-provided templates may already contain legitimate off-canvas objects
    or connector arrangements that a generic inspector cannot understand.
    Strict reuse must preserve—not re-litigate—those baseline findings.
    """
    baseline_signatures = {_issue_signature(issue) for issue in baseline.get("issues", [])}
    new_issues = [
        issue for issue in candidate.get("issues", [])
        if _issue_signature(issue) not in baseline_signatures
    ]
    blocking = [issue for issue in new_issues if issue.get("severity") in {"error", "fatal"}]
    return {
        "status": "failed" if blocking else "passed",
        "baseline_status": baseline.get("status"),
        "candidate_status": candidate.get("status"),
        "baseline_issue_count": len(baseline.get("issues", [])),
        "candidate_issue_count": len(candidate.get("issues", [])),
        "new_issue_count": len(new_issues),
        "new_issues": new_issues,
    }


def _resolve_component_operation(
    operation: dict,
    *,
    component_atlas: dict | None,
) -> tuple[
    dict | None,
    str,
    list[str] | None,
    list[list[str]] | None,
    list[str] | None,
    list[dict] | None,
    list[str] | None,
    list[dict],
]:
    elements = operation["elements"]
    requirement = operation.get("component_requirement")
    resolved = None
    if requirement is not None:
        if component_atlas is None:
            raise ValueError("component_requirement needs a reviewed component atlas")
        if not isinstance(requirement, dict):
            raise ValueError("component_requirement must be an object")
        if not isinstance(elements, list):
            raise ValueError("elements must be a list")
        if requirement.get("element_count") != len(elements):
            raise ValueError("component_requirement element_count must equal the number of elements")
        resolved = resolve_component_binding(component_atlas, requirement)
        if resolved.get("binding_mode") == "extended":
            return (
                resolved,
                resolved["component_type"],
                None,
                None,
                None,
                resolved["item_groups"],
                resolved["shared_names"],
                elements,
            )
        return (
            resolved,
            resolved["component_type"],
            None,
            resolved["segment_groups"],
            resolved["label_names"],
            None,
            None,
            elements,
        )
    return (
        None,
        str(operation["component_type"]),
        operation.get("segment_names"),
        operation.get("segment_groups"),
        operation["label_names"],
        None,
        None,
        elements,
    )


def _apply_operations(
    template_pptx: Path,
    output_pptx: Path,
    strict_plan: dict,
    *,
    component_atlas: dict | None = None,
    ir: dict | None = None,
) -> tuple[list[dict], set[str], set[int], set[str]]:
    operations = strict_plan.get("operations") if isinstance(strict_plan, dict) else None
    if not isinstance(operations, list) or not operations:
        raise _operation_error("operations must be a non-empty list")
    applied: list[dict] = []
    if not isinstance(ir, dict):
        ir = {}
    slide_ids: set[str] = set()
    physical_slide_indices: set[int] = set()
    binding_names: set[str] = set()
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise _operation_error(f"operation {index} must be an object")
        kind = operation.get("kind")
        try:
            destination_slide = int(operation["destination_slide_index"])
        except (KeyError, TypeError, ValueError) as exc:
            raise _operation_error(f"operation {index} is missing a valid destination slide index") from exc
        if kind in {
            "component_clone", "chart_component_clone", "chart_dashboard_clone",
            "native_group_component_clone", "model_authored_native_component",
        } and operation.get("source_slide_index") is None:
            source_slide = None
        else:
            try:
                source_slide = int(operation["source_slide_index"])
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(f"operation {index} is missing a valid source slide index") from exc
        binding_name = operation.get("binding_name")
        if kind not in {
            "component_bind_existing", "component_clone", "native_group_clone",
            "chart_component_clone", "chart_dashboard_bind_existing", "chart_dashboard_clone",
            "native_group_component_clone", "model_authored_native_component",
        }:
            if not isinstance(binding_name, str) or not binding_name:
                raise _operation_error(f"operation {index} requires binding_name")
        if kind == "model_authored_native_component":
            try:
                from .model_template_component_runtime import author_model_template_component

                copied = author_model_template_component(
                    output_pptx,
                    template_pptx=template_pptx,
                    script_path=operation["author_script"],
                    slide_index=destination_slide,
                    slide_id=operation["slide_id"],
                    component_id=operation["component_id"],
                    placement=operation["placement"],
                    ir=ir,
                    required_binding_names=operation.get("required_binding_names"),
                    asset_bindings=operation.get("asset_bindings"),
                    author_context=operation.get("author_context"),
                    component_atlas=component_atlas,
                )
                binding = {
                    "binding_names": copied["binding_names"],
                    "slide_index": destination_slide,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"model_authored_native_component operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "chart_component_clone":
            if component_atlas is None:
                raise _operation_error(
                    f"chart_component_clone operation {index} requires a reviewed component atlas"
                )
            try:
                requirement = operation.get("component_requirement")
                if not isinstance(requirement, dict):
                    raise ValueError("component_requirement must be an object")
                resolved_chart = resolve_chart_component_binding(component_atlas, requirement)
                atlas_source_slide = int(resolved_chart["source_slide_index"])
                if source_slide is not None and source_slide != atlas_source_slide:
                    raise ValueError("declared source slide does not match the selected component")
                source_slide = atlas_source_slide
                chart_spec = operation.get("chart")
                if not isinstance(chart_spec, dict):
                    raise ValueError("chart component requires chart data and binding")
                data = chart_spec.get("data")
                declared_chart_name = chart_spec.get("binding_name")
                if not isinstance(data, dict) or not isinstance(declared_chart_name, str):
                    raise ValueError("chart component requires valid chart data and binding_name")

                chart_source_name = resolved_chart["chart_names"][0]
                non_chart_names = [
                    name for names in resolved_chart["label_fields"].values() for name in names
                ] + list(resolved_chart["decoration_names"])
                cloned_component = clone_native_shape_trees(
                    output_pptx,
                    source_slide_index=source_slide,
                    destination_slide_index=destination_slide,
                    shape_names=list(dict.fromkeys([chart_source_name, *non_chart_names])),
                )
                name_map = cloned_component["shape_names"]
                place_native_shapes(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=cloned_component["top_level_shape_names"],
                    placement=operation.get("placement"),
                )
                decoration_result = mark_native_shapes_as_decorations(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=[
                        name_map[name] for name in resolved_chart["decoration_names"]
                    ],
                    decoration_prefix=(
                        f"decoration:component:{resolved_chart['component_type']}:"
                        f"{resolved_chart['component_id']}:shared"
                    ),
                )
                chart_result = bind_chart_data(
                    output_pptx,
                    slide_index=destination_slide,
                    chart_name=name_map[chart_source_name],
                    binding_name=declared_chart_name,
                    categories=data["categories"],
                    series=data["series"],
                )

                text_bindings = operation.get("text_bindings", [])
                if not isinstance(text_bindings, list):
                    raise ValueError("text_bindings must be a list")
                by_field: dict[str, list[dict]] = {}
                for text_binding in text_bindings:
                    if not isinstance(text_binding, dict):
                        raise ValueError("chart component text bindings must be objects")
                    by_field.setdefault(text_binding.get("field"), []).append(text_binding)
                if set(by_field) != set(resolved_chart["label_fields"]):
                    raise ValueError("chart component must bind every reviewed semantic label field")
                declared = [declared_chart_name]
                bound_by_field: dict[str, list[str]] = {}
                for field, source_names in resolved_chart["label_fields"].items():
                    bindings = by_field[field]
                    if len(bindings) != len(source_names):
                        raise ValueError(f"chart component field {field!r} binding count does not match review")
                    for source_name, text_binding in zip(source_names, bindings):
                        binding_name = text_binding.get("binding_name")
                        text = text_binding.get("text")
                        if not isinstance(binding_name, str) or binding_name in declared:
                            raise ValueError("chart component binding names must be non-empty and distinct")
                        if not isinstance(text, str) or not text:
                            raise ValueError("chart component text bindings require non-empty text")
                        bind_text_shape(
                            output_pptx,
                            slide_index=destination_slide,
                            shape_name=name_map[source_name],
                            binding_name=binding_name,
                            text=text,
                        )
                        bound_by_field.setdefault(field, []).append(binding_name)
                        declared.append(binding_name)
                for responsive in resolved_chart.get("responsive_text_backgrounds", []):
                    field = responsive.get("field")
                    bound_names = bound_by_field.get(field, [])
                    if len(bound_names) != 1:
                        raise ValueError("responsive text background requires one bound label field")
                    background_source = responsive.get("background_shape_name")
                    container_source = responsive.get("container_shape_name")
                    if background_source not in name_map or container_source not in name_map:
                        raise ValueError("responsive text background references uncloned source shapes")
                    decoration_name_map = decoration_result.get("shape_names", {})
                    fit_text_background(
                        output_pptx,
                        slide_index=destination_slide,
                        text_shape_name=bound_names[0],
                        background_shape_name=decoration_name_map.get(
                            name_map[background_source], name_map[background_source]
                        ),
                        container_shape_name=decoration_name_map.get(
                            name_map[container_source], name_map[container_source]
                        ),
                        padding_x_pt=float(responsive.get("padding_x_pt", 8.0)),
                        padding_y_pt=float(responsive.get("padding_y_pt", 3.0)),
                    )
                for responsive in resolved_chart.get("responsive_text_fields", []):
                    field = responsive.get("field")
                    bound_names = bound_by_field.get(field, [])
                    if len(bound_names) != 1:
                        raise ValueError("responsive text field requires one bound label field")
                    container_source = responsive.get("container_shape_name")
                    if container_source not in name_map:
                        raise ValueError("responsive text field references an uncloned source shape")
                    decoration_name_map = decoration_result.get("shape_names", {})
                    fit_text_to_container(
                        output_pptx,
                        slide_index=destination_slide,
                        text_shape_name=bound_names[0],
                        container_shape_name=decoration_name_map.get(
                            name_map[container_source], name_map[container_source]
                        ),
                        maximum_width_ratio=float(responsive.get("maximum_width_ratio", 0.5)),
                    )
                binding = {"binding_names": declared, "slide_index": destination_slide}
                copied = {
                    "component_id": resolved_chart["component_id"],
                    "component_type": resolved_chart["component_type"],
                    "source_slide_index": source_slide,
                    "destination_slide_index": destination_slide,
                    "chart_result": chart_result,
                    "decoration_names": list(decoration_result["shape_names"].values()),
                    "cloned_top_level_shape_names": cloned_component["top_level_shape_names"],
                    "copied_parts": cloned_component["copied_parts"],
                    "cloned_template_chart_component": True,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"chart_component_clone operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "chart_dashboard_clone":
            if component_atlas is None:
                raise _operation_error(
                    f"chart_dashboard_clone operation {index} requires a reviewed component atlas"
                )
            try:
                requirement = operation.get("component_requirement")
                if not isinstance(requirement, dict):
                    raise ValueError("component_requirement must be an object")
                resolved_dashboard = resolve_chart_dashboard_binding(component_atlas, requirement)
                atlas_source_slide = int(resolved_dashboard["source_slide_index"])
                if source_slide is not None and source_slide != atlas_source_slide:
                    raise ValueError("declared source slide does not match the selected dashboard")
                source_slide = atlas_source_slide
                charts = operation.get("charts")
                if not isinstance(charts, list) or len(charts) != len(resolved_dashboard["chart_names"]):
                    raise ValueError("charts must align exactly with the reviewed dashboard chart group")

                source_names = list(dict.fromkeys(
                    resolved_dashboard["chart_names"]
                    + resolved_dashboard["text_names"]
                    + resolved_dashboard["decoration_names"]
                ))
                cloned_dashboard = clone_native_shape_trees(
                    output_pptx,
                    source_slide_index=source_slide,
                    destination_slide_index=destination_slide,
                    shape_names=source_names,
                )
                all_name_map = cloned_dashboard["shape_names"]
                chart_name_map = {
                    name: all_name_map[name] for name in resolved_dashboard["chart_names"]
                }
                native_name_map = {
                    name: all_name_map[name]
                    for name in resolved_dashboard["text_names"] + resolved_dashboard["decoration_names"]
                }
                placement = None
                if operation.get("placement") is not None:
                    placement = place_native_shapes(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_names=cloned_dashboard["top_level_shape_names"],
                        placement=operation["placement"],
                    )
                decoration_result = mark_native_shapes_as_decorations(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=[
                        native_name_map[name] for name in resolved_dashboard["decoration_names"]
                    ],
                    decoration_prefix=(
                        "decoration:component:chart_dashboard:"
                        f"{resolved_dashboard['component_id']}:shared"
                    ),
                )

                declared: list[str] = []
                chart_results: list[dict] = []
                for source_chart_name, chart_spec in zip(resolved_dashboard["chart_names"], charts):
                    if not isinstance(chart_spec, dict):
                        raise ValueError("dashboard chart entries must be objects")
                    data = chart_spec.get("data")
                    declared_name = chart_spec.get("binding_name")
                    if not isinstance(data, dict):
                        raise ValueError("dashboard chart entries require data")
                    if not isinstance(declared_name, str) or declared_name in declared:
                        raise ValueError("dashboard chart binding names must be non-empty and distinct")
                    chart_results.append(bind_chart_data(
                        output_pptx,
                        slide_index=destination_slide,
                        chart_name=chart_name_map[source_chart_name],
                        binding_name=declared_name,
                        categories=data["categories"],
                        series=data["series"],
                    ))
                    declared.append(declared_name)

                text_bindings = operation.get("text_bindings", [])
                clear_text_names = operation.get("clear_text_names", [])
                if not isinstance(text_bindings, list) or not isinstance(clear_text_names, list):
                    raise ValueError("text_bindings and clear_text_names must be lists")
                bound_text_names: list[str] = []
                for text_binding in text_bindings:
                    if not isinstance(text_binding, dict):
                        raise ValueError("dashboard text binding entries must be objects")
                    source_name = text_binding.get("shape_name")
                    if source_name not in resolved_dashboard["text_names"]:
                        raise ValueError(
                            f"text binding references unreviewed dashboard shape {source_name!r}"
                        )
                    declared_name = text_binding.get("binding_name")
                    value = text_binding.get("text")
                    if not isinstance(declared_name, str) or declared_name in declared:
                        raise ValueError("dashboard binding names must be non-empty and distinct")
                    if not isinstance(value, str) or not value:
                        raise ValueError("dashboard text bindings require non-empty text")
                    bind_text_shape(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_name=native_name_map[source_name],
                        binding_name=declared_name,
                        text=value,
                    )
                    bound_text_names.append(source_name)
                    declared.append(declared_name)
                if any(not isinstance(name, str) for name in clear_text_names):
                    raise ValueError("clear_text_names must contain strings")
                reviewed_texts = set(resolved_dashboard["text_names"])
                handled_texts = set(bound_text_names) | set(clear_text_names)
                if handled_texts != reviewed_texts or len(handled_texts) != len(bound_text_names) + len(clear_text_names):
                    raise ValueError(
                        "every reviewed dashboard text frame must be handled exactly once by binding or clearing"
                    )
                cleared: list[str] = []
                for clear_index, source_name in enumerate(clear_text_names):
                    decoration_name = (
                        f"decoration:cleared-text:{resolved_dashboard['component_id']}:{clear_index}"
                    )
                    clear_text_shape(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_name=native_name_map[source_name],
                        decoration_name=decoration_name,
                    )
                    cleared.append(decoration_name)
                binding = {"binding_names": declared, "slide_index": destination_slide}
                copied = {
                    "component_id": resolved_dashboard["component_id"],
                    "component_type": "chart_dashboard",
                    "source_slide_index": source_slide,
                    "destination_slide_index": destination_slide,
                    "chart_names": [chart_name_map[name] for name in resolved_dashboard["chart_names"]],
                    "cleared_text_names": cleared,
                    "decoration_names": list(decoration_result["shape_names"].values()),
                    "placement": placement,
                    "cloned_template_dashboard": True,
                    "cloned_top_level_shape_names": cloned_dashboard["top_level_shape_names"],
                    "copied_parts": cloned_dashboard["copied_parts"],
                    "chart_results": chart_results,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"chart_dashboard_clone operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "chart_dashboard_bind_existing":
            if source_slide != destination_slide:
                raise _operation_error(
                    f"chart_dashboard_bind_existing operation {index} must use the same source and destination slide"
                )
            if component_atlas is None:
                raise _operation_error(
                    f"chart_dashboard_bind_existing operation {index} requires a reviewed component atlas"
                )
            try:
                requirement = operation.get("component_requirement")
                if not isinstance(requirement, dict):
                    raise ValueError("component_requirement must be an object")
                resolved_dashboard = resolve_chart_dashboard_binding(component_atlas, requirement)
                if int(resolved_dashboard["source_slide_index"]) != source_slide:
                    raise ValueError("selected dashboard source slide does not match source_slide_index")
                charts = operation.get("charts")
                if not isinstance(charts, list) or len(charts) != len(resolved_dashboard["chart_names"]):
                    raise ValueError("charts must align exactly with the reviewed dashboard chart group")
                decoration_result = mark_native_shapes_as_decorations(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=resolved_dashboard["decoration_names"],
                    decoration_prefix=(
                        "decoration:component:chart_dashboard:"
                        f"{resolved_dashboard['component_id']}:shared"
                    ),
                )
                declared: list[str] = []
                chart_results: list[dict] = []
                for chart_name, chart_spec in zip(resolved_dashboard["chart_names"], charts):
                    if not isinstance(chart_spec, dict):
                        raise ValueError("dashboard chart entries must be objects")
                    data = chart_spec.get("data")
                    if not isinstance(data, dict):
                        raise ValueError("dashboard chart entries require data")
                    declared_name = chart_spec.get("binding_name")
                    if not isinstance(declared_name, str) or declared_name in declared:
                        raise ValueError("dashboard chart binding names must be non-empty and distinct")
                    chart_results.append(bind_chart_data(
                        output_pptx,
                        slide_index=destination_slide,
                        chart_name=chart_name,
                        binding_name=declared_name,
                        categories=data["categories"],
                        series=data["series"],
                    ))
                    declared.append(declared_name)

                text_bindings = operation.get("text_bindings", [])
                clear_text_names = operation.get("clear_text_names", [])
                if not isinstance(text_bindings, list) or not isinstance(clear_text_names, list):
                    raise ValueError("text_bindings and clear_text_names must be lists")
                bound_text_names: list[str] = []
                for text_binding in text_bindings:
                    if not isinstance(text_binding, dict):
                        raise ValueError("dashboard text binding entries must be objects")
                    shape_name = text_binding.get("shape_name")
                    if shape_name not in resolved_dashboard["text_names"]:
                        raise ValueError(f"text binding references unreviewed dashboard shape {shape_name!r}")
                    declared_name = text_binding.get("binding_name")
                    text = text_binding.get("text")
                    if not isinstance(declared_name, str) or declared_name in declared:
                        raise ValueError("dashboard binding names must be non-empty and distinct")
                    if not isinstance(text, str) or not text:
                        raise ValueError("dashboard text bindings require non-empty text")
                    bind_text_shape(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_name=shape_name,
                        binding_name=declared_name,
                        text=text,
                    )
                    bound_text_names.append(shape_name)
                    declared.append(declared_name)
                if any(not isinstance(name, str) for name in clear_text_names):
                    raise ValueError("clear_text_names must contain strings")
                reviewed_texts = set(resolved_dashboard["text_names"])
                handled_texts = set(bound_text_names) | set(clear_text_names)
                if handled_texts != reviewed_texts or len(handled_texts) != len(bound_text_names) + len(clear_text_names):
                    raise ValueError(
                        "every reviewed dashboard text frame must be handled exactly once by binding or clearing"
                    )
                cleared: list[str] = []
                for clear_index, shape_name in enumerate(clear_text_names):
                    decoration_name = (
                        f"decoration:cleared-text:{resolved_dashboard['component_id']}:{clear_index}"
                    )
                    clear_text_shape(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_name=shape_name,
                        decoration_name=decoration_name,
                    )
                    cleared.append(decoration_name)
                binding = {"binding_names": declared, "slide_index": destination_slide}
                copied = {
                    "component_id": resolved_dashboard["component_id"],
                    "component_type": "chart_dashboard",
                    "source_slide_index": source_slide,
                    "destination_slide_index": destination_slide,
                    "chart_names": resolved_dashboard["chart_names"],
                    "cleared_text_names": cleared,
                    "decoration_names": list(decoration_result["shape_names"].values()),
                    "existing_template_dashboard": True,
                    "chart_results": chart_results,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"chart_dashboard_bind_existing operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "chart_clone":
            copied = clone_chart_shape(
                template_pptx, output_pptx,
                source_slide_index=source_slide, destination_slide_index=destination_slide,
                chart_name=operation.get("chart_name"),
            )
            binding = bind_chart_shape(
                output_pptx, slide_index=destination_slide,
                chart_name=copied["chart_name"], binding_name=binding_name,
            )
        elif kind == "chart_bind_existing":
            if source_slide != destination_slide:
                raise _operation_error(
                    f"chart_bind_existing operation {index} must use the same source and destination slide"
                )
            data = operation.get("data")
            if not isinstance(data, dict):
                raise _operation_error(f"chart_bind_existing operation {index} requires data")
            try:
                binding = bind_chart_data(
                    output_pptx, slide_index=destination_slide,
                    chart_name=str(operation["chart_name"]), binding_name=binding_name,
                    categories=data["categories"], series=data["series"],
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"chart_bind_existing operation {index} has invalid chart data: {exc}"
                ) from exc
            copied = {
                "chart_name": operation["chart_name"],
                "source_slide_index": source_slide,
                "destination_slide_index": destination_slide,
                "existing_template_chart": True,
            }
        elif kind == "text_bind_existing":
            if source_slide != destination_slide:
                raise _operation_error(
                    f"text_bind_existing operation {index} must use the same source and destination slide"
                )
            if not isinstance(operation.get("text"), str):
                raise _operation_error(f"text_bind_existing operation {index} requires text")
            try:
                binding = bind_text_shape(
                    output_pptx, slide_index=destination_slide,
                    shape_name=str(operation["shape_name"]), binding_name=binding_name,
                    text=operation["text"],
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"text_bind_existing operation {index} is invalid: {exc}"
                ) from exc
            copied = {
                "shape_name": operation["shape_name"],
                "source_slide_index": source_slide,
                "destination_slide_index": destination_slide,
                "existing_template_text": True,
            }
        elif kind == "native_group_component_clone":
            if component_atlas is None:
                raise _operation_error(
                    f"native_group_component_clone operation {index} requires a reviewed component atlas"
                )
            try:
                requirement = operation.get("component_requirement")
                if not isinstance(requirement, dict):
                    raise ValueError("component_requirement must be an object")
                resolved_group = resolve_native_group_binding(component_atlas, requirement)
                atlas_source_slide = int(resolved_group["source_slide_index"])
                if source_slide is not None and source_slide != atlas_source_slide:
                    raise ValueError("declared source slide does not match the selected native group")
                source_slide = atlas_source_slide
                source_names = list(dict.fromkeys(
                    [
                        name
                        for names in resolved_group["label_fields"].values()
                        for name in names
                    ]
                    + resolved_group["decoration_names"]
                ))
                cloned_group = clone_native_shape_trees(
                    output_pptx,
                    source_slide_index=source_slide,
                    destination_slide_index=destination_slide,
                    shape_names=source_names,
                )
                name_map = cloned_group["shape_names"]
                placement = place_native_shapes(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=cloned_group["top_level_shape_names"],
                    placement=operation.get("placement"),
                )
                decoration_result = mark_native_shapes_as_decorations(
                    output_pptx,
                    slide_index=destination_slide,
                    shape_names=[
                        name_map[name] for name in resolved_group["decoration_names"]
                    ],
                    decoration_prefix=(
                        f"decoration:component:{resolved_group['component_type']}:"
                        f"{resolved_group['component_id']}:shared"
                    ),
                )
                text_bindings = operation.get("text_bindings")
                if not isinstance(text_bindings, list) or not text_bindings:
                    raise ValueError("native group component requires text_bindings")
                by_field: dict[str, list[dict]] = {}
                for text_binding in text_bindings:
                    if not isinstance(text_binding, dict):
                        raise ValueError("native group text bindings must be objects")
                    by_field.setdefault(text_binding.get("field"), []).append(text_binding)
                if set(by_field) != set(resolved_group["label_fields"]):
                    raise ValueError("native group component must bind every reviewed semantic label field")
                declared: list[str] = []
                for field, source_names in resolved_group["label_fields"].items():
                    bindings = by_field[field]
                    if len(bindings) != len(source_names):
                        raise ValueError(
                            f"native group field {field!r} binding count does not match review"
                        )
                    for source_name, text_binding in zip(source_names, bindings):
                        binding_name = text_binding.get("binding_name")
                        text = text_binding.get("text")
                        if not isinstance(binding_name, str) or binding_name in declared:
                            raise ValueError("native group binding names must be non-empty and distinct")
                        if not isinstance(text, str) or not text:
                            raise ValueError("native group text bindings require non-empty text")
                        bind_text_shape(
                            output_pptx,
                            slide_index=destination_slide,
                            shape_name=name_map[source_name],
                            binding_name=binding_name,
                            text=text,
                        )
                        declared.append(binding_name)
                binding = {"binding_names": declared, "slide_index": destination_slide}
                copied = {
                    "component_id": resolved_group["component_id"],
                    "component_type": resolved_group["component_type"],
                    "source_slide_index": source_slide,
                    "destination_slide_index": destination_slide,
                    "decoration_names": list(decoration_result["shape_names"].values()),
                    "placement": placement,
                    "cloned_top_level_shape_names": cloned_group["top_level_shape_names"],
                    "copied_parts": cloned_group["copied_parts"],
                    "cloned_template_native_group_component": True,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"native_group_component_clone operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "native_group_clone":
            shape_names = operation.get("shape_names")
            text_bindings = operation.get("text_bindings")
            if (
                not isinstance(shape_names, list)
                or not shape_names
                or any(not isinstance(name, str) or not name for name in shape_names)
            ):
                raise _operation_error(
                    f"native_group_clone operation {index} requires non-empty shape_names"
                )
            if not isinstance(text_bindings, list) or not text_bindings:
                raise _operation_error(
                    f"native_group_clone operation {index} requires non-empty text_bindings"
                )
            try:
                cloned = clone_native_shapes(
                    output_pptx,
                    source_slide_index=source_slide,
                    destination_slide_index=destination_slide,
                    shape_names=shape_names,
                )
                name_map = cloned["shape_names"]
                placement = None
                if operation.get("placement") is not None:
                    placement = place_native_shapes(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_names=list(name_map.values()),
                        placement=operation["placement"],
                    )
                declared: list[str] = []
                bound_shapes: list[str] = []
                for text_binding in text_bindings:
                    if not isinstance(text_binding, dict):
                        raise ValueError("text_bindings entries must be objects")
                    source_name = text_binding.get("shape_name")
                    if source_name not in name_map:
                        raise ValueError(
                            f"text binding references uncloned shape {source_name!r}"
                        )
                    declared_name = text_binding.get("binding_name")
                    text = text_binding.get("text")
                    if not isinstance(declared_name, str) or not declared_name.startswith("bind:"):
                        raise ValueError("text binding requires a bind:* binding_name")
                    if declared_name in declared:
                        raise ValueError("text binding names must be distinct within a native group")
                    if not isinstance(text, str):
                        raise ValueError("text binding requires text")
                    bind_text_shape(
                        output_pptx,
                        slide_index=destination_slide,
                        shape_name=name_map[source_name],
                        binding_name=declared_name,
                        text=text,
                    )
                    declared.append(declared_name)
                    bound_shapes.append(source_name)
                binding = {
                    "binding_names": declared,
                    "slide_index": destination_slide,
                }
                copied = {
                    **cloned,
                    "bound_shape_names": bound_shapes,
                    "placement": placement,
                    "cloned_template_group": True,
                }
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"native_group_clone operation {index} is invalid: {exc}"
                ) from exc
        elif kind == "component_clone":
            try:
                (
                    resolved,
                    component_type,
                    _segment_names,
                    segment_groups,
                    label_names,
                    item_groups,
                    shared_names,
                    elements,
                ) = _resolve_component_operation(operation, component_atlas=component_atlas)
                if resolved is None:
                    raise ValueError("component_clone requires component_requirement")
                atlas_source_slide = int(resolved["source_slide_index"])
                if source_slide is not None and source_slide != atlas_source_slide:
                    raise ValueError("declared source slide does not match the selected component")
                source_slide = atlas_source_slide
                if item_groups is not None:
                    item_native_names = [
                        name
                        for item_group in item_groups
                        for name in item_group["segment_names"]
                    ] + [
                        name
                        for item_group in item_groups
                        for names in item_group["label_fields"].values()
                        for name in names
                    ]
                    if component_type in {"card_grid", "icon_card_grid"}:
                        native_names = list(shared_names or []) + item_native_names
                    else:
                        native_names = item_native_names + list(shared_names or [])
                else:
                    native_names = [
                        name for group in segment_groups or [] for name in group
                    ] + list(label_names or [])
                cloned = clone_native_shapes(
                    output_pptx,
                    source_slide_index=source_slide,
                    destination_slide_index=destination_slide,
                    shape_names=list(dict.fromkeys(native_names)),
                )
                name_map = cloned["shape_names"]
                cloned_segment_groups = [
                    [name_map[name] for name in group]
                    for group in segment_groups or []
                ]
                cloned_label_names = [name_map[name] for name in label_names or []]
                cloned_item_groups = None
                cloned_shared_names = None
                if item_groups is not None:
                    cloned_segment_groups = None
                    cloned_label_names = None
                    cloned_item_groups = [{
                        "segment_names": [name_map[name] for name in item_group["segment_names"]],
                        "label_fields": {
                            field: [name_map[name] for name in names]
                            for field, names in item_group["label_fields"].items()
                        },
                    } for item_group in item_groups]
                    cloned_shared_names = [name_map[name] for name in shared_names or []]
                binding = bind_template_component(
                    output_pptx,
                    slide_index=destination_slide,
                    component_type=component_type,
                    segment_names=None,
                    label_names=cloned_label_names,
                    elements=elements,
                    segment_groups=cloned_segment_groups,
                    item_groups=cloned_item_groups,
                    shared_names=cloned_shared_names,
                    placement=operation.get("placement"),
                    component_instance_id=operation.get("component_instance_id"),
                    layout_mode=resolved.get("layout_mode"),
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"component_clone operation {index} is invalid: {exc}"
                ) from exc
            copied = {
                "component_id": resolved["component_id"],
                "component_type": component_type,
                "source_slide_index": source_slide,
                "destination_slide_index": destination_slide,
                "cloned_template_component": True,
                "shape_names": cloned["shape_names"],
            }
        elif kind == "component_bind_existing":
            if source_slide != destination_slide:
                raise _operation_error(
                    f"component_bind_existing operation {index} must use the same source and destination slide"
                )
            try:
                (
                    resolved,
                    component_type,
                    segment_names,
                    segment_groups,
                    label_names,
                    item_groups,
                    shared_names,
                    elements,
                ) = _resolve_component_operation(operation, component_atlas=component_atlas)
                if resolved is not None and resolved["source_slide_index"] != source_slide:
                    raise ValueError("selected component source slide does not match source_slide_index")
                binding = bind_template_component(
                    output_pptx,
                    slide_index=destination_slide,
                    component_type=component_type,
                    segment_names=segment_names,
                    label_names=label_names,
                    elements=elements,
                    segment_groups=segment_groups,
                    item_groups=item_groups,
                    shared_names=shared_names,
                    placement=operation.get("placement"),
                    component_instance_id=operation.get("component_instance_id"),
                    layout_mode=resolved.get("layout_mode") if resolved is not None else None,
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise _operation_error(
                    f"component_bind_existing operation {index} is invalid: {exc}"
                ) from exc
            copied = {
                "component_type": component_type,
                "source_slide_index": source_slide,
                "destination_slide_index": destination_slide,
                "existing_template_component": True,
            }
            if resolved is not None:
                copied["component_id"] = resolved["component_id"]
        elif kind == "table_clone":
            rows = operation.get("rows")
            if not isinstance(rows, list) or any(not isinstance(row, list) for row in rows):
                raise _operation_error(f"table operation {index} requires rows as a matrix")
            copied = clone_table_shape(
                template_pptx, output_pptx,
                source_slide_index=source_slide, destination_slide_index=destination_slide,
                table_name=operation.get("table_name"),
            )
            binding = bind_table_data(
                output_pptx, slide_index=destination_slide, table_name=copied["table_name"],
                binding_name=binding_name, rows=rows,
            )
        else:
            raise _operation_error(f"operation {index} has unsupported kind {kind!r}")
        operation_binding_names = binding.get("binding_names", [binding_name])
        for declared_name in operation_binding_names:
            binding_parts = declared_name.split(":")
            if len(binding_parts) < 3 or binding_parts[0] != "bind":
                raise _operation_error(f"operation {index} returned malformed binding {declared_name!r}")
            slide_ids.add(binding_parts[2])
            binding_names.add(declared_name)
        physical_slide_indices.add(destination_slide)
        applied.append({"kind": kind, "copied": copied, "binding": binding})
    return applied, slide_ids, physical_slide_indices, binding_names


def execute_strict_template(
    *,
    request: dict,
    template_pptx: str | Path,
    strict_plan: dict,
    ir: dict,
    source_docs: dict,
    output_pptx: str | Path,
    render_engine: str = "auto",
    component_atlas: dict | None = None,
    evidence_ledger: dict | None = None,
    content_bindings: dict | None = None,
    final_delivery: bool = False,
) -> dict:
    """Create a strictly template-native candidate and prove its delivery gates.

    This accepts only declared native-object operations, including reviewed
    Atlas components selected by semantic use and capacity.  It begins from a
    copy of the source template, so masters, layouts, theme and in-template
    brand media remain byte-identical unless the gate rejects it.
    """
    if request.get("route") != "template":
        return {"ok": False, "code": "TEMPLATE_ROUTE_REQUIRED"}
    template_path, output_path = Path(template_pptx), Path(output_pptx)
    context = prepare_template_context(request, template_path)
    if context.get("status") != "ready_for_visual_interpretation":
        return {"ok": False, "code": context.get("code", "TEMPLATE_CONTEXT_REJECTED"), "template": context}
    if context.get("use_mode") != "strict":
        return {"ok": False, "code": "STRICT_TEMPLATE_MODE_REQUIRED", "template": context}
    if component_atlas is not None:
        atlas_sha = component_atlas.get("source", {}).get("sha256")
        template_sha = context.get("source", {}).get("sha256")
        if atlas_sha != template_sha:
            return {
                "ok": False,
                "code": "COMPONENT_ATLAS_SOURCE_HASH_MISMATCH",
                "template": context,
                "component_atlas_source_sha256": atlas_sha,
                "template_source_sha256": template_sha,
            }
    if evidence_ledger is None or content_bindings is None:
        return {"ok": False, "code": "CONTENT_INTEGRITY_REQUIRED"}

    from .content_integrity_gate import evaluate_template_content_integrity

    content_integrity = evaluate_template_content_integrity(
        content_bindings, evidence_ledger,
    )
    if content_integrity.get("status") != "pass":
        return {
            "ok": False,
            "code": "CONTENT_INTEGRITY_FAILED",
            "content_integrity": content_integrity,
        }
    from .speaker_notes import (
        inspect_speaker_notes,
        validate_speaker_notes,
        write_speaker_notes,
    )

    notes_contract = validate_speaker_notes(
        ir,
        evidence_ledger=evidence_ledger,
        require_body_notes=final_delivery,
    )
    if final_delivery and notes_contract["status"] != "pass":
        return {
            "ok": False,
            "code": "SPEAKER_NOTES_FAILED",
            "speaker_notes": notes_contract,
            "content_integrity": content_integrity,
        }
    from .component_atlas import validate_model_authoring_atlas
    from .component_intent import evaluate_component_intents

    atlas_contract = validate_model_authoring_atlas(
        component_atlas or {"components": []},
    )
    if final_delivery and atlas_contract["status"] != "pass":
        return {
            "ok": False,
            "code": "COMPONENT_ATLAS_INCOMPLETE",
            "component_atlas": atlas_contract,
            "speaker_notes": notes_contract,
            "content_integrity": content_integrity,
        }

    component_intent = evaluate_component_intents(
        ir,
        component_atlas or {"status": "reviewed", "components": []},
        require_all_content_slides=final_delivery,
    )
    if final_delivery and component_intent["status"] != "pass":
        return {
            "ok": False,
            "code": "COMPONENT_INTENT_FAILED",
            "component_intent": component_intent,
            "speaker_notes": notes_contract,
            "content_integrity": content_integrity,
        }
    page_composition = strict_plan.get("page_composition")
    if strict_plan.get("authoring_mode") == "model_directed_template":
        if not isinstance(page_composition, dict) or page_composition.get("status") != "pass":
            return {
                "ok": False,
                "code": "TEMPLATE_PAGE_COMPOSITION_FAILED",
                "template_page_composition": page_composition,
                "component_intent": component_intent,
                "speaker_notes": notes_contract,
                "content_integrity": content_integrity,
            }
    from .model_authored_quality import evaluate_model_authored_quality

    authored_quality = evaluate_model_authored_quality(
        ir, require_assertions=final_delivery,
    )
    if final_delivery and authored_quality["status"] != "pass":
        return {
            "ok": False,
            "code": "MODEL_AUTHORED_QUALITY_FAILED",
            "model_authored_quality": authored_quality,
            "component_intent": component_intent,
            "speaker_notes": notes_contract,
            "content_integrity": content_integrity,
        }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pptsmith-template-work-", dir=output_path.parent) as work_dir:
        working_path = Path(work_dir) / "candidate-with-template-pages.pptx"
        expanded_baseline_path = Path(work_dir) / "expanded-template-baseline.pptx"
        baseline_path = Path(work_dir) / "baseline-delivery-pages.pptx"
        shutil.copyfile(template_path, working_path)
        try:
            canvas = _ensure_destination_slides(working_path, strict_plan)
            shutil.copyfile(working_path, expanded_baseline_path)
            applied, slide_ids, physical_slide_indices, binding_names = _apply_operations(
                template_path,
                working_path,
                strict_plan,
                component_atlas=component_atlas,
                ir=ir,
            )
            if final_delivery:
                from .template_readability import enforce_bound_text_floor

                readability_normalization = enforce_bound_text_floor(working_path)
            else:
                readability_normalization = {
                    "status": "not_applied",
                    "adjusted_run_count": 0,
                    "adjustments": [],
                }
        except ValueError as exc:
            return {"ok": False, "code": str(exc).split(":", 1)[0], "message": str(exc), "template": context}

        delivery_slide_numbers = sorted(physical_slide_indices)
        delivery = write_slide_subset(
            working_path,
            output_path,
            slide_numbers=delivery_slide_numbers,
        )
        physical_to_slide_id: dict[int, str] = {}
        for operation in applied:
            destination = operation.get("binding", {}).get("slide_index")
            names = operation.get("binding", {}).get("binding_names")
            if not isinstance(names, list):
                single = operation.get("binding", {}).get("binding_name")
                names = [single] if isinstance(single, str) else []
            for name in names:
                parts = name.split(":") if isinstance(name, str) else []
                if isinstance(destination, int) and len(parts) >= 3:
                    physical_to_slide_id[destination] = parts[2]
        ir_by_id = {
            slide.get("id"): slide
            for slide in ir.get("slides", [])
            if isinstance(slide, dict) and isinstance(slide.get("id"), str)
        }
        notes_by_output_index: dict[int, dict] = {}
        required_note_indices: list[int] = []
        for output_index, physical_index in enumerate(delivery_slide_numbers, 1):
            slide = ir_by_id.get(physical_to_slide_id.get(physical_index))
            if not isinstance(slide, dict):
                continue
            if slide.get("slide_role", "content") not in {"cover", "section", "closing"}:
                required_note_indices.append(output_index)
            if isinstance(slide.get("speaker_notes"), dict):
                notes_by_output_index[output_index] = slide["speaker_notes"]
        notes_write = (
            write_speaker_notes(output_path, notes_by_output_index)
            if notes_by_output_index else {"status": "not_written", "count": 0, "slide_indices": []}
        )
        notes_inspection = inspect_speaker_notes(
            output_path,
            required_slide_indices=required_note_indices if final_delivery else sorted(notes_by_output_index),
        )
        write_slide_subset(
            expanded_baseline_path,
            baseline_path,
            slide_numbers=delivery_slide_numbers,
        )

        from ppt_qa.verifier import run_render_report, run_structural_inspection

        binding = verify_authored_page(
            output_path, ir, slide_ids=sorted(slide_ids), source_docs=source_docs,
            declared_binding_names=binding_names,
        )
        baseline_inspection = run_structural_inspection(baseline_path, route="template")
        candidate_inspection = run_structural_inspection(output_path, route="template")
        inspection = _inspection_delta(baseline_inspection, candidate_inspection)
        inspection["qa_route"] = "template"
    source_size = context["source"]["slide_size_in"]
    aspect = float(source_size["width"]) / float(source_size["height"])
    render_dir = output_path.parent / "qa" / "candidate"
    if render_dir.exists():
        shutil.rmtree(render_dir)
    render = run_render_report(
        output_path, render_dir,
        engine=render_engine, expected_slides=int(delivery["output_slide_count"]),
        expected_aspect=aspect, dpi=96,
    )
    for page in render.get("slides", []):
        image = Path(page.get("image", ""))
        if image.is_file():
            page["sha256"] = "sha256:" + hashlib.sha256(image.read_bytes()).hexdigest()
    assets = _asset_preservation(template_path, output_path)
    from .template_readability import inspect_template_native_visual_floor
    from .template_delivery_quality import inspect_template_delivery_quality
    from .template_visual_quality import inspect_template_visual_quality

    native_visual_floor = inspect_template_native_visual_floor(output_path)
    template_delivery_quality = inspect_template_delivery_quality(output_path, ir=ir)
    template_visual_quality = inspect_template_visual_quality(
        output_path,
        ir=ir,
        render_report=render,
        page_composition=page_composition,
    )
    ok = (
        binding.get("status") == "pass"
        and inspection.get("status") == "passed"
        and render.get("status") == "passed"
        and assets["status"] == "pass"
        and (not final_delivery or native_visual_floor["status"] == "pass")
        and (not final_delivery or template_delivery_quality["status"] == "pass")
        and (not final_delivery or template_visual_quality["status"] == "pass")
        and (not final_delivery or notes_inspection["status"] == "pass")
    )
    return {
        "ok": ok,
        "status": "strict_candidate_verified" if ok else "strict_candidate_rejected",
        "template": context,
        "operations": applied,
        "canvas": canvas,
        "readability_normalization": readability_normalization,
        "delivery": delivery,
        "binding": binding,
        "inspection": inspection,
        "render": render,
        "asset_preservation": assets,
        "native_visual_floor": native_visual_floor,
        "template_delivery_quality": template_delivery_quality,
        "template_visual_quality": template_visual_quality,
        "content_integrity": content_integrity,
        "component_intent": component_intent,
        "template_page_composition": page_composition,
        "component_atlas_contract": atlas_contract,
        "model_authored_quality": authored_quality,
        "speaker_notes": {
            "contract": notes_contract,
            "write": notes_write,
            "inspection": notes_inspection,
        },
        "output_pptx": str(output_path),
        "visual_review": "required_before_final_delivery",
        "visual_review_contract": "page_visual_v1",
    }
