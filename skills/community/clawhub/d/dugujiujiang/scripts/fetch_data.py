#!/usr/bin/env python3
"""
独孤九剑 · 数据获取层 (v2.0 — 多源容灾版)
基于多数据源获取 A 股所需全维度数据，单只查询不触发封控。

数据维度：
  1. 日K线（OHLCV）— 腾讯优先，新浪备选
  2. 分钟K线 — 腾讯优先
  3. 资金流向 — 东财单只查询 + 指数退避重试
  4. 实时行情 — 新浪优先（单只），腾讯备选
  5. 股票基本信息 — 东财个股信息

变更日志 (v2.0):
  - 实时行情: 移除 stock_zh_a_spot_em() 全市场扫描 → 单只查询
  - 日K线: push2his 被封 → 切换腾讯/新浪数据源
  - 资金流向: 增加指数退避重试 + 请求间隔
  - 防御层: 随机延迟、UA轮换、数据源健康检查
"""

import json
import sys
import time
import random
import requests
from datetime import datetime, timedelta
from typing import Optional

import akshare as ak
import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════
# 防御层：速率控制 & 重试 & UA 轮换
# ══════════════════════════════════════════════════════════

# 请求间隔追踪
_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 0.8   # 最小请求间隔（秒）
_MAX_REQUEST_INTERVAL: float = 2.0   # 最大随机间隔（秒）

# User-Agent 池
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Session 缓存（同一股票同一天不重复请求）
_session_cache: dict = {}
_CACHE_TTL_SECONDS: int = 300  # 缓存有效期 5 分钟


def _random_ua() -> str:
    """返回随机 User-Agent"""
    return random.choice(_USER_AGENTS)


def _rate_limit():
    """请求间隔控制：确保两次请求之间至少间隔 0.8-2.0 秒"""
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        delay = _MIN_REQUEST_INTERVAL - elapsed + random.uniform(0, _MAX_REQUEST_INTERVAL - _MIN_REQUEST_INTERVAL)
        time.sleep(delay)
    _last_request_time = time.time()


def _cache_key(prefix: str, code: str) -> str:
    """生成缓存键"""
    today = datetime.now().strftime("%Y%m%d")
    return f"{prefix}:{code}:{today}"


def _cache_get(key: str) -> Optional[dict]:
    """读取缓存（未过期则返回）"""
    entry = _session_cache.get(key)
    if entry and (time.time() - entry["ts"]) < _CACHE_TTL_SECONDS:
        return entry["data"]
    return None


def _cache_set(key: str, data):
    """写入缓存"""
    _session_cache[key] = {"data": data, "ts": time.time()}


def _retry_with_backoff(fn, name: str, max_retries: int = 3) -> dict:
    """
    指数退避重试。
    重试间隔: 1s → 3s → 7s (带随机抖动)
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            _rate_limit()
            result = fn()
            if result is not None:
                if isinstance(result, pd.DataFrame) and result.empty:
                    last_error = f"{name}: 返回空数据"
                    continue
                return {"data": result, "success": True}
            else:
                last_error = f"{name}: 返回 None"
        except Exception as e:
            last_error = f"{name}: {str(e)}"
            if attempt < max_retries - 1:
                wait = 2 ** attempt + random.uniform(0, 1)
                time.sleep(wait)
    return {"error": last_error, "success": False}


# ══════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════

def _clean_stock_code(code: str) -> str:
    """清洗股票代码，去除 sh/sz 前缀和多余字符"""
    return code.strip().replace("sh", "").replace("sz", "").replace(" ", "")


def _to_ak_code(code: str) -> str:
    """转换为 akshare 格式（如 sh600519 或 sz002594）"""
    code = _clean_stock_code(code)
    if code.startswith(("0", "3")):
        return f"sz{code}"
    elif code.startswith("6"):
        return f"sh{code}"
    elif code.startswith("8") or code.startswith("4"):
        return f"bj{code}"
    return code


def _to_tencent_code(code: str) -> str:
    """转换为腾讯行情代码格式（如 sh600519 或 sz002594）"""
    code = _clean_stock_code(code)
    if code.startswith(("0", "3")):
        return f"sz{code}"
    elif code.startswith("6"):
        return f"sh{code}"
    elif code.startswith("8") or code.startswith("4"):
        return f"bj{code}"
    return f"sh{code}"


def _safe_fetch(fn, name: str, **kwargs):
    """安全获取数据，捕获异常后优雅返回（保留兼容旧调用）"""
    try:
        _rate_limit()
        result = fn(**kwargs)
        if result is None or (isinstance(result, pd.DataFrame) and result.empty):
            return {"error": f"{name}: 返回空数据", "success": False}
        return {"data": result, "success": True}
    except Exception as e:
        return {"error": f"{name}: {str(e)}", "success": False}


# ══════════════════════════════════════════════════════════
# 实时行情（多源：新浪 → 腾讯 → 东财单只）
# ══════════════════════════════════════════════════════════

def _fetch_quote_sina(code: str) -> Optional[dict]:
    """
    新浪财经实时行情（单只股票）
    API: http://hq.sinajs.cn/list=sh600519
    返回字段：名称、今开、昨收、现价、最高、最低、成交量、成交额 等
    """
    tc = _to_tencent_code(code)
    url = f"http://hq.sinajs.cn/list={tc}"
    headers = {
        "Referer": "http://finance.sina.com.cn",
        "User-Agent": _random_ua(),
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = "gb2312"
    text = resp.text.strip()

    if not text or "FAILED" in text or '=""' in text:
        return None

    # 提取引号内数据
    parts = text.split('"')
    if len(parts) < 2:
        return None
    fields = parts[1].split(",")
    if len(fields) < 30:
        return None

    # 新浪字段映射（标准新浪行情格式，约 30+ 字段）
    name = fields[0]
    open_price = float(fields[1]) if fields[1] else 0
    pre_close = float(fields[2]) if fields[2] else 0
    price = float(fields[3]) if fields[3] else 0
    high = float(fields[4]) if fields[4] else 0
    low = float(fields[5]) if fields[5] else 0
    volume = float(fields[8]) if fields[8] else 0   # 成交量（手）
    amount = float(fields[9]) if fields[9] else 0    # 成交额（万）

    change_pct = round((price - pre_close) / pre_close * 100, 2) if pre_close > 0 else 0
    change_amount = round(price - pre_close, 2)

    # 换手率（新浪字段位置 37 附近，不同股票可能略有差异）
    turnover_rate = 0.0
    try:
        if len(fields) > 37:
            turnover_rate = float(fields[37]) if fields[37] else 0.0
    except (ValueError, IndexError):
        pass

    return {
        "code": _clean_stock_code(code),
        "name": name,
        "price": price,
        "change_pct": change_pct,
        "change_amount": change_amount,
        "volume_ratio": 0,   # 新浪不直接提供量比，后续可计算
        "turnover_rate": turnover_rate,
        "volume": volume,
        "amount": amount,
        "high": high,
        "low": low,
        "open": open_price,
        "pre_close": pre_close,
        "pe": 0,             # 新浪单只行情不含PE，由 stock_info 补充
        "total_market_cap": 0,
    }


def _fetch_quote_tencent(code: str) -> Optional[dict]:
    """
    腾讯财经实时行情（单只股票）
    API: http://qt.gtimg.cn/q=sh600519
    返回字段丰富，包含量比、市盈率等
    """
    tc = _to_tencent_code(code)
    url = f"http://qt.gtimg.cn/q={tc}"
    headers = {"User-Agent": _random_ua()}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = "gb2312"
    text = resp.text.strip()

    if not text or "none" in text.lower():
        return None

    # 提取引号内数据
    parts = text.split('"')
    if len(parts) < 2:
        return None
    fields = parts[1].split("~")
    if len(fields) < 40:
        return None

    # 腾讯字段映射（约 50+ 字段，基于常见行情接口）
    try:
        name = fields[1]
        raw_code = fields[2]
        price = float(fields[3]) if fields[3] else 0
        pre_close = float(fields[4]) if fields[4] else 0
        open_price = float(fields[5]) if fields[5] else 0
        volume = float(fields[6]) if fields[6] else 0       # 成交量（手）
        high = float(fields[33]) if fields[33] else 0
        low = float(fields[34]) if fields[34] else 0
        amount = float(fields[37]) if fields[37] else 0     # 成交额（万）
        turnover_rate = float(fields[38]) if fields[38] else 0
        pe = float(fields[39]) if fields[39] else 0
        change_pct = float(fields[32]) if fields[32] else 0
        total_market_cap = float(fields[45]) if len(fields) > 45 and fields[45] else 0
        volume_ratio = float(fields[47]) if len(fields) > 47 and fields[47] else 0

        change_amount = round(price - pre_close, 2)

        return {
            "code": _clean_stock_code(code),
            "name": name,
            "price": price,
            "change_pct": change_pct,
            "change_amount": change_amount,
            "volume_ratio": volume_ratio,
            "turnover_rate": turnover_rate,
            "volume": volume,
            "amount": amount,
            "high": high,
            "low": low,
            "open": open_price,
            "pre_close": pre_close,
            "pe": pe,
            "total_market_cap": total_market_cap,
        }
    except (ValueError, IndexError) as e:
        return None


def fetch_real_time_quote(code: str) -> dict:
    """
    获取实时行情快照（v2.0 — 单只查询，多源容灾）

    优先级：新浪 → 腾讯 → 东财个股信息补PE/市值
    彻底移除 stock_zh_a_spot_em() 全市场扫描。

    Returns:
        {"data": {...}, "success": True/False, "source": "..."}
    """
    cache_k = _cache_key("quote", code)
    cached = _cache_get(cache_k)
    if cached:
        return {"data": cached, "success": True, "source": "cache"}

    sources = [
        ("sina", _fetch_quote_sina),
        ("tencent", _fetch_quote_tencent),
    ]

    errors = []
    for src_name, src_fn in sources:
        try:
            data = src_fn(code)
            if data and data.get("price", 0) > 0:
                # 补充 PE / 市值（新浪不提供）
                if data.get("pe", 0) == 0 or data.get("total_market_cap", 0) == 0:
                    info = fetch_stock_info(code)
                    if info["success"]:
                        si = info["data"]
                        if data.get("pe", 0) == 0:
                            data["pe"] = float(si.get("市盈率-动态", 0) or 0)
                        if data.get("total_market_cap", 0) == 0:
                            data["total_market_cap"] = float(si.get("总市值", 0) or 0)

                _cache_set(cache_k, data)
                return {"data": data, "success": True, "source": f"direct:{src_name}"}
        except Exception as e:
            errors.append(f"{src_name}: {str(e)}")

    return {"error": f"实时行情: 所有数据源均失败 — {'; '.join(errors)}", "success": False}


# ══════════════════════════════════════════════════════════
# 日K线（多源：腾讯 → 新浪 akshare → baostock）
# ══════════════════════════════════════════════════════════

def _fetch_kline_tencent(code: str, days: int = 120) -> Optional[pd.DataFrame]:
    """
    腾讯财经历史日K线（前复权）
    API: http://web.ifzq.gtimg.cn/appstock/app/fqkline/get
    返回干净的 JSON，不需要 akshare 依赖
    """
    tc = _to_tencent_code(code)
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={tc},day,,,{days},qfq"
    headers = {"User-Agent": _random_ua()}
    resp = requests.get(url, headers=headers, timeout=15)
    data = resp.json()

    if data.get("code") != 0:
        return None

    stock_data = data.get("data", {}).get(tc, {})
    if not stock_data:
        return None

    # 优先取前复权数据
    kline_list = stock_data.get("qfqday") or stock_data.get("day")
    if not kline_list or len(kline_list) == 0:
        return None

    # 腾讯日K线格式: [date, open, close, high, low, volume]
    # 注意：与标准 OHLCV 不同！腾讯把 close 放在 high/low 前面
    rows = []
    for item in kline_list:
        try:
            rows.append({
                "date": pd.to_datetime(item[0]),
                "open": float(item[1]),
                "close": float(item[2]),
                "high": float(item[3]),
                "low": float(item[4]),
                "volume": float(item[5]),
            })
        except (ValueError, IndexError):
            continue

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values("date").tail(days).reset_index(drop=True)

    # 计算成交额（估算：成交量 * 收盘价的均价近似，实际从腾讯 qt 字段获取更准）
    # 这里用 close * volume 做近似（单位：手 → 需要换算）
    df["amount"] = df["close"] * df["volume"] * 100  # 近似成交额（元）

    # 换手率（腾讯日K线API不直接提供，设0后由特征计算自行处理）
    df["turnover"] = 0.0

    # 涨跌幅
    df["pct_change"] = df["close"].pct_change() * 100
    df["pct_change"] = df["pct_change"].fillna(0)

    return df


def _fetch_kline_sina_ak(code: str, days: int = 120) -> Optional[pd.DataFrame]:
    """
    新浪财经历史日K线（通过 akshare，新浪源不受 push2his 封禁影响）
    备选方案
    """
    raw_code = _clean_stock_code(code)
    start_date = (datetime.now() - timedelta(days=days + 30)).strftime("%Y%m%d")
    end_date = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_daily(
            symbol=f"sh{raw_code}" if raw_code.startswith("6") else f"sz{raw_code}",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
        )
        if df is None or df.empty:
            return None

        # 标准化列名（新浪返回中文列名）
        col_map = {
            "date": "date",
            "open": "open",
            "close": "close",
            "high": "high",
            "low": "low",
            "volume": "volume",
        }
        # 检测实际列名并映射
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if "日期" in str(col) or "date" in col_lower:
                df = df.rename(columns={col: "date"})
            elif "开盘" in str(col) or "open" in col_lower:
                df = df.rename(columns={col: "open"})
            elif "收盘" in str(col) or "close" in col_lower:
                df = df.rename(columns={col: "close"})
            elif "最高" in str(col) or "high" in col_lower:
                df = df.rename(columns={col: "high"})
            elif "最低" in str(col) or "low" in col_lower:
                df = df.rename(columns={col: "low"})
            elif "成交" in str(col) and "量" in str(col) or "volume" in col_lower:
                df = df.rename(columns={col: "volume"})
            elif "成交" in str(col) and "额" in str(col) or "amount" in col_lower:
                df = df.rename(columns={col: "amount"})
            elif "换手" in str(col) or "turnover" in col_lower:
                df = df.rename(columns={col: "turnover"})
            elif "涨跌" in str(col) or "pct" in col_lower:
                df = df.rename(columns={col: "pct_change"})

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").tail(days).reset_index(drop=True)

        # 确保必要列存在
        for col in ["open", "close", "high", "low", "volume"]:
            if col not in df.columns:
                return None

        if "amount" not in df.columns:
            df["amount"] = df["close"] * df["volume"] * 100
        if "turnover" not in df.columns:
            df["turnover"] = 0.0
        if "pct_change" not in df.columns:
            df["pct_change"] = df["close"].pct_change() * 100
            df["pct_change"] = df["pct_change"].fillna(0)

        return df
    except Exception:
        return None


def fetch_daily_kline(code: str, days: int = 120) -> dict:
    """
    获取日K线数据（v2.0 — 多源容灾）

    优先级：腾讯直接API → 新浪 akshare
    彻底移除对 push2his.eastmoney.com 的依赖。

    Returns:
        {"data": DataFrame, "success": True/False, "source": "..."}
    """
    cache_k = _cache_key("kline", code)
    cached = _cache_get(cache_k)
    if cached is not None:
        return {"data": cached, "success": True, "source": "cache"}

    sources = [
        ("tencent", _fetch_kline_tencent),
        ("sina_akshare", _fetch_kline_sina_ak),
    ]

    errors = []
    for src_name, src_fn in sources:
        try:
            df = src_fn(code, days)
            if df is not None and not df.empty and len(df) >= min(10, days // 3):
                # 确保数值类型
                for col in ["open", "close", "high", "low", "volume", "amount", "turnover", "pct_change"]:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors="coerce")

                _cache_set(cache_k, df.copy())
                return {"data": df, "success": True, "source": f"direct:{src_name}"}
        except Exception as e:
            errors.append(f"{src_name}: {str(e)}")

    return {"error": f"日K线: 所有数据源均失败 — {'; '.join(errors)}", "success": False}


# ══════════════════════════════════════════════════════════
# 分钟K线（多源）
# ══════════════════════════════════════════════════════════

def _fetch_minute_kline_tencent(code: str, period: str = "60") -> Optional[pd.DataFrame]:
    """
    腾讯财经分钟K线
    API: http://ifzq.gtimg.cn/appstock/app/kline/mkline
    period: 1/5/15/30/60
    """
    tc = _to_tencent_code(code)
    # 腾讯分钟K线接口（ifzq 子域，与日K线不同）
    url = f"http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={tc},m{period},,120"
    headers = {"User-Agent": _random_ua()}
    resp = requests.get(url, headers=headers, timeout=15)

    if resp.status_code != 200:
        return None

    try:
        data = resp.json()
    except Exception:
        return None

    if data.get("code") != 0:
        return None

    stock_data = data.get("data", {}).get(tc, {})
    if not stock_data:
        return None

    kline_list = stock_data.get(f"m{period}") or stock_data.get("m5") or stock_data.get("m15")
    if not kline_list:
        return None

    rows = []
    for item in kline_list:
        try:
            # 腾讯分钟K线格式: [datetime, open, close, high, low, volume, ...]
            rows.append({
                "datetime": pd.to_datetime(item[0]),
                "open": float(item[1]),
                "close": float(item[2]),
                "high": float(item[3]),
                "low": float(item[4]),
                "volume": float(item[5]) if len(item) > 5 else 0,
            })
        except (ValueError, IndexError):
            continue

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values("datetime").reset_index(drop=True)
    return df


def fetch_minute_kline(code: str, period: str = "5") -> dict:
    """
    获取分钟K线数据（v2.0 — 腾讯优先）
    period: "1"/"5"/"15"/"30"/"60"
    """
    cache_k = _cache_key(f"minute{period}", code)
    cached = _cache_get(cache_k)
    if cached is not None:
        return {"data": cached, "success": True, "source": "cache"}

    # 尝试腾讯分钟K线
    try:
        df = _fetch_minute_kline_tencent(code, period)
        if df is not None and not df.empty:
            _cache_set(cache_k, df.copy())
            return {"data": df, "success": True, "source": "direct:tencent:minute"}
    except Exception:
        pass

    # 兜底：尝试 akshare（可能走东财，大概率失败但不妨一试）
    result = _safe_fetch(
        ak.stock_zh_a_hist,
        "分钟K线",
        symbol=_clean_stock_code(code),
        period=period,
        adjust="qfq",
    )
    if result["success"]:
        df = result["data"]
        col_map = {
            "日期": "datetime", "开盘": "open", "收盘": "close",
            "最高": "high", "最低": "low", "成交量": "volume",
        }
        df = df.rename(columns=col_map)
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime").reset_index(drop=True)
        _cache_set(cache_k, df.copy())
        return {"data": df, "success": True, "source": "akshare:fallback"}

    return {"error": "分钟K线: 所有数据源均失败", "success": False}


# ══════════════════════════════════════════════════════════
# 资金流向（东财单只查询 + 指数退避重试）
# ══════════════════════════════════════════════════════════

def fetch_fund_flow(code: str, days: int = 30) -> dict:
    """
    获取个股资金流向（v2.0 — 单只查询，指数退避重试）

    东财是 A 股免费个股资金流向的唯一数据源。
    单只查询不会触发封控，加入指数退避重试增加成功率。

    Returns:
        {"data": DataFrame, "success": True/False, "source": "..."}
    """
    cache_k = _cache_key("fundflow", code)
    cached = _cache_get(cache_k)
    if cached is not None:
        return {"data": cached, "success": True, "source": "cache"}

    raw_code = _clean_stock_code(code)
    market = "sh" if raw_code.startswith("6") else "sz"

    # 指数退避重试
    last_error = None
    for attempt in range(3):
        try:
            _rate_limit()
            df = ak.stock_individual_fund_flow(
                stock=raw_code,
                market=market,
            )
            if df is not None and not df.empty:
                date_col = df.columns[0]
                df = df.rename(columns={date_col: "date"})
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date").tail(days).reset_index(drop=True)
                _cache_set(cache_k, df.copy())
                return {"data": df, "success": True, "source": "akshare:stock_individual_fund_flow"}

            last_error = "返回空数据"
        except Exception as e:
            last_error = str(e)
            if attempt < 2:
                wait = 2 ** attempt + random.uniform(0.5, 1.5)
                time.sleep(wait)

    return {"error": f"资金流向: {last_error}", "success": False}


# ══════════════════════════════════════════════════════════
# 股票基本信息
# ══════════════════════════════════════════════════════════

def fetch_stock_info(code: str) -> dict:
    """
    获取股票基本信息（v2.0 — 多源容灾）

    优先级：东财个股信息 → 腾讯实时行情提取
    """
    raw_code = _clean_stock_code(code)
    cache_k = _cache_key("info", code)
    cached = _cache_get(cache_k)
    if cached:
        return {"data": cached, "success": True, "source": "cache"}

    # 方案1: 东财个股信息接口
    try:
        _rate_limit()
        df = ak.stock_individual_info_em(symbol=raw_code)
        info = {}
        for _, row in df.iterrows():
            info[row["item"]] = row["value"]
        _cache_set(cache_k, info)
        return {"data": info, "success": True, "source": "akshare:stock_individual_info_em"}
    except Exception:
        pass

    # 方案2: 从腾讯实时行情提取基本信息
    try:
        quote = _fetch_quote_tencent(code)
        if quote and quote.get("name"):
            info = {
                "股票简称": quote["name"],
                "最新价": quote.get("price", 0),
                "市盈率-动态": quote.get("pe", 0),
                "总市值": quote.get("total_market_cap", 0),
            }
            _cache_set(cache_k, info)
            return {"data": info, "success": True, "source": "tencent:quote_extract"}
    except Exception:
        pass

    # 方案3: 从新浪实时行情提取
    try:
        quote = _fetch_quote_sina(code)
        if quote and quote.get("name"):
            info = {
                "股票简称": quote["name"],
                "最新价": quote.get("price", 0),
                "市盈率-动态": 0,
                "总市值": 0,
            }
            _cache_set(cache_k, info)
            return {"data": info, "success": True, "source": "sina:quote_extract"}
    except Exception:
        pass

    return {"error": "股票信息: 所有数据源均失败", "success": False}


# ══════════════════════════════════════════════════════════
# 数据源健康检查
# ══════════════════════════════════════════════════════════

def check_data_source_health() -> dict:
    """
    数据源健康检查。
    在启动时或定期调用，了解各数据源的可用状态。

    Returns:
        {
            "tencent_kline": True/False,
            "tencent_quote": True/False,
            "sina_quote": True/False,
            "sina_kline_ak": True/False,
            "eastmoney_fundflow": True/False,
            "eastmoney_info": True/False,
            "checked_at": "..."
        }
    """
    test_code = "600519"  # 贵州茅台，交易时段有数据
    results = {}

    # 腾讯日K线
    try:
        r = _fetch_kline_tencent(test_code, 5)
        results["tencent_kline"] = r is not None and not r.empty
    except Exception:
        results["tencent_kline"] = False

    # 腾讯实时行情
    try:
        r = _fetch_quote_tencent(test_code)
        results["tencent_quote"] = r is not None and r.get("price", 0) > 0
    except Exception:
        results["tencent_quote"] = False

    # 新浪实时行情
    try:
        r = _fetch_quote_sina(test_code)
        results["sina_quote"] = r is not None and r.get("price", 0) > 0
    except Exception:
        results["sina_quote"] = False

    # 新浪日K线（akshare）
    try:
        r = _fetch_kline_sina_ak(test_code, 5)
        results["sina_kline_ak"] = r is not None and not r.empty
    except Exception:
        results["sina_kline_ak"] = False

    # 东财资金流向
    try:
        r = fetch_fund_flow(test_code, 5)
        results["eastmoney_fundflow"] = r["success"]
    except Exception:
        results["eastmoney_fundflow"] = False

    # 东财个股信息
    try:
        r = fetch_stock_info(test_code)
        results["eastmoney_info"] = r["success"]
    except Exception:
        results["eastmoney_info"] = False

    results["checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return results


# ══════════════════════════════════════════════════════════
# 一站式获取（保持不变）
# ══════════════════════════════════════════════════════════

def fetch_all(code: str, days: int = 120, include_intraday: bool = True) -> dict:
    """
    一站式获取全部数据

    Args:
        code: 股票代码，如 600519
        days: 日线回溯天数
        include_intraday: 是否包含分钟数据

    Returns:
        {
            "success": True/False,
            "code": "600519",
            "name": "贵州茅台",
            "daily_kline": DataFrame,
            "minute_60": DataFrame (optional),
            "fund_flow": DataFrame,
            "realtime": dict,
            "stock_info": dict,
            "fetched_at": "2024-01-01 12:00:00",
            "errors": [...]
        }
    """
    code = _clean_stock_code(code)
    errors = []

    # 获取数据（各函数内部已包含重试和速率控制）
    kline = fetch_daily_kline(code, days)
    if not kline["success"]:
        errors.append(kline.get("error", "日K线获取失败"))

    fund = fetch_fund_flow(code, days=30)
    if not fund["success"]:
        errors.append(fund.get("error", "资金流向获取失败"))

    realtime = fetch_real_time_quote(code)
    if not realtime["success"]:
        errors.append(realtime.get("error", "实时行情获取失败"))

    info = fetch_stock_info(code)
    stock_name = ""
    if info["success"]:
        stock_name = info["data"].get("股票简称", "")

    result = {
        "success": kline["success"],
        "code": code,
        "name": stock_name or realtime.get("data", {}).get("name", ""),
        "daily_kline": kline.get("data") if kline["success"] else None,
        "fund_flow": fund.get("data") if fund["success"] else None,
        "realtime": realtime.get("data") if realtime["success"] else None,
        "stock_info": info.get("data") if info["success"] else None,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "errors": errors if errors else None,
    }

    # 分钟线（可选的，较大数据量）
    if include_intraday and kline["success"]:
        m60 = fetch_minute_kline(code, "60")
        if m60["success"]:
            result["minute_60"] = m60["data"]
        else:
            errors.append(m60.get("error", "60分钟线获取失败"))

    return result


# ══════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fetch_data.py <股票代码> [回溯天数] [--json] [--health]")
        print("示例: python fetch_data.py 600519 120 --json")
        print("      python fetch_data.py --health")
        sys.exit(1)

    if "--health" in sys.argv:
        print("🔍 数据源健康检查中...\n")
        health = check_data_source_health()
        for k, v in health.items():
            if k == "checked_at":
                print(f"\n⏱️ 检查时间: {v}")
            else:
                icon = "✅" if v else "❌"
                print(f"  {icon} {k}: {'可用' if v else '不可用'}")
        sys.exit(0)

    code = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    as_json = "--json" in sys.argv

    data = fetch_all(code, days)

    if as_json:
        output = {k: v for k, v in data.items() if k not in ("daily_kline", "minute_60", "fund_flow")}
        if data.get("daily_kline") is not None:
            output["daily_kline"] = data["daily_kline"].to_dict("records")
        if data.get("minute_60") is not None:
            output["minute_60"] = data["minute_60"].to_dict("records")[-240:]
        if data.get("fund_flow") is not None:
            output["fund_flow"] = data["fund_flow"].to_dict("records")
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"✅ 股票: {data['name']}({data['code']})")
        print(f"📅 获取时间: {data['fetched_at']}")
        if data.get("daily_kline") is not None:
            print(f"📊 日K线: {len(data['daily_kline'])} 条")
        if data.get("minute_60") is not None:
            print(f"⏱️ 60分钟线: {len(data['minute_60'])} 条")
        if data.get("fund_flow") is not None:
            print(f"💰 资金流向: {len(data['fund_flow'])} 条")
        if data.get("errors"):
            for e in data["errors"]:
                print(f"⚠️ {e}")
        if data.get("daily_kline") is not None:
            print("\n📈 最近5日K线:")
            print(data["daily_kline"][["date", "open", "close", "high", "low", "volume", "turnover"]].tail(5).to_string(index=False))
