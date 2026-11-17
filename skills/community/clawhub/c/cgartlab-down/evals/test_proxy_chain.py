#!/usr/bin/env python3
"""Unit tests for scripts/proxy_chain.py.

Stdlib only (unittest). No network. Mocks os.environ and ~/.downrc to
test chain resolution and deduplication logic.

Run via:
    python -m unittest evals.test_proxy_chain -v
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Make scripts/ importable when run from repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import proxy_chain as pc  # noqa: E402
from proxy_chain import resolve_chain, main  # noqa: E402


class TestBuiltinDefaults(unittest.TestCase):
    """BUILTIN_PROXY_CHAIN is hardcoded and ordered."""

    def test_builtin_chain_has_three_entries(self):
        self.assertEqual(len(pc.BUILTIN_PROXY_CHAIN), 3)

    def test_builtin_chain_order(self):
        # Hermes-verified first, then Clash default, then LAN fallback.
        self.assertEqual(pc.BUILTIN_PROXY_CHAIN[0], "http://127.0.0.1:7897")
        self.assertEqual(pc.BUILTIN_PROXY_CHAIN[1], "http://127.0.0.1:7890")
        self.assertEqual(pc.BUILTIN_PROXY_CHAIN[2], "http://192.168.31.135:7890")

    def test_builtin_chain_unique(self):
        self.assertEqual(len(pc.BUILTIN_PROXY_CHAIN), len(set(pc.BUILTIN_PROXY_CHAIN)))


class TestChainResolution(unittest.TestCase):
    """resolve_chain() builds the ordered, deduplicated chain."""

    def test_no_env_no_config_yields_direct_plus_builtins(self):
        """Empty env, no config → direct + 3 builtins = 4 entries."""
        with patch.dict(os.environ, {}, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    r = resolve_chain()
        # direct + 3 builtins
        self.assertEqual(len(r["chain"]), 4)
        self.assertEqual(r["chain"][0]["type"], "direct")
        self.assertEqual(r["chain"][1]["type"], "builtin")
        self.assertEqual(r["chain"][1]["proxy"], "http://127.0.0.1:7897")

    def test_env_only_env_before_builtins(self):
        """HTTPS_PROXY env → env entry before builtins, deduped with builtins."""
        env = {
            "HTTPS_PROXY": "http://127.0.0.1:7897",
            "NO_PROXY": "localhost,127.0.0.1",
        }
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    r = resolve_chain()
        # direct + env(7897) + builtins without 7897 (deduped) = 4
        self.assertEqual(len(r["chain"]), 4)
        # order: direct, env, builtin(7890), builtin(135:7890)
        self.assertEqual(r["chain"][0]["type"], "direct")
        self.assertEqual(r["chain"][1]["type"], "env")
        self.assertEqual(r["chain"][1]["proxy"], "http://127.0.0.1:7897")
        self.assertEqual(r["chain"][2]["type"], "builtin")
        self.assertEqual(r["chain"][2]["proxy"], "http://127.0.0.1:7890")

    def test_env_http_and_https_proxy_both_added(self):
        """Both HTTPS_PROXY and HTTP_PROXY → two env entries."""
        env = {
            "HTTPS_PROXY": "http://127.0.0.1:7897",
            "HTTP_PROXY": "http://127.0.0.1:8080",
            "NO_PROXY": "localhost",
        }
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    r = resolve_chain()
        # direct + 2 env + 2 builtins (7897 deduped with env) = 5
        self.assertEqual(len(r["chain"]), 5)
        env_types = [e for e in r["chain"] if e["type"] == "env"]
        self.assertEqual(len(env_types), 2)

    def test_config_file_adds_extra_proxies(self):
        """~/.downrc with proxy_chain → config entries added."""
        env = {"NO_PROXY": "localhost"}
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                config_path = Path(tmp) / "downrc"
                config_path.write_text(
                    json.dumps({"proxy_chain": ["http://1.2.3.4:1080", "http://5.6.7.8:1080"]}),
                    encoding="utf-8"
                )
                with patch.object(pc, "_resolve_config_path", return_value=config_path):
                    r = resolve_chain()
        # direct + 3 builtins + 2 config = 6
        self.assertEqual(len(r["chain"]), 6)
        file_types = [e for e in r["chain"] if e["type"] == "file"]
        self.assertEqual(len(file_types), 2)
        self.assertTrue(r["config_exists"])

    def test_env_config_and_builtin_deduped(self):
        """Same proxy in env + config + builtin → appears only once (env wins)."""
        env = {
            "HTTPS_PROXY": "http://127.0.0.1:7897",
            "NO_PROXY": "localhost",
        }
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                config_path = Path(tmp) / "downrc"
                # Config contains duplicates of env and builtin
                config_path.write_text(
                    json.dumps({"proxy_chain": ["http://127.0.0.1:7897", "http://127.0.0.1:7890"]}),
                    encoding="utf-8"
                )
                with patch.object(pc, "_resolve_config_path", return_value=config_path):
                    r = resolve_chain()
        # All duplicates collapsed. Env has 7897, builtin has 7897/7890.
        # deduped: direct + env(7897) + builtin(7890) + builtin(135:7890) = 4
        self.assertEqual(len(r["chain"]), 4)

    def test_empty_config_proxy_chain(self):
        """Config with empty proxy_chain list → behaves like no config."""
        env = {"NO_PROXY": "localhost"}
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                config_path = Path(tmp) / "downrc"
                config_path.write_text(
                    json.dumps({"proxy_chain": []}), encoding="utf-8"
                )
                with patch.object(pc, "_resolve_config_path", return_value=config_path):
                    r = resolve_chain()
        # direct + 3 builtins = 4
        self.assertEqual(len(r["chain"]), 4)

    def test_malformed_config_json_ignored(self):
        """Invalid JSON in ~/.downrc → config ignored, no crash."""
        env = {"NO_PROXY": "localhost"}
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                config_path = Path(tmp) / "downrc"
                config_path.write_text("{ this is not valid json }}}", encoding="utf-8")
                with patch.object(pc, "_resolve_config_path", return_value=config_path):
                    r = resolve_chain()
        # Falls back to direct + 3 builtins = 4
        self.assertEqual(len(r["chain"]), 4)

    def test_noproxy_returned(self):
        """NO_PROXY env is returned as-is for caller to match against target."""
        env = {"NO_PROXY": "localhost,127.0.0.1,::1,sensenova.cn"}
        with patch.dict(os.environ, env, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    r = resolve_chain()
        self.assertEqual(r["noproxy"], "localhost,127.0.0.1,::1,sensenova.cn")

    def test_config_file_field_always_present(self):
        """config_file and config_exists are always in output."""
        with patch.dict(os.environ, {}, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    r = resolve_chain()
        self.assertIn("config_file", r)
        self.assertIn("config_exists", r)
        self.assertFalse(r["config_exists"])


class TestMainCLI(unittest.TestCase):
    """main() emits valid JSON on stdout."""

    def test_main_emits_json(self):
        buf = io.StringIO()
        with patch.dict(os.environ, {"NO_PROXY": "localhost"}, clear=True):
            with tempfile.TemporaryDirectory() as tmp:
                with patch.object(pc, "_resolve_config_path",
                                  return_value=Path(tmp) / "nonexistent.downrc"):
                    with contextlib.redirect_stdout(buf):
                        rc = main(["--json"])
        self.assertEqual(rc, 0)
        d = json.loads(buf.getvalue())
        self.assertIn("chain", d)
        self.assertIn("noproxy", d)
        self.assertIn("config_exists", d)
        # First entry is always direct
        self.assertEqual(d["chain"][0]["type"], "direct")


class TestConfigFileLoading(unittest.TestCase):
    """_load_config handles file errors gracefully."""

    def test_load_nonexistent_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = pc._load_config(Path(tmp) / "nonexistent.downrc")
            self.assertIsNone(result)

    def test_load_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "downrc"
            p.write_text(json.dumps({"proxy_chain": ["http://x:1"]}), encoding="utf-8")
            result = pc._load_config(p)
            self.assertEqual(result["proxy_chain"], ["http://x:1"])

    def test_load_invalid_json_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "downrc"
            p.write_text("{ invalid", encoding="utf-8")
            result = pc._load_config(p)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
