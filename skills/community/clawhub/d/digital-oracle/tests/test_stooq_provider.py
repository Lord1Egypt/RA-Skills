from __future__ import annotations

import unittest
from datetime import datetime

from digital_oracle.providers import PriceHistoryQuery, StooqProvider


class FakePriceFetcher:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str]] = []

    def fetch_history(
        self,
        symbol: str,
        *,
        period: str,
        interval: str,
    ) -> list[dict[str, object]]:
        self.calls.append((symbol, period, interval))
        return [
            {
                "Date": datetime(2026, 4, 10),
                "Open": 100.0,
                "High": 105.0,
                "Low": 99.0,
                "Close": 104.0,
                "Volume": 12345,
            }
        ]


class StooqProviderTests(unittest.TestCase):
    def test_maps_us_equities_to_yahoo_symbols(self) -> None:
        fetcher = FakePriceFetcher()
        provider = StooqProvider(fetcher=fetcher)

        history = provider.get_history(PriceHistoryQuery(symbol="spy.us", limit=1))

        self.assertEqual(fetcher.calls[0][0], "SPY")
        self.assertEqual(history.symbol, "SPY")
        self.assertEqual(history.raw_symbol, "spy.us")
        self.assertEqual(history.provider_id, "stooq")

    def test_maps_commodities_and_fx_pairs(self) -> None:
        fetcher = FakePriceFetcher()
        provider = StooqProvider(fetcher=fetcher)

        provider.get_history(PriceHistoryQuery(symbol="xauusd", limit=1))
        provider.get_history(PriceHistoryQuery(symbol="usdcny", limit=1))

        self.assertEqual(fetcher.calls[0][0], "GC=F")
        self.assertEqual(fetcher.calls[1][0], "USDCNY=X")

    def test_passes_through_unknown_symbols_uppercased(self) -> None:
        fetcher = FakePriceFetcher()
        provider = StooqProvider(fetcher=fetcher)

        provider.get_history(PriceHistoryQuery(symbol="^vix", limit=1))

        self.assertEqual(fetcher.calls[0][0], "^VIX")


if __name__ == "__main__":
    unittest.main()
