"""金融分析工具包 - 快速分析脚本"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_stock_basic(code: str) -> dict:
    """获取个股基本信息"""
    try:
        # Get stock info
        df = ak.stock_individual_info_em(symbol=code)
        info = dict(zip(df['item'], df['value']))
        return info
    except Exception as e:
        return {"error": str(e)}

def get_stock_price(code: str, days: int = 60) -> pd.DataFrame:
    """获取个股日 K 线"""
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        return df.tail(days)
    except Exception as e:
        return pd.DataFrame()

def get_stock_financials(code: str) -> dict:
    """获取个股财务数据"""
    try:
        df = ak.stock_yjbb_em(date="20251231")  # 最新年报
        row = df[df['代码'] == code]
        if not row.empty:
            return row.iloc[0].to_dict()
        return {"error": "未找到财务数据"}
    except Exception as e:
        return {"error": str(e)}

def get_index_price(symbol: str) -> pd.DataFrame:
    """获取指数行情"""
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        return df.tail(30)
    except Exception as e:
        return pd.DataFrame()

def get_market_overview() -> dict:
    """获取市场概览"""
    result = {}
    try:
        # 涨跌家数
        df = ak.stock_zh_a_spot_em()
        result['total'] = len(df)
        result['up'] = len(df[df['涨跌幅'] > 0])
        result['down'] = len(df[df['涨跌幅'] < 0])
        result['limit_up'] = len(df[df['涨跌幅'] >= 9.9])
        result['limit_down'] = len(df[df['涨跌幅'] <= -9.9])
        result['total_volume'] = df['成交额'].sum() / 1e8  # 亿
    except Exception as e:
        result['error'] = str(e)
    return result

def quick_analyze(code: str):
    """快速分析个股"""
    print(f"=== {code} 快速分析 ===\n")
    
    # 基本信息
    info = get_stock_basic(code)
    print("基本信息:")
    for k, v in info.items():
        if k != 'error':
            print(f"  {k}: {v}")
    
    # 近期行情
    price = get_stock_price(code)
    if not price.empty:
        print(f"\n近期行情 (最近 {len(price)} 个交易日):")
        latest = price.iloc[-1]
        prev = price.iloc[-2]
        change = (latest['收盘'] - prev['收盘']) / prev['收盘'] * 100
        print(f"  最新收盘: {latest['收盘']} ({change:+.2f}%)")
        print(f"  5 日均量: {price['成交量'].tail(5).mean():.0f}")
        
        # 简单均线
        ma5 = price['收盘'].tail(5).mean()
        ma20 = price['收盘'].tail(20).mean()
        print(f"  MA5: {ma5:.2f}, MA20: {ma20:.2f}")
        print(f"  价格 vs MA5: {'上方' if latest['收盘'] > ma5 else '下方'}")
        print(f"  价格 vs MA20: {'上方' if latest['收盘'] > ma20 else '下方'}")
    
    # 财务数据
    fin = get_stock_financials(code)
    if 'error' not in fin:
        print("\n财务数据 (最新年报):")
        for key in ['净资产收益率', '销售净利率', '营业总收入', '净利润', '每股收益']:
            if key in fin:
                print(f"  {key}: {fin[key]}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        code = "600519"  # 贵州茅台
    quick_analyze(code)
