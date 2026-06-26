"""
Polymarket CLOB API client for orderbook / spread / depth lookups.

The CLOB API exposes Polymarket's Central Limit Order Book for real-time
pricing, depth, midpoint and spread calculations. It is publicly
accessible (no authentication required for read endpoints).

Used by the divergence trader to:
- Reject markets whose spread eats too much of the edge
- Cap position size to a small fraction of top-of-book depth
"""

import json
import logging
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

CLOB_API_BASE = "https://clob.polymarket.com"


class ClobClient:
    """Minimal read-only CLOB client using stdlib HTTP."""

    def __init__(self, base_url: str = CLOB_API_BASE, timeout: int = 6):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = f"{url}?{urlencode(filtered)}"
        try:
            req = Request(url, headers={"User-Agent": "simmer-sdk-divergence"})
            with urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except (HTTPError, URLError, json.JSONDecodeError, TimeoutError) as e:
            logger.debug("CLOB API request failed: %s %s", url, e)
            return None

    def midpoint(self, token_id: str) -> Optional[float]:
        data = self._get("/midpoint", {"token_id": token_id})
        if not isinstance(data, dict):
            return None
        try:
            return float(data.get("mid"))
        except (TypeError, ValueError):
            return None

    def orderbook(self, token_id: str) -> Optional[Dict[str, Any]]:
        """Return raw orderbook dict with bids/asks arrays."""
        return self._get("/book", {"token_id": token_id})

    def book_summary(self, token_id: str) -> Optional[Dict[str, float]]:
        """Return {best_bid, best_ask, spread, bid_depth_usd, ask_depth_usd}.

        Depth is sized in USD at the top of book (price * size for the best level).
        Returns None on any fetch / parse error so callers can degrade gracefully.
        """
        book = self.orderbook(token_id)
        if not isinstance(book, dict):
            return None

        bids = book.get("bids") or []
        asks = book.get("asks") or []
        if not bids or not asks:
            return None

        try:
            # Polymarket returns bids sorted high→low, asks low→high; both as
            # [{"price": "0.45", "size": "1234"}, ...]
            best_bid = float(bids[0]["price"])
            best_ask = float(asks[0]["price"])
            bid_depth = float(bids[0]["size"]) * best_bid
            ask_depth = float(asks[0]["size"]) * best_ask
        except (KeyError, ValueError, TypeError, IndexError):
            return None

        # Some markets return inverted orderbooks (sort order varies). Guard.
        if best_bid > best_ask:
            best_bid, best_ask = best_ask, best_bid
            bid_depth, ask_depth = ask_depth, bid_depth

        return {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": best_ask - best_bid,
            "mid": (best_bid + best_ask) / 2,
            "bid_depth_usd": bid_depth,
            "ask_depth_usd": ask_depth,
        }
