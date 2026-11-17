from __future__ import annotations

from typing import Any


ROUTES = (
    "research_report",
    "technical_architecture",
    "enterprise_proposal",
    "product_business_review",
    "product_prd",
    "editorial_knowledge",
    "domain_adapter",
)

GENERAL_ROUTE = "general_visual_narrative"
SCHEMA_VERSION = "1.0"
RESEARCH_EVIDENCE = {"statistics", "comparison", "trend"}
ARCHITECTURE_RELATIONSHIPS = {"system_boundary", "data_flow", "layer"}


def route_task(analysis: Any, explicit_route: str | None = None) -> dict[str, Any]:
    scores = {route: 0.0 for route in ROUTES}
    warnings: list[str] = []
    analysis_map = _analysis_mapping(analysis)
    if analysis_map is None:
        warnings.append("TASK_ROUTE_INVALID_ANALYSIS")
        analysis_map = {}

    if explicit_route is None and analysis_map.get("requested_route") == "product_prd":
        explicit_route = "product_prd"

    evidence = set(_string_list(analysis_map.get("evidence_types")))
    relationships = set(_string_list(analysis_map.get("relationship_types")))
    research_hits = evidence & RESEARCH_EVIDENCE
    architecture_hits = relationships & ARCHITECTURE_RELATIONSHIPS

    if len(research_hits) >= 2:
        scores["research_report"] += 0.65
    elif research_hits:
        scores["research_report"] += 0.35

    if len(architecture_hits) >= 2:
        scores["technical_architecture"] += 0.65
    elif architecture_hits:
        scores["technical_architecture"] += 0.35

    if _string_list(analysis_map.get("project_governance_terms")):
        scores["domain_adapter"] += 0.45

    if explicit_route in scores:
        scores[explicit_route] += 0.75 if explicit_route == "product_prd" else 0.4

    selected = max(scores, key=scores.get)
    confidence = scores[selected]
    rejected_routes = [route for route in ROUTES if route != selected]

    if confidence < 0.6:
        selected = GENERAL_ROUTE
        warnings.append("TASK_ROUTE_LOW_CONFIDENCE")
        rejected_routes = list(ROUTES)

    return {
        "schema_version": SCHEMA_VERSION,
        "selected_route": selected,
        "confidence": confidence,
        "scores": scores,
        "rejected_routes": rejected_routes,
        "warnings": warnings,
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _analysis_mapping(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    return None
