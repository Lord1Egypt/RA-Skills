"""Unified data source: yfinance + cache + all other sources."""
import yfinance as yf
import pandas as pd
from data_cache import Cache


class UnifiedDataSource:
    def __init__(self, cache=None):
        self.cache = cache or Cache()

    def get_ticker_info(self, ticker):
        cached = self.cache.get_fundamentals(ticker)
        if cached:
            return cached
        try:
            t = yf.Ticker(ticker)
            info = t.info
            result = {
                "ticker": ticker,
                "name": info.get("longName", info.get("shortName", ticker)),
                "sector": info.get("sector", "N/A"),
                "market_cap": info.get("marketCap"),
                "pe_ttm": info.get("trailingPE"),
                "pb": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "currency": info.get("currency", "USD"),
                "exchange": info.get("exchange", ""),
                "country": info.get("country", ""),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "avg_volume": info.get("averageVolume"),
                "employees": info.get("fullTimeEmployees"),
                "website": info.get("website", ""),
                "business_summary": info.get("longBusinessSummary", "")[:500],
            }
            self.cache.set_fundamentals(ticker, result)
            return result
        except Exception:
            return self._mock_ticker_info(ticker)

    def get_price_history(self, ticker, period="1y", interval="1d"):
        cache_key = f"price:{ticker}:{period}:{interval}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period=period, interval=interval)
            if hist.empty:
                return self._mock_price_history(ticker, period)
            data = []
            for date, row in hist.tail(100).iterrows():
                data.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "open": round(row["Open"], 2),
                        "high": round(row["High"], 2),
                        "low": round(row["Low"], 2),
                        "close": round(row["Close"], 2),
                        "volume": int(row["Volume"]),
                    }
                )
            result = {
                "ticker": ticker,
                "period": period,
                "interval": interval,
                "data": data,
            }
            self.cache.set(cache_key, result, ttl_seconds=3600)
            return result
        except Exception:
            return self._mock_price_history(ticker, period)

    def get_ah_spread(self, h_ticker):
        """Calculate A-H share spread. h_ticker like 0700.HK."""
        try:
            # Load ticker map to find A-share
            import json
            import os

            map_path = os.path.join(os.path.dirname(__file__), "ticker_map.json")
            with open(map_path) as f:
                tm = json.load(f).get("tickers", {})
            info = tm.get(h_ticker, {})
            a_share = info.get("a_share")
            if not a_share:
                return {
                    "h_ticker": h_ticker,
                    "a_ticker": None,
                    "h_price": None,
                    "a_price_cny": None,
                    "spread_pct": None,
                    "note": "No A-share mapping",
                }
            h_info = self.get_ticker_info(h_ticker)
            a_info = self.get_ticker_info(a_share)
            h_price = h_info.get("regularMarketPrice") or h_info.get(
                "previousClose"
            )
            a_price = a_info.get("regularMarketPrice") or a_info.get(
                "previousClose"
            )
            if h_price and a_price:
                spread = (
                    (a_price - h_price) / h_price * 100 if h_price else None
                )
                return {
                    "h_ticker": h_ticker,
                    "a_ticker": a_share,
                    "h_price": h_price,
                    "a_price_cny": a_price,
                    "spread_pct": round(spread, 2) if spread else None,
                    "premium_discount": (
                        "premium"
                        if spread and spread > 0
                        else "discount"
                    ),
                }
            return {"h_ticker": h_ticker, "mock": True}
        except Exception:
            return {"h_ticker": h_ticker, "spread_pct": None, "mock": True}

    def _mock_ticker_info(self, ticker):
        return {
            "ticker": ticker,
            "name": f"Mock Company {ticker}",
            "sector": "Technology",
            "market_cap": 1000000000,
            "pe_ttm": 15.0,
            "currency": "HKD" if ".HK" in ticker else "USD",
            "mock": True,
        }

    def _mock_price_history(self, ticker, period):
        import random
        from datetime import date, timedelta

        data = []
        base = 100
        for i in range(30):
            d = date.today() - timedelta(days=i)
            change = random.uniform(-0.02, 0.02)
            close = base * (1 + change)
            data.append(
                {
                    "date": d.strftime("%Y-%m-%d"),
                    "open": round(close * 0.99, 2),
                    "high": round(close * 1.01, 2),
                    "low": round(close * 0.98, 2),
                    "close": round(close, 2),
                    "volume": random.randint(1000000, 10000000),
                }
            )
            base = close
        return {
            "ticker": ticker,
            "period": period,
            "interval": "1d",
            "data": data,
            "mock": True,
        }
