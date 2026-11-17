from __future__ import annotations

from typing import Any


SCHEMA_VERSION = "1.0.0"
MINIMUM_PRIMARY_ANCHOR_AREA_RATIO = 0.50
MINIMUM_VISUAL_RUBRIC_DIMENSION = 2.5

ALLOWED_ACTIONS = frozenset(
    {
        "delete_duplicate_copy",
        "merge_supporting_blocks",
        "replace_component",
        "enlarge_primary_anchor",
        "rebalance_density",
        "correct_style_tokens",
    }
)

PROTECTED_FIELDS = [
    "evidence_values",
    "source_refs",
    "message",
    "editability_requirement",
]

_ACTION_BY_OBSERVATION = {
    "VISUAL_DUPLICATE_COPY": {
        "action": "delete_duplicate_copy",
        "target": "supporting",
    },
    "VISUAL_FRAGMENTED_SUPPORT": {
        "action": "merge_supporting_blocks",
        "target": "supporting",
    },
    "VISUAL_REPEATED_CARDS": {
        "action": "replace_component",
        "target": "primary",
    },
    "VISUAL_WEAK_PRIMARY_ANCHOR": {
        "action": "enlarge_primary_anchor",
        "minimum_area_ratio": MINIMUM_PRIMARY_ANCHOR_AREA_RATIO,
    },
    "VISUAL_DENSITY_IMBALANCE": {
        "action": "rebalance_density",
        "target": "slide",
    },
    "VISUAL_STYLE_TOKEN_DRIFT": {
        "action": "correct_style_tokens",
        "target": "slide",
    },
}


class VisualRevisionError(ValueError):
    pass


def build_revision_request(
    visual_plan: Any,
    observations: Any,
    *,
    rubric_score: Any = None,
    contact_sheet_metrics: Any = None,
) -> dict[str, Any]:
    slides = _validated_slides(visual_plan)
    actions_by_slide: dict[str, list[dict[str, Any]]] = {
        slide_id: [] for slide_id in slides
    }

    for observation in _validated_observations(observations):
        slide_id = observation["slide_id"]
        if slide_id not in actions_by_slide:
            continue
        for code in observation["codes"]:
            action = _ACTION_BY_OBSERVATION.get(code)
            if action is not None:
                _append_action(actions_by_slide[slide_id], action)

    for metric in _validated_contact_metrics(contact_sheet_metrics):
        slide_id = metric["slide_id"]
        if slide_id not in actions_by_slide:
            continue
        actions = actions_by_slide[slide_id]
        component = slides[slide_id]["semantic_component"]
        anchor_ratio = _optional_number(metric.get("primary_anchor_area_ratio"))
        if (
            anchor_ratio is not None
            and anchor_ratio < MINIMUM_PRIMARY_ANCHOR_AREA_RATIO
        ):
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_WEAK_PRIMARY_ANCHOR"])
        if (
            _number(metric.get("repeated_card_count")) >= 3
            and component in {"generic_cards", "narrative_statement"}
        ):
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_REPEATED_CARDS"])
        if _number(metric.get("supporting_block_count")) > 2:
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_FRAGMENTED_SUPPORT"])
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_DENSITY_IMBALANCE"])
        if _number(metric.get("duplicate_copy_count")) > 0:
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_DUPLICATE_COPY"])
        if _number(metric.get("style_token_drift_count")) > 0:
            _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_STYLE_TOKEN_DRIFT"])

    rubric = _validated_rubric(rubric_score)
    if rubric.get("page_composition", 3.0) < MINIMUM_VISUAL_RUBRIC_DIMENSION:
        for slide_id, slide in slides.items():
            if slide["priority"] == "key":
                _append_action(
                    actions_by_slide[slide_id],
                    _ACTION_BY_OBSERVATION["VISUAL_WEAK_PRIMARY_ANCHOR"],
                )
    if rubric.get("component_craft", 3.0) < MINIMUM_VISUAL_RUBRIC_DIMENSION:
        for actions in actions_by_slide.values():
            if actions:
                _append_action(actions, _ACTION_BY_OBSERVATION["VISUAL_STYLE_TOKEN_DRIFT"])

    revision_slides = [
        {"slide_id": slide_id, "actions": actions_by_slide[slide_id]}
        for slide_id in slides
        if actions_by_slide[slide_id]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "revision_required" if revision_slides else "no_revision",
        "protected_fields": list(PROTECTED_FIELDS),
        "slides": revision_slides,
    }


def _validated_slides(visual_plan: Any) -> dict[str, dict[str, str]]:
    if not isinstance(visual_plan, dict):
        raise VisualRevisionError("REVISION_PLAN_INVALID")
    raw_slides = visual_plan.get("slides")
    if not isinstance(raw_slides, list) or not raw_slides:
        raise VisualRevisionError("REVISION_PLAN_INVALID")

    slides: dict[str, dict[str, str]] = {}
    for slide in raw_slides:
        if not isinstance(slide, dict):
            raise VisualRevisionError("REVISION_PLAN_INVALID")
        slide_id = slide.get("slide_id")
        priority = slide.get("priority")
        component = slide.get("semantic_component")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (slide_id, priority, component)
        ):
            raise VisualRevisionError("REVISION_PLAN_INVALID")
        normalized_id = slide_id.strip()
        if normalized_id in slides:
            raise VisualRevisionError("REVISION_PLAN_INVALID")
        slides[normalized_id] = {
            "priority": priority.strip(),
            "semantic_component": component.strip(),
        }
    return slides


def _validated_observations(observations: Any) -> list[dict[str, Any]]:
    if observations is None:
        return []
    if not isinstance(observations, list):
        raise VisualRevisionError("REVISION_OBSERVATIONS_INVALID")
    validated: list[dict[str, Any]] = []
    for observation in observations:
        if not isinstance(observation, dict):
            raise VisualRevisionError("REVISION_OBSERVATIONS_INVALID")
        slide_id = observation.get("slide_id")
        codes = observation.get("codes")
        if (
            not isinstance(slide_id, str)
            or not slide_id.strip()
            or not isinstance(codes, list)
        ):
            raise VisualRevisionError("REVISION_OBSERVATIONS_INVALID")
        validated.append(
            {
                "slide_id": slide_id.strip(),
                "codes": [
                    code.strip()
                    for code in codes
                    if isinstance(code, str) and code.strip()
                ],
            }
        )
    return validated


def _validated_contact_metrics(contact_sheet_metrics: Any) -> list[dict[str, Any]]:
    if contact_sheet_metrics is None:
        return []
    if not isinstance(contact_sheet_metrics, dict):
        raise VisualRevisionError("REVISION_CONTACT_METRICS_INVALID")
    metrics = contact_sheet_metrics.get("slides", [])
    if not isinstance(metrics, list):
        raise VisualRevisionError("REVISION_CONTACT_METRICS_INVALID")
    return [
        metric
        for metric in metrics
        if isinstance(metric, dict)
        and isinstance(metric.get("slide_id"), str)
        and metric["slide_id"].strip()
    ]


def _validated_rubric(rubric_score: Any) -> dict[str, float]:
    if rubric_score is None:
        return {}
    if not isinstance(rubric_score, dict):
        raise VisualRevisionError("REVISION_RUBRIC_INVALID")
    return {
        key: float(value)
        for key, value in rubric_score.items()
        if key in {"page_composition", "component_craft"}
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
    }


def _number(value: Any) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return 0.0


def _optional_number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def _append_action(actions: list[dict[str, Any]], action: dict[str, Any]) -> None:
    normalized = dict(action)
    if normalized["action"] not in ALLOWED_ACTIONS:
        raise VisualRevisionError("REVISION_ACTION_NOT_ALLOWED")
    if normalized not in actions:
        actions.append(normalized)
