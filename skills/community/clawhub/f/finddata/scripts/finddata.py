"""
FindData — One API for all public data.

Usage:
    from finddata import FindData

    fd = FindData(api_key="your_api_key")
    result = fd.query("Apple stock price")
    print(result)
"""

import os
import requests
from typing import Optional


class FindData:
    """Thin client for the FindData API."""

    DEFAULT_BASE_URL = "https://finddata.ai/api"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("FINDDATA_API_KEY", "")
        self.base_url = (base_url or os.environ.get("FINDDATA_BASE_URL", self.DEFAULT_BASE_URL)).rstrip("/")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers["X-API-Key"] = self.api_key
        self.session.headers["Content-Type"] = "application/json"

    def query(self, question: str, strategy: str = "smart") -> dict:
        """
        Send a natural language data question.

        Args:
            question: Any data question in plain English (or Chinese).
                      e.g. "Apple stock price", "China GDP growth", "Tesla 10-K filing"
            strategy: "smart" (LLM routing, default) or "keyword" (faster, keyword matching)

        Returns:
            dict with matched_source, confidence, suggested_function, suggested_params, etc.
        """
        resp = self.session.post(
            f"{self.base_url}/query",
            json={"query": question, "strategy": strategy},
        )
        resp.raise_for_status()
        return resp.json()

    def catalog(self) -> dict:
        """List all available data sources."""
        resp = self.session.get(f"{self.base_url}/catalog")
        resp.raise_for_status()
        return resp.json()

    def health(self) -> dict:
        """Check API health status."""
        resp = self.session.get(f"{self.base_url}/health")
        resp.raise_for_status()
        return resp.json()


# ─── Convenience function ───────────────────────────────────
_default_client: Optional[FindData] = None


def finddata(question: str, strategy: str = "smart") -> dict:
    """
    One-liner convenience function.

    Usage:
        from finddata import finddata
        result = finddata("Apple stock price")
    """
    global _default_client
    if _default_client is None:
        _default_client = FindData()
    return _default_client.query(question, strategy)


# ─── CLI demo ───────────────────────────────────────────────
if __name__ == "__main__":
    import json
    import sys

    key = os.environ.get("FINDDATA_API_KEY", "")
    fd = FindData(api_key=key)

    queries = sys.argv[1:] or [
        "Apple stock price",
        "China GDP growth rate",
        "Tesla 10-K annual report",
        "US Federal Funds Rate",
    ]

    print("=" * 60)
    print("FindData — One API for All Public Data")
    print("=" * 60)

    for q in queries:
        print(f"\n>>> {q}")
        try:
            result = fd.query(q)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"  Error: {e}")
