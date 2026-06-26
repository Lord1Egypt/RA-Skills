from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from digital_oracle.providers.base import ProviderParseError
from digital_oracle.providers.fear_greed import FearGreedProvider

SAMPLE_RESPONSE = {
    "fear_and_greed": {
        "score": 32.5,
        "rating": "Fear",
        "timestamp": "2026-04-10T16:00:00.000Z",
        "previous_close": 30.1,
        "previous_1_week": 45.2,
        "previous_1_month": 55.0,
        "previous_1_year": 68.3,
    }
}

SAMPLE_EXTREME_FEAR = {
    "fear_and_greed": {
        "score": 0,
        "rating": "Extreme Fear",
        "timestamp": "2026-04-10T16:00:00.000Z",
    }
}

SAMPLE_EXTREME_GREED = {
    "fear_and_greed": {
        "score": 100,
        "rating": "Extreme Greed",
        "timestamp": "2026-04-10T16:00:00.000Z",
    }
}

SAMPLE_NO_RATING = {
    "fear_and_greed": {
        "score": 80,
        "timestamp": "2026-04-10T16:00:00.000Z",
    }
}

SAMPLE_MISSING_HISTORY = {
    "fear_and_greed": {
        "score": 50,
        "rating": "Neutral",
    }
}


class FakeJsonClient:
    def __init__(self, data: Any = None) -> None:
        self.data = data
        self.calls: list[tuple[str, Mapping[str, object] | None]] = []

    def get_json(self, url: str, *, params: Mapping[str, object] | None = None) -> Any:
        self.calls.append((url, params))
        return self.data


class FearGreedProviderTests(unittest.TestCase):
    def test_parse_full_response(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient(SAMPLE_RESPONSE))
        snap = provider.get_index()
        self.assertAlmostEqual(snap.score, 32.5)
        self.assertEqual(snap.rating, "Fear")
        self.assertEqual(snap.timestamp, "2026-04-10T16:00:00.000Z")
        self.assertAlmostEqual(snap.previous_close, 30.1)
        self.assertAlmostEqual(snap.one_week_ago, 45.2)
        self.assertAlmostEqual(snap.one_month_ago, 55.0)
        self.assertAlmostEqual(snap.one_year_ago, 68.3)

    def test_extreme_fear(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient(SAMPLE_EXTREME_FEAR))
        snap = provider.get_index()
        self.assertAlmostEqual(snap.score, 0)
        self.assertEqual(snap.rating, "Extreme Fear")

    def test_extreme_greed(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient(SAMPLE_EXTREME_GREED))
        snap = provider.get_index()
        self.assertAlmostEqual(snap.score, 100)
        self.assertEqual(snap.rating, "Extreme Greed")

    def test_derives_rating_when_missing(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient(SAMPLE_NO_RATING))
        snap = provider.get_index()
        self.assertEqual(snap.rating, "Extreme Greed")

    def test_missing_history_fields(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient(SAMPLE_MISSING_HISTORY))
        snap = provider.get_index()
        self.assertAlmostEqual(snap.score, 50)
        self.assertIsNone(snap.timestamp)
        self.assertIsNone(snap.previous_close)
        self.assertIsNone(snap.one_week_ago)
        self.assertIsNone(snap.one_month_ago)
        self.assertIsNone(snap.one_year_ago)

    def test_missing_fear_and_greed_key_raises(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient({"other": {}}))
        with self.assertRaises(ProviderParseError):
            provider.get_index()

    def test_missing_score_raises(self) -> None:
        provider = FearGreedProvider(
            http_client=FakeJsonClient({"fear_and_greed": {"rating": "Fear"}})
        )
        with self.assertRaises(ProviderParseError):
            provider.get_index()


class FearGreedProviderMetadataTests(unittest.TestCase):
    def test_describe(self) -> None:
        provider = FearGreedProvider(http_client=FakeJsonClient())
        meta = provider.describe()
        self.assertEqual(meta.provider_id, "fear_greed")
        self.assertIn("CNN", meta.display_name)
        self.assertIn("market_sentiment", meta.capabilities)


if __name__ == "__main__":
    unittest.main()
