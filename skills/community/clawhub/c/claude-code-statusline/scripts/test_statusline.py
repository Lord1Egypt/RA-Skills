#!/usr/bin/env python3
"""Unit tests for statusline.py"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import statusline


class TestFormatTokens(unittest.TestCase):

    def test_below_thousand(self):
        self.assertEqual(statusline.format_tokens(500), "500")
        self.assertEqual(statusline.format_tokens(0), "0")
        self.assertEqual(statusline.format_tokens(999), "999")

    def test_thousands(self):
        self.assertEqual(statusline.format_tokens(1000), "1.0K")
        self.assertEqual(statusline.format_tokens(1500), "1.5K")
        self.assertEqual(statusline.format_tokens(8500), "8.5K")
        self.assertEqual(statusline.format_tokens(10000), "10.0K")

    def test_large_numbers(self):
        self.assertEqual(statusline.format_tokens(100000), "100.0K")
        self.assertEqual(statusline.format_tokens(200500), "200.5K")

    def test_negative_returns_zero(self):
        self.assertEqual(statusline.format_tokens(-1), "0")

    def test_non_int_returns_zero(self):
        self.assertEqual(statusline.format_tokens("abc"), "0")
        self.assertEqual(statusline.format_tokens(None), "0")


class TestSanitize(unittest.TestCase):

    def test_strips_ansi_codes(self):
        result = statusline._sanitize("\033[31mhello\033[0m")
        self.assertEqual(result, "hello")

    def test_strips_control_chars(self):
        result = statusline._sanitize("hello\x00world\x07")
        self.assertEqual(result, "helloworld")

    def test_truncates(self):
        result = statusline._sanitize("a" * 200, 10)
        self.assertEqual(len(result), 10)

    def test_preserves_normal_text(self):
        result = statusline._sanitize("hello world")
        self.assertEqual(result, "hello world")


class TestSafeInt(unittest.TestCase):

    def test_extracts_nested_int(self):
        data = {"a": {"b": {"c": 42}}}
        self.assertEqual(statusline._safe_int(data, "a", "b", "c"), 42)

    def test_returns_default_for_missing_key(self):
        self.assertEqual(statusline._safe_int({}, "a", "b", default=5), 5)

    def test_returns_default_for_null(self):
        self.assertEqual(statusline._safe_int({"a": None}, "a"), 0)

    def test_returns_default_for_negative(self):
        self.assertEqual(statusline._safe_int({"a": -1}, "a"), 0)

    def test_converts_float_to_int(self):
        self.assertEqual(statusline._safe_int({"a": 3.7}, "a"), 3)

    def test_returns_default_for_string(self):
        self.assertEqual(statusline._safe_int({"a": "not a number"}, "a"), 0)


class TestSafeStr(unittest.TestCase):

    def test_extracts_nested_string(self):
        data = {"model": {"display_name": "Opus 4.5"}}
        self.assertEqual(statusline._safe_str(data, "model", "display_name"), "Opus 4.5")

    def test_returns_default_for_missing(self):
        self.assertEqual(statusline._safe_str({}, "a", default="fallback"), "fallback")

    def test_returns_default_for_non_string(self):
        self.assertEqual(statusline._safe_str({"a": 42}, "a", default="x"), "x")

    def test_sanitizes_output(self):
        data = {"a": "hello\033[31m world"}
        result = statusline._safe_str(data, "a")
        self.assertNotIn("\033", result)


class TestParseColor(unittest.TestCase):

    def test_color_name(self):
        self.assertEqual(statusline._parse_color("green"), "\033[32m")
        self.assertEqual(statusline._parse_color("RED"), "\033[31m")

    def test_numeric_code(self):
        self.assertEqual(statusline._parse_color("32"), "\033[32m")
        self.assertEqual(statusline._parse_color("38;5;208"), "\033[38;5;208m")

    def test_escape_sequence(self):
        self.assertEqual(statusline._parse_color("\\033[32m"), "\033[32m")

    def test_invalid_returns_none(self):
        self.assertIsNone(statusline._parse_color("rainbow"))
        self.assertIsNone(statusline._parse_color(""))


class TestGetPctColor(unittest.TestCase):

    def setUp(self):
        self.cfg = dict(statusline.DEFAULTS)

    def test_green_below_yellow(self):
        color = statusline.get_pct_color(10, self.cfg)
        self.assertEqual(color, self.cfg["COLOR_GREEN"])

    def test_yellow_at_threshold(self):
        color = statusline.get_pct_color(40, self.cfg)
        self.assertEqual(color, self.cfg["COLOR_YELLOW"])

    def test_orange_at_threshold(self):
        color = statusline.get_pct_color(50, self.cfg)
        self.assertEqual(color, self.cfg["COLOR_ORANGE"])

    def test_red_at_threshold(self):
        color = statusline.get_pct_color(70, self.cfg)
        self.assertEqual(color, self.cfg["COLOR_RED"])

    def test_red_at_100(self):
        color = statusline.get_pct_color(100, self.cfg)
        self.assertEqual(color, self.cfg["COLOR_RED"])


class TestLoadConfig(unittest.TestCase):

    def test_returns_defaults_when_no_file(self):
        cfg = statusline.load_config("/nonexistent/path")
        self.assertEqual(cfg["TOKEN_DISPLAY"], "separate")
        self.assertEqual(cfg["THRESHOLD_YELLOW"], 40)

    def test_loads_valid_config(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("TOKEN_DISPLAY=combined\nTHRESHOLD_RED=90\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            self.assertEqual(cfg["TOKEN_DISPLAY"], "combined")
            self.assertEqual(cfg["THRESHOLD_RED"], 90)
        finally:
            os.unlink(tmp)

    def test_ignores_unknown_keys(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("UNKNOWN=value\nTOKEN_DISPLAY=separate\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            self.assertNotIn("UNKNOWN", cfg)
        finally:
            os.unlink(tmp)

    def test_skips_comments_and_blanks(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("# comment\n\nTHRESHOLD_YELLOW=30\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            self.assertEqual(cfg["THRESHOLD_YELLOW"], 30)
        finally:
            os.unlink(tmp)

    def test_rejects_bad_permissions(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("TOKEN_DISPLAY=combined\n")
            tmp = f.name
        os.chmod(tmp, 0o644)  # too permissive
        try:
            cfg = statusline.load_config(tmp)
            self.assertEqual(cfg["TOKEN_DISPLAY"], "separate")  # default, not "combined"
        finally:
            os.unlink(tmp)

    def test_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            real = Path(d) / "real.config"
            real.write_text("TOKEN_DISPLAY=combined\n")
            os.chmod(str(real), 0o600)
            link = Path(d) / "link.config"
            link.symlink_to(real)
            cfg = statusline.load_config(str(link))
            self.assertEqual(cfg["TOKEN_DISPLAY"], "separate")  # default

    def test_resets_bad_threshold_ordering(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("THRESHOLD_YELLOW=80\nTHRESHOLD_ORANGE=50\nTHRESHOLD_RED=30\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            # Should reset to defaults
            self.assertEqual(cfg["THRESHOLD_YELLOW"], 40)
            self.assertEqual(cfg["THRESHOLD_ORANGE"], 50)
            self.assertEqual(cfg["THRESHOLD_RED"], 70)
        finally:
            os.unlink(tmp)

    def test_loads_color_names(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("COLOR_GREEN=cyan\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            self.assertEqual(cfg["COLOR_GREEN"], "\033[36m")
        finally:
            os.unlink(tmp)

    def test_rejects_invalid_threshold(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".config", delete=False) as f:
            f.write("THRESHOLD_YELLOW=abc\n")
            tmp = f.name
        os.chmod(tmp, 0o600)
        try:
            cfg = statusline.load_config(tmp)
            self.assertEqual(cfg["THRESHOLD_YELLOW"], 40)  # default
        finally:
            os.unlink(tmp)


class TestGetGitAheadBehind(unittest.TestCase):

    def _mock_upstream_exists(self, mock_run, ahead="0", behind="0"):
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="origin/main\n"),  # upstream check
            MagicMock(returncode=0, stdout=f"{ahead}\n"),     # ahead count
            MagicMock(returncode=0, stdout=f"{behind}\n"),    # behind count
        ]

    @patch("statusline.subprocess.run")
    def test_ahead_only(self, mock_run):
        self._mock_upstream_exists(mock_run, ahead="3", behind="0")
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "↑3")

    @patch("statusline.subprocess.run")
    def test_behind_only(self, mock_run):
        self._mock_upstream_exists(mock_run, ahead="0", behind="2")
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "↓2")

    @patch("statusline.subprocess.run")
    def test_ahead_and_behind(self, mock_run):
        self._mock_upstream_exists(mock_run, ahead="2", behind="1")
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "↑2↓1")

    @patch("statusline.subprocess.run")
    def test_neither_ahead_nor_behind(self, mock_run):
        self._mock_upstream_exists(mock_run, ahead="0", behind="0")
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "")

    @patch("statusline.subprocess.run")
    def test_no_upstream(self, mock_run):
        mock_run.return_value = MagicMock(returncode=128, stdout="")
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "")

    @patch("statusline.subprocess.run", side_effect=FileNotFoundError)
    def test_returns_empty_when_git_missing(self, _):
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "")

    @patch("statusline.subprocess.run", side_effect=subprocess.TimeoutExpired("git", 5))
    def test_returns_empty_on_timeout(self, _):
        self.assertEqual(statusline.get_git_ahead_behind("/repo"), "")


class TestVisibleLen(unittest.TestCase):

    def test_plain_text(self):
        self.assertEqual(statusline.visible_len("hello"), 5)

    def test_strips_ansi(self):
        s = "\033[32mhello\033[0m"
        self.assertEqual(statusline.visible_len(s), 5)

    def test_empty_string(self):
        self.assertEqual(statusline.visible_len(""), 0)

    def test_multiple_ansi_codes(self):
        s = "\033[32m\033[1mhi\033[0m there\033[31m!"
        self.assertEqual(statusline.visible_len(s), len("hi there!"))

    def test_no_ansi(self):
        self.assertEqual(statusline.visible_len("plain text"), 10)


class TestRenderProgressBar(unittest.TestCase):

    def setUp(self):
        self.cfg = dict(statusline.DEFAULTS)

    def test_zero_percent(self):
        bar = statusline.render_progress_bar(0, self.cfg, width=10)
        self.assertIn("░" * 10, bar)
        self.assertIn("0%", bar)

    def test_100_percent(self):
        bar = statusline.render_progress_bar(100, self.cfg, width=10)
        self.assertIn("█" * 10, bar)
        self.assertIn("100%", bar)

    def test_50_percent(self):
        bar = statusline.render_progress_bar(50, self.cfg, width=10)
        self.assertIn("█" * 5, bar)
        self.assertIn("░" * 5, bar)
        self.assertIn("50%", bar)

    def test_clamps_above_100(self):
        bar = statusline.render_progress_bar(150, self.cfg, width=10)
        self.assertIn("█" * 10, bar)
        self.assertIn("100%", bar)

    def test_clamps_below_0(self):
        bar = statusline.render_progress_bar(-5, self.cfg, width=10)
        self.assertIn("░" * 10, bar)
        self.assertIn("0%", bar)

    def test_default_width(self):
        bar = statusline.render_progress_bar(50, self.cfg)
        # Default width=20, so 10 filled + 10 empty
        stripped = statusline.visible_len(bar)
        # [████████████████████ 50%] = 1 + 20 + 1 + len(" 50%") + 1 = 27
        self.assertIn("█" * 10, bar)
        self.assertIn("░" * 10, bar)

    def test_color_coding_green(self):
        bar = statusline.render_progress_bar(10, self.cfg)
        self.assertIn(self.cfg["COLOR_GREEN"], bar)

    def test_color_coding_red(self):
        bar = statusline.render_progress_bar(80, self.cfg)
        self.assertIn(self.cfg["COLOR_RED"], bar)


class TestGetGitBranch(unittest.TestCase):

    @patch("statusline.subprocess.run")
    def test_returns_branch_name(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="main\n")
        result = statusline.get_git_branch("/some/repo")
        self.assertEqual(result, "main")

    @patch("statusline.subprocess.run")
    def test_returns_short_hash_on_detached(self, mock_run):
        mock_run.side_effect = [
            MagicMock(returncode=1, stdout=""),  # symbolic-ref fails
            MagicMock(returncode=0, stdout="abc1234\n"),  # rev-parse succeeds
        ]
        result = statusline.get_git_branch("/some/repo")
        self.assertEqual(result, "abc1234")

    @patch("statusline.subprocess.run", side_effect=FileNotFoundError)
    def test_returns_empty_when_git_missing(self, _):
        result = statusline.get_git_branch("/some/repo")
        self.assertEqual(result, "")

    @patch("statusline.subprocess.run")
    def test_sanitizes_branch_name(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="\033[31mevil\033[0m\n")
        result = statusline.get_git_branch("/repo")
        self.assertNotIn("\033", result)
        self.assertEqual(result, "evil")


class TestRender(unittest.TestCase):

    def _make_data(self, **overrides):
        data = {
            "workspace": {"current_dir": "/tmp/test-project"},
            "model": {"display_name": "Opus 4.5"},
            "context_window": {
                "context_window_size": 200000,
                "current_usage": {
                    "input_tokens": 8500,
                    "output_tokens": 1200,
                    "cache_creation_input_tokens": 5000,
                    "cache_read_input_tokens": 2000,
                },
            },
        }
        for k, v in overrides.items():
            if k in data["context_window"]["current_usage"]:
                data["context_window"]["current_usage"][k] = v
            elif k in data["context_window"]:
                data["context_window"][k] = v
            elif k in data:
                data[k] = v
        return data

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="main")
    @patch("statusline.socket.gethostname", return_value="macbook.local")
    @patch.dict(os.environ, {"USER": "testuser"})
    def test_full_output(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)

        self.assertIn("testuser@macbook", result)
        self.assertIn("test-project", result)
        self.assertIn("(main)", result)
        self.assertIn("Opus 4.5", result)
        self.assertIn("In:8.5K", result)
        self.assertIn("Out:1.2K", result)
        self.assertIn("Cache:7.0K", result)
        # Progress bar should be present
        self.assertIn("█", result)
        self.assertIn("░", result)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="↑2↓1")
    @patch("statusline.get_git_branch", return_value="main")
    @patch("statusline.socket.gethostname", return_value="macbook.local")
    @patch.dict(os.environ, {"USER": "testuser"})
    def test_ahead_behind(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertIn("(main↑2↓1)", result)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_no_git_branch(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertNotIn("(", result)

    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_no_token_data(self, mock_host, mock_git, mock_ab):
        data = {
            "workspace": {"current_dir": "/tmp"},
            "model": {"display_name": "Sonnet"},
            "context_window": {
                "context_window_size": 200000,
                "current_usage": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                },
            },
        }
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertIn("Sonnet", result)
        self.assertNotIn("In:", result)
        self.assertNotIn("█", result)  # No progress bar when no tokens

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_combined_mode(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        cfg["TOKEN_DISPLAY"] = "combined"
        result = statusline.render(data, cfg)
        self.assertIn("Tokens:", result)
        self.assertNotIn("In:", result)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_percentage_clamped_to_100(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data(context_window_size=100, input_tokens=200)
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertIn("100%]", result)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_zero_context_size(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data(context_window_size=0, input_tokens=100)
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        # Should not crash; division by zero protected
        self.assertIn("100%]", result)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_home_directory_shows_tilde(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        data["workspace"]["current_dir"] = str(Path.home())
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertIn("~", result)

    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_missing_fields_use_defaults(self, mock_host, mock_git, mock_ab):
        data = {}
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        self.assertIn("unknown", result)  # default model name

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((50, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="↑1")
    @patch("statusline.get_git_branch", return_value="very-long-feature-branch-name")
    @patch("statusline.socket.gethostname", return_value="macbook.local")
    @patch.dict(os.environ, {"USER": "testuser"})
    def test_dynamic_two_line_split(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        # Should split into two lines when too wide
        self.assertIn("\n", result)
        lines = result.split("\n")
        self.assertEqual(len(lines), 2)
        # Second line should have the progress bar
        self.assertIn("█", lines[1])

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="main")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_single_line_when_fits(self, mock_host, mock_git, mock_ab, mock_term):
        data = self._make_data()
        cfg = dict(statusline.DEFAULTS)
        result = statusline.render(data, cfg)
        # Wide terminal -- should be single line
        self.assertNotIn("\n", result)
        self.assertIn("█", result)


class TestMain(unittest.TestCase):

    @patch("statusline.load_config", return_value=dict(statusline.DEFAULTS))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_invalid_json_exits_1(self, mock_host, mock_git, mock_ab, mock_cfg):
        with patch("sys.stdin", MagicMock(buffer=MagicMock(read=MagicMock(return_value=b"not json")))):
            with patch("builtins.print") as mock_print:
                with self.assertRaises(SystemExit) as ctx:
                    statusline.main()
                self.assertEqual(ctx.exception.code, 1)

    @patch("statusline.os.get_terminal_size", return_value=os.terminal_size((200, 24)))
    @patch("statusline.load_config", return_value=dict(statusline.DEFAULTS))
    @patch("statusline.get_git_ahead_behind", return_value="")
    @patch("statusline.get_git_branch", return_value="main")
    @patch("statusline.socket.gethostname", return_value="host")
    @patch.dict(os.environ, {"USER": "u"})
    def test_valid_json_prints_output(self, mock_host, mock_git, mock_ab, mock_cfg, mock_term):
        data = json.dumps({
            "workspace": {"current_dir": "/tmp"},
            "model": {"display_name": "Test"},
            "context_window": {
                "context_window_size": 200000,
                "current_usage": {
                    "input_tokens": 1000,
                    "output_tokens": 500,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                },
            },
        }).encode()
        with patch("sys.stdin", MagicMock(buffer=MagicMock(read=MagicMock(return_value=data)))):
            with patch("builtins.print") as mock_print:
                statusline.main()
                output = mock_print.call_args[0][0]
                self.assertIn("Test", output)
                self.assertIn("(main)", output)


if __name__ == "__main__":
    unittest.main()
