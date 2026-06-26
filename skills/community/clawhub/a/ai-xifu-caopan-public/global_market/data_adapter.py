#!/usr/bin/env python3
"""
📊 全球数据适配器 v2.0 — 统一数据接口
============================================
统一数据格式输出，不管什么市场：
  {date, open, high, low, close, volume}

用法:
  python3 data_adapter.py --market 美股 --symbol AAPL --days 30
  python3 data_adapter.py --market A股 --symbol 600519 --days 20
  python3 data_adapter.py --market 美股 --real-time
"""

import json
import os
import sys
import subprocess
import re
from datetime import datetime, timedelta

# ============================================================
# 配置
# ============================================================
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
GS_SCRIPTS_DIR = os.path.expanduser("~/.openclaw/workspace/skills/guosen-finance-all/scripts")

# 国信API市场代码映射
GS_SET_CODE = {
    "美股": 74,
    "A股_上海": 1,
    "A股_深圳": 0,
    "港股": -1
}

# Yahoo/Sina 的代码映射（备用）
SYMBOL_MAP = {
    "美股": {
        "AAPL": "aapl",
        "MSFT": "msft",
        "GOOGL": "googl",
        "AMZN": "amzn",
        "TSLA": "tsla",
        "NVDA": "nvda",
        "META": "meta",
        "JPM": "jpm",
        "V": "v",
        "SPY": "spy",
        "QQQ": "qqq",
    },
    "指数": {
        "DJI": "^DJI",
        "IXIC": "^IXIC",
        "SPX": "^GSPC"
    }
}

# ============================================================
# 数据获取 — 国信API（主力）
# ============================================================
def get_gs_realtime(market, symbol):
    """国信API实时行情"""
    set_code = GS_SET_CODE.get(market, 74)
    script = os.path.join(GS_SCRIPTS_DIR, "gs_stock_market_query.py")
    
    try:
        result = subprocess.run(
            ["python3", script, "single_hq", "--code", symbol, "--set_code", str(set_code)],
            capture_output=True, text=True, timeout=20,
            env={**os.environ}
        )
        return result.stdout
    except Exception as e:
        return f"❌ 国信实时行情失败: {e}"

def get_gs_history(market, symbol, days=30):
    """国信API历史行情"""
    set_code = GS_SET_CODE.get(market, 74)
    script = os.path.join(GS_SCRIPTS_DIR, "gs_stock_market_query.py")
    
    try:
        result = subprocess.run(
            ["python3", script, "past_hq", "--code", symbol, "--set_code", str(set_code), "--want_nums", str(days)],
            capture_output=True, text=True, timeout=20,
            env={**os.environ}
        )
        return result.stdout
    except Exception as e:
        return f"❌ 国信历史行情失败: {e}"

# ============================================================
# 数据获取 — 新浪API（备用·美股实时）
# ============================================================
def get_sina_realtime(symbol_lower):
    """新浪接口获取美股实时"""
    import urllib.request
    url = f'https://hq.sinajs.cn/list=gb_{symbol_lower}'
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://finance.sina.com.cn/stock/usstock/',
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode('gbk')
        if '=' not in text:
            return None
        parts = text.split('"')[1].split(',')
        return {
            'name': parts[0],
            'price': float(parts[1]),
            'change': float(parts[2]),
            'time': parts[3],
            'chg_pct': float(parts[4]),
            'open': float(parts[5]),
            'high': float(parts[6]),
            'low': float(parts[7]),
            'pre_close': float(parts[8]),
            'high_52w': float(parts[9]),
            'volume': int(parts[11]) if parts[11] else 0,
            'market_cap': parts[13],
            'pe': parts[14],
        }
    except:
        return None

def get_stooq_realtime(symbol_lower):
    """Stooq备用行情"""
    import urllib.request, json
    url = f'https://stooq.com/q/l/?s={symbol_lower}.us&f=sd2t2ohlcvn&h&e=json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            s = data['symbols'][0]
            return {
                'name': s.get('name', symbol_lower.upper()),
                'price': float(s['close']),
                'open': float(s['open']),
                'high': float(s['high']),
                'low': float(s['low']),
                'volume': int(s['volume']),
                'source': 'stooq',
            }
    except:
        return None

# ============================================================
# 美股实时行情 — 智能获取（先国信，再新浪，再Stooq）
# ============================================================
def get_us_realtime(symbol):
    """美股实时行情智能获取"""
    symbol = symbol.upper()
    lower = SYMBOL_MAP["美股"].get(symbol, symbol.lower())
    
    print(f"📡 正在获取 {symbol} 实时行情...", file=sys.stderr)
    
    # 方案1: 国信API
    gs_data = get_gs_realtime("美股", symbol)
    if "❌" not in str(gs_data) and gs_data and len(gs_data) > 50:
        print(f"  ✅ 国信API", file=sys.stderr)
        return {"source": "guosen", "raw": gs_data, "symbol": symbol}
    
    # 方案2: 新浪
    sina = get_sina_realtime(lower)
    if sina:
        print(f"  ✅ 新浪财经", file=sys.stderr)
        sina["source"] = "sina"
        sina["symbol"] = symbol
        return sina
    
    # 方案3: Stooq
    stooq = get_stooq_realtime(lower)
    if stooq:
        print(f"  ✅ Stooq", file=sys.stderr)
        stooq["symbol"] = symbol
        return stooq
    
    return None

# ============================================================
# 美股统一行情展示（格式化输出）
# ============================================================
def display_us_realtime(data):
    """展示美股实时行情"""
    if not data:
        print("❌ 无法获取数据")
        return
    
    source = data.get("source", "unknown")
    
    if source == "sina":
        print(f"\n📊 {data['symbol']} ({data['name']}) — 实时行情")
        print("=" * 50)
        print(f"  最新价: ${data['price']:.2f}")
        print(f"  涨跌:   {data['chg_pct']:+.2f}% ({data['change']:+.2f})")
        print(f"  开盘:   ${data['open']:.2f}")
        print(f"  最高:   ${data['high']:.2f}")
        print(f"  最低:   ${data['low']:.2f}")
        print(f"  昨收:   ${data['pre_close']:.2f}")
        print(f"  成交量: {data['volume']:,}")
        print(f"  52周高: ${data['high_52w']:.2f}")
        if data['pe']:
            print(f"  市盈率: {data['pe']}")
        print(f"  数据源: 📡 新浪财经")
        
    elif source == "stooq":
        print(f"\n📊 {data['symbol']} — 实时行情")
        print("=" * 50)
        print(f"  最新价: ${data['price']:.2f}")
        print(f"  开盘:   ${data['open']:.2f}")
        print(f"  最高:   ${data['high']:.2f}")
        print(f"  最低:   ${data['low']:.2f}")
        print(f"  成交量: {data['volume']:,}")
        print(f"  数据源: 📡 Stooq")
        
    elif source == "guosen":
        print(f"\n📊 {data['symbol']} — 实时行情 (国信证券)")
        print("=" * 50)
        print(data.get("raw", "")[:500])

# ====================================================================
# 统一美股拉取 + 技术分析（给推理模型用）
# ====================================================================
def analyze_us_stock(symbol, days=30):
    """美股综合分析 — 统一数据格式输出"""
    # 获取实时行情
    realtime = get_us_realtime(symbol)
    
    # 获取历史数据
    history = get_gs_history("美股", symbol, days)
    
    return {
        "symbol": symbol,
        "realtime": realtime,
        "history_raw": history,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

# ============================================================
# 主入口
# ============================================================
def main():
    print("\n🌍 全球数据适配器 v2.0")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python3 data_adapter.py --market 美股 --symbol AAPL --realtime")
        print("  python3 data_adapter.py --market 美股 --symbol AAPL,TSLA,NVDA --realtime")
        print("  python3 data_adapter.py --market 美股 --symbol AAPL --history --days 30")
        print("  python3 data_adapter.py --list")
        print("\n热门美股:")
        for s, n in SYMBOL_MAP["美股"].items():
            print(f"  {s:<6} → {n}")
        return
    
    args = sys.argv[1:]
    
    if "--list" in args:
        print("\n🇺🇸 热门美股代码:")
        for s, n in SYMBOL_MAP["美股"].items():
            print(f"  {s:<6} ({n})")
        print("\n📈 指数代码:")
        for s, n in SYMBOL_MAP["指数"].items():
            print(f"  {s:<6} ({n})")
        return
    
    market = "美股"  # 当前只做了美股
    symbol = None
    
    if "--symbol" in args:
        idx = args.index("--symbol") + 1
        if idx < len(args):
            symbol = args[idx]
    
    if not symbol:
        print("❌ 请指定股票代码")
        return
    
    if "--realtime" in args or "-r" in args:
        # 支持多个代码用逗号分隔
        symbols = [s.strip().upper() for s in symbol.split(",")]
        for s in symbols[:5]:  # 最多5个
            data = get_us_realtime(s)
            display_us_realtime(data)
            print()

if __name__ == "__main__":
    main()
