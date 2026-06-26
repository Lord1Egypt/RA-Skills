"""
Chart Library Python wrapper — thin HTTP client for the Chart Library API.

Usage:
    from wrapper import ChartLibrary

    cl = ChartLibrary()  # uses CHART_LIBRARY_API_KEY env var
    results = cl.search("AAPL 2024-06-15")
    analysis = cl.analyze("AAPL 2024-06-15")
    picks = cl.discover()
"""

import os
from typing import Any

import requests


class ChartLibraryError(Exception):
    """Raised when the Chart Library API returns an error."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ChartLibrary:
    """Thin wrapper over the Chart Library HTTP API."""

    DEFAULT_BASE_URL = "https://chartlibrary.io"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int = 30,
    ):
        self.api_key = api_key or os.environ.get("CHART_LIBRARY_API_KEY")
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "chart-library-python/1.0.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        self._session.headers.update(headers)

    def _post(self, path: str, body: dict) -> dict:
        """Make an authenticated POST request."""
        url = f"{self.base_url}{path}"
        resp = self._session.post(url, json=body, timeout=self.timeout)
        if not resp.ok:
            detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise ChartLibraryError(f"API error {resp.status_code}: {detail}", resp.status_code)
        return resp.json()

    def _get(self, path: str) -> dict:
        """Make an authenticated GET request."""
        url = f"{self.base_url}{path}"
        resp = self._session.get(url, timeout=self.timeout)
        if not resp.ok:
            detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise ChartLibraryError(f"API error {resp.status_code}: {detail}", resp.status_code)
        return resp.json()

    def search(
        self,
        query: str,
        timeframe: str = "auto",
        top_n: int = 10,
    ) -> dict[str, Any]:
        """Search for similar historical chart patterns.

        Args:
            query: Ticker + date, e.g. "AAPL 2024-06-15" or "TSLA 6/15/24 3d"
            timeframe: Session type — "auto", "rth", "premarket", "rth_3d", "rth_5d", "rth_10d"
            top_n: Number of results to return (1-50)

        Returns:
            Dict with "query", "results" (list of matches), "count", "timeframe"
        """
        return self._post("/api/v1/search/text", {
            "query": query,
            "timeframe": timeframe,
            "top_n": top_n,
        })

    def follow_through(self, results: list[dict]) -> dict[str, Any]:
        """Compute forward returns for search results.

        Args:
            results: List of match dicts from search() — each needs symbol, date, timeframe

        Returns:
            Dict with "horizon_returns" ({1: [...], 3: [...], 5: [...], 10: [...]}),
            "all_paths", "weighted_stats"
        """
        return self._post("/api/v1/follow-through", {"results": results})

    def summary(
        self,
        query_label: str,
        n_matches: int,
        horizon_returns: dict[int, list[float]],
    ) -> dict[str, Any]:
        """Generate an AI plain-English summary of pattern results.

        Args:
            query_label: Human-readable label, e.g. "AAPL 2024-06-15"
            n_matches: Number of matches
            horizon_returns: Forward returns by horizon day

        Returns:
            Dict with "summary" (string)
        """
        return self._post("/api/v1/summary", {
            "query_label": query_label,
            "n_matches": n_matches,
            "horizon_returns": horizon_returns,
        })

    def analyze(
        self,
        query: str,
        timeframe: str = "auto",
        top_n: int = 10,
        include_summary: bool = True,
    ) -> dict[str, Any]:
        """Full analysis pipeline: search + follow-through + summary in one call.

        This is the recommended method — it uses the combined /api/v1/analyze endpoint
        for a single round trip instead of 3 separate calls.

        Args:
            query: Ticker + date, e.g. "AAPL 2024-06-15"
            timeframe: Session type
            top_n: Number of results
            include_summary: Whether to include AI summary

        Returns:
            Dict with "results", "follow_through", "outcome_distribution", "summary"
        """
        return self._post("/api/v1/analyze", {
            "query": query,
            "timeframe": timeframe,
            "top_n": top_n,
            "include_summary": include_summary,
        })

    def discover(self) -> dict[str, Any]:
        """Get today's most interesting chart patterns from the daily scanner.

        Returns:
            Dict with "picks" (list of pattern dicts with ticker, summary, stats)
        """
        return self._get("/api/v1/discover/picks")

    def status(self) -> dict[str, Any]:
        """Get database statistics.

        Returns:
            Dict with total embeddings, symbol count, date range, coverage
        """
        return self._get("/api/v1/status")
