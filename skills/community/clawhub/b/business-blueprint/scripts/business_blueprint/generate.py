from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from clarify import build_clarify_requests
from model import load_json, new_revision_meta, write_json


_VALID_INDUSTRIES = frozenset({"common", "finance", "manufacturing", "retail"})


def load_seed(repo_root: Path, industry: str) -> dict[str, Any]:
    if industry not in _VALID_INDUSTRIES:
        raise ValueError(
            f"Unknown industry '{industry}'. "
            f"Valid choices: {sorted(_VALID_INDUSTRIES)}"
        )
    seed_path = repo_root / "business_blueprint" / "templates" / industry / "seed.json"
    return load_json(seed_path)


def load_industry_hints(repo_root: Path, industry: str) -> dict[str, Any] | None:
    """Load industry hints/checklist from seed template. Returns None if no hints."""
    seed = load_seed(repo_root, industry)
    return seed.get("industryHints")


def _build_views(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": "view-capability",
            "type": "business-capability-map",
            "title": "业务能力蓝图",
            "includedNodeIds": [entity["id"] for entity in blueprint["library"]["capabilities"]],
            "includedRelationIds": [],
            "layout": {"groups": []},
            "annotations": [],
        },
        {
            "id": "view-swimlane",
            "type": "swimlane-flow",
            "title": "泳道流程图",
            "includedNodeIds": [
                entity["id"]
                for entity in blueprint["library"]["actors"] + blueprint["library"]["flowSteps"]
            ],
            "includedRelationIds": [],
            "layout": {"lanes": [actor["id"] for actor in blueprint["library"]["actors"]]},
            "annotations": [],
        },
        {
            "id": "view-architecture",
            "type": "application-architecture",
            "title": "应用架构图",
            "includedNodeIds": [
                entity["id"]
                for entity in blueprint["library"]["systems"] + blueprint["library"]["capabilities"]
            ],
            "includedRelationIds": [],
            "layout": {"groups": []},
            "annotations": [],
        },
    ]


def create_blueprint_from_text(
    source_text: str,
    industry: str,
    repo_root: Path,
) -> dict[str, Any]:
    blueprint = deepcopy(load_seed(repo_root, industry))
    # Remove hints from output (they're for AI, not for the blueprint)
    blueprint.pop("industryHints", None)
    blueprint["meta"] = {
        "title": "Generated Blueprint",
        "industry": industry,
        **new_revision_meta(parent_revision_id=None, modified_by="ai"),
    }
    blueprint["context"]["sourceRefs"] = [{"type": "inline-text", "excerpt": source_text}]

    blueprint["views"] = _build_views(blueprint)
    blueprint["context"]["clarifyRequests"] = build_clarify_requests(blueprint)
    return blueprint


def write_plan_output(
    output_path: Path,
    source_text: str,
    industry: str,
    repo_root: Path,
) -> dict[str, Any]:
    blueprint = create_blueprint_from_text(source_text, industry, repo_root)
    write_json(output_path, blueprint)
    return blueprint
