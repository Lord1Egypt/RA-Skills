"""
CoinMarketCap API Client
"""

import requests
from typing import Optional, List, Dict

from config import CMC_BASE_URL, CONVERT_ID, SYMBOL_TO_ID
from .models import Quote, KlineData


class CMCClient:
    """CoinMarketCap API 客户端"""

    def __init__(self, base_url: str = CMC_BASE_URL, convert_id: int = CONVERT_ID):
        self.base_url = base_url
        self.convert_id = convert_id
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; CryptoDataProcessor/1.0)",
        })

    def get_historical(
        self,
        symbol: str,
        currency_id: Optional[int] = None,
        interval: str = "1d",
    ) -> KlineData:
        """
        获取历史价格数据

        Args:
            symbol: 币种符号（ETH, BNB, SOL 等）
            currency_id: 币种 ID（可选，不传则从配置查）
            interval: 时间间隔（1d=日线，1h=小时线）

        Returns:
            KlineData: K 线数据集合
        """
        if currency_id is None:
            currency_id = SYMBOL_TO_ID.get(symbol.upper())
            if currency_id is None:
                raise ValueError(f"Unknown symbol: {symbol}")

        url = f"{self.base_url}/cryptocurrency/historical"
        params = {
            "id": currency_id,
            "convertId": self.convert_id,
            "interval": interval,
        }

        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()

        data = resp.json()

        if "data" not in data:
            raise ValueError(f"Invalid API response: {data}")

        quote_data = data["data"]
        quotes = []

        for q in quote_data.get("quotes", []):
            quote = Quote(
                time_open=q["timeOpen"],
                time_close=q["timeClose"],
                time_high=q["timeHigh"],
                time_low=q["timeLow"],
                open=q["quote"]["open"],
                high=q["quote"]["high"],
                low=q["quote"]["low"],
                close=q["quote"]["close"],
                volume=q["quote"]["volume"],
                market_cap=q["quote"]["marketCap"],
                circulating_supply=q["quote"]["circulatingSupply"],
                timestamp=q["quote"]["timestamp"],
            )
            quotes.append(quote)

        return KlineData(symbol=symbol.upper(), currency_id=currency_id, quotes=quotes)

    def get_symbols(self, symbols: List[str]) -> Dict[str, KlineData]:
        """批量获取多个币种数据"""
        results = {}
        for symbol in symbols:
            print(f"Fetching {symbol}...")
            try:
                results[symbol.upper()] = self.get_historical(symbol)
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                results[symbol.upper()] = None
        return results
