#!/usr/bin/env python3
"""Unit tests for statusline_installer.py"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import statusline_installer


class TestCheckJq(unittest.TestCase):

    @patch("statusline_installer.shutil.which", return_value="/usr/bin/jq")
    def test_returns_true_when_installed(self, _):
        self.assertTrue(statusline_installer.check_jq())

    @patch("statusline_installer.shutil.which", return_value=None)
    def test_returns_false_when_missing(self, _):
        self.assertFalse(statusline_installer.check_jq())


class TestValidateThreshold(unittest.TestCase):

    def test_valid_values(self):
        self.assertEqual(statusline_installer.validate_threshold("0"), 0)
        self.assertEqual(statusline_installer.validate_threshold("50"), 50)
        self.assertEqual(statusline_installer.validate_threshold("100"), 100)

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            statusline_installer.validate_threshold("-1")

    def test_rejects_over_100(self):
        with self.assertRaises(ValueError):
            statusline_installer.validate_threshold("101")

    def test_rejects_non_numeric(self):
        with self.assertRaises(ValueError):
            statusline_installer.validate_threshold("abc")


class TestValidateColor(unittest.TestCase):

    def test_valid_color_names(self):
        for name in ["green", "yellow", "orange", "red", "blue", "cyan", "magenta"]:
            result = statusline_installer.validate_color(name)
            self.assertTrue(result.startswith("\\033["))
            self.assertTrue(result.endswith("m"))

    def test_numeric_ansi_code(self):
        result = statusline_installer.validate_color("32")
        self.assertEqual(result, "\\033[32m")

    def test_extended_ansi_code(self):
        result = statusline_installer.validate_color("38;5;208")
        self.assertEqual(result, "\\033[38;5;208m")

    def test_rejects_unknown_name(self):
        with self.assertRaises(ValueError):
            statusline_installer.validate_color("rainbow")

    def test_rejects_invalid_format(self):
        with self.assertRaises(ValueError):
            statusline_installer.validate_color("not;a;color;name")


class TestWriteAndReadConfig(unittest.TestCase):

    def test_write_and_read_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "statusline.config"
            config = {
                "TOKEN_DISPLAY": "combined",
                "THRESHOLD_YELLOW": "30",
                "THRESHOLD_ORANGE": "50",
                "THRESHOLD_RED": "80",
                "COLOR_GREEN": "\\033[32m",
                "COLOR_YELLOW": "\\033[33m",
                "COLOR_ORANGE": "\\033[38;5;208m",
                "COLOR_RED": "\\033[31m",
            }
            statusline_installer.write_config(config, path)
            loaded = statusline_installer.read_config(path)
            self.assertEqual(loaded["TOKEN_DISPLAY"], "combined")
            self.assertEqual(loaded["THRESHOLD_YELLOW"], "30")
            self.assertEqual(loaded["THRESHOLD_RED"], "80")

    def test_write_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "subdir" / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, path)
            self.assertTrue(path.exists())

    def test_write_sets_permissions_600(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, path)
            perms = oct(path.stat().st_mode & 0o777)
            self.assertEqual(perms, "0o600")

    def test_read_missing_file_returns_defaults(self):
        result = statusline_installer.read_config(Path("/nonexistent/config"))
        self.assertEqual(result, statusline_installer.DEFAULT_CONFIG)

    def test_read_skips_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "statusline.config"
            path.write_text(
                "# comment\n"
                "\n"
                "TOKEN_DISPLAY=combined\n"
                "# another comment\n"
                "THRESHOLD_RED=90\n"
            )
            result = statusline_installer.read_config(path)
            self.assertEqual(result["TOKEN_DISPLAY"], "combined")
            self.assertEqual(result["THRESHOLD_RED"], "90")

    def test_read_ignores_unknown_keys(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "statusline.config"
            path.write_text("UNKNOWN_KEY=value\nTOKEN_DISPLAY=separate\n")
            result = statusline_installer.read_config(path)
            self.assertNotIn("UNKNOWN_KEY", result)
            self.assertEqual(result["TOKEN_DISPLAY"], "separate")


class TestLoadAndSaveSettings(unittest.TestCase):

    def test_load_missing_file(self):
        result = statusline_installer.load_settings(Path("/nonexistent.json"))
        self.assertEqual(result, {})

    def test_load_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json{{{")
            tmp = f.name
        try:
            result = statusline_installer.load_settings(Path(tmp))
            self.assertEqual(result, {})
        finally:
            os.unlink(tmp)

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            data = {"statusLine": {"type": "command", "command": "/path/to/script"}}
            statusline_installer.save_settings(path, data)
            loaded = statusline_installer.load_settings(path)
            self.assertEqual(loaded["statusLine"]["command"], "/path/to/script")

    def test_save_sets_permissions_600(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            statusline_installer.save_settings(path, {"key": "val"})
            perms = oct(path.stat().st_mode & 0o777)
            self.assertEqual(perms, "0o600")


class TestUpdateSettingsFile(unittest.TestCase):

    def test_adds_statusline_to_empty_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            path.write_text("{}")
            with patch.object(statusline_installer, "STATUSLINE_SCRIPT",
                              Path("/home/user/.claude/scripts/statusline.sh")):
                result = statusline_installer.update_settings_file(path)
            self.assertTrue(result)
            data = json.loads(path.read_text())
            self.assertEqual(data["statusLine"]["type"], "command")

    def test_returns_false_if_already_configured(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            script_path = "/home/user/.claude/scripts/statusline.py"
            cmd = f"python3 {script_path}"
            data = {"statusLine": {"type": "command", "command": cmd}}
            path.write_text(json.dumps(data))
            with patch.object(statusline_installer, "STATUSLINE_SCRIPT", Path(script_path)):
                result = statusline_installer.update_settings_file(path)
            self.assertFalse(result)

    def test_updates_existing_different_command(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            data = {"statusLine": {"type": "command", "command": "/old/path"}}
            path.write_text(json.dumps(data))
            new_path = "/home/user/.claude/scripts/statusline.py"
            with patch.object(statusline_installer, "STATUSLINE_SCRIPT", Path(new_path)):
                result = statusline_installer.update_settings_file(path)
            self.assertTrue(result)
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded["statusLine"]["command"], f"python3 {new_path}")


class TestRemoveFromSettings(unittest.TestCase):

    def test_removes_statusline_key(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            data = {"statusLine": {"type": "command"}, "other": "keep"}
            path.write_text(json.dumps(data))
            result = statusline_installer.remove_from_settings(path)
            self.assertTrue(result)
            loaded = json.loads(path.read_text())
            self.assertNotIn("statusLine", loaded)
            self.assertEqual(loaded["other"], "keep")

    def test_returns_false_if_no_statusline(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            path.write_text('{"other": "val"}')
            result = statusline_installer.remove_from_settings(path)
            self.assertFalse(result)

    def test_returns_false_if_file_missing(self):
        result = statusline_installer.remove_from_settings(Path("/nonexistent.json"))
        self.assertFalse(result)


class TestCmdInstall(unittest.TestCase):

    @patch("statusline_installer.update_settings_file", return_value=True)
    @patch("statusline_installer.write_config")
    @patch("statusline_installer.check_jq", return_value=True)
    @patch("statusline_installer.BUNDLED_SCRIPT")
    @patch("statusline_installer.STATUSLINE_SCRIPT")
    @patch("statusline_installer.SCRIPT_DIR")
    @patch("statusline_installer.SETTINGS_LOCAL")
    @patch("statusline_installer.SETTINGS_JSON")
    @patch("builtins.print")
    def test_install_copies_script_and_writes_config(
        self, mock_print, mock_sj, mock_sl, mock_sd, mock_ss,
        mock_bs, mock_jq, mock_wc, mock_us
    ):
        mock_bs.exists.return_value = True
        mock_sd.mkdir = MagicMock()
        mock_sl.exists.return_value = True
        mock_sl.__eq__ = lambda self, other: True
        mock_sj.exists.return_value = False

        args = MagicMock(
            token_display=None,
            threshold_yellow=None,
            threshold_orange=None,
            threshold_red=None,
        )

        with patch("statusline_installer.shutil.copy2"), \
             patch("statusline_installer.os.chmod"):
            statusline_installer.cmd_install(args)

        mock_wc.assert_called_once()
        mock_us.assert_called_once()

    @patch("statusline_installer.BUNDLED_SCRIPT")
    @patch("builtins.print")
    def test_install_exits_if_script_missing(self, mock_print, mock_bs):
        mock_bs.exists.return_value = False
        args = MagicMock()
        with self.assertRaises(SystemExit) as ctx:
            statusline_installer.cmd_install(args)
        self.assertEqual(ctx.exception.code, 1)

    @patch("statusline_installer.update_settings_file", return_value=True)
    @patch("statusline_installer.write_config")
    @patch("statusline_installer.check_jq", return_value=True)
    @patch("statusline_installer.BUNDLED_SCRIPT")
    @patch("statusline_installer.STATUSLINE_SCRIPT")
    @patch("statusline_installer.SCRIPT_DIR")
    @patch("statusline_installer.SETTINGS_LOCAL")
    @patch("statusline_installer.SETTINGS_JSON")
    @patch("builtins.print")
    def test_install_rejects_bad_threshold_order(
        self, mock_print, mock_sj, mock_sl, mock_sd, mock_ss,
        mock_bs, mock_jq, mock_wc, mock_us
    ):
        mock_bs.exists.return_value = True
        mock_sd.mkdir = MagicMock()

        args = MagicMock(
            token_display=None,
            threshold_yellow=70,
            threshold_orange=50,
            threshold_red=30,
        )

        with patch("statusline_installer.shutil.copy2"), \
             patch("statusline_installer.os.chmod"):
            with self.assertRaises(SystemExit) as ctx:
                statusline_installer.cmd_install(args)
            self.assertEqual(ctx.exception.code, 1)


class TestCmdUninstall(unittest.TestCase):

    def test_removes_script_and_reverts_settings(self):
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "statusline.sh"
            script.touch()
            settings = Path(d) / "settings.local.json"
            settings.write_text(json.dumps({
                "statusLine": {"type": "command", "command": str(script)},
                "other": "keep"
            }))

            with patch.object(statusline_installer, "STATUSLINE_SCRIPT", script), \
                 patch.object(statusline_installer, "CONFIG_FILE", Path(d) / "config"), \
                 patch.object(statusline_installer, "SETTINGS_LOCAL", settings), \
                 patch.object(statusline_installer, "SETTINGS_JSON", Path(d) / "missing.json"), \
                 patch("builtins.print"):
                args = MagicMock(remove_config=False)
                statusline_installer.cmd_uninstall(args)

            self.assertFalse(script.exists())
            loaded = json.loads(settings.read_text())
            self.assertNotIn("statusLine", loaded)
            self.assertEqual(loaded["other"], "keep")

    def test_removes_config_when_requested(self):
        with tempfile.TemporaryDirectory() as d:
            config = Path(d) / "statusline.config"
            config.write_text("TOKEN_DISPLAY=separate\n")

            with patch.object(statusline_installer, "STATUSLINE_SCRIPT", Path(d) / "missing"), \
                 patch.object(statusline_installer, "CONFIG_FILE", config), \
                 patch.object(statusline_installer, "SETTINGS_LOCAL", Path(d) / "s1.json"), \
                 patch.object(statusline_installer, "SETTINGS_JSON", Path(d) / "s2.json"), \
                 patch("builtins.print"):
                args = MagicMock(remove_config=True)
                statusline_installer.cmd_uninstall(args)

            self.assertFalse(config.exists())


class TestCmdStatus(unittest.TestCase):

    @patch("statusline_installer.shutil.which")
    @patch("builtins.print")
    def test_outputs_valid_json(self, mock_print, mock_which):
        mock_which.side_effect = lambda x: "/usr/bin/" + x if x in ("jq", "git") else None

        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "statusline.sh"
            script.touch()
            config = Path(d) / "config"
            config.write_text("TOKEN_DISPLAY=separate\n")
            settings = Path(d) / "settings.local.json"
            settings.write_text(json.dumps({
                "statusLine": {"command": str(script)}
            }))

            with patch.object(statusline_installer, "STATUSLINE_SCRIPT", script), \
                 patch.object(statusline_installer, "CONFIG_FILE", config), \
                 patch.object(statusline_installer, "SETTINGS_LOCAL", settings), \
                 patch.object(statusline_installer, "SETTINGS_JSON", Path(d) / "miss.json"):
                statusline_installer.cmd_status(MagicMock())

        output = json.loads(mock_print.call_args[0][0])
        self.assertTrue(output["script_installed"])
        self.assertTrue(output["config_exists"])
        self.assertTrue(output["git_installed"])


class TestCmdConfigure(unittest.TestCase):

    def test_updates_token_display(self):
        with tempfile.TemporaryDirectory() as d:
            config_path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, config_path)

            with patch.object(statusline_installer, "CONFIG_FILE", config_path), \
                 patch("builtins.print"):
                args = MagicMock(
                    token_display="combined",
                    threshold_yellow=None,
                    threshold_orange=None,
                    threshold_red=None,
                    color_green=None,
                    color_yellow=None,
                    color_orange=None,
                    color_red=None,
                )
                statusline_installer.cmd_configure(args)

            result = statusline_installer.read_config(config_path)
            self.assertEqual(result["TOKEN_DISPLAY"], "combined")

    def test_updates_thresholds(self):
        with tempfile.TemporaryDirectory() as d:
            config_path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, config_path)

            with patch.object(statusline_installer, "CONFIG_FILE", config_path), \
                 patch("builtins.print"):
                args = MagicMock(
                    token_display=None,
                    threshold_yellow=20,
                    threshold_orange=40,
                    threshold_red=60,
                    color_green=None,
                    color_yellow=None,
                    color_orange=None,
                    color_red=None,
                )
                statusline_installer.cmd_configure(args)

            result = statusline_installer.read_config(config_path)
            self.assertEqual(result["THRESHOLD_YELLOW"], "20")
            self.assertEqual(result["THRESHOLD_ORANGE"], "40")
            self.assertEqual(result["THRESHOLD_RED"], "60")

    def test_rejects_bad_threshold_order(self):
        with tempfile.TemporaryDirectory() as d:
            config_path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, config_path)

            with patch.object(statusline_installer, "CONFIG_FILE", config_path), \
                 patch("builtins.print"):
                args = MagicMock(
                    token_display=None,
                    threshold_yellow=80,
                    threshold_orange=50,
                    threshold_red=30,
                    color_green=None,
                    color_yellow=None,
                    color_orange=None,
                    color_red=None,
                )
                with self.assertRaises(SystemExit):
                    statusline_installer.cmd_configure(args)

    def test_updates_colors(self):
        with tempfile.TemporaryDirectory() as d:
            config_path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, config_path)

            with patch.object(statusline_installer, "CONFIG_FILE", config_path), \
                 patch("builtins.print"):
                args = MagicMock(
                    token_display=None,
                    threshold_yellow=None,
                    threshold_orange=None,
                    threshold_red=None,
                    color_green="cyan",
                    color_yellow=None,
                    color_orange=None,
                    color_red=None,
                )
                statusline_installer.cmd_configure(args)

            result = statusline_installer.read_config(config_path)
            self.assertEqual(result["COLOR_GREEN"], "\\033[36m")

    def test_no_changes_prints_current(self):
        with tempfile.TemporaryDirectory() as d:
            config_path = Path(d) / "statusline.config"
            statusline_installer.write_config(statusline_installer.DEFAULT_CONFIG, config_path)

            with patch.object(statusline_installer, "CONFIG_FILE", config_path), \
                 patch("builtins.print") as mock_print:
                args = MagicMock(
                    token_display=None,
                    threshold_yellow=None,
                    threshold_orange=None,
                    threshold_red=None,
                    color_green=None,
                    color_yellow=None,
                    color_orange=None,
                    color_red=None,
                )
                statusline_installer.cmd_configure(args)

            # Should print "No changes" message
            first_call = mock_print.call_args_list[0][0][0]
            self.assertIn("No changes", first_call)


class TestDefaultConfig(unittest.TestCase):

    def test_defaults_have_all_keys(self):
        expected_keys = {
            "TOKEN_DISPLAY", "THRESHOLD_YELLOW", "THRESHOLD_ORANGE", "THRESHOLD_RED",
            "COLOR_GREEN", "COLOR_YELLOW", "COLOR_ORANGE", "COLOR_RED",
        }
        self.assertEqual(set(statusline_installer.DEFAULT_CONFIG.keys()), expected_keys)

    def test_default_thresholds_are_ordered(self):
        y = int(statusline_installer.DEFAULT_CONFIG["THRESHOLD_YELLOW"])
        o = int(statusline_installer.DEFAULT_CONFIG["THRESHOLD_ORANGE"])
        r = int(statusline_installer.DEFAULT_CONFIG["THRESHOLD_RED"])
        self.assertLessEqual(y, o)
        self.assertLessEqual(o, r)


class TestColorToAnsi(unittest.TestCase):

    def test_all_valid_colors_have_mappings(self):
        for color in statusline_installer.VALID_COLORS:
            self.assertIn(color, statusline_installer.COLOR_TO_ANSI,
                          f"Missing ANSI mapping for '{color}'")

    def test_validate_color_accepts_all_valid_names(self):
        for color in statusline_installer.VALID_COLORS:
            result = statusline_installer.validate_color(color)
            self.assertTrue(result.startswith("\\033["), f"Bad result for '{color}': {result}")


if __name__ == "__main__":
    unittest.main()
