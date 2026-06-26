"""Tests for bracket-hook stop hook."""

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
        ["bash", str(SCRIPTS_DIR / "bracket-hook.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestBracketHook:
    def test_first_call_creates_state(self, env):
        e, tmp = env
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
        state = tmp / ".openclaw/shared-context/sessions/test-sess/bracket.json"
        assert state.exists()
        data = json.loads(state.read_text())
        assert data["total_turns"] == 1
        assert data["session_start"] > 0

    def test_increments_turn_count(self, env):
        e, tmp = env
        inp = json.dumps({})
        run(e, inp)
        run(e, inp)
        run(e, inp)
        state = tmp / ".openclaw/shared-context/sessions/test-sess/bracket.json"
        data = json.loads(state.read_text())
        assert data["total_turns"] == 3

    def test_no_session_allows(self, env):
        e, _ = env
        e["NC_SESSION"] = ""
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_long_session_warns(self, env):
        e, tmp = env
        # Pre-seed state with session_start far in the past (3 hours ago)
        session_dir = tmp / ".openclaw/shared-context/sessions/test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        import time
        old_start = int(time.time()) - (3 * 3600)
        state_file = session_dir / "bracket.json"
        state_file.write_text(json.dumps({
            "total_turns": 50,
            "session_start": old_start,
            "total_duration_s": 10800,
            "last_turn": "2026-01-01T00:00:00Z",
        }))
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        ctx = result.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "WARNING" in ctx
        assert "hours" in ctx

    def test_records_last_turn_timestamp(self, env):
        e, tmp = env
        run(e, json.dumps({}))
        state = tmp / ".openclaw/shared-context/sessions/test-sess/bracket.json"
        data = json.loads(state.read_text())
        assert "last_turn" in data
        assert "T" in data["last_turn"]  # ISO format
