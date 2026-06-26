"""
AKShare Helper Script: Get Market Overview

Get real-time market overview including top gainers, losers, and market statistics.

Usage:
    python get_market_overview.py
"""

import akshare as ak

def get_market_overview():
    """Get A-share market overview"""
    print("Fetching A-share market data...")
    
    # Get all A-shares
    df = ak.stock_zh_a_spot_em()
    
    print(f"\n=== Market Overview ===")
    print(f"Total stocks: {len(df)}")
    print(f"Up: {len(df[df['涨跌幅'] > 0])}")
    print(f"Down: {len(df[df['涨跌幅'] < 0])}")
    print(f"Flat: {len(df[df['涨跌幅'] == 0])}")
    
    # Limit up/down
    limit_up = len(df[df['涨跌幅'] >= 9.9])
    limit_down = len(df[df['涨跌幅'] <= -9.9])
    print(f"Limit up: {limit_up}")
    print(f"Limit down: {limit_down}")
    
    # Top gainers
    print(f"\n=== Top 10 Gainers ===")
    top_gainers = df.nlargest(10, '涨跌幅')
    print(top_gainers[['代码', '名称', '最新价', '涨跌幅', '成交额']])
    
    # Top losers
    print(f"\n=== Top 10 Losers ===")
    top_losers = df.nsmallest(10, '涨跌幅')
    print(top_losers[['代码', '名称', '最新价', '涨跌幅', '成交额']])
    
    # Save to CSV
    df.to_csv('market_overview.csv', index=False, encoding='utf-8-sig')
    print(f"\nFull data saved to: market_overview.csv")
    
    return df

if __name__ == "__main__":
    get_market_overview()
