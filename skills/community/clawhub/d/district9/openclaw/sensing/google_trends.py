"""Google Trends sensor (optional dependency: pytrends)."""

from .base import BaseSensor, Signal


class GoogleTrendsSensor(BaseSensor):
    """Scan Google Trends for trending searches (requires pytrends)."""

    name = "google_trends"

    def scan(self) -> list[Signal]:
        try:
            from pytrends.request import TrendReq
        except ImportError:
            return [Signal(
                source="google_trends",
                keyword="pytrends not installed",
                score=0,
                context="Install with: pip install openclaw[sensors]",
            )]

        try:
            pytrends = TrendReq(hl="en-US", tz=360)
            trending = pytrends.trending_searches(pn="united_states")

            signals = []
            for i, row in trending.head(10).iterrows():
                keyword = str(row[0])
                signals.append(Signal(
                    source="google_trends",
                    keyword=keyword,
                    score=80.0 - i * 5,
                    context=f"'{keyword}' is trending on Google in the US.",
                ))
            return signals
        except Exception:
            return []
