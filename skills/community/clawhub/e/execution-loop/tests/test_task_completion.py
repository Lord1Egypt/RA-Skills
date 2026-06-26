"""Tests for task-completion-gate stop hook."""

import json
import os
import subprocess
import time
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
        ["bash", str(SCRIPTS_DIR / "task-completion-gate.sh")],
        capture_output=True, text=True, env=env, input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


def make_task_file(path, tasks):
    """Create a .harness-tasks.json file at the given path."""
    data = {"tasks": tasks}
    path.write_text(json.dumps(data))


class TestTaskCompletionGate:
    def test_no_checklist_allows(self, env):
        e, _ = env
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_all_done_allows(self, env):
        e, tmp = env
        session_dir = tmp / ".openclaw" / "shared-context" / "sessions" / "test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        make_task_file(session_dir / ".harness-tasks.json", [
            {"name": "Write tests", "done": True},
            {"name": "Fix bug", "done": True},
        ])
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_items_remaining_blocks(self, env):
        e, tmp = env
        session_dir = tmp / ".openclaw" / "shared-context" / "sessions" / "test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        make_task_file(session_dir / ".harness-tasks.json", [
            {"name": "Write tests", "done": True},
            {"name": "Fix lint", "done": False},
            {"name": "Update docs", "done": False},
        ])
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("decision") == "block"
        assert "Fix lint" in result.get("reason", "")
        assert "Update docs" in result.get("reason", "")

    def test_stale_checklist_allows(self, env):
        e, tmp = env
        session_dir = tmp / ".openclaw" / "shared-context" / "sessions" / "test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        task_file = session_dir / ".harness-tasks.json"
        make_task_file(task_file, [
            {"name": "Old task", "done": False},
        ])
        # Set mtime to 25 hours ago
        old_time = time.time() - (25 * 3600)
        os.utime(str(task_file), (old_time, old_time))
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_no_session_allows(self, env):
        e, _ = env
        e["NC_SESSION"] = ""
        stdout, rc = run(e, json.dumps({}))
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_single_remaining_blocks_with_name(self, env):
        e, tmp = env
        session_dir = tmp / ".openclaw" / "shared-context" / "sessions" / "test-sess"
        session_dir.mkdir(parents=True, exist_ok=True)
        make_task_file(session_dir / ".harness-tasks.json", [
            {"name": "Run integration tests", "done": False},
        ])
        stdout, rc = run(e, json.dumps({}))
        result = json.loads(stdout)
        assert result.get("decision") == "block"
        assert "1 unchecked" in result.get("reason", "")
        assert "Run integration tests" in result.get("reason", "")
