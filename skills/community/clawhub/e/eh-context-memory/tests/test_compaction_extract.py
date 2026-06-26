"""Tests for compaction-extract stop hook."""

import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


@pytest.fixture
def env(tmp_path):
    e = os.environ.copy()
    e["HOME"] = str(tmp_path)
    sessions = tmp_path / ".openclaw" / "shared-context" / "sessions"
    sessions.mkdir(parents=True)
    return e, tmp_path


def run(env, stdin_data="", session_id="test-sess"):
    env["NC_SESSION"] = session_id
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "compaction-extract.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestCompactionExtract:
    def test_first_call_allows_and_counts(self, env):
        e, tmp = env
        inp = json.dumps({"last_assistant_message": "working on feature"})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
        # State file should have count 1
        state = tmp / ".openclaw/shared-context/sessions/test-sess/compaction-extract.json"
        assert state.exists()
        data = json.loads(state.read_text())
        assert data["stop_count"] == 1

    def test_count_below_interval_allows(self, env):
        e, tmp = env
        e["COMPACTION_EXTRACT_INTERVAL"] = "5"
        inp = json.dumps({"last_assistant_message": "doing stuff"})
        for _ in range(4):
            stdout, rc = run(e, inp)
            result = json.loads(stdout)
            assert result.get("continue") is True

    def test_at_interval_extracts(self, env):
        e, tmp = env
        e["COMPACTION_EXTRACT_INTERVAL"] = "3"
        inp = json.dumps({"last_assistant_message": "Important decision: use Redis for caching."})
        # Calls 1 and 2 should allow
        run(e, inp)
        run(e, inp)
        # Call 3 should extract
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        ctx = result.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "snapshot saved" in ctx
        assert "stop #3" in ctx
        # Handoff file should exist
        handoffs = tmp / ".openclaw/shared-context/sessions/test-sess/handoffs"
        files = list(handoffs.glob("pre-compact-*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "Redis for caching" in content

    def test_no_session_allows(self, env):
        e, _ = env
        e["NC_SESSION"] = ""
        inp = json.dumps({"last_assistant_message": "test"})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_empty_message_at_interval_allows(self, env):
        e, tmp = env
        e["COMPACTION_EXTRACT_INTERVAL"] = "2"
        # Empty message — even at interval, should not extract
        inp = json.dumps({"last_assistant_message": ""})
        run(e, inp)
        stdout, rc = run(e, inp)  # 2nd call, at interval
        result = json.loads(stdout)
        # Should allow (no content to extract)
        assert result.get("continue") is True
