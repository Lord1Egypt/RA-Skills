"""
Binance Spot API Client (Ed25519 signing)
Extracted for standalone use in binance-trade-hunter skill.
"""

import time
import base64
import logging
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter, Retry
from cryptography.hazmat.primitives.serialization import load_pem_private_key

logger = logging.getLogger("binance-client")


class BinanceClient:
    """Binance Spot API client with Ed25519 signing"""

    BASE_URL = "https://api.binance.com"

    def __init__(self, api_key: str, private_key_path: str):
        self.api_key = api_key
        with open(private_key_path, "rb") as f:
            self.private_key = load_pem_private_key(f.read(), password=None)

        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5)
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def _sign(self, params: dict) -> dict:
        """Ed25519 signature"""
        query = urlencode(params)
        sig = self.private_key.sign(query.encode("utf-8"))
        params["signature"] = base64.b64encode(sig).decode("utf-8")
        return params

    def _request(self, method: str, endpoint: str,
                 params: dict = None, signed: bool = True) -> dict:
        """Send API request"""
        if params is None:
            params = {}
        if signed:
            params = dict(params)
            params["timestamp"] = int(time.time() * 1000)
            params = self._sign(params)

        headers = {"X-MBX-APIKEY": self.api_key}
        url = f"{self.BASE_URL}{endpoint}"

        if method == "GET":
            resp = self.session.get(url, params=params,
                                   headers=headers, timeout=15)
        elif method == "POST":
            resp = self.session.post(url, params=params,
                                    headers=headers, timeout=15)
        elif method == "DELETE":
            resp = self.session.delete(url, params=params,
                                      headers=headers, timeout=15)
        else:
            raise ValueError(f"Unknown method: {method}")

        data = resp.json()
        if "code" in data and data["code"] < 0:
            logger.error(f"API error: {data}")
        return data

    # --- Account ---
    def get_account(self) -> dict:
        return self._request("GET", "/api/v3/account")

    def get_balance(self, asset: str = "USDT") -> float:
        account = self.get_account()
        for b in account.get("balances", []):
            if b["asset"] == asset:
                return float(b["free"])
        return 0.0

    def get_all_balances(self) -> dict:
        account = self.get_account()
        result = {}
        for b in account.get("balances", []):
            free = float(b["free"])
            locked = float(b["locked"])
            if free > 0 or locked > 0:
                result[b["asset"]] = free + locked
        return result

    # --- Market ---
    def get_ticker_price(self, symbol: str) -> float:
        data = self._request("GET", "/api/v3/ticker/price",
                            {"symbol": symbol}, signed=False)
        return float(data.get("price", 0))

    def get_exchange_info(self, symbol: str) -> dict:
        data = self._request("GET", "/api/v3/exchangeInfo",
                            {"symbol": symbol}, signed=False)
        for s in data.get("symbols", []):
            if s["symbol"] == symbol:
                return s
        return {}

    # --- Trade ---
    def market_buy(self, symbol: str, quote_qty: float) -> dict:
        """Market buy by USDT amount"""
        params = {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quoteOrderQty": f"{quote_qty:.2f}",
        }
        return self._request("POST", "/api/v3/order", params)

    def market_sell(self, symbol: str, qty: float,
                    step_size: str = None) -> dict:
        """Market sell by quantity"""
        if step_size:
            qty = self._truncate_qty(qty, step_size)
        params = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": f"{qty}",
        }
        return self._request("POST", "/api/v3/order", params)

    def _truncate_qty(self, qty: float, step_size: str) -> float:
        step = float(step_size)
        if step == 0:
            return qty
        step_str = f"{step:.10f}".rstrip('0')
        if '.' in step_str:
            decimals = len(step_str.split('.')[1])
        else:
            decimals = 0
        truncated = int(qty / step) * step
        return round(truncated, decimals)
