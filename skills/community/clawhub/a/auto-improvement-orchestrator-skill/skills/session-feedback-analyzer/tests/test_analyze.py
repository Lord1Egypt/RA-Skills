"""Tests for session feedback analyzer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import analyze  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _skill_tool_use(uuid: str, skill_id: str, ts: str = "2026-04-05T10:00:00Z"):
    return {
        "type": "assistant",
        "uuid": uuid,
        "timestamp": ts,
        "message": {
            "content": [{
                "type": "tool_use",
                "name": "Skill",
                "input": {"skill": skill_id},
                "id": f"toolu_{uuid[:8]}",
            }],
        },
    }


def _slash_command(uuid: str, command: str, ts: str = "2026-04-05T10:00:00Z"):
    return {
        "type": "system",
        "subtype": "local_command",
        "uuid": uuid,
        "timestamp": ts,
        "content": f"<command-name>/{command}</command-name>\n<command-message>{command}</command-message>",
    }


def _user_msg(uuid: str, text: str, parent: str = "", ts: str = "2026-04-05T10:01:00Z"):
    return {
        "type": "user",
        "uuid": uuid,
        "parentUuid": parent,
        "timestamp": ts,
        "message": {"role": "user", "content": text},
    }


def _assistant_msg(uuid: str, text: str = "", tools: list[dict] | None = None, ts: str = "2026-04-05T10:00:30Z"):
    content = []
    if text:
        content.append({"type": "text", "text": text})
    for t in (tools or []):
        content.append(t)
    return {
        "type": "assistant",
        "uuid": uuid,
        "timestamp": ts,
        "message": {"content": content},
    }


def _bash_tool_use(command: str):
    return {
        "type": "tool_use",
        "name": "Bash",
        "input": {"command": command},
        "id": "toolu_bash",
    }


# ---------------------------------------------------------------------------
# Tests: detect_skill_invocations
# ---------------------------------------------------------------------------


class TestDetectSkillInvocations:
    def test_detects_tool_use_skill(self):
        messages = [
            _skill_tool_use("uuid-1", "cpp-expert"),
        ]
        result = analyze.detect_skill_invocations(messages)
        assert len(result) == 1
        assert result[0].skill_id == "cpp-expert"
        assert result[0].invocation_id == "uuid-1"
        assert result[0].message_index == 0

    def test_detects_slash_command(self):
        messages = [
            _slash_command("uuid-2", "deslop"),
        ]
        result = analyze.detect_skill_invocations(messages)
        assert len(result) == 1
        assert result[0].skill_id == "deslop"

    def test_skips_builtin_commands(self):
        messages = [
            _slash_command("uuid-3", "help"),
            _slash_command("uuid-4", "clear"),
            _slash_command("uuid-5", "resume"),
        ]
        result = analyze.detect_skill_invocations(messages)
        assert len(result) == 0

    def test_detects_multiple_invocations(self):
        messages = [
            _skill_tool_use("uuid-1", "cpp-expert"),
            _user_msg("uuid-u1", "ok"),
            _slash_command("uuid-2", "deslop"),
        ]
        result = analyze.detect_skill_invocations(messages)
        assert len(result) == 2
        assert result[0].skill_id == "cpp-expert"
        assert result[1].skill_id == "deslop"

    def test_ignores_non_skill_tool_use(self):
        messages = [{
            "type": "assistant",
            "uuid": "uuid-x",
            "timestamp": "2026-04-05T10:00:00Z",
            "message": {
                "content": [{
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/foo"},
                    "id": "toolu_read",
                }],
            },
        }]
        result = analyze.detect_skill_invocations(messages)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# Tests: classify_outcome
# ---------------------------------------------------------------------------


class TestClassifyOutcome:
    def test_correction_rejection_zh(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert"),
            _user_msg("u-1", "不对，应该用snake_case"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "correction"
        assert event.correction_type == "rejection"
        assert event.confidence >= 0.9

    def test_correction_rejection_en(self):
        messages = [
            _skill_tool_use("inv-1", "code-review"),
            _user_msg("u-1", "No, that's not right. Use the other approach"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "correction"

    def test_correction_redo(self):
        messages = [
            _skill_tool_use("inv-1", "deslop"),
            _user_msg("u-1", "重新来，这个效果不好"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "correction"
        assert event.correction_type in ("redo", "rejection")

    def test_correction_revert(self):
        messages = [
            _skill_tool_use("inv-1", "code-review"),
            _assistant_msg("a-1", tools=[_bash_tool_use("git checkout -- src/main.py")]),
            _user_msg("u-1", "just undo that"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "correction"
        assert event.correction_type == "revert"

    def test_partial_correction(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert"),
            _user_msg("u-1", "这个可以，但是命名应该用camelCase"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "partial"

    def test_acceptance_explicit(self):
        messages = [
            _skill_tool_use("inv-1", "deslop"),
            _user_msg("u-1", "looks good, thanks"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "acceptance"

    def test_acceptance_silent_continuation(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert"),
            _user_msg("u-1", "Now let's work on the authentication module next"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert event.outcome == "acceptance"
        assert event.confidence <= 0.7

    def test_ambiguous_no_user_response(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert"),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is None

    def test_window_bounded_by_next_invocation(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert", ts="2026-04-05T10:00:00Z"),
            _user_msg("u-1", "looks good, thanks for the help"),
            _skill_tool_use("inv-2", "deslop", ts="2026-04-05T10:01:00Z"),
            _user_msg("u-2", "不对"),
        ]
        invocations = analyze.detect_skill_invocations(messages)
        # First invocation's window should NOT include "不对" after second invocation
        event1 = analyze.classify_outcome(messages, invocations[0], invocations[1].message_index)
        assert event1 is not None
        assert event1.outcome == "acceptance"

    def test_snippet_truncation(self):
        messages = [
            _skill_tool_use("inv-1", "cpp-expert"),
            _user_msg("u-1", "不对 " + "x" * 300),
        ]
        inv = analyze.detect_skill_invocations(messages)[0]
        event = analyze.classify_outcome(messages, inv)
        assert event is not None
        assert len(event.user_message_snippet) <= 200


# ---------------------------------------------------------------------------
# Tests: attribute_dimension
# ---------------------------------------------------------------------------


class TestAttributeDimension:
    def test_accuracy(self):
        assert analyze.attribute_dimension("命名不对") == "accuracy"
        assert analyze.attribute_dimension("wrong naming convention") == "accuracy"

    def test_coverage(self):
        assert analyze.attribute_dimension("你漏了错误处理") == "coverage"
        assert analyze.attribute_dimension("missing error handling") == "coverage"

    def test_security(self):
        assert analyze.attribute_dimension("token exposed") == "security"

    def test_none_for_generic(self):
        assert analyze.attribute_dimension("hello world") is None


# ---------------------------------------------------------------------------
# Tests: write_feedback_jsonl
# ---------------------------------------------------------------------------


class TestWriteFeedbackJsonl:
    def test_creates_file(self, tmp_path):
        event = analyze.FeedbackEvent(
            event_id="abc123",
            timestamp="2026-04-05T10:00:00Z",
            session_id="sess-1",
            skill_id="cpp-expert",
            invocation_uuid="inv-1",
            outcome="correction",
            confidence=0.9,
            correction_type="rejection",
            user_message_snippet="不对",
            turns_to_feedback=1,
            ai_tools_used=["Read", "Edit"],
            dimension_hint="accuracy",
        )
        out = tmp_path / "feedback.jsonl"
        analyze.write_feedback_jsonl([event], out)
        assert out.exists()
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 1
        parsed = json.loads(lines[0])
        assert parsed["event_id"] == "abc123"
        assert parsed["outcome"] == "correction"

    def test_deduplicates(self, tmp_path):
        event = analyze.FeedbackEvent(
            event_id="abc123", timestamp="", session_id="", skill_id="x",
            invocation_uuid="", outcome="correction", confidence=0.9,
            correction_type=None, user_message_snippet="", turns_to_feedback=1,
            ai_tools_used=[], dimension_hint=None,
        )
        out = tmp_path / "feedback.jsonl"
        analyze.write_feedback_jsonl([event], out)
        analyze.write_feedback_jsonl([event], out)  # write again
        lines = out.read_text().strip().split("\n")
        assert len(lines) == 1  # no duplicate

    def test_no_snippets_mode(self, tmp_path):
        event = analyze.FeedbackEvent(
            event_id="def456", timestamp="", session_id="", skill_id="x",
            invocation_uuid="", outcome="correction", confidence=0.9,
            correction_type=None, user_message_snippet="sensitive text",
            turns_to_feedback=1, ai_tools_used=[], dimension_hint=None,
        )
        out = tmp_path / "feedback.jsonl"
        analyze.write_feedback_jsonl([event], out, no_snippets=True)
        parsed = json.loads(out.read_text().strip())
        assert parsed["user_message_snippet"] == ""


# ---------------------------------------------------------------------------
# Tests: archive_old_events
# ---------------------------------------------------------------------------


class TestArchiveOldEvents:
    def test_archives_old_events(self, tmp_path):
        feedback = tmp_path / "feedback.jsonl"
        archive_dir = tmp_path / "archive"

        old_event = {"event_id": "old", "timestamp": "2025-01-01T00:00:00Z", "outcome": "correction"}
        new_event = {"event_id": "new", "timestamp": "2026-04-05T00:00:00Z", "outcome": "acceptance"}

        with feedback.open("w") as f:
            f.write(json.dumps(old_event) + "\n")
            f.write(json.dumps(new_event) + "\n")

        count = analyze.archive_old_events(feedback, archive_dir, days=90)
        assert count == 1

        remaining = feedback.read_text().strip().split("\n")
        assert len(remaining) == 1
        assert json.loads(remaining[0])["event_id"] == "new"

        archived_files = list(archive_dir.glob("*.jsonl"))
        assert len(archived_files) == 1
