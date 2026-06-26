"""Tests for tool error tracker and advisor scripts."""

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


def run(script, env, stdin_data="", session_id="test-sess"):
    env["NC_SESSION"] = session_id
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / script)],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


def make_failure_input(tool="Bash", command="cargo build", error="command not found: cargo"):
    return json.dumps({
        "tool_name": tool,
        "tool_input": {"command": command},
        "error": error,
    })


class TestToolErrorTracker:
    def test_first_failure_no_output(self, env):
        e, tmp = env
        stdout, rc = run("tool-error-tracker.sh", e, make_failure_input())
        assert rc == 0
        # First failure — no advice yet (count=1, threshold=3)
        assert "MUST" not in stdout

    def test_soft_threshold_at_3(self, env):
        e, tmp = env
        inp = make_failure_input()
        for _ in range(2):
            run("tool-error-tracker.sh", e, inp)
        stdout, _ = run("tool-error-tracker.sh", e, inp)
        assert "Consider" in stdout or "failed 3 times" in stdout

    def test_hard_threshold_at_5(self, env):
        e, tmp = env
        inp = make_failure_input()
        for _ in range(4):
            run("tool-error-tracker.sh", e, inp)
        stdout, _ = run("tool-error-tracker.sh", e, inp)
        assert "MUST" in stdout
        assert "alternative" in stdout.lower()

    def test_different_tool_resets_count(self, env):
        e, tmp = env
        for _ in range(4):
            run("tool-error-tracker.sh", e, make_failure_input(tool="Bash"))
        # Switch to different tool
        stdout, _ = run("tool-error-tracker.sh", e, make_failure_input(tool="Write"))
        assert "MUST" not in stdout  # Count reset to 1

    def test_state_file_created(self, env):
        e, tmp = env
        run("tool-error-tracker.sh", e, make_failure_input())
        state = tmp / ".openclaw/shared-context/sessions/test-sess/tool-errors.json"
        assert state.exists()
        data = json.loads(state.read_text())
        assert data["tool_name"] == "Bash"
        assert data["count"] == 1


class TestToolErrorAdvisor:
    def test_no_state_allows(self, env):
        e, _ = env
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cargo build"}})
        stdout, rc = run("tool-error-advisor.sh", e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_blocks_at_threshold(self, env):
        e, _ = env
        fail_inp = make_failure_input()
        for _ in range(5):
            run("tool-error-tracker.sh", e, fail_inp)
        # Now try to use same tool
        advisor_inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cargo build"}})
        stdout, _ = run("tool-error-advisor.sh", e, advisor_inp)
        result = json.loads(stdout)
        # PreToolUse uses hookSpecificOutput.permissionDecision, not top-level decision
        perm = result.get("hookSpecificOutput", {}).get("permissionDecision")
        assert perm == "deny"


class TestHashFallbackChain:
    """Verify the hash computation fallback chain in tracker/advisor."""

    def test_tracker_produces_deterministic_hash(self, env):
        """Same tool+input should produce same hash across two calls."""
        e, tmp = env
        fail_inp = make_failure_input()
        run("tool-error-tracker.sh", e, fail_inp)
        state = tmp / ".openclaw/shared-context/sessions/test-sess/tool-errors.json"
        hash1 = json.loads(state.read_text())["input_hash"]
        run("tool-error-tracker.sh", e, fail_inp)
        hash2 = json.loads(state.read_text())["input_hash"]
        assert hash1 == hash2
        assert hash1 != "unknown", "Hash should not fall through to 'unknown'"

    def test_different_input_different_hash(self, env):
        """Different tool input should produce different hash."""
        e, tmp = env
        inp1 = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cargo build"},
                           "tool_error": "not found"})
        inp2 = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cargo test"},
                           "tool_error": "not found"})
        run("tool-error-tracker.sh", e, inp1, session_id="s1")
        state1 = tmp / ".openclaw/shared-context/sessions/s1/tool-errors.json"
        hash1 = json.loads(state1.read_text())["input_hash"]
        run("tool-error-tracker.sh", e, inp2, session_id="s2")
        state2 = tmp / ".openclaw/shared-context/sessions/s2/tool-errors.json"
        hash2 = json.loads(state2.read_text())["input_hash"]
        assert hash1 != hash2
