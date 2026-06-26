#!/usr/bin/env python3
"""
股票数据查询工具
使用新浪财经API获取A股、港股、美股数据
"""

import requests
import json
import sys

def get_stock_quote(code):
    """
    获取A股/港股/美股行情
    使用新浪财经API
    """
    code = code.strip().upper()
    
    # 判断市场并添加前缀
    if not code.startswith(('SH', 'SZ', 'HK', 'US')):
        if code.startswith('6') or code.startswith('5'):
            code = f"sh{code}"
        elif code.startswith('0') or code.startswith('3'):
            code = f"sz{code}"
    
    url = f"https://hq.sinajs.cn/list={code}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn',
    }
    
    try:
        response = requests.get(url, timeout=10, headers=headers)
        
        if response.status_code != 200:
            return {'error': f'HTTP错误: {response.status_code}'}
        
        data = response.text.strip()
        
        if 'v_hq_str' in data or '不存在' in data:
            return {'error': '股票代码不存在', 'code': code}
        
        # 解析数据
        # 格式: var hq_str_sh600519="名称,开盘价,昨日收盘价,...;"
        if '=' not in data:
            return {'error': '数据格式异常'}
        
        # 提取=号后面的内容
        parts = data.split('=')
        if len(parts) < 2:
            return {'error': '数据格式异常'}
        
        content = parts[1].strip().strip('";')
        values = content.split(',')
        
        if len(values) < 32:
            return {'error': '数据不完整', 'code': code}
        
        name = values[0]
        open_price = float(values[1]) if values[1] else 0
        yesterday_close = float(values[2]) if values[2] else 0
        current_price = float(values[3]) if values[3] else 0
        high_price = float(values[4]) if values[4] else 0
        low_price = float(values[5]) if values[5] else 0
        
        # 计算涨跌
        change = current_price - yesterday_close
        if current_price > 0 and yesterday_close > 0:
            change_percent = (change / yesterday_close) * 100
        else:
            change_percent = 0
        
        # 获取成交量和成交额
        # 注意: values[7]是当前价, values[8]是成交量(股), values[9]是成交额(元)
        try:
            volume_raw = values[8] if len(values) > 8 and values[8] else '0'
            volume = int(float(volume_raw))  # 成交量(股)
        except:
            volume = 0
        
        try:
            amount_raw = values[9] if len(values) > 9 and values[9] else '0'
            amount = float(amount_raw)  # 成交额(元)
        except:
            amount = 0
        
        # 获取时间
        date = values[30] if len(values) > 30 else ''
        time = values[31] if len(values) > 31 else ''
        
        # 判断市场
        market = 'A股'
        if code.startswith('sh'):
            market = '沪市A股'
            stock_code = code[2:].upper()
        elif code.startswith('sz'):
            market = '深市A股'
            stock_code = code[2:].upper()
        else:
            stock_code = code
        
        return {
            'code': stock_code,
            'name': name,
            'price': current_price,
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'volume': volume,
            'amount': amount,
            'market': market,
            'date': date,
            'time': time,
        }
        
    except Exception as e:
        return {'error': str(e)}

def format_stock_info(stock):
    """格式化股票信息"""
    if 'error' in stock:
        return f"❌ 获取失败: {stock['error']}"
    
    code = stock.get('code', '')
    name = stock.get('name', '')
    price = stock.get('price', 0)
    change = stock.get('change', 0)
    change_pct = stock.get('change_percent', 0)
    market = stock.get('market', '')
    
    emoji = '📈' if change >= 0 else '📉'
    sign = '+' if change >= 0 else ''
    
    info = f"""
{emoji} **{name}** ({code}) - {market}
━━━━━━━━━━━━━━━━
💰 当前价格: ¥{price:.2f}
📊 涨跌: {sign}{change:.2f} ({sign}{change_pct:.2f}%)
📈 最高: ¥{stock.get('high', 0):.2f}
📉 最低: ¥{stock.get('low', 0):.2f}
📦 成交量: {stock.get('volume', 0)/10000:.2f} 万股
💵 成交额: ¥{stock.get('amount', 0)/100000000:.2f} 亿元
⏰ {stock.get('date', '')} {stock.get('time', '')}
"""
    
    return info.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python stock.py <code>")
        print("Examples:")
        print("  python stock.py 600519      # A股-贵州茅台")
        print("  python stock.py 000001      # A股-平安银行")
        print("  python stock.py 300750      # A股-宁德时代")
        sys.exit(1)
    
    stock = get_stock_quote(sys.argv[1])
    print(format_stock_info(stock))

if __name__ == '__main__':
    main()
