#!/usr/bin/env python3
"""
多数据源管理器 - 故障转移和性能优化
按市场分别路由到最适合的数据源：

A股/港股数据源（按优先级）：
- P0: 腾讯财经 API (免费、稳定、无需 token)
- P1: AkShare (东方财富聚合，A股历史稳定，实时接口可能限流)
- P2: YFinance (全球覆盖，A股数据相对简单)
- P3: Tushare (付费接口，配置 Token 后自动提升优先级)

美股数据源：
- P0: YFinance (全球覆盖，美股数据最全面，免费)

特性：
- 智能市场路由：自动检测股票所属市场并选择最优数据源
- 故障转移：单数据源失败自动切换到下一个
- 熔断器保护：连续失败后冷却 5 分钟
- 缓存：5 分钟内相同请求直接返回缓存
- 防封禁：随机延迟
"""

import logging
import time
import random
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Optional
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import akshare as ak
except ImportError:
    ak = None

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


def detect_market(stock_code: str) -> str:
    """检测股票代码所属市场: 'us', 'hk', 'a_sh', 'a_sz', 'unknown'"""
    s = stock_code.strip().upper()
    if s.endswith('.HK'):
        return 'hk'
    if s.endswith(('.SH', '.SS')):
        return 'a_sh'
    if s.endswith('.SZ'):
        return 'a_sz'
    code = s.split('.')[0]
    if code.isdigit():
        if len(code) == 5:
            return 'hk'
        if len(code) == 6:
            return 'a_sh' if code.startswith('6') else 'a_sz'
    if s.isalpha():
        return 'us'
    base = s.split('.')[0]
    if base.isalpha():
        return 'us'
    return 'unknown'


class CircuitBreaker:
    """熔断器：保护不稳定的接口"""

    def __init__(self, failure_threshold: int = 3, cooldown_seconds: int = 300):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failures: Dict[str, List[datetime]] = {}
        self.open_until: Dict[str, datetime] = {}

    def record_failure(self, name: str, error: Exception) -> bool:
        now = datetime.now()
        if name not in self.failures:
            self.failures[name] = []
        self.failures[name] = [
            t for t in self.failures[name]
            if (now - t).total_seconds() < self.cooldown_seconds
        ]
        self.failures[name].append(now)
        if len(self.failures[name]) >= self.failure_threshold:
            self.open_until[name] = now + timedelta(seconds=self.cooldown_seconds)
            logger.warning(
                f"熔断器打开: {name} (连续失败 {len(self.failures[name])} 次，"
                f"冷却 {self.cooldown_seconds} 秒)"
            )
            return True
        return False

    def record_success(self, name: str):
        if name in self.failures:
            self.failures[name] = []
        if name in self.open_until:
            del self.open_until[name]

    def is_open(self, name: str) -> bool:
        if name not in self.open_until:
            return False
        now = datetime.now()
        if now < self.open_until[name]:
            return True
        del self.open_until[name]
        return False


class DataFetcherManager:
    """数据源管理器 — 支持 A股/港股/美股"""

    def __init__(self, tushare_token: Optional[str] = None):
        self.tushare_token = tushare_token
        self.circuit_breaker = CircuitBreaker()
        self.cache: Dict[str, Dict] = {}
        self.cache_time: Dict[str, datetime] = {}
        self.cache_ttl = 300

        # A股/港股数据源优先级
        self.cn_hk_sources = self._init_cn_hk_sources()
        # 美股数据源
        self.us_sources = ['yfinance']

        logger.info(
            f"DataFetcherManager 初始化完成, "
            f"A股/港股源: {self.cn_hk_sources}, 美股源: {self.us_sources}"
        )

    def _init_cn_hk_sources(self) -> List[str]:
        """初始化 A股/港股 数据源优先级列表"""
        sources = ['tencent', 'akshare', 'yfinance']
        if self.tushare_token:
            sources.insert(1, 'tushare')
            logger.info("检测到 Tushare Token，加入 Tushare 数据源")
        return sources

    def _random_sleep(self, min_s: float = 0.5, max_s: float = 2.0):
        time.sleep(random.uniform(min_s, max_s))

    # ---------- 市场检测 ----------

    def _detect_market(self, stock_code: str) -> str:
        return detect_market(stock_code)

    def _normalize_code(self, stock_code: str, for_source: str = 'auto') -> str:
        code = stock_code.strip().upper()
        if '.' in code:
            parts = code.split('.')
            code_num = parts[0]
        else:
            code_num = code

        if code_num.isdigit() and 4 <= len(code_num) <= 5:
            code_num = code_num.zfill(5)
            if for_source == 'yfinance':
                return f"{code_num}.HK"
            return code_num
        if code_num.isdigit() and len(code_num) == 6:
            if for_source == 'yfinance':
                return f"{code_num}.SS" if code_num.startswith('6') else f"{code_num}.SZ"
            return code_num
        return code

    # ---------- 缓存 ----------

    def get_cache(self, key: str) -> Optional[Dict]:
        if key not in self.cache:
            return None
        cache_time = self.cache_time.get(key)
        if cache_time and (datetime.now() - cache_time).total_seconds() < self.cache_ttl:
            return self.cache[key]
        del self.cache[key]
        del self.cache_time[key]
        return None

    def set_cache(self, key: str, data: Dict):
        self.cache[key] = data
        self.cache_time[key] = datetime.now()

    # ---------- 统一入口 ----------

    def get_realtime_data(self, stock_code: str) -> Tuple[pd.DataFrame, str]:
        """获取实时行情（自动路由 + 故障转移）"""
        market = self._detect_market(stock_code)
        normalized = self._normalize_code(stock_code)

        cached = self.get_cache(f"rt_{normalized}")
        if cached:
            return pd.DataFrame([cached]), 'cache'

        if market == 'us':
            sources = self.us_sources
        else:
            sources = self.cn_hk_sources

        errors = []
        for src in sources:
            if self.circuit_breaker.is_open(src):
                continue
            try:
                self._random_sleep(0.5, 1.5)
                df = self._dispatch_realtime(src, stock_code, normalized, market)
                if df is not None and not df.empty:
                    self.circuit_breaker.record_success(src)
                    self.set_cache(f"rt_{normalized}", df.iloc[0].to_dict())
                    logger.info(f"✅ realtime 使用: {src}")
                    return df, src
            except Exception as e:
                errors.append(f"[{src}] {e}")
                logger.debug(f"realtime {src} 失败: {e}")
                self.circuit_breaker.record_failure(src, e)

        # 最后尝试 yfinance（即使不在优先列表）
        if 'yfinance' not in sources and yf:
            try:
                df = self._fetch_realtime_yfinance(stock_code)
                if df is not None and not df.empty:
                    return df, 'yfinance(fallback)'
            except Exception:
                pass

        raise Exception(f"所有数据源均失败:\n" + "\n".join(errors))

    def get_history_data(self, stock_code: str, period: str = '3y') -> Tuple[pd.DataFrame, str]:
        """获取历史K线（自动路由 + 故障转移）"""
        market = self._detect_market(stock_code)
        normalized = self._normalize_code(stock_code)

        if market == 'us':
            sources = self.us_sources
        else:
            sources = self.cn_hk_sources

        errors = []
        for src in sources:
            if self.circuit_breaker.is_open(src):
                continue
            try:
                self._random_sleep(0.5, 2.0)
                df = self._dispatch_history(src, stock_code, normalized, market, period)
                if df is not None and not df.empty:
                    self.circuit_breaker.record_success(src)
                    logger.info(f"✅ history 使用: {src}")
                    return df, src
            except Exception as e:
                errors.append(f"[{src}] {e}")
                logger.debug(f"history {src} 失败: {e}")
                self.circuit_breaker.record_failure(src, e)

        if 'yfinance' not in sources and yf:
            try:
                df = self._fetch_history_yfinance(stock_code, period)
                if df is not None and not df.empty:
                    return df, 'yfinance(fallback)'
            except Exception:
                pass

        raise Exception(f"所有数据源均失败:\n" + "\n".join(errors))

    # ---------- 调度器 ----------

    def _dispatch_realtime(self, source: str, raw_code: str, normalized: str, market: str):
        if source == 'tencent':
            return self._fetch_realtime_tencent(raw_code)
        elif source == 'akshare':
            return self._fetch_realtime_akshare(normalized, market)
        elif source == 'yfinance':
            return self._fetch_realtime_yfinance(raw_code)
        return None

    def _dispatch_history(self, source: str, raw_code: str, normalized: str, market: str, period: str):
        if source == 'tencent':
            return self._fetch_history_tencent(raw_code, period)
        elif source == 'akshare':
            return self._fetch_history_akshare(normalized, market, period)
        elif source == 'yfinance':
            yf_sym = self._normalize_code(raw_code, for_source='yfinance')
            return self._fetch_history_yfinance(yf_sym, period)
        return None

    # ---------- 腾讯财经 API ----------

    def _to_tencent_code(self, symbol: str):
        s = symbol.strip().upper()
        if s.endswith('.HK'):
            return f"hk{s.split('.')[0].zfill(5)}", True
        if s.endswith(('.SH', '.SS')):
            return f"sh{s.split('.')[0]}", False
        if s.endswith('.SZ'):
            return f"sz{s.split('.')[0]}", False
        if s.isdigit():
            if len(s) == 5:
                return f"hk{s}", True
            if len(s) == 6:
                return (f"sh{s}" if s.startswith('6') else f"sz{s}"), False
        return None, None

    def _fetch_realtime_tencent(self, symbol: str) -> Optional[pd.DataFrame]:
        if requests is None:
            return None
        code, is_hk = self._to_tencent_code(symbol)
        if code is None:
            return None
        base_url = ("http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
                    if is_hk else
                    "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get")
        url = f"{base_url}?param={code},day,,,5,qfq"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://stock.finance.qq.com/'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json()
        if data.get('code') != 0:
            return None
        stock_data = data.get('data', {}).get(code)
        if not stock_data:
            return None
        for key in ['qfqday', 'day']:
            if key in stock_data and stock_data[key]:
                last = stock_data[key][-1]
                return pd.DataFrame([{
                    '股票代码': symbol,
                    '股票名称': symbol,
                    '最新价': float(last[2]),
                    '涨跌幅(%)': 0,
                    '成交量': int(float(last[5])),
                    '成交额': float(last[1]) * float(last[5]),
                    '市盈率': 0,
                    '市净率': 0,
                }])
        return None

    def _fetch_history_tencent(self, symbol: str, period: str) -> Optional[pd.DataFrame]:
        if requests is None:
            return None
        code, is_hk = self._to_tencent_code(symbol)
        if code is None:
            return None
        period_days = {'1mo': 22, '3mo': 66, '6mo': 126, '1y': 252,
                       '2y': 504, '3y': 756, '5y': 1260, '10y': 2520, 'max': 3000}
        count = period_days.get(period, 756)
        base_url = ("http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
                    if is_hk else
                    "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get")
        url = f"{base_url}?param={code},day,,,{count},qfq"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://stock.finance.qq.com/'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json()
        if data.get('code') != 0:
            return None
        stock_data = data.get('data', {}).get(code)
        if not stock_data:
            return None
        import numpy as np
        for key in ['qfqday', 'day']:
            if key in stock_data and stock_data[key]:
                rows = []
                for item in stock_data[key]:
                    h, l = float(item[3]), float(item[4])
                    rows.append({
                        'Date': item[0], 'Open': float(item[1]),
                        'Close': float(item[2]), 'High': max(h, l),
                        'Low': min(h, l), 'Volume': float(item[5]),
                    })
                df = pd.DataFrame(rows)
                df['Amount'] = (df['Open'] * df['Volume']).fillna(0)
                df['Amplitude'] = ((df['High'] - df['Low']) / df['Low'].replace(0, np.nan) * 100).fillna(0)
                df['Change_Pct'] = df['Close'].pct_change().fillna(0) * 100
                df['Change'] = df['Close'].diff().fillna(0)
                df['Turnover'] = 0
                return df
        return None

    # ---------- AkShare ----------

    def _fetch_realtime_akshare(self, code: str, market: str) -> Optional[pd.DataFrame]:
        if ak is None:
            return None
        if market in ('a_sh', 'a_sz'):
            df_all = ak.stock_zh_a_spot_em()
            row = df_all[df_all['代码'] == code]
        elif market == 'hk':
            code = code.zfill(5)
            df_all = ak.stock_hk_spot_em()
            row = df_all[df_all['代码'] == code]
        else:
            return None
        if row.empty:
            return None
        r = row.iloc[0]

        def sf(key, default=0.0):
            try:
                if key in r and pd.notna(r[key]):
                    return float(r[key])
            except Exception:
                pass
            return default

        return pd.DataFrame([{
            '股票代码': code, '股票名称': r.get('名称', code),
            '最新价': sf('最新价'), '涨跌幅(%)': sf('涨跌幅'),
            '成交量': int(sf('成交量')), '成交额': sf('成交额'),
            '市盈率': sf('市盈率-动态', sf('市盈率')),
            '市净率': sf('市净率'),
        }])

    def _fetch_history_akshare(self, code: str, market: str, period: str) -> Optional[pd.DataFrame]:
        if ak is None:
            return None
        period_days = {'1mo': 35, '3mo': 100, '6mo': 200, '1y': 370,
                       '2y': 740, '3y': 1100, '5y': 1850, '10y': 3700}
        days = period_days.get(period, 1100)
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')

        if market in ('a_sh', 'a_sz'):
            df = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date, adjust="qfq"
            )
        elif market == 'hk':
            code = code.zfill(5)
            df = ak.stock_hk_hist(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date, adjust="qfq"
            )
        else:
            return None

        if df is None or df.empty:
            return None

        col_map = {
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume',
            '成交额': 'Amount', '振幅': 'Amplitude',
            '涨跌幅': 'Change_Pct', '涨跌额': 'Change', '换手率': 'Turnover'
        }
        df = df.rename(columns=col_map)
        return df

    # ---------- YFinance（带速率限制保护） ----------

    _yf_ticker_cache = {}
    _yf_info_cache = {}
    _yf_last_request = 0

    def _yf_throttle(self):
        """确保 yfinance 请求间隔 >= 2秒"""
        now = time.time()
        elapsed = now - DataFetcherManager._yf_last_request
        if elapsed < 2.0:
            time.sleep(2.0 - elapsed)
        DataFetcherManager._yf_last_request = time.time()

    def _yf_get_ticker(self, symbol):
        if symbol not in DataFetcherManager._yf_ticker_cache:
            DataFetcherManager._yf_ticker_cache[symbol] = yf.Ticker(symbol)
        return DataFetcherManager._yf_ticker_cache[symbol]

    def _yf_call_with_retry(self, func, label="yfinance", max_retries=3):
        """带指数退避重试的 yfinance 调用"""
        for attempt in range(max_retries):
            self._yf_throttle()
            try:
                return func()
            except Exception as e:
                if 'RateLimit' in type(e).__name__ or 'Too Many Requests' in str(e):
                    wait = 3 * (2 ** attempt)
                    logger.warning(f"{label} 速率限制 ({attempt+1}/{max_retries})，等待 {wait}s")
                    time.sleep(wait)
                    DataFetcherManager._yf_ticker_cache.clear()
                    DataFetcherManager._yf_info_cache.clear()
                    if attempt == max_retries - 1:
                        raise
                else:
                    raise
        return None

    def _fetch_realtime_yfinance(self, stock_code: str) -> Optional[pd.DataFrame]:
        if yf is None:
            return None
        yf_sym = self._normalize_code(stock_code, for_source='yfinance')

        # 使用 info 缓存
        if yf_sym in DataFetcherManager._yf_info_cache:
            info = DataFetcherManager._yf_info_cache[yf_sym]
        else:
            def _fetch():
                ticker = self._yf_get_ticker(yf_sym)
                return ticker.info
            info = self._yf_call_with_retry(_fetch, f"yfinance.info({yf_sym})")
            if info:
                DataFetcherManager._yf_info_cache[yf_sym] = info

        if not info:
            return None
        price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        prev = info.get('previousClose') or price
        return pd.DataFrame([{
            '股票代码': stock_code,
            '股票名称': info.get('shortName', stock_code),
            '最新价': float(price),
            '涨跌幅(%)': ((float(price) / float(prev)) - 1) * 100 if prev else 0,
            '成交量': int(info.get('volume', 0)),
            '成交额': int(info.get('volume', 0)) * float(price),
            '市盈率': float(info.get('trailingPE', 0)),
            '市净率': float(info.get('priceToBook', 0)),
        }])

    def _fetch_history_yfinance(self, stock_code: str, period: str) -> Optional[pd.DataFrame]:
        """历史K线：只调用 history()，不触发 info"""
        if yf is None:
            return None

        def _fetch():
            ticker = self._yf_get_ticker(stock_code)
            return ticker.history(period=period)

        df = self._yf_call_with_retry(_fetch, f"yfinance.history({stock_code})")
        if df is None or df.empty:
            return None
        df = df.reset_index()
        required = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if 'Date' not in df.columns and len(df.columns) > 0:
            df = df.rename(columns={df.columns[0]: 'Date'})
        if not all(c in df.columns for c in required):
            return None
        return df[required]

    # ---------- 批量预取 ----------

    def prefetch_realtime_quotes(self, stock_codes: List[str]):
        """批量预取实时行情（仅 A股，性能优化）"""
        a_codes = [c for c in stock_codes if detect_market(c) in ('a_sh', 'a_sz')]
        if len(a_codes) < 5 or ak is None:
            return
        logger.info(f"批量预取 {len(a_codes)} 只 A股...")
        try:
            df = ak.stock_zh_a_spot_em()
            cached = 0
            for code in a_codes:
                normalized = self._normalize_code(code)
                row = df[df['代码'] == normalized]
                if not row.empty:
                    r = row.iloc[0]
                    self.set_cache(f"rt_{normalized}", {
                        '股票代码': normalized, '股票名称': r['名称'],
                        '最新价': float(r['最新价']),
                        '涨跌幅(%)': float(r['涨跌幅']),
                        '成交量': int(r['成交量']),
                        '成交额': float(r['成交额']),
                        '市盈率': float(r.get('市盈率-动态', 0)),
                        '市净率': float(r.get('市净率', 0)),
                    })
                    cached += 1
            logger.info(f"✅ 批量预取: {cached}/{len(a_codes)}")
        except Exception as e:
            logger.warning(f"批量预取失败: {e}")


# 模块级单例
_fetcher_manager: Optional[DataFetcherManager] = None


def get_fetcher_manager(tushare_token: Optional[str] = None) -> DataFetcherManager:
    global _fetcher_manager
    if _fetcher_manager is None:
        _fetcher_manager = DataFetcherManager(tushare_token=tushare_token)
    return _fetcher_manager
