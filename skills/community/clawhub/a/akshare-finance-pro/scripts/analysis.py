#!/usr/bin/env python3
"""
A股智能投资助手 - 增强版
支持错误处理、重试、备用数据源
"""

import time
import json
from datetime import datetime, timedelta
from functools import wraps


def retry(max_retries=3, delay=2, backoff=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise Exception(f"{func.__name__} 失败 (重试{max_retries}次): {e}")
                    print(f"[重试] {func.__name__} 失败，{current_delay}秒后重试 ({retries}/{max_retries})...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator


def safe_import(module_name):
    """安全导入模块"""
    try:
        return __import__(module_name)
    except ImportError:
        raise Exception(f"请安装 {module_name}: pip install {module_name}")


# ============ 数据获取函数 ============

@retry(max_retries=3, delay=2)
def get_stock_list():
    """获取A股股票列表"""
    ak = safe_import('akshare')
    df = ak.stock_zh_a_spot_em()
    return df


@retry(max_retries=3, delay=2)
def get_stock_kline(symbol, period='daily', start_date='20240101'):
    """获取K线数据"""
    ak = safe_import('akshare')
    df = ak.stock_zh_kline(symbol=symbol, period=period, adjust='qfq', start_date=start_date)
    return df


@retry(max_retries=3, delay=2)
def get_macro_data(func_name):
    """获取宏观经济数据"""
    ak = safe_import('akshare')
    func = getattr(ak, func_name, None)
    if func is None:
        raise Exception(f"接口 {func_name} 不存在")
    return func()


# ============ 备用数据源 ============

@retry(max_retries=3, delay=2)
def get_stock_from_eastmoney(symbol):
    """从东方财富直接获取股票数据（备用方案）"""
    requests = safe_import('requests')
    pd = safe_import('pandas')
    
    # 转换股票代码格式
    if symbol.startswith('6'):
        secid = f"1.{symbol}"
    else:
        secid = f"0.{symbol}"
    
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        'secid': secid,
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt': '101',  # 日K
        'fqt': '1',    # 前复权
        'beg': '20240101',
        'end': '20500101',
        'lmt': '1000'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.eastmoney.com'
    }
    
    r = requests.get(url, params=params, headers=headers, timeout=15)
    data = r.json()
    
    if data.get('data') and data['data'].get('klines'):
        klines = data['data']['klines']
        rows = []
        for line in klines:
            parts = line.split(',')
            rows.append({
                '日期': parts[0],
                '开盘': float(parts[1]),
                '收盘': float(parts[2]),
                '最高': float(parts[3]),
                '最低': float(parts[4]),
                '成交量': float(parts[5]),
                '成交额': float(parts[6]),
                '振幅': float(parts[7]),
                '涨跌幅': float(parts[8]),
                '涨跌额': float(parts[9]),
                '换手率': float(parts[10])
            })
        return pd.DataFrame(rows)
    
    raise Exception("未获取到数据")


@retry(max_retries=3, delay=2)
def get_realtime_from_eastmoney():
    """从东方财富获取实时行情（备用方案）"""
    requests = safe_import('requests')
    pd = safe_import('pandas')
    
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': '1',
        'pz': '5000',
        'po': '1',
        'np': '1',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
        'fields': 'f2,f3,f4,f5,f6,f7,f12,f14,f15,f16,f17,f18'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.eastmoney.com'
    }
    
    r = requests.get(url, params=params, headers=headers, timeout=15)
    data = r.json()
    
    if data.get('data') and data['data'].get('diff'):
        rows = []
        for item in data['data']['diff']:
            rows.append({
                '代码': item.get('f12', ''),
                '名称': item.get('f14', ''),
                '最新价': item.get('f2', 0),
                '涨跌幅': item.get('f3', 0),
                '涨跌额': item.get('f4', 0),
                '成交量': item.get('f5', 0),
                '成交额': item.get('f6', 0),
                '振幅': item.get('f7', 0),
                '最高': item.get('f15', 0),
                '最低': item.get('f16', 0),
                '今开': item.get('f17', 0),
                '昨收': item.get('f18', 0)
            })
        return pd.DataFrame(rows)
    
    raise Exception("未获取到数据")


# ============ 智能数据获取 ============

def get_stock_data_smart(symbol, start_date='20240101'):
    """智能获取股票数据（自动尝试多个数据源）"""
    # 方案1: AKShare
    try:
        return get_stock_kline(symbol, start_date=start_date)
    except Exception as e:
        print(f"⚠️ AKShare 失败: {e}")
    
    # 方案2: 东方财富直接API
    try:
        print("尝试备用数据源: 东方财富...")
        return get_stock_from_eastmoney(symbol)
    except Exception as e:
        print(f"⚠️ 东方财富失败: {e}")
    
    raise Exception("所有数据源均不可用，请检查网络连接")


def get_realtime_smart():
    """智能获取实时行情（自动尝试多个数据源）"""
    # 方案1: AKShare
    try:
        return get_stock_list()
    except Exception as e:
        print(f"⚠️ AKShare 失败: {e}")
    
    # 方案2: 东方财富直接API
    try:
        print("尝试备用数据源: 东方财富...")
        return get_realtime_from_eastmoney()
    except Exception as e:
        print(f"⚠️ 东方财富失败: {e}")
    
    raise Exception("所有数据源均不可用，请检查网络连接")


# ============ 技术指标计算 ============

def calc_indicators(df):
    """计算技术指标"""
    ta = safe_import('ta')
    pd = safe_import('pandas')
    
    # 确保列名正确
    close_col = '收盘' if '收盘' in df.columns else 'close'
    high_col = '最高' if '最高' in df.columns else 'high'
    low_col = '最低' if '最低' in df.columns else 'low'
    
    # MACD
    df['macd'] = ta.trend.macd(df[close_col])
    df['macd_signal'] = ta.trend.macd_signal(df[close_col])
    df['macd_hist'] = ta.trend.macd_diff(df[close_col])
    
    # KDJ
    df['stoch_k'] = ta.momentum.stoch(df[high_col], df[low_col], df[close_col])
    df['stoch_d'] = ta.momentum.stoch_signal(df[high_col], df[low_col], df[close_col])
    df['stoch_j'] = 3 * df['stoch_k'] - 2 * df['stoch_d']
    
    # 布林带
    df['bb_upper'] = ta.volatility.bollinger_hband(df[close_col])
    df['bb_middle'] = ta.volatility.bollinger_mavg(df[close_col])
    df['bb_lower'] = ta.volatility.bollinger_lband(df[close_col])
    
    # RSI
    df['rsi'] = ta.momentum.rsi(df[close_col])
    
    # 均线
    df['ma5'] = df[close_col].rolling(5).mean()
    df['ma10'] = df[close_col].rolling(10).mean()
    df['ma20'] = df[close_col].rolling(20).mean()
    df['ma60'] = df[close_col].rolling(60).mean()
    
    return df


def detect_signals(df):
    """识别买卖信号"""
    signals = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    close_col = '收盘' if '收盘' in df.columns else 'close'
    
    # MACD 金叉/死叉
    if prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal']:
        signals.append("📈 MACD金叉 (买入信号)")
    elif prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal']:
        signals.append("📉 MACD死叉 (卖出信号)")
    
    # KDJ 超买超卖
    if latest['stoch_j'] > 100:
        signals.append("⚠️ KDJ超买 (J>100)")
    elif latest['stoch_j'] < 0:
        signals.append("💡 KDJ超卖 (J<0)")
    
    # RSI 超买超卖
    if latest['rsi'] > 70:
        signals.append("⚠️ RSI超买 (>70)")
    elif latest['rsi'] < 30:
        signals.append("💡 RSI超卖 (<30)")
    
    # 布林带突破
    if latest[close_col] > latest['bb_upper']:
        signals.append("🚀 突破布林上轨")
    elif latest[close_col] < latest['bb_lower']:
        signals.append("💰 跌破布林下轨")
    
    # 均线多头/空头
    if latest['ma5'] > latest['ma10'] > latest['ma20']:
        signals.append("🔺 均线多头排列")
    elif latest['ma5'] < latest['ma10'] < latest['ma20']:
        signals.append("🔻 均线空头排列")
    
    return signals


# ============ 告警功能 ============

def check_alerts(watchlist, thresholds=None):
    """检查自选股告警"""
    if thresholds is None:
        thresholds = {
            'pct_change_up': 5.0,
            'pct_change_down': -5.0,
        }
    
    try:
        df = get_realtime_smart()
    except Exception as e:
        return [{'error': f'获取行情失败: {e}'}]
    
    alerts = []
    for ticker in watchlist:
        stock = df[df['代码'] == ticker]
        if stock.empty:
            continue
        
        stock = stock.iloc[0]
        pct = stock.get('涨跌幅', 0)
        name = stock.get('名称', ticker)
        
        if pct >= thresholds['pct_change_up']:
            alerts.append({
                'ticker': ticker,
                'name': name,
                'type': '涨幅告警',
                'message': f"🚀 {name}({ticker}) 涨幅 {pct:.2f}%"
            })
        elif pct <= thresholds['pct_change_down']:
            alerts.append({
                'ticker': ticker,
                'name': name,
                'type': '跌幅告警',
                'message': f"📉 {name}({ticker}) 跌幅 {pct:.2f}%"
            })
    
    return alerts


# ============ 报告生成 ============

def generate_report(watchlist):
    """生成持仓报告"""
    try:
        df = get_realtime_smart()
    except Exception as e:
        return f"获取行情失败: {e}"
    
    report = []
    report.append(f"# 持仓日报 {datetime.now().strftime('%Y-%m-%d')}\n")
    
    for ticker in watchlist:
        stock = df[df['代码'] == ticker]
        if stock.empty:
            continue
        stock = stock.iloc[0]
        
        name = stock.get('名称', ticker)
        price = stock.get('最新价', 'N/A')
        pct = stock.get('涨跌幅', 0)
        
        # 获取技术信号
        try:
            kline = get_stock_data_smart(ticker, start_date='20240101')
            indicators = calc_indicators(kline)
            signals = detect_signals(indicators)
            signal_str = ", ".join(signals[:2]) if signals else "无明显信号"
        except Exception as e:
            signal_str = f"分析失败: {e}"
        
        report.append(f"**{name}** ({ticker})")
        report.append(f"- 最新价: {price}")
        report.append(f"- 涨跌幅: {pct:.2f}%")
        report.append(f"- 技术信号: {signal_str}")
        report.append("")
    
    return "\n".join(report)


# ============ 主程序 ============

if __name__ == "__main__":
    # 测试
    watchlist = ["000001", "600519", "000858"]
    print(generate_report(watchlist))
