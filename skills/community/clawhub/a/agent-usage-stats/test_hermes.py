#!/usr/bin/env python3
"""Regression tests for Hermes data collection."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from token_stats import app


class HermesImmutableFallbackTests(unittest.TestCase):
    def test_collect_falls_back_to_immutable_read_when_normal_sqlite_read_fails(self):
        with tempfile.TemporaryDirectory(prefix="token-stats-hermes-fixture-") as tmp:
            db = Path(tmp) / "state.db"
            conn = sqlite3.connect(db)
            conn.execute(
                "CREATE TABLE sessions ("
                "model TEXT, input_tokens INTEGER, output_tokens INTEGER, "
                "cache_read_tokens INTEGER, api_call_count INTEGER, tool_call_count INTEGER, "
                "started_at REAL, ended_at REAL)"
            )
            conn.execute(
                "INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?)",
                ("model-a", 1000, 200, 5000, 3, 1, 100, 200),
            )
            conn.execute(
                "INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?)",
                ("model-a", 0, 0, 0, 0, 0, 300, 400),
            )
            conn.commit()
            conn.close()

            real_connect = sqlite3.connect

            class BrokenConnection:
                row_factory = None

                def execute(self, *args, **kwargs):
                    raise sqlite3.OperationalError("unable to open database file")

                def close(self):
                    pass

            def connect_side_effect(path, *args, **kwargs):
                if kwargs.get("uri"):
                    return real_connect(path, *args, **kwargs)
                return BrokenConnection()

            with mock.patch("token_stats.app._find_hermes_db", return_value=str(db)), \
                    mock.patch("token_stats.app.sqlite3.connect", side_effect=connect_side_effect):
                data = app.HermesAgent().collect()

            self.assertEqual(data.stats["input_tokens"], 1000)
            self.assertEqual(data.stats["output_tokens"], 200)
            self.assertEqual(data.stats["cache_read"], 5000)
            self.assertEqual(data.stats["api_calls"], 3)
            self.assertEqual(data.stats["session_count"], 2)
            self.assertIn("model-a", data.raw)


if __name__ == "__main__":
    unittest.main()
