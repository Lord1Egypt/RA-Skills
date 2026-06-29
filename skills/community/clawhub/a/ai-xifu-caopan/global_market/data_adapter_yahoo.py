#!/usr/bin/env python3
"""
📊 美股数据适配器 — Yahoo Finance 统一数据接口
=============================================
不管什么市场，数据到我这里都变成统一格式：
  {date, open, high, low, close, volume}

用法:
  python3 data_adapter_yahoo.py --symbol AAPL --days 30
  python3 data_adapter_yahoo.py --symbol TSLA --days 60 --indicator macd
  python3 data_adapter_yahoo.py --symbol ^DJI --index  (大盘指数用^前缀)
  python3 data_adapter_yahoo.py --symbol 0700.HK --days 20 (港股)
"""

import json
import sys
import os
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# Yahoo Finance API 端点（免费，无需 Key）
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start}&period2={end}&interval=1d&events=history"

def get_unix_timestamp(days_ago=30):
    """获取几天前的 Unix 时间戳"""
    target = datetime.now() - timedelta(days=days_ago)
    return int(target.timestamp())

def fetch_yahoo_data(symbol, days=30):
    """
    从 Yahoo Finance 拉取日线数据
    返回统一格式的列表
    """
    start_ts = get_unix_timestamp(days)
    end_ts = int(datetime.now().timestamp())
    
    url = YAHOO_CHART_URL.format(symbol=symbol, start=start_ts, end=end_ts)
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
        
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        quotes = result["indicators"]["quote"][0]
        
        # 统一格式输出
        unified = []
        for i in range(len(timestamps)):
            dt = datetime.fromtimestamp(timestamps[i])
            date_str = dt.strftime("%Y-%m-%d")
            
            o = quotes.get("open", [None])[i]
            h = quotes.get("high", [None])[i]
            l = quotes.get("low", [None])[i]
            c = quotes.get("close", [None])[i]
            v = quotes.get("volume", [None])[i]
            
            if o is None or c is None:
                continue  # 跳过空数据
            
            unified.append({
                "date": date_str,
                "open": round(o, 2),
                "high": round(h, 2),
                "low": round(l, 2),
                "close": round(c, 2),
                "volume": int(v) if v else 0
            })
        
        return unified
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 错误 {e.code}: {symbol}")
        if e.code == 404:
            print(f"   symbol '{symbol}' 不存在，试试不同的代码格式")
        return None
    except Exception as e:
        print(f"❌ 数据拉取失败: {e}")
        return None

def calculate_sma(data, period=5):
    """计算简单移动平均线"""
    closes = [d["close"] for d in data]
    sma = []
    for i in range(len(closes)):
        if i < period - 1:
            sma.append(None)
        else:
            sma.append(round(sum(closes[i-period+1:i+1]) / period, 2))
    return sma

def calculate_macd(data, fast=12, slow=26, signal=9):
    """
    计算 MACD
    简化版：用SMA替代EMA
    """
    closes = [d["close"] for d in data]
    if len(closes) < slow:
        return None, None, None
    
    # 简化的EMA计算
    def ema(values, period):
        k = 2 / (period + 1)
        result = [values[0]]
        for i in range(1, len(values)):
            result.append(values[i] * k + result[-1] * (1 - k))
        return result
    
    fast_ema = ema(closes, fast)
    slow_ema = ema(closes, slow)
    
    macd_line = [round(f - s, 2) for f, s in zip(fast_ema, slow_ema)]
    
    signal_line = ema(macd_line, signal)
    signal_line = [round(s, 2) for s in signal_line]
    
    histogram = [round(m - s, 2) for m, s in zip(macd_line, signal_line)]
    
    return macd_line, signal_line, histogram

def print_market_data(data, symbol):
    """打印行情数据"""
    if not data:
        return
    
    print(f"\n📊 {symbol} — 最近 {len(data)} 个交易日")
    print("=" * 60)
    print(f"{'日期':<12} {'开盘':<10} {'最高':<10} {'最低':<10} {'收盘':<10} {'成交量':<12}")
    print("-" * 60)
    
    # 打印最近10条
    for d in data[-15:]:
        vol = f"{d['volume']:,}" if d['volume'] > 0 else "-"
        print(f"{d['date']:<12} {d['open']:<10.2f} {d['high']:<10.2f} {d['low']:<10.2f} {d['close']:<10.2f} {vol:<12}")
    
    # 技术分析
    closes = [d["close"] for d in data]
    if closes:
        print(f"\n📈 技术指标:")
        print(f"  最高价: {max(closes):.2f}")
        print(f"  最低价: {min(closes):.2f}")
        print(f"  均价: {sum(closes)/len(closes):.2f}")
        print(f"  最新: {closes[-1]:.2f}")
        print(f"  涨幅: {((closes[-1] - closes[0]) / closes[0] * 100):.2f}% (近{len(data)}日)")
        
        # 5日/20日均线
        sma5 = calculate_sma(data, 5)
        sma20 = calculate_sma(data, 20)
        if sma5[-1] and sma20[-1]:
            print(f"  MA5: {sma5[-1]:.2f} | MA20: {sma20[-1]:.2f}")
            trend = "多头排列 📈" if sma5[-1] > sma20[-1] else "空头排列 📉"
            print(f"  均线趋势: {trend}")
        
        # MACD
        macd, signal, hist = calculate_macd(data)
        if macd:
            print(f"  MACD: {macd[-1]:.4f}")
            print(f"  Signal: {signal[-1]:.4f}")
            print(f"  柱状: {hist[-1]:.4f}")
            macd_trend = "金叉 🔵" if macd[-1] > signal[-1] else "死叉 🔴"
            print(f"  MACD状态: {macd_trend}")

def main():
    if len(sys.argv) < 2:
        print("📊 美股数据适配器 v1.0")
        print("\n用法:")
        print("  python3 data_adapter_yahoo.py --symbol AAPL --days 30")
        print("  python3 data_adapter_yahoo.py --symbol TSLA --days 60")
        print("  python3 data_adapter_yahoo.py --symbol ^DJI --index")
        print("  python3 data_adapter_yahoo.py --list-markets")
        print("\n热门美股代码:")
        print("  AAPL 苹果 | MSFT 微软 | GOOGL 谷歌 | AMZN 亚马逊")
        print("  TSLA 特斯拉 | NVDA 英伟达 | META Meta | JPM 摩根大通")
        print("  ^DJI 道指 | ^IXIC 纳指 | ^GSPC 标普500")
        return
    
    args = sys.argv[1:]
    
    if "--list-markets" in args:
        print("🌍 支持的市场代码示例:")
        print("  🇺🇸 美股: AAPL, MSFT, GOOGL, TSLA, NVDA, ^DJI, ^IXIC, ^GSPC")
        print("  🇭🇰 港股: 0700.HK (腾讯), 9988.HK (阿里), 1810.HK (小米)")
        print("  🇬🇧 英股: HSBA.L (汇丰), BP.L (BP石油)")
        print("  🇯🇵 日股: 9984.T (软银), 7203.T (丰田)")
        print("\n  PS：以上代码格式需跟Yahoo Finance一致")
        return
    
    symbol = None
    days = 30
    
    if "--symbol" in args:
        idx = args.index("--symbol") + 1
        if idx < len(args):
            symbol = args[idx]
    
    if "--days" in args:
        idx = args.index("--days") + 1
        if idx < len(args):
            try:
                days = int(args[idx])
            except:
                pass
    
    if symbol:
        data = fetch_yahoo_data(symbol, days)
        if data:
            print_market_data(data, symbol)
            
            # 保存为JSON以供后续分析使用
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cache")
            os.makedirs(output_dir, exist_ok=True)
            
            cache_file = os.path.join(output_dir, f"{symbol.replace('^', '')}_{datetime.now().strftime('%Y%m%d')}.json")
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 数据已缓存: {cache_file}")
        else:
            print(f"\n❌ 拉取 {symbol} 数据失败，请检查代码是否正确")
            print("   美股示例: AAPL, TSLA, MSFT")
            print("   港股示例: 0700.HK, 9988.HK")
            print("   指数示例: ^DJI, ^IXIC, ^GSPC")

if __name__ == "__main__":
    main()
