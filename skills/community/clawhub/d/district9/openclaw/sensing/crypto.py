"""Crypto market sensor — Fear & Greed Index + trending narratives."""

import requests

from .base import BaseSensor, Signal


class CryptoSensor(BaseSensor):
    """Reads crypto market sentiment from free APIs (no API key required)."""

    name = "crypto"

    def scan(self) -> list[Signal]:
        signals = []
        signals.extend(self._fear_greed())
        signals.extend(self._trending_coins())
        return signals

    def _fear_greed(self) -> list[Signal]:
        """Fetch Fear & Greed Index from alternative.me."""
        try:
            resp = requests.get(
                "https://api.alternative.me/fng/?limit=1",
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()["data"][0]

            value = int(data["value"])
            classification = data["value_classification"]

            # Map F&G to meme relevance:
            # Extreme fear (0-25) → contrarian "buy the dip" memes
            # Extreme greed (75-100) → euphoria/FOMO memes
            # Neutral → lower relevance
            if value <= 25 or value >= 75:
                score = 80.0
            elif value <= 40 or value >= 60:
                score = 50.0
            else:
                score = 30.0

            return [Signal(
                source="crypto",
                keyword=f"Fear & Greed: {classification}",
                score=score,
                context=f"Crypto market sentiment is '{classification}' (index: {value}/100). "
                        f"{'Extreme sentiment creates meme opportunities.' if score >= 70 else ''}",
            )]
        except Exception:
            return []

    def _trending_coins(self) -> list[Signal]:
        """Fetch trending coins from CoinGecko (free, no key)."""
        try:
            resp = requests.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=10,
            )
            resp.raise_for_status()
            coins = resp.json().get("coins", [])[:5]

            signals = []
            for i, item in enumerate(coins):
                coin = item.get("item", {})
                name = coin.get("name", "Unknown")
                symbol = coin.get("symbol", "???")
                rank = coin.get("market_cap_rank")

                signals.append(Signal(
                    source="crypto",
                    keyword=f"Trending: {name} ({symbol})",
                    score=70.0 - i * 10,
                    context=f"{name} ({symbol}) is trending on CoinGecko"
                            f"{f', rank #{rank}' if rank else ''}. "
                            f"This indicates community interest.",
                ))
            return signals
        except Exception:
            return []
