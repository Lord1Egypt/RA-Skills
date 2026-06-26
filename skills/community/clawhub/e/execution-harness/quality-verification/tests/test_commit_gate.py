"""Tests for test-before-commit PreToolUse hook."""

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
        ["bash", str(SCRIPTS_DIR / "test-before-commit.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestTestBeforeCommit:
    def test_non_bash_allows(self, env):
        e, _ = env
        inp = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "/tmp/x"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_non_commit_allows(self, env):
        e, _ = env
        e["TEST_BEFORE_COMMIT"] = "1"
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_disabled_by_default_allows(self, env):
        e, _ = env
        # TEST_BEFORE_COMMIT not set — feature disabled
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git commit -m 'test'"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_no_test_runner_allows(self, env, tmp_path):
        e, _ = env
        e["TEST_BEFORE_COMMIT"] = "1"
        # Run in a directory with no test runner markers
        empty_dir = tmp_path / "empty_project"
        empty_dir.mkdir()
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git commit -m 'test'"}})
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "test-before-commit.sh")],
            capture_output=True, text=True, env=e, input=inp, timeout=10,
            cwd=str(empty_dir),
        )
        stdout = result.stdout.strip()
        out = json.loads(stdout)
        assert out.get("continue") is True

    def test_amend_allows(self, env):
        e, _ = env
        e["TEST_BEFORE_COMMIT"] = "1"
        inp = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git commit --amend -m 'fix'"}})
        stdout, rc = run(e, inp)
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True
