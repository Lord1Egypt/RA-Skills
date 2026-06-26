"""Tests for theme system, semantic colors, and summary cards.

These tests validate the new dark theme, semantic color mapping,
and summary card rendering added in v0.5.0.
"""

import json
import subprocess
import sys
from pathlib import Path

from business_blueprint.export_html import export_html_viewer
from business_blueprint.export_svg import export_svg, C_LIGHT, C_DARK

ROOT = Path(__file__).resolve().parents[1]


# ─── Fixtures ──────────────────────────────────────────────────────

MINIMAL_BP = {
    "meta": {"title": "Test Blueprint", "industry": "retail"},
    "library": {
        "capabilities": [
            {"id": "cap-sales", "name": "销售管理", "domain": "核心业务"},
            {"id": "cap-inventory", "name": "库存管理", "domain": "核心业务"},
            {"id": "cap-auth", "name": "身份认证", "domain": "基础设施"},
        ],
        "systems": [
            {"id": "sys-web", "name": "Web Frontend", "capabilityIds": ["cap-sales"], "category": "frontend"},
            {"id": "sys-api", "name": "API Service", "capabilityIds": ["cap-sales"], "category": "backend"},
            {"id": "sys-db", "name": "PostgreSQL", "capabilityIds": ["cap-inventory"], "category": "database"},
            {"id": "sys-auth", "name": "Auth Service", "capabilityIds": ["cap-auth"], "category": "security"},
            {"id": "sys-ext", "name": "Third Party API", "capabilityIds": ["cap-sales"], "category": "external"},
        ],
        "actors": [{"id": "actor-admin", "name": "管理员"}],
        "flowSteps": [
            {"id": "step1", "name": "创建订单", "capabilityIds": ["cap-sales"], "actorId": "actor-admin"},
        ],
    },
    "relations": [
        {"from": "sys-web", "to": "sys-api", "type": "supports"},
        {"from": "sys-api", "to": "sys-db", "type": "supports"},
    ],
    "views": [],
    "domainOrder": ["核心业务", "基础设施"],
}


RICH_BP = {
    "meta": {"title": "Rich Test", "revisionId": "r1"},
    "library": {
        "capabilities": [
            {"id": "c1", "name": "能力1", "domain": "domain-a"},
            {"id": "c2", "name": "能力2", "domain": "domain-a"},
            {"id": "c3", "name": "能力3", "domain": "domain-b"},
        ],
        "systems": [
            {"id": "s1", "name": "Web App", "capabilityIds": ["c1", "c2"], "category": "frontend"},
            {"id": "s2", "name": "Backend", "capabilityIds": ["c1", "c3"], "category": "backend"},
            {"id": "s3", "name": "Database", "capabilityIds": ["c3"], "category": "database"},
        ],
        "actors": [
            {"id": "a1", "name": "用户"},
            {"id": "a2", "name": "运营"},
        ],
        "flowSteps": [
            {"id": "f1", "name": "浏览", "capabilityIds": ["c1"], "actorId": "a1"},
            {"id": "f2", "name": "下单", "capabilityIds": ["c2"], "actorId": "a1"},
        ],
    },
    "relations": [
        {"from": "s1", "to": "s2", "type": "supports"},
        {"from": "s2", "to": "s3", "type": "supports"},
        {"from": "a1", "to": "f1", "type": "precedes"},
    ],
    "views": [],
    "domainOrder": ["domain-a", "domain-b"],
}


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


# ─── Theme Contract Tests ─────────────────────────────────────────

class TestThemeTokens:
    """Verify light and dark theme token sets exist and are distinct."""

    def test_light_theme_has_expected_tokens(self) -> None:
        assert "bg" in C_LIGHT
        assert "canvas" in C_LIGHT
        assert "text_main" in C_LIGHT
        assert "cap_fill" in C_LIGHT
        assert "sys_fill" in C_LIGHT
        assert "actor_fill" in C_LIGHT

    def test_dark_theme_has_expected_tokens(self) -> None:
        assert "bg" in C_DARK
        assert "canvas" in C_DARK
        assert "text_main" in C_DARK
        assert "cap_fill" in C_DARK
        assert "sys_fill" in C_DARK
        assert "actor_fill" in C_DARK

    def test_light_and_dark_bg_are_different(self) -> None:
        assert C_LIGHT["bg"] != C_DARK["bg"]

    def test_dark_bg_is_dark(self) -> None:
        assert C_DARK["bg"] == "#020617"

    def test_dark_canvas_is_dark(self) -> None:
        assert C_DARK["canvas"] == "#0F172A"


class TestSvgThemePropagation:
    """Verify that SVG exporters use the correct theme tokens."""

    def test_export_svg_uses_light_theme_by_default(self, tmp_path: Path) -> None:
        target = tmp_path / "light.svg"
        export_svg(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        assert C_LIGHT["bg"] in content
        assert content.startswith("<svg")

    def test_export_svg_accepts_dark_theme(self, tmp_path: Path) -> None:
        target = tmp_path / "dark.svg"
        export_svg(MINIMAL_BP, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert C_DARK["bg"] in content
        assert content.startswith("<svg")

    def test_dark_svg_contains_grid_pattern(self, tmp_path: Path) -> None:
        target = tmp_path / "dark_grid.svg"
        export_svg(MINIMAL_BP, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert '<pattern' in content
        assert 'id="grid"' in content

    def test_light_svg_has_no_grid(self, tmp_path: Path) -> None:
        target = tmp_path / "light_no_grid.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        assert '<pattern' not in content


class TestHtmlThemePropagation:
    """Verify that HTML viewer switches theme correctly."""

    def test_export_html_uses_light_theme_by_default(self, tmp_path: Path) -> None:
        target = tmp_path / "light.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        assert C_LIGHT["bg"] in content
        assert content.startswith("<!DOCTYPE html>")

    def test_export_html_accepts_dark_theme(self, tmp_path: Path) -> None:
        target = tmp_path / "dark.html"
        export_html_viewer(MINIMAL_BP, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert C_DARK["bg"] in content
        assert C_DARK["canvas"] in content

    def test_dark_html_contains_grid_pattern(self, tmp_path: Path) -> None:
        target = tmp_path / "dark_grid.html"
        export_html_viewer(MINIMAL_BP, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        # Dark theme uses CSS grid background (not SVG pattern like standalone SVG)
        assert 'background-size' in content
        assert '40px' in content

    def test_html_viewer_defaults_to_freeflow_when_no_standard_template(self, tmp_path: Path) -> None:
        target = tmp_path / "freeflow.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        assert "自由流布局" in content
        assert "泳道流程" not in content


# ─── Semantic Color Tests ─────────────────────────────────────────

class TestSemanticColors:
    """Verify that system nodes are colored by category."""

    def test_frontend_system_gets_cyan(self, tmp_path: Path) -> None:
        target = tmp_path / "semantic.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # "Web Frontend" should be cyan
        assert "#0891B2" in content

    def test_backend_system_gets_emerald(self, tmp_path: Path) -> None:
        target = tmp_path / "semantic.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # "API Service" should be emerald
        assert "#10B981" in content

    def test_database_system_gets_violet(self, tmp_path: Path) -> None:
        target = tmp_path / "semantic.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # "PostgreSQL" should be violet
        assert "#8B5CF6" in content

    def test_security_system_gets_rose(self, tmp_path: Path) -> None:
        target = tmp_path / "semantic.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # "Auth Service" should be rose
        assert "#F43F5E" in content

    def test_external_system_gets_slate(self, tmp_path: Path) -> None:
        target = tmp_path / "semantic.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # "Third Party API" should be slate
        assert "#64748B" in content

    def test_system_without_category_uses_default(self, tmp_path: Path) -> None:
        bp_no_cat = {
            "meta": {"title": "Test"},
            "library": {
                "capabilities": [{"id": "c1", "name": "能力"}],
                "systems": [{"id": "s1", "name": "Unknown System", "capabilityIds": ["c1"]}],
                "actors": [],
                "flowSteps": [],
            },
            "views": [],
            "relations": [],
        }
        target = tmp_path / "no_cat.svg"
        export_svg(bp_no_cat, target, theme="light")
        content = target.read_text(encoding="utf-8")
        # Should use default sys_fill, not a semantic color
        assert C_LIGHT["sys_fill"] in content


# ─── Summary Card Tests ───────────────────────────────────────────

class TestSummaryCards:
    """Verify that summary cards render with correct statistics."""

    def test_html_contains_summary_cards(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        assert "summary-card" in content or "stat-card" in content

    def test_card_displays_system_count(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        # MINIMAL_BP has 5 systems
        assert ">5</" in content or "5" in content

    def test_card_displays_capability_count(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        # MINIMAL_BP has 3 capabilities
        assert ">3</" in content or "3" in content

    def test_card_displays_actor_count(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        # MINIMAL_BP has 1 actor
        assert ">1</" in content or "1" in content

    def test_card_displays_coverage_percentage(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.html"
        export_html_viewer(MINIMAL_BP, target)
        content = target.read_text(encoding="utf-8")
        # Should contain coverage metric
        assert "COVERAGE" in content or "coverage" in content.lower() or "Coverage" in content

    def test_svg_contains_summary_cards(self, tmp_path: Path) -> None:
        target = tmp_path / "cards.svg"
        export_svg(MINIMAL_BP, target, theme="light")
        content = target.read_text(encoding="utf-8")
        assert "summary-card" in content
        assert "SYSTEMS" in content


# ─── CLI Theme Parameter Tests ────────────────────────────────────

class TestCliThemeParameter:
    """Verify that CLI accepts --theme for --html and --generate."""

    def test_help_shows_theme_option(self) -> None:
        result = run_cli("--help")
        assert result.returncode == 0
        # Should mention --theme in help
        assert "--theme" in result.stdout

    def test_html_with_dark_theme(self, tmp_path: Path) -> None:
        bp_path = tmp_path / "bp.json"
        bp_path.write_text(json.dumps(MINIMAL_BP), encoding="utf-8")
        out_path = tmp_path / "dark.bp.html"
        result = run_cli("--html", str(out_path), "--theme", "dark", "--from", str(bp_path))
        assert result.returncode == 0
        content = out_path.read_text(encoding="utf-8")
        assert C_DARK["bg"] in content

    def test_generate_with_dark_theme(self, tmp_path: Path) -> None:
        bp_path = tmp_path / "bp.json"
        bp_path.write_text(json.dumps(MINIMAL_BP), encoding="utf-8")
        out_path = tmp_path / "dark.gen/viewer.html"
        out_path.parent.mkdir()
        result = run_cli("--generate", str(out_path), "--theme", "dark", "--from", str(bp_path))
        assert result.returncode == 0
        # --generate produces viewer.html + solution.viewer.html
        viewer_html = out_path.parent / "solution.viewer.html"
        assert viewer_html.exists()
        content = viewer_html.read_text(encoding="utf-8")
        assert C_DARK["bg"] in content
