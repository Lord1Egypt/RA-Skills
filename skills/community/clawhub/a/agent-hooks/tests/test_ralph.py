"""Tests for Ralph persistent execution loop scripts."""

import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


@pytest.fixture
def ralph_env(tmp_path):
    """Create isolated session-scoped state directories."""
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    # Create the expected directory structure
    sessions = tmp_path / ".openclaw" / "shared-context" / "sessions"
    sessions.mkdir(parents=True)
    return env, tmp_path


def run_script(script_name, env, stdin_data="", args=None):
    """Run a bash script and return (stdout, returncode)."""
    cmd = ["bash", str(SCRIPTS_DIR / script_name)]
    if args:
        cmd.extend(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        input=stdin_data, timeout=10,
    )
    return result.stdout.strip(), result.returncode


def session_dir(tmp, session_id):
    return tmp / ".openclaw" / "shared-context" / "sessions" / session_id


class TestRalphInit:
    def test_creates_state_file(self, ralph_env):
        env, tmp = ralph_env
        stdout, rc = run_script("ralph-init.sh", env, args=["test-sess", "20"])
        assert rc == 0
        state_file = session_dir(tmp, "test-sess") / "ralph.json"
        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert state["session_id"] == "test-sess"
        assert state["active"] is True
        assert state["iteration"] == 0
        assert state["max_iterations"] == 20

    def test_default_max_iterations(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["test-sess"])
        state_file = session_dir(tmp, "test-sess") / "ralph.json"
        state = json.loads(state_file.read_text())
        assert state["max_iterations"] == 50

    def test_missing_session_id_fails(self, ralph_env):
        env, _ = ralph_env
        _, rc = run_script("ralph-init.sh", env, args=[])
        assert rc != 0

    def test_crash_recovery_resumes(self, ralph_env):
        """Simulate crash: init, run 5 iterations, then re-init should resume."""
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["crash-test", "50"])
        # Simulate 5 iterations by modifying state
        state_file = session_dir(tmp, "crash-test") / "ralph.json"
        state = json.loads(state_file.read_text())
        state["iteration"] = 5
        state_file.write_text(json.dumps(state))
        # Re-init (crash recovery)
        stdout, rc = run_script("ralph-init.sh", env, args=["crash-test", "50"])
        assert rc == 0
        assert "Resuming" in stdout
        state = json.loads(state_file.read_text())
        assert state["iteration"] == 5  # Preserved, not reset
        assert state["active"] is True


class TestRalphStopHook:
    def test_allows_when_no_session(self, ralph_env):
        env, _ = ralph_env
        env.pop("NC_SESSION", None)
        stdout, rc = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_allows_when_no_state_file(self, ralph_env):
        env, _ = ralph_env
        env["NC_SESSION"] = "nonexistent-session"
        stdout, rc = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_blocks_when_active(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["block-test", "10"])
        env["NC_SESSION"] = "block-test"
        stdout, rc = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        assert rc == 0
        result = json.loads(stdout)
        assert result.get("decision") == "block"
        assert "RALPH LOOP 1/10" in result.get("reason", "")

    def test_increments_iteration(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["inc-test", "10"])
        env["NC_SESSION"] = "inc-test"
        run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        assert "RALPH LOOP 2/10" in result.get("reason", "")

    def test_allows_after_max_iterations(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["max-test", "3"])
        env["NC_SESSION"] = "max-test"
        for _ in range(3):
            run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        assert result.get("continue") is True

    def test_allows_when_inactive(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["inactive-test", "10"])
        state_file = session_dir(tmp, "inactive-test") / "ralph.json"
        state = json.loads(state_file.read_text())
        state["active"] = False
        state_file.write_text(json.dumps(state))
        env["NC_SESSION"] = "inactive-test"
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        assert result.get("continue") is True


    def test_allows_on_auth_error(self, ralph_env):
        """Safety valve: auth errors in last_assistant_message should allow stop."""
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["auth-test", "50"])
        env["NC_SESSION"] = "auth-test"
        hook_input = json.dumps({
            "session_id": "auth-test",
            "last_assistant_message": "Error: 401 Unauthorized - API key expired",
        })
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data=hook_input)
        result = json.loads(stdout)
        assert result.get("continue") is True
        state = json.loads((session_dir(tmp, "auth-test") / "ralph.json").read_text())
        assert state["deactivation_reason"] == "auth_error"

    def test_allows_on_stale_timeout(self, ralph_env):
        """Safety valve: >2 hours idle should allow stop."""
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["stale-test", "50"])
        # Manually set last_checked_at to 3 hours ago
        state_file = session_dir(tmp, "stale-test") / "ralph.json"
        state = json.loads(state_file.read_text())
        from datetime import datetime, timedelta, timezone
        three_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        state["last_checked_at"] = three_hours_ago
        state_file.write_text(json.dumps(state))
        env["NC_SESSION"] = "stale-test"
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        assert result.get("continue") is True
        state = json.loads(state_file.read_text())
        assert state["deactivation_reason"] == "stale"

    def test_expired_cancel_is_ignored(self, ralph_env):
        """Expired cancel signal should be cleaned up, ralph continues."""
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["expire-test", "50"])
        # Create an expired cancel signal (expires_at in the past)
        cancel_file = session_dir(tmp, "expire-test") / "cancel.json"
        cancel_file.write_text(json.dumps({
            "requested_at": "2020-01-01T00:00:00Z",
            "expires_at": "2020-01-01T00:00:30Z",
            "reason": "old_cancel",
        }))
        env["NC_SESSION"] = "expire-test"
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        # Ralph should block (expired cancel ignored, ralph still active)
        assert result.get("decision") == "block"
        # Expired cancel file should be cleaned up
        assert not cancel_file.exists()


class TestRalphCancel:
    def test_creates_cancel_signal(self, ralph_env):
        env, tmp = ralph_env
        stdout, rc = run_script("ralph-cancel.sh", env, args=["cancel-test"])
        assert rc == 0
        cancel_file = session_dir(tmp, "cancel-test") / "cancel.json"
        assert cancel_file.exists()
        signal = json.loads(cancel_file.read_text())
        assert "requested_at" in signal
        assert "expires_at" in signal
        assert signal["reason"] == "user_abort"

    def test_custom_reason(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-cancel.sh", env, args=["cancel-test", "timeout"])
        cancel_file = session_dir(tmp, "cancel-test") / "cancel.json"
        signal = json.loads(cancel_file.read_text())
        assert signal["reason"] == "timeout"

    def test_cancel_stops_ralph(self, ralph_env):
        env, tmp = ralph_env
        run_script("ralph-init.sh", env, args=["cancel-flow", "50"])
        run_script("ralph-cancel.sh", env, args=["cancel-flow"])
        env["NC_SESSION"] = "cancel-flow"
        stdout, _ = run_script("ralph-stop-hook.sh", env, stdin_data="{}")
        result = json.loads(stdout)
        assert result.get("continue") is True
        state_file = session_dir(tmp, "cancel-flow") / "ralph.json"
        state = json.loads(state_file.read_text())
        assert state["active"] is False
        assert state["deactivation_reason"] == "cancelled"
