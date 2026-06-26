"""
币安 API 客户端 - 封装币安 API 调用
"""

import hmac
import hashlib
import os
import time
import requests
from typing import Dict, List, Optional, Any
from config import BinanceConfig


class BinanceAPIClient:
    """币安 API 客户端"""

    def __init__(self, config: BinanceConfig):
        self.api_key = config.api_key
        self.api_secret = config.api_secret
        self.testnet = config.testnet

        # 支持多个 API URL 配置
        self.api_urls = {
            "main": "https://api.binance.com",
            "main_futures": "https://fapi.binance.com",
            "test": "https://testnet.binance.vision",
            "test_futures": "https://testnet.binancefuture.com"
        }

        # 根据配置选择 base_url
        if self.testnet:
            self.base_url = self.api_urls["test"]
        else:
            self.base_url = self.api_urls["main"]

        # 创建多个 session
        self.session = requests.Session()
        self.futures_session = requests.Session()

        # 设置 headers
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }

        self.session.headers.update(headers)
        self.futures_session.headers.update(headers)

        # 配置代理和超时
        self._setup_session(self.session)
        self._setup_session(self.futures_session)

        # 超时设置
        self.timeout = 30

    def _setup_session(self, session):
        """设置 session 参数"""
        proxies = self._get_proxies()
        if proxies:
            session.proxies = proxies

        # 重试配置
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

    def _get_proxies(self):
        """获取代理配置"""
        # 1. 从环境变量获取
        env_proxies = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
        if env_proxies:
            return {
                "http": env_proxies,
                "https": env_proxies
            }

        # 2. 从配置文件获取（新增）
        proxy_config = getattr(self, 'proxy_url', None)
        if proxy_config:
            return {
                "http": proxy_config,
                "https": proxy_config
            }

        return None

    def _generate_signature(self, params: Dict) -> str:
        """生成签名"""
        # 创建参数字符串，按照字母顺序排列
        sorted_params = sorted(params.items())
        query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False, use_futures: bool = False) -> Dict:
        """发送 API 请求"""
        if params is None:
            params = {}

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)

        url = f"{self.base_url}{endpoint}"
        session = self.futures_session if use_futures else self.session

        try:
            if method == "GET":
                response = session.get(url, params=params, timeout=self.timeout)
            elif method == "POST":
                response = session.post(url, params=params, timeout=self.timeout)
            elif method == "DELETE":
                response = session.delete(url, params=params, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json() if e.response.content else {}
            raise Exception(f"API Error: {e} - {error_detail}")
        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout: {self.timeout} seconds")
        except requests.exceptions.ProxyError:
            raise Exception("Proxy error - check proxy configuration")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Connection error: {e}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")

    # ========== 公共接口 ==========

    def get_server_time(self) -> int:
        """获取服务器时间"""
        return self._request("GET", "/api/v3/time")["serverTime"]

    def ping(self) -> bool:
        """测试连接"""
        try:
            self._request("GET", "/api/v3/ping")
            return True
        except:
            return False

    def get_exchange_info(self, symbol: str = None) -> Dict:
        """获取交易规则和交易对信息"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/api/v3/exchangeInfo", params)

    def get_symbol_ticker(self, symbol: str) -> Dict:
        """获取最新价格"""
        return self._request("GET", "/api/v3/ticker/price", {"symbol": symbol})

    def get_24h_ticker(self, symbol: str = None) -> Dict:
        """24小时价格变化情况"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/api/v3/ticker/24hr", params)

    def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """获取订单簿深度"""
        return self._request("GET", "/api/v3/depth", {"symbol": symbol, "limit": limit})

    def get_klines(self, symbol: str, interval: str = "1h", limit: int = 100) -> List:
        """获取K线数据"""
        return self._request("GET", "/api/v3/klines", {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        })

    # ========== 需要签名的接口 ==========

    def get_account(self) -> Dict:
        """获取账户信息"""
        return self._request("GET", "/api/v3/account", signed=True)

    def get_balances(self) -> List[Dict]:
        """获取所有资产余额"""
        account = self.get_account()
        balances = []
        for b in account["balances"]:
            # 安全转换，处理字符串和数字格式
            try:
                free = float(b["free"]) if b["free"] else 0
                locked = float(b["locked"]) if b["locked"] else 0
                total = free + locked
            except (ValueError, TypeError):
                # 如果转换失败，跳过该资产
                continue

            if total > 0:
                balances.append({
                    "asset": b["asset"],
                    "free": free,
                    "locked": locked,
                    "total": total
                })
        return balances

    def get_trade_fee(self, symbol: str = None) -> Dict:
        """获取交易手续费"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/sapi/v1/asset/tradeFee", params, signed=True)

    def get_asset_detail(self) -> Dict:
        """获取资产详情（最小交易量等）"""
        return self._request("GET", "/sapi/v1/asset/assetDetail", signed=True)

    def dust_transfer(self, assets: List[str]) -> Dict:
        """小额资产兑换 BNB (Dust Sweep)"""
        return self._request("POST", "/sapi/v1/asset/dust", {
            "asset": ",".join(assets)
        }, signed=True)

    def dust_btc(self, assets: List[str]) -> Dict:
        """小额资产兑换 BTC"""
        return self._request("POST", "/sapi/v1/asset/dust-btc", {
            "assets": ",".join(assets)
        }, signed=True)

    # ========== 资金费率相关 (合约) ==========

    def get_funding_rate(self, symbol: str = None) -> List[Dict]:
        """获取资金费率"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        # 使用专门的 futures session
        url = f"{self.api_urls['main_futures']}/fapi/v1/fundingRate"
        response = self.futures_session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_premium_index(self, symbol: str = None) -> Dict:
        """获取标记价格和资金费率"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        url = f"{self.api_urls['main_futures']}/fapi/v1/premiumIndex"
        response = self.futures_session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    # ========== 现货交易 ==========

    def new_order(self, symbol: str, side: str, order_type: str, quantity: float,
                  price: float = None, time_in_force: str = "GTC") -> Dict:
        """下单"""
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "newOrderRespType": "FULL"
        }
        if price:
            params["price"] = price
            params["timeInForce"] = time_in_force

        return self._request("POST", "/api/v3/order", params, signed=True)

    def cancel_order(self, symbol: str, order_id: int = None, client_order_id: str = None) -> Dict:
        """取消订单"""
        params = {"symbol": symbol}
        if order_id:
            params["orderId"] = order_id
        if client_order_id:
            params["origClientOrderId"] = client_order_id
        return self._request("DELETE", "/api/v3/order", params, signed=True)

    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """获取当前挂单"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        return self._request("GET", "/api/v3/openOrders", params, signed=True)

    def get_my_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """获取历史成交"""
        return self._request("GET", "/api/v3/myTrades", {
            "symbol": symbol,
            "limit": limit
        }, signed=True)
