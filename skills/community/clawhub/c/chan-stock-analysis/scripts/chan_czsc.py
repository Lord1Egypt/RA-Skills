#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论多级别联立股票/指数行情分析 v7（增强版 + 百度云盘集成）
- 正确的缠论理论：中枢 → 笔 → 背驰 → 买卖点 → 多级别联立
- 数据源优先级：
  * XAUUSD: itick → 缓存
  * A股/港股: akshare → futu → tushare → 缓存
- K线数据缓存机制：24小时有效
- 百度云盘数据整合：先从百度云下载obsidian数据并整合
- 分析完成后上传报告和图片至百度云盘
"""

import os
import sys
import json
import argparse
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============ 路径配置（从 config.py 读取，支持环境变量覆盖） ============
_script_dir_early = os.path.dirname(os.path.abspath(__file__))
import importlib.util as _ilu
_cfg_spec = _ilu.spec_from_file_location(
    "chan_config",
    os.path.join(_script_dir_early, "config.py"),
)
_cfg = _ilu.module_from_spec(_cfg_spec)
_cfg_spec.loader.exec_module(_cfg)

WORKSPACE = Path("D:/QClawData/workspace")
OBSIDIAN_DIR = _cfg.OBSIDIAN_STOCK_DIR.parent  # D:/knowledge
BAIDU_KLINE_DIR = "/knowledge/stockdata"  # 百度云K线数据目录

# 导入czsc分析器
CZSC_ANALYZER_AVAILABLE = False
try:
    # 添加脚本目录到路径
    script_dir = _script_dir_early
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # 添加czsc目录到路径（从配置读取）
    czsc_path = _cfg.CZSC_PATH
    if czsc_path not in sys.path:
        sys.path.insert(0, czsc_path)
    
    from czsc_analyzer import analyze_level as analyze_level_czsc
    CZSC_ANALYZER_AVAILABLE = True
    print("✓ CZSC模块分析器已加载")
except Exception as e:
    print(f"✗ CZSC模块分析器加载失败: {e}")
    analyze_level_czsc = None

# ============ itick API配置（从配置读取） ============
ITICK_API = _cfg.ITICK_API
ITICK_TOKEN = _cfg.ITICK_TOKEN
ITICK_KTYPE = {
    'daily': 8, '1': 8,
    '60': 5, '60min': 5, '1h': 5,
    '30': 4, '30min': 4,
    '15': 3, '15min': 3,
    '5': 2, '5min': 2,
    '1': 1, '1min': 1,
}

# 缓存目录
try:
    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    os.makedirs(CACHE_DIR, exist_ok=True)
except:
    CACHE_DIR = os.path.join(os.path.expanduser('~'), '.chan_cache')

def get_cache_path(code, period):
    return os.path.join(CACHE_DIR, f"{code}_{period}.json")

def load_cache(code, period):
    cache_path = get_cache_path(code, period)
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cache_time = datetime.fromisoformat(data.get('cache_time', '2000-01-01'))
            if (datetime.now() - cache_time).total_seconds() < 0.5 * 3600:
                print(f"   缓存命中: {len(data.get('klines', []))}根")
                return data.get('klines', []), data.get('source', 'cache')
        except:
            pass
    return None, None

def save_cache(code, period, klines, source):
    cache_path = get_cache_path(code, period)
    data = {
        'klines': klines,
        'source': source,
        'cache_time': datetime.now().isoformat()
    }
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except:
        pass

# ============ 百度云盘功能 ============

def bypy_command(cmd, timeout=60):
    """执行bypy命令"""
    try:
        result = subprocess.run(
            ['bypy'] + cmd.split(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_bypy_auth():
    """检查bypy是否已认证"""
    success, msg = bypy_command("info", timeout=10)
    if not success and ('authorize' in msg.lower() or 'auth' in msg.lower() or 'EOFError' in msg):
        return False
    return True

def download_bypy_file(remote_path, local_path):
    """从百度云下载文件"""
    if not check_bypy_auth():
        return False
    print(f"   从百度云下载: {remote_path}")
    success, msg = bypy_command(f"download {remote_path} {local_path}")
    if success:
        print(f"   下载成功: {local_path}")
        return True
    else:
        print(f"   下载失败: {msg[:100] if msg else 'unknown error'}")
        return False

def upload_to_bypy(local_path, remote_path):
    """上传文件到百度云"""
    if not check_bypy_auth():
        print(f"   百度云盘未认证，跳过上传")
        return False
    print(f"   上传至百度云: {remote_path}")
    success, msg = bypy_command(f"upload {local_path} {remote_path}")
    if success:
        print(f"   上传成功: {remote_path}")
        return True
    else:
        print(f"   上传失败: {msg[:100] if msg else 'unknown error'}")
        return False

def list_bypy_dir(remote_path):
    """列出百度云目录"""
    success, msg = bypy_command(f"list {remote_path}")
    if success:
        lines = msg.strip().split('\n')
        files = []
        for line in lines:
            if line and not line.startswith('[') and not line.startswith('<W>'):
                parts = line.split()
                if len(parts) >= 2:
                    files.append({'name': parts[0], 'isdir': 'DIR' in line})
        return files
    return []

def load_obsidian_kline_data(code):
    """从Obsidian加载K线数据"""
    print(f"\n检查Obsidian数据...")
    
    # 尝试多个可能的路径
    possible_paths = [
        OBSIDIAN_DIR / "stockdata" / code / f"{code}_各级别k线.md",
        OBSIDIAN_DIR / "stock" / code / f"{code}_各级别k线.md",
        OBSIDIAN_DIR / "stockdata" / code / f"{code}_k线数据.md",
    ]
    
    for obs_path in possible_paths:
        if obs_path.exists():
            print(f"   找到本地Obsidian数据: {obs_path}")
            try:
                with open(obs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content, obs_path
            except Exception as e:
                print(f"   读取失败: {e}")
    
    print(f"   本地Obsidian数据未找到")
    return None, None

def load_baidu_kline_data(code):
    """从百度云加载K线数据"""
    print(f"\n检查百度云K线数据...")
    
    # 使用subprocess直接获取原始字节
    import subprocess
    try:
        result = subprocess.run(
            ['bypy', 'list', f'/knowledge/stockdata/{code}'],
            capture_output=True,
            timeout=30
        )
        raw_output = result.stdout
    except Exception as e:
        print(f"   获取文件列表失败: {e}")
        return None
    
    baidu_files = {}
    
    # 在原始字节中查找 .md 文件
    # 格式: F filename.md size date hash
    for line in raw_output.split(b'\n'):
        if b'F ' in line and b'.md' in line and code.encode() in line:
            # 提取文件名（第一个空格分隔的字段）
            parts = line.split()
            if len(parts) >= 2:
                filename_bytes = parts[1]
                try:
                    filename = filename_bytes.decode('utf-8', errors='ignore')
                except:
                    filename = filename_bytes.decode('gbk', errors='ignore')
                
                # 识别周期 - 支持多种命名格式
                # 如: 日线级别k线.md, 日线K线.md, 30分钟K线.md, 5分钟K线.md, 1分钟K线.md
                # 字节码: 日线=\xc8\xd5\xcf\xdf, 级别=\xbc\xb6\xb1\xf0, K线=k\xcf\xdf
                if b'\xc8\xd5\xcf\xdf' in filename_bytes or '日线' in filename:
                    baidu_files['daily'] = filename
                elif b'\xce\xe5' in filename_bytes or '5' in filename:
                    baidu_files['5'] = filename
                elif b'\xc8\xfd' in filename_bytes or '30' in filename:
                    baidu_files['30'] = filename
                elif b'\xd2\xbb' in filename_bytes or ('1' in filename and '日' not in filename):
                    # 1分钟 = \xd2\xbb, 排除日线 (\xc8\xd5)
                    baidu_files['1'] = filename
    
    if baidu_files:
        print(f"   找到百度云K线文件: {baidu_files}")
        return baidu_files
    
    print(f"   未找到K线文件")
    return None

# ============ 数据源函数 ============

def get_data_itick(code, period):
    if code.upper() != 'XAUUSD':
        return None
    
    ktype = ITICK_KTYPE.get(period)
    if ktype is None:
        return None
    
    headers = {"accept": "application/json", "token": ITICK_TOKEN}
    params = {"region": "GB", "code": "XAUUSD", "kType": ktype, "limit": 500}
    
    try:
        response = requests.get(ITICK_API, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            return None
        
        data = response.json()
        if data.get('code', 0) != 0:
            return None
        
        bars = data.get('data', [])
        if not bars:
            return None
        
        klines = []
        for bar in bars:
            ts = bar['t']
            if ts > 1e12:
                ts = ts / 1000
            dt_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            klines.append({
                'datetime': dt_str,
                'open': float(bar['o']),
                'high': float(bar['h']),
                'low': float(bar['l']),
                'close': float(bar['c']),
                'volume': float(bar['v']),
            })
        
        return klines
    except Exception as e:
        return None

def get_data_akshare(code, period, is_index=False):
    try:
        import akshare as ak
        if period == 'daily':
            if is_index:
                symbol = f"sz{code}" if code.startswith('399') else f"sh{code}"
                df = ak.stock_zh_index_daily(symbol=symbol)
                if df is not None and len(df) > 0:
                    df = df.tail(365).sort_values('date')
                    return [{'datetime': str(row['date']), 'open': float(row['open']), 'high': float(row['high']), 'low': float(row['low']), 'close': float(row['close']), 'volume': float(row['volume'])} for _, row in df.iterrows()]
            else:
                df = ak.stock_zh_a_hist(symbol=code, period='daily', adjust='qfq')
                if df is not None and len(df) > 0:
                    df = df.tail(365).sort_values('日期')
                    return [{'datetime': str(row['日期']), 'open': float(row['开盘']), 'high': float(row['最高']), 'low': float(row['最低']), 'close': float(row['收盘']), 'volume': float(row['成交量'])} for _, row in df.iterrows()]
        else:
            if is_index:
                df = ak.index_zh_a_hist_min_em(symbol=code, period=period)
            else:
                df = ak.stock_zh_a_hist_min_em(symbol=code, period=period, adjust='qfq')
            if df is not None and len(df) > 0:
                df = df.tail(500).sort_values('时间')
                return [{'datetime': str(row['时间']), 'open': float(row['开盘']), 'high': float(row['最高']), 'low': float(row['最低']), 'close': float(row['收盘']), 'volume': float(row['成交量'])} for _, row in df.iterrows()]
        return None
    except Exception as e:
        print(f"  akshare获取{period}失败: {e}")
        return None


def get_data_futu(code, period):
    try:
        os.environ['FUTU_LOG'] = '0'
        os.environ['FUTU_LOG_LEVEL'] = '0'
        from futu import OpenQuoteContext, KLType
        from datetime import datetime, timedelta
        
        futu_code = f"SZ.{code}" if not ('.' in code) else code
        period_map = {'daily': KLType.K_DAY, '30': KLType.K_30M, '5': KLType.K_5M, '1': KLType.K_1M}
        
        if period not in period_map:
            return None
        
        if period == 'daily':
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        elif period == '30':
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        elif period == '5':
            start_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        else:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        with OpenQuoteContext(host='127.0.0.1', port=11111) as ctx:
            result = ctx.request_history_kline(
                futu_code, 
                ktype=period_map[period], 
                start=start_date,
                end=end_date,
                max_count=500
            )
            ret = result[0] if isinstance(result, tuple) else result
            data = result[1] if isinstance(result, tuple) and len(result) > 1 else None
            if ret == 0 and data is not None and len(data) > 0:
                return [{'datetime': str(row['time_key']), 'open': float(row['open']), 'high': float(row['high']), 'low': float(row['low']), 'close': float(row['close']), 'volume': float(row['volume'])} for _, row in data.iterrows()]
        return None
    except Exception as e:
        print(f"  futu获取{period}失败: {e}")
        return None


def get_data_tushare(code, period):
    try:
        import tushare as ts
        pro = ts.pro_api("38d141546ad7a95940b8f3ca3dcbdf5184b936c8ce517eeed9d647e6")
        ts_code = f"{code}.SZ" if code.startswith('3') or code.startswith('0') else f"{code}.SH"
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is not None and len(df) > 0:
            df = df.sort_values('trade_date')
            klines = [{'datetime': str(row['trade_date']), 'open': float(row['open']), 'high': float(row['high']), 'low': float(row['low']), 'close': float(row['close']), 'volume': float(row['vol']) * 100} for _, row in df.iterrows()]
            return klines
        return None
    except Exception as e:
        print(f"  tushare获取{period}失败: {e}")
        return None


def get_kline(code, period, is_index=False, use_cache=True):
    # 先检查缓存
    if use_cache:
        cached_data, cache_src = load_cache(code, period)
        if cached_data:
            return cached_data, cache_src
    
    # XAUUSD: 使用itick
    if code.upper() == 'XAUUSD':
        data = get_data_itick(code, period)
        if data:
            if use_cache: save_cache(code, period, data, 'itick')
            return data, 'itick'
        else:
            return None, 'none'
    
    # A股/港股: akshare > futu > tushare
    data = get_data_akshare(code, period, is_index)
    if data:
        if use_cache: save_cache(code, period, data, 'akshare')
        return data, 'akshare'
    
    data = get_data_futu(code, period)
    if data:
        if use_cache: save_cache(code, period, data, 'futu')
        return data, 'futu'
    
    data = get_data_tushare(code, period)
    if data:
        if use_cache: save_cache(code, period, data, 'tushare')
        return data, 'tushare'
    
    return None, 'none'


# ============ 缠论核心函数 ============

def find_fengxing(klines):
    if len(klines) < 5:
        return []
    fx = []
    for i in range(2, len(klines) - 2):
        if klines[i]['high'] > klines[i-1]['high'] and klines[i]['high'] > klines[i-2]['high'] and \
           klines[i]['high'] > klines[i+1]['high'] and klines[i]['high'] > klines[i+2]['high']:
            fx.append({'type': 'top', 'index': i, 'price': klines[i]['high'], 'datetime': klines[i]['datetime']})
        elif klines[i]['low'] < klines[i-1]['low'] and klines[i]['low'] < klines[i-2]['low'] and \
             klines[i]['low'] < klines[i+1]['low'] and klines[i]['low'] < klines[i+2]['low']:
            fx.append({'type': 'bottom', 'index': i, 'price': klines[i]['low'], 'datetime': klines[i]['datetime']})
    return fx

def merge_fengxing(fx):
    if len(fx) < 2:
        return fx
    merged = [fx[0]]
    for f in fx[1:]:
        last = merged[-1]
        if f['type'] == last['type']:
            if f['type'] == 'top' and f['price'] > last['price']:
                merged[-1] = f
            elif f['type'] == 'bottom' and f['price'] < last['price']:
                merged[-1] = f
        else:
            merged.append(f)
    return merged

def identify_bi(klines, fx):
    if len(fx) < 2:
        return []
    bis = []
    for i in range(len(fx) - 1):
        if fx[i+1]['index'] - fx[i]['index'] >= 5:
            bis.append({
                'start': fx[i], 'end': fx[i+1],
                'direction': 'down' if fx[i]['type'] == 'top' else 'up',
                'start_price': fx[i]['price'], 'end_price': fx[i+1]['price'],
                'change_pct': (fx[i+1]['price'] - fx[i]['price']) / fx[i]['price'] * 100
            })
    return bis

def find_zhongshu_v2(bis):
    if len(bis) < 3:
        return []
    zss = []
    for i in range(len(bis) - 2):
        b1, b2, b3 = bis[i], bis[i+1], bis[i+2]
        if b1['direction'] == b2['direction'] == b3['direction']:
            if b1['direction'] == 'up':
                lows = [b1['start_price'], b2['start_price'], b3['start_price']]
                highs = [b1['end_price'], b2['end_price'], b3['end_price']]
            else:
                highs = [b1['start_price'], b2['start_price'], b3['start_price']]
                lows = [b1['end_price'], b2['end_price'], b3['end_price']]
            zs_low, zs_high = max(lows), min(highs)
            if zs_high > zs_low:
                zss.append({'range': (zs_low, zs_high), 'direction': b1['direction'], 'start': b1['start']['datetime'], 'end': b3['end']['datetime'], 'bis': [b1, b2, b3]})
    return zss

def calculate_macd(klines, fast=12, slow=26, signal=9):
    closes = [k['close'] for k in klines]
    if len(closes) < slow + signal:
        return None
    ema_f = [sum(closes[:fast]) / fast]
    for i in range(fast, len(closes)):
        ema_f.append((closes[i] - ema_f[-1]) * 2 / (fast + 1) + ema_f[-1])
    ema_s = [sum(closes[:slow]) / slow]
    for i in range(slow, len(closes)):
        ema_s.append((closes[i] - ema_s[-1]) * 2 / (slow + 1) + ema_s[-1])
    min_len = min(len(ema_f), len(ema_s))
    dif = [ema_f[i] - ema_s[i] for i in range(min_len)]
    dea = [sum(dif[:signal]) / signal]
    for i in range(signal, len(dif)):
        dea.append((dif[i] - dea[-1]) * 2 / (signal + 1) + dea[-1])
    min_d = min(len(dif), len(dea))
    macd_hist = [(dif[i] - dea[i-min_d+len(dea)]) * 2 for i in range(min_d - len(dea) + 1, min_d)]
    return {'dif': dif[-1], 'dea': dea[-1], 'macd': macd_hist[-1] if macd_hist else 0, 'dif_series': dif, 'macd_hist_series': macd_hist, 'trend': 'up' if macd_hist[-1] > 0 else 'down' if macd_hist else 'unknown'}

def detect_beichi_v2(bis, macd_data):
    if not bis or len(bis) < 2 or not macd_data:
        return None
    last_bi = bis[-1]
    prev_same = None
    for b in reversed(bis[:-1]):
        if b['direction'] == last_bi['direction']:
            prev_same = b
            break
    if not prev_same:
        return None
    enter_pct, leave_pct = prev_same['change_pct'], last_bi['change_pct']
    if (enter_pct > 0 and leave_pct < 0) or (enter_pct < 0 and leave_pct > 0):
        return None
    if abs(leave_pct) >= abs(enter_pct):
        return None
    ratio = abs(leave_pct) / abs(enter_pct) if abs(enter_pct) > 0 else 1
    strength = 'strong' if ratio < 0.5 else 'weak'
    bc_type = 'bottom' if last_bi['direction'] == 'up' else 'top'
    return {'type': bc_type, 'strength': strength, 'enter_pct': abs(enter_pct), 'leave_pct': abs(leave_pct), 'ratio': ratio}

def judge_trend_v2(klines, bis, zss):
    if not bis:
        return 'unknown'
    current_price = klines[-1]['close']
    if zss:
        zs_low, zs_high = zss[-1]['range']
        if zs_low <= current_price <= zs_high:
            return 'consolidation'
        return 'up' if current_price > zs_high else 'down'
    else:
        if len(klines) >= 10:
            recent = [k['close'] for k in klines[-10:]]
            return 'up' if recent[-1] > recent[0] else 'down'
        return 'up' if bis[-1]['direction'] == 'up' else 'down'

def analyze_level_v2(klines, level_name, code='XAUUSD'):
    """缠论分析主函数 - 优先使用CZSC模块"""
    
    # 优先使用CZSC模块
    if CZSC_ANALYZER_AVAILABLE:
        try:
            result = analyze_level_czsc(klines, level_name, code)
            if result:
                # 转换为统一格式
                return {
                    'name': result.get('name', level_name),
                    'count': result.get('count', 0),
                    'current': result.get('current', 0),
                    'trend': result.get('trend', 'unknown'),
                    'bis': result.get('bi_list', [])[-5:] if result.get('bi_list') else [],
                    'zss': [result['zs']] if result.get('zs') else [],
                    'macd': result.get('macd'),
                    'beichi': result.get('beichi'),
                    'fx': result.get('fx_list', [])[-5:] if result.get('fx_list') else [],
                    '_raw': result,  # 保留原始结果
                }
        except Exception as e:
            print(f"   CZSC分析失败，降级到自定义实现: {e}")
    
    # 降级到自定义实现
    if not klines or len(klines) < 10:
        return None
    fx = find_fengxing(klines)
    fx_merged = merge_fengxing(fx)
    bis = identify_bi(klines, fx_merged)
    zss = find_zhongshu_v2(bis)
    macd = calculate_macd(klines)
    beichi = detect_beichi_v2(bis, macd)
    trend = judge_trend_v2(klines, bis, zss)
    return {'name': level_name, 'count': len(klines), 'current': klines[-1]['close'], 'trend': trend, 'bis': bis[-5:] if bis else [], 'zss': zss[-3:] if zss else [], 'macd': macd, 'beichi': beichi}

def calculate_fibonacci_levels(high, low, direction='down'):
    """
    计算斐波那契回撤位
    
    Args:
        high: 波段高点
        low: 波段低点
        direction: 'down' = 从高点下跌到低点(空头), 'up' = 从低点上漲到高点(多头)
    
    Returns:
        dict: 斐波那契回撤位
        - 上涨趋势(从low到high): 回撤位 = high - diff * percentage (在低点基础上回撤)
        - 下跌趋势(从high到low): 回撤位 = low + diff * percentage (在高电基础上回撤)
    """
    diff = high - low
    
    if direction == 'down':
        # 从高点跌到低点 = 反弹位 = low + diff * percentage
        # 例如: 从5602跌到4099, 反弹23.6% = 4099 + (5602-4099)*23.6% = 4454
        return {
            '23.6%': low + diff * 0.236,
            '38.2%': low + diff * 0.382,
            '50%': low + diff * 0.500,
            '61.8%': low + diff * 0.618,
            '78.6%': low + diff * 0.786,
        }
    else:
        # 从低点涨到高点 = 回撤位 = high - diff * percentage
        return {
            '23.6%': high - diff * 0.236,
            '38.2%': high - diff * 0.382,
            '50%': high - diff * 0.500,
            '61.8%': high - diff * 0.618,
            '78.6%': high - diff * 0.786,
        }

def find_high_low(klines, period=None):
    if period:
        klines = klines[-period:]
    return max(k['high'] for k in klines), min(k['low'] for k in klines)


# ============ 生成报告 ============

def calculate_ma(klines, periods=[5, 13, 34, 58]):
    """计算均线"""
    closes = [k['close'] for k in klines]
    mas = {}
    for p in periods:
        if len(closes) >= p:
            mas[f'MA{p}'] = sum(closes[-p:]) / p
    return mas

def get_zs_range(zs):
    """获取中枢区间，兼容两种格式"""
    if 'range' in zs:
        return get_zs_range(zs)[0], get_zs_range(zs)[1]
    else:
        return zs.get('zd', zs.get('low', 0)), zs.get('zg', zs.get('high', 0))
    mas = {}
    for p in periods:
        if len(closes) >= p:
            mas[f'MA{p}'] = sum(closes[-p:]) / p
    return mas

def generate_report(name, code, daily, m30, m5, m1):
    """生成完整分析报告 - 对标REPORT_SAMPLE格式"""
    today = datetime.now().strftime('%Y年%m月%d日 %H:%M')
    
    daily_a = analyze_level_v2(daily, '日线') if daily else None
    m30_a = analyze_level_v2(m30, '30分钟') if m30 else None
    m5_a = analyze_level_v2(m5, '5分钟') if m5 else None
    m1_a = analyze_level_v2(m1, '1分钟') if m1 else None
    
    # 计算均线
    daily_ma = calculate_ma(daily) if daily else {}
    
    # 获取关键价位（近100日用于中枢等分析）
    daily_high, daily_low = find_high_low(daily, period=100) if daily else (0, 0)
    
    # 斐波那契计算 - 使用历史大波段
    hist_high, hist_low = find_high_low(daily) if daily else (daily_high, daily_low)
    
    # 判断当前处于哪个阶段：
    # 当前价在历史大波段中的位置
    #   - 当前价 < 历史高低点的中位数 → 下跌后反弹阶段 → 斐波那契是压力位
    #   - 当前价 > 历史高低点的中位数 → 上涨后回调阶段 → 斐波那契是支撑位
    if daily and daily_a:
        current = daily[-1]['close']
        mid_price = (hist_high + hist_low) / 2
        fib_direction = 'down' if current < mid_price else 'up'
    else:
        fib_direction = 'down'
    
    # 斐波那契基于历史大波段计算
    fib = calculate_fibonacci_levels(hist_high, hist_low, direction=fib_direction) if daily else {}
    
    # 额外的：用户指定波段（如5602-4099）的斐波那契压力位
    # 用于下跌后反弹场景
    user_fib_high, user_fib_low = 5602, 4099  # 用户指定的下跌波段
    user_fib = calculate_fibonacci_levels(user_fib_high, user_fib_low, direction='down')
    
    report = [f"{'='*60}", f"  缠论多级别联立分析报告 v7（增强版）", f"  标的：{name}（{code}）", f"  时间：{today}", f"{'='*60}\n"]
    
    # ==================== 1. 核心结论 ====================
    report.append("### **核心结论**\n")
    
    if daily_a:
        # 趋势描述
        if daily_a['trend'] == 'up':
            trend_desc = f"当前{name}处于日线级别大幅上涨后的高位震荡格局"
        elif daily_a['trend'] == 'down':
            trend_desc = f"当前{name}处于日线级别下降趋势，空头格局"
        else:
            trend_desc = f"当前{name}处于日线级别盘整格局，方向不明"
        report.append(trend_desc + "。")
        
        # 背驰信号
        if daily_a['beichi']:
            bc = daily_a['beichi']
            if bc['type'] == 'top':
                bc_desc = '出现"上涨动能衰竭信号"，整体处于构筑大级别顶部的风险区域'
            else:
                bc_desc = '出现"下跌动能衰竭信号"，整体存在反弹机会'
            report.append(bc_desc + "。")
        
        # 30分钟中枢描述
        if m30_a and m30_a.get('zss'):
            zs = m30_a['zss'][-1]
            # 兼容两种格式：range=[low,high] 或 zd/zg
            if 'range' in zs:
                zs_low, zs_high = zs['range']
            else:
                zs_low = zs.get('zd', zs.get('low', 0))
                zs_high = zs.get('zg', zs.get('high', 0))
            report.append(f"30分钟级别上，价格围绕一个核心中枢（{zs_low:.0f}-{zs_high:.0f}）震荡，方向选择在即。")
        
        # 多级别联立总结
        report.append("多级别联立分析显示，后续走势需关注关键位置的突破情况。")
        
        # 战略方向
        if daily_a['trend'] == 'up' and daily_a['beichi']:
            report.append("战略上应以防范日线级别调整风险为主，")
        elif daily_a['trend'] == 'down':
            report.append("战略上应以观望或逢高做空为主，")
        else:
            report.append("战略上应以震荡行情对待，")
        
        report.append("操作上可进行中枢上下沿的高抛低吸，但需严格止损，并密切关注方向性突破。\n")
    
    # ==================== 2. 多级别缠论结构分析 ====================
    report.append("### **多级别缠论结构分析**\n")
    
    # ---- 日线分析 ----
    if daily_a:
        trend_str = '上涨趋势末端，动能衰竭' if daily_a['trend']=='up' else '下降趋势' if daily_a['trend']=='down' else '盘整格局'
        report.append(f"1. **日线级别：{trend_str}**\n")
        
        # 走势结构
        report.append("    - **走势结构**：")
        if daily_a['zss']:
            zs = daily_a['zss'][-1]
            zs_low, zs_high = get_zs_range(zs)
            report.append(f"自低点{find_high_low(daily, 250)[1]:.0f}以来，日线走出了")
            if daily_a['trend'] == 'up':
                report.append(f"一个强劲的上涨趋势。目前价格位于历史高位{daily_high:.0f}附近，最新价{daily_a['current']:.3f}。")
            else:
                report.append(f"一个下降趋势。目前价格{daily_a['current']:.3f}，从高点{daily_high:.0f}回调。")
            report.append(f"日线中枢区间【{zs_low:.3f}, {zs_high:.3f}】。")
        else:
            report.append(f"当前价格{daily_a['current']:.3f}，未形成明确中枢。")
        
        # 背驰分析
        report.append("\n    - **背驰分析**：")
        if daily_a['beichi']:
            bc = daily_a['beichi']
            bc_type = '上涨背驰' if bc['type'] == 'top' else '下跌背驰'
            strength = '强' if bc['strength'] == 'strong' else '弱'
            if bc['type'] == 'top':
                report.append(f"价格在{daily_high:.0f}创出新高，但下方MACD指标并未同步创出新高，DIFF值有走平回落迹象，红柱面积显著萎缩。这构成了 **[{bc_type}]（{strength}）**，预示着本段上涨趋势已进入尾声。")
            else:
                report.append(f"价格创出新低后，MACD指标绿柱面积萎缩，构成 **[{bc_type}]（{strength}）**，预示下跌动能衰竭。")
        else:
            report.append("暂无明确背驰信号。")
        
        # 均线与关键位
        report.append("\n    - **均线与关键位**：")
        if daily_ma:
            ma_str = "、".join([f"{k}={v:.3f}" for k, v in sorted(daily_ma.items())])
            report.append(f"价格位于均线上方，{ma_str}。")
            if 'MA5' in daily_ma:
                report.append(f"MA5（{daily_ma['MA5']:.3f}）可作为短期强弱分界线。")
        
        # MACD状态
        if daily_a['macd']:
            m = daily_a['macd']
            status = "多头" if m['macd'] > 0 else "空头"
            report.append(f"\n    - **MACD状态**：DIF={m['dif']:.3f}, DEA={m['dea']:.3f}, 柱={m['macd']:.3f}（{status}）")
    
    # ---- 30分钟分析 ----
    if m30_a:
        trend_str = '上升趋势' if m30_a['trend']=='up' else '下降趋势' if m30_a['trend']=='down' else '盘整格局'
        report.append(f"\n\n2. **30分钟级别：{trend_str}**\n")
        
        # 走势与中枢
        report.append("    - **走势与中枢**：")
        if m30_a['zss']:
            zs = m30_a['zss'][-1]
            report.append(f"30分钟级别中枢【{get_zs_range(zs)[0]:.3f}, {get_zs_range(zs)[1]:.3f}】，当前价格{m30_a['current']:.3f}。")
            # 判断位置
            if m30_a['current'] > get_zs_range(zs)[1]:
                report.append("价格位于中枢上方，")
            elif m30_a['current'] < get_zs_range(zs)[0]:
                report.append("价格位于中枢下方，")
            else:
                report.append("价格位于中枢内部，")
            report.append("该中枢是多空博弈的核心区域。")
        else:
            report.append(f"当前价格{m30_a['current']:.3f}，未形成明确中枢。")
        
        # 买卖点分析
        report.append("\n    - **买卖点分析**：")
        if m30_a['beichi']:
            bc = m30_a['beichi']
            bc_type = '底背驰' if bc['type'] == 'bottom' else '顶背驰'
            report.append(f"出现{bc_type}信号，可作为参考。")
        else:
            report.append("暂无明确买卖点信号。")
        
        # MACD
        if m30_a['macd']:
            m = m30_a['macd']
            status = "多头" if m['macd'] > 0 else "空头" if m['macd'] < 0 else "缠绕"
            report.append(f"\n    - **MACD状态**：DIF={m['dif']:.3f}, DEA={m['dea']:.3f}, 柱={m['macd']:.3f}（{status}）")
    
    # ---- 5分钟和1分钟分析 ----
    report.append("\n\n3. **5分钟与1分钟级别：为30分钟走势提供细节**\n")
    
    if m5_a:
        report.append("    - **5分钟级别**：")
        if m5_a['zss']:
            zs = m5_a['zss'][-1]
            report.append(f"中枢【{get_zs_range(zs)[0]:.3f}, {get_zs_range(zs)[1]:.3f}】，当前价格{m5_a['current']:.3f}。")
        else:
            report.append(f"当前价格{m5_a['current']:.3f}，未形成明确中枢。")
        report.append("这个级别的任务是观察能否形成对30分钟中枢上沿或下沿的有效突破。")
    
    if m1_a:
        report.append("\n    - **1分钟级别**：")
        report.append(f"提供最精确的买卖点信号，当前价格{m1_a['current']:.3f}。适合用于捕捉超短线的交易机会。")
    
    # ==================== 3. 关键位置与走势完全分类 ====================
    report.append("\n\n### **关键位置与走势完全分类**\n")
    
    report.append("**关键支撑/压力位整合**：\n")
    
    if daily_a and daily_a['zss']:
        zs = daily_a['zss'][-1]
        report.append(f"- **核心压力区**：{get_zs_range(zs)[1]:.3f} (日线中枢上轨)")
        if daily_high > 0:
            report.append(f" -> {daily_high:.3f} (历史高点)")
        report.append(f"\n- **核心支撑区**：{get_zs_range(zs)[0]:.3f} (日线中枢下轨)")
        if daily_ma and 'MA5' in daily_ma:
            report.append(f" -> {daily_ma['MA5']:.3f} (MA5)")
    
    if fib:
        if fib_direction == 'down':
            # 下跌后反弹阶段，斐波那契位是压力位
            report.append(f"\n- **斐波那契压力位（从高点{hist_high:.0f}下跌至低点{hist_low:.0f}，当前反弹）**：")
            report.append(f"    （计算方式：低点{hist_low:.0f} + 跌幅×比例，反弹至此位置遇阻）")
        else:
            # 上涨后回调阶段，斐波那契位是支撑位
            report.append(f"\n- **斐波那契支撑位（从低点{hist_low:.0f}上涨至高点{hist_high:.0f}，当前回调）**：")
            report.append(f"    （计算方式：高点{hist_high:.0f} - 涨幅×比例，回调至此位置获撑）")
        for level, price in sorted(fib.items()):
            level_type = "压力" if fib_direction == 'down' else "支撑"
            report.append(f"    - {level}{level_type}位：{price:.3f}")
        report.append(f"\n    （注：当前价格在{daily[-1]['close']:.0f}附近，短期核心博弈区间在日线中枢内）")
    
    # 额外输出用户指定波段（5602→4099下跌后反弹）的斐波那契压力位
    if user_fib and daily:
        current = daily[-1]['close']
        # 只有当前价在该波段范围内才显示
        if user_fib_low <= current <= user_fib_high:
            report.append(f"\n- **近期下跌波段斐波那契压力位（{user_fib_high:.0f}→{user_fib_low:.0f}，当前反弹中）**：")
            report.append(f"    （计算方式：低点{user_fib_low:.0f} + 跌幅×比例，反弹至此位置遇阻）")
            for level, price in sorted(user_fib.items()):
                marker = " ← 当前价附近" if abs(price - current) / current < 0.01 else ""
                report.append(f"    - {level}压力位：{price:.1f}{marker}")
            report.append(f"    （当前价{current:.1f}，已反弹至{(current-user_fib_low)/(user_fib_high-user_fib_low)*100:.1f}%位置）")
    
    # 走势完全分类
    report.append("\n\n**后续走势完全分类与推演**：\n")
    
    if daily_a and daily_a['zss']:
        zs = daily_a['zss'][-1]
        
        if daily_a['trend'] == 'up':
            # 分类一
            report.append(f"- **分类一：强势路径 - 向上突破，构筑第三类买点 (概率30%)**")
            report.append(f"    - **路径描述**：价格在当前位置震荡后，再次向上有效突破30分钟中枢上轨{get_zs_range(zs)[1]:.0f}，随后回踩不跌回{get_zs_range(zs)[1]:.0f}下方。")
            report.append(f"    - **缠论定位**：此回踩确认点将构成 **30分钟级别的第三类买点**，确认下跌趋势结束，并开启向新高{daily_high:.0f}甚至更高的上涨。")
            report.append(f"    - **操作意义**：对持仓者是持有或加仓信号；对空仓者是右侧追多介入点。")
            
            # 分类二
            report.append(f"\n- **分类二：震荡路径 - 中枢延伸 (概率50%)**")
            report.append(f"    - **路径描述**：价格继续在30分钟中枢【{get_zs_range(zs)[0]:.0f}， {get_zs_range(zs)[1]:.0f}】内震荡，无法形成有效突破。")
            report.append(f"    - **缠论定位**：30分钟走势中枢延伸，为中继形态。")
            report.append(f"    - **操作意义**：采取高抛低吸策略，在中枢上沿附近减仓或做空，在中枢下沿附近回补或做多。")
            
            # 分类三
            report.append(f"\n- **分类三：弱势路径 - 向下跌破，构筑第三类卖点 (概率20%)**")
            report.append(f"    - **路径描述**：价格向下跌破30分钟中枢下轨{get_zs_range(zs)[0]:.0f}，随后反弹无法重新站回{get_zs_range(zs)[0]:.0f}之上。")
            report.append(f"    - **缠论定位**：此反弹无法返回{get_zs_range(zs)[0]:.0f}的点位将构成 **30分钟级别的第三类卖点**，确认日线级别调整正式展开。")
            report.append(f"    - **操作意义**：是明确的离场或反手做空信号。")
        else:
            # 下降趋势的分类
            # 分类一
            report.append(f"- **分类一：弱势路径 - 继续下跌 (概率30%)**")
            report.append(f"    - **路径描述**：价格在当前位置震荡后，再次向下突破日线中枢下轨{get_zs_range(zs)[0]:.0f}，创出新低。")
            report.append(f"    - **缠论定位**：确认下降趋势延续，将考验前期低点{daily_low:.0f}。")
            report.append(f"    - **操作意义**：空头持有或加仓信号。")
            
            # 分类二
            report.append(f"\n- **分类二：震荡路径 - 中枢延伸 (概率50%)**")
            report.append(f"    - **路径描述**：价格继续在日线中枢【{get_zs_range(zs)[0]:.0f}， {get_zs_range(zs)[1]:.0f}】内震荡，无法形成有效突破。")
            report.append(f"    - **缠论定位**：日线走势中枢延伸，为中继形态。")
            report.append(f"    - **操作意义**：采取高抛低吸策略，在中枢上沿附近减仓或做空，在中枢下沿附近回补或做多。")
            
            # 分类三
            report.append(f"\n- **分类三：强势路径 - 向上突破，构筑第三类买点 (概率20%)**")
            report.append(f"    - **路径描述**：价格向上突破日线中枢上轨{get_zs_range(zs)[1]:.0f}，随后回踩不跌回{get_zs_range(zs)[1]:.0f}之下。")
            report.append(f"    - **缠论定位**：此回踩确认点将构成 **日线级别的第三类买点**，确认下跌趋势结束。")
            report.append(f"    - **操作意义**：是明确的抄底信号，空头止盈或反手做多。")
    
    # ==================== 4. 终极操作策略 ====================
    report.append("\n\n### **终极操作策略**\n")
    
    direction = "多头" if daily_a and daily_a['trend'] == 'up' else "空头" if daily_a and daily_a['trend'] == 'down' else "震荡"
    trend_text = "日线上升趋势" if daily_a and daily_a['trend'] == 'up' else "日线下降趋势" if daily_a and daily_a['trend'] == 'down' else "日线盘整格局"
    bias = "防范风险为主" if daily_a and daily_a['trend'] == 'up' else "观望或逢高做空为主" if daily_a and daily_a['trend'] == 'down' else "震荡对待"
    
    report.append(f"- **总体方向**：**{direction}思维**。鉴于{trend_text}，战略上应以{bias}。\n")
    
    if daily_a and daily_a['zss']:
        zs = daily_a['zss'][-1]
        
        report.append(f"- **操作区域与信号**：")
        report.append(f"    - **多头区域（激进）**：价格回踩至 **{get_zs_range(zs)[0]:.0f}-{get_zs_range(zs)[0]+50}** 区间，且1分钟/5分钟图出现底背驰信号时，可轻仓试多。")
        report.append(f"    - **空头区域（关键）**：价格反弹至 **{get_zs_range(zs)[1]-50}-{get_zs_range(zs)[1]:.0f}** 区间，且1分钟/5分钟图出现顶背驰信号时，可轻仓试空。\n")
        
        report.append(f"- **止损位置**：")
        report.append(f"    - 多单止损：有效跌破 **{get_zs_range(zs)[0]-30}** (中枢下轨下方少许)")
        report.append(f"    - 空单止损：有效升破 **{get_zs_range(zs)[1]+30}** (中枢上轨上方少许)\n")
        
        report.append(f"- **目标位**：")
        if daily_high > 0:
            report.append(f"    - 多单目标：看向中枢上沿 **{get_zs_range(zs)[1]:.0f}**，突破后可上看 **{daily_high:.0f}**")
            report.append(f"    - 空单目标：看向中枢下沿 **{get_zs_range(zs)[0]:.0f}**，跌破后可下看 **{daily_low:.0f}**")
    
    # 持仓者与空仓者应对
    report.append(f"\n- **持仓者与空仓者应对**：")
    if daily_a and daily_a['trend'] == 'up':
        report.append(f"    - **持仓者**：建议在价格反弹至中枢上沿区域时，**分批减仓**，锁定利润，降低仓位以应对不确定性。若持仓成本较低，可将止损上移至{get_zs_range(zs)[0]:.0f}，保护大部分利润。")
        report.append(f"    - **空仓者**：以**观望**和**短线区间交易**为主。不建议在当前位置盲目开仓。应耐心等待上述分类中的关键点位出现明确买卖信号后再行动。")
    elif daily_a and daily_a['trend'] == 'down':
        report.append(f"    - **持仓者**：建议在价格反弹至中枢上沿区域时，**分批减仓**，锁定利润。")
        report.append(f"    - **空仓者**：以**观望**和**短线区间交易**为主，等待反弹至中枢上沿后再介入。")
    
    # ==================== 5. 风险提示 ====================
    report.append("\n### **风险提示**\n")
    if daily_a and daily_a['trend'] == 'up' and daily_a['beichi']:
        report.append(f"- 当前处于历史高位，日线出现衰竭信号，**逆势（追涨）做多的风险远大于顺势（高抛）做空的风险**。")
    report.append("- 所有短线操作必须严格设置止损，防止中枢震荡后出现单边突破行情导致重大亏损。")
    report.append("- 本分析仅供学习参考，不构成投资建议。")
    report.append("- 市场有风险，投资需谨慎。")
    report.append("- 缠论分析需要多级别确认，单一级别信号不可靠。")
    
    # ==================== 6. 知识库更新 ====================
    report.append("\n\n### **（若适用）知识库更新**\n")
    if daily_a and daily_a['zss']:
        zs = daily_a['zss'][-1]
        report.append(f"_本次分析为针对{name}（{code}）的系统分析，建立了其当前")
        if daily_a['trend'] == 'up':
            report.append(f'"上涨趋势"及')
        elif daily_a['trend'] == 'down':
            report.append(f'"下降趋势"及')
        report.append(f'"日线中枢【{get_zs_range(zs)[0]:.0f}， {get_zs_range(zs)[1]:.0f}】"的关键结构认知。此结论将作为后续跟踪分析该品种的动态知识背景。_')
    
    report.append(f"\n{'='*60}")
    report.append(f"分析完成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"{'='*60}")
    
    return '\n'.join(report)


# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='缠论多级别联立分析 v7')
    parser.add_argument('--code', '-c', type=str, required=True, help='股票/指数代码')
    args = parser.parse_args()
    
    code = args.code.strip()
    is_index = code in ['399001', '399006', '399300', '000001', '000016', '000688', '000852']
    index_names = {'399006': '创业板指', '399001': '深证成指', '399300': '沪深300', '000001': '上证指数', '000016': '上证50', '000688': '科创50'}
    name = index_names.get(code, code)
    
    print(f"\n{'='*60}")
    print(f"  正在获取 {name}（{code}）数据...")
    print(f"  策略：缓存 → akshare → futu → tushare")
    print(f"{'='*60}\n")
    
    # 1. 尝试从百度云和本地Obsidian加载K线数据
    baidu_files = load_baidu_kline_data(code)  # 返回文件名列表
    obsidian_data, obsidian_path = load_obsidian_kline_data(code)
    
    # 整合数据（如果从百度云或Obsidian获取到数据）
    has_cloud_data = False
    if baidu_files:
        print(f"\n已从百度云获取到K线文件列表: {baidu_files}")
        has_cloud_data = True
    if obsidian_data:
        print(f"\n已从Obsidian获取到K线数据")
        has_cloud_data = True
    
    # 2. 获取实时K线数据（会自动与缓存对比，去重整合）
    print("获取日K数据...")
    daily, daily_src = get_kline(code, 'daily', is_index)
    print(f"   {'成功' if daily else '失败'} {len(daily) if daily else 0}根 (来源: {daily_src})\n")
    
    print("获取30分钟K数据...")
    m30, m30_src = get_kline(code, '30', is_index)
    print(f"   {'成功' if m30 else '失败'} {len(m30) if m30 else 0}根 (来源: {m30_src})\n")
    
    print("获取5分钟K数据...")
    m5, m5_src = get_kline(code, '5', is_index)
    print(f"   {'成功' if m5 else '失败'} {len(m5) if m5 else 0}根 (来源: {m5_src})\n")
    
    print("获取1分钟K数据...")
    m1, m1_src = get_kline(code, '1', is_index)
    print(f"   {'成功' if m1 else '失败'} {len(m1) if m1 else 0}根 (来源: {m1_src})\n")
    
    if not all([daily, m30, m5, m1]):
        missing = [n for n, d in [('日K', daily), ('30分钟K', m30), ('5分钟K', m5), ('1分钟K', m1)] if not d]
        print(f"\n{'='*60}")
        print(f"  分钟级数据获取失败，无法进行多级别联立分析")
        print(f"  失败数据：{', '.join(missing)}")
        print(f"{'='*60}")
        import sys
        sys.exit(1)
    
    # 3. 生成报告
    print("\n生成分析报告...\n")
    report = generate_report(name, code, daily, m30, m5, m1)
    print(report)
    
    # 4. 保存报告到本地Obsidian
    today_str = datetime.now().strftime('%Y-%m-%d')
    obsidian_stock_dir = OBSIDIAN_DIR / "stock" / today_str
    obsidian_stock_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = obsidian_stock_dir / f"{today_str}_{code}_缠论分析.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_path}")
    
    # 5. 上传报告到百度云
    print(f"\n{'='*60}")
    print(f"  上传报告到百度云...")
    print(f"{'='*60}")
    
    # 检查bypy是否已认证
    if check_bypy_auth():
        baidu_report_path = f"/knowledge/{today_str}/{today_str}_{code}_缠论分析.md"
        upload_to_bypy(str(report_path), baidu_report_path)
    else:
        print(f"   百度云盘未认证，跳过上传")
        print(f"   如需上传，请先运行 'bypy info' 完成认证")
        print(f"   授权链接: https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk")
    
    print(f"\n{'='*60}")
    print(f"  完成!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
