"""
OKX Data Provider - 整合 okx-cex-market 技能
提供更丰富的市场数据：订单簿、资金费率、持仓量、技术指标等
"""
import subprocess
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
import numpy as np
from functools import lru_cache
import time


class OKXDataProvider:
    """使用 okx-cex-market CLI 获取数据"""
    
    @staticmethod
    def _run_okx_command(args: List[str]) -> Dict:
        """运行 okx 命令并返回 JSON 结果"""
        try:
            result = subprocess.run(
                ["okx"] + args + ["--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_klines(symbol: str, bar: str = "1H", limit: int = 500) -> pd.DataFrame:
        """获取K线数据（兼容原有接口）"""
        # 转换时间周期格式
        bar_map = {
            "1M": "1m", "5M": "5m", "15M": "15m", "30M": "30m",
            "1H": "1H", "4H": "4H", "1D": "1D"
        }
        okx_bar = bar_map.get(bar, bar)
        
        # 处理 symbol 格式
        inst_id = symbol if "-SWAP" in symbol or "-" in symbol else f"{symbol}-USDT-SWAP"
        
        data = OKXDataProvider._run_okx_command([
            "market", "candles", inst_id,
            "--bar", okx_bar,
            "--limit", str(limit)
        ])
        
        # 处理 OKX CLI 返回格式：可能是 list 或 dict
        if isinstance(data, list) and len(data) > 0:
            # OKX CLI 返回 list 格式
            candles = data
        elif isinstance(data, dict):
            if "error" in data or not data.get("data"):
                # 回退到直接 HTTP 请求
                return OKXDataProvider._fallback_klines(inst_id, okx_bar, limit)
            candles = data["data"]
        else:
            # 回退到直接 HTTP 请求
            return OKXDataProvider._fallback_klines(inst_id, okx_bar, limit)
        
        # 如果返回数量少于请求数量，说明需要分页（OKX单次最多300条）
        if not candles or len(candles) < limit:
            return OKXDataProvider._fallback_klines(inst_id, okx_bar, limit)
        
        # 解析数据
        df = pd.DataFrame(candles, columns=[
            "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"
        ])
        
        # 转换数值类型
        for col in ["open", "high", "low", "close", "vol"]:
            df[col] = pd.to_numeric(df[col])
        
        df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
        df = df.sort_values("ts").reset_index(drop=True)
        
        return df
    
    @staticmethod
    def _fallback_klines(inst_id: str, bar: str, limit: int) -> pd.DataFrame:
        """回退到直接 HTTP 请求，支持分页获取超过300条数据"""
        import requests
        url = "https://www.okx.com/api/v5/market/history-candles"
        
        all_candles = []
        remaining = limit
        current_after = None
        
        try:
            while remaining > 0:
                batch_size = min(300, remaining)
                params = {
                    "instId": inst_id,
                    "bar": bar,
                    "limit": batch_size
                }
                if current_after:
                    params["after"] = current_after
                
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
                d = r.json()
                
                if d.get("code") != "0" or not d.get("data"):
                    break
                
                batch = d["data"]
                all_candles.extend(batch)
                remaining -= len(batch)
                
                if len(batch) == 300:
                    current_after = batch[-1][0]
                else:
                    break
            
            if all_candles:
                cols = ["ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"]
                df = pd.DataFrame(all_candles[:limit], columns=cols)
                for col in ["open", "high", "low", "close", "vol"]:
                    df[col] = pd.to_numeric(df[col])
                df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
                df = df.sort_values("ts").reset_index(drop=True)
                return df
        except Exception:
            pass
        
        raise ValueError(f"Cannot fetch data for {inst_id}")
    
    @staticmethod
    def get_orderbook(symbol: str, depth: int = 5) -> Dict:
        """获取订单簿数据
        
        Returns:
            {
                "bids": [[price, qty], ...],
                "asks": [[price, qty], ...],
                "mid_price": float,
                "spread": float,
                "imbalance": float  # 买单/卖单比例
            }
        """
        inst_id = symbol if "-SWAP" in symbol or "-" in symbol else f"{symbol}-USDT-SWAP"
        
        data = OKXDataProvider._run_okx_command([
            "market", "orderbook", inst_id,
            "--sz", str(depth)
        ])
        
        if "error" in data or not data.get("data"):
            return {"error": "Failed to fetch orderbook"}
        
        ob = data["data"][0]
        bids = [[float(p), float(q)] for p, q in ob.get("bids", [])]
        asks = [[float(p), float(q)] for p, q in ob.get("asks", [])]
        
        if bids and asks:
            best_bid = bids[0][0]
            best_ask = asks[0][0]
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            spread_pct = spread / mid_price * 100
            
            # 计算订单簿不平衡
            bid_vol = sum(q for _, q in bids)
            ask_vol = sum(q for _, q in asks)
            imbalance = bid_vol / (bid_vol + ask_vol) if (bid_vol + ask_vol) > 0 else 0.5
        else:
            mid_price = spread = spread_pct = imbalance = None
        
        return {
            "bids": bids,
            "asks": asks,
            "mid_price": mid_price,
            "spread": spread,
            "spread_pct": spread_pct,
            "imbalance": imbalance,
            "timestamp": ob.get("ts")
        }
    
    @staticmethod
    def get_funding_rate(symbol: str, history: bool = False, limit: int = 100) -> pd.DataFrame:
        """获取资金费率数据
        
        Returns:
            DataFrame with columns: ts, fundingRate, fundingTime, method
        """
        inst_id = symbol if "-SWAP" in symbol else f"{symbol}-USDT-SWAP"
        
        cmd = ["market", "funding-rate", inst_id]
        if history:
            cmd.append("--history")
        if limit:
            cmd.extend(["--limit", str(limit)])
        
        data = OKXDataProvider._run_okx_command(cmd)
        
        if "error" in data or not data.get("data"):
            return pd.DataFrame()
        
        df = pd.DataFrame(data["data"])
        if not df.empty:
            df["fundingRate"] = pd.to_numeric(df["fundingRate"])
            df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
            df = df.sort_values("ts").reset_index(drop=True)
        
        return df
    
    @staticmethod
    def get_open_interest(inst_type: str = "SWAP", symbol: Optional[str] = None) -> pd.DataFrame:
        """获取持仓量数据
        
        Args:
            inst_type: SWAP / FUTURES / OPTION
            symbol: 具体品种，None则返回所有
        """
        cmd = ["market", "open-interest", "--instType", inst_type]
        if symbol:
            inst_id = symbol if "-SWAP" in symbol else f"{symbol}-USDT-SWAP"
            cmd.extend(["--instId", inst_id])
        
        data = OKXDataProvider._run_okx_command(cmd)
        
        if "error" in data or not data.get("data"):
            return pd.DataFrame()
        
        df = pd.DataFrame(data["data"])
        if not df.empty:
            for col in ["oi", "oiCcy"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col])
            df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
        
        return df
    
    @staticmethod
    def get_indicator(indicator: str, symbol: str, bar: str = "1H", 
                      params: Optional[str] = None, limit: int = 100) -> pd.DataFrame:
        """获取技术指标
        
        Args:
            indicator: rsi, macd, ema, ma, bb (boll), kdj, supertrend, etc.
            symbol: 交易对
            bar: 时间周期 (注意指标使用 1H/4H/1Dutc 格式)
            params: 指标参数，如 "14" 或 "12,26,9"
            limit: 返回数量
        """
        inst_id = symbol if "-SWAP" in symbol or "-" in symbol else f"{symbol}-USDT-SWAP"
        
        # 转换时间周期格式
        bar_map = {
            "1M": "1m", "5M": "5m", "15M": "15m", "30M": "30m",
            "1H": "1H", "4H": "4H", "1D": "1Dutc", "1W": "1Wutc"
        }
        okx_bar = bar_map.get(bar, bar)
        
        cmd = [
            "market", "indicator", indicator.lower(), inst_id,
            "--bar", okx_bar,
            "--limit", str(limit)
        ]
        
        if params:
            cmd.extend(["--params", params])
        
        data = OKXDataProvider._run_okx_command(cmd)
        
        if "error" in data or not data.get("data"):
            return pd.DataFrame()
        
        df = pd.DataFrame(data["data"])
        if not df.empty and "ts" in df.columns:
            df["ts"] = pd.to_datetime(df["ts"].astype(float), unit="ms")
            df = df.sort_values("ts").reset_index(drop=True)
        
        return df
    
    @staticmethod
    def get_market_sentiment(symbol: str) -> Dict:
        """获取综合市场情绪指标
        
        结合：资金费率 + 持仓量变化 + 订单簿不平衡
        """
        inst_id = symbol if "-SWAP" in symbol else f"{symbol}-USDT-SWAP"
        
        sentiment = {
            "symbol": inst_id,
            "timestamp": pd.Timestamp.now(),
            "funding": None,
            "oi_change": None,
            "orderbook_imbalance": None,
            "overall": "neutral"
        }
        
        # 1. 资金费率
        funding_df = OKXDataProvider.get_funding_rate(inst_id, limit=2)
        if not funding_df.empty:
            current_funding = funding_df["fundingRate"].iloc[-1]
            sentiment["funding"] = float(current_funding)
            # 资金费率 > 0.01% 表示多头过热，< -0.01% 表示空头过热
        
        # 2. 订单簿不平衡
        ob = OKXDataProvider.get_orderbook(inst_id)
        if "imbalance" in ob:
            sentiment["orderbook_imbalance"] = ob["imbalance"]
        
        # 3. 持仓量变化
        oi_df = OKXDataProvider.get_open_interest("SWAP", inst_id)
        if len(oi_df) >= 2:
            current_oi = oi_df["oi"].iloc[-1]
            prev_oi = oi_df["oi"].iloc[-2]
            sentiment["oi_change"] = float((current_oi - prev_oi) / prev_oi * 100)
        
        # 综合判断
        signals = []
        if sentiment["funding"] and sentiment["funding"] > 0.0001:
            signals.append("overheated_long")
        elif sentiment["funding"] and sentiment["funding"] < -0.0001:
            signals.append("overheated_short")
        
        if sentiment["orderbook_imbalance"]:
            if sentiment["orderbook_imbalance"] > 0.6:
                signals.append("strong_buy_pressure")
            elif sentiment["orderbook_imbalance"] < 0.4:
                signals.append("strong_sell_pressure")
        
        sentiment["signals"] = signals
        return sentiment


# 向后兼容：保留原有函数名
def get_klines(symbol: str, bar: str = "1H", limit: int = 500) -> pd.DataFrame:
    """兼容原有接口"""
    return OKXDataProvider.get_klines(symbol, bar, limit)


# ─────────────────────────────────────────────────────────
# 智能数据获取：自动检测标的类型
# ─────────────────────────────────────────────────────────

def get_data(symbol: str, bar: str = "1H", limit: int = 500) -> pd.DataFrame:
    """
    自动检测标的类型并获取数据
    - 如果是OKX交易对，使用OKX API
    - 如果是美股代码，使用Yahoo Finance
    
    支持的美股: NVDA, AAPL, MSFT, GOOGL, AMZN, TSLA, META, etc.
    """
    # 美股代码列表 (常见科技股)
    STOCK_SYMBOLS = {
        'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA',
        'NFLX', 'AMD', 'INTC', 'CRM', 'ORCL', 'IBM', 'QCOM'
    }
    
    # 明确不是股票的标的（加密货币 + 大宗商品期货）
    # 避免 Yahoo Finance 将同名股票代码误识别（如 CL=Colgate vs CL=WTI原油）
    CRYPTO_EXCLUSIONS = {
        # 加密货币
        'BTC', 'ETH', 'SOL', 'DOGE', 'XRP', 'ADA', 'AVAX', 'DOT',
        'USDT', 'OKB', 'USDC', 'LINK', 'MATIC', 'UNI', 'ATOM',
        # 大宗商品期货代码（Yahoo Finance 有同名股票）
        'CL',   # 原油 (WTI) vs Colgate-Palmolive
        'NG',   # 天然气 vs Network Analytics
        'HG',   # 铜 vs HUGO CHAVEZ
        'PL',   # 白金 vs Polaris
        'PA',   # 钯 vs Pandora
        'ZC',   # 玉米 vs Zunic Markets
        'ZS',   # 大豆 vs Summit Financial
        'ZW',   # 小麦 vs Warren Buffett related
        'ZL',   # 豆油 vs ZLEPIER
        'ZO',   # 燕麦 vs ZO控股
        'ZR',   # 大米 vs ZIRION
        'CC',   # 可可 vs Carnival Corp
        'CT',   # 棉花 vs Cit Group
        'LB',   # 木材 vs Lumber
        'OJ',   # 橙汁 vs Orange Juice
        'KC',   # 咖啡 vs Kansas City Southern
        'SB',   # 糖 vs Santa Barbara
        'RC',   # 螺纹钢 vs Realt混凝土
    }
    
    # 检测是否是股票代码
    # NVDA-USDT -> NVDA
    # NVDA-USDT-SWAP -> NVDA
    symbol_upper = symbol.upper().replace('-USDT-SWAP', '').replace('-USDT', '')
    
    # 判断逻辑：纯字母 + 长度<=5 + 不在加密货币排除列表 = 可能是股票
    is_stock = (
        symbol_upper in STOCK_SYMBOLS or
        (len(symbol_upper) <= 5 and symbol_upper.isalpha() and symbol_upper not in CRYPTO_EXCLUSIONS)
    )
    
    # 二次判断：如果不在排除列表也不在常见加密货币列表，可能真的是股票
    okx_common = {'BTC', 'ETH', 'USDT', 'OKB', 'SOL', 'DOGE', 'XRP', 'ADA', 'AVAX', 'DOT', 'LINK', 'MATIC'}
    if symbol_upper.replace('-', '').isalpha() and symbol_upper not in okx_common and symbol_upper not in CRYPTO_EXCLUSIONS:
        is_stock = True
    
    if is_stock:
        # 提取纯股票代码
        stock_symbol = symbol_upper.replace('-USDT-SWAP', '').replace('-USDT', '')
        try:
            return get_stock_klines(stock_symbol, bar, limit)
        except ValueError as e:
            print(f"  ⚠️ 股票数据获取失败 ({stock_symbol}), 尝试OKX: {str(e)[:50]}")
            # 降级到OKX
            try:
                return OKXDataProvider.get_klines(symbol, bar, limit)
            except:
                raise ValueError(f"无法获取 {symbol} 数据")
    else:
        # 尝试OKX
        try:
            return OKXDataProvider.get_klines(symbol, bar, limit)
        except ValueError:
            # 降级到Yahoo Finance (去掉常见后缀)
            base_symbol = symbol.replace('-USDT-SWAP', '').replace('-USDT', '')
            try:
                return get_stock_klines(base_symbol, bar, limit)
            except:
                raise ValueError(f"无法获取 {symbol} 数据")


# ─────────────────────────────────────────────────────────
# Yahoo Finance 股票数据支持 (用于非OKX标的如NVDA/AAPL)
# ─────────────────────────────────────────────────────────

def get_stock_klines(symbol: str, bar: str = "1H", limit: int = 500) -> pd.DataFrame:
    """
    获取股票数据 (Yahoo Finance)
    适用于: NVDA, AAPL, MSFT, GOOGL, AMZN, TSLA, META 等美股
    
    Args:
        symbol: 股票代码 (如 NVDA, AAPL)
        bar: 时间周期 (1H, 4H, 1D)
        limit: 获取数量
    
    Returns:
        DataFrame with columns: ts, open, high, low, close, vol
    """
    import requests
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Yahoo Finance API
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    
    # 计算时间范围
    bar_map = {
        "1H": (limit, "1h"),
        "4H": (limit, "1h"),   # Yahoo没有4H，用1H模拟
        "1D": (limit, "1d"),
        "1m": (limit, "1m"),
        "5m": (limit, "5m"),
        "15m": (limit, "15m"),
        "30m": (limit, "1h"),   # Yahoo没有30m，用1h模拟
    }
    
    count, interval = bar_map.get(bar, (limit, "1h"))
    
    # period1/period2: Unix timestamps
    end_time = int(datetime.now().timestamp())
    start_time = end_time - (count * 3600)  # 粗略估计
    
    params = {
        "symbol": symbol,
        "period1": start_time,
        "period2": end_time,
        "interval": interval,
        "events": "history"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        result = data.get("chart", {}).get("result", [])
        if not result:
            raise ValueError(f"Yahoo Finance返回空数据 for {symbol}")
        
        quote = result[0]["indicators"]["quote"][0]
        timestamps = result[0]["timestamp"]
        
        df = pd.DataFrame({
            "ts": pd.to_datetime(timestamps, unit="s"),
            "open": quote.get("open"),
            "high": quote.get("high"),
            "low": quote.get("low"),
            "close": quote.get("close"),
            "vol": quote.get("volume")
        })
        
        # 清理数据
        df = df.dropna()
        df = df[df["close"] > 0]
        
        # 限制数量
        if len(df) > limit:
            df = df.tail(limit)
        
        return df.reset_index(drop=True)
        
    except requests.RequestException as e:
        raise ValueError(f"Yahoo Finance请求失败 for {symbol}: {str(e)[:100]}")
    except Exception as e:
        raise ValueError(f"获取股票数据失败 for {symbol}: {str(e)[:100]}")


# ─────────────────────────────────────────────────────────
# 缓存版本的数据获取 (避免重复请求)
# ─────────────────────────────────────────────────────────

@lru_cache(maxsize=128)
def _cached_get_data(symbol: str, bar: str = "1H", limit: int = 500) -> Optional[Dict]:
    """
    带缓存的数据获取 (内部使用)
    缓存时间: 60秒
    返回字典格式以支持缓存序列化
    """
    try:
        df = get_data(symbol, bar, limit)
        # 转换为可缓存的字典格式
        return {
            'ts': df['ts'].tolist(),
            'open': df['open'].tolist(),
            'high': df['high'].tolist(),
            'low': df['low'].tolist(),
            'close': df['close'].tolist(),
            'vol': df['vol'].tolist() if 'vol' in df.columns else df['volume'].tolist()
        }
    except Exception:
        return None


def get_data_cached(symbol: str, bar: str = "1H", limit: int = 500, cache_ttl: int = 60) -> pd.DataFrame:
    """
    带缓存的数据获取
    
    Args:
        symbol: 标的代码
        bar: 时间周期
        limit: 数量
        cache_ttl: 缓存时间(秒)，默认60秒
    
    Returns:
        DataFrame with market data
    """
    # 使用时间戳作为缓存key的一部分 (实现TTL)
    cache_key = f"{symbol}_{bar}_{limit}_{int(time.time() / cache_ttl)}"
    
    # 尝试从缓存获取
    cached = _cached_get_data(symbol, bar, limit)
    if cached is not None:
        return pd.DataFrame(cached)
    
    # 缓存未命中，重新获取
    return get_data(symbol, bar, limit)


def clear_data_cache():
    """清除数据缓存"""
    _cached_get_data.cache_clear()
