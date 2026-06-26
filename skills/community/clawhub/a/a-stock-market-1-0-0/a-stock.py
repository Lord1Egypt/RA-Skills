#!/usr/bin/env python3
"""
A 股行情查询 - 使用腾讯财经免费 API
"""
import sys
import urllib.request

def get_stock_info(symbol):
    """获取股票信息 - 腾讯财经 API"""
    url = f"https://qt.gtimg.cn/q={symbol}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://stock.tencent.com/'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('gbk')
        
        # 解析：v_sh600519="1~ 贵州茅台~600519~1426.19~1440.11~..."
        if '~' in data:
            # 去掉开头的 v_xxxxxx="
            data = data.split('="')[1].strip('";')
            parts = data.split('~')
            
            if len(parts) >= 35:
                name = parts[1] if len(parts) > 1 else symbol
                current = float(parts[3]) if parts[3] else 0
                last_close = float(parts[4]) if parts[4] else 0
                open_price = float(parts[5]) if parts[5] else 0
                high = float(parts[33]) if len(parts) > 33 and parts[33] else 0
                low = float(parts[34]) if len(parts) > 34 and parts[34] else 0
                volume = float(parts[6]) if len(parts) > 6 and parts[6] else 0
                amount = float(parts[7]) if len(parts) > 7 and parts[7] else 0  # 成交额 (万)
                
                return {
                    'name': name,
                    'symbol': symbol,
                    'current': current,
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'volume': volume,
                    'amount': amount,  # 万
                    'last_close': last_close,
                }
    except Exception as e:
        return {'error': str(e)}
    
    return None

def format_change(current, last_close):
    """计算涨跌幅"""
    if last_close == 0:
        return 0
    return ((current - last_close) / last_close) * 100

def main():
    if len(sys.argv) < 2:
        print("用法：a-stock <股票代码> [代码 2] ...\n示例：a-stock sh600519 sz000858")
        sys.exit(1)
    
    symbols = sys.argv[1:]
    
    for symbol in symbols:
        info = get_stock_info(symbol)
        if info and 'error' not in info:
            change = format_change(info['current'], info['last_close'])
            change_str = f"{'+' if change >= 0 else ''}{change:.2f}%"
            arrow = "📈" if change >= 0 else "📉"
            
            print(f"{arrow} {info['name']} ({info['symbol']})")
            print(f"   现价：{info['current']:.2f}  {change_str}")
            print(f"   开盘：{info['open']:.2f}  最高：{info['high']:.2f}  最低：{info['low']:.2f}")
            print(f"   昨收：{info['last_close']:.2f}")
            print(f"   成交量：{info['volume']:.0f}手  成交额：{info['amount']:.0f}万")
            print()
        elif info and 'error' in info:
            print(f"❌ {symbol}: {info['error']}")
        else:
            print(f"❌ {symbol}: 无法获取数据")

if __name__ == '__main__':
    main()
