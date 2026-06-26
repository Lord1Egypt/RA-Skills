#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""金融行情数据获取模板"""
import sys
sys.path.insert(0, 'skills/financial-market-data/python')


def get_daily_k(symbol, count=100):
    """获取日K线（TickFlow免费版）

    Args:
        symbol: 股票代码，如 "600519.SH", "00700.HK", "AAPL.US"
        count: 获取条数

    Returns:
        DataFrame: trade_date, open, high, low, close, volume
    """
    from tickflow import TickFlow
    tf = TickFlow.free()
    df = tf.klines.get(symbol, period="1d", count=count, as_dataframe=True)
    return df


def get_minute_k_pytdx(code, market=0, count=100):
    """获取分钟K线（pytdx通达信接口）

    Args:
        code: 股票代码，如 "000001"（不带市场前缀）
        market: 0=上海 1=深圳
        count: 获取条数

    Returns:
        list: [{date, time, open, high, low, close, volume}, ...]
    """
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    if api.connect('218.75.126.9', 7709):
        # category=9=1分钟K, market=0/1=沪/深
        data = api.get_security_bars(9, market, code, 0, count)
        api.disconnect()
        return data
    return None


def get_realtime_eastmoney(symbols):
    """获取实时行情（东方财富MX API）

    Args:
        symbols: 逗号分隔的股票代码，如 "600519.SH,000001.SZ"

    Returns:
        list: [{name, code, close, pctChg, volume, ...}, ...]
    """
    import requests
    import json

    api_key = "mkt_HFeitkf4UQNDF8rpr6wZMVfweIxmPegsR1jJK0kF0_I"
    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"

    payload = {
        "toolQuery": json.dumps({
            "func": "get_quote_list_ts",
            "params": [symbols, 1]
        })
    }
    headers = {"Content-Type": "application/json", "apiKey": api_key}
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    return resp.json()


def get_daily_k_baostock(ts_code, start_date, end_date, frequency="d", adjustflag="3"):
    """获取日K线（BaoStock，支持全量历史+复权）

    Args:
        ts_code: 聚宽代码格式，如 "sz.000001", "sh.600519"
        start_date: YYYYMMDD
        end_date: YYYYMMDD
        frequency: d=日线 w=周线 m=月线
        adjustflag: 1=后复权 2=前复权 3=不复权

    Returns:
        list of dict
    """
    import baostock as bs

    bs.login()
    rs = bs.query_history_k_data_plus(
        ts_code,
        "date,code,open,high,low,close,volume,pctChg",
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        adjustflag=adjustflag
    )
    data_list = []
    while rs.next:
        data_list.append(rs.get_row_data())
    bs.logout()
    return data_list


def get_futures_daily_akshare(symbol, start_date, end_date):
    """获取期货日K线（AkShare）

    Args:
        symbol: 期货代码，如 "au2504"（黄金2504合约）
        start_date: YYYYMMDD
        end_date: YYYYMMDD

    Returns:
        DataFrame
    """
    import akshare as ak
    df = ak.futures_zh_daily(symbol=symbol, start_date=start_date, end_date=end_date)
    return df


def get_etf_hist_akshare(symbol):
    """获取ETF历史数据（AkShare）

    Args:
        symbol: 如 "sh510300"（沪深300ETF）

    Returns:
        DataFrame
    """
    import akshare as ak
    df = ak.fund_etf_hist_sina(symbol=symbol)
    return df


def get_sector_boards_akshare():
    """获取行业板块列表（AkShare）

    Returns:
        DataFrame: 板块名称、代码、涨跌幅等
    """
    import akshare as ak
    df = ak.stock_board_industry_name_em()
    return df


def get_financial_baostock(ts_code, year, quarter):
    """获取财务数据（BaoStock）

    Args:
        ts_code: 如 "sz.000001"
        year: 年份，如 2024
        quarter: 季度，如 4

    Returns:
        DataFrame: 盈利能力、成长能力等
    """
    import baostock as bs

    bs.login()

    # 盈利能力
    rs = bs.query_profit_data(code=ts_code, year=year, quarter=quarter)
    profit_df = rs.get_data()

    # 成长能力
    rs = bs.query_growth_data(code=ts_code, year=year, quarter=quarter)
    growth_df = rs.get_data()

    bs.logout()
    return profit_df, growth_df


if __name__ == "__main__":
    print("=== 金融行情数据接口测试 ===")

    # 1. 日K（TickFlow）
    print("\n[1] TickFlow 日K测试")
    try:
        df = get_daily_k("600519.SH", count=5)
        print(f"  茅台日K: {len(df)} 条")
        print(f"  最新: {df.iloc[-1]['trade_date']} 收盘 {df.iloc[-1]['close']}")
    except Exception as e:
        print(f"  FAIL: {e}")

    # 2. 实时行情（东方财富MX API）
    print("\n[2] 东方财富MX API 实时测试")
    try:
        data = get_realtime_eastmoney("600519.SH,000001.SZ")
        print(f"  获取: {len(data)} 只")
        for item in data[:2]:
            print(f"  {item.get('code')} {item.get('name')} {item.get('close')}")
    except Exception as e:
        print(f"  FAIL: {e}")

    # 3. BaoStock日K
    print("\n[3] BaoStock 日K测试")
    try:
        data = get_daily_k_baostock("sz.000001", "20260101", "20260404")
        print(f"  平安银行: {len(data)} 条")
        if data:
            print(f"  最新: {data[-1][0]} 收盘 {data[-1][4]}")
    except Exception as e:
        print(f"  FAIL: {e}")

    # 4. 期货日K
    print("\n[4] AkShare 期货日K测试")
    try:
        df = get_futures_daily_akshare("au2504", "20260301", "20260404")
        print(f"  黄金期货: {len(df)} 条")
        if not df.empty:
            print(f"  最新: {df.iloc[-1]['日期']} 收盘 {df.iloc[-1]['收盘']}")
    except Exception as e:
        print(f"  FAIL: {e}")

    # 5. 行业板块
    print("\n[5] AkShare 行业板块测试")
    try:
        df = get_sector_boards_akshare()
        print(f"  行业板块: {len(df)} 个")
        print(df.head(3))
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n=== 测试完成 ===")
