from __future__ import annotations

import json
from pathlib import Path

import pytest

from engram_server import registry
from engram_server import server
from engram_server.server import main


class _FakeResponse:
    def __init__(self, payload: str):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload.encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *_args) -> None:
        return None


def test_fetch_registry_success(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = json.dumps([{"name": "fitness-coach", "source": "https://example.com/a.git"}])
    monkeypatch.setattr(registry, "urlopen", lambda *_args, **_kwargs: _FakeResponse(payload))

    entries = registry.fetch_registry()
    assert len(entries) == 1
    assert entries[0]["name"] == "fitness-coach"


def test_search_registry_fuzzy_match() -> None:
    entries = [
        {
            "name": "fitness-coach",
            "description": "训练计划与营养建议",
            "tags": ["fitness", "增肌"],
        },
        {
            "name": "language-partner",
            "description": "English and Japanese speaking practice",
            "tags": ["language", "conversation"],
        },
    ]

    zh_result = registry.search_registry("营养", entries)
    en_result = registry.search_registry("english", entries)
    tag_result = registry.search_registry("conversation", entries)

    assert [item["name"] for item in zh_result] == ["fitness-coach"]
    assert [item["name"] for item in en_result] == ["language-partner"]
    assert [item["name"] for item in tag_result] == ["language-partner"]


def test_search_registry_list_all_queries() -> None:
    entries = [
        {"name": "fitness-coach", "description": "训练计划", "tags": ["fitness"]},
        {"name": "language-partner", "description": "口语陪练", "tags": ["language"]},
    ]

    for query in ("all", "engram", "expert", "全部", ""):
        matched = registry.search_registry(query, entries)
        assert [item["name"] for item in matched] == [
            "fitness-coach",
            "language-partner",
        ]


def test_search_registry_multi_token_prefers_name_hits() -> None:
    entries = [
        {
            "name": "contract-lawyer",
            "description": "合同审查与条款风险识别",
            "tags": ["legal", "contract"],
        },
        {
            "name": "lawyer-helper",
            "description": "contract template and review",
            "tags": ["assistant"],
        },
    ]

    matched = registry.search_registry("contract lawyer", entries)
    assert [item["name"] for item in matched] == [
        "contract-lawyer",
        "lawyer-helper",
    ]


def test_load_registry_file_invalid_json_returns_empty(tmp_path: Path) -> None:
    broken = tmp_path / "registry.local.json"
    broken.write_text("{bad json", encoding="utf-8")
    assert registry.load_registry_file(broken) == []


def test_merge_registry_entries_allows_later_override() -> None:
    base = [
        {"name": "fitness-coach", "source": "https://example.com/base.git"},
        {"name": "lawyer", "source": "https://example.com/lawyer.git"},
    ]
    override = [
        {"name": "Fitness-Coach", "source": "https://example.com/override.git"},
    ]

    merged = registry.merge_registry_entries(base, override)
    assert len(merged) == 2
    assert registry.resolve_name("fitness-coach", merged) == "https://example.com/override.git"


def test_load_registry_entries_merges_local_overrides(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / ".claude" / "engram").mkdir(parents=True)
    monkeypatch.chdir(workspace)

    home_dir = tmp_path / "home"
    home_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))

    def fake_load_registry_file(path: Path | str) -> list[dict]:
        path_text = str(Path(path).expanduser())
        if path_text.endswith("registry.json"):
            return [{"name": "demo", "source": "built-in"}]
        if path_text.endswith(".engram/registry.local.json"):
            return [{"name": "demo", "source": "user-local"}]
        if path_text.endswith(".claude/engram/registry.local.json"):
            return [{"name": "demo", "source": "project-local"}]
        return []

    monkeypatch.setattr(server, "load_registry_file", fake_load_registry_file)
    monkeypatch.setattr(server, "fetch_registry", lambda: [{"name": "demo", "source": "remote"}])

    entries = server._load_registry_entries()
    assert registry.resolve_name("demo", entries) == "project-local"


def test_resolve_name_exact_and_missing() -> None:
    entries = [{"name": "fitness-coach", "source": "https://example.com/fitness.git"}]

    assert registry.resolve_name("fitness-coach", entries) == "https://example.com/fitness.git"
    assert registry.resolve_name("unknown", entries) is None


def test_install_subcommand_uses_registry_for_name(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "engram_server.server._install_engram_from_local_examples",
        lambda _name, _packs_dir: None,
    )
    monkeypatch.setattr(
        "engram_server.server._load_registry_entries",
        lambda: [{"name": "demo-pack", "source": "https://example.com/demo.git"}],
    )
    monkeypatch.setattr(
        "engram_server.server.install_engram_from_source",
        lambda source, _packs_dir: {"ok": True, "message": f"source={source}"},
    )

    main(["install", "demo-pack", "--packs-dir", str(tmp_path)])
    out = capsys.readouterr().out
    assert "source=https://example.com/demo.git" in out


def test_install_subcommand_keeps_url_branch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "engram_server.server._load_registry_entries",
        lambda: (_ for _ in ()).throw(AssertionError("registry should not be used")),
    )
    monkeypatch.setattr(
        "engram_server.server.install_engram_from_source",
        lambda source, _packs_dir: {"ok": True, "message": f"source={source}"},
    )

    main(["install", "https://example.com/direct.git", "--packs-dir", str(tmp_path)])
    out = capsys.readouterr().out
    assert "source=https://example.com/direct.git" in out


def test_install_subcommand_prefers_local_examples(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "engram_server.server._install_engram_from_local_examples",
        lambda _name, _packs_dir: {"ok": True, "message": "local-example-ok"},
    )
    monkeypatch.setattr(
        "engram_server.server._load_registry_entries",
        lambda: (_ for _ in ()).throw(AssertionError("registry should not be used")),
    )

    main(["install", "demo-pack", "--packs-dir", str(tmp_path)])
    out = capsys.readouterr().out
    assert "local-example-ok" in out


def test_install_subcommand_fallbacks_to_main_repo_examples_on_registry_clone_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "engram_server.server._install_engram_from_local_examples",
        lambda _name, _packs_dir: None,
    )
    monkeypatch.setattr(
        "engram_server.server._load_registry_entries",
        lambda: [{"name": "demo-pack", "source": "https://example.com/not-found.git"}],
    )
    monkeypatch.setattr(
        "engram_server.server.install_engram_from_source",
        lambda _source, _packs_dir: {"ok": False, "message": "安装失败：git clone 出错。404"},
    )
    monkeypatch.setattr(
        "engram_server.server._install_engram_from_main_repo_examples",
        lambda _name, _packs_dir: {"ok": True, "message": "安装成功：demo-pack - fallback"},
    )

    main(["install", "demo-pack", "--packs-dir", str(tmp_path)])
    out = capsys.readouterr().out
    assert "安装成功：demo-pack - fallback（已回退主仓库 examples）" in out


def test_search_subcommand_formats_matches(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "engram_server.server._load_registry_entries",
        lambda: [
            {
                "name": "fitness-coach",
                "description": "训练专家",
                "tags": ["fitness", "rehab"],
                "author": "engram-team",
            }
        ],
    )

    main(["search", "fit"])
    out = capsys.readouterr().out
    assert "fitness-coach - 训练专家 [fitness, rehab] (engram-team)" in out
