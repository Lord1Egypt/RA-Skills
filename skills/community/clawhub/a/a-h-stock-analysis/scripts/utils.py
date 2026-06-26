#!/usr/bin/env python3
import os
import sys
import pandas as pd
import importlib

# Try to import both data sources
HAVE_TUSHARE = False
HAVE_AKSHARE = False
ts = None
ak = None

try:
    import tushare as ts
    HAVE_TUSHARE = True
except ImportError:
    pass

try:
    import akshare as ak
    HAVE_AKSHARE = True
except ImportError:
    pass

def init_tushare():
    if not HAVE_TUSHARE:
        return None
    token = os.environ.get('TUSHARE_TOKEN')
    if not token:
        return None
    try:
        return ts.pro_api(token)
    except Exception:
        return None

def format_ts_code(code):
    """Convert user input code to Tushare format"""
    code = code.strip()
    
    # Handle HK stocks (user inputs 5-digit code)
    if len(code) == 5:
        return f"{code}.HK"
    
    # Handle A shares (user inputs 6-digit code)
    if len(code) == 6:
        first_char = code[0]
        if first_char in ['6', '5', '9']:
            return f"{code}.SH"
        elif first_char in ['0', '3']:
            return f"{code}.SZ"
        elif first_char in ['4', '8']:
            return f"{code}.BJ"
        else:
            # Default to SH if unknown
            return f"{code}.SH"
    
    # Already in Tushare format
    if '.' in code:
        return code
    
    # Fallback
    return code

def format_ak_code(code):
    """Convert user input code to AKShare format"""
    code = code.strip()
    
    # HK stocks (AKShare uses 1-digit prefix 0 + 5-digit)
    if len(code) == 5:
        return code.zfill(6) + '.HK'
    
    # A shares: SH/SZ format consistent
    if len(code) == 6:
        first_char = code[0]
        if first_char in ['6', '5', '9']:
            return f"{code}.SH"
        elif first_char in ['0', '3']:
            return f"{code}.SZ"
        elif first_char in ['4', '8']:
            return f"{code}.BJ"
        else:
            return f"{code}.SH"
    
    if '.' in code:
        return code
    
    return code

def get_hk_daily_tushare(pro, ts_code, start_date, end_date):
    """Get HK daily data from Tushare"""
    df = pro.hk_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df.sort_values('trade_date', ascending=True)

def get_a_share_daily_tushare(pro, ts_code, start_date, end_date):
    """Get A share daily data from Tushare"""
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df.sort_values('trade_date', ascending=True)

def get_daily_akshare(code, start_date, end_date):
    """Get daily data from AKShare (fallback)"""
    ak_code = format_ak_code(code)
    
    if ak_code.endswith('.HK'):
        # HK stock
        df = ak.hk_stock_zh_a_daily(symbol=ak_code, adjust="qfq")
    else:
        # A share
        df = ak.stock_zh_a_daily(symbol=ak_code, adjust="qfq")
    
    # Standardize column names to match Tushare format
    column_map = {
        'date': 'trade_date',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'vol',
    }
    
    df = df.reset_index()
    df = df.rename(columns=column_map)
    
    # Convert date format to YYYYMMDD if needed
    if not pd.api.types.is_numeric_dtype(df['trade_date']):
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y%m%d').astype(int)
    
    # Filter by date range
    if start_date:
        start_int = int(start_date)
        df = df[df['trade_date'] >= start_int]
    if end_date:
        end_int = int(end_date)
        df = df[df['trade_date'] <= end_int]
    
    return df.sort_values('trade_date', ascending=True)

def get_daily(pro, code, start_date=None, end_date=None):
    """
    Get daily data: try Tushare first, fallback to AKShare
    """
    # Try Tushare first if available and initialized
    if pro is not None and HAVE_TUSHARE:
        try:
            ts_code = format_ts_code(code)
            if ts_code.endswith('.HK'):
                df = get_hk_daily_tushare(pro, ts_code, start_date, end_date)
            else:
                df = get_a_share_daily_tushare(pro, ts_code, start_date, end_date)
            if not df.empty:
                return df
        except Exception as e:
            print(f"Tushare failed: {str(e)}, trying AKShare...", file=sys.stderr)
    
    # Fallback to AKShare
    if HAVE_AKSHARE:
        try:
            return get_daily_akshare(code, start_date, end_date)
        except Exception as e:
            print(f"AKShare also failed: {str(e)}", file=sys.stderr)
    
    print("No available data source succeeded", file=sys.stderr)
    return pd.DataFrame()

def get_stock_basic(code):
    """Get stock basic info, try Tushare then AKShare"""
    # Try Tushare first
    pro = init_tushare()
    if pro is not None:
        try:
            ts_code = format_ts_code(code)
            if ts_code.endswith('.HK'):
                df = pro.hk_basic(ts_code=ts_code)
            else:
                df = pro.stock_basic(ts_code=ts_code)
            if not df.empty:
                return df, 'tushare'
        except Exception:
            pass
    
    # Fallback to AKShare
    if HAVE_AKSHARE:
        try:
            ak_code = format_ak_code(code).replace('.', '')
            if len(code) == 5:
                # HK stock
                df = ak.hk_stock_info(symbol=ak_code)
            else:
                # A share
                df = ak.stock_info(symbol=ak_code)
            return pd.DataFrame([df]), 'akshare'
        except Exception:
            pass
    
    return pd.DataFrame(), None
