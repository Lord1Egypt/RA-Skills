#!/usr/bin/env python3
"""
查询虚拟币价格
支持 BTC、ETH 等主流币种
支持历史数据查询和趋势图生成
"""

import sys
import urllib.request
import urllib.error
import json
from urllib.parse import urlencode
from datetime import datetime, timedelta

# 币种名称映射
COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "BNB": "binancecoin",
    "SOL": "solana",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "DOT": "polkadot",
    "MATIC": "matic-network"
}

def get_crypto_price(symbol):
    """
    获取指定币种的当前价格信息
    
    Args:
        symbol: 币种代码，如 BTC、ETH
    
    Returns:
        dict: 包含价格信息的字典
    """
    symbol = symbol.upper()
    coin_id = COIN_MAP.get(symbol, symbol.lower())
    
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd,cny",
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }
    
    try:
        url = f"{api_url}?{urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if coin_id not in data:
                return None
            
            coin_data = data[coin_id]
            return {
                "symbol": symbol,
                "usd": coin_data.get("usd", 0),
                "cny": coin_data.get("cny", 0),
                "usd_24h_change": coin_data.get("usd_24h_change", 0),
                "market_cap_usd": coin_data.get("usd_market_cap", 0)
            }
            
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return {"error": "API 请求过于频繁，请稍后再试"}
        return {"error": f"HTTP 错误: {e.code}"}
    except Exception as e:
        return {"error": f"请求失败: {str(e)}"}

def get_crypto_history(symbol, days=3):
    """
    获取指定币种的历史价格数据
    
    Args:
        symbol: 币种代码
        days: 查询天数（默认3天）
    
    Returns:
        list: 包含历史价格的列表 [(timestamp, price), ...]
    """
    symbol = symbol.upper()
    coin_id = COIN_MAP.get(symbol, symbol.lower())
    
    api_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    
    try:
        url = f"{api_url}?{urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            prices = data.get("prices", [])
            
            # 转换为 (日期, 价格) 列表
            result = []
            for timestamp_ms, price in prices:
                date = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%m-%d")
                result.append((date, price))
            
            return result
            
    except Exception as e:
        return {"error": f"获取历史数据失败: {str(e)}"}

def generate_chart(symbol, days=3, output_path=None):
    """
    生成价格趋势图
    
    Args:
        symbol: 币种代码
        days: 天数
        output_path: 输出图片路径
    
    Returns:
        str: 图片保存路径
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # 非交互式后端
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        
        # 设置支持中文的字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except ImportError:
        return {"error": "未安装 matplotlib，请运行: pip3 install matplotlib"}
    
    symbol = symbol.upper()
    history = get_crypto_history(symbol, days)
    
    if isinstance(history, dict) and "error" in history:
        return history
    
    if not history:
        return {"error": "未获取到历史数据"}
    
    # 准备数据
    dates = [h[0] for h in history]
    prices = [h[1] for h in history]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制价格线
    ax.plot(dates, prices, marker='o', linewidth=2, markersize=8, color='#2ecc71')
    
    # 填充区域
    ax.fill_between(dates, prices, alpha=0.3, color='#2ecc71')
    
    # 设置标题和标签
    ax.set_title(f'{symbol} 价格趋势 ({days}天)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('价格 (USD)', fontsize=12)
    
    # 格式化 Y 轴价格
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 添加数据标签
    for i, (date, price) in enumerate(history):
        ax.annotate(f'${price:,.0f}', 
                   xy=(i, price), 
                   xytext=(0, 10), 
                   textcoords='offset points',
                   ha='center',
                   fontsize=9,
                   color='#27ae60')
    
    # 设置背景色
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    if output_path is None:
        output_path = f"/Users/admin/.openclaw/workspace/{symbol}_trend_{days}d.png"
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path

def format_price(price):
    """格式化价格显示"""
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    else:
        return f"${price:.4f}"

def format_market_cap(cap):
    """格式化市值显示"""
    if cap >= 1e12:
        return f"${cap/1e12:.2f}T"
    elif cap >= 1e9:
        return f"${cap/1e9:.2f}B"
    elif cap >= 1e6:
        return f"${cap/1e6:.2f}M"
    else:
        return f"${cap:,.0f}"

def print_current_price(symbol):
    """打印当前价格"""
    result = get_crypto_price(symbol)
    
    if result is None:
        print(f"错误: 未找到币种 {symbol}")
        return False
    
    if "error" in result:
        print(f"错误: {result['error']}")
        return False
    
    print(f"\n📊 {result['symbol']} 价格信息")
    print(f"{'='*40}")
    print(f"💵 美元价格: {format_price(result['usd'])}")
    print(f"💴 人民币价格: ¥{result['cny']:,.2f}")
    
    change = result['usd_24h_change']
    change_emoji = "📈" if change >= 0 else "📉"
    print(f"{change_emoji} 24h 涨跌: {change:+.2f}%")
    
    if result['market_cap_usd']:
        print(f"🏦 市值: {format_market_cap(result['market_cap_usd'])}")
    
    print(f"{'='*40}\n")
    return True

def print_history(symbol, days=3):
    """打印历史价格"""
    history = get_crypto_history(symbol, days)
    
    if isinstance(history, dict) and "error" in history:
        print(f"错误: {history['error']}")
        return False
    
    print(f"\n📈 {symbol.upper()} {days}天历史价格")
    print(f"{'='*40}")
    for date, price in history:
        print(f"  {date}: ${price:,.2f}")
    print(f"{'='*40}\n")
    return True

def generate_comparison_chart(symbols, days=3, output_path=None):
    """
    生成多币种对比趋势图
    
    Args:
        symbols: 币种代码列表，如 ['BTC', 'ETH']
        days: 天数
        output_path: 输出图片路径
    
    Returns:
        str: 图片保存路径
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        return {"error": "未安装 matplotlib，请运行: pip3 install matplotlib"}
    
    # 颜色方案
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    all_data = {}
    valid_symbols = []
    
    # 获取所有币种数据
    for i, symbol in enumerate(symbols):
        symbol = symbol.upper()
        history = get_crypto_history(symbol, days)
        
        if isinstance(history, dict) and "error" in history:
            print(f"⚠️ 跳过 {symbol}: {history['error']}")
            continue
        
        if not history:
            print(f"⚠️ 跳过 {symbol}: 无数据")
            continue
        
        all_data[symbol] = history
        valid_symbols.append(symbol)
    
    if not valid_symbols:
        return {"error": "没有有效的币种数据"}
    
    # 上图：价格趋势（原始价格）
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        dates = [h[0] for h in history]
        prices = [h[1] for h in history]
        color = colors[i % len(colors)]
        
        ax1.plot(dates, prices, marker='o', linewidth=2.5, markersize=8, 
                label=symbol, color=color)
        ax1.fill_between(dates, prices, alpha=0.15, color=color)
    
    ax1.set_title(f'Multi-Coin Price Trend ({days} Days)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend(loc='best', fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.set_facecolor('#f8f9fa')
    
    # 下图：涨跌幅对比（归一化到起始日）
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        dates = [h[0] for h in history]
        prices = [h[1] for h in history]
        color = colors[i % len(colors)]
        
        # 计算相对于起始日的涨跌幅
        start_price = prices[0]
        normalized = [(p / start_price - 1) * 100 for p in prices]
        
        ax2.plot(dates, normalized, marker='s', linewidth=2.5, markersize=7, 
                label=symbol, color=color)
    
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('Relative Change (%) from Start', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Change (%)', fontsize=12)
    ax2.legend(loc='best', fontsize=11, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_facecolor('#f8f9fa')
    
    # 添加涨跌幅标签
    for i, symbol in enumerate(valid_symbols):
        history = all_data[symbol]
        prices = [h[1] for h in history]
        start_price = prices[0]
        end_price = prices[-1]
        change = (end_price / start_price - 1) * 100
        
        color = colors[i % len(colors)]
        ax2.text(0.02, 0.95 - i*0.08, f'{symbol}: {change:+.2f}%', 
                transform=ax2.transAxes, fontsize=10, color=color,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    if output_path is None:
        symbols_str = '_'.join(valid_symbols)
        output_path = f"/Users/admin/.openclaw/workspace/{symbols_str}_comparison_{days}d.png"
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_path

def main():
    if len(sys.argv) < 2:
        print("用法: python3 crypto_price.py <币种代码> [选项]")
        print("\n选项:")
        print("  --current            查询当前价格（默认）")
        print("  --history N          查询 N 天历史价格")
        print("  --chart N            生成 N 天趋势图")
        print("  --compare COIN1,COIN2,...  对比多个币种")
        print("\n示例:")
        print("  python3 crypto_price.py BTC")
        print("  python3 crypto_price.py BTC --history 3")
        print("  python3 crypto_price.py BTC --chart 3")
        print("  python3 crypto_price.py BTC --compare BTC,ETH,SOL")
        print("\n支持: BTC, ETH, USDT, BNB, SOL, XRP, ADA, DOGE, DOT, MATIC")
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    
    # 解析参数
    if len(sys.argv) >= 3:
        option = sys.argv[2]
        
        if option == "--history":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            print_history(symbol, days)
        
        elif option == "--chart":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            print(f"正在生成 {symbol} {days}天趋势图...")
            result = generate_chart(symbol, days)
            
            if isinstance(result, dict) and "error" in result:
                print(f"错误: {result['error']}")
                sys.exit(1)
            
            print(f"✅ 趋势图已保存: {result}")
            
            # 同时显示当前价格
            print_current_price(symbol)
        
        elif option == "--compare":
            if len(sys.argv) < 4:
                print("错误: --compare 需要提供币种列表，如: BTC,ETH,SOL")
                sys.exit(1)
            
            symbols_str = sys.argv[3]
            symbols = [s.strip().upper() for s in symbols_str.split(',')]
            days = int(sys.argv[4]) if len(sys.argv) > 4 else 3
            
            print(f"正在生成 {', '.join(symbols)} 对比图 ({days}天)...")
            result = generate_comparison_chart(symbols, days)
            
            if isinstance(result, dict) and "error" in result:
                print(f"错误: {result['error']}")
                sys.exit(1)
            
            print(f"✅ 对比图已保存: {result}")
            
            # 显示所有币种当前价格
            print(f"\n📊 当前价格汇总")
            print(f"{'='*50}")
            for s in symbols:
                result_price = get_crypto_price(s)
                if result_price and "error" not in result_price:
                    change = result_price['usd_24h_change']
                    change_emoji = "📈" if change >= 0 else "📉"
                    print(f"{s}: ${result_price['usd']:,.2f} ({change_emoji} {change:+.2f}%)")
            print(f"{'='*50}\n")
        
        else:
            print(f"未知选项: {option}")
            sys.exit(1)
    else:
        # 默认查询当前价格
        print_current_price(symbol)

if __name__ == "__main__":
    main()
