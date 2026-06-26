import json
from pathlib import Path

from business_blueprint.projection import build_narrative_projection, default_projection_path


def test_default_projection_path_uses_blueprint_stem(tmp_path: Path) -> None:
    blueprint_path = tmp_path / "solution.blueprint.json"
    assert default_projection_path(blueprint_path) == tmp_path / "solution.projection.json"


def test_build_narrative_projection_returns_v1_contract(tmp_path: Path) -> None:
    blueprint = {
        "meta": {
            "title": "Retail Blueprint",
            "industry": "retail",
            "revisionId": "rev-20260420-01",
            "lastModifiedAt": "2026-04-20T12:00:00Z",
        },
        "context": {
            "goals": ["Reduce checkout queue time"],
            "scope": ["Store operations", "Member operations"],
            "assumptions": ["POS remains system of record"],
            "constraints": ["No ERP replacement in phase 1"],
            "clarifyRequests": [],
            "clarifications": [],
        },
        "library": {
            "capabilities": [
                {
                    "id": "cap-store",
                    "name": "Store Operations",
                    "description": "Run daily store operations",
                    "ownerActorIds": ["actor-manager"],
                    "supportingSystemIds": ["sys-pos"],
                }
            ],
            "actors": [{"id": "actor-manager", "name": "Store Manager"}],
            "flowSteps": [
                {
                    "id": "flow-checkout",
                    "name": "Checkout",
                    "actorId": "actor-manager",
                    "capabilityIds": ["cap-store"],
                    "systemIds": ["sys-pos"],
                    "stepType": "task",
                }
            ],
            "systems": [
                {
                    "id": "sys-pos",
                    "kind": "system",
                    "name": "POS",
                    "description": "Cashier system",
                    "capabilityIds": ["cap-store"],
                }
            ],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    projection = build_narrative_projection(
        blueprint,
        blueprint_path=tmp_path / "solution.blueprint.json",
    )

    assert projection["meta"]["adapterVersion"] == "v1"
    assert projection["summary"]["goals"] == ["Reduce checkout queue time"]
    assert projection["business"]["actors"][0]["storyRoles"] == ["operator"]
    assert projection["technology"]["systems"][0]["name"] == "POS"
    assert projection["provenance"]["blueprintPath"].endswith("solution.blueprint.json")
    assert projection["provenance"]["blueprintHash"]
    assert projection["diagnostics"]["warnings"] == []


def test_build_narrative_projection_emits_warning_for_missing_goals(tmp_path: Path) -> None:
    blueprint = {
        "meta": {"title": "Sparse Blueprint", "industry": "common", "revisionId": "rev-1"},
        "context": {"goals": [], "scope": [], "assumptions": [], "constraints": []},
        "library": {"capabilities": [], "actors": [], "flowSteps": [], "systems": []},
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    projection = build_narrative_projection(blueprint, blueprint_path=tmp_path / "solution.blueprint.json")

    assert projection["summary"]["goals"] == []
    assert projection["diagnostics"]["warnings"] == [
        {
            "field": "summary.goals",
            "severity": "warning",
            "message": "No explicit business goals found in blueprint context.",
        }
    ]
    # Ensure the result is serializable as the canonical file artifact.
    json.dumps(projection, ensure_ascii=False)
