#!/usr/bin/env python3
"""
股票/指数历史K线数据获取
支持AKShare和新浪财经API，自动切换
默认使用前复权数据
"""

import json
import urllib.request
from typing import List, Dict, Optional


def get_stock_history(code: str, days: int = 500, adjust: str = "qfq") -> List[Dict]:
    """
    获取股票历史K线数据 (自动切换数据源)
    
    Args:
        code: 股票代码，如 "600519.SH"
        days: 获取天数，默认500天
        adjust: 复权类型
            "qfq" - 前复权 (默认，推荐用于计算涨幅)
            "hfq" - 后复权
            ""    - 不复权
    
    Returns:
        K线数据列表，每项包含 day, open, high, low, close, volume
    """
    # 优先尝试AKShare (支持复权)
    try:
        data = _get_stock_history_akshare(code, days, adjust)
        if data:
            return data
    except Exception as e:
        print(f"AKShare failed: {e}")
    
    # 降级到新浪API (未复权)
    print("WARNING: Falling back to Sina API (unadjusted - may have ex-dividend gaps)")
    print("建议安装AKShare: pip install akshare pandas")
    try:
        return _get_stock_history_sina(code, days)
    except Exception as e:
        print(f"Sina API failed: {e}")
        return []


def _get_stock_history_akshare(code: str, days: int, adjust: str) -> List[Dict]:
    """AKShare获取 (支持复权)"""
    import akshare as ak
    
    # 转换代码格式: 600519.SH -> 600519
    symbol = code.replace(".SH", "").replace(".SZ", "")
    
    # 计算日期范围
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days * 1.5)).strftime("%Y%m%d")
    
    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )
    
    # 转换为标准格式
    result = []
    for _, row in df.iterrows():
        date_val = row["日期"]
        if hasattr(date_val, 'strftime'):
            day = date_val.strftime("%Y-%m-%d")
        else:
            day = str(date_val)[:10]
        
        result.append({
            "day": day,
            "open": float(row["开盘"]),
            "high": float(row["最高"]),
            "low": float(row["最低"]),
            "close": float(row["收盘"]),
            "volume": float(row["成交量"]),
        })
    
    return result[-days:] if result else result


def _get_stock_history_sina(code: str, days: int = 500) -> List[Dict]:
    """新浪财经API获取 (未复权)"""
    if code.endswith('.SH'):
        symbol = 'sh' + code.replace('.SH', '')
    elif code.endswith('.SZ'):
        symbol = 'sz' + code.replace('.SZ', '')
    else:
        symbol = code
    
    url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=240&ma=5&datalen={days}"
    
    # 添加Headers避免403
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, timeout=15)
    data = response.read().decode('gb2312')
    return json.loads(data)


def get_today_change(code: str) -> Optional[Dict]:
    """
    获取股票当天涨跌幅
    
    Args:
        code: 股票代码
    
    Returns:
        当日涨跌幅信息
    """
    # 优先尝试AKShare
    try:
        result = _get_today_change_akshare(code)
        if result:
            return result
    except Exception as e:
        print(f"AKShare realtime failed: {e}")
    
    # 降级到新浪
    return _get_today_change_sina(code)


def _get_today_change_akshare(code: str) -> Optional[Dict]:
    """AKShare实时行情"""
    import akshare as ak
    
    symbol = code.replace(".SH", "").replace(".SZ", "")
    
    # 尝试获取实时数据
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                            start_date="20260301", end_date="20260316",
                            adjust="qfq")
    
    if not df.empty:
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        change_pct = float(latest['涨跌幅'])
        change = float(latest['涨跌额']) if '涨跌额' in latest else 0
        
        return {
            "name": symbol,
            "open": float(latest['开盘']),
            "close": float(latest['收盘']),
            "high": float(latest['最高']),
            "low": float(latest['最低']),
            "volume": float(latest['成交量']),
            "change_pct": round(change_pct, 2),
            "change": round(change, 2) if change else round(float(latest['收盘']) - float(prev['收盘']), 2),
        }
    return None


def _get_today_change_sina(code: str) -> Optional[Dict]:
    """新浪实时行情"""
    if code.endswith('.SH'):
        symbol = 'sh' + code.replace('.SH', '')
    elif code.endswith('.SZ'):
        symbol = 'sz' + code.replace('.SZ', '')
    else:
        symbol = code
    
    url = f"https://hq.sinajs.cn/list={symbol}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode('gb2312')
        
        if '=' in data:
            parts = data.split('=')[1].strip('";\n').split(',')
            if len(parts) >= 6:
                open_price = float(parts[1]) if parts[1] else 0
                close_price = float(parts[2]) if parts[2] else 0
                
                change = close_price - open_price
                change_pct = (change / open_price * 100) if open_price else 0
                
                return {
                    "name": parts[0],
                    "open": open_price,
                    "close": close_price,
                    "high": float(parts[3]) if parts[3] else 0,
                    "low": float(parts[4]) if parts[4] else 0,
                    "volume": float(parts[5]) if parts[5] else 0,
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                }
    except Exception as e:
        print(f"Sina realtime error: {e}")
    
    return None


def get_index_history(code: str, days: int = 500) -> List[Dict]:
    """获取指数历史K线"""
    # 优先尝试AKShare
    try:
        data = _get_index_history_akshare(code, days)
        if data:
            return data
    except Exception as e:
        print(f"AKShare index failed: {e}")
    
    # 降级到新浪
    return _get_index_history_sina(code, days)


def _get_index_history_akshare(code: str, days: int) -> List[Dict]:
    """AKShare指数数据"""
    import akshare as ak
    from datetime import datetime, timedelta
    
    # 转换: 000001.SH -> 000001
    symbol = code.replace(".SH", "").replace(".SZ", "")
    
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days * 1.5)).strftime("%Y%m%d")
    
    df = ak.index_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date
    )
    
    result = []
    for _, row in df.iterrows():
        date_val = row["日期"]
        if hasattr(date_val, 'strftime'):
            day = date_val.strftime("%Y-%m-%d")
        else:
            day = str(date_val)[:10]
        
        result.append({
            "day": day,
            "open": float(row["开盘"]),
            "high": float(row["最高"]),
            "low": float(row["最低"]),
            "close": float(row["收盘"]),
            "volume": float(row["成交量"]),
        })
    
    return result[-days:]


def _get_index_history_sina(code: str, days: int = 500) -> List[Dict]:
    """新浪指数数据"""
    if code == "000001.SH" or code == "sh000001":
        symbol = "sh000001"
    elif code == "399001.SZ" or code == "sz399001":
        symbol = "sz399001"
    elif code == "399006.SZ":
        symbol = "sz399006"
    elif code == "000300.SH":
        symbol = "sh000300"
    else:
        symbol = code
    
    url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=240&ma=5&datalen={days}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        data = response.read().decode('gb2312')
        return json.loads(data)
    except Exception as e:
        print(f"Error fetching index {code}: {e}")
        return []


def calc_change_rate(old_price: float, new_price: float) -> Optional[float]:
    """计算涨跌幅百分比"""
    if old_price and new_price and old_price != 0:
        return round((new_price - old_price) / old_price * 100, 2)
    return None


def build_price_map(kline_data: List[Dict]) -> Dict[str, float]:
    """构建日期到收盘价的映射"""
    return {item['day']: float(item['close']) for item in kline_data if 'day' in item and 'close' in item}


def get_accurate_change(code: str, target_date: str, prev_date: str, adjust: str = "qfq") -> Optional[Dict]:
    """
    获取准确的涨跌幅 (使用复权数据)
    
    Args:
        code: 股票代码
        target_date: 目标日期，如 "2026-03-13"
        prev_date: 前一交易日，如 "2026-03-12"
        adjust: 复权类型 "qfq"(前复权) 或 "hfq"(后复权)
    
    Returns:
        {
            "target_price": float,
            "prev_price": float,
            "change_pct": float,
        }
    """
    kline = get_stock_history(code, days=100, adjust=adjust)
    price_map = build_price_map(kline)
    
    target_price = price_map.get(target_date)
    prev_price = price_map.get(prev_date)
    
    if target_price and prev_price:
        return {
            "target_price": target_price,
            "prev_price": prev_price,
            "change_pct": calc_change_rate(prev_price, target_price),
        }
    return None


if __name__ == "__main__":
    print("=== 测试获取股票数据 (自动复权) ===")
    try:
        data = get_stock_history("600519.SH", 5)
        for item in data:
            print(item)
    except Exception as e:
        print(f"需要安装AKShare: {e}")
    
    print("\n=== 测试当天涨跌幅 ===")
    result = get_today_change("600519.SH")
    if result:
        print(f"贵州茅台: 开盘={result['open']}, 当前={result['close']}, 涨跌幅={result['change_pct']}%")
