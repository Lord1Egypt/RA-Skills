from __future__ import annotations

from collections import Counter
from typing import Any

from knowledge_validate import validate_knowledge_extension
from model import ensure_top_level_shape


def _issue(
    severity: str,
    error_code: str,
    message: str,
    affected_ids: list[str],
    suggested_fix: str,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "errorCode": error_code,
        "message": message,
        "affectedIds": affected_ids,
        "suggestedFix": suggested_fix,
    }


def validate_blueprint(payload: dict[str, Any]) -> dict[str, Any]:
    blueprint = ensure_top_level_shape(payload)
    issues: list[dict[str, Any]] = []

    # v2 knowledge extension validation runs first so missing core fields are
    # surfaced before downstream architecture-specific checks.
    issues.extend(validate_knowledge_extension(blueprint))

    all_ids: list[str] = []
    for collection in blueprint["library"].values():
        if isinstance(collection, list):
            all_ids.extend(
                item["id"]
                for item in collection
                if isinstance(item, dict) and "id" in item
            )

    duplicates = [item_id for item_id, count in Counter(all_ids).items() if count > 1]
    for item_id in duplicates:
        issues.append(
            _issue(
                "error",
                "DUPLICATE_ID",
                f"Duplicate identifier {item_id}.",
                [item_id],
                "Rename one of the duplicate entities.",
            )
        )

    capabilities = [
        capability
        for capability in blueprint["library"]["capabilities"]
        if isinstance(capability, dict)
    ]
    capability_ids = {
        cap["id"] for cap in capabilities if isinstance(cap, dict) and "id" in cap
    }
    flow_steps = blueprint["library"]["flowSteps"]
    systems = blueprint["library"]["systems"]
    views = blueprint["views"]

    unmapped_flow_steps = [
        step["id"]
        for step in flow_steps
        if not step.get("unmappedAllowed") and not step.get("capabilityIds")
    ]
    for step_id in unmapped_flow_steps:
        issues.append(
            _issue(
                "warning",
                "UNMAPPED_FLOW_STEP",
                f"Flow step {step_id} is not linked to a capability.",
                [step_id],
                "Add capabilityIds or mark the step unmappedAllowed.",
            )
        )

    unmapped_systems = [
        system["id"]
        for system in systems
        if not system.get("supportOnly")
        and system.get("category") != "external"
        and not system.get("capabilityIds")
    ]
    for system_id in unmapped_systems:
        issues.append(
            _issue(
                "warning",
                "UNMAPPED_SYSTEM",
                f"System {system_id} is not linked to any capability.",
                [system_id],
                "Link the system to one or more capabilities or mark it supportOnly.",
            )
        )

    invalid_cap_refs: list[tuple[str, str]] = []
    for step in flow_steps:
        for capability_id in step.get("capabilityIds", []):
            if capability_id not in capability_ids:
                invalid_cap_refs.append((step["id"], capability_id))
    for owner_id, capability_id in invalid_cap_refs:
        issues.append(
            _issue(
                "error",
                "MISSING_CAPABILITY_REFERENCE",
                f"{owner_id} references missing capability {capability_id}.",
                [owner_id, capability_id],
                "Create the capability or remove the bad reference.",
            )
        )

    flow_step_missing_actor_ids = [
        step["id"]
        for step in flow_steps
        if not step.get("actorId")
    ]
    for step_id in flow_step_missing_actor_ids:
        issues.append(
            _issue(
                "warning",
                "FLOW_STEP_MISSING_ACTOR",
                f"Flow step {step_id} does not identify an actor.",
                [step_id],
                "Add actorId for the flow step.",
            )
        )

    linked_capability_ids = set()
    for step in flow_steps:
        linked_capability_ids.update(step.get("capabilityIds", []))
    for system in systems:
        linked_capability_ids.update(system.get("capabilityIds", []))

    orphan_capability_ids = [
        capability["id"]
        for capability in capabilities
        if capability.get("id") and capability["id"] not in linked_capability_ids
    ]
    for capability_id in orphan_capability_ids:
        issues.append(
            _issue(
                "warning",
                "ORPHAN_CAPABILITY",
                f"Capability {capability_id} is not linked to any flow step or system.",
                [capability_id],
                "Link the capability to flow steps or supporting systems.",
            )
        )

    capability_map_view = next(
        (
            view
            for view in views
            if isinstance(view, dict)
            and view.get("type") == "business-capability-map"
        ),
        None,
    )
    capability_map_ids = set(capability_map_view.get("includedNodeIds", [])) if capability_map_view else set()
    for capability_id in linked_capability_ids:
        if capability_id not in capability_map_ids:
            issues.append(
                _issue(
                    "warning",
                    "CAPABILITY_MISSING_FROM_MAP",
                    f"Capability {capability_id} is used outside the map view but missing from the capability map.",
                    [capability_id],
                    "Include the capability in the business-capability-map view.",
                )
            )

    shared_capability_ids = {
        capability_id
        for capability_id in linked_capability_ids
        if any(capability_id in step.get("capabilityIds", []) for step in flow_steps)
        and any(capability_id in system.get("capabilityIds", []) for system in systems)
    }
    if flow_steps and systems and not shared_capability_ids:
        issues.append(
            _issue(
                "warning",
                "NO_SHARED_CAPABILITY_LINKAGE",
                "Flow and architecture views do not share any capability linkage.",
                [],
                "Link at least one capability across flow steps and systems.",
            )
        )

    summary = {
        "errorCount": sum(1 for issue in issues if issue["severity"] == "error"),
        "warningCount": sum(1 for issue in issues if issue["severity"] == "warning"),
        "infoCount": sum(1 for issue in issues if issue["severity"] == "info"),
        "capability_to_flow_coverage": 0
        if not flow_steps
        else round((len(flow_steps) - len(unmapped_flow_steps)) / len(flow_steps), 2),
        "capability_to_system_coverage": 0
        if not systems
        else round((len(systems) - len(unmapped_systems)) / len(systems), 2),
        "shared_capability_count": len(shared_capability_ids),
        "orphan_capability_count": len(orphan_capability_ids),
        "orphan_capability_ids": orphan_capability_ids,
        "flow_step_missing_actor_count": len(flow_step_missing_actor_ids),
        "flow_step_missing_actor_ids": flow_step_missing_actor_ids,
    }
    return {"summary": summary, "issues": issues}
