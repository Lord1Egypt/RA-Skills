#!/usr/bin/env python3
"""Tests for setup_notifications.py"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Add script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import setup_notifications as sn


class TestSetupHooks(unittest.TestCase):
    """Tests for setup_hooks function."""

    def test_setup_hooks_creates_new(self):
        """Creates hooks in empty settings.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"

            sn.setup_hooks(settings_path)

            with open(settings_path) as f:
                data = json.load(f)

            self.assertIn("hooks", data)
            self.assertIn("Notification", data["hooks"])
            self.assertEqual(len(data["hooks"]["Notification"]), 3)
            self.assertEqual(
                data["hooks"]["Notification"][0]["matcher"],
                "permission_prompt"
            )

    def test_setup_hooks_already_configured(self):
        """Skips if hooks already present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            existing_data = {
                "hooks": {
                    "Notification": [
                        {"matcher": "test", "hooks": []}
                    ]
                }
            }
            with open(settings_path, "w") as f:
                json.dump(existing_data, f)

            with mock.patch("setup_notifications.info") as mock_info:
                sn.setup_hooks(settings_path)
                mock_info.assert_called_once()

            # Should not change existing hooks
            with open(settings_path) as f:
                data = json.load(f)

            self.assertEqual(data["hooks"]["Notification"], existing_data["hooks"]["Notification"])

    def test_setup_hooks_corrupt_json_backs_up(self):
        """Backs up and recreates on invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            backup_path = Path(str(settings_path) + ".bak")

            # Write corrupt JSON
            settings_path.write_text("{invalid json")

            with mock.patch("setup_notifications.warn"):
                sn.setup_hooks(settings_path)

            # Backup should exist
            self.assertTrue(backup_path.exists())
            self.assertEqual(backup_path.read_text(), "{invalid json")

            # New settings should be valid
            with open(settings_path) as f:
                data = json.load(f)

            self.assertIn("hooks", data)


class TestCreateLaunchdPlist(unittest.TestCase):
    """Tests for create_launchd_plist function."""

    def test_create_launchd_plist_contains_paths(self):
        """Plist XML has correct paths."""
        python3_path = "/usr/bin/python3"
        scripts_dir = Path("/Users/test/.claude/scripts")
        logs_dir = Path("/Users/test/.claude/logs")

        plist = sn.create_launchd_plist(python3_path, scripts_dir, logs_dir)

        self.assertIn(python3_path, plist)
        self.assertIn(str(scripts_dir / "notify-listener.py"), plist)
        self.assertIn(str(logs_dir / "notify-listener.log"), plist)
        self.assertIn(sn.PLIST_LABEL, plist)
        self.assertIn("<?xml version", plist)
        self.assertIn("<plist version", plist)


class TestAddSshForward(unittest.TestCase):
    """Tests for add_ssh_forward function."""

    def test_add_ssh_forward_new_host(self):
        """Appends Host block with RemoteForward."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ssh_dir = Path(tmpdir) / ".ssh"
            ssh_dir.mkdir()
            ssh_config = ssh_dir / "config"
            ssh_config.write_text("# Existing config\n")

            with mock.patch("pathlib.Path.home") as mock_home:
                mock_home.return_value = Path(tmpdir)
                with mock.patch("subprocess.run") as mock_run:
                    # Mock ssh -G to return no remoteforward
                    mock_run.return_value = mock.Mock(
                        returncode=0,
                        stdout="hostname testhost\n"
                    )

                    sn.add_ssh_forward("testhost", port=19876)

            content = ssh_config.read_text()
            self.assertIn("Host testhost", content)
            self.assertIn("RemoteForward 19876 127.0.0.1:19876", content)

    def test_add_ssh_forward_existing_host(self):
        """Inserts RemoteForward into existing Host block."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ssh_dir = Path(tmpdir) / ".ssh"
            ssh_dir.mkdir()
            ssh_config = ssh_dir / "config"
            ssh_config.write_text("Host testhost\n    User testuser\n\nHost other\n")

            with mock.patch("pathlib.Path.home") as mock_home:
                mock_home.return_value = Path(tmpdir)
                with mock.patch("subprocess.run") as mock_run:
                    # Mock ssh -G to return no remoteforward
                    mock_run.return_value = mock.Mock(
                        returncode=0,
                        stdout="hostname testhost\n"
                    )

                    sn.add_ssh_forward("testhost", port=19876)

            content = ssh_config.read_text()
            lines = content.split("\n")

            # Find the Host testhost block
            host_idx = lines.index("Host testhost")
            user_idx = lines.index("    User testuser")
            remote_forward_lines = [i for i, l in enumerate(lines) if "RemoteForward" in l]

            self.assertTrue(len(remote_forward_lines) > 0)
            # RemoteForward should be before the next Host block
            remote_idx = remote_forward_lines[0]
            self.assertGreater(remote_idx, host_idx)

    def test_add_ssh_forward_already_configured(self):
        """Skips when already present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ssh_dir = Path(tmpdir) / ".ssh"
            ssh_dir.mkdir()
            ssh_config = ssh_dir / "config"
            ssh_config.write_text("Host testhost\n")

            with mock.patch("pathlib.Path.home") as mock_home:
                mock_home.return_value = Path(tmpdir)
                with mock.patch("subprocess.run") as mock_run:
                    # Mock ssh -G to return existing remoteforward
                    mock_run.return_value = mock.Mock(
                        returncode=0,
                        stdout="remoteforward 19876 127.0.0.1:19876\n"
                    )
                    with mock.patch("setup_notifications.info") as mock_info:
                        sn.add_ssh_forward("testhost", port=19876)
                        mock_info.assert_called_once()

            # Should not modify config
            content = ssh_config.read_text()
            self.assertEqual(content.count("RemoteForward"), 0)


class TestSetupLocal(unittest.TestCase):
    """Tests for setup_local function."""

    @mock.patch("setup_notifications.setup_hooks")
    @mock.patch("subprocess.run")
    @mock.patch("shutil.which")
    @mock.patch("time.sleep")
    def test_setup_local_installs_terminal_notifier(
        self, mock_sleep, mock_which, mock_run, mock_setup_hooks
    ):
        """Calls brew install when missing."""
        # First call returns None (not found), second call returns path (after install)
        mock_which.side_effect = [
            None,  # First check - not found
            "/opt/homebrew/bin/terminal-notifier",  # After install
            "/usr/bin/python3"  # python3 check
        ]

        # Mock subprocess calls
        def run_side_effect(*args, **kwargs):
            cmd = args[0]
            if "brew" in cmd:
                return mock.Mock(returncode=0, stdout="", stderr="")
            elif "lsof" in cmd:
                return mock.Mock(returncode=1, stdout="", stderr="")
            elif "launchctl" in cmd:
                return mock.Mock(returncode=0, stdout="", stderr="")
            elif str(args[0][0]).endswith("notify.py"):
                return mock.Mock(returncode=0, stdout="", stderr="")
            else:
                return mock.Mock(returncode=0, stdout="ok\n", stderr="")

        mock_run.side_effect = run_side_effect

        with tempfile.TemporaryDirectory() as tmpdir:
            script_dir = Path(tmpdir) / "scripts"
            script_dir.mkdir()
            (script_dir / "notify.py").write_text("#!/usr/bin/env python3\n")
            (script_dir / "notify-listener.py").write_text("__TERMINAL_NOTIFIER_PATH__\n")

            claude_dir = Path(tmpdir) / ".claude"
            scripts_dir = claude_dir / "scripts"
            logs_dir = claude_dir / "logs"
            scripts_dir.mkdir(parents=True)
            logs_dir.mkdir(parents=True)

            with mock.patch("setup_notifications.SCRIPTS_DIR", scripts_dir):
                with mock.patch("setup_notifications.LOGS_DIR", logs_dir):
                    with mock.patch("setup_notifications.PLIST_PATH", Path(tmpdir) / "test.plist"):
                        sn.setup_local(script_dir, claude_dir)

        # Check brew install was called
        brew_calls = [call for call in mock_run.call_args_list if "brew" in str(call)]
        self.assertTrue(len(brew_calls) > 0)

    @mock.patch("setup_notifications.setup_hooks")
    @mock.patch("subprocess.run")
    @mock.patch("shutil.which")
    @mock.patch("time.sleep")
    def test_setup_local_skips_install(
        self, mock_sleep, mock_which, mock_run, mock_setup_hooks
    ):
        """No brew when found."""
        mock_which.side_effect = [
            "/opt/homebrew/bin/terminal-notifier",  # terminal-notifier found
            "/usr/bin/python3"  # python3 found
        ]

        def run_side_effect(*args, **kwargs):
            cmd = args[0]
            if "lsof" in cmd:
                return mock.Mock(returncode=1, stdout="", stderr="")
            elif "launchctl" in cmd:
                return mock.Mock(returncode=0, stdout="", stderr="")
            elif str(args[0][0]).endswith("notify.py"):
                return mock.Mock(returncode=0, stdout="", stderr="")
            else:
                return mock.Mock(returncode=0, stdout="ok\n", stderr="")

        mock_run.side_effect = run_side_effect

        with tempfile.TemporaryDirectory() as tmpdir:
            script_dir = Path(tmpdir) / "scripts"
            script_dir.mkdir()
            (script_dir / "notify.py").write_text("#!/usr/bin/env python3\n")
            (script_dir / "notify-listener.py").write_text("__TERMINAL_NOTIFIER_PATH__\n")

            claude_dir = Path(tmpdir) / ".claude"
            scripts_dir = claude_dir / "scripts"
            logs_dir = claude_dir / "logs"
            scripts_dir.mkdir(parents=True)
            logs_dir.mkdir(parents=True)

            with mock.patch("setup_notifications.SCRIPTS_DIR", scripts_dir):
                with mock.patch("setup_notifications.LOGS_DIR", logs_dir):
                    with mock.patch("setup_notifications.PLIST_PATH", Path(tmpdir) / "test.plist"):
                        sn.setup_local(script_dir, claude_dir)

        # Check brew install was NOT called
        brew_calls = [call for call in mock_run.call_args_list if "brew" in str(call)]
        self.assertEqual(len(brew_calls), 0)


class TestSetupDevpod(unittest.TestCase):
    """Tests for setup_devpod function."""

    @mock.patch("setup_notifications.add_ssh_forward")
    @mock.patch("setup_notifications.setup_devpod_hooks")
    @mock.patch("subprocess.run")
    def test_setup_devpod_verifies_ssh(self, mock_run, mock_hooks, mock_forward):
        """SSH connectivity check."""
        # First call should succeed (echo ok)
        mock_run.side_effect = [
            mock.Mock(returncode=0, stdout="ok\n", stderr=""),  # ssh echo ok
            mock.Mock(returncode=0, stdout="", stderr=""),  # mkdir
            mock.Mock(returncode=0, stdout="", stderr=""),  # scp
            mock.Mock(returncode=0, stdout="", stderr=""),  # chmod
            mock.Mock(returncode=0, stdout="", stderr=""),  # tmux check
            mock.Mock(returncode=0, stdout="", stderr="")   # tmux reload
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            script_dir = Path(tmpdir)
            (script_dir / "notify.py").write_text("#!/usr/bin/env python3\n")

            with mock.patch("setup_notifications.SCRIPTS_DIR", Path(tmpdir) / "scripts"):
                (Path(tmpdir) / "scripts").mkdir()
                (Path(tmpdir) / "scripts" / "notify.py").write_text("#!/usr/bin/env python3\n")
                sn.setup_devpod("testhost", script_dir)

        # Verify SSH connectivity check was called
        first_call = mock_run.call_args_list[0]
        self.assertIn("ssh", first_call[0][0])
        self.assertIn("echo ok", first_call[0][0])

    @mock.patch("setup_notifications.add_ssh_forward")
    @mock.patch("setup_notifications.setup_devpod_hooks")
    @mock.patch("subprocess.run")
    def test_setup_devpod_copies_notify_script(self, mock_run, mock_hooks, mock_forward):
        """scp called for notify.py."""
        mock_run.side_effect = [
            mock.Mock(returncode=0, stdout="ok\n", stderr=""),  # ssh echo ok
            mock.Mock(returncode=0, stdout="", stderr=""),  # mkdir
            mock.Mock(returncode=0, stdout="", stderr=""),  # scp
            mock.Mock(returncode=0, stdout="", stderr=""),  # chmod
            mock.Mock(returncode=0, stdout="", stderr=""),  # tmux check
            mock.Mock(returncode=0, stdout="", stderr="")   # tmux reload
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            script_dir = Path(tmpdir)
            (script_dir / "notify.py").write_text("#!/usr/bin/env python3\n")

            with mock.patch("setup_notifications.SCRIPTS_DIR", Path(tmpdir) / "scripts"):
                (Path(tmpdir) / "scripts").mkdir()
                (Path(tmpdir) / "scripts" / "notify.py").write_text("#!/usr/bin/env python3\n")
                sn.setup_devpod("testhost", script_dir)

        # Verify scp was called
        scp_calls = [call for call in mock_run.call_args_list if "scp" in str(call)]
        self.assertTrue(len(scp_calls) > 0)

    @mock.patch("setup_notifications.add_ssh_forward")
    @mock.patch("setup_notifications.setup_devpod_hooks")
    @mock.patch("subprocess.run")
    def test_setup_devpod_configures_tmux(self, mock_run, mock_hooks, mock_forward):
        """SSH command for tmux passthrough."""
        mock_run.side_effect = [
            mock.Mock(returncode=0, stdout="ok\n", stderr=""),  # ssh echo ok
            mock.Mock(returncode=0, stdout="", stderr=""),  # mkdir
            mock.Mock(returncode=0, stdout="", stderr=""),  # scp
            mock.Mock(returncode=0, stdout="", stderr=""),  # chmod
            mock.Mock(returncode=0, stdout="", stderr=""),  # tmux check
            mock.Mock(returncode=0, stdout="", stderr="")   # tmux reload
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            script_dir = Path(tmpdir)
            (script_dir / "notify.py").write_text("#!/usr/bin/env python3\n")

            with mock.patch("setup_notifications.SCRIPTS_DIR", Path(tmpdir) / "scripts"):
                (Path(tmpdir) / "scripts").mkdir()
                (Path(tmpdir) / "scripts" / "notify.py").write_text("#!/usr/bin/env python3\n")
                sn.setup_devpod("testhost", script_dir)

        # Verify tmux config check was called
        tmux_calls = [call for call in mock_run.call_args_list if "allow-passthrough" in str(call)]
        self.assertTrue(len(tmux_calls) > 0)


class TestMain(unittest.TestCase):
    """Tests for main function."""

    @mock.patch("setup_notifications.setup_devpod")
    @mock.patch("setup_notifications.setup_local")
    @mock.patch("sys.argv", ["setup_notifications.py"])
    def test_main_local_only(self, mock_local, mock_devpod):
        """No devpod args, only local setup."""
        sn.main()

        mock_local.assert_called_once()
        mock_devpod.assert_not_called()

    @mock.patch("setup_notifications.setup_devpod")
    @mock.patch("setup_notifications.setup_local")
    @mock.patch("sys.argv", ["setup_notifications.py", "--devpod", "host1", "--devpod", "host2"])
    def test_main_with_devpods(self, mock_local, mock_devpod):
        """Multiple --devpod args trigger setup_devpod."""
        sn.main()

        mock_local.assert_called_once()
        self.assertEqual(mock_devpod.call_count, 2)

        # Verify hosts were passed correctly
        calls = [call[0][0] for call in mock_devpod.call_args_list]
        self.assertIn("host1", calls)
        self.assertIn("host2", calls)


class TestRequireMacos(unittest.TestCase):
    """Tests for require_macos platform guard."""

    @mock.patch("setup_notifications.platform.system", return_value="Linux")
    def test_exits_on_linux(self, _):
        with self.assertRaises(SystemExit) as ctx:
            sn.require_macos()
        self.assertEqual(ctx.exception.code, 1)

    @mock.patch("setup_notifications.platform.system", return_value="Darwin")
    def test_passes_on_macos(self, _):
        # Should not raise
        sn.require_macos()


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling."""

    def test_error_exits_with_code_1(self):
        """error() calls sys.exit(1)."""
        with self.assertRaises(SystemExit) as cm:
            sn.error("test error")

        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
