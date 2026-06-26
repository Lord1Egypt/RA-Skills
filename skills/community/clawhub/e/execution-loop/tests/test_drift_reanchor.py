"""Tests for drift-reanchor stop hook."""

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
        ["bash", str(SCRIPTS_DIR / "drift-reanchor.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestDriftReanchor:
    def test_first_call_inits_state(self, env):
        e, tmp = env
        stdout, rc = run(e, json.dumps({"last_assistant_message": "hello"}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
        # State file should exist with turn_count=1
        state = tmp / ".openclaw/shared-context/sessions/test-sess/reanchor.json"
        assert state.exists()
        data = json.loads(state.read_text())
        assert data["turn_count"] == 1

    def test_increments_count(self, env):
        e, tmp = env
        inp = json.dumps({"last_assistant_message": "working"})
        run(e, inp)  # turn 1 (init)
        run(e, inp)  # turn 2
        run(e, inp)  # turn 3
        state = tmp / ".openclaw/shared-context/sessions/test-sess/reanchor.json"
        data = json.loads(state.read_text())
        assert data["turn_count"] == 3

    def test_injects_at_interval(self, env):
        e, tmp = env
        e["REANCHOR_INTERVAL"] = "3"
        # Set up state with original_task so reminder fires
        session_dir = tmp / ".openclaw/shared-context/sessions/test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        state_file = session_dir / "reanchor.json"
        state_file.write_text(json.dumps({
            "turn_count": 2,
            "original_task": "Fix the login bug",
        }))
        inp = json.dumps({"last_assistant_message": "still working"})
        stdout, rc = run(e, inp)  # turn 3, interval=3, should fire
        assert rc == 0
        result = json.loads(stdout)
        ctx = result.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert "Fix the login bug" in ctx
        assert "TASK REMINDER" in ctx

    def test_no_inject_without_original_task(self, env):
        e, tmp = env
        e["REANCHOR_INTERVAL"] = "3"
        inp = json.dumps({"last_assistant_message": "working"})
        # First call inits (turn 1)
        run(e, inp)
        # turn 2
        run(e, inp)
        # turn 3 — interval hit but no original_task set
        stdout, rc = run(e, inp)
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_no_session_allows(self, env):
        e, _ = env
        e["NC_SESSION"] = ""
        stdout, rc = run(e, json.dumps({"last_assistant_message": "test"}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
