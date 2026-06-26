#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 itick.org API 获取XAUUSD真实K线数据
kType: 1=1分钟, 2=5分钟, 3=15分钟, 4=30分钟, 5=1小时, 8=日线
"""
import os
import sys
import requests
import json
import importlib.util as _ilu
from datetime import datetime

# 从 config.py 读取配置（支持 ITICK_TOKEN 环境变量覆盖）
_script_dir = os.path.dirname(os.path.abspath(__file__))
_cfg_spec = _ilu.spec_from_file_location(
    "chan_config", os.path.join(_script_dir, "config.py")
)
_cfg = _ilu.module_from_spec(_cfg_spec)
_cfg_spec.loader.exec_module(_cfg)

API_URL = _cfg.ITICK_API
API_TOKEN = _cfg.ITICK_TOKEN

# KType映射
KTYPE_MAP = {
    '1min': 1,
    '5min': 2,
    '15min': 3,
    '30min': 4,
    '60min': 5,
    'daily': 8,
}

def get_xauusd_data(ktype_name, limit=500):
    """获取XAUUSD数据"""
    
    ktype = KTYPE_MAP.get(ktype_name)
    if ktype is None:
        raise Exception(f"Unknown ktype: {ktype_name}")
    
    headers = {
        "accept": "application/json",
        "token": API_TOKEN
    }
    
    params = {
        "region": "GB",
        "code": "XAUUSD",
        "kType": ktype,
        "limit": limit
    }
    
    print(f"Fetching {ktype_name}...", end=' ')
    
    response = requests.get(API_URL, headers=headers, params=params, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")
    
    data = response.json()
    
    if data.get('code', 0) != 0:
        raise Exception(f"API Error: {data.get('msg')}")
    
    bars = data.get('data', [])
    
    if not bars:
        raise Exception("Empty data")
    
    # 转换格式: dict -> klines
    klines = []
    for bar in bars:
        ts = bar['t']
        if ts > 1e12:
            ts = ts / 1000
        dt_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        klines.append({
            'symbol': 'XAUUSD',
            'datetime': dt_str,
            'open': round(float(bar['o']), 4),
            'high': round(float(bar['h']), 4),
            'low': round(float(bar['l']), 4),
            'close': round(float(bar['c']), 4),
            'volume': round(float(bar['v']), 0),
            'amount': round(float(bar.get('tu', 0)), 0),
        })
    
    print(f"OK {len(klines)} bars (last: {klines[-1]['datetime']} close={klines[-1]['close']})")
    
    return klines

# 获取各周期数据
print("=" * 80)
print("XAUUSD Real Data from itick.org")
print("=" * 80)
print()

cache_dir = r"D:\QClawData\workspace\skills\chan-stock-analysis\scripts\cache"

data = {}

# 日线
print("1. Daily...", end=' ')
try:
    klines = get_xauusd_data('daily', limit=365)
    data['daily'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 60分钟
print("2. 60min...", end=' ')
try:
    klines = get_xauusd_data('60min', limit=500)
    data['60'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 30分钟
print("3. 30min...", end=' ')
try:
    klines = get_xauusd_data('30min', limit=500)
    data['30'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 15分钟
print("4. 15min...", end=' ')
try:
    klines = get_xauusd_data('15min', limit=500)
    data['15'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 5分钟
print("5. 5min...", end=' ')
try:
    klines = get_xauusd_data('5min', limit=500)
    data['5'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 1分钟
print("6. 1min...", end=' ')
try:
    klines = get_xauusd_data('1min', limit=500)
    data['1'] = klines
except Exception as e:
    print(f"FAILED: {e}")
    raise

# 保存
print()
print("Saving to cache...")
for period, klines in data.items():
    cache_file = f"{cache_dir}/XAUUSD_{period}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({'klines': klines}, f, indent=2, ensure_ascii=False)
    print(f"  OK {period}: {len(klines)} bars")

print()
print("=" * 80)
print("Done!")
print("=" * 80)
