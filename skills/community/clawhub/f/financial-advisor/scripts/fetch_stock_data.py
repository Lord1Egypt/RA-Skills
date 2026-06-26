#!/usr/bin/env python3
"""
专业股票数据采集脚本 — 支持 A股/港股/美股 全市场
数据源策略：
  - A股/港股 行情与K线：优先腾讯财经 API → 备用 akshare → 备用 yfinance
  - 美股 行情与K线：优先 yfinance（全球覆盖，免费稳定）→ 备用 akshare 美股接口
  - 财务/基本面/分红/估值：所有市场统一使用 yfinance
  - akshare：A股历史K线稳定可用，实时接口可能不稳定（东方财富限流）
- 以 CSV 格式保存到输出目录
- 采集开始时记录准确时间，写入元数据
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 脚本启动时记录准确时间（用于报告中的数据截至时间）
SCRIPT_START_TIME = datetime.now(timezone.utc).astimezone()

try:
    import requests
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install requests pandas numpy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import akshare as ak
except ImportError:
    ak = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

THROTTLE_DELAY = 2
MAX_RETRIES = 3
RETRY_DELAY = 5
YF_BASE_BACKOFF = 3  # yfinance 指数退避基础秒数

# period -> 交易日数量（约）
PERIOD_DAYS = {
    '1d': 1, '5d': 5, '1mo': 22, '3mo': 66, '6mo': 126,
    '1y': 252, '2y': 504, '3y': 756, '5y': 1260, '10y': 2520, 'max': 3000
}

# period -> 自然日数量（用于 akshare start_date 计算）
PERIOD_CALENDAR_DAYS = {
    '1d': 5, '5d': 10, '1mo': 35, '3mo': 100, '6mo': 200,
    '1y': 370, '2y': 740, '3y': 1100, '5y': 1850, '10y': 3700, 'max': 7300
}


# ---------- 市场识别工具 ----------

def detect_market(symbol):
    """
    检测股票代码所属市场
    返回: 'us', 'hk', 'a_sh', 'a_sz', 'unknown'
    """
    s = symbol.strip().upper()
    # 带后缀的明确标识
    if s.endswith('.HK'):
        return 'hk'
    if s.endswith(('.SH', '.SS')):
        return 'a_sh'
    if s.endswith('.SZ'):
        return 'a_sz'
    # 纯数字
    if s.replace('.', '').isdigit():
        code = s.split('.')[0]
        if len(code) == 5:
            return 'hk'
        if len(code) == 6:
            return 'a_sh' if code.startswith('6') else 'a_sz'
    # 纯字母 = 美股（如 AAPL, TSLA, GOOG）
    if s.isalpha():
        return 'us'
    # 字母+数字混合且无后缀（如 BRK.B）— 视为美股
    if not any(s.endswith(sfx) for sfx in ('.SH', '.SS', '.SZ', '.HK')):
        # 检查是否像美股代码
        base = s.split('.')[0]
        if base.isalpha():
            return 'us'
    return 'unknown'


def is_us_stock(symbol):
    return detect_market(symbol) == 'us'


def is_hk_stock(symbol):
    return detect_market(symbol) == 'hk'


def is_a_stock(symbol):
    return detect_market(symbol) in ('a_sh', 'a_sz')


def parse_args():
    parser = argparse.ArgumentParser(description='股票数据采集工具（支持 A股/港股/美股）')
    parser.add_argument('--symbol', required=True,
                        help='股票代码（A股: 600519.SH, 港股: 00700.HK, 美股: AAPL）')
    parser.add_argument('--type', required=True,
                        choices=['realtime', 'history', 'financial', 'fundamental', 'dividends', 'valuation'],
                        help='数据类型')
    parser.add_argument('--period', default='3y', help='历史数据周期')
    parser.add_argument('--interval', default='1d', help='数据间隔')
    parser.add_argument('--reports', default='income,balance,cashflow', help='财务报表类型')
    parser.add_argument('--years', type=int, default=5, help='财务数据年数')
    parser.add_argument('--output-dir', default='./financial_data', help='输出目录')
    parser.add_argument('--format', default='csv,json', help='输出格式')
    parser.add_argument('--source', default='auto',
                        choices=['auto', 'tencent', 'yfinance', 'akshare'],
                        help='数据源：auto=根据市场自动选择最优源')
    return parser.parse_args()


def to_tencent_code(symbol):
    """转换为腾讯 API 代码格式"""
    symbol = symbol.strip().upper()
    if symbol.endswith('.HK'):
        code = symbol.split('.')[0].zfill(5)
        return f"hk{code}", True
    if symbol.endswith(('.SH', '.SS')):
        code = symbol.split('.')[0]
        return f"sh{code}", False
    if symbol.endswith('.SZ'):
        code = symbol.split('.')[0]
        return f"sz{code}", False
    if symbol.isdigit():
        if len(symbol) == 5:
            return f"hk{symbol}", True
        if len(symbol) == 6:
            return (f"sh{symbol}" if symbol.startswith('6') else f"sz{symbol}"), False
    return None, None


def is_tencent_supported(symbol):
    """腾讯 API 仅支持 A股、港股，不支持美股"""
    code, is_hk = to_tencent_code(symbol)
    return code is not None


def fetch_tencent_kline(symbol, count=756, period='day'):
    """
    腾讯财经 K 线（与 niuniu_dev/demo.py 完全一致，确保数据可靠性）
    接口：港股 hkfqkline/get，A股 fqkline/get；参数 param={code},{period},,,{count},qfq
    """
    code, is_hk = to_tencent_code(symbol)
    if code is None:
        return None

    if is_hk:
        base_url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
    else:
        base_url = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get"

    url = f"{base_url}?param={code},{period},,,{count},qfq"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://stock.finance.qq.com/'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        if data.get('code') != 0:
            return None

        stock_data = data.get('data', {}).get(code)
        if not stock_data:
            return None

        for key in (['qfqday', 'day'] if period == 'day' else ['qfqweek', 'week'] if period == 'week' else ['qfqmonth', 'month']):
            if key in stock_data and stock_data[key]:
                klines = stock_data[key]
                break
        else:
            return None

        rows = []
        for item in klines:
            h, l = float(item[3]), float(item[4])
            rows.append({
                'Date': item[0],
                'Open': float(item[1]),
                'Close': float(item[2]),
                'High': max(h, l),
                'Low': min(h, l),
                'Volume': float(item[5]),
            })
        df = pd.DataFrame(rows)
        df['Amount'] = (df['Open'] * df['Volume']).fillna(0)
        df['Amplitude'] = ((df['High'] - df['Low']) / df['Low'].replace(0, np.nan) * 100).fillna(0)
        df['Change_Pct'] = df['Close'].pct_change().fillna(0) * 100
        df['Change'] = df['Close'].diff().fillna(0)
        df['Turnover'] = 0
        return df
    except Exception as e:
        logger.debug(f"腾讯 API 失败: {e}")
        return None


def add_metadata(df, symbol, data_type, source):
    """添加元数据，使用脚本启动时的准确时间"""
    df = df.copy()
    df['数据来源'] = source
    df['股票代码'] = symbol
    df['数据类型'] = data_type
    df['获取时间'] = SCRIPT_START_TIME.strftime('%Y-%m-%d %H:%M:%S')
    return df


def save_data(df, output_dir, filename_base, formats, metadata=None):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    saved = []
    if 'csv' in formats:
        p = output_path / f"{filename_base}.csv"
        df.to_csv(p, index=False, encoding='utf-8-sig')
        saved.append(str(p))
        logger.info(f"CSV已保存: {p}")
    if 'json' in formats:
        p = output_path / f"{filename_base}.json"
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({'metadata': metadata or {}, 'data': df.to_dict(orient='records')},
                      f, ensure_ascii=False, indent=2, default=str)
        saved.append(str(p))
    if 'xlsx' in formats:
        p = output_path / f"{filename_base}.xlsx"
        df.to_excel(p, index=False, engine='openpyxl')
        saved.append(str(p))
    return saved


# ---------- 腾讯 API 获取（优先） ----------

def fetch_realtime_tencent(symbol, original_symbol):
    """实时行情：从腾讯 1 日 K 线取最后一行"""
    df = fetch_tencent_kline(symbol, count=5, period='day')
    if df is None or df.empty:
        return None
    row = df.iloc[-1]
    result = pd.DataFrame([{
        '股票代码': original_symbol,
        '股票名称': original_symbol,
        '最新价': row['Close'],
        '涨跌额': row['Change'],
        '涨跌幅(%)': row['Change_Pct'],
        '成交量': int(row['Volume']),
        '成交额': row['Amount'],
        '振幅(%)': row['Amplitude'],
        '最高': row['High'],
        '最低': row['Low'],
        '今开': row['Open'],
        '昨收': row['Open'] if len(df) < 2 else df.iloc[-2]['Close'],
        '换手率(%)': 0,
        '市盈率': 0,
        '市净率': 0,
    }])
    return add_metadata(result, original_symbol, 'realtime', 'tencent')


def fetch_history_tencent(symbol, period, original_symbol):
    """历史 K 线"""
    count = PERIOD_DAYS.get(period, 756)
    df = fetch_tencent_kline(symbol, count=count, period='day')
    if df is None or df.empty:
        return None
    return add_metadata(df, original_symbol, 'history', 'tencent')


# ---------- akshare 备用（A股稳定，港股/美股需测试） ----------

def _get_akshare_code(symbol):
    """提取纯数字代码用于 akshare"""
    s = symbol.strip().upper()
    if '.' in s:
        return s.split('.')[0]
    return s


def fetch_realtime_akshare(symbol, original_symbol):
    """akshare 实时行情（A股/港股）"""
    if ak is None:
        return None
    market = detect_market(symbol)
    code = _get_akshare_code(symbol)
    try:
        if market in ('a_sh', 'a_sz'):
            df_all = ak.stock_zh_a_spot_em()
            row = df_all[df_all['代码'] == code]
        elif market == 'hk':
            code = code.zfill(5)
            df_all = ak.stock_hk_spot_em()
            row = df_all[df_all['代码'] == code]
        else:
            return None

        if row.empty:
            return None
        r = row.iloc[0]

        def safe_float(key, default=0.0):
            try:
                if key in r and pd.notna(r[key]):
                    return float(r[key])
            except Exception:
                pass
            return default

        result = pd.DataFrame([{
            '股票代码': original_symbol,
            '股票名称': r.get('名称', original_symbol),
            '最新价': safe_float('最新价'),
            '涨跌额': safe_float('涨跌额'),
            '涨跌幅(%)': safe_float('涨跌幅'),
            '成交量': int(safe_float('成交量')),
            '成交额': safe_float('成交额'),
            '振幅(%)': safe_float('振幅'),
            '最高': safe_float('最高'),
            '最低': safe_float('最低'),
            '今开': safe_float('今开'),
            '昨收': safe_float('昨收'),
            '换手率(%)': safe_float('换手率'),
            '市盈率': safe_float('市盈率-动态', safe_float('市盈率')),
            '市净率': safe_float('市净率'),
        }])
        return add_metadata(result, original_symbol, 'realtime', 'akshare')
    except Exception as e:
        logger.debug(f"akshare realtime 失败: {e}")
        return None


def fetch_history_akshare(symbol, period, original_symbol):
    """akshare 历史K线（A股稳定可靠，港股需测试）"""
    if ak is None:
        return None
    market = detect_market(symbol)
    code = _get_akshare_code(symbol)
    days = PERIOD_CALENDAR_DAYS.get(period, 1100)
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')

    try:
        if market in ('a_sh', 'a_sz'):
            df = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date, adjust="qfq"
            )
        elif market == 'hk':
            code = code.zfill(5)
            df = ak.stock_hk_hist(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date, adjust="qfq"
            )
        else:
            return None

        if df is None or df.empty:
            return None

        # akshare 的列名可能是中文，需要标准化
        col_map = {
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close',
            '最高': 'High', '最低': 'Low', '成交量': 'Volume',
            '成交额': 'Amount', '振幅': 'Amplitude',
            '涨跌幅': 'Change_Pct', '涨跌额': 'Change', '换手率': 'Turnover'
        }
        df = df.rename(columns=col_map)

        # 确保必要列存在
        for col in ['Amount', 'Amplitude', 'Change_Pct', 'Change', 'Turnover']:
            if col not in df.columns:
                if col == 'Amount':
                    df[col] = (df['Open'] * df['Volume']).fillna(0)
                elif col == 'Amplitude':
                    df[col] = ((df['High'] - df['Low']) / df['Low'].replace(0, np.nan) * 100).fillna(0)
                elif col == 'Change_Pct':
                    df[col] = df['Close'].pct_change().fillna(0) * 100
                elif col == 'Change':
                    df[col] = df['Close'].diff().fillna(0)
                else:
                    df[col] = 0

        return add_metadata(df, original_symbol, 'history', 'akshare')
    except Exception as e:
        logger.debug(f"akshare history 失败: {e}")
        return None


# ---------- yfinance（全球市场通用，带速率限制保护） ----------

# Ticker 对象缓存：避免重复创建 Ticker 导致多次 cookie/crumb 请求
_yf_ticker_cache = {}
# 上次 yfinance 请求时间戳
_yf_last_request_time = 0
# info 缓存：同一个 symbol 的 info 只获取一次
_yf_info_cache = {}


def get_yfinance_symbol(symbol):
    symbol = symbol.strip().upper()
    if symbol.endswith(('.SS', '.SZ', '.HK')):
        return symbol
    if symbol.endswith('.SH'):
        return symbol.replace('.SH', '.SS')
    if symbol.isdigit():
        if len(symbol) == 6:
            return f"{symbol}.SS" if symbol.startswith('6') else f"{symbol}.SZ"
        if len(symbol) == 5:
            return f"{symbol}.HK"
    return symbol


def _yf_get_ticker(symbol):
    """获取或复用 Ticker 对象，避免重复创建"""
    if symbol not in _yf_ticker_cache:
        _yf_ticker_cache[symbol] = yf.Ticker(symbol)
    return _yf_ticker_cache[symbol]


def _yf_throttle():
    """自适应节流：确保两次 yfinance 请求间隔足够"""
    global _yf_last_request_time
    now = time.time()
    elapsed = now - _yf_last_request_time
    if elapsed < THROTTLE_DELAY:
        time.sleep(THROTTLE_DELAY - elapsed)
    _yf_last_request_time = time.time()


def _yf_call_with_retry(func, label="yfinance"):
    """带指数退避的 yfinance 调用包装器，专门处理 YFRateLimitError"""
    for attempt in range(MAX_RETRIES):
        _yf_throttle()
        try:
            return func()
        except Exception as e:
            err_name = type(e).__name__
            if 'RateLimit' in err_name or 'Too Many Requests' in str(e):
                wait = YF_BASE_BACKOFF * (2 ** attempt)
                logger.warning(f"{label} 速率限制 (尝试 {attempt+1}/{MAX_RETRIES})，等待 {wait}s...")
                time.sleep(wait)
                # 清空 Ticker 缓存，因为限流后 cookie/crumb 可能失效
                _yf_ticker_cache.clear()
                _yf_info_cache.clear()
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"{label} 已达最大重试次数，放弃")
                    raise
            else:
                raise
    return None


def _yf_get_info(symbol):
    """获取 info 并缓存：同一 symbol 在单次脚本运行中只请求一次"""
    if symbol in _yf_info_cache:
        return _yf_info_cache[symbol]

    def _fetch():
        ticker = _yf_get_ticker(symbol)
        info = ticker.info
        if info:
            _yf_info_cache[symbol] = info
        return info

    info = _yf_call_with_retry(_fetch, f"yfinance.info({symbol})")
    return info


def fetch_realtime_yfinance(symbol, original_symbol):
    """
    yfinance 实时行情获取策略：
    1. 先尝试 info (丰富但容易触发限流)
    2. info 被限流时 fallback 到 history(period='5d') (不走 info 端点)
    """
    if yf is None:
        return None

    # 策略1: 尝试 info
    try:
        info = _yf_get_info(symbol)
        if info:
            price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
            prev = info.get('previousClose') or price
            df = pd.DataFrame([{
                '股票代码': original_symbol,
                '股票名称': info.get('shortName', original_symbol),
                '最新价': float(price),
                '涨跌额': float(price - prev) if prev else 0,
                '涨跌幅(%)': float(info.get('regularMarketChangePercent', 0)),
                '成交量': int(info.get('volume', 0)),
                '成交额': int(info.get('volume', 0)) * float(price),
                '振幅(%)': 0,
                '最高': float(info.get('dayHigh', 0)),
                '最低': float(info.get('dayLow', 0)),
                '今开': float(info.get('open', 0)),
                '昨收': float(prev),
                '换手率(%)': 0,
                '市盈率': float(info.get('trailingPE', 0)),
                '市净率': float(info.get('priceToBook', 0)),
            }])
            return add_metadata(df, original_symbol, 'realtime', 'yfinance')
    except Exception as e:
        logger.info(f"yfinance info 受限，尝试 history fallback: {type(e).__name__}")

    # 策略2: info 失败/限流时，用 history(period='5d') 取最近交易日数据
    try:
        def _fetch_hist():
            ticker = _yf_get_ticker(symbol)
            return ticker.history(period='5d', interval='1d')

        hist = _yf_call_with_retry(_fetch_hist, f"yfinance.history_fallback({symbol})")
        if hist is not None and not hist.empty:
            last = hist.iloc[-1]
            prev_close = hist.iloc[-2]['Close'] if len(hist) >= 2 else last['Open']
            price = float(last['Close'])
            df = pd.DataFrame([{
                '股票代码': original_symbol,
                '股票名称': original_symbol,
                '最新价': price,
                '涨跌额': price - float(prev_close),
                '涨跌幅(%)': ((price / float(prev_close)) - 1) * 100 if prev_close else 0,
                '成交量': int(last.get('Volume', 0)),
                '成交额': int(last.get('Volume', 0)) * price,
                '振幅(%)': ((float(last['High']) - float(last['Low'])) / float(last['Low']) * 100) if last['Low'] else 0,
                '最高': float(last['High']),
                '最低': float(last['Low']),
                '今开': float(last['Open']),
                '昨收': float(prev_close),
                '换手率(%)': 0,
                '市盈率': 0,
                '市净率': 0,
            }])
            logger.info("使用 history fallback 获取 realtime 数据")
            return add_metadata(df, original_symbol, 'realtime', 'yfinance(history_fallback)')
    except Exception as e:
        logger.debug(f"yfinance history fallback 也失败: {type(e).__name__}: {e}")

    return None


def fetch_history_yfinance(symbol, period, original_symbol):
    """历史K线：只调用 ticker.history()，不触发 info 请求"""
    if yf is None:
        return None
    try:
        def _fetch():
            ticker = _yf_get_ticker(symbol)
            return ticker.history(period=period, interval='1d', auto_adjust=True)

        hist = _yf_call_with_retry(_fetch, f"yfinance.history({symbol})")
        if hist is None or hist.empty:
            return None
        df = hist.reset_index()
        if 'Date' not in df.columns and len(df.columns) > 0:
            df = df.rename(columns={df.columns[0]: 'Date'})
        required = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(c in df.columns for c in required):
            return None
        df = df[required].copy()
        df['Amount'] = (df['Open'] * df['Volume']).fillna(0)
        df['Amplitude'] = ((df['High'] - df['Low']) / df['Low'].replace(0, np.nan) * 100).fillna(0)
        df['Change_Pct'] = df['Close'].pct_change().fillna(0) * 100
        df['Change'] = df['Close'].diff().fillna(0)
        df['Turnover'] = 0
        return add_metadata(df, original_symbol, 'history', 'yfinance')
    except Exception as e:
        logger.debug(f"yfinance history 失败: {type(e).__name__}: {e}")
        return None


def fetch_financial_yfinance(symbol, original_symbol, reports):
    if yf is None:
        return None
    try:
        def _fetch():
            ticker = _yf_get_ticker(symbol)
            all_dfs = []
            mapping = {'income': 'income_stmt', 'balance': 'balance_sheet', 'cashflow': 'cashflow'}
            for r in [x.strip() for x in reports.split(',')]:
                if r not in mapping:
                    continue
                try:
                    tbl = getattr(ticker, mapping[r], None)
                    if tbl is not None and hasattr(tbl, 'columns'):
                        df = pd.DataFrame(tbl).reset_index()
                        if not df.empty:
                            df['报表类型'] = r
                            all_dfs.append(add_metadata(df, original_symbol, f'financial_{r}', 'yfinance'))
                except Exception:
                    pass
            return all_dfs

        all_dfs = _yf_call_with_retry(_fetch, f"yfinance.financial({symbol})")
        if not all_dfs:
            return None
        return pd.concat(all_dfs, ignore_index=True)
    except Exception as e:
        logger.debug(f"yfinance financial 失败: {type(e).__name__}: {e}")
        return None


def fetch_fundamental_yfinance(symbol, original_symbol):
    if yf is None:
        return None
    try:
        info = _yf_get_info(symbol)
        if not info:
            return None
        df = pd.DataFrame([{
            '股票代码': original_symbol,
            '市盈率': info.get('trailingPE'),
            '市净率': info.get('priceToBook'),
            '市销率': info.get('priceToSalesTrailing12Months'),
            '市值': info.get('marketCap'),
            'ROE': info.get('returnOnEquity'),
            'ROA': info.get('returnOnAssets'),
            '毛利率': info.get('grossMargins'),
            '净利率': info.get('profitMargins'),
            '营收增长率': info.get('revenueGrowth'),
            '股息率': info.get('dividendYield'),
        }])
        return add_metadata(df, original_symbol, 'fundamental', 'yfinance')
    except Exception as e:
        logger.debug(f"yfinance fundamental 失败: {type(e).__name__}: {e}")
        return None


def fetch_dividends_yfinance(symbol, original_symbol):
    if yf is None:
        return None
    try:
        def _fetch():
            ticker = _yf_get_ticker(symbol)
            return ticker.dividends

        div = _yf_call_with_retry(_fetch, f"yfinance.dividends({symbol})")
        if div is None or len(div) == 0:
            return None
        df = div.reset_index()
        df.columns = ['Date', '分红金额']
        df['股票代码'] = original_symbol
        return add_metadata(df, original_symbol, 'dividends', 'yfinance')
    except Exception as e:
        logger.debug(f"yfinance dividends 失败: {type(e).__name__}: {e}")
        return None


def fetch_valuation_yfinance(symbol, original_symbol):
    """估值数据：复用 info 缓存，不额外请求"""
    if yf is None:
        return None
    try:
        info = _yf_get_info(symbol)
        if not info:
            return None
        df = pd.DataFrame([{
            '股票代码': original_symbol,
            '市盈率': info.get('trailingPE'),
            '市净率': info.get('priceToBook'),
            '市销率': info.get('priceToSalesTrailing12Months'),
            '市值': info.get('marketCap'),
            '企业价值': info.get('enterpriseValue'),
        }])
        return add_metadata(df, original_symbol, 'valuation', 'yfinance')
    except Exception as e:
        logger.debug(f"yfinance valuation 失败: {type(e).__name__}: {e}")
        return None



def main():
    args = parse_args()
    symbol = args.symbol
    market = detect_market(symbol)
    logger.info(f"开始采集: {symbol}, 类型: {args.type}, 检测市场: {market}")

    df = None
    metadata = {'symbol': symbol, 'data_type': args.type,
                'market': market, 'fetch_time': SCRIPT_START_TIME.isoformat()}

    yf_sym = get_yfinance_symbol(symbol)
    source = args.source

    # ========== realtime ==========
    if args.type == 'realtime':
        if market == 'us':
            # 美股：直接 yfinance，不浪费时间尝试其他源
            if source in ('auto', 'yfinance') and yf:
                df = fetch_realtime_yfinance(yf_sym, symbol)
        else:
            # A股/港股：腾讯 → akshare → yfinance（yfinance 仅作最后兜底）
            if source in ('auto', 'tencent') and is_tencent_supported(symbol):
                df = fetch_realtime_tencent(symbol, symbol)
            if df is None and source in ('auto', 'akshare') and ak:
                df = fetch_realtime_akshare(symbol, symbol)
            if df is None and source in ('auto', 'yfinance') and yf:
                logger.info("A股/港股前两个源失败，尝试 yfinance 兜底")
                df = fetch_realtime_yfinance(yf_sym, symbol)

    # ========== history ==========
    elif args.type == 'history':
        metadata['period'] = args.period
        if market == 'us':
            # 美股：直接 yfinance
            if source in ('auto', 'yfinance') and yf:
                df = fetch_history_yfinance(yf_sym, args.period, symbol)
        else:
            # A股/港股：腾讯 → akshare → yfinance
            if source in ('auto', 'tencent') and is_tencent_supported(symbol):
                df = fetch_history_tencent(symbol, args.period, symbol)
            if df is None and source in ('auto', 'akshare') and ak:
                df = fetch_history_akshare(symbol, args.period, symbol)
            if df is None and source in ('auto', 'yfinance') and yf:
                logger.info("A股/港股前两个源失败，尝试 yfinance 兜底")
                df = fetch_history_yfinance(yf_sym, args.period, symbol)

    # ========== financial ==========
    elif args.type == 'financial':
        metadata['reports'] = args.reports
        if yf:
            df = fetch_financial_yfinance(yf_sym, symbol, args.reports)

    # ========== fundamental ==========
    elif args.type == 'fundamental':
        if yf:
            df = fetch_fundamental_yfinance(yf_sym, symbol)

    # ========== dividends ==========
    elif args.type == 'dividends':
        if yf:
            df = fetch_dividends_yfinance(yf_sym, symbol)

    # ========== valuation ==========
    elif args.type == 'valuation':
        if yf:
            df = fetch_valuation_yfinance(yf_sym, symbol)

    # ========== 保存结果 ==========
    if df is not None and not df.empty:
        metadata['source'] = df['数据来源'].iloc[0] if '数据来源' in df.columns else 'unknown'
        safe = symbol.replace('.', '_')
        formats = [f.strip() for f in args.format.split(',')]
        save_data(df, args.output_dir, f"{safe}_{args.type}", formats, metadata)
        logger.info(f"✅ 成功! 记录数: {len(df)}, 数据源: {metadata['source']}, 市场: {market}")
        print("\n数据预览:")
        print(df.head().to_string())
        sys.exit(0)
    else:
        logger.error(f"❌ 未获取到数据 (symbol={symbol}, type={args.type}, market={market})")
        logger.error("建议：")
        if market == 'us':
            logger.error("  美股需要 yfinance 支持，请确保: pip install yfinance")
            logger.error("  且网络可访问 Yahoo Finance (可能需要代理)")
            logger.error("  如遇速率限制，请稍等几分钟后重试")
        elif market == 'unknown':
            logger.error(f"  无法识别 {symbol} 所属市场，请检查代码格式")
            logger.error("  A股: 600519.SH / 000858.SZ, 港股: 00700.HK, 美股: AAPL")
        sys.exit(2)


if __name__ == '__main__':
    main()
