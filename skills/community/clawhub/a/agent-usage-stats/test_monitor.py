#!/usr/bin/env python3
"""Regression tests for realtime monitor summaries."""

from __future__ import annotations

import contextlib
import io
import signal
import threading
import unittest

from token_stats.monitor import _render_aligned_monitor_block, watch_agent
from token_stats.formatting import align_rows, strip_ansi


class FakeMixedModeAgent:
    @staticmethod
    def display_name() -> str:
        return "Fake CodeX"

    _has_live_context = False

    def __init__(self):
        self.collect_calls = []

    def collect(self, *, from_ts=None, to_ts=None):
        self.collect_calls.append((from_ts, to_ts))
        if from_ts is not None:
            return FakeData(
                token_mode="split",
                per_model=[
                    {
                        "model": "gpt-split",
                        "input": 30,
                        "output": 7,
                        "cache": 11,
                        "calls": 2,
                        "token_mode": "split",
                    }
                ],
            )
        return FakeData(
            token_mode="total",
            per_model=[
                {
                    "model": "gpt-split",
                    "input": 100,
                    "output": 20,
                    "cache": 40,
                    "calls": 3,
                    "token_mode": "split",
                },
                {
                    "model": "legacy-total",
                    "input": 999,
                    "output": 0,
                    "cache": 0,
                    "calls": 1,
                    "token_mode": "total",
                },
            ],
        )


class FakeIncrementAgent:
    @staticmethod
    def display_name() -> str:
        return "Fake Increment"

    _has_live_context = False

    def __init__(self):
        self.snapshot_calls = 0

    def collect(self, *, from_ts=None, to_ts=None):
        if from_ts is not None:
            return FakeData(token_mode="split", per_model=[])
        self.snapshot_calls += 1
        if self.snapshot_calls == 1:
            return FakeData(
                token_mode="split",
                per_model=[
                    {
                        "model": "gpt-split",
                        "input": 100,
                        "output": 20,
                        "cache": 40,
                        "calls": 3,
                        "token_mode": "split",
                    }
                ],
            )
        return FakeData(
            token_mode="split",
            per_model=[
                {
                    "model": "gpt-split",
                    "input": 140,
                    "output": 25,
                    "cache": 48,
                    "calls": 5,
                    "token_mode": "split",
                }
            ],
        )


class FakeData:
    def __init__(self, *, token_mode, per_model):
        self.token_mode = token_mode
        self.per_model = per_model
        self.stats = {}


def fake_helpers():
    return {
        "fmt_num": lambda n: str(n),
        "calc_cache_rate": lambda inp, cache: None if inp == 0 else cache / inp * 100,
        "fmt_cache_val": lambda cache, inp: f"缓 {cache}",
        "get_model_price": lambda model: None,
        "calc_cost": lambda inp, out, cache, price: 0,
        "calc_total_cost": lambda per_model: {},
        "fmt_cost": lambda inp, out, cache, price: "-",
        "fmt_total_cost": lambda totals: "",
        "to_cny": lambda cost, currency: cost,
        "has_any_price": lambda per_model: False,
        "align_rows": lambda rows: rows,
        "progress_bar": lambda pct: "",
    }


class MonitorSummaryTests(unittest.TestCase):
    def test_monitor_block_aligns_columns_and_rule_spans_content(self):
        lines = _render_aligned_monitor_block(
            [
                [
                    "gpt-5.5",
                    "入 +6.96K",
                    "出 +335",
                    "缓 +146.82K (95.5%)",
                    "总计/+缓存 +7.29K/+154.11K",
                    "调用 +1",
                    "≈¥2.9862",
                ],
                [
                    "codex-auto-review",
                    "入 +120",
                    "出 +9",
                    "缓 +0",
                    "总计/+缓存 +129/+129",
                    "调用 +1",
                    "≈¥0.0000",
                ],
            ],
            align_rows,
        )

        self.assertGreaterEqual(len(lines), 4)
        content = [strip_ansi(line) for line in lines[1:-1]]
        pipe_positions = [[idx for idx, ch in enumerate(line) if ch == "|"] for line in content]
        self.assertEqual(pipe_positions[0], pipe_positions[1])
        rule_width = len(strip_ansi(lines[0]).strip())
        self.assertGreaterEqual(rule_width, max(len(line.strip()) for line in content))

    def test_mixed_mode_codex_keeps_split_rows_and_uses_ranged_today(self):
        agent = FakeMixedModeAgent()
        timer = threading.Timer(0.05, lambda: signal.raise_signal(signal.SIGINT))
        buf = io.StringIO()
        timer.start()
        try:
            with contextlib.redirect_stdout(buf):
                watch_agent(agent, 1, fake_helpers())
        finally:
            timer.cancel()

        output = buf.getvalue()
        self.assertIn("gpt-split | 入 100 | 出 20 | 缓 40 | 总计/+缓存 120/160 | 调用 3", output)
        self.assertIn("legacy-total | 总计 999 | 调用 1", output)
        self.assertIn("gpt-split | 入 30 | 出 7 | 缓 11 | 总计/+缓存 37/48 | 调用 2", output)
        self.assertNotIn("gpt-split | 总计 120", output)
        self.assertTrue(any(from_ts is not None for from_ts, _ in agent.collect_calls))

    def test_monitor_period_delta_uses_today_summary_columns(self):
        agent = FakeIncrementAgent()
        timer = threading.Timer(0.05, lambda: signal.raise_signal(signal.SIGINT))
        buf = io.StringIO()
        timer.start()
        try:
            with contextlib.redirect_stdout(buf):
                watch_agent(agent, 1, fake_helpers())
        finally:
            timer.cancel()

        output = buf.getvalue()
        self.assertIn("监控期间增量:", output)
        self.assertIn("gpt-split | 入 40 | 出 5 | 缓 8 | 总计/+缓存 45/53 | 调用 2", output)
        self.assertNotIn("+45总计", output)
        self.assertNotIn("+40入", output)


if __name__ == "__main__":
    unittest.main()
