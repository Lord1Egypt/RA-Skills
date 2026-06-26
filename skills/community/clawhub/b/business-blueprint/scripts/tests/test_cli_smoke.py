import subprocess
import sys
from pathlib import Path

import pytest

from business_blueprint.export_integrity import ExportIntegrityError, ExportIntegrityFailure


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_help_lists_supported_commands() -> None:
    result = run_cli("--help")
    assert result.returncode == 0
    assert "--plan" in result.stdout
    assert "--project" in result.stdout
    assert "--generate" in result.stdout
    assert "--validate" in result.stdout


def test_cli_export_returns_structured_diagnostics_on_integrity_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from business_blueprint import cli as cli_module

    blueprint = tmp_path / "solution.blueprint.json"
    blueprint.write_text(
        '{"meta":{"title":"Broken"},"library":{"capabilities":[],"actors":[],"flowSteps":[],"systems":[]},"relations":[]}',
        encoding="utf-8",
    )

    def fake_export_svg_auto(*args, **kwargs):
        del args, kwargs
        raise ExportIntegrityError(
            ExportIntegrityFailure(
                requested_route="poster",
                attempted_route="freeflow",
                fallback_route="freeflow",
                terminal_reason="integrity_failed_after_fallback",
                errors=[{"kind": "canvas_clipping", "axis": "y", "actual": 110.0, "limit": 100.0}],
            )
        )

    monkeypatch.setattr(cli_module, "export_svg_auto", fake_export_svg_auto)
    monkeypatch.setattr(cli_module.sys, "argv", ["business-blueprint", "--export", str(blueprint)])

    exit_code = cli_module.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert '"kind": "export_integrity_failure"' in captured.err
    assert '"terminalReason": "integrity_failed_after_fallback"' in captured.err


# ── Prompt file generation (Phase 1) ──────────────────────────

_MINIMAL_BLUEPRINT = (
    '{"version":"1.0","meta":{"title":"Test","industry":"common","version":"1.0"},'
    '"library":{"capabilities":[],"actors":[],"flowSteps":[],"systems":[]},'
    '"relations":[]}'
)


def test_cli_export_generates_prompt_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from business_blueprint import cli as cli_module

    bp = tmp_path / "solution.blueprint.json"
    bp.write_text(_MINIMAL_BLUEPRINT, encoding="utf-8")

    monkeypatch.setattr(cli_module, "export_svg_auto", lambda *a, **k: None)
    monkeypatch.setattr(cli_module, "export_html_viewer", lambda *a, **k: None)
    monkeypatch.setattr(cli_module.sys, "argv", ["bb", "--export", str(bp)])

    exit_code = cli_module.main()
    assert exit_code == 0

    export_dir = tmp_path / "solution.exports"
    prompt_files = list(export_dir.glob("generation-prompt-*.md"))
    assert len(prompt_files) == 1
    content = prompt_files[0].read_text()
    assert "## Provenance" in content
    assert "## Export Configuration" in content


def test_cli_export_drawio_generates_prompt_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from business_blueprint import cli as cli_module

    bp = tmp_path / "solution.blueprint.json"
    bp.write_text(_MINIMAL_BLUEPRINT, encoding="utf-8")

    monkeypatch.setattr(cli_module, "export_drawio", lambda *a, **k: None)
    monkeypatch.setattr(cli_module.sys, "argv", ["bb", "--export", str(bp), "--format", "drawio"])

    exit_code = cli_module.main()
    assert exit_code == 0

    export_dir = tmp_path / "solution.exports"
    prompt_files = list(export_dir.glob("generation-prompt-*.md"))
    assert len(prompt_files) == 1
    content = prompt_files[0].read_text()
    assert "**Format**: drawio" in content


def test_cli_export_auto_generates_prompt_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from business_blueprint import cli as cli_module

    bp = tmp_path / "solution.blueprint.json"
    bp.write_text(_MINIMAL_BLUEPRINT, encoding="utf-8")

    monkeypatch.setattr(cli_module, "export_svg", lambda *a, **k: None)
    monkeypatch.setattr(cli_module, "export_html_viewer", lambda *a, **k: None)
    monkeypatch.setattr(cli_module.sys, "argv", ["bb", "--export-auto", str(bp)])

    exit_code = cli_module.main()
    assert exit_code == 0

    export_dir = tmp_path / "solution.exports"
    if not export_dir.exists():
        # --export-auto uses stem.exports = {bp_stem}.exports
        export_dir = tmp_path / f"{bp.stem}.exports"
    prompt_files = list(export_dir.glob("generation-prompt-*.md"))
    assert len(prompt_files) == 1, f"No prompt files in {export_dir}; contents: {list(export_dir.iterdir()) if export_dir.exists() else 'dir missing'}"
    content = prompt_files[0].read_text()
    assert "**Format**: auto-svg" in content


def test_cli_html_generates_prompt_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from business_blueprint import cli as cli_module

    bp = tmp_path / "solution.blueprint.json"
    bp.write_text(_MINIMAL_BLUEPRINT, encoding="utf-8")
    html_out = tmp_path / "output.html"

    monkeypatch.setattr(cli_module, "export_html_viewer", lambda *a, **k: None)
    monkeypatch.setattr(cli_module.sys, "argv", ["bb", "--html", str(html_out), "--from", str(bp)])

    exit_code = cli_module.main()
    assert exit_code == 0

    prompt_files = list(tmp_path.glob("generation-prompt-*.md"))
    assert len(prompt_files) == 1
    content = prompt_files[0].read_text()
    assert "**Format**: html" in content
