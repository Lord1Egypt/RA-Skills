from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from model import utc_now


def default_projection_path(blueprint_path: Path) -> Path:
    if blueprint_path.name.endswith(".blueprint.json"):
        return blueprint_path.with_name(
            blueprint_path.name.replace(".blueprint.json", ".projection.json")
        )
    return blueprint_path.with_name(f"{blueprint_path.stem}.projection.json")


def build_narrative_projection(
    blueprint: dict[str, Any],
    *,
    blueprint_path: Path | None = None,
) -> dict[str, Any]:
    meta = blueprint.get("meta", {})
    context = blueprint.get("context", {})
    library = blueprint.get("library", {})

    actors = {row["id"]: row for row in library.get("actors", []) if row.get("id")}
    systems = {row["id"]: row for row in library.get("systems", []) if row.get("id")}
    capabilities = library.get("capabilities", [])
    flow_steps = library.get("flowSteps", [])

    key_capabilities = [
        {
            "id": row["id"],
            "name": row["name"],
            "summary": row.get("description", ""),
            "ownerActors": [
                actors[actor_id]["name"]
                for actor_id in row.get("ownerActorIds", [])
                if actor_id in actors
            ],
            "supportingSystems": [
                systems[system_id]["name"]
                for system_id in row.get("supportingSystemIds", [])
                if system_id in systems
            ],
        }
        for row in capabilities
        if row.get("id") and row.get("name")
    ]

    projection = {
        "meta": {
            "adapterVersion": "v1",
            "title": meta.get("title", "Untitled Blueprint"),
            "industry": meta.get("industry", "common"),
            "revisionId": meta.get("revisionId"),
            "generatedAt": meta.get("lastModifiedAt") or utc_now(),
        },
        "summary": {
            "goals": context.get("goals", []),
            "scope": context.get("scope", []),
            "assumptions": context.get("assumptions", []),
            "constraints": context.get("constraints", []),
            "openQuestions": [
                row.get("question", "")
                for row in context.get("clarifyRequests", [])
                if row.get("question")
            ],
        },
        "business": {
            "capabilityGroups": _build_capability_groups(key_capabilities),
            "keyCapabilities": key_capabilities,
            "actors": [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "storyRoles": ["operator"],
                }
                for row in actors.values()
                if row.get("name")
            ],
            "coreFlows": _build_core_flows(flow_steps, actors, context),
        },
        "technology": {
            "systems": [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "kind": row.get("kind", "system"),
                    "summary": row.get("description", ""),
                    "supportsCapabilityIds": row.get("capabilityIds", []),
                }
                for row in systems.values()
                if row.get("name")
            ],
            "systemLandscapeSummary": "Systems supporting the capabilities captured in the blueprint library.",
        },
        "narrativeHints": {
            "keyProblems": context.get("constraints", []),
            "keyDesignChoices": context.get("assumptions", []),
            "narrativeAngles": [
                {
                    "name": "capability-transformation",
                    "summary": "Frame the blueprint as an operating-model and system-support transformation.",
                    "aiGenerated": True,
                    "sourceRefs": [
                        "context.goals",
                        "library.capabilities",
                        "library.flowSteps",
                    ],
                }
            ],
        },
        "provenance": {
            "blueprintPath": str(blueprint_path) if blueprint_path else "",
            "derivedFromRevisionId": meta.get("revisionId"),
            "blueprintHash": sha256(
                json.dumps(blueprint, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ).hexdigest(),
        },
        "diagnostics": {
            "warnings": [],
        },
    }

    if not projection["summary"]["goals"]:
        projection["diagnostics"]["warnings"].append(
            {
                "field": "summary.goals",
                "severity": "warning",
                "message": "No explicit business goals found in blueprint context.",
            }
        )

    return projection


def _build_capability_groups(
    key_capabilities: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not key_capabilities:
        return []
    return [
        {
            "name": "Core Capabilities",
            "capabilityIds": [row["id"] for row in key_capabilities],
            "summary": "Primary capabilities extracted from the blueprint library.",
        }
    ]


def _build_core_flows(
    flow_steps: list[dict[str, Any]],
    actors: dict[str, dict[str, Any]],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    if not flow_steps:
        return []

    first_step = flow_steps[0]
    return [
        {
            "name": "primary-flow",
            "goal": context.get("goals", [""])[0] if context.get("goals") else "",
            "primaryActor": actors.get(first_step.get("actorId", ""), {}).get("name", ""),
            "stepSummaries": [
                row["name"] for row in flow_steps if row.get("name")
            ],
            "capabilityIds": sorted(
                {
                    capability_id
                    for row in flow_steps
                    for capability_id in row.get("capabilityIds", [])
                }
            ),
            "systemIds": sorted(
                {
                    system_id
                    for row in flow_steps
                    for system_id in row.get("systemIds", [])
                }
            ),
        }
    ]
