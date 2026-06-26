from __future__ import annotations

import json
from pathlib import Path

from business_blueprint.export_routes import resolve_export_route


ROOT = Path(__file__).resolve().parents[1]


def _load_fixture(name: str) -> dict:
    return json.loads((ROOT / "evals" / "fixtures" / name).read_text(encoding="utf-8"))


def test_resolve_export_route_defaults_to_freeflow_for_generic_blueprint() -> None:
    blueprint = _load_fixture("route-freeflow.json")

    decision = resolve_export_route(blueprint, requested_route=None)

    assert decision.route == "freeflow"
    assert decision.reason == "generic fallback"
    assert decision.fallback_route is None
    assert decision.terminal_behavior == "error"


def test_resolve_export_route_detects_architecture_template() -> None:
    blueprint = _load_fixture("route-architecture.json")

    decision = resolve_export_route(blueprint, requested_route=None)

    assert decision.route == "architecture-template"
    assert decision.fallback_route == "freeflow"


def test_resolve_export_route_detects_poster_for_layered_blueprint() -> None:
    blueprint = {
        "meta": {"title": "Layered"},
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [
                {"id": "sys-entry", "name": "Entry", "layer": "第一层 用户层"},
                {"id": "sys-harness", "name": "Harness", "layer": "第二层 支撑层"},
            ],
        },
    }

    decision = resolve_export_route(blueprint, requested_route=None)

    assert decision.route == "poster"
    assert decision.fallback_route == "freeflow"


def test_resolve_export_route_detects_evolution_from_dated_steps() -> None:
    blueprint = _load_fixture("route-evolution.json")

    decision = resolve_export_route(blueprint, requested_route=None)

    assert decision.route == "evolution"
    assert decision.fallback_route == "freeflow"
