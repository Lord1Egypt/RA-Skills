#!/usr/bin/env python3
"""
投资研究系统 - 多数据源模块
支持多个数据源：腾讯财经、AKShare、东方财富

数据源优先级：
1. 腾讯财经 (qt.gtimg.cn) - 实时行情
2. AKShare - 财经数据（如果安装）
3. 东方财富 - 行情和资讯
"""
import requests
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import time
import sys
import os

try:
    from config import REQUEST_TIMEOUT, REQUEST_DELAY
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    REQUEST_TIMEOUT = 10
    REQUEST_DELAY = 0.3

# 尝试导入 AKShare
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("Warning: AKShare not installed, some features will be limited")


class MultiDataSource:
    """多数据源管理器"""
    
    # 白名单域名
    ALLOWED_DOMAINS = [
        "qt.gtimg.cn",      # 腾讯财经
        "push2.eastmoney.com",  # 东方财富
        "stock.xueqiu.com",     # 雪球
    ]
    
    def __init__(self, delay: float = REQUEST_DELAY, preferred_source: str = "auto"):
        self.delay = delay
        self.preferred_source = preferred_source  # auto/tengxun/akshare/dongfang
        self._cache = {}
        self._cache_timeout = 60  # 缓存60秒
        self._last_request_time = {}
        
        # 各数据源状态
        self.source_status = {
            "tengxun": {"available": True, "latency": 0},
            "akshare": {"available": HAS_AKSHARE, "latency": 0},
            "dongfang": {"available": True, "latency": 0}
        }
    
    def _get_market(self, code: str) -> str:
        """判断市场代码"""
        if code.startswith('6'):
            return 'sh'
        elif code.startswith(('0', '3')):
            return 'sz'
        elif code.startswith('8') or code.startswith('4'):
            return 'bj'  # 北交所
        return 'sz'
    
    def _check_cache(self, key: str) -> Optional[Any]:
        """检查缓存"""
        if key in self._cache:
            cached_time, cached_data = self._cache[key]
            if time.time() - cached_time < self._cache_timeout:
                return cached_data
        return None
    
    def _set_cache(self, key: str, data: Any):
        """设置缓存"""
        self._cache[key] = (time.time(), data)
    
    def _rate_limit(self, source: str):
        """请求频率限制"""
        current_time = time.time()
        if source in self._last_request_time:
            elapsed = current_time - self._last_request_time[source]
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        self._last_request_time[source] = current_time
    
    # ==================== 腾讯财经 ====================
    
    def get_realtime_quote_tengxun(self, code: str) -> Dict[str, Any]:
        """获取实时行情（腾讯财经）"""
        self._rate_limit("tengxun")
        market = self._get_market(code)
        
        try:
            url = f'https://qt.gtimg.cn/q={market}{code}'
            start = time.time()
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            self.source_status["tengxun"]["latency"] = time.time() - start
            
            text = resp.content.decode('gbk')
            
            if '~' in text:
                parts = text.split('~')
                return {
                    "source": "tengxun",
                    "code": code,
                    "name": parts[1] if len(parts) > 1 else "",
                    "price": self._safe_float(parts[3]) if len(parts) > 3 else 0,
                    "change": self._safe_float(parts[4]) if len(parts) > 4 else 0,
                    "change_pct": self._safe_float(parts[5]) if len(parts) > 5 else 0,
                    "volume": self._safe_float(parts[6]) if len(parts) > 6 else 0,
                    "amount": self._safe_float(parts[7]) if len(parts) > 7 else 0,
                    "open": self._safe_float(parts[17]) if len(parts) > 17 else 0,
                    "high": self._safe_float(parts[33]) if len(parts) > 33 else 0,
                    "low": self._safe_float(parts[34]) if len(parts) > 34 else 0,
                    "close": self._safe_float(parts[3]) if len(parts) > 3 else 0,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.source_status["tengxun"]["available"] = False
            return {"error": str(e), "source": "tengxun"}
        
        return {"error": "No data", "source": "tengxun"}
    
    # ==================== AKShare ====================
    
    def get_realtime_quote_akshare(self, code: str) -> Dict[str, Any]:
        """获取实时行情（AKShare）"""
        if not HAS_AKSHARE:
            return {"error": "AKShare not installed", "source": "akshare"}
        
        self._rate_limit("akshare")
        start = time.time()
        
        try:
            # 转换代码格式
            market = self._get_market(code)
            symbol = f"{market}{code}"
            
            # 使用 AKShare 获取实时行情
            df = ak.stock_zh_a_spot_em()
            stock = df[df['代码'] == code]
            
            if not stock.empty:
                row = stock.iloc[0]
                self.source_status["akshare"]["latency"] = time.time() - start
                return {
                    "source": "akshare",
                    "code": code,
                    "name": row.get('名称', ''),
                    "price": float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else 0,
                    "change": float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
                    "change_pct": float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
                    "volume": float(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else 0,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.source_status["akshare"]["available"] = False
            return {"error": str(e), "source": "akshare"}
        
        return {"error": "No data", "source": "akshare"}
    
    def get_financial_data_akshare(self, code: str, indicator: str = "main") -> Dict[str, Any]:
        """获取财务数据（AKShare）"""
        if not HAS_AKSHARE:
            return {"error": "AKShare not installed", "source": "akshare"}
        
        try:
            # 获取财务指标
            if indicator == "main":
                df = ak.stock_financial_abstract_ths(symbol=code)
            else:
                df = ak.stock_financial_analysis_indicator(symbol=code)
            
            return {
                "source": "akshare",
                "data": df.to_dict('records') if not df.empty else [],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "source": "akshare"}
    
    def get_fund_data_akshare(self, fund_code: str) -> Dict[str, Any]:
        """获取基金数据（AKShare）"""
        if not HAS_AKSHARE:
            return {"error": "AKShare not installed", "source": "akshare"}
        
        try:
            # 基金净值
            df = ak.fund_nav_em(fund=fund_code)
            
            # 基金持仓
            df_holding = ak.fund_portfolio_hold_em(fund=fund_code)
            
            return {
                "source": "akshare",
                "nav": df.to_dict('records') if not df.empty else [],
                "holding": df_holding.to_dict('records') if not df_holding.empty else [],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "source": "akshare"}
    
    # ==================== 东方财富 ====================
    
    def get_realtime_quote_dongfang(self, code: str) -> Dict[str, Any]:
        """获取实时行情（东方财富）"""
        self._rate_limit("dongfang")
        market = self._get_market(code)
        
        try:
            # 东财实时行情接口
            url = f'https://push2.eastmoney.com/api/qt/stock/get'
            params = {
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
                "invt": "2",
                "fltt": "2",
                "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f59,f60,f116,f117,f162,f163,f164,f167,f168,f169,f170,f171,f173,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203",
                "secid": f"{1 if market == 'sh' else 0}.{code}"
            }
            
            start = time.time()
            resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            self.source_status["dongfang"]["latency"] = time.time() - start
            
            data = resp.json()
            if "data" in data and data["data"]:
                f = data["data"]
                # 东方财富价格字段需要除以100
                return {
                    "source": "dongfang",
                    "code": code,
                    "name": f.get("f57", ""),
                    "price": float(f.get("f43", 0)) / 100 if f.get("f43") else 0,
                    "change": float(f.get("f4", 0)) / 100 if f.get("f4") else 0,
                    "change_pct": float(f.get("f3", 0)) / 100 if f.get("f3") else 0,
                    "volume": f.get("f47", 0),
                    "amount": f.get("f48", 0),
                    "open": float(f.get("f17", 0)) / 100 if f.get("f17") else 0,
                    "high": float(f.get("f15", 0)) / 100 if f.get("f15") else 0,
                    "low": float(f.get("f16", 0)) / 100 if f.get("f16") else 0,
                    "close": float(f.get("f2", 0)) / 100 if f.get("f2") else 0,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.source_status["dongfang"]["available"] = False
            return {"error": str(e), "source": "dongfang"}
        
        return {"error": "No data", "source": "dongfang"}
    
    def get_news_dongfang(self, code: str) -> List[Dict]:
        """获取个股新闻（东方财富）"""
        try:
            url = f'https://np-anotice-stock.eastmoney.com/api/config/get'
            params = {
                "ut": "7eea3edcaed7348a8b9960e3db6c4338",
                "codes": code,
                "page": 1,
                "pageSize": 10
            }
            
            resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            data = resp.json()
            
            news_list = []
            if "data" in data and data["data"]:
                for item in data["data"].get("data", []):
                    news_list.append({
                        "title": item.get("title", ""),
                        "time": item.get("datetime", ""),
                        "source": item.get("信息来源", ""),
                        "url": item.get("url", "")
                    })
            
            return news_list
        except Exception as e:
            return []
    
    # ==================== 统一接口 ====================
    
    def get_realtime_quote(self, code: str, source: str = "auto") -> Dict[str, Any]:
        """获取实时行情（自动选择最佳数据源）"""
        cache_key = f"quote_{code}_{source}"
        cached = self._check_cache(cache_key)
        if cached:
            return cached
        
        if source == "auto":
            # 优先使用腾讯财经
            result = self.get_realtime_quote_tengxun(code)
            if "error" not in result:
                self._set_cache(cache_key, result)
                return result
            
            # 备用东方财富
            result = self.get_realtime_quote_dongfang(code)
            if "error" not in result:
                self._set_cache(cache_key, result)
                return result
            
            # 备用 AKShare
            if HAS_AKSHARE:
                result = self.get_realtime_quote_akshare(code)
                if "error" not in result:
                    self._set_cache(cache_key, result)
                    return result
            
            return {"error": "All sources failed", "code": code}
        
        elif source == "tengxun":
            result = self.get_realtime_quote_tengxun(code)
        elif source == "akshare":
            result = self.get_realtime_quote_akshare(code)
        elif source == "dongfang":
            result = self.get_realtime_quote_dongfang(code)
        else:
            return {"error": f"Unknown source: {source}"}
        
        if "error" not in result:
            self._set_cache(cache_key, result)
        
        return result
    
    def get_source_status(self) -> Dict[str, Any]:
        """获取数据源状态"""
        return self.source_status
    
    def get_best_source(self) -> str:
        """获取最佳数据源"""
        for source in ["tengxun", "dongfang", "akshare"]:
            if self.source_status[source]["available"]:
                return source
        return "none"
    
    def _safe_float(self, value, default: float = 0.0) -> float:
        """安全转换浮点数"""
        try:
            return float(value) if value else default
        except (ValueError, TypeError):
            return default


def test_multi_source():
    """测试多数据源"""
    fetcher = MultiDataSource()
    
    print("=== 测试多数据源 ===\n")
    
    # 测试腾讯财经
    print("1. 腾讯财经:")
    result = fetcher.get_realtime_quote_tengxun("000001")
    print(f"   平安银行: {result.get('name')} - {result.get('price')}")
    
    # 测试东方财富
    print("\n2. 东方财富:")
    result = fetcher.get_realtime_quote_dongfang("000001")
    print(f"   平安银行: {result.get('name')} - {result.get('price')}")
    
    # 测试自动选择
    print("\n3. 自动选择:")
    result = fetcher.get_realtime_quote("000001")
    print(f"   数据源: {result.get('source')} - 价格: {result.get('price')}")
    
    # 查看数据源状态
    print("\n4. 数据源状态:")
    status = fetcher.get_source_status()
    for source, info in status.items():
        print(f"   {source}: {'可用' if info['available'] else '不可用'} (延迟: {info['latency']:.3f}s)")
    
    print(f"\n最佳数据源: {fetcher.get_best_source()}")


if __name__ == "__main__":
    test_multi_source()