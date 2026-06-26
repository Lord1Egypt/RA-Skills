#!/usr/bin/env python3
"""
Fetch historical time series data for financial indicators.
Supports: FRED (US macro), Yahoo Finance (commodities/indices), Tushare (A-shares)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Try imports with fallbacks
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
    # Set token from environment
    ts.set_token(os.environ.get('TUSHARE_TOKEN', ''))
except ImportError:
    TUSHARE_AVAILABLE = False

# Indicator mapping: indicator_id -> data source config
INDICATOR_MAPPING = {
    # Commodities (Yahoo Finance)
    'brent_crude': {'source': 'yahoo', 'symbol': 'BZ=F', 'name': 'Brent Crude Oil'},
    'wti_crude': {'source': 'yahoo', 'symbol': 'CL=F', 'name': 'WTI Crude Oil'},
    'gold': {'source': 'yahoo', 'symbol': 'GC=F', 'name': 'Gold Futures'},
    'silver': {'source': 'yahoo', 'symbol': 'SI=F', 'name': 'Silver Futures'},
    'copper': {'source': 'yahoo', 'symbol': 'HG=F', 'name': 'Copper Futures'},
    'aluminum': {'source': 'yahoo', 'symbol': 'ALI=F', 'name': 'Aluminum Futures'},
    'natural_gas': {'source': 'yahoo', 'symbol': 'NG=F', 'name': 'Natural Gas Futures'},
    
    # US Indices (Yahoo Finance)
    'sp500': {'source': 'yahoo', 'symbol': '^GSPC', 'name': 'S&P 500'},
    'nasdaq': {'source': 'yahoo', 'symbol': '^IXIC', 'name': 'NASDAQ Composite'},
    'dow_jones': {'source': 'yahoo', 'symbol': '^DJI', 'name': 'Dow Jones Industrial'},
    'russell2000': {'source': 'yahoo', 'symbol': '^RUT', 'name': 'Russell 2000'},
    'vix': {'source': 'yahoo', 'symbol': '^VIX', 'name': 'VIX Index'},
    
    # US ETFs (sector representatives)
    'xlk': {'source': 'yahoo', 'symbol': 'XLK', 'name': 'Technology ETF'},
    'xle': {'source': 'yahoo', 'symbol': 'XLE', 'name': 'Energy ETF'},
    'xlf': {'source': 'yahoo', 'symbol': 'XLF', 'name': 'Financial ETF'},
    'xlv': {'source': 'yahoo', 'symbol': 'XLV', 'name': 'Healthcare ETF'},
    'xli': {'source': 'yahoo', 'symbol': 'XLI', 'name': 'Industrial ETF'},
    'xly': {'source': 'yahoo', 'symbol': 'XLY', 'name': 'Consumer Discretionary ETF'},
    'xlp': {'source': 'yahoo', 'symbol': 'XLP', 'name': 'Consumer Staples ETF'},
    'xlu': {'source': 'yahoo', 'symbol': 'XLU', 'name': 'Utilities ETF'},
    'jets': {'source': 'yahoo', 'symbol': 'JETS', 'name': 'US Global Jets ETF'},
    'iyr': {'source': 'yahoo', 'symbol': 'IYR', 'name': 'Real Estate ETF'},
    'gdx': {'source': 'yahoo', 'symbol': 'GDX', 'name': 'Gold Miners ETF'},
    'tlt': {'source': 'yahoo', 'symbol': 'TLT', 'name': '20+ Year Treasury Bond ETF'},
    
    # Foreign Exchange (Yahoo Finance)
    'usd_cny': {'source': 'yahoo', 'symbol': 'CNY=X', 'name': 'USD/CNY'},
    'usd_index': {'source': 'yahoo', 'symbol': 'DX-Y.NYB', 'name': 'US Dollar Index'},
    'eur_usd': {'source': 'yahoo', 'symbol': 'EURUSD=X', 'name': 'EUR/USD'},
    
    # US Treasury (Yahoo Finance)
    'us_10y_treasury': {'source': 'yahoo', 'symbol': '^TNX', 'name': '10-Year Treasury Yield'},
    'us_2y_treasury': {'source': 'yahoo', 'symbol': '^FVX', 'name': '2-Year Treasury Yield'},
    
    # FRED (Federal Reserve Economic Data)
    'fed_funds_rate': {'source': 'fred', 'symbol': 'FEDFUNDS', 'name': 'Federal Funds Rate'},
    'cpi_us': {'source': 'fred', 'symbol': 'CPIAUCSL', 'name': 'US CPI'},
    'gdp_us': {'source': 'fred', 'symbol': 'GDP', 'name': 'US GDP'},
    'unemployment_us': {'source': 'fred', 'symbol': 'UNRATE', 'name': 'US Unemployment Rate'},
    'oil_production_us': {'source': 'fred', 'symbol': 'IPG2111111SQ', 'name': 'US Oil Production'},
    
    # A-share Indices (Tushare)
    'csi300': {'source': 'tushare', 'symbol': '000300.SH', 'name': 'CSI 300 Index'},
    'sse_composite': {'source': 'tushare', 'symbol': '000001.SH', 'name': 'Shanghai Composite'},
    'chinext': {'source': 'tushare', 'symbol': '399006.SZ', 'name': 'ChiNext Index'},
    'sse50': {'source': 'tushare', 'symbol': '000016.SH', 'name': 'SSE 50 Index'},
}


def fetch_yahoo(symbol: str, years: int = 30) -> pd.DataFrame:
    """Fetch data from Yahoo Finance."""
    if not YFINANCE_AVAILABLE:
        raise ImportError("yfinance not installed. Run: pip install yfinance")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date, auto_adjust=True)
    
    if df.empty:
        raise ValueError(f"No data returned for symbol: {symbol}")
    
    # Handle MultiIndex or flat columns from yfinance
    df = df.reset_index()
    
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Rename columns to lowercase for consistency
    col_map = {col: col.lower() for col in df.columns}
    df = df.rename(columns=col_map)
    
    # Handle date column (could be 'date' or index name)
    date_col = None
    for col in df.columns:
        if 'date' in col.lower() or col.lower() in ['datetime', 'index']:
            date_col = col
            break
    if date_col:
        df = df.rename(columns={date_col: 'date'})
    elif df.columns[0].lower() not in ['open', 'high', 'low', 'close']:
        df.columns = ['date'] + list(df.columns[1:])
    
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    return df[['date', 'close']]


def fetch_fred(symbol: str, years: int = 30) -> pd.DataFrame:
    """Fetch data from FRED API."""
    try:
        import fredapi
        fred = fredapi.Fred(api_key=os.environ.get('FRED_API_KEY', ''))
    except ImportError:
        # Fallback: use pandas-datareader or manual download
        raise ImportError("fredapi not installed. Run: pip install fredapi")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    data = fred.get_series(symbol, observation_start=start_date, observation_end=end_date)
    
    df = pd.DataFrame({'date': data.index, 'close': data.values})
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    return df


def fetch_tushare(symbol: str, years: int = 30) -> pd.DataFrame:
    """Fetch A-share index data from Tushare."""
    if not TUSHARE_AVAILABLE:
        raise ImportError("tushare not installed. Run: pip install tushare")
    
    pro = ts.pro_api()
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=years * 365)).strftime('%Y%m%d')
    
    df = pro.index_daily(ts_code=symbol, start_date=start_date, end_date=end_date)
    
    if df.empty:
        raise ValueError(f"No data returned for symbol: {symbol}")
    
    df = df.sort_values('trade_date')
    df['date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d')
    
    return df[['date', 'close']]


def fetch_indicator(indicator_id: str, years: int = 30) -> pd.DataFrame:
    """Fetch data for a given indicator."""
    if indicator_id not in INDICATOR_MAPPING:
        raise ValueError(f"Unknown indicator: {indicator_id}. Use --list to see available indicators.")
    
    config = INDICATOR_MAPPING[indicator_id]
    source = config['source']
    symbol = config['symbol']
    
    print(f"Fetching {config['name']} ({symbol}) from {source}...")
    
    if source == 'yahoo':
        return fetch_yahoo(symbol, years)
    elif source == 'fred':
        return fetch_fred(symbol, years)
    elif source == 'tushare':
        return fetch_tushare(symbol, years)
    else:
        raise ValueError(f"Unknown data source: {source}")


def list_indicators():
    """List all available indicators."""
    print("\nAvailable Indicators:")
    print("=" * 60)
    
    categories = {
        'Commodities': ['brent_crude', 'wti_crude', 'gold', 'silver', 'copper', 'aluminum', 'natural_gas'],
        'US Indices': ['sp500', 'nasdaq', 'dow_jones', 'russell2000', 'vix'],
        'US Sector ETFs': ['xlk', 'xle', 'xlf', 'xlv', 'xli', 'jets', 'iyr'],
        'Foreign Exchange': ['usd_cny', 'usd_index', 'eur_usd'],
        'US Treasury': ['us_10y_treasury', 'us_2y_treasury'],
        'FRED Macro': ['fed_funds_rate', 'cpi_us', 'gdp_us', 'unemployment_us', 'oil_production_us'],
        'A-share Indices': ['csi300', 'sse_composite', 'chinext', 'sse50'],
    }
    
    for category, indicators in categories.items():
        print(f"\n{category}:")
        for ind in indicators:
            config = INDICATOR_MAPPING.get(ind, {})
            print(f"  {ind}: {config.get('name', 'N/A')}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Fetch financial indicator historical data')
    parser.add_argument('indicator', nargs='?', help='Indicator ID to fetch')
    parser.add_argument('--years', type=int, default=30, help='Years of historical data (default: 30)')
    parser.add_argument('--output', '-o', help='Output file path (CSV or JSON)')
    parser.add_argument('--list', action='store_true', help='List available indicators')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.list:
        list_indicators()
        return
    
    if not args.indicator:
        parser.error("Please specify an indicator or use --list")
    
    df = fetch_indicator(args.indicator, args.years)
    
    # Print summary
    print(f"\nData Summary:")
    print(f"  Total records: {len(df)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Price range: {df['close'].min():.2f} to {df['close'].max():.2f}")
    
    # Output
    if args.output:
        if args.json:
            data = {
                'indicator': args.indicator,
                'name': INDICATOR_MAPPING[args.indicator]['name'],
                'data': df.to_dict('records')
            }
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            df.to_csv(args.output, index=False)
        print(f"\nSaved to: {args.output}")
    else:
        if args.json:
            print(json.dumps(df.to_dict('records'), indent=2))
        else:
            print(df.to_string())


if __name__ == '__main__':
    main()