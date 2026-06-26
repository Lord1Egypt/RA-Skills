"""Tests for doubt gate stop hook."""

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


def run_doubt_gate(env, last_msg="", session_id="test-sess"):
    env["NC_SESSION"] = session_id
    inp = json.dumps({"last_assistant_message": last_msg})
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "doubt-gate.sh")],
        capture_output=True, text=True, env=env, input=inp, timeout=10,
    )
    return json.loads(result.stdout.strip()), result.returncode


class TestDoubtGate:
    def test_allows_concrete_response(self, env):
        e, _ = env
        result, rc = run_doubt_gate(e, "I have verified the fix by running pytest. All 12 tests pass.")
        assert result.get("continue") is True

    def test_blocks_speculative_english(self, env):
        e, _ = env
        result, _ = run_doubt_gate(e, "I think this should fix the bug. It will probably work.")
        assert result.get("decision") == "block"
        assert "evidence" in result.get("reason", "").lower() or "verify" in result.get("reason", "").lower()

    def test_blocks_speculative_chinese(self, env):
        e, _ = env
        result, _ = run_doubt_gate(e, "这个修改应该是可以解决问题的，大概不会有副作用。")
        assert result.get("decision") == "block"

    def test_allows_after_guard_fires(self, env):
        e, tmp = env
        # First call blocks
        result1, _ = run_doubt_gate(e, "I think this might work.")
        assert result1.get("decision") == "block"
        # Second call with same speculative text — guard fired, allows through
        result2, _ = run_doubt_gate(e, "I think this might work.")
        assert result2.get("continue") is True

    def test_ignores_code_blocks(self, env):
        e, _ = env
        msg = "The fix is applied.\n```python\n# I think this might need review\nresult = maybe_func()\n```\nAll tests pass."
        result, _ = run_doubt_gate(e, msg)
        assert result.get("continue") is True

    def test_allows_empty_message(self, env):
        e, _ = env
        result, _ = run_doubt_gate(e, "")
        assert result.get("continue") is True

    def test_no_session_allows(self, env):
        e, _ = env
        e.pop("NC_SESSION", None)
        e["NC_SESSION"] = ""
        inp = json.dumps({"last_assistant_message": "I think maybe this works"})
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "doubt-gate.sh")],
            capture_output=True, text=True, env=e, input=inp, timeout=10,
        )
        out = json.loads(result.stdout.strip())
        assert out.get("continue") is True
