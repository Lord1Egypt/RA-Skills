"""
Tests for bsky CLI.
"""

import subprocess
import os

import sys

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "bsky.py")
_VENV_PYTHON = os.path.join(
    os.path.dirname(__file__), "..", "scripts", "venv", "bin", "python3"
)
VENV_PYTHON = _VENV_PYTHON if os.path.exists(_VENV_PYTHON) else sys.executable


class TestVersion:
    """Test --version flag."""

    def test_version_flag(self):
        """bsky --version should return version string."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "--version"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "bsky" in result.stdout.lower() or "1." in result.stdout


class TestDryRun:
    """Test --dry-run flag for post command."""

    def test_post_dry_run_no_auth_needed(self):
        """bsky post --dry-run should work without authentication."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "post", "Test post", "--dry-run"],
            capture_output=True,
            text=True,
        )
        # Should show preview, not error about auth
        assert "test post" in result.stdout.lower() or "dry" in result.stdout.lower()


class TestInputValidation:
    """Test input validation."""

    def test_post_empty_text_rejected(self):
        """Empty post text should be rejected."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "post", "", "--dry-run"],
            capture_output=True,
            text=True,
        )
        # Should fail or warn about empty text
        assert (
            result.returncode != 0
            or "empty" in result.stderr.lower()
            or "empty" in result.stdout.lower()
        )

    def test_post_too_long_rejected(self):
        """Post over 300 chars should be rejected."""
        long_text = "x" * 350
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "post", long_text, "--dry-run"],
            capture_output=True,
            text=True,
        )
        # Should fail or warn about length
        assert (
            result.returncode != 0
            or "long" in result.stderr.lower()
            or "char" in result.stdout.lower()
        )


class TestHelpText:
    """Test help output."""

    def test_help_flag(self):
        """bsky --help should show usage."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "--help"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "timeline" in result.stdout.lower()

    def test_post_help(self):
        """bsky post --help should show post options."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "post", "--help"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "dry" in result.stdout.lower() or "post" in result.stdout.lower()

    def test_login_help_does_not_accept_password_argument(self):
        """Login should use the hidden prompt, not a command-line secret."""
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH, "login", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--" + "password" not in result.stdout

    def test_high_impact_commands_have_confirmation_flag(self):
        """Account-changing commands should expose an explicit confirmation flag."""
        for command in ["delete", "repost", "follow", "block", "mute"]:
            result = subprocess.run(
                [VENV_PYTHON, SCRIPT_PATH, command, "--help"],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0
            assert "--yes" in result.stdout
