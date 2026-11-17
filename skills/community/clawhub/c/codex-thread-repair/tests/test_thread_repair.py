#!/usr/bin/env python3
"""Focused regression tests for the supported Codex rollout repair."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "thread_repair.py"
SPEC = importlib.util.spec_from_file_location("thread_repair", SCRIPT)
assert SPEC and SPEC.loader
thread_repair = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(thread_repair)


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def supported_records(thread_id: str) -> list[dict]:
    stale_turn = "turn-stale"
    next_turn = "turn-next"
    return [
        {
            "timestamp": "2026-09-06T08:00:00.000Z",
            "ordinal": 0,
            "type": "session_meta",
            "payload": {"id": thread_id},
        },
        {
            "timestamp": "2026-09-06T08:01:00.000Z",
            "ordinal": 1,
            "type": "event_msg",
            "payload": {
                "type": "task_started",
                "turn_id": stale_turn,
                "started_at": "2026-09-06T08:01:00.000Z",
            },
        },
        {
            "timestamp": "2026-09-06T08:01:01.000Z",
            "ordinal": 2,
            "type": "response_item",
            "payload": {"turn_id": stale_turn, "text": "must stay byte-identical"},
        },
        {
            "timestamp": "2026-09-06T09:00:00.000Z",
            "ordinal": 1,
            "type": "thread_settings_applied",
            "payload": {},
        },
        {
            "timestamp": "2026-09-06T09:00:01.000Z",
            "ordinal": 2,
            "type": "event_msg",
            "payload": {
                "type": "task_started",
                "turn_id": next_turn,
                "started_at": "2026-09-06T09:00:01.000Z",
            },
        },
        {
            "timestamp": "2026-09-06T09:00:02.000Z",
            "ordinal": 3,
            "type": "event_msg",
            "payload": {"type": "task_complete", "turn_id": next_turn},
        },
    ]


def create_catalog(codex_home: Path, thread_id: str, rollout: Path) -> None:
    (codex_home / "sqlite").mkdir(parents=True)
    with closing(sqlite3.connect(codex_home / "state_5.sqlite")) as connection:
        connection.execute(
            "CREATE TABLE threads (id TEXT, title TEXT, rollout_path TEXT, "
            "cwd TEXT, updated_at INTEGER, archived INTEGER)"
        )
        connection.execute(
            "INSERT INTO threads VALUES (?, ?, ?, ?, ?, ?)",
            (thread_id, "source title", str(rollout), "/tmp", 1, 0),
        )
        connection.commit()
    with closing(sqlite3.connect(codex_home / "sqlite" / "codex-dev.db")) as connection:
        connection.execute(
            "CREATE TABLE local_thread_catalog "
            "(thread_id TEXT, display_title TEXT, missing_candidate INTEGER)"
        )
        connection.execute(
            "INSERT INTO local_thread_catalog VALUES (?, ?, ?)",
            (thread_id, "Visible title", 0),
        )
        connection.commit()


class ThreadRepairTests(unittest.TestCase):
    def test_supported_regression_becomes_healthy_without_body_changes(self) -> None:
        thread_id = "01test-thread"
        stale_turn = "turn-stale"
        records = supported_records(thread_id)
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / "source.jsonl"
            repaired = directory / "repaired.jsonl"
            write_jsonl(source, records)
            thread = {"id": thread_id, "rollout_path": str(source)}

            diagnosis = thread_repair.inspect_rollout(thread)
            self.assertEqual(diagnosis["status"], "supported_ordinal_orphan")
            self.assertEqual(diagnosis["plan"]["orphan_turn_id"], stale_turn)

            thread_repair.build_repaired_rollout(
                source,
                repaired,
                {**diagnosis, "thread": thread},
            )
            final = thread_repair.inspect_rollout(
                {"id": thread_id, "rollout_path": str(repaired)}
            )
            self.assertEqual(final["status"], "healthy")
            self.assertEqual(final["records"], len(records) + 1)
            self.assertEqual(final["ordinal_max"], len(records))
            self.assertEqual(
                thread_repair.normalized_rollout_hash(source),
                thread_repair.normalized_rollout_hash(repaired, stale_turn),
            )

    def test_resolves_exact_ui_title_and_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            codex_home = Path(temporary_directory)
            thread_id = "01catalog-thread"
            rollout = codex_home / "sessions" / "rollout.jsonl"
            rollout.parent.mkdir()
            create_catalog(codex_home, thread_id, rollout)

            by_title = thread_repair.resolve_thread(codex_home, "Visible title")
            by_id = thread_repair.resolve_thread(codex_home, thread_id)
            self.assertEqual(by_title["id"], thread_id)
            self.assertEqual(by_id["display_title"], "Visible title")

    def test_resolve_rejects_rollout_outside_selected_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_home = root / "codex-home"
            outside = root / "outside.jsonl"
            create_catalog(codex_home, "01outside", outside)
            with self.assertRaises(thread_repair.RepairError):
                thread_repair.resolve_thread(codex_home, "01outside")

    def test_prepare_preserves_custom_home_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_home = root / "custom codex home"
            rollout = codex_home / "sessions" / "rollout.jsonl"
            rollout.parent.mkdir(parents=True)
            thread_id = "01custom-home"
            write_jsonl(rollout, supported_records(thread_id))
            create_catalog(codex_home, thread_id, rollout)
            launcher = root / "repair.command"
            args = SimpleNamespace(
                codex_home=codex_home,
                selector=thread_id,
                output=str(launcher),
            )
            with mock.patch.object(thread_repair, "desktop_running", return_value=False):
                with redirect_stdout(StringIO()):
                    self.assertEqual(thread_repair.command_prepare(args), 0)
                content = launcher.read_text(encoding="utf-8")
                self.assertIn("--codex-home", content)
                self.assertIn(str(codex_home), content)
                with self.assertRaises(thread_repair.RepairError):
                    thread_repair.command_prepare(args)

    def test_verify_fails_when_catalog_integrity_fails(self) -> None:
        args = SimpleNamespace(codex_home=Path("/tmp/codex"), selector="thread")
        healthy = {"status": "healthy"}

        def fake_integrity(path: Path) -> str:
            return "corrupt" if path.name == "codex-dev.db" else "ok"

        with mock.patch.object(thread_repair, "diagnose", return_value=healthy.copy()):
            with mock.patch.object(thread_repair, "integrity_check", side_effect=fake_integrity):
                with redirect_stdout(StringIO()):
                    self.assertEqual(thread_repair.command_verify(args), 3)

    def test_rejects_invalid_timestamps_and_misplaced_ordinal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "invalid.jsonl"
            records = supported_records("01invalid-time")
            records[3]["timestamp"] = "not-a-timestamp"
            write_jsonl(source, records)
            result = thread_repair.inspect_rollout(
                {"id": "01invalid-time", "rollout_path": str(source)}
            )
            self.assertEqual(result["status"], "unsupported")
        raw = '{"payload":{"ordinal":99},"ordinal":1}\n'
        with self.assertRaises(thread_repair.RepairError):
            thread_repair.replace_top_level_ordinal(raw, 1, 2)

    def test_rollback_rejects_target_outside_sessions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_home = root / "codex-home"
            (codex_home / "sessions").mkdir(parents=True)
            backup = root / "backup"
            backup.mkdir()
            thread_id = "01rollback"
            original = backup / "original-rollout.jsonl"
            write_jsonl(original, supported_records(thread_id))
            outside = root / "must-not-overwrite.txt"
            outside.write_text("safe", encoding="utf-8")
            manifest = {
                "thread": {"id": thread_id, "rollout_path": str(outside)},
                "original_sha256": thread_repair.sha256_file(original),
            }
            (backup / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = SimpleNamespace(
                codex_home=codex_home,
                backup_directory=str(backup),
                reopen=False,
            )
            with mock.patch.object(thread_repair, "desktop_running", return_value=False):
                with self.assertRaises(thread_repair.RepairError):
                    thread_repair.command_rollback(args)
            self.assertEqual(outside.read_text(encoding="utf-8"), "safe")

    def test_apply_and_valid_rollback_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_home = root / "codex-home"
            rollout = codex_home / "sessions" / "rollout-01roundtrip.jsonl"
            rollout.parent.mkdir(parents=True)
            thread_id = "01roundtrip"
            write_jsonl(rollout, supported_records(thread_id))
            create_catalog(codex_home, thread_id, rollout)
            apply_args = SimpleNamespace(
                codex_home=codex_home,
                selector=thread_id,
                reopen=False,
            )
            with mock.patch.object(thread_repair, "desktop_running", return_value=False):
                with mock.patch.object(thread_repair.Path, "home", return_value=root):
                    with redirect_stdout(StringIO()):
                        self.assertEqual(thread_repair.command_apply(apply_args), 0)
            self.assertEqual(
                thread_repair.inspect_rollout(
                    {"id": thread_id, "rollout_path": str(rollout)}
                )["status"],
                "healthy",
            )
            backups = list((root / ".codex-repair-backups" / thread_id).iterdir())
            self.assertEqual(len(backups), 1)
            rollback_args = SimpleNamespace(
                codex_home=codex_home,
                backup_directory=str(backups[0]),
                reopen=False,
            )
            with mock.patch.object(thread_repair, "desktop_running", return_value=False):
                with redirect_stdout(StringIO()):
                    self.assertEqual(thread_repair.command_rollback(rollback_args), 0)
            self.assertEqual(
                thread_repair.inspect_rollout(
                    {"id": thread_id, "rollout_path": str(rollout)}
                )["status"],
                "supported_ordinal_orphan",
            )


if __name__ == "__main__":
    unittest.main()
