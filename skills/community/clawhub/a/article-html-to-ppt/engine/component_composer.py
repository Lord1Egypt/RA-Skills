"""Build strict native-component operations from page-level semantic slots."""
from __future__ import annotations

from copy import deepcopy

from .component_atlas import select_component
from .template_component_adaptation import evaluate_component_target_fit


def _placement(value: object, *, page_index: int, component_index: int) -> dict:
    if not isinstance(value, dict):
        raise ValueError(
            f"page {page_index} component {component_index} requires a placement object"
        )
    resolved: dict[str, float] = {}
    for key in ("x", "y", "w", "h"):
        item = value.get(key)
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError(f"component placement {key} must be a number")
        resolved[key] = float(item)
    if resolved["x"] < 0 or resolved["y"] < 0 or resolved["w"] <= 0 or resolved["h"] <= 0:
        raise ValueError("component placement must have non-negative origin and positive size")
    if resolved["x"] + resolved["w"] > 1 or resolved["y"] + resolved["h"] > 1:
        raise ValueError("component placement must remain inside the slide")
    fit_mode = value.get("fit_mode")
    if fit_mode is not None:
        if fit_mode not in {"contain", "stretch"}:
            raise ValueError("component placement fit_mode must be contain or stretch")
        resolved["fit_mode"] = fit_mode
    require_fill = value.get("require_fill")
    if require_fill is not None:
        if not isinstance(require_fill, bool):
            raise ValueError("component placement require_fill must be boolean")
        resolved["require_fill"] = require_fill
    return resolved


def _overlaps(first: dict, second: dict) -> bool:
    return (
        max(first["x"], second["x"]) < min(first["x"] + first["w"], second["x"] + second["w"])
        and max(first["y"], second["y"]) < min(first["y"] + first["h"], second["y"] + second["h"])
    )


def _within(parent: dict, child: dict) -> dict:
    return {
        "x": round(parent["x"] + child["x"] * parent["w"], 10),
        "y": round(parent["y"] + child["y"] * parent["h"], 10),
        "w": round(child["w"] * parent["w"], 10),
        "h": round(child["h"] * parent["h"], 10),
    }


def _payload_label_texts(spec: dict) -> list[str]:
    texts: list[str] = []
    for element in spec.get("elements", []) if isinstance(spec.get("elements"), list) else []:
        if not isinstance(element, dict):
            continue
        for key, value in element.items():
            if key in {"binding_name", "value", "id"}:
                continue
            if isinstance(value, str) and value.strip():
                texts.append(value.strip())
            elif isinstance(value, dict):
                for nested in value.values():
                    if isinstance(nested, str) and nested.strip() and not nested.startswith("bind:"):
                        texts.append(nested.strip())
                    elif isinstance(nested, dict):
                        text = nested.get("text")
                        if isinstance(text, str) and text.strip():
                            texts.append(text.strip())
    return texts


def _numeric_annotation_count(spec: dict) -> int:
    annotations = spec.get("numeric_annotations", [])
    count = len(annotations) if isinstance(annotations, list) else 0
    elements = spec.get("elements", [])
    if isinstance(elements, list):
        count += sum(
            isinstance(element, dict)
            and isinstance(element.get("value"), (int, float))
            and not isinstance(element.get("value"), bool)
            for element in elements
        )
    return count


def build_component_plan(atlas: dict, composition: dict) -> dict:
    """Translate semantic page slots into fail-closed ``component_clone`` ops.

    Element capacity is derived from the actual data list.  The caller does
    not specify or hard-code a template shape count, and components occupying
    the same destination page must have non-overlapping normalized slots.
    """
    if not isinstance(composition, dict) or composition.get("schema_version") != "1.0.0":
        raise ValueError("component composition schema_version must be 1.0.0")
    pages = composition.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("component composition requires a non-empty pages list")

    operations: list[dict] = []
    selections: list[dict] = []
    for page_index, page in enumerate(pages):
        if not isinstance(page, dict):
            raise ValueError(f"page {page_index} must be an object")
        destination_slide_index = page.get("destination_slide_index")
        if (
            isinstance(destination_slide_index, bool)
            or not isinstance(destination_slide_index, int)
            or destination_slide_index < 1
        ):
            raise ValueError(f"page {page_index} requires a positive destination_slide_index")
        components = page.get("components")
        if not isinstance(components, list) or not components:
            raise ValueError(f"page {page_index} requires a non-empty components list")

        occupied: list[dict] = []
        for component_index, component in enumerate(components):
            if not isinstance(component, dict):
                raise ValueError(f"page {page_index} component {component_index} must be an object")
            placement = _placement(
                component.get("placement"),
                page_index=page_index,
                component_index=component_index,
            )
            if any(_overlaps(placement, existing) for existing in occupied):
                raise ValueError(
                    f"component slots overlap on destination slide {destination_slide_index}"
                )
            occupied.append(placement)

            component_instance_id = f"slide-{destination_slide_index}-component-{component_index + 1}"

            def expand(spec: dict, box: dict, instance_id: str, *, exact_component_id: str | None = None) -> None:
                if spec.get("model_authored") is True:
                    script = spec.get("author_script")
                    slide_id = spec.get("slide_id")
                    component_id = spec.get("component_id")
                    if not all(isinstance(value, str) and value for value in (
                        script, slide_id, component_id,
                    )):
                        raise ValueError(
                            f"model-authored component {instance_id} requires script, slide_id and component_id"
                        )
                    required_binding_names = spec.get("required_binding_names", [])
                    if not isinstance(required_binding_names, list) or any(
                        not isinstance(name, str) or not name
                        for name in required_binding_names
                    ):
                        raise ValueError(
                            f"model-authored component {instance_id} has invalid required bindings"
                        )
                    asset_bindings = spec.get("asset_bindings", [])
                    if not isinstance(asset_bindings, list) or any(
                        not isinstance(asset, dict) for asset in asset_bindings
                    ):
                        raise ValueError(
                            f"model-authored component {instance_id} has invalid asset bindings"
                        )
                    author_context = spec.get("author_context", {})
                    if not isinstance(author_context, dict):
                        raise ValueError(
                            f"model-authored component {instance_id} has invalid author context"
                        )
                    selections.append({
                        "destination_slide_index": destination_slide_index,
                        "component_index": component_index,
                        "component_instance_id": instance_id,
                        "component_id": component_id,
                        "family": "model_authored_native",
                        "granularity": "model_authored",
                        "reason": "no feasible reviewed template component; model-authored native component",
                    })
                    operations.append({
                        "kind": "model_authored_native_component",
                        "destination_slide_index": destination_slide_index,
                        "component_instance_id": instance_id,
                        "component_id": component_id,
                        "slide_id": slide_id,
                        "author_script": script,
                        "required_binding_names": deepcopy(required_binding_names),
                        "asset_bindings": deepcopy(asset_bindings),
                        "author_context": deepcopy(author_context),
                        "placement": box,
                    })
                    return
                elements = spec.get("elements")
                if isinstance(elements, list) and elements:
                    element_count = len(elements)
                else:
                    element_count = spec.get("element_count", 1 if spec.get("chart") else None)
                if isinstance(element_count, bool) or not isinstance(element_count, int) or element_count < 1:
                    raise ValueError(f"component {instance_id} requires elements or a positive element_count")
                requirement = {
                    "semantic_use": spec.get("semantic_use"),
                    "element_count": element_count,
                }
                if spec.get("family") is not None:
                    requirement["family"] = spec["family"]
                if spec.get("required_slots") is not None:
                    requirement["required_slots"] = spec["required_slots"]
                for field in (
                    "topology", "archetype", "composition_role",
                    "text_requirements", "data_shape",
                ):
                    if spec.get(field) is not None:
                        requirement[field] = spec[field]
                requested_component_id = exact_component_id or spec.get("component_id")
                if requested_component_id is not None:
                    requirement["component_id"] = requested_component_id
                selection = select_component(atlas, {**requirement, "target_placement": box})
                if selection["status"] != "selected":
                    raise ValueError(f"component {instance_id}: {selection['reason']}")
                selected = next(
                    item for item in atlas.get("components", [])
                    if item.get("component_id") == selection["component_id"]
                )
                adaptation = selected.get("adaptation_contract")
                if isinstance(adaptation, dict):
                    fit = evaluate_component_target_fit(selected, box)
                    if fit.get("status") != "pass":
                        raise ValueError(
                            f"component {instance_id}: {fit.get('code')} "
                            f"target={fit.get('target_aspect_ratio')} "
                            f"supported={fit.get('supported_aspect_ratio')}"
                        )
                    density = adaptation.get("density", {})
                    minimum_label_chars = density.get("minimum_label_chars", 1)
                    labels = _payload_label_texts(spec)
                    if minimum_label_chars > 1 and (
                        not labels or sum(map(len, labels)) < minimum_label_chars * element_count
                    ):
                        raise ValueError(
                            f"component {instance_id}: TEMPLATE_COMPONENT_LABEL_DENSITY_LOW"
                        )
                    minimum_numeric = density.get("minimum_numeric_annotations", 0)
                    if minimum_numeric and _numeric_annotation_count(spec) < minimum_numeric:
                        raise ValueError(
                            f"component {instance_id}: TEMPLATE_COMPONENT_NUMERIC_ANNOTATION_LOW"
                        )
                selections.append({
                    "destination_slide_index": destination_slide_index,
                    "component_index": component_index,
                    "component_instance_id": instance_id,
                    "component_id": selection["component_id"],
                    "family": selection["family"],
                    "granularity": selected.get("granularity", "micro"),
                    "reason": selection["reason"],
                    **({"adaptation": fit} if isinstance(adaptation, dict) else {}),
                })

                children = selected.get("children", [])
                if children:
                    child_payloads = spec.get("children")
                    if not isinstance(child_payloads, dict):
                        raise ValueError(f"component {instance_id} requires child slot data")
                    known_slots = {child["slot_id"] for child in children}
                    unknown = set(child_payloads) - known_slots
                    if unknown:
                        raise ValueError(f"component {instance_id} has unknown child slots {sorted(unknown)!r}")
                    for child in children:
                        slot_id = child["slot_id"]
                        child_spec = child_payloads.get(slot_id)
                        if child_spec is None:
                            if child.get("required", True):
                                raise ValueError(f"component {instance_id} is missing required child slot {slot_id!r}")
                            continue
                        if not isinstance(child_spec, dict):
                            raise ValueError(f"component {instance_id} child slot {slot_id!r} must be an object")
                        child_component = next(
                            item for item in atlas.get("components", [])
                            if item.get("component_id") == child["component_id"]
                        )
                        resolved_child_spec = deepcopy(child_spec)
                        resolved_child_spec.setdefault(
                            "semantic_use", child_component.get("semantic_uses", [None])[0]
                        )
                        resolved_child_spec.setdefault("family", child_component.get("family"))
                        expand(
                            resolved_child_spec,
                            _within(box, child["placement"]),
                            f"{instance_id}-{slot_id}",
                            exact_component_id=child["component_id"],
                        )
                    return

                if selected.get("renderer") == "native_group":
                    text_bindings = spec.get("text_bindings")
                    if not isinstance(text_bindings, list) or not text_bindings:
                        raise ValueError(
                            f"native group component {instance_id} requires text_bindings"
                        )
                    operations.append({
                        "kind": "native_group_component_clone",
                        "destination_slide_index": destination_slide_index,
                        "component_instance_id": instance_id,
                        "component_requirement": requirement,
                        "text_bindings": deepcopy(text_bindings),
                        "placement": box,
                        **({"adaptation": deepcopy(adaptation)} if isinstance(adaptation, dict) else {}),
                    })
                    return

                if any(group.get("role") == "chart" for group in selected.get("groups", [])):
                    if selected.get("family") == "chart_dashboard":
                        charts = spec.get("charts")
                        text_bindings = spec.get("text_bindings", [])
                        clear_text_names = spec.get("clear_text_names", [])
                        if not isinstance(charts, list) or len(charts) != element_count:
                            raise ValueError(
                                f"dashboard component {instance_id} requires one chart payload per element"
                            )
                        if not isinstance(text_bindings, list) or not isinstance(clear_text_names, list):
                            raise ValueError(
                                f"dashboard component {instance_id} requires text and clear lists"
                            )
                        operations.append({
                            "kind": "chart_dashboard_clone",
                            "destination_slide_index": destination_slide_index,
                            "component_instance_id": instance_id,
                            "component_requirement": requirement,
                            "charts": deepcopy(charts),
                            "text_bindings": deepcopy(text_bindings),
                            "clear_text_names": deepcopy(clear_text_names),
                            "placement": box,
                            **({"adaptation": deepcopy(adaptation)} if isinstance(adaptation, dict) else {}),
                        })
                        return
                    chart = spec.get("chart")
                    text_bindings = spec.get("text_bindings", [])
                    if not isinstance(chart, dict) or not isinstance(text_bindings, list):
                        raise ValueError(f"chart component {instance_id} requires chart and text_bindings")
                    operations.append({
                        "kind": "chart_component_clone",
                        "destination_slide_index": destination_slide_index,
                        "component_instance_id": instance_id,
                        "component_requirement": requirement,
                        "chart": deepcopy(chart),
                        "text_bindings": deepcopy(text_bindings),
                        "placement": box,
                        **({"adaptation": deepcopy(adaptation)} if isinstance(adaptation, dict) else {}),
                    })
                    return
                if not isinstance(elements, list) or not elements:
                    raise ValueError(f"component {instance_id} requires elements")
                operations.append({
                    "kind": "component_clone",
                    "destination_slide_index": destination_slide_index,
                    "component_instance_id": instance_id,
                    "component_requirement": requirement,
                    "elements": deepcopy(elements),
                    "placement": box,
                    **({"adaptation": deepcopy(adaptation)} if isinstance(adaptation, dict) else {}),
                })

            expand(component, placement, component_instance_id)

    result = {
        "schema_version": "1.0.0",
        "operations": operations,
        "selections": selections,
    }
    if isinstance(composition.get("page_composition"), dict):
        result["authoring_mode"] = "model_directed_template"
        result["page_composition"] = deepcopy(composition["page_composition"])
    return result
