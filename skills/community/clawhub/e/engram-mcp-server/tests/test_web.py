from __future__ import annotations

import json
from pathlib import Path

from engram_server.web import _build_loader


def _create_minimal_engram(root: Path, name: str) -> None:
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(
        json.dumps({"name": name, "description": f"{name} description"}),
        encoding="utf-8",
    )


def test_web_loader_uses_project_engram_only_when_available(
    tmp_path: Path, monkeypatch
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    project_packs = workspace / ".claude" / "engram"
    project_packs.mkdir(parents=True)
    _create_minimal_engram(project_packs, "project-only")

    configured = tmp_path / "configured"
    configured.mkdir()
    _create_minimal_engram(configured, "configured-only")

    monkeypatch.chdir(workspace)
    loader = _build_loader(configured)

    assert loader.packs_dirs == [project_packs.resolve()]
    assert loader.packs_dir == project_packs.resolve()
    names = [item["name"] for item in loader.list_engrams()]
    assert names == ["project-only"]


def test_web_loader_falls_back_to_configured_dir(
    tmp_path: Path, monkeypatch
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    configured = tmp_path / "configured"
    configured.mkdir()
    _create_minimal_engram(configured, "configured-only")

    monkeypatch.chdir(workspace)
    loader = _build_loader(configured)

    assert loader.packs_dirs == [configured.resolve()]
    assert loader.packs_dir == configured.resolve()
    names = [item["name"] for item in loader.list_engrams()]
    assert names == ["configured-only"]
