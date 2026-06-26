"""Tests for lib/env.py — configuration and API key loading."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import lib.env as env_mod


class TestGetConfig(unittest.TestCase):
    def test_reads_from_environ(self):
        with patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_testtoken"}, clear=False):
            config = env_mod.get_config()
            self.assertEqual(config.get("GITHUB_TOKEN"), "ghp_testtoken")

    def test_returns_dict(self):
        config = env_mod.get_config()
        self.assertIsInstance(config, dict)

    def test_has_config_source_key(self):
        config = env_mod.get_config()
        self.assertIn("_CONFIG_SOURCE", config)

    def test_reads_global_env_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("GITHUB_TOKEN=ghp_fromfile\n")
            with patch.object(env_mod, "_GLOBAL_CONFIG_FILE", env_file):
                env_backup = os.environ.pop("GITHUB_TOKEN", None)
                try:
                    config = env_mod.get_config()
                    self.assertEqual(config.get("GITHUB_TOKEN"), "ghp_fromfile")
                finally:
                    if env_backup:
                        os.environ["GITHUB_TOKEN"] = env_backup

    def test_environ_overrides_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text("GITHUB_TOKEN=ghp_fromfile\n")
            with patch.object(env_mod, "_GLOBAL_CONFIG_FILE", env_file):
                with patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_fromenv"}, clear=False):
                    config = env_mod.get_config()
                    self.assertEqual(config.get("GITHUB_TOKEN"), "ghp_fromenv")

    def test_handles_missing_env_file_gracefully(self):
        nonexistent = Path("/nonexistent/path/that/does/not/exist/.env")
        with patch.object(env_mod, "_GLOBAL_CONFIG_FILE", nonexistent):
            config = env_mod.get_config()
            self.assertIsInstance(config, dict)


class TestIsGithubAuthed(unittest.TestCase):
    """is_github_authed(config) takes config dict."""

    def test_true_when_token_set(self):
        self.assertTrue(env_mod.is_github_authed({"GITHUB_TOKEN": "ghp_test"}))

    def test_false_when_no_token(self):
        self.assertFalse(env_mod.is_github_authed({}))

    def test_false_when_token_empty_string(self):
        self.assertFalse(env_mod.is_github_authed({"GITHUB_TOKEN": ""}))


class TestIsRedditAvailable(unittest.TestCase):
    def test_true_when_key_set(self):
        self.assertTrue(env_mod.is_reddit_available({"SCRAPECREATORS_API_KEY": "sc_test"}))

    def test_false_when_no_key(self):
        self.assertFalse(env_mod.is_reddit_available({}))


class TestIsTwitterAvailable(unittest.TestCase):
    def test_true_with_xai_key(self):
        self.assertTrue(env_mod.is_twitter_available({"XAI_API_KEY": "xai_test"}))

    def test_true_with_cookie_auth(self):
        self.assertTrue(env_mod.is_twitter_available({
            "AUTH_TOKEN": "token123",
            "CT0": "ct0value"
        }))

    def test_false_with_no_keys(self):
        self.assertFalse(env_mod.is_twitter_available({}))

    def test_false_with_only_auth_token(self):
        # Need BOTH AUTH_TOKEN and CT0
        self.assertFalse(env_mod.is_twitter_available({"AUTH_TOKEN": "token"}))


class TestGithubHeaders(unittest.TestCase):
    def test_includes_auth_header_when_token_set(self):
        headers = env_mod.github_headers({"GITHUB_TOKEN": "ghp_test"})
        self.assertIn("Authorization", headers)
        self.assertIn("ghp_test", headers["Authorization"])

    def test_no_auth_header_when_no_token(self):
        headers = env_mod.github_headers({})
        self.assertNotIn("Authorization", headers)

    def test_always_includes_accept_header(self):
        headers = env_mod.github_headers({})
        self.assertIn("Accept", headers)


class TestLoadEnvFile(unittest.TestCase):
    """_load_env_file(path) — reads a Path object."""

    def test_parses_key_value_pairs(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("GITHUB_TOKEN=ghp_abc\nSTACKOVERFLOW_API_KEY=so_xyz\n")
            fname = f.name
        try:
            result = env_mod._load_env_file(Path(fname))
            self.assertEqual(result.get("GITHUB_TOKEN"), "ghp_abc")
            self.assertEqual(result.get("STACKOVERFLOW_API_KEY"), "so_xyz")
        finally:
            os.unlink(fname)

    def test_skips_comments(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("# This is a comment\nGITHUB_TOKEN=ghp_abc\n")
            fname = f.name
        try:
            result = env_mod._load_env_file(Path(fname))
            self.assertEqual(result.get("GITHUB_TOKEN"), "ghp_abc")
            self.assertEqual(len(result), 1)
        finally:
            os.unlink(fname)

    def test_strips_double_quotes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write('GITHUB_TOKEN="ghp_abc"\n')
            fname = f.name
        try:
            result = env_mod._load_env_file(Path(fname))
            self.assertEqual(result.get("GITHUB_TOKEN"), "ghp_abc")
        finally:
            os.unlink(fname)

    def test_strips_single_quotes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("GITHUB_TOKEN='ghp_abc'\n")
            fname = f.name
        try:
            result = env_mod._load_env_file(Path(fname))
            self.assertEqual(result.get("GITHUB_TOKEN"), "ghp_abc")
        finally:
            os.unlink(fname)

    def test_skips_unknown_keys(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("UNKNOWN_KEY=value\nGITHUB_TOKEN=ghp_abc\n")
            fname = f.name
        try:
            result = env_mod._load_env_file(Path(fname))
            self.assertNotIn("UNKNOWN_KEY", result)
            self.assertIn("GITHUB_TOKEN", result)
        finally:
            os.unlink(fname)

    def test_returns_empty_dict_on_missing_file(self):
        result = env_mod._load_env_file(Path("/nonexistent/file.env"))
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
