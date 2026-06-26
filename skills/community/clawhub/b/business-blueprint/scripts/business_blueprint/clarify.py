from __future__ import annotations

from typing import Any


def build_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    library = blueprint.get("library", {})

    for system in library.get("systems", []):
        if system.get("resolution", {}).get("status") == "ambiguous":
            requests.append(
                {
                    "code": "AMBIGUOUS_SYSTEM",
                    "question": f"Please clarify whether '{system.get('name', '')}' refers to an existing canonical system or a distinct system.",
                    "affectedIds": [system["id"]],
                }
            )

    if not library.get("actors"):
        requests.append(
            {
                "code": "MISSING_PRIMARY_ACTOR",
                "question": "Which primary business actors should appear in the solution?",
                "affectedIds": [],
            }
        )

    if not library.get("capabilities"):
        requests.append(
            {
                "code": "MISSING_CAPABILITY",
                "question": "Which business capabilities must be represented in the blueprint?",
                "affectedIds": [],
            }
        )

    if library.get("capabilities") and not library.get("flowSteps"):
        requests.append(
            {
                "code": "MISSING_MAIN_FLOW",
                "question": "What is the main business flow that should be represented?",
                "affectedIds": [],
            }
        )

    if not library.get("systems"):
        requests.append(
            {
                "code": "MISSING_SYSTEM",
                "question": "Which existing or target systems should appear in the architecture?",
                "affectedIds": [],
            }
        )

    return requests
