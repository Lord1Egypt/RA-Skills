"""
scanner.py — A股全市场数据扫描器
作者：Jarvis | 2026-03-07 | 基于 akshare 高效批处理
功能：一次性获取 ~5000 只 A 股的实时/收盘数据
"""

import pandas as pd
import numpy as np
import time
from typing import List, Dict
try:
    import akshare as ak
except ImportError:
    raise RuntimeError("akshare not installed. Run: pip install akshare")

def scan_all_a_shares() -> pd.DataFrame:
    """
    扫描全部 A 股（含科创板、创业板）
    返回列：symbol, name, close, volume, market_cap, industry, is_st
    """
    print("[scanner] Fetching stock list...")
    # 获取所有A股代码（排除B股、ETF等）
    stock_list = ak.stock_zh_a_spot_em()
    # 仅保留普通A股（剔除指数、基金等）
    stock_list = stock_list[stock_list['代码'].str.match(r'^[036]\d{5}$')].copy()
    
    # 提取关键字段
    df = pd.DataFrame()
    df['symbol'] = stock_list['代码'].apply(lambda x: x + ('.SH' if x.startswith('6') else '.SZ'))
    df['name'] = stock_list['名称']
    df['close'] = stock_list['最新价']
    df['volume'] = stock_list['成交量'] * 100  # akshare 单位是手 → 转为股
    df['market_cap'] = stock_list['总市值'] * 1e4  # 万元 → 元
    df['industry'] = stock_list['所属行业']
    df['is_st'] = stock_list['名称'].str.contains(r'(ST|*ST)', na=False)
    
    # 补充流通市值（若缺失，用总市值近似）
    if '流通市值' in stock_list.columns:
        df['float_market_cap'] = stock_list['流通市值'] * 1e4
    else:
        df['float_market_cap'] = df['market_cap']
    
    print(f"[scanner] Fetched {len(df)} stocks.")
    return df.reset_index(drop=True)

def get_daily_kline(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """获取单只股票日线（用于后续因子计算）"""
    try:
        code = symbol[:6]
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date.replace('-', ''),
            end_date=end_date.replace('-', ''),
            adjust="qfq"
        )
        df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'change', 'turnover']
        df['date'] = pd.to_datetime(df['date'])
        return df.set_index('date').sort_index()
    except Exception as e:
        print(f"[kline failed] {symbol}: {e}")
        return pd.DataFrame()

# 快速测试
if __name__ == "__main__":
    data = scan_all_a_shares()
    print(data.head())
    # 示例：筛选非ST、流通市值>50亿
    mask = (~data['is_st']) & (data['float_market_cap'] > 50e8)
    print(f"Qualified stocks: {mask.sum()}")