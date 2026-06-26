"""
AKShare Helper Script: Get Stock Historical Data

Usage:
    python get_stock_history.py <stock_code> [start_date] [end_date] [adjust]

Examples:
    python get_stock_history.py 000001
    python get_stock_history.py 000001 20200101 20231231
    python get_stock_history.py 000001 20200101 20231231 qfq
"""

import sys
import akshare as ak
from datetime import datetime, timedelta

def get_stock_history(symbol, start_date=None, end_date=None, adjust="qfq"):
    """
    Get stock historical K-line data
    
    Args:
        symbol: Stock code (6 digits, e.g., "000001")
        start_date: Start date (YYYYMMDD format)
        end_date: End date (YYYYMMDD format)
        adjust: Adjustment type ("qfq"=forward, "hfq"=backward, ""=none)
    """
    # Default to last year if dates not provided
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    
    print(f"Fetching {symbol} from {start_date} to {end_date} (adjust={adjust})...")
    
    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )
    
    print(f"\nData shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nLast 5 rows:")
    print(df.tail())
    
    # Save to CSV
    output_file = f"{symbol}_{start_date}_{end_date}.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved to: {output_file}")
    
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    symbol = sys.argv[1]
    start_date = sys.argv[2] if len(sys.argv) > 2 else None
    end_date = sys.argv[3] if len(sys.argv) > 3 else None
    adjust = sys.argv[4] if len(sys.argv) > 4 else "qfq"
    
    get_stock_history(symbol, start_date, end_date, adjust)
