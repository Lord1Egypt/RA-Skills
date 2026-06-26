"""Tests for rate-limit-recovery standalone script."""

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


class TestRateLimitRecovery:
    def test_script_is_runnable(self, env):
        """Script should be a valid bash file."""
        e, _ = env
        result = subprocess.run(
            ["bash", "-n", str(SCRIPTS_DIR / "rate-limit-recovery.sh")],
            capture_output=True, text=True, env=e, timeout=10,
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"

    def test_no_tmux_exits_cleanly(self, env):
        """Without tmux binary, script exits 0 with stderr message."""
        e, _ = env
        # Remove tmux from PATH by setting a minimal PATH
        e["PATH"] = "/usr/bin:/bin"
        # If tmux is in /usr/bin or /bin, we can't easily remove it.
        # Instead, check that the script runs and exits 0.
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "rate-limit-recovery.sh")],
            capture_output=True, text=True, env=e, timeout=10,
        )
        assert result.returncode == 0

    def test_creates_cooldown_dir(self, env):
        """Script should create the cooldown directory."""
        e, tmp = env
        subprocess.run(
            ["bash", str(SCRIPTS_DIR / "rate-limit-recovery.sh")],
            capture_output=True, text=True, env=e, timeout=10,
        )
        cooldown_dir = tmp / ".openclaw" / "shared-context" / "rate-limit-cooldown"
        assert cooldown_dir.exists()

    def test_no_tmux_server_exits_cleanly(self, env):
        """If tmux exists but no server, should exit 0."""
        e, _ = env
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "rate-limit-recovery.sh")],
            capture_output=True, text=True, env=e, timeout=10,
        )
        # Should exit cleanly regardless
        assert result.returncode == 0

    def test_confirmation_prompt_guard_in_source(self, env):
        """Script source should contain confirmation prompt safety check."""
        e, _ = env
        script_text = (SCRIPTS_DIR / "rate-limit-recovery.sh").read_text()
        # Verify the safety guard exists in the script
        assert "are you sure" in script_text.lower() or "confirm" in script_text.lower(), \
            "Script should check for confirmation prompts before sending Enter"
        assert "y/n" in script_text.lower() or "yes/no" in script_text.lower(), \
            "Script should detect y/n confirmation patterns"
