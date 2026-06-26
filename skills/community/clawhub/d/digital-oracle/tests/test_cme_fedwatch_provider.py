from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from digital_oracle.providers.base import ProviderParseError
from digital_oracle.providers.cme_fedwatch import CMEFedWatchProvider

SAMPLE_RESPONSE = {
    "meetings": [
        {
            "meetingDate": "2026-05-07",
            "currentTarget": "425-450",
            "probabilities": {
                "400-425": "12.5",
                "425-450": "65.3",
                "450-475": "22.2",
            },
        },
        {
            "meetingDate": "2026-06-18",
            "currentTarget": "425-450",
            "probabilities": {
                "375-400": "5.0",
                "400-425": "30.0",
                "425-450": "50.0",
                "450-475": "15.0",
            },
        },
    ]
}

SAMPLE_LIST_FORMAT = [
    {
        "meetingDate": "2026-05-07",
        "currentTarget": "425-450",
        "probabilities": {
            "425-450": "80.0",
            "450-475": "20.0",
        },
    }
]

SAMPLE_ZERO_PROBS = {
    "meetings": [
        {
            "meetingDate": "2026-05-07",
            "currentTarget": "425-450",
            "probabilities": {
                "400-425": "0",
                "425-450": "100.0",
                "450-475": "0.0",
            },
        }
    ]
}

SAMPLE_EMPTY = {"meetings": []}


class FakeJsonClient:
    def __init__(self, data: Any = None) -> None:
        self.data = data
        self.calls: list[tuple[str, Mapping[str, object] | None]] = []

    def get_json(self, url: str, *, params: Mapping[str, object] | None = None) -> Any:
        self.calls.append((url, params))
        return self.data


class CMEFedWatchProviderTests(unittest.TestCase):
    def test_parse_meetings(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient(SAMPLE_RESPONSE))
        meetings = provider.get_probabilities()
        self.assertEqual(len(meetings), 2)

        m1 = meetings[0]
        self.assertEqual(m1.meeting_date, "2026-05-07")
        self.assertAlmostEqual(m1.current_target_low, 4.25)
        self.assertAlmostEqual(m1.current_target_high, 4.50)
        self.assertEqual(len(m1.probabilities), 3)
        self.assertAlmostEqual(m1.probabilities[0].probability, 0.125)
        self.assertAlmostEqual(m1.probabilities[0].target_low, 4.00)
        self.assertAlmostEqual(m1.probabilities[0].target_high, 4.25)

    def test_list_format(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient(SAMPLE_LIST_FORMAT))
        meetings = provider.get_probabilities()
        self.assertEqual(len(meetings), 1)
        self.assertEqual(meetings[0].meeting_date, "2026-05-07")
        self.assertEqual(len(meetings[0].probabilities), 2)

    def test_zero_probs_filtered(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient(SAMPLE_ZERO_PROBS))
        meetings = provider.get_probabilities()
        self.assertEqual(len(meetings), 1)
        probs = meetings[0].probabilities
        self.assertEqual(len(probs), 1)
        self.assertAlmostEqual(probs[0].probability, 1.0)

    def test_empty_meetings(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient(SAMPLE_EMPTY))
        meetings = provider.get_probabilities()
        self.assertEqual(len(meetings), 0)

    def test_invalid_response_raises(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient("not json"))
        with self.assertRaises(ProviderParseError):
            provider.get_probabilities()

    def test_probabilities_sum_roughly_one(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient(SAMPLE_RESPONSE))
        meetings = provider.get_probabilities()
        for m in meetings:
            total = sum(p.probability for p in m.probabilities)
            self.assertAlmostEqual(total, 1.0, places=2)


class CMEFedWatchMetadataTests(unittest.TestCase):
    def test_describe(self) -> None:
        provider = CMEFedWatchProvider(http_client=FakeJsonClient())
        meta = provider.describe()
        self.assertEqual(meta.provider_id, "cme_fedwatch")
        self.assertIn("FedWatch", meta.display_name)
        self.assertIn("rate_probabilities", meta.capabilities)


if __name__ == "__main__":
    unittest.main()
