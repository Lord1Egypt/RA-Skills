from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from free_search.health import HealthTracker


class TestHealthTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        self.path = Path(self.tmpdir) / "test-health.jsonl"
        self.tracker = HealthTracker(storage_path=self.path)

    def test_record_and_load(self) -> None:
        self.tracker.record("brave", success=True, latency_ms=200)
        self.tracker.record("brave", success=False, latency_ms=5000, error_type="NetworkError")

        records = self.tracker._load_records(window_hours=1)
        self.assertEqual(len(records), 2)
        self.assertTrue(records[0]["success"])
        self.assertFalse(records[1]["success"])

    def test_scores_computation(self) -> None:
        # Add several successful fast records
        for _ in range(5):
            self.tracker.record("fast_provider", success=True, latency_ms=300)
        # Add several failed slow records
        for _ in range(5):
            self.tracker.record("slow_provider", success=False, latency_ms=4000, error_type="UpstreamError")

        scores = self.tracker.get_scores(window_hours=1)

        self.assertIn("fast_provider", scores)
        self.assertIn("slow_provider", scores)
        self.assertGreater(scores["fast_provider"], scores["slow_provider"])

    def test_summary(self) -> None:
        self.tracker.record("brave", success=True, latency_ms=200)
        self.tracker.record("brave", success=True, latency_ms=300)
        self.tracker.record("tavily", success=False, latency_ms=5000, error_type="AuthError")

        summary = self.tracker.get_summary(window_hours=1)

        self.assertEqual(summary["total_records"], 3)
        self.assertEqual(len(summary["providers"]), 2)

        brave = next(p for p in summary["providers"] if p["provider"] == "brave")
        self.assertEqual(brave["total_requests"], 2)
        self.assertEqual(brave["success_rate"], 1.0)

    def test_smart_order_with_insufficient_data(self) -> None:
        # With < 5 records, should return base order unchanged
        self.tracker.record("brave", success=True, latency_ms=200)
        base = ["brave", "tavily", "duckduckgo"]
        result = self.tracker.smart_order(base)
        self.assertEqual(result, base)

    def test_smart_order_with_sufficient_data(self) -> None:
        # Add enough records to trigger reordering
        for _ in range(6):
            self.tracker.record("tavily", success=True, latency_ms=200)
        for _ in range(3):
            self.tracker.record("brave", success=False, latency_ms=4000, error_type="NetworkError")

        base = ["brave", "tavily", "duckduckgo"]
        result = self.tracker.smart_order(base)

        # tavily should be first since it has better health
        self.assertEqual(result[0], "tavily")
        # duckduckgo has no data, should be at the end
        self.assertIn("duckduckgo", result)

    def test_compact(self) -> None:
        self.tracker.record("brave", success=True, latency_ms=200)
        removed = self.tracker.compact(keep_hours=1)
        self.assertEqual(removed, 0)  # All records are fresh

    def test_empty_scores(self) -> None:
        scores = self.tracker.get_scores()
        self.assertEqual(scores, {})


if __name__ == "__main__":
    unittest.main()
