from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from support import load_skill_script


archive_sources = load_skill_script("archive_sources.py")
extract_sources = load_skill_script("extract_sources.py")


def test_archive_sources_defaults_to_dry_run(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "010 outbox" / "note.md"
    source.parent.mkdir(parents=True)
    source.write_text("---\ntags:\n  - LLM\n---\n\n# Title\n", encoding="utf-8")

    rows = archive_sources.archive_sources(vault, [source])

    archived = vault / "Archived" / "010 outbox" / "note.md"
    assert rows[0]["status"] == "planned"
    assert rows[0]["archived_path"] == str(archived)
    assert rows[0]["obsidian_link"] == "[[Archived/010 outbox/note.md|Archived/010 outbox/note.md]]"
    assert source.exists()
    assert not archived.exists()
    assert "archived" not in source.read_text(encoding="utf-8")


def test_archive_sources_execute_moves_under_archived_and_adds_tag(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "010 outbox" / "note.md"
    source.parent.mkdir(parents=True)
    source.write_text("---\ntags:\n  - LLM\n---\n\n# Title\n", encoding="utf-8")

    rows = archive_sources.archive_sources(vault, [source], execute=True)

    archived = vault / "Archived" / "010 outbox" / "note.md"
    assert rows[0]["status"] == "archived"
    assert not source.exists()
    assert archived.exists()
    archived_text = archived.read_text(encoding="utf-8")
    assert "  - LLM\n" in archived_text
    assert "  - archived\n" in archived_text


def test_legacy_dry_run_false_does_not_bypass_execute_gate(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "note.txt"
    vault.mkdir()
    source.write_text("source", encoding="utf-8")

    rows = archive_sources.archive_sources(vault, [source], False)

    assert rows[0]["status"] == "planned"
    assert source.exists()
    assert not (vault / "Archived" / "note.txt").exists()


def test_archive_cli_requires_execute_and_keeps_legacy_report_shape(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "notes" / "note.txt"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    report = tmp_path / "archive-map.json"

    result = subprocess.run(
        [
            sys.executable,
            str(archive_sources.__file__),
            "--vault-root",
            str(vault),
            "--map-output",
            str(report),
            str(source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert list(payload) == ["archives"]
    assert payload["archives"][0]["status"] == "planned"
    assert source.exists()


def test_archive_cli_execute_moves_source(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "notes" / "note.txt"
    source.parent.mkdir(parents=True)
    source.write_text("source", encoding="utf-8")
    report = tmp_path / "archive-map.json"

    result = subprocess.run(
        [
            sys.executable,
            str(archive_sources.__file__),
            "--vault-root",
            str(vault),
            "--map-output",
            str(report),
            "--execute",
            str(source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["archives"][0]["status"] == "archived"
    assert not source.exists()
    assert (vault / "Archived" / "notes" / "note.txt").exists()


def test_archive_sources_obsidian_heading_link(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    archived = vault / "Archived" / "note.md"
    link = archive_sources.obsidian_heading_link(archived, vault, "原始标题", "note#原始标题")

    assert link == "[[Archived/note.md#原始标题|note#原始标题]]"


def test_extract_collect_sources_skips_archived_dir_and_tag(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    included = vault / "notes" / "keep.md"
    archived_tag = vault / "notes" / "old.md"
    archived_dir = vault / "Archived" / "notes" / "older.md"
    included.parent.mkdir(parents=True)
    archived_dir.parent.mkdir(parents=True)
    included.write_text("---\ntags:\n  - LLM\n---\n\n# Keep\n", encoding="utf-8")
    archived_tag.write_text("---\ntags:\n  - archived\n---\n\n# Old\n", encoding="utf-8")
    archived_dir.write_text("# Older\n", encoding="utf-8")

    assert extract_sources.collect_sources([vault]) == [included]
