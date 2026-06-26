"""数据提供层 - Tushare（选装）+ 东方财富 + Yahoo（选装）+ 长桥（选装）+ 缓存 + 重试"""
from __future__ import annotations
import logging, os, time
from typing import Any, Dict, List, Optional
from datetime import date, timedelta
import requests, pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from ..config import get_config
from ..models import StockInfo, MoneyFlow, SectorFlow, DragonTiger, DataSource

logger = logging.getLogger(__name__)


def _validate_credentials(required_vars: List[str]) -> None:
    """验证必需的环境变量是否存在"""
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.warning(f"缺少环境变量: {', '.join(missing)}，相关功能将不可用")


def _validate_token_format(token: str, var_name: str) -> bool:
    """验证 token 格式是否安全（非占位符）"""
    if not token:
        return False
    placeholders = ["your_", "xxx", "test", "placeholder", "example"]
    if any(p in token.lower() for p in placeholders):
        logger.warning(f"{var_name} 看起来是占位符，请设置真实的 API Token")
        return False
    return True

_retry = retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1,min=1,max=10),
    retry=retry_if_exception_type((requests.RequestException,ConnectionError,TimeoutError)),
    before_sleep=before_sleep_log(logger,logging.WARNING), reraise=True)

class _Cache:
    def __init__(self, ttl=300): self._s={}; self._ttl=ttl
    def get(self, k):
        if k in self._s:
            entry = self._s[k]
            if len(entry) == 2:
                v, t = entry
                entry_ttl = self._ttl
            else:
                v, t, entry_ttl = entry
            if time.time() - t < entry_ttl: return v
            del self._s[k]
        return None
    def set(self, k, v, ttl=None):
        effective_ttl = ttl if ttl is not None else self._ttl
        self._s[k] = (v, time.time(), effective_ttl)

_cache = _Cache()

class TushareProvider:
    """Tushare 数据源（选装）
    
    需要安装: pip install beergaao[tushare] 或 pip install tushare
    """
    def __init__(self):
        try:
            import tushare as ts
        except ImportError:
            logger.warning("tushare 未安装，请运行: pip install beergaao[tushare]")
            self._pro = None
            return
        cfg = get_config()
        if cfg.tushare_token and _validate_token_format(cfg.tushare_token, "TUSHARE_TOKEN"):
            ts.set_token(cfg.tushare_token)
        else:
            logger.warning("TUSHARE_TOKEN 未配置或无效，Tushare 数据源不可用")
        self._pro = ts.pro_api()

    @_retry
    def get_daily(self, code, start, end):
        if not self._pro:
            return pd.DataFrame()
        k = f"daily:{code}:{start}:{end}"
        c = _cache.get(k)
        if c is not None: return c
        df = self._pro.daily(ts_code=code, start_date=start, end_date=end)
        if df is not None and not df.empty:
            df = df.sort_values("trade_date").reset_index(drop=True)
            _cache.set(k, df)
        return df if df is not None else pd.DataFrame()

    @_retry
    def get_market_daily(self, td):
        if not self._pro:
            return pd.DataFrame()
        k = f"market:{td}"
        c = _cache.get(k)
        if c is not None: return c
        df = self._pro.daily(trade_date=td)
        if df is not None: _cache.set(k, df)
        return df if df is not None else pd.DataFrame()

    @_retry
    def get_stock_info(self, code):
        if not self._pro:
            return StockInfo(code=code, name=code)
        k = f"info:{code}"
        c = _cache.get(k)
        if c is not None: return c
        df = self._pro.stock_basic(ts_code=code, fields="ts_code,name,industry,market")
        if df is not None and not df.empty:
            r = df.iloc[0]
            info = StockInfo(code=code, name=r.get("name",code), industry=r.get("industry",""), market=r.get("market",""))
            _cache.set(k, info, 86400)
            return info
        return StockInfo(code=code, name=code)

    @_retry
    def get_trade_dates(self, end, n):
        if not self._pro:
            return []
        df = self._pro.trade_cal(exchange="SSE", end_date=end, is_open="1")
        if df is not None and len(df)>=n: return df.head(n)["cal_date"].tolist()
        return []

    @_retry
    def get_dragon_tiger(self, td):
        if not self._pro:
            return []
        df = self._pro.top_list(trade_date=td)
        if df is None or df.empty: return []
        return [DragonTiger(code=r.get("ts_code",""),name=r.get("name",""),close=float(r.get("close",0)),
            pct_change=float(r.get("pct_change",0)),net_amount=float(r.get("amount",0)),
            buy_amount=float(r.get("l_buy",0)),sell_amount=float(r.get("l_sell",0)),reason=r.get("reason","")) for _,r in df.head(10).iterrows()]

class EastMoneyProvider:
    HEADERS = {"User-Agent":"Mozilla/5.0","Referer":"https://quote.eastmoney.com/"}
    def __init__(self):
        self._t = get_config().http_timeout
    @property
    def _UT(self):
        return os.getenv("EASTMONEY_UT", "fa5fd1943c7b386f172d6893dbbd1131")
    @staticmethod
    def _secid(code):
        c = code.split(".")[0]
        if code.endswith(".SH"):
            return f"1.{c}"
        elif code.endswith(".HK"):
            return f"116.{c.zfill(5)}"
        return f"0.{c}"

    @_retry
    def get_realtime_quote(self, code):
        k = f"quote:{code}"; c = _cache.get(k)
        if c is not None: return c
        r = requests.get("https://push2.eastmoney.com/api/qt/stock/get",
            params={"secid":self._secid(code),"fields":"f57,f58,f43,f169,f170,f46,f47,f44,f51","ut":self._UT},
            headers=self.HEADERS, timeout=self._t)
        r.raise_for_status(); d = r.json()
        if d.get("data"):
            dd = d["data"]
            res = {"code":code,"name":dd.get("f58",""),"price":dd.get("f43",0)/100,"change_pct":dd.get("f170",0)/100,
                   "volume":dd.get("f47",0),"amount":dd.get("f46",0)/10000,"high":dd.get("f44",0)/100,"low":dd.get("f51",0)/100}
            _cache.set(k, res, 60); return res
        return {}

    @_retry
    def get_money_flow(self, code):
        k = f"flow:{code}"; c = _cache.get(k)
        if c is not None: return c
        r = requests.get("https://push2.eastmoney.com/api/qt/stock/fflow/kline/get",
            params={"secid":self._secid(code),"fields1":"f1,f2,f3,f7","fields2":"f51,f52,f53,f54,f55,f56,f57","klt":"1","lmt":"1"},
            headers=self.HEADERS, timeout=self._t)
        r.raise_for_status(); d = r.json()
        if d.get("data") and d["data"].get("klines"):
            p = d["data"]["klines"][0].split(",")
            if len(p)>=6:
                res = MoneyFlow(code=code,name="",main_net_inflow=round(float(p[1])/10000,2),
                    super_large_net=round(float(p[2])/10000,2),large_net=round(float(p[3])/10000,2),
                    medium_net=round(float(p[4])/10000,2),small_net=round(float(p[5])/10000,2))
                _cache.set(k, res, 120); return res
        return None

    @_retry
    def get_sector_flow(self, limit=10):
        k = f"sector:{limit}"; c = _cache.get(k)
        if c is not None: return c
        r = requests.get("https://push2.eastmoney.com/api/qt/clist/get",
            params={"fid":"f62","po":"1","pz":str(limit),"pn":"1","np":"1","fltt":"2","invt":"2",
                    "fs":"b:BK04801+f:!50","fields":"f12,f14,f2,f3,f62"},
            headers=self.HEADERS, timeout=self._t)
        r.raise_for_status(); d = r.json()
        sectors = []
        if d.get("data") and d["data"].get("diff"):
            for item in d["data"]["diff"]:
                sectors.append(SectorFlow(sector_name=item.get("f14",""),change_pct=round(item.get("f3",0),2),
                    main_net_inflow=round(item.get("f62",0)/10000,2)))
        _cache.set(k, sectors, 120); return sectors

class YahooProvider:
    """雅虎财经数据源（选装）- 支持美股/港股/A股
    
    需要安装: pip install yfinance
    """
    def __init__(self):
        try:
            import yfinance as yf
            self._yf = yf
        except ImportError:
            logger.warning("yfinance 未安装，请运行: pip install yfinance")
            self._yf = None

    def _convert_code(self, code: str) -> str:
        """转换股票代码为雅虎格式"""
        if code.endswith(".SH"):
            return code.replace(".SH", ".SS")
        return code

    @_retry
    def get_daily(self, code: str, start: str, end: str) -> pd.DataFrame:
        """获取历史日线数据"""
        if not self._yf:
            return pd.DataFrame()
        
        k = f"yahoo_daily:{code}:{start}:{end}"
        c = _cache.get(k)
        if c is not None:
            return c
        
        try:
            yahoo_code = self._convert_code(code)
            ticker = self._yf.Ticker(yahoo_code)
            df = ticker.history(start=start, end=end)
            if df is not None and not df.empty:
                df = df.reset_index()
                df = df.rename(columns={"Date": "date", "Open": "open", "High": "high", 
                                       "Low": "low", "Close": "close", "Volume": "volume"})
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                _cache.set(k, df)
                return df
        except Exception as e:
            logger.warning(f"Yahoo 获取 {code} 数据失败: {e}")
        return pd.DataFrame()

    @_retry
    def get_realtime_quote(self, code: str) -> Dict[str, Any]:
        """获取实时行情"""
        if not self._yf:
            return {}
        
        k = f"yahoo_quote:{code}"
        c = _cache.get(k)
        if c is not None:
            return c
        
        try:
            yahoo_code = self._convert_code(code)
            ticker = self._yf.Ticker(yahoo_code)
            info = ticker.info
            if info:
                res = {
                    "code": code,
                    "name": info.get("shortName", ""),
                    "price": info.get("regularMarketPrice", 0),
                    "change_pct": info.get("regularMarketChangePercent", 0),
                    "volume": info.get("regularMarketVolume", 0),
                    "amount": info.get("regularMarketVolume", 0) * info.get("regularMarketPrice", 0),
                    "high": info.get("regularMarketDayHigh", 0),
                    "low": info.get("regularMarketDayLow", 0)
                }
                _cache.set(k, res, 60)
                return res
        except Exception as e:
            logger.warning(f"Yahoo 获取 {code} 行情失败: {e}")
        return {}

class LongportProvider:
    """长桥数据源（选装）- 支持美股/港股/A股（仅数据查询，不执行交易）
    
    需要安装: pip install longport
    需要配置: LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN
    """
    def __init__(self):
        cfg = get_config()
        self._config = cfg
        self._quote_ctx = None
        self._trade_ctx = None
        self._initialized = False
        # 验证凭证
        if cfg.longport_app_key and cfg.longport_access_token:
            _validate_credentials(["LONGPORT_APP_KEY", "LONGPORT_APP_SECRET", "LONGPORT_ACCESS_TOKEN"])

    def _init_context(self):
        """初始化长桥上下文"""
        if self._initialized:
            return

        # 验证凭证完整性
        if not all([self._config.longport_app_key, self._config.longport_app_secret, self._config.longport_access_token]):
            logger.warning("长桥凭证不完整，请配置 LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN")
            return
        
        try:
            from longport.openapi import Config, QuoteContext, TradeContext
            lp_config = {
                "app_key": self._config.longport_app_key,
                "app_secret": self._config.longport_app_secret,
                "access_token": self._config.longport_access_token,
            }
            config = Config(**lp_config)
            self._quote_ctx = QuoteContext(config)
            self._trade_ctx = TradeContext(config)
            self._initialized = True
        except ImportError:
            logger.warning("longport 未安装，请运行: pip install longport")
        except Exception as e:
            logger.warning(f"长桥初始化失败: {e}")

    def _convert_code(self, code: str) -> str:
        """长桥直接使用 .SH/.SZ/.HK 格式，无需转换"""
        return code

    @_retry
    def get_quote(self, codes: List[str]) -> List[Dict[str, Any]]:
        """获取实时行情"""
        self._init_context()
        if not self._quote_ctx:
            return []
        
        try:
            longport_codes = [self._convert_code(c) for c in codes]
            resp = self._quote_ctx.quote(longport_codes)
            result = []
            for quote in resp:
                result.append({
                    "code": quote.symbol,
                    "name": quote.name,
                    "price": quote.last_done,
                    "change_pct": quote.change_percentage,
                    "volume": quote.volume,
                    "amount": quote.turnover,
                    "high": quote.high,
                    "low": quote.low
                })
            return result
        except Exception as e:
            logger.warning(f"长桥获取行情失败: {e}")
            return []

    @_retry
    def get_realtime_quote(self, code: str) -> Dict[str, Any]:
        """获取单只股票实时行情"""
        k = f"longport_quote:{code}"
        c = _cache.get(k)
        if c is not None:
            return c
        
        quotes = self.get_quote([code])
        if quotes:
            _cache.set(k, quotes[0], 60)
            return quotes[0]
        return {}

class DataGateway:
    """数据网关 - 整合多数据源
    
    核心数据源（必装）：
        - 东方财富: 实时行情、资金流向
    
    可选数据源（选装）：
        - Tushare: 历史K线、基本面数据（需安装 tushare）
        - Yahoo Finance: 美股/港股行情（需安装 yfinance）
        - 长桥 OpenAPI: 美股/港股行情（需安装 longport 并配置凭证）
    """
    def __init__(self): 
        self._tushare = None
        self.eastmoney = EastMoneyProvider()
        self._yahoo = None
        self._longport = None
    
    @property
    def tushare(self):
        """延迟加载 Tushare Provider（可选依赖）"""
        if self._tushare is None:
            self._tushare = TushareProvider()
        return self._tushare
    
    @property
    def yahoo(self):
        """延迟加载 Yahoo Provider（可选依赖）"""
        if self._yahoo is None:
            self._yahoo = YahooProvider()
        return self._yahoo
    
    @property
    def longport(self):
        """延迟加载 Longport Provider（可选依赖）"""
        if self._longport is None:
            self._longport = LongportProvider()
        return self._longport
    
    def _check_tushare(self) -> bool:
        """检查 Tushare 是否可用"""
        if self.tushare._pro is None:
            logger.warning("Tushare 数据源不可用（未安装或未配置），请运行: pip install beergaao[tushare]")
            return False
        return True
    
    def get_kline(self, code, days=250, source="tushare"):
        """获取K线数据，支持多数据源
        
        Args:
            code: 股票代码
            days: 获取天数
            source: 数据源，可选 "tushare"（默认，需安装）、"yahoo"（选装，需安装 yfinance）
        """
        end = date.today().strftime("%Y%m%d")
        start = (date.today()-timedelta(days=days)).strftime("%Y%m%d")
        
        if source == "yahoo":
            if self.yahoo._yf is None:
                logger.warning("Yahoo 数据源不可用（yfinance 未安装），将使用 Tushare 作为备选")
                source = "tushare"
            else:
                df = self.yahoo.get_daily(code, start, end)
                if not df.empty:
                    for c in ["open","high","low","close","volume"]:
                        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
                    return df
                logger.warning(f"Yahoo 获取 {code} 数据失败，将使用 Tushare 作为备选")
                source = "tushare"
        
        # 默认使用 tushare
        if not self._check_tushare():
            return pd.DataFrame()
        df = self.tushare.get_daily(code, start, end)
        if df.empty: return df
        df = df.rename(columns={"vol":"volume","trade_date":"date"})
        for c in ["open","high","low","close","volume","amount"]:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
        return df
    
    def get_market_snapshot(self, td=None):
        if not self._check_tushare():
            return pd.DataFrame()
        if not td: td = date.today().strftime("%Y%m%d")
        return self.tushare.get_market_daily(td)
    
    def get_stock_info(self, code):
        if not self._check_tushare():
            return StockInfo(code=code, name=code)
        return self.tushare.get_stock_info(code)
    
    def get_money_flow(self, code):
        f = self.eastmoney.get_money_flow(code)
        if f: f.name = self.get_stock_info(code).name
        return f
    
    def get_sector_flow(self, limit=10): return self.eastmoney.get_sector_flow(limit)
    
    def get_dragon_tiger(self):
        if not self._check_tushare():
            return []
        return self.tushare.get_dragon_tiger(date.today().strftime("%Y%m%d"))
    
    def get_realtime_quote(self, code, source="eastmoney"):
        """获取实时行情，支持多数据源
        
        Args:
            code: 股票代码
            source: 数据源，可选 "eastmoney"（默认）、"yahoo"（选装）、"longport"（选装）
        """
        if source == "yahoo":
            if self.yahoo._yf is None:
                logger.warning("Yahoo 数据源不可用（yfinance 未安装），将使用东方财富作为备选")
                return self.eastmoney.get_realtime_quote(code)
            return self.yahoo.get_realtime_quote(code)
        elif source == "longport":
            self.longport._init_context()
            if not self.longport._quote_ctx:
                logger.warning("长桥数据源不可用（凭证未配置或 longport 未安装），将使用东方财富作为备选")
                return self.eastmoney.get_realtime_quote(code)
            return self.longport.get_realtime_quote(code)
        return self.eastmoney.get_realtime_quote(code)
    
    def get_recent_trade_dates(self, n=5):
        if not self._check_tushare():
            return []
        return self.tushare.get_trade_dates(date.today().strftime("%Y%m%d"), n)
