from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = PACKAGE_ROOT / "skills" / "kb-review" / "SKILL.md"
SCRIPT_PATH = SKILL_PATH.parent / "scripts" / "kb_review.py"
SPEC = importlib.util.spec_from_file_location("kb_review", SCRIPT_PATH)
assert SPEC is not None
kb_review = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(kb_review)


def write_review_file(path: Path, rows: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "| index | decision | confidence | title | reason | source_path |",
                "| --- | --- | --- | --- | --- | --- |",
                *rows,
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_duplicates_file(path: Path, rows: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "| duplicate_group | index | decision | confidence | title | reason | source_path |",
                "| --- | --- | --- | --- | --- | --- | --- |",
                *rows,
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_execution_log(path: Path, rows: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "# Trash Execution Log",
                "",
                f"- rows: {len(rows)}",
                "",
                "| status | duplicate_group | decision | confidence | title | source_path | trash_path | executed_at | note | pruned_dirs |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                *rows,
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_source_path_cell_parses_plain_markdown_and_angle_markdown_links(tmp_path: Path) -> None:
    plain = tmp_path / "plain.md"
    linked = tmp_path / "linked.md"
    spaced = tmp_path / "path with spaces" / "note.md"

    assert kb_review.source_path_from_cell(str(plain), tmp_path) == plain.resolve(strict=False)
    assert kb_review.source_path_from_cell(f"[Linked]({linked})", tmp_path) == linked.resolve(strict=False)
    assert kb_review.source_path_from_cell(f"[Spaced](<{spaced}>)", tmp_path) == spaced.resolve(strict=False)


def test_source_path_cell_parses_obsidian_wikilinks(tmp_path: Path) -> None:
    vault = tmp_path / "Obsidian Vault"
    review_dir = vault / "Flomo" / "KB-Review-test"
    source = vault / "Flomo" / "AI" / "Agent.agent.md"
    (vault / ".obsidian").mkdir(parents=True)
    review_dir.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    source.write_text("# Agent\n", encoding="utf-8")

    assert (
        kb_review.source_path_from_cell("[[Flomo/AI/Agent.agent.md]]", review_dir)
        == source.resolve(strict=False)
    )
    assert (
        kb_review.source_path_from_cell("[[Flomo/AI/Agent.agent\\|AI/Agent.agent.md]]", review_dir)
        == source.resolve(strict=False)
    )


def test_review_table_parses_obsidian_wikilinks_with_escaped_alias_pipe(tmp_path: Path) -> None:
    vault = tmp_path / "Obsidian Vault"
    review_dir = vault / "Flomo" / "KB-Review-test"
    source = vault / "Flomo" / "AI" / "Agent.agent.md"
    (vault / ".obsidian").mkdir(parents=True)
    review_dir.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    source.write_text("# Agent\n", encoding="utf-8")
    write_review_file(
        review_dir / "delete.md",
        ["| 1 | 0 | 3 | Agent | reason | [[Flomo/AI/Agent.agent\\|AI/Agent.agent.md]] |"],
    )

    rows = kb_review.read_review_table(review_dir / "delete.md")

    assert len(rows) == 1
    assert rows[0]["source_path"] == str(source.resolve(strict=False))


def test_delete_moves_only_decision_zero_rows_to_home_trash_and_prunes_empty_parents(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    source_root = tmp_path / "source"
    delete_source = source_root / "nested" / "delete.md"
    keep_source = source_root / "keep.md"
    delete_source.parent.mkdir(parents=True)
    delete_source.write_text("# Delete\n", encoding="utf-8")
    keep_source.write_text("# Keep\n", encoding="utf-8")

    review_dir = source_root / "KB-Review-test"
    review_dir.mkdir()
    write_review_file(
        review_dir / "keep.md",
        [f"| 1 | 1 | 3 | Keep | keep reason | {keep_source} |"],
    )
    write_review_file(
        review_dir / "delete.md",
        [f"| 1 | 0 | 3 | Delete | delete reason | {delete_source} |"],
    )

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=source_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=home / ".Trash",
        execute=True,
    )

    moved_rows = [row for row in rows if row["status"] == "moved-to-trash"]
    assert [row["source_path"] for row in moved_rows] == [str(delete_source)]
    assert moved_rows[0]["trash_path"] == str(home / ".Trash" / "delete.md")
    assert not delete_source.exists()
    assert (home / ".Trash" / "delete.md").read_text(encoding="utf-8") == "# Delete\n"
    assert keep_source.exists()
    assert not (source_root / "nested").exists()
    assert "nested" in moved_rows[0]["pruned_dirs"]
    assert "moved-to-trash" in (review_dir / "trash-execution-log.md").read_text(encoding="utf-8")


def test_delete_prunes_parents_that_only_contain_macos_metadata(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    source_root = tmp_path / "source"
    source = source_root / "notion-export" / "workspace" / "note.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Delete\n", encoding="utf-8")
    (source_root / ".DS_Store").write_text("", encoding="utf-8")
    (source_root / "notion-export" / ".DS_Store").write_text("", encoding="utf-8")
    (source_root / "notion-export" / "workspace" / ".DS_Store").write_text("", encoding="utf-8")

    review_dir = source_root / "KB-Review-test"
    review_dir.mkdir()
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Delete | reason | {source} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=source_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=home / ".Trash",
        execute=True,
    )

    assert not (source_root / "notion-export").exists()
    assert source_root.exists()
    assert "notion-export" in rows[0]["pruned_dirs"]


def test_delete_does_not_prune_parents_for_missing_source_rows(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    source_root = tmp_path / "source"
    missing = source_root / "Users" / "example-user" / "missing.md"
    missing.parent.mkdir(parents=True)
    (source_root / "Users" / ".DS_Store").write_text("", encoding="utf-8")
    (source_root / "Users" / "example-user" / ".DS_Store").write_text("", encoding="utf-8")

    review_dir = tmp_path / "review"
    review_dir.mkdir()
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Missing | reason | {missing} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=home / ".Trash",
        execute=True,
    )

    assert rows[0]["status"] == "missing-source"
    assert (source_root / "Users").exists()
    assert rows[0]["pruned_dirs"] == ""


def test_delete_dry_run_writes_planned_action_without_moving_or_pruning(tmp_path: Path, monkeypatch) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    source = tmp_path / "source" / "nested" / "delete.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Delete\n", encoding="utf-8")

    review_dir = tmp_path / "review"
    review_dir.mkdir()
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Delete | reason | {source} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=home / ".Trash",
    )

    assert [row["status"] for row in rows] == ["planned-trash"]
    assert source.exists()
    assert source.parent.exists()
    assert not (home / ".Trash" / "delete.md").exists()


def test_force_delete_path_contains_overrides_keep_decision(tmp_path: Path, monkeypatch) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    source = tmp_path / "source" / "obsolete" / "keep.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Force delete\n", encoding="utf-8")

    review_dir = tmp_path / "review"
    review_dir.mkdir()
    write_review_file(review_dir / "keep.md", [f"| 1 | 1 | 3 | Keep | reason | {source} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=["obsolete"],
        trash_dir=home / ".Trash",
        execute=True,
    )

    assert [row["status"] for row in rows] == ["moved-to-trash"]
    assert rows[0]["decision"] == "1"
    assert "force-delete-path-component=obsolete" in rows[0]["note"]
    assert not source.exists()
    assert (home / ".Trash" / "keep.md").exists()


def test_delete_records_missing_source_without_failing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    missing = tmp_path / "missing.md"
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Missing | reason | {missing} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=tmp_path / "home" / ".Trash",
        execute=True,
    )

    assert [row["status"] for row in rows] == ["missing-source"]


def test_rollback_restores_moved_to_trash_and_legacy_trashed_rows(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    trash_dir = tmp_path / "trash"
    review_dir.mkdir()
    trash_dir.mkdir()
    first_trash = trash_dir / "first.md"
    second_trash = trash_dir / "second.md"
    first_source = tmp_path / "source" / "first.md"
    second_source = tmp_path / "source" / "nested" / "second.md"
    first_trash.write_text("# First\n", encoding="utf-8")
    second_trash.write_text("# Second\n", encoding="utf-8")
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | First | {first_source} | {first_trash} | 2026-05-07T00:00:00 | reason |  |",
            f"| trashed |  | 0 | 3 | Second | {second_source} | {second_trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    rows = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=trash_dir,
        execute=True,
    )

    assert [row["status"] for row in rows] == ["restored", "restored"]
    assert first_source.read_text(encoding="utf-8") == "# First\n"
    assert second_source.read_text(encoding="utf-8") == "# Second\n"
    assert not first_trash.exists()
    assert not second_trash.exists()
    assert "trash-rollback-log.md" in str(review_dir / "trash-rollback-log.md")


def test_rollback_restores_renamed_when_source_path_already_exists(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(kb_review, "timestamp_for_path", lambda: "20260507-010203")
    review_dir = tmp_path / "review"
    trash_dir = tmp_path / "trash"
    review_dir.mkdir()
    trash_dir.mkdir()
    source = tmp_path / "source" / "note.md"
    trash = trash_dir / "note.md"
    source.parent.mkdir()
    source.write_text("# Existing\n", encoding="utf-8")
    trash.write_text("# Restored\n", encoding="utf-8")
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | Note | {source} | {trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    rows = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=trash_dir,
        execute=True,
    )

    renamed = source.parent / "note.restored-20260507-010203.md"
    assert [row["status"] for row in rows] == ["restored-renamed-conflict"]
    assert rows[0]["restored_path"] == str(renamed)
    assert source.read_text(encoding="utf-8") == "# Existing\n"
    assert renamed.read_text(encoding="utf-8") == "# Restored\n"
    assert not trash.exists()


def test_rollback_missing_trash_is_reported_without_failing(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    source = tmp_path / "source.md"
    trash = tmp_path / "trash" / "missing.md"
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | Missing | {source} | {trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    rows = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=tmp_path / "trash",
        execute=True,
    )

    assert [row["status"] for row in rows] == ["missing-trash"]
    assert rows[0]["note"] == (
        "trash_path does not exist; rollback is unavailable / "
        "trash_path 不存在；无法回退"
    )
    rollback_report = (review_dir / "trash-rollback-log.md").read_text(encoding="utf-8")
    assert rollback_report.startswith(
        "# Trash Rollback Log / 回收站回退日志\n\n- rows / 行数: 1\n"
    )


def test_rollback_dry_run_writes_planned_without_moving_or_creating_dirs(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    trash_dir = tmp_path / "trash"
    review_dir.mkdir()
    trash_dir.mkdir()
    source = tmp_path / "source" / "note.md"
    trash = trash_dir / "note.md"
    trash.write_text("# Note\n", encoding="utf-8")
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | Note | {source} | {trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    rows = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=trash_dir,
    )

    assert [row["status"] for row in rows] == ["planned-restore"]
    assert trash.exists()
    assert not source.exists()
    assert not source.parent.exists()


def test_repeated_rollback_reports_missing_trash_after_first_restore(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    trash_dir = tmp_path / "trash"
    review_dir.mkdir()
    trash_dir.mkdir()
    source = tmp_path / "source" / "note.md"
    trash = trash_dir / "note.md"
    trash.write_text("# Note\n", encoding="utf-8")
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | Note | {source} | {trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    first = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=trash_dir,
        execute=True,
    )
    second = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=tmp_path,
        trash_dir=trash_dir,
        execute=True,
    )

    assert [row["status"] for row in first] == ["restored"]
    assert [row["status"] for row in second] == ["missing-trash"]


def test_help_and_unknown_arguments_do_not_create_reports(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    review_dir.mkdir()

    help_result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        check=False,
        text=True,
        capture_output=True,
    )
    unknown_result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--review-dir", str(review_dir), "--rebuild"],
        check=False,
        text=True,
        capture_output=True,
    )

    assert help_result.returncode == 0
    assert "--rollback" in help_result.stdout
    assert "--review-root" in help_result.stdout
    assert "--execute" in help_result.stdout
    assert "--rebuild" not in help_result.stdout
    assert unknown_result.returncode != 0
    assert not (review_dir / "trash-execution-log.md").exists()
    assert not (review_dir / "trash-rollback-log.md").exists()


def test_read_all_review_rows_includes_duplicates_with_extra_group_column(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")

    review_dir = tmp_path / "review"
    review_dir.mkdir()
    write_duplicates_file(
        review_dir / "duplicates.md",
        [f"| dup-001 | 1 | 0 | 3 | Source | duplicate copy | {source} |"],
    )

    rows = kb_review.read_all_review_rows(review_dir)

    assert len(rows) == 1
    assert rows[0]["review_file"] == "duplicates.md"
    assert rows[0]["duplicate_group"] == "dup-001"
    assert rows[0]["source_path"] == str(source)


def test_default_scan_excludes_generated_backup_config_trash_and_attachment_paths(tmp_path: Path) -> None:
    source_root = tmp_path / "vault"
    included = source_root / "notes" / "keep.md"
    excluded = [
        source_root / "KB-Review-2026-05-06" / "keep.md",
        source_root / "KB-Refactor-2026-05-06" / "keep.md",
        source_root / "AI-Era-2026-05-06" / "backup.md",
        source_root / ".obsidian" / "workspace.json",
        source_root / ".trash" / "deleted.md",
        source_root / ".smart-env" / "cache.md",
        source_root / "Archived" / "old.md",
        source_root / "Attachment" / "image.png",
        source_root / "notes" / "Attachment.png",
        source_root / "attachments" / "scan.md",
        source_root / "notes" / "Attachments" / "diagram.png",
    ]
    included.parent.mkdir(parents=True)
    included.write_text("# Keep\n", encoding="utf-8")
    for path in excluded:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("excluded\n", encoding="utf-8")

    candidates = kb_review.iter_scan_candidates(source_root)

    assert candidates == [included]
    assert not kb_review.is_scan_excluded(included, source_root)
    assert all(kb_review.is_scan_excluded(path, source_root) for path in excluded)


def test_scan_exclusion_allows_extra_patterns(tmp_path: Path) -> None:
    source_root = tmp_path / "vault"
    normal = source_root / "notes" / "keep.md"
    draft = source_root / "drafts" / "skip.md"
    normal.parent.mkdir(parents=True)
    draft.parent.mkdir(parents=True)
    normal.write_text("# Keep\n", encoding="utf-8")
    draft.write_text("# Skip\n", encoding="utf-8")

    candidates = kb_review.iter_scan_candidates(source_root, extra_excluded_patterns=["drafts"])

    assert candidates == [normal]
    assert kb_review.is_scan_excluded(draft, source_root, extra_patterns=["drafts"])


def test_default_scan_excludes_archived_frontmatter_tag(tmp_path: Path) -> None:
    source_root = tmp_path / "vault"
    normal = source_root / "notes" / "keep.md"
    archived = source_root / "notes" / "old.md"
    normal.parent.mkdir(parents=True)
    normal.write_text("---\ntags:\n  - LLM\n---\n\n# Keep\n", encoding="utf-8")
    archived.write_text("---\ntags:\n  - archived\n---\n\n# Old\n", encoding="utf-8")

    candidates = kb_review.iter_scan_candidates(source_root)

    assert candidates == [normal]
    assert kb_review.scan_excluded_tag_hits(archived) == ["archived"]


def test_second_brain_coverage_matches_sibling_agent_doc_and_skips_archived(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    index = tmp_path / "documents.jsonl"
    agent_doc = vault / "notes" / "source.agent.md"
    raw_doc = vault / "notes" / "source.md"
    archived_raw = vault / "Archived" / "notes" / "source.md"
    agent_doc.parent.mkdir(parents=True)
    raw_doc.write_text("# Raw\n", encoding="utf-8")
    archived_raw.parent.mkdir(parents=True)
    archived_raw.write_text("# Archived\n", encoding="utf-8")
    index.write_text(
        json.dumps(
            {
                "record_id": "doc:notes/source.agent.md",
                "record_type": "document",
                "path": "notes/source.agent.md",
                "title": "Source",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    records = kb_review.load_second_brain_records(index)
    raw_coverage = kb_review.second_brain_coverage_for_path(raw_doc, vault, records)
    archived_coverage = kb_review.second_brain_coverage_for_path(archived_raw, vault, records)

    assert raw_coverage["status"] == "covered-by-agent-doc"
    assert raw_coverage["agent_path"] == "notes/source.agent.md"
    assert archived_coverage["status"] == "skipped-archived"
    assert archived_coverage["agent_path"] == ""


def test_second_brain_coverage_report_for_review_rows(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    source = vault / "notes" / "source.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Raw\n", encoding="utf-8")
    review_dir = vault / "KB-Review-test"
    review_dir.mkdir()
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Source | reason | {source} |"])
    index = tmp_path / "documents.jsonl"
    index.write_text(
        json.dumps(
            {
                "record_id": "doc:notes/source.agent.md",
                "record_type": "document",
                "path": "notes/source.agent.md",
                "title": "Source Agent",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    rows = kb_review.write_second_brain_coverage_report(review_dir, index, vault)

    assert rows[0]["status"] == "covered-by-agent-doc"
    assert rows[0]["agent_path"] == "notes/source.agent.md"
    report = (review_dir / "second-brain-coverage.md").read_text(encoding="utf-8")
    assert "covered-by-agent-doc" in report
    assert "notes/source.agent.md" in report
    assert rows[0]["note"] == (
        "A matching .agent.md is indexed by SecondBrain / "
        "匹配的 .agent.md 已被 SecondBrain 索引"
    )
    assert report.startswith(
        "# Second Brain Coverage / 第二大脑覆盖情况\n\n- rows / 行数: 1\n"
    )


def test_skill_frontmatter_declares_public_release_without_user_invocable() -> None:
    frontmatter = SKILL_PATH.read_text(encoding="utf-8").split("---", 2)[1]

    assert "user-invocable" not in frontmatter
    assert "metadata:" in frontmatter
    assert 'version: "0.2.0"' in frontmatter


def test_second_brain_index_defaults_to_nested_sibling_and_supports_overrides(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.delenv("KB_REVIEW_PACKAGE_ROOT", raising=False)
    monkeypatch.delenv("KB_REVIEW_SECOND_BRAIN_INDEX", raising=False)

    expected_nested = (
        SCRIPT_PATH.parents[2]
        / "second-brain"
        / "references"
        / "generated"
        / "documents.jsonl"
    )
    assert kb_review.default_second_brain_index() == expected_nested

    package_root = tmp_path / "suite"
    monkeypatch.setenv("KB_REVIEW_PACKAGE_ROOT", str(package_root))
    assert kb_review.default_second_brain_index() == (
        package_root / "skills" / "second-brain" / "references" / "generated" / "documents.jsonl"
    )

    explicit_index = tmp_path / "indexes" / "documents.jsonl"
    monkeypatch.setenv("KB_REVIEW_SECOND_BRAIN_INDEX", str(explicit_index))
    assert kb_review.default_second_brain_index() == explicit_index


def test_delete_is_preview_by_default_and_execute_gate_enables_mutation(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    source = review_root / "notes" / "delete.md"
    review_dir = review_root / "KB-Review-test"
    trash_dir = tmp_path / "portable-trash"
    source.parent.mkdir(parents=True)
    review_dir.mkdir()
    source.write_text("# Delete\n", encoding="utf-8")
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Delete | reason | {source} |"])

    preview_rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=review_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=trash_dir,
    )

    assert [row["status"] for row in preview_rows] == ["planned-trash"]
    assert source.exists()

    executed_rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=review_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=trash_dir,
        execute=True,
    )

    assert [row["status"] for row in executed_rows] == ["moved-to-trash"]
    assert not source.exists()
    assert (trash_dir / "delete.md").exists()


def test_delete_skips_paths_outside_explicit_review_root(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    review_dir = review_root / "KB-Review-test"
    outside = tmp_path / "outside.md"
    review_dir.mkdir(parents=True)
    outside.write_text("# Outside\n", encoding="utf-8")
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Outside | reason | {outside} |"])

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=review_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=tmp_path / "trash",
        execute=True,
    )

    assert [row["status"] for row in rows] == ["skipped-outside-review-root"]
    assert outside.exists()


def test_force_delete_matches_whole_path_components_only(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    exact = review_root / "obsolete" / "note.md"
    substring = review_root / "not-obsolete" / "note.md"

    assert kb_review.should_force_delete(exact, review_root, ["obsolete"]) == "obsolete"
    assert kb_review.should_force_delete(substring, review_root, ["obsolete"]) == ""

    for unsafe in ("../outside", "/absolute", "C:/absolute", "obsolete/*"):
        try:
            kb_review.validate_force_delete_patterns([unsafe])
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe force-delete pattern accepted: {unsafe}")


def test_portable_trash_override_and_optional_macos_adapter(tmp_path: Path, monkeypatch) -> None:
    explicit = tmp_path / "trash"
    assert kb_review.resolve_trash_dir(explicit=explicit) == explicit.resolve(strict=False)

    monkeypatch.setenv("KB_REVIEW_TRASH_DIR", str(tmp_path / "env-trash"))
    assert kb_review.resolve_trash_dir() == (tmp_path / "env-trash").resolve(strict=False)

    monkeypatch.delenv("KB_REVIEW_TRASH_DIR")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(kb_review.sys, "platform", "darwin")
    assert kb_review.resolve_trash_dir(adapter="macos") == tmp_path / "home" / ".Trash"


def test_cli_delete_defaults_to_preview_and_requires_review_root(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    source = review_root / "notes" / "delete.md"
    review_dir = review_root / "KB-Review-test"
    trash_dir = tmp_path / "trash"
    source.parent.mkdir(parents=True)
    review_dir.mkdir()
    source.write_text("# Delete\n", encoding="utf-8")
    write_review_file(review_dir / "delete.md", [f"| 1 | 0 | 3 | Delete | reason | {source} |"])

    missing_root = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--review-dir", str(review_dir), "--delete"],
        check=False,
        text=True,
        capture_output=True,
    )
    preview = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--review-dir",
            str(review_dir),
            "--review-root",
            str(review_root),
            "--trash-dir",
            str(trash_dir),
            "--delete",
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert missing_root.returncode != 0
    assert "--review-root" in missing_root.stderr
    assert preview.returncode == 0
    assert source.exists()
    assert "planned-trash" in (review_dir / "trash-execution-log.md").read_text(encoding="utf-8")

    execute = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--review-dir",
            str(review_dir),
            "--review-root",
            str(review_root),
            "--trash-dir",
            str(trash_dir),
            "--delete",
            "--execute",
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert execute.returncode == 0
    assert not source.exists()
    assert (trash_dir / "delete.md").exists()


def test_rollback_enforces_review_and_trash_roots(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    review_dir = review_root / "KB-Review-test"
    trash_dir = tmp_path / "trash"
    outside_source = tmp_path / "outside.md"
    outside_trash = tmp_path / "rogue-trash" / "inside.md"
    inside_source = review_root / "notes" / "inside.md"
    inside_trash = trash_dir / "outside.md"
    review_dir.mkdir(parents=True)
    trash_dir.mkdir()
    outside_trash.parent.mkdir()
    inside_trash.write_text("outside source\n", encoding="utf-8")
    outside_trash.write_text("outside trash\n", encoding="utf-8")
    write_execution_log(
        review_dir / "trash-execution-log.md",
        [
            f"| moved-to-trash |  | 0 | 3 | Outside source | {outside_source} | {inside_trash} | 2026-05-07T00:00:00 | reason |  |",
            f"| moved-to-trash |  | 0 | 3 | Outside trash | {inside_source} | {outside_trash} | 2026-05-07T00:00:00 | reason |  |",
        ],
    )

    rows = kb_review.rollback_delete(
        review_dir=review_dir,
        review_root=review_root,
        trash_dir=trash_dir,
        execute=True,
    )

    assert [row["status"] for row in rows] == [
        "skipped-outside-review-root",
        "skipped-outside-trash-root",
    ]
    assert inside_trash.exists()
    assert outside_trash.exists()
    assert not outside_source.exists()
    assert not inside_source.exists()


def test_kb_review_publication_scope_has_no_unpaired_chinese() -> None:
    han = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
    english = re.compile(r"[A-Za-z]{2,}")
    failures: list[str] = []

    for path in sorted(SKILL_PATH.parent.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".yaml", ".yml", ".json"}:
            continue
        previous_nonblank = ""
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            previous = previous_nonblank.strip()
            paired = (
                ("bilingual-compat:" in line and bool(english.search(line)))
                or ("bilingual-compat:" in previous and bool(english.search(previous)))
                or (stripped.startswith("ZH-CN:") and previous.startswith("EN:") and bool(english.search(previous)))
                or (" / " in line and bool(english.search(line)))
            )
            if han.search(line) and not paired:
                failures.append(f"{path.relative_to(SKILL_PATH.parent)}:{line_number}: {stripped}")
            if stripped:
                previous_nonblank = line

    assert not failures, "Unpaired Chinese in kb-review publication scope:\n" + "\n".join(failures)


def test_publication_declares_english_normative_and_bilingual_reason_contract() -> None:
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    output_spec = (SKILL_PATH.parent / "references" / "output-spec.md").read_text(encoding="utf-8")
    agent_yaml = (SKILL_PATH.parent / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert "English is normative" in skill_text
    assert "English / 中文" in output_spec
    assert "EN:" in agent_yaml
    assert "ZH-CN:" in agent_yaml


def test_cli_help_is_bilingual() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0
    assert "Operate on kb-review Markdown review files. / 操作 kb-review Markdown 审查文件。" in result.stdout
    assert "Preview decision=0 rows / 预览 decision=0 的行" in result.stdout
    assert "Perform delete or rollback mutations / 执行删除或回退变更" in result.stdout


def test_generated_delete_report_is_bilingual_snapshot(tmp_path: Path) -> None:
    review_root = tmp_path / "vault"
    review_dir = review_root / "KB-Review-test"
    missing = review_root / "notes" / "missing.md"
    review_dir.mkdir(parents=True)
    write_review_file(
        review_dir / "delete.md",
        [f"| 1 | 0 | 3 | Missing | reason | {missing} |"],
    )

    rows = kb_review.execute_delete(
        review_dir=review_dir,
        review_root=review_root,
        forbidden_paths=[],
        forbidden_tags=["PII"],
        force_delete_path_contains=[],
        trash_dir=tmp_path / "trash",
        execute=True,
    )

    assert rows[0]["note"] == (
        "Source file does not exist; parent directories were not pruned / "
        "源文件不存在；未清理父目录"
    )
    report_lines = (review_dir / "trash-execution-log.md").read_text(encoding="utf-8").splitlines()
    assert report_lines[:4] == [
        "# Trash Execution Log / 回收站执行日志",
        "",
        "- rows / 行数: 1",
        "",
    ]
