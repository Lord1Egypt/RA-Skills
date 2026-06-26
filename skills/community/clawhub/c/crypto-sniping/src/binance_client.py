"""Binance API client wrapper."""
import os
import hmac
import hashlib
import time
import requests
from typing import Dict, List, Optional
from urllib.parse import urlencode

class BinanceClient:
    """Binance API client with rate limiting and error handling."""
    
    BASE_URL = "https://api.binance.com"
    FAPI_URL = "https://fapi.binance.com"  # Futures
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = False):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Binance API key and secret required. Set BINANCE_API_KEY and BINANCE_API_SECRET env vars.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })
    
    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature."""
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds."""
        return int(time.time() * 1000)
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False, futures: bool = False) -> Dict:
        """Make API request."""
        base = self.FAPI_URL if futures else self.BASE_URL
        url = f"{base}{endpoint}"
        
        if params is None:
            params = {}
        
        if signed:
            params["timestamp"] = self._get_timestamp()
            query_string = urlencode(params)
            params["signature"] = self._generate_signature(query_string)
        
        if method == "GET":
            response = self.session.get(url, params=params)
        elif method == "POST":
            response = self.session.post(url, data=params)
        elif method == "DELETE":
            response = self.session.delete(url, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    # === SPOT API ===
    
    def get_account(self) -> Dict:
        """Get account information."""
        return self._request("GET", "/api/v3/account", signed=True)
    
    def get_balance(self, asset: str) -> float:
        """Get balance for specific asset."""
        account = self.get_account()
        for balance in account.get("balances", []):
            if balance["asset"] == asset:
                return float(balance["free"]) + float(balance["locked"])
        return 0.0
    
    def get_symbol_price(self, symbol: str) -> float:
        """Get current price for symbol."""
        data = self._request("GET", "/api/v3/ticker/price", {"symbol": symbol})
        return float(data["price"])
    
    def get_klines(self, symbol: str, interval: str = "1h", limit: int = 100) -> List:
        """Get OHLCV data."""
        return self._request("GET", "/api/v3/klines", {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        })
    
    def get_orderbook(self, symbol: str, limit: int = 100) -> Dict:
        """Get order book."""
        return self._request("GET", "/api/v3/depth", {
            "symbol": symbol,
            "limit": limit
        })
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: Optional[float] = None, quote_quantity: Optional[float] = None,
                   price: Optional[float] = None, stop_price: Optional[float] = None) -> Dict:
        """Place order."""
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper()
        }
        
        if quantity:
            params["quantity"] = quantity
        if quote_quantity:
            params["quoteOrderQty"] = quote_quantity
        if price:
            params["price"] = price
        if stop_price:
            params["stopPrice"] = stop_price
        
        return self._request("POST", "/api/v3/order", params, signed=True)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List:
        """Get open orders."""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/api/v3/openOrders", params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel order."""
        return self._request("DELETE", "/api/v3/order", {
            "symbol": symbol,
            "orderId": order_id
        }, signed=True)
    
    # === FUTURES API ===
    
    def get_futures_account(self) -> Dict:
        """Get futures account information."""
        return self._request("GET", "/fapi/v2/account", signed=True, futures=True)
    
    def get_futures_klines(self, symbol: str, interval: str = "1h", limit: int = 100) -> List:
        """Get futures OHLCV data."""
        return self._request("GET", "/fapi/v1/klines", {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }, futures=True)
    
    def get_funding_rate(self, symbol: str) -> float:
        """Get current funding rate."""
        data = self._request("GET", "/fapi/v1/premiumIndex", {"symbol": symbol}, futures=True)
        return float(data.get("lastFundingRate", 0))
    
    def get_liquidations(self, symbol: str, start_time: Optional[int] = None, 
                        end_time: Optional[int] = None, limit: int = 100) -> List:
        """Get forced liquidation orders."""
        params = {"symbol": symbol, "limit": limit}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return self._request("GET", "/fapi/v1/forceOrders", params, futures=True)
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> List:
        """Get recent trades."""
        return self._request("GET", "/api/v3/trades", {
            "symbol": symbol,
            "limit": limit
        })
