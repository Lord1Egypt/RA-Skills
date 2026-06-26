from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from business_blueprint.export_svg import export_svg_auto
from business_blueprint.export_theme import C_DARK, C_LIGHT, resolve_theme
from business_blueprint.visual_profiles import (
    VISUAL_PROFILES,
    apply_visual_profile,
    resolve_visual_profile,
)
from business_blueprint.rule_engine import load_perspective


ROOT = Path(__file__).resolve().parents[1]


def _blueprint(industry: str = "retail") -> dict:
    return {
        "meta": {"title": "Profile Demo", "industry": industry},
        "library": {
            "capabilities": [{"id": "cap-order", "name": "订单履约"}],
            "actors": [{"id": "actor-user", "name": "用户"}],
            "flowSteps": [],
            "systems": [
                {"id": "sys-web", "name": "商城前端", "category": "frontend", "capabilityIds": ["cap-order"]},
                {"id": "sys-api", "name": "订单服务", "category": "backend", "capabilityIds": ["cap-order"]},
                {"id": "sys-db", "name": "订单库", "category": "database", "capabilityIds": ["cap-order"]},
            ],
        },
        "relations": [
            {"from": "sys-web", "to": "sys-api", "type": "flows-to", "label": "下单"},
            {"from": "sys-api", "to": "sys-db", "type": "depends-on", "label": "写入"},
        ],
        "views": [],
    }


def test_visual_profile_registry_contains_business_specific_profiles() -> None:
    assert {
        "executive-clean",
        "blueprint-technical",
        "dark-ops",
        "warm-consulting",
        "knowledge-canvas",
    } <= set(VISUAL_PROFILES)


def test_auto_profile_selects_knowledge_canvas_for_domain_knowledge() -> None:
    profile = resolve_visual_profile(
        "auto",
        industry="cross-border-ecommerce",
        blueprint_type="domain-knowledge",
        theme="dark",
    )

    assert profile.profile_id == "knowledge-canvas"


def test_apply_visual_profile_changes_palette_without_mutating_base() -> None:
    themed = apply_visual_profile(C_LIGHT, "warm-consulting", theme="light")

    assert themed["bg"] != C_LIGHT["bg"]
    assert C_LIGHT["bg"] == "#F8FAFC"
    assert themed["profile_id"] == "warm-consulting"
    assert themed["profile_label"] == VISUAL_PROFILES["warm-consulting"].label


def test_resolve_theme_accepts_visual_profile() -> None:
    themed = resolve_theme("dark", visual_profile="dark-ops")

    assert themed["profile_id"] == "dark-ops"
    assert themed["bg"] != C_DARK["bg"]


def test_export_svg_auto_embeds_visual_profile_metadata(tmp_path: Path) -> None:
    target = tmp_path / "profile.svg"

    export_svg_auto(_blueprint(), target, theme="light", visual_profile="warm-consulting")

    svg = target.read_text(encoding="utf-8")
    assert "visual-profile: warm-consulting" in svg
    assert VISUAL_PROFILES["warm-consulting"].palette["light"]["bg"] in svg


def test_strategy_registry_loads_utf8_json_on_windows() -> None:
    perspective = load_perspective("technical-architecture")

    assert perspective["strategyId"] == "technical-architecture"
    assert "rules" in perspective


def test_cli_accepts_visual_profile_for_html_export(tmp_path: Path) -> None:
    bp = tmp_path / "profile.blueprint.json"
    out = tmp_path / "profile.html"
    bp.write_text(json.dumps(_blueprint(), ensure_ascii=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "business_blueprint.cli",
            "--html",
            str(out),
            "--from",
            str(bp),
            "--visual-profile",
            "warm-consulting",
            "--theme",
            "light",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    html = out.read_text(encoding="utf-8")
    assert "visual-profile: warm-consulting" in html
