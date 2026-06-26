from __future__ import annotations

import json
from pathlib import Path

import pytest

from business_blueprint.export_integrity import ExportIntegrityError, check_svg_definition_integrity, check_svg_geometry_integrity
from business_blueprint.export_svg import export_svg_auto


ROOT = Path(__file__).resolve().parents[1]


def _taxonomy_categories() -> set[str]:
    payload = json.loads((ROOT / "evals" / "defect-taxonomy.json").read_text(encoding="utf-8"))
    return set(payload["categories"])


def test_check_svg_definition_integrity_reports_missing_marker() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <line x1="0" y1="0" x2="10" y2="10" marker-end="url(#arrow-solid)"/>
    </svg>"""

    result = check_svg_definition_integrity(svg)

    assert result.errors == [
        {"kind": "defs_reference_missing", "ref": "arrow-solid"}
    ]
    assert result.errors[0]["kind"] in _taxonomy_categories()


def test_check_svg_definition_integrity_accepts_defined_marker() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <defs>
      <marker id="arrow-solid" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" />
    </defs>
    <line x1="0" y1="0" x2="10" y2="10" marker-end="url(#arrow-solid)"/>
    </svg>"""

    result = check_svg_definition_integrity(svg)

    assert result.errors == []


def test_check_svg_geometry_integrity_reports_canvas_overflow() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <rect x="10" y="80" width="20" height="30" />
    </svg>"""

    result = check_svg_geometry_integrity(svg)

    assert result.errors == [
        {"kind": "canvas_clipping", "axis": "y", "actual": 110.0, "limit": 100.0}
    ]
    assert result.errors[0]["kind"] in _taxonomy_categories()


def test_export_svg_auto_falls_back_when_primary_route_fails_integrity(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from business_blueprint import export_svg as export_svg_module

    target = tmp_path / "diagram.svg"
    blueprint = {
        "meta": {"title": "Timeline"},
        "library": {
            "capabilities": [],
            "actors": [{"id": "actor-1", "name": "Manager"}],
            "flowSteps": [
                {"id": "flow-1", "name": "2026-03-11：发布超级套件", "actorId": "actor-1"},
                {"id": "flow-2", "name": "2026-04-03：强化行业定位", "actorId": "actor-1"},
            ],
            "systems": [{"id": "sys-1", "name": "System"}],
        },
        "relations": [],
    }

    def fake_export_by_route(payload, path, *, route, theme, industry=None):
        if route == "evolution":
            path.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><line x1="0" y1="0" x2="10" y2="10" marker-end="url(#missing)"/></svg>',
                encoding="utf-8",
            )
        else:
            path.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><defs><marker id="arrow-solid" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" /></defs><rect x="10" y="10" width="20" height="20" /></svg>',
                encoding="utf-8",
            )

    monkeypatch.setattr(export_svg_module, "_export_by_route", fake_export_by_route)

    export_svg_auto(blueprint, target, theme="dark")

    svg = target.read_text(encoding="utf-8")
    assert 'url(#missing)' not in svg
    assert '<rect x="10" y="10" width="20" height="20"' in svg


def test_export_svg_auto_raises_structured_error_when_fallback_also_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from business_blueprint import export_svg as export_svg_module

    target = tmp_path / "diagram.svg"
    blueprint = {
        "meta": {"title": "Timeline"},
        "library": {
            "capabilities": [],
            "actors": [{"id": "actor-1", "name": "Manager"}],
            "flowSteps": [
                {"id": "flow-1", "name": "2026-03-11：发布超级套件", "actorId": "actor-1"},
                {"id": "flow-2", "name": "2026-04-03：强化行业定位", "actorId": "actor-1"},
            ],
            "systems": [{"id": "sys-1", "name": "System"}],
        },
        "relations": [],
    }

    def fake_export_by_route(payload, path, *, route, theme, industry=None):
        del payload, route, theme, industry
        path.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><line x1="0" y1="0" x2="10" y2="10" marker-end="url(#missing)"/></svg>',
            encoding="utf-8",
        )

    monkeypatch.setattr(export_svg_module, "_export_by_route", fake_export_by_route)

    with pytest.raises(ExportIntegrityError) as exc_info:
        export_svg_auto(blueprint, target, theme="dark")

    payload = exc_info.value.to_payload()
    assert payload["kind"] == "export_integrity_failure"
    assert payload["requestedRoute"] == "evolution"
    assert payload["attemptedRoute"] == "freeflow"
    assert payload["fallbackRoute"] == "freeflow"
    assert payload["terminalReason"] == "integrity_failed_after_fallback"
    assert payload["errors"][0]["kind"] in _taxonomy_categories()
