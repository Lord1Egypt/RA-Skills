"""A股/ETF数据获取工具 - 基于akshare（免费无需token）

用法:
    from scripts.fetch_data import fetch_etf_daily, fetch_stock_daily
    df = fetch_etf_daily("159915", "20250101", "20260301")
"""

import akshare as ak
import pandas as pd


def fetch_etf_daily(code: str, start: str = "", end: str = "") -> pd.DataFrame:
    """获取ETF日线数据。

    Args:
        code: ETF代码，如 "159915"
        start: 起始日期 "YYYYMMDD"，默认最近一年
        end: 结束日期 "YYYYMMDD"
    Returns:
        DataFrame with columns: date, open, high, low, close, volume, amount
    """
    df = ak.fund_etf_hist_sina(symbol=code)
    df = df.rename(columns={
        "date": "date", "open": "open", "high": "high",
        "low": "low", "close": "close", "volume": "volume"
    })
    df["date"] = pd.to_datetime(df["date"])
    if start:
        df = df[df["date"] >= pd.to_datetime(start)]
    if end:
        df = df[df["date"] <= pd.to_datetime(end)]
    df = df.reset_index(drop=True)
    # 标准化列名小写
    df.columns = [c.lower() for c in df.columns]
    return df


def fetch_stock_daily(code: str, start: str = "", end: str = "") -> pd.DataFrame:
    """获取A股个股日线数据。

    Args:
        code: 股票代码，如 "000001"（平安银行）
        start: 起始日期 "YYYYMMDD"
        end: 结束日期 "YYYYMMDD"
    Returns:
        DataFrame with columns: date, open, high, low, close, volume, amount
    """
    df = ak.stock_zh_a_hist(
        symbol=code, period="daily",
        start_date=start or "20240101", end_date=end or "20991231",
        adjust="qfq"
    )
    df = df.rename(columns={
        "日期": "date", "开盘": "open", "最高": "high",
        "最低": "low", "收盘": "close", "成交量": "volume", "成交额": "amount"
    })
    df["date"] = pd.to_datetime(df["date"])
    df = df[["date", "open", "high", "low", "close", "volume", "amount"]].reset_index(drop=True)
    return df


def fetch_etf_intraday(code: str) -> pd.DataFrame:
    """获取ETF分时数据（日内做T用）。

    Args:
        code: ETF代码
    Returns:
        DataFrame with columns: time, price, volume, avg_price
    """
    df = ak.fund_etf_hist_sina(symbol=code)
    # 分时数据通过实时接口获取
    df_rt = ak.fund_etf_spot_em()
    row = df_rt[df_rt["代码"] == code]
    if row.empty:
        return pd.DataFrame()
    info = row.iloc[0]
    return pd.DataFrame([{
        "time": pd.Timestamp.now(),
        "price": float(info.get("最新价", 0)),
        "volume": float(info.get("成交量", 0)),
        "avg_price": float(info.get("均价", 0)),
    }])


def fetch_realtime(code: str) -> pd.DataFrame:
    """获取实时行情快照。

    Args:
        code: 证券代码
    Returns:
        DataFrame with current quote info
    """
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == code]
        if row.empty:
            return pd.DataFrame()
        return row.reset_index(drop=True)
    except Exception:
        # 尝试ETF实时
        df = ak.fund_etf_spot_em()
        row = df[df["代码"] == code]
        if row.empty:
            return pd.DataFrame()
        return row.reset_index(drop=True)


def fetch_etf_list() -> pd.DataFrame:
    """获取全部ETF列表。

    Returns:
        DataFrame: code, name, ...
    """
    df = ak.fund_etf_spot_em()
    df = df[["代码", "名称"]].rename(columns={"代码": "code", "名称": "name"})
    return df.reset_index(drop=True)


def search_etf(keyword: str) -> pd.DataFrame:
    """按关键词搜索ETF。

    Args:
        keyword: 搜索词，如 "创业板" "纳斯达克"
    Returns:
        匹配的ETF列表
    """
    df = fetch_etf_list()
    return df[df["name"].str.contains(keyword, na=False)].reset_index(drop=True)


# --- CLI入口 ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python fetch_data.py <代码> [start] [end]")
        print("示例: python fetch_data.py 159915 20250101 20260301")
        sys.exit(1)

    code = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else ""
    end = sys.argv[3] if len(sys.argv) > 3 else ""

    # 判断ETF还是股票（6位数字）
    if code.startswith("1") or code.startswith("5"):
        df = fetch_etf_daily(code, start, end)
        print(f"ETF {code} 日线数据: {len(df)} 条")
    else:
        df = fetch_stock_daily(code, start, end)
        print(f"股票 {code} 日线数据: {len(df)} 条")

    if not df.empty:
        print(df.tail(5).to_string(index=False))
