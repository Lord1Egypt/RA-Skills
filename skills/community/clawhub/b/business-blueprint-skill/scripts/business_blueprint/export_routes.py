from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[：:\s]")


@dataclass(frozen=True)
class ExportRouteDecision:
    route: str
    reason: str
    fallback_route: str | None
    terminal_behavior: str


def resolve_export_route(
    blueprint: dict[str, Any],
    requested_route: str | None = None,
) -> ExportRouteDecision:
    requested = requested_route.strip() if requested_route else None
    library = blueprint.get("library", {})
    systems = list(library.get("systems", []))
    flow_steps = list(library.get("flowSteps", []))
    actors = list(library.get("actors", []))

    if requested:
        if _is_route_eligible(requested, systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
            return ExportRouteDecision(
                route=requested,
                reason=f"requested route: {requested}",
                fallback_route=_fallback_for(requested),
                terminal_behavior="error",
            )
        fallback = _fallback_for(requested) or "freeflow"
        return ExportRouteDecision(
            route=fallback,
            reason=f"requested route not eligible: {requested}",
            fallback_route=None if fallback == "freeflow" else _fallback_for(fallback),
            terminal_behavior="error",
        )

    # Route priority: architecture-template > poster > hierarchy > freeflow > evolution > swimlane
    # Swimlane is the most constrained scenario - lowest priority
    if _is_route_eligible("architecture-template", systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
        return ExportRouteDecision("architecture-template", "categorized architecture systems", "freeflow", "error")
    if _is_route_eligible("poster", systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
        return ExportRouteDecision("poster", "layered systems", "freeflow", "error")
    if _is_route_eligible("hierarchy", systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
        return ExportRouteDecision("hierarchy", "hierarchical system grouping", "freeflow", "error")
    if _is_route_eligible("evolution", systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
        return ExportRouteDecision("evolution", "dated flow steps", "freeflow", "error")
    if _is_route_eligible("swimlane", systems=systems, flow_steps=flow_steps, actors=actors, blueprint=blueprint):
        return ExportRouteDecision("swimlane", "actor-owned flow steps", "freeflow", "error")
    return ExportRouteDecision("freeflow", "generic fallback", None, "error")


def _fallback_for(route: str) -> str | None:
    return {
        "architecture-template": "freeflow",
        "poster": "freeflow",
        "swimlane": "freeflow",
        "hierarchy": "freeflow",
        "evolution": "freeflow",
        "freeflow": None,
    }.get(route, "freeflow")


def _is_route_eligible(
    route: str,
    *,
    systems: list[dict[str, Any]],
    flow_steps: list[dict[str, Any]],
    actors: list[dict[str, Any]],
    blueprint: dict[str, Any],
) -> bool:
    if route == "freeflow":
        return bool(systems or flow_steps or blueprint.get("relations"))
    if route == "architecture-template":
        categories = {s.get("category") for s in systems if s.get("category")}
        infra_types = {
            s.get("properties", {}).get("type")
            for s in systems
            if isinstance(s.get("properties"), dict)
        }
        return bool(systems) and (
            {"frontend", "backend", "database"}.issubset(categories)
            or {"aws", "k8s"} & infra_types
        )
    if route == "poster":
        # Poster requires explicit layer/group structure on systems.
        # Freeflow is the default; poster only when blueprint has real layer data.
        layers = {s.get("layer") for s in systems if s.get("layer")}
        return len(layers) >= 2
    if route == "swimlane":
        # Swimlane is the MOST CONSTRAINED scenario — only when the blueprint
        # is clearly flow-centric (steps >> systems) with sequential orchestration.
        # A blueprint with many systems and a few steps is architecture-focused,
        # not flow-focused, and should use freeflow instead.
        actor_ids = {a.get("id") for a in actors if a.get("id")}
        actor_owned = [step for step in flow_steps if step.get("actorId") in actor_ids]
        has_sequence = any(
            step.get("inputRefs") or step.get("outputRefs")
            for step in flow_steps
        )
        flow_dominant = len(flow_steps) > len(systems)
        return (
            len(actor_ids) >= 3
            and len(actor_owned) >= 3
            and len(flow_steps) >= 4
            and has_sequence
            and flow_dominant
        )
    if route == "hierarchy":
        has_segment = any(
            s.get("layer")
            or s.get("segment")
            or (isinstance(s.get("properties"), dict) and s.get("properties", {}).get("segment"))
            for s in systems
        )
        return len(systems) >= 2 and has_segment
    if route == "evolution":
        dated_steps = [step for step in flow_steps if DATE_PREFIX_RE.match(step.get("name", ""))]
        return len(dated_steps) >= 2
    return False
