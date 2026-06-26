#!/usr/bin/env python3
"""Unit tests for notify.py"""

import io
import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import urllib.error

# Add scripts directory to path for importing notify module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notify


class TestNotify(unittest.TestCase):
    """Test cases for notify module."""

    def test_send_remote_success(self):
        """Test send_remote returns True on successful POST."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = notify.send_remote("Test message", "Test title", "Glass")
            self.assertTrue(result)

    def test_send_remote_failure(self):
        """Test send_remote returns False when URLError is raised."""
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
            result = notify.send_remote("Test message", "Test title", "Glass")
            self.assertFalse(result)

    def test_send_osc9_in_tmux(self):
        """Test send_osc9 uses DCS passthrough when TMUX env is set."""
        with patch.dict(os.environ, {"TMUX": "tmux-session"}):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                notify.send_osc9("Test message", "Test title")
                output = mock_stdout.getvalue()
                # Should contain DCS passthrough sequence
                self.assertIn("\033Ptmux;", output)
                self.assertIn("Test title: Test message", output)

    def test_send_osc9_no_tmux(self):
        """Test send_osc9 sends direct OSC 9 when no TMUX env."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                notify.send_osc9("Test message", "Test title")
                output = mock_stdout.getvalue()
                # Should start with OSC 9 sequence
                self.assertTrue(output.startswith("\033]9;"))
                self.assertIn("Test title: Test message", output)
                # Should NOT contain tmux passthrough
                self.assertNotIn("Ptmux", output)

    def test_detect_bundle_id_warp(self):
        """Test detect_bundle_id maps WarpTerminal correctly."""
        with patch.dict(os.environ, {"TERM_PROGRAM": "WarpTerminal"}):
            result = notify.detect_bundle_id()
            self.assertEqual(result, "dev.warp.Warp-Stable")

    def test_detect_bundle_id_iterm(self):
        """Test detect_bundle_id maps iTerm.app correctly."""
        with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}):
            result = notify.detect_bundle_id()
            self.assertEqual(result, "com.googlecode.iterm2")

    def test_detect_bundle_id_unknown(self):
        """Test detect_bundle_id returns None for unrecognized terminal."""
        with patch.dict(os.environ, {"TERM_PROGRAM": "UnknownTerminal"}):
            result = notify.detect_bundle_id()
            self.assertIsNone(result)

    def test_send_local_with_bundle_id(self):
        """Test send_local passes -activate flag when bundle ID is detected."""
        with patch.dict(os.environ, {"TERM_PROGRAM": "WarpTerminal"}):
            with patch("subprocess.run") as mock_run:
                notify.send_local("Test message", "Test title", "Glass")
                mock_run.assert_called_once()
                args = mock_run.call_args[0][0]
                self.assertIn("-activate", args)
                self.assertIn("dev.warp.Warp-Stable", args)
                self.assertIn("Test message", args)

    def test_send_local_without_bundle_id(self):
        """Test send_local omits -activate flag when no bundle ID detected."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("subprocess.run") as mock_run:
                notify.send_local("Test message", "Test title", "Glass")
                mock_run.assert_called_once()
                args = mock_run.call_args[0][0]
                self.assertNotIn("-activate", args)
                self.assertIn("Test message", args)

    def test_notify_no_terminal_notifier_tries_remote(self):
        """Test notify falls back to remote when terminal-notifier not found."""
        with patch("shutil.which", return_value=None):
            with patch("notify.send_remote", return_value=True) as mock_remote:
                with patch("notify.send_osc9") as mock_osc9:
                    notify.notify("Test message")
                    mock_remote.assert_called_once_with("Test message", "Claude Code", "Glass")
                    # Should not fall back to OSC 9 if remote succeeds
                    mock_osc9.assert_not_called()

    def test_notify_no_terminal_notifier_falls_back_osc9(self):
        """Test notify falls back to OSC 9 when remote fails."""
        with patch("shutil.which", return_value=None):
            with patch("notify.send_remote", return_value=False):
                with patch("notify.send_osc9") as mock_osc9:
                    notify.notify("Test message", "Test title")
                    mock_osc9.assert_called_once_with("Test message", "Test title")

    def test_notify_with_terminal_notifier(self):
        """Test notify calls send_local when terminal-notifier is available."""
        with patch("shutil.which", return_value="/usr/local/bin/terminal-notifier"):
            with patch("notify.send_local") as mock_local:
                notify.notify("Test message", "Test title", "Ping")
                mock_local.assert_called_once_with("Test message", "Test title", "Ping")


if __name__ == "__main__":
    unittest.main()
