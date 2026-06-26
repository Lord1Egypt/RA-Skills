"""
多源数据客户端 — 直接调用公开 API

数据源:
  - Binance Futures: K线、资金费率、持仓量、合约信息、标记价格
  - Binance Spot: 现货 K线
  - CoinGecko: PAXG/XAUT 等加密代币价格
  - yfinance: 美股(AAPL/NVDA/SPY...)、大宗商品(WTI/NG/铜)、贵金属现货(XAU/XAG)
  - DeFi Llama: 协议 TVL、手续费收入（免费端点）

全部免费公开端点，无需 API Key。
国内访问 Binance 可配置代理: PROXY_URL 环境变量。
"""

import time
from datetime import datetime, timezone
from typing import Optional

import httpx
import pandas as pd
from loguru import logger

BINANCE_FUTURES_BASE = "https://fapi.binance.com"
BINANCE_SPOT_BASE = "https://api.binance.com"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
DEFILLAMA_BASE = "https://api.llama.fi"

INTERVAL_MAP = {
    "1m": "1m", "5m": "5m", "15m": "15m",
    "1h": "1h", "4h": "4h", "1d": "1d",
}

COINGECKO_IDS = {
    "PAXG": "pax-gold",
    "XAUT": "tether-gold",
    "OUSG": "ondo-us-government-bond-fund",
    "OMMF": "ondo-us-dollar-yield",
}

# yfinance ticker 映射
YFINANCE_TICKERS = {
    "RWA:AAPL": "AAPL", "RWA:NVDA": "NVDA", "RWA:TSLA": "TSLA",
    "RWA:MSFT": "MSFT", "RWA:GOOGL": "GOOGL", "RWA:AMZN": "AMZN",
    "RWA:META": "META", "RWA:SPY": "SPY", "RWA:QQQ": "QQQ",
    "COMM:WTI": "CL=F", "COMM:BRENT": "BZ=F",
    "COMM:NG": "NG=F", "COMM:COPPER": "HG=F",
    "METAL:XAU-SPOT": "GC=F", "METAL:XAG-SPOT": "SI=F",
}


def _ts_ms(dt_str: str) -> int:
    """日期字符串 (YYYY-MM-DD) 转毫秒时间戳。"""
    dt = datetime.strptime(dt_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def _symbol_to_binance(symbol: str) -> str:
    """BTC-USDT-PERP → BTCUSDT, BTC-USDT-SPOT → BTCUSDT"""
    parts = symbol.upper().replace("-PERP", "").replace("-SPOT", "").split("-")
    return "".join(parts)


class DataClient:
    """多源数据客户端，支持 Binance / CoinGecko / yfinance / DeFi Llama。"""

    def __init__(self, proxy: Optional[str] = None):
        import os
        proxy_url = proxy or os.environ.get("PROXY_URL")
        self._client = httpx.Client(
            timeout=30.0,
            proxy=proxy_url,
        )

    def _get(self, url: str, params: dict = None) -> dict | list:
        """带 429 限流重试的 GET 请求。"""
        resp = self._client.get(url, params=params)
        if resp.status_code == 429:
            retry = int(resp.headers.get("Retry-After", "5"))
            logger.warning(f"429 限流，等待 {retry}s")
            time.sleep(retry)
            resp = self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # ════════════════════════════════════════
    #  Binance Futures — 永续合约
    # ════════════════════════════════════════

    def get_perp_klines(
        self,
        symbol: str,
        interval: str = "1d",
        start_date: str = None,
        end_date: str = None,
        limit: int = 1500,
    ) -> pd.DataFrame:
        """
        永续合约 K 线。

        Binance 端点: GET /fapi/v1/klines
        无需 API Key，限流 2400 次/分钟。
        单次最多 1500 条，自动分页拉取完整历史。

        参数:
            symbol: 合约代码，如 "BTC-USDT-PERP"
            interval: K 线周期 (1m/5m/15m/1h/4h/1d)
            start_date: 起始日期 "YYYY-MM-DD"
            end_date: 结束日期 "YYYY-MM-DD"
            limit: 单次请求条数（最大 1500）

        返回:
            DataFrame [datetime, open, high, low, close, volume,
                       volume_usd, trades, taker_buy_volume_usd, taker_sell_volume_usd]
        """
        bn_symbol = _symbol_to_binance(symbol)
        all_rows = []
        params = {
            "symbol": bn_symbol,
            "interval": INTERVAL_MAP.get(interval, interval),
            "limit": limit,
        }
        if start_date:
            params["startTime"] = _ts_ms(start_date)
        if end_date:
            params["endTime"] = _ts_ms(end_date)

        while True:
            data = self._get(f"{BINANCE_FUTURES_BASE}/fapi/v1/klines", params)
            if not data:
                break
            all_rows.extend(data)
            if len(data) < limit:
                break
            params["startTime"] = data[-1][0] + 1
            if end_date and params["startTime"] > _ts_ms(end_date):
                break
            time.sleep(0.1)

        if not all_rows:
            return pd.DataFrame()

        df = pd.DataFrame(all_rows, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_volume",
            "taker_buy_quote_volume", "ignore",
        ])
        df["datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        for col in ["open", "high", "low", "close", "volume", "quote_volume",
                     "taker_buy_volume", "taker_buy_quote_volume"]:
            df[col] = df[col].astype(float)
        df = df.rename(columns={
            "quote_volume": "volume_usd",
            "taker_buy_quote_volume": "taker_buy_volume_usd",
        })
        df["taker_sell_volume_usd"] = df["volume_usd"] - df["taker_buy_volume_usd"]
        return df[["datetime", "open", "high", "low", "close", "volume",
                    "volume_usd", "trades", "taker_buy_volume_usd",
                    "taker_sell_volume_usd"]].reset_index(drop=True)

    def get_funding_rate(
        self,
        symbol: str,
        start_date: str = None,
        end_date: str = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """
        资金费率历史。

        Binance 端点: GET /fapi/v1/fundingRate
        每 8 小时一条，自动分页拉取。

        返回:
            DataFrame [datetime, funding_rate, mark_price]
        """
        bn_symbol = _symbol_to_binance(symbol)
        all_rows = []
        params = {"symbol": bn_symbol, "limit": limit}
        if start_date:
            params["startTime"] = _ts_ms(start_date)
        if end_date:
            params["endTime"] = _ts_ms(end_date)

        while True:
            data = self._get(f"{BINANCE_FUTURES_BASE}/fapi/v1/fundingRate", params)
            if not data:
                break
            all_rows.extend(data)
            if len(data) < limit:
                break
            params["startTime"] = data[-1]["fundingTime"] + 1
            time.sleep(0.1)

        if not all_rows:
            return pd.DataFrame()

        df = pd.DataFrame(all_rows)
        df["datetime"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
        df["funding_rate"] = df["fundingRate"].astype(float)
        df["mark_price"] = df["markPrice"].astype(float)
        return df[["datetime", "funding_rate", "mark_price"]].reset_index(drop=True)

    def get_open_interest(self, symbol: str) -> dict:
        """
        当前持仓量快照。

        Binance 端点: GET /fapi/v1/openInterest
        仅返回当前快照，不含历史。
        """
        bn_symbol = _symbol_to_binance(symbol)
        data = self._get(
            f"{BINANCE_FUTURES_BASE}/fapi/v1/openInterest",
            {"symbol": bn_symbol},
        )
        return {
            "symbol": symbol,
            "open_interest": float(data["openInterest"]),
            "timestamp": data["time"],
        }

    def get_open_interest_hist(
        self,
        symbol: str,
        period: str = "1d",
        limit: int = 30,
    ) -> pd.DataFrame:
        """
        持仓量历史统计。

        Binance 端点: GET /futures/data/openInterestHist
        ⚠️ 限制: 仅最近 30 天数据。
        """
        bn_symbol = _symbol_to_binance(symbol)
        data = self._get(f"{BINANCE_FUTURES_BASE}/futures/data/openInterestHist", {
            "pair": bn_symbol,
            "contractType": "PERPETUAL",
            "period": period,
            "limit": limit,
        })
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df["open_interest"] = df["sumOpenInterest"].astype(float)
        df["open_interest_usd"] = df["sumOpenInterestValue"].astype(float)
        return df[["datetime", "open_interest", "open_interest_usd"]].reset_index(drop=True)

    def get_long_short_ratio(
        self,
        symbol: str,
        period: str = "1d",
        limit: int = 30,
    ) -> pd.DataFrame:
        """
        Top Trader 多空持仓比。

        Binance 端点: GET /futures/data/topLongShortPositionRatio
        ⚠️ 限制: 仅最近 30 天。
        """
        bn_symbol = _symbol_to_binance(symbol)
        data = self._get(
            f"{BINANCE_FUTURES_BASE}/futures/data/topLongShortPositionRatio",
            {"symbol": bn_symbol, "period": period, "limit": limit},
        )
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df["long_short_ratio"] = df["longShortRatio"].astype(float)
        df["long_account"] = df["longAccount"].astype(float)
        df["short_account"] = df["shortAccount"].astype(float)
        return df[["datetime", "long_short_ratio", "long_account",
                    "short_account"]].reset_index(drop=True)

    def get_mark_price(self, symbol: str) -> dict:
        """
        当前标记价格和资金费率。

        Binance 端点: GET /fapi/v1/premiumIndex
        """
        bn_symbol = _symbol_to_binance(symbol)
        data = self._get(
            f"{BINANCE_FUTURES_BASE}/fapi/v1/premiumIndex",
            {"symbol": bn_symbol},
        )
        return {
            "symbol": symbol,
            "mark_price": float(data["markPrice"]),
            "index_price": float(data["indexPrice"]),
            "funding_rate": float(data["lastFundingRate"]),
            "next_funding_time": data["nextFundingTime"],
        }

    def get_exchange_info(self, symbol: str = None) -> dict | list:
        """
        合约信息（面值、杠杆上限、最小下单量等）。

        Binance 端点: GET /fapi/v1/exchangeInfo
        """
        data = self._get(f"{BINANCE_FUTURES_BASE}/fapi/v1/exchangeInfo")
        symbols = data.get("symbols", [])

        if symbol:
            bn_symbol = _symbol_to_binance(symbol)
            for s in symbols:
                if s["symbol"] == bn_symbol:
                    return self._parse_contract_info(s, symbol)
            raise ValueError(f"合约 {symbol} 未找到")

        return [
            self._parse_contract_info(s, f"{s.get('baseAsset', '')}-{s.get('quoteAsset', '')}-PERP")
            for s in symbols
            if s.get("contractType") == "PERPETUAL"
        ]

    @staticmethod
    def _parse_contract_info(raw: dict, symbol: str) -> dict:
        filters = {f["filterType"]: f for f in raw.get("filters", [])}
        price_filter = filters.get("PRICE_FILTER", {})
        lot_filter = filters.get("LOT_SIZE", {})
        return {
            "symbol": symbol,
            "base_asset": raw.get("baseAsset", ""),
            "quote_asset": raw.get("quoteAsset", ""),
            "contract_type": raw.get("contractType", ""),
            "tick_size": float(price_filter.get("tickSize", 0)),
            "min_qty": float(lot_filter.get("minQty", 0)),
            "max_qty": float(lot_filter.get("maxQty", 0)),
            "step_size": float(lot_filter.get("stepSize", 0)),
            "maintenance_margin_rate": float(raw.get("maintMarginPercent", 2.5)) / 100,
            "required_margin_rate": float(raw.get("requiredMarginPercent", 5)) / 100,
        }

    def list_perp_symbols(self) -> list[str]:
        """列出 Binance 所有永续合约代码。"""
        data = self._get(f"{BINANCE_FUTURES_BASE}/fapi/v1/exchangeInfo")
        return [
            f"{s['baseAsset']}-{s['quoteAsset']}-PERP"
            for s in data.get("symbols", [])
            if s.get("contractType") == "PERPETUAL" and s.get("status") == "TRADING"
        ]

    # ════════════════════════════════════════
    #  Binance Spot — 现货
    # ════════════════════════════════════════

    def get_spot_klines(
        self,
        symbol: str,
        interval: str = "1d",
        start_date: str = None,
        end_date: str = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """
        现货 K 线。

        Binance 端点: GET /api/v3/klines
        自动分页，无限历史。

        返回:
            DataFrame [datetime, open, high, low, close, volume, volume_usd]
        """
        bn_symbol = _symbol_to_binance(symbol)
        all_rows = []
        params = {"symbol": bn_symbol, "interval": interval, "limit": limit}
        if start_date:
            params["startTime"] = _ts_ms(start_date)
        if end_date:
            params["endTime"] = _ts_ms(end_date)

        while True:
            data = self._get(f"{BINANCE_SPOT_BASE}/api/v3/klines", params)
            if not data:
                break
            all_rows.extend(data)
            if len(data) < limit:
                break
            params["startTime"] = data[-1][0] + 1
            time.sleep(0.1)

        if not all_rows:
            return pd.DataFrame()

        df = pd.DataFrame(all_rows, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_volume",
            "taker_buy_quote_volume", "ignore",
        ])
        df["datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        for col in ["open", "high", "low", "close", "volume", "quote_volume"]:
            df[col] = df[col].astype(float)
        df = df.rename(columns={"quote_volume": "volume_usd"})
        return df[["datetime", "open", "high", "low", "close", "volume",
                    "volume_usd"]].reset_index(drop=True)

    # ════════════════════════════════════════
    #  CoinGecko — 代币价格
    # ════════════════════════════════════════

    def get_token_history(
        self,
        token: str,
        days: int = 365,
    ) -> pd.DataFrame:
        """
        代币价格历史（日线）。

        CoinGecko 端点: GET /api/v3/coins/{id}/market_chart
        免费版限流 10-30 次/分钟，日线最多 365 天。

        参数:
            token: 代币名称 (PAXG/XAUT/OUSG 等)
            days: 历史天数

        返回:
            DataFrame [datetime, close, volume_usd, market_cap]
        """
        cg_id = COINGECKO_IDS.get(token.upper(), token.lower())
        data = self._get(f"{COINGECKO_BASE}/coins/{cg_id}/market_chart", {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily",
        })
        prices = data.get("prices", [])
        volumes = data.get("total_volumes", [])
        caps = data.get("market_caps", [])

        if not prices:
            return pd.DataFrame()

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        if volumes and len(volumes) == len(prices):
            df["volume_usd"] = [v[1] for v in volumes]
        if caps and len(caps) == len(prices):
            df["market_cap"] = [c[1] for c in caps]
        return df.drop(columns=["timestamp"]).reset_index(drop=True)

    # ════════════════════════════════════════
    #  yfinance — 美股 / 大宗商品 / 贵金属
    # ════════════════════════════════════════

    @staticmethod
    def get_stock_klines(
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        美股/ETF K 线。

        数据源: yfinance（Yahoo Finance 公开数据）
        支持 Symbol: RWA:AAPL / RWA:SPY / RWA:QQQ 等
        历史深度: 日线 30+ 年

        返回:
            DataFrame [datetime, open, high, low, close, volume, volume_usd, dividends?]
        """
        import yfinance as yf

        ticker = YFINANCE_TICKERS.get(symbol.upper(), symbol.replace("RWA:", ""))
        yf_interval = {"1d": "1d", "1h": "1h", "5m": "5m", "1m": "1m"}.get(interval, "1d")

        tk = yf.Ticker(ticker)
        df = tk.history(start=start_date, end=end_date, interval=yf_interval)

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        date_col = "Date" if "Date" in df.columns else "Datetime"
        df = df.rename(columns={
            date_col: "datetime",
            "Open": "open", "High": "high", "Low": "low",
            "Close": "close", "Volume": "volume",
        })
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df["volume_usd"] = df["close"] * df["volume"]

        cols = ["datetime", "open", "high", "low", "close", "volume", "volume_usd"]
        if "Dividends" in df.columns:
            df["dividends"] = df["Dividends"]
            cols.append("dividends")

        return df[cols].reset_index(drop=True)

    @staticmethod
    def get_commodity_klines(
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        大宗商品期货 K 线。

        数据源: yfinance
        支持: COMM:WTI / COMM:BRENT / COMM:NG / COMM:COPPER
        历史深度: 10+ 年

        返回:
            DataFrame [datetime, open, high, low, close, volume, volume_usd]
        """
        import yfinance as yf

        ticker = YFINANCE_TICKERS.get(symbol.upper())
        if not ticker:
            raise ValueError(
                f"未知大宗商品 Symbol: {symbol}，"
                f"支持: {[k for k in YFINANCE_TICKERS if k.startswith('COMM:')]}"
            )

        tk = yf.Ticker(ticker)
        df = tk.history(start=start_date, end=end_date, interval=interval)

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        date_col = "Date" if "Date" in df.columns else "Datetime"
        df = df.rename(columns={
            date_col: "datetime",
            "Open": "open", "High": "high", "Low": "low",
            "Close": "close", "Volume": "volume",
        })
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df["volume_usd"] = df["close"] * df["volume"]
        return df[["datetime", "open", "high", "low", "close",
                    "volume", "volume_usd"]].reset_index(drop=True)

    @staticmethod
    def get_metal_spot_klines(
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """
        贵金属现货 K 线（通过期货合约代理）。

        数据源: yfinance (GC=F 黄金期货 / SI=F 白银期货)
        支持: METAL:XAU-SPOT / METAL:XAG-SPOT
        历史深度: 10+ 年

        返回:
            DataFrame [datetime, open, high, low, close, volume]
        """
        import yfinance as yf

        ticker = YFINANCE_TICKERS.get(symbol.upper())
        if not ticker:
            raise ValueError(
                f"未知贵金属 Symbol: {symbol}，支持: METAL:XAU-SPOT / METAL:XAG-SPOT"
            )

        tk = yf.Ticker(ticker)
        df = tk.history(start=start_date, end=end_date, interval="1d")

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        date_col = "Date" if "Date" in df.columns else "Datetime"
        df = df.rename(columns={
            date_col: "datetime",
            "Open": "open", "High": "high", "Low": "low",
            "Close": "close", "Volume": "volume",
        })
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        return df[["datetime", "open", "high", "low", "close",
                    "volume"]].reset_index(drop=True)

    # ════════════════════════════════════════
    #  DeFi Llama — 协议 TVL / 手续费
    # ════════════════════════════════════════

    def get_protocol_tvl(self, protocol: str) -> pd.DataFrame:
        """
        协议 TVL 历史。

        DeFi Llama 端点: GET /protocol/{slug}
        免费，无需 Key。
        支持: aave, compound-v3, lido, curve-dex, uniswap 等

        返回:
            DataFrame [datetime, tvl_usd]
        """
        data = self._get(f"{DEFILLAMA_BASE}/protocol/{protocol}")
        tvl_history = data.get("tvl", [])

        if not tvl_history:
            return pd.DataFrame()

        df = pd.DataFrame(tvl_history)
        df["datetime"] = pd.to_datetime(df["date"], unit="s", utc=True)
        df["tvl_usd"] = df["totalLiquidityUSD"].astype(float)
        return df[["datetime", "tvl_usd"]].reset_index(drop=True)

    def get_protocol_info(self, protocol: str) -> dict:
        """
        协议当前信息（TVL、类别、链等）。

        DeFi Llama 端点: GET /protocol/{slug}
        """
        data = self._get(f"{DEFILLAMA_BASE}/protocol/{protocol}")
        return {
            "name": data.get("name", ""),
            "category": data.get("category", ""),
            "chains": data.get("chains", []),
            "current_tvl": data.get("currentChainTvls", {}),
            "total_tvl": float(data.get("tvl", [{}])[-1].get("totalLiquidityUSD", 0))
            if data.get("tvl") else 0,
        }

    def get_defi_fees(self, protocol: str = None) -> pd.DataFrame:
        """
        协议手续费/收入数据。

        DeFi Llama 端点: GET /overview/fees
        免费，返回所有协议的 24h 手续费和收入。

        返回:
            DataFrame [name, category, fees_24h, fees_7d, fees_30d, revenue_24h]
        """
        data = self._get(f"{DEFILLAMA_BASE}/overview/fees")
        protocols = data.get("protocols", [])

        if protocol:
            protocols = [
                p for p in protocols
                if p.get("name", "").lower() == protocol.lower()
                or p.get("slug", "") == protocol.lower()
            ]

        if not protocols:
            return pd.DataFrame()

        rows = []
        for p in protocols:
            rows.append({
                "name": p.get("name", ""),
                "category": p.get("category", ""),
                "fees_24h": float(p.get("total24h", 0) or 0),
                "fees_7d": float(p.get("total7d", 0) or 0),
                "fees_30d": float(p.get("total30d", 0) or 0),
                "revenue_24h": float(p.get("revenue24h", 0) or 0),
            })
        return pd.DataFrame(rows)

    def list_defi_protocols(self) -> pd.DataFrame:
        """
        所有 DeFi 协议列表及 TVL。

        DeFi Llama 端点: GET /protocols

        返回:
            DataFrame [name, slug, category, chains, tvl] (前 200 个)
        """
        data = self._get(f"{DEFILLAMA_BASE}/protocols")
        rows = []
        for p in data[:200]:
            rows.append({
                "name": p.get("name", ""),
                "slug": p.get("slug", ""),
                "category": p.get("category", ""),
                "chains": ", ".join(p.get("chains", [])),
                "tvl": float(p.get("tvl", 0) or 0),
            })
        return pd.DataFrame(rows)

    # ════════════════════════════════════════
    #  生命周期
    # ════════════════════════════════════════

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
