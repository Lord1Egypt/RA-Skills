import argparse
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import skill_feedback  # noqa: E402


class SkillFeedbackTests(unittest.TestCase):
    def test_codex_roots_do_not_guess_other_agent_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            codex_home = Path(temp_dir) / "codex-home"
            other_home = Path(temp_dir) / "other-agent-home"
            environment = {
                "CODEX_HOME": str(codex_home),
                "OTHER_AGENT_USER_DATA_DIR": str(other_home),
            }
            with mock.patch.dict(os.environ, environment, clear=False):
                roots = skill_feedback._codex_trajectory_roots()

            self.assertIn(codex_home / "sessions", roots)
            self.assertIn(codex_home / "archived_sessions", roots)
            self.assertFalse(any(str(other_home) in str(root) for root in roots))

    def test_codex_provider_discovers_strong_skill_signals(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            records = [
                {
                    "timestamp": timestamp,
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "input": {
                            "cmd": "sed -n '1,200p' /tmp/.codex/skills/demo-skill/SKILL.md"
                        },
                    },
                },
                {
                    "timestamp": timestamp,
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "请使用 $another-skill 完成任务",
                    },
                },
            ]
            trajectory = root / "rollout-550e8400-e29b-41d4-a716-446655440000.jsonl"
            trajectory.write_text(
                "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                encoding="utf-8",
            )

            result = skill_feedback.discover_skills([root], days=30)

            self.assertEqual(skill_feedback.CODEX_PROVIDER_ID, result["provider"])
            self.assertFalse(result["needsAgentDiscovery"])
            self.assertEqual({"demo-skill", "another-skill"}, {item["name"] for item in result["skills"]})

    def test_unknown_agent_fallback_requires_current_agent_discovery(self):
        result = skill_feedback._agent_discovery_result()

        self.assertTrue(result["needsAgentDiscovery"])
        self.assertIsNone(result["provider"])
        self.assertIn("current Agent", result["message"])
        self.assertTrue(any("unknown vendor format" in item for item in result["invariants"]))

    def test_codex_provider_does_not_apply_to_another_agent(self):
        with mock.patch.object(
            skill_feedback,
            "_codex_trajectory_roots",
            return_value=[Path("/tmp/fake-codex-sessions")],
        ), mock.patch.object(Path, "is_dir", return_value=True), mock.patch.object(
            Path,
            "rglob",
            return_value=iter([Path("/tmp/fake-codex-sessions/rollout.jsonl")]),
        ):
            provider = skill_feedback.probe_providers("NovelAgent")[0]

        self.assertTrue(provider["detected"])
        self.assertFalse(provider["applicable"])

    def test_redaction_and_validation_accept_normalized_draft(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "read /Users/alice/private.txt",
                "skillPerformance": "used a domain workflow and completed the task",
                "rating": 8,
                "comment": "contact me@example.com with Authorization: Bearer abcdef123456",
            },
        }

        sanitized = skill_feedback.sanitize_value(draft)

        self.assertEqual([], skill_feedback.validate_payload(sanitized))
        self.assertIn("[REDACTED_EMAIL]", sanitized["evaluation"]["comment"])
        self.assertIn("[REDACTED_SECRET]", sanitized["evaluation"]["comment"])
        self.assertIn("[REDACTED_HOME]", sanitized["evaluation"]["usageScenario"])

    def test_validation_requires_exact_four_evaluation_fields(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow and contributed to the result",
                "rating": 8,
                "comment": "useful",
                "strengths": ["legacy field"],
            },
        }

        errors = skill_feedback.validate_payload(draft)

        self.assertTrue(
            any(
                "only accepts usageScenario, skillPerformance, rating, and comment" in error
                for error in errors
            )
        )

        del draft["evaluation"]["strengths"]
        del draft["evaluation"]["skillPerformance"]
        errors = skill_feedback.validate_payload(draft)

        self.assertIn("evaluation.skillPerformance is required", errors)

        draft["evaluation"]["skillPerformance"] = "provided a workflow"
        del draft["evaluation"]["rating"]
        del draft["evaluation"]["comment"]
        errors = skill_feedback.validate_payload(draft)

        self.assertIn("evaluation.rating must be between 1 and 10", errors)
        self.assertIn("evaluation.comment field is required; use null when omitted", errors)

    def test_validation_accepts_ten_point_rating_and_optional_comment(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 10,
                "comment": None,
            },
        }

        self.assertEqual([], skill_feedback.validate_payload(draft))

        draft["evaluation"]["rating"] = 10.1
        self.assertIn(
            "evaluation.rating must be between 1 and 10",
            skill_feedback.validate_payload(draft),
        )

    def test_validation_accepts_estimated_token_usage(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"estimatedTokenUsage": 1500},
        }

        self.assertEqual([], skill_feedback.validate_payload(draft))

    def test_validation_accepts_missing_estimated_token_usage(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"agentType": "openclaw"},
        }

        self.assertEqual([], skill_feedback.validate_payload(draft))

        draft["context"]["estimatedTokenUsage"] = None
        self.assertEqual([], skill_feedback.validate_payload(draft))

    def test_validation_rejects_non_integer_estimated_token_usage(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"estimatedTokenUsage": "1500"},
        }

        for invalid_value in ("1500", 1500.0, True):
            draft["context"]["estimatedTokenUsage"] = invalid_value
            errors = skill_feedback.validate_payload(draft)
            self.assertIn("context.estimatedTokenUsage must be an integer", errors)

    def test_validation_rejects_negative_estimated_token_usage(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"estimatedTokenUsage": -1},
        }

        self.assertIn(
            "context.estimatedTokenUsage must be >= 0",
            skill_feedback.validate_payload(draft),
        )

    def test_validation_rejects_unknown_context_fields(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"extraField": "not allowed"},
        }

        errors = skill_feedback.validate_payload(draft)
        self.assertTrue(
            any(
                "context only accepts agentType, occurredAt, trajectoryIdHash, and estimatedTokenUsage" in error
                for error in errors
            )
        )

    def test_validation_rejects_non_object_context(self):
        draft = {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": "not an object",
        }

        self.assertIn("context must be an object", skill_feedback.validate_payload(draft))

    def test_validation_accepts_legacy_schema_version_without_new_field(self):
        draft = {
            "schemaVersion": "1.3",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": None,
            },
            "context": {"agentType": "openclaw"},
        }

        self.assertEqual([], skill_feedback.validate_payload(draft))

    def test_submit_generates_schema_version_1_4(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            draft_path.write_text(
                json.dumps(
                    {
                        "schemaVersion": "1.4",
                        "skill": {"name": "demo-skill"},
                        "evaluation": {
                            "usageScenario": "demo task",
                            "skillPerformance": "provided a workflow",
                            "rating": 8,
                            "comment": None,
                        },
                        "context": {"estimatedTokenUsage": 1200},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=str(outbox_path),
            )

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = skill_feedback._command_submit(args)

            self.assertEqual(0, exit_code)
            record = json.loads(outbox_path.read_text(encoding="utf-8"))
            self.assertEqual("1.4", record["payload"]["schemaVersion"])
            self.assertEqual(1200, record["payload"]["context"]["estimatedTokenUsage"])

    def test_submit_refuses_without_review_assertion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            draft_path.write_text(
                json.dumps(
                    {
                        "schemaVersion": "1.4",
                        "skill": {"name": "demo-skill"},
                        "evaluation": {
                            "usageScenario": "demo task",
                            "skillPerformance": "provided a workflow",
                            "rating": 8,
                            "comment": None,
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                confirmed=False,
                input=str(draft_path),
                outbox=str(outbox_path),
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_submit(args)

            self.assertEqual(2, exit_code)
            self.assertFalse(outbox_path.exists())

    def test_submit_accepts_reviewed_usage_scenario(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            draft_path.write_text(
                json.dumps(
                    {
                        "schemaVersion": "1.4",
                        "skill": {"name": "demo-skill"},
                        "evaluation": {
                            "usageScenario": "demo task",
                            "skillPerformance": "provided a workflow",
                            "rating": 8,
                            "comment": "useful",
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=str(outbox_path),
            )

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = skill_feedback._command_submit(args)

            self.assertEqual(0, exit_code)
            record = json.loads(outbox_path.read_text(encoding="utf-8"))
            self.assertEqual("demo task", record["payload"]["evaluation"]["usageScenario"])

    # ---- upload 命令测试 ----

    def _make_valid_payload(self) -> dict:
        return {
            "schemaVersion": "1.4",
            "skill": {"name": "demo-skill"},
            "evaluation": {
                "usageScenario": "demo task",
                "skillPerformance": "provided a workflow",
                "rating": 8,
                "comment": "useful",
            },
        }

    def test_upload_refuses_without_confirmed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            draft_path.write_text(
                json.dumps(self._make_valid_payload(), ensure_ascii=False),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                confirmed=False,
                input=str(draft_path),
                outbox=None,
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(2, exit_code)

    def test_upload_refuses_sensitive_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft = self._make_valid_payload()
            draft["evaluation"]["comment"] = "contact me@example.com"
            draft_path = Path(temp_dir) / "draft.json"
            draft_path.write_text(
                json.dumps(draft, ensure_ascii=False),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=None,
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(3, exit_code)

    def test_upload_success_sends_post_and_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            draft_path.write_text(
                json.dumps(self._make_valid_payload(), ensure_ascii=False),
                encoding="utf-8",
            )

            fake_resp = mock.MagicMock()
            fake_resp.status = 200
            fake_resp.read.return_value = json.dumps({"ok": True}).encode()
            fake_resp.__enter__ = mock.MagicMock(return_value=fake_resp)
            fake_resp.__exit__ = mock.MagicMock(return_value=False)

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                return_value=fake_resp,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            mock_urlopen.assert_called_once()
            req = mock_urlopen.call_args[0][0]
            self.assertEqual("POST", req.method)
            content_type = req.headers.get("Content-type") or req.headers.get("Content-Type")
            self.assertIsNotNone(content_type)
            self.assertIn("application/json", content_type)

    def test_upload_failure_saves_to_outbox_and_returns_one(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            draft_path.write_text(
                json.dumps(self._make_valid_payload(), ensure_ascii=False),
                encoding="utf-8",
            )

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                side_effect=skill_feedback.urllib.error.URLError("connection refused"),
            ), contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=str(outbox_path),
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(1, exit_code)
            self.assertTrue(outbox_path.exists())
            record = json.loads(outbox_path.read_text(encoding="utf-8"))
            self.assertFalse(record["uploadAttempts"][0]["success"])
            self.assertEqual("local-outbox", record["transport"])

    def test_upload_accepts_outbox_record_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = self._make_valid_payload()
            record = {
                "schemaVersion": "1.4",
                "feedbackId": "test-id-123",
                "savedAt": "2026-01-01T00:00:00Z",
                "transport": "local-outbox",
                "consent": {"confirmed": True, "confirmedAt": "2026-01-01T00:00:00Z"},
                "uploadAttempts": [],
                "payload": payload,
            }
            draft_path = Path(temp_dir) / "record.json"
            draft_path.write_text(
                json.dumps(record, ensure_ascii=False),
                encoding="utf-8",
            )

            fake_resp = mock.MagicMock()
            fake_resp.status = 200
            fake_resp.read.return_value = json.dumps({"ok": True}).encode()
            fake_resp.__enter__ = mock.MagicMock(return_value=fake_resp)
            fake_resp.__exit__ = mock.MagicMock(return_value=False)

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                return_value=fake_resp,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                )
                exit_code = skill_feedback._command_upload(args)
                self.assertEqual(0, exit_code)
                # Verify the request was sent with correct payload
                req = mock_urlopen.call_args[0][0]
                sent_body = json.loads(req.data)
                self.assertEqual("test-id-123", sent_body["feedbackId"])
                self.assertEqual("demo task", sent_body["evaluation"]["usageScenario"])

    def test_upload_validates_outbox_record_payload(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            record = {
                "schemaVersion": "1.4",
                "feedbackId": "test-id-456",
                "savedAt": "2026-01-01T00:00:00Z",
                "consent": {"confirmed": True, "confirmedAt": "2026-01-01T00:00:00Z"},
                "payload": {
                    "schemaVersion": "1.4",
                    "skill": {},
                    "evaluation": {
                        "usageScenario": "demo",
                        "skillPerformance": "ok",
                        "rating": 8,
                        "comment": None,
                    },
                },
            }
            draft_path = Path(temp_dir) / "record.json"
            draft_path.write_text(
                json.dumps(record, ensure_ascii=False),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(2, exit_code)

    def test_upload_handles_non_json_response(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            draft_path.write_text(
                json.dumps(self._make_valid_payload(), ensure_ascii=False),
                encoding="utf-8",
            )

            fake_resp = mock.MagicMock()
            fake_resp.status = 200
            fake_resp.read.return_value = b"<html>Not JSON</html>"
            fake_resp.__enter__ = mock.MagicMock(return_value=fake_resp)
            fake_resp.__exit__ = mock.MagicMock(return_value=False)

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                return_value=fake_resp,
            ), contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)

    def test_upload_outbox_record_with_sensitive_payload_refuses(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = self._make_valid_payload()
            payload["evaluation"]["comment"] = "contact me@example.com"
            record = {
                "schemaVersion": "1.4",
                "feedbackId": "test-id-789",
                "savedAt": "2026-01-01T00:00:00Z",
                "consent": {"confirmed": True, "confirmedAt": "2026-01-01T00:00:00Z"},
                "uploadAttempts": [],
                "payload": payload,
            }
            draft_path = Path(temp_dir) / "record.json"
            draft_path.write_text(
                json.dumps(record, ensure_ascii=False),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(3, exit_code)

    # ---- attachment tests ----

    def _make_small_attachment(self, temp_dir: str, size: int = 100, suffix: str = ".png") -> Path:
        path = Path(temp_dir) / f"attachment{suffix}"
        path.write_bytes(b"x" * size)
        return path

    def _make_large_attachment(self, temp_dir: str, size: int = 60 * 1024, suffix: str = ".mp4") -> Path:
        path = Path(temp_dir) / f"attachment{suffix}"
        # Vary content by filename so multiple large files have unique sha256
        seed = suffix.encode("utf-8")
        payload = seed + b"y" * (size - len(seed))
        path.write_bytes(payload)
        return path

    def test_validation_accepts_valid_inline_attachment(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "inline",
                "name": "screenshot.png",
                "mimeType": "image/png",
                "size": 100,
                "sha256": "a" * 64,
                "data": "aGVsbG8=",
            }
        ]

        self.assertEqual([], skill_feedback.validate_payload(draft))

    def test_validation_accepts_valid_storage_attachment(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "storage",
                "name": "recording.mp4",
                "mimeType": "video/mp4",
                "size": 102400,
                "sha256": "b" * 64,
                "storageKey": "attachments/2026/09/17/f/recording.mp4",
            }
        ]

        self.assertEqual([], skill_feedback.validate_payload(draft))

    def test_validation_rejects_invalid_attachment_type(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "unknown",
                "name": "file.txt",
                "mimeType": "text/plain",
                "size": 100,
                "sha256": "c" * 64,
            }
        ]

        errors = skill_feedback.validate_payload(draft)
        self.assertTrue(any("type must be 'inline' or 'storage'" in error for error in errors))
        self.assertTrue(any("mimeType must be image/* or video/*" in error for error in errors))

    def test_validation_rejects_attachment_with_bad_sha256(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "inline",
                "name": "screenshot.png",
                "mimeType": "image/png",
                "size": 100,
                "sha256": "too-short",
                "data": "aGVsbG8=",
            }
        ]

        errors = skill_feedback.validate_payload(draft)
        self.assertTrue(any("sha256 must be a 64-character" in error for error in errors))

    def test_validation_rejects_inline_attachment_without_data(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "inline",
                "name": "screenshot.png",
                "mimeType": "image/png",
                "size": 100,
                "sha256": "d" * 64,
            }
        ]

        errors = skill_feedback.validate_payload(draft)
        self.assertTrue(any("data is required for inline attachments" in error for error in errors))

    def test_submit_with_small_attachment_inlines_and_saves(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            attachment_path = self._make_small_attachment(temp_dir, size=100)

            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=str(outbox_path),
                attachment=[str(attachment_path)],
            )

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = skill_feedback._command_submit(args)

            self.assertEqual(0, exit_code)
            record = json.loads(outbox_path.read_text(encoding="utf-8"))
            self.assertEqual(1, len(record["payload"]["attachments"]))
            self.assertEqual("inline", record["payload"]["attachments"][0]["type"])
            self.assertEqual("attachment.png", record["payload"]["attachments"][0]["name"])
            self.assertIn("data", record["payload"]["attachments"][0])

    def test_submit_rejects_large_attachment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            outbox_path = Path(temp_dir) / "outbox.jsonl"
            attachment_path = self._make_large_attachment(temp_dir)

            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=str(outbox_path),
                attachment=[str(attachment_path)],
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_submit(args)

            self.assertEqual(2, exit_code)
            self.assertFalse(outbox_path.exists())

    def test_upload_with_small_attachment_inlines(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            attachment_path = self._make_small_attachment(temp_dir, size=100)
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            fake_resp = mock.MagicMock()
            fake_resp.status = 200
            fake_resp.read.return_value = json.dumps({"ok": True}).encode()
            fake_resp.__enter__ = mock.MagicMock(return_value=fake_resp)
            fake_resp.__exit__ = mock.MagicMock(return_value=False)

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                return_value=fake_resp,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                    attachment=[str(attachment_path)],
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            req = mock_urlopen.call_args[0][0]
            sent_body = json.loads(req.data)
            self.assertEqual(1, len(sent_body["attachments"]))
            self.assertEqual("inline", sent_body["attachments"][0]["type"])

    def test_upload_with_large_attachment_uses_server_relay(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            attachment_path = self._make_large_attachment(temp_dir)
            file_sha256 = hashlib.sha256(attachment_path.read_bytes()).hexdigest()
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            upload_response = {
                "code": 200,
                "data": [
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                        "url": "https://mss.sankuai.com/mars-open-image/skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                        "name": "recording.mp4",
                        "mimeType": "video/mp4",
                        "size": 61440,
                        "sha256": file_sha256,
                    }
                ],
            }

            feedback_resp = mock.MagicMock()
            feedback_resp.status = 200
            feedback_resp.read.return_value = json.dumps({"ok": True}).encode()
            feedback_resp.__enter__ = mock.MagicMock(return_value=feedback_resp)
            feedback_resp.__exit__ = mock.MagicMock(return_value=False)

            upload_url = skill_feedback.FEEDBACK_API_URL + skill_feedback.ATTACHMENT_UPLOAD_PATH

            def urlopen_side_effect(req, **kwargs):
                if req.full_url == upload_url:
                    upload_mock = mock.MagicMock()
                    upload_mock.status = 200
                    upload_mock.read.return_value = json.dumps(upload_response).encode()
                    upload_mock.__enter__ = mock.MagicMock(return_value=upload_mock)
                    upload_mock.__exit__ = mock.MagicMock(return_value=False)
                    return upload_mock
                return feedback_resp

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                side_effect=urlopen_side_effect,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                    attachment=[str(attachment_path)],
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            # Find the feedback request
            feedback_calls = [
                call for call in mock_urlopen.call_args_list
                if call.args[0].full_url == skill_feedback.FEEDBACK_API_URL
            ]
            self.assertEqual(1, len(feedback_calls))
            sent_body = json.loads(feedback_calls[0].args[0].data)
            self.assertEqual(1, len(sent_body["attachments"]))
            self.assertEqual("storage", sent_body["attachments"][0]["type"])
            self.assertEqual(
                "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                sent_body["attachments"][0]["storageKey"],
            )
            self.assertEqual("video/mp4", sent_body["attachments"][0]["mimeType"])

    def test_upload_with_multiple_large_attachments_batch_uploads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            attachment1 = self._make_large_attachment(temp_dir, suffix=".mp4")
            attachment2 = self._make_large_attachment(temp_dir, suffix=".png")
            sha1 = hashlib.sha256(attachment1.read_bytes()).hexdigest()
            sha2 = hashlib.sha256(attachment2.read_bytes()).hexdigest()
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            upload_response = {
                "code": 200,
                "data": [
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                        "name": "attachment.mp4",
                        "mimeType": "video/mp4",
                        "size": 61440,
                        "sha256": sha1,
                    },
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/screenshot.png",
                        "name": "attachment.png",
                        "mimeType": "image/png",
                        "size": 61440,
                        "sha256": sha2,
                    },
                ],
            }

            feedback_resp = mock.MagicMock()
            feedback_resp.status = 200
            feedback_resp.read.return_value = json.dumps({"ok": True}).encode()
            feedback_resp.__enter__ = mock.MagicMock(return_value=feedback_resp)
            feedback_resp.__exit__ = mock.MagicMock(return_value=False)

            upload_url = skill_feedback.FEEDBACK_API_URL + skill_feedback.ATTACHMENT_UPLOAD_PATH
            upload_call_count = 0

            def urlopen_side_effect(req, **kwargs):
                nonlocal upload_call_count
                if req.full_url == upload_url:
                    upload_call_count += 1
                    upload_mock = mock.MagicMock()
                    upload_mock.status = 200
                    upload_mock.read.return_value = json.dumps(upload_response).encode()
                    upload_mock.__enter__ = mock.MagicMock(return_value=upload_mock)
                    upload_mock.__exit__ = mock.MagicMock(return_value=False)
                    return upload_mock
                return feedback_resp

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                side_effect=urlopen_side_effect,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                    attachment=[str(attachment1), str(attachment2)],
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            self.assertEqual(1, upload_call_count)

            feedback_calls = [
                call for call in mock_urlopen.call_args_list
                if call.args[0].full_url == skill_feedback.FEEDBACK_API_URL
            ]
            self.assertEqual(1, len(feedback_calls))
            sent_body = json.loads(feedback_calls[0].args[0].data)
            self.assertEqual(2, len(sent_body["attachments"]))
            self.assertTrue(all(att["type"] == "storage" for att in sent_body["attachments"]))
            self.assertEqual(
                {"attachment.mp4", "attachment.png"},
                {att["name"] for att in sent_body["attachments"]},
            )

    def test_upload_with_mixed_sizes_inlines_small_and_batches_large(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            small = self._make_small_attachment(temp_dir, size=100)
            large = self._make_large_attachment(temp_dir)
            large_sha = hashlib.sha256(large.read_bytes()).hexdigest()
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            upload_response = {
                "code": 200,
                "data": [
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                        "name": "attachment.mp4",
                        "mimeType": "video/mp4",
                        "size": 61440,
                        "sha256": large_sha,
                    }
                ],
            }

            feedback_resp = mock.MagicMock()
            feedback_resp.status = 200
            feedback_resp.read.return_value = json.dumps({"ok": True}).encode()
            feedback_resp.__enter__ = mock.MagicMock(return_value=feedback_resp)
            feedback_resp.__exit__ = mock.MagicMock(return_value=False)

            upload_url = skill_feedback.FEEDBACK_API_URL + skill_feedback.ATTACHMENT_UPLOAD_PATH
            upload_call_count = 0

            def urlopen_side_effect(req, **kwargs):
                nonlocal upload_call_count
                if req.full_url == upload_url:
                    upload_call_count += 1
                    upload_mock = mock.MagicMock()
                    upload_mock.status = 200
                    upload_mock.read.return_value = json.dumps(upload_response).encode()
                    upload_mock.__enter__ = mock.MagicMock(return_value=upload_mock)
                    upload_mock.__exit__ = mock.MagicMock(return_value=False)
                    return upload_mock
                return feedback_resp

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                side_effect=urlopen_side_effect,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                    attachment=[str(small), str(large)],
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            self.assertEqual(1, upload_call_count)

            feedback_calls = [
                call for call in mock_urlopen.call_args_list
                if call.args[0].full_url == skill_feedback.FEEDBACK_API_URL
            ]
            sent_body = json.loads(feedback_calls[0].args[0].data)
            types = {att["type"] for att in sent_body["attachments"]}
            self.assertEqual({"inline", "storage"}, types)

    def test_upload_batch_response_order_mismatch_maps_by_sha256(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            attachment1 = self._make_large_attachment(temp_dir, suffix=".mp4")
            attachment2 = self._make_large_attachment(temp_dir, suffix=".png")
            sha1 = hashlib.sha256(attachment1.read_bytes()).hexdigest()
            sha2 = hashlib.sha256(attachment2.read_bytes()).hexdigest()
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            # Server returns items in reverse order relative to request
            upload_response = {
                "code": 200,
                "data": [
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/screenshot.png",
                        "name": "attachment.png",
                        "mimeType": "image/png",
                        "size": 61440,
                        "sha256": sha2,
                    },
                    {
                        "storageKey": "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                        "name": "attachment.mp4",
                        "mimeType": "video/mp4",
                        "size": 61440,
                        "sha256": sha1,
                    },
                ],
            }

            feedback_resp = mock.MagicMock()
            feedback_resp.status = 200
            feedback_resp.read.return_value = json.dumps({"ok": True}).encode()
            feedback_resp.__enter__ = mock.MagicMock(return_value=feedback_resp)
            feedback_resp.__exit__ = mock.MagicMock(return_value=False)

            upload_url = skill_feedback.FEEDBACK_API_URL + skill_feedback.ATTACHMENT_UPLOAD_PATH

            def urlopen_side_effect(req, **kwargs):
                if req.full_url == upload_url:
                    upload_mock = mock.MagicMock()
                    upload_mock.status = 200
                    upload_mock.read.return_value = json.dumps(upload_response).encode()
                    upload_mock.__enter__ = mock.MagicMock(return_value=upload_mock)
                    upload_mock.__exit__ = mock.MagicMock(return_value=False)
                    return upload_mock
                return feedback_resp

            with mock.patch.object(
                skill_feedback.urllib.request,
                "urlopen",
                side_effect=urlopen_side_effect,
            ) as mock_urlopen, contextlib.redirect_stdout(io.StringIO()):
                args = argparse.Namespace(
                    confirmed=True,
                    input=str(draft_path),
                    outbox=None,
                    attachment=[str(attachment1), str(attachment2)],
                )
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(0, exit_code)
            feedback_calls = [
                call for call in mock_urlopen.call_args_list
                if call.args[0].full_url == skill_feedback.FEEDBACK_API_URL
            ]
            sent_body = json.loads(feedback_calls[0].args[0].data)
            attachments_by_name = {att["name"]: att for att in sent_body["attachments"]}
            self.assertEqual(
                "skill-feedback-attachments/2026/09/18/client-id/fb-001/recording.mp4",
                attachments_by_name["attachment.mp4"]["storageKey"],
            )
            self.assertEqual(
                "skill-feedback-attachments/2026/09/18/client-id/fb-001/screenshot.png",
                attachments_by_name["attachment.png"]["storageKey"],
            )

    def test_upload_attachment_not_found_returns_two(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=None,
                attachment=["/nonexistent/path/screenshot.png"],
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(2, exit_code)

    def test_upload_rejects_non_image_video_attachment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.json"
            attachment_path = Path(temp_dir) / "notes.txt"
            attachment_path.write_text("plain text", encoding="utf-8")
            payload = self._make_valid_payload()
            payload["schemaVersion"] = "1.5"
            draft_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            args = argparse.Namespace(
                confirmed=True,
                input=str(draft_path),
                outbox=None,
                attachment=[str(attachment_path)],
            )

            with contextlib.redirect_stderr(io.StringIO()):
                exit_code = skill_feedback._command_upload(args)

            self.assertEqual(2, exit_code)

    def test_storage_key_with_uuid_is_not_redacted(self):
        draft = self._make_valid_payload()
        draft["schemaVersion"] = "1.5"
        draft["attachments"] = [
            {
                "type": "storage",
                "name": "recording.mp4",
                "mimeType": "video/mp4",
                "size": 1048576,
                "sha256": "a" * 64,
                "storageKey": "skill-feedback-attachments/2026/09/18/c95fce51-5081-43ba-bf61-1234567890ab/recording.mp4",
            }
        ]

        sanitized = skill_feedback.sanitize_value(draft)

        self.assertEqual(draft, sanitized)
        self.assertIn(
            "c95fce51-5081-43ba-bf61-1234567890ab",
            sanitized["attachments"][0]["storageKey"],
        )


if __name__ == "__main__":
    unittest.main()
