#!/usr/bin/env python3
"""
测试 600323 股票数据
"""

import requests

def get_stock_data(code):
    """获取股票行情"""
    code = code.strip().upper()
    
    # 添加市场前缀
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
            print(f"❌ HTTP 错误：{response.status_code}")
            return None
        
        data = response.text.strip()
        print(f"原始数据：{data[:200]}...")
        
        if '=' not in data:
            print("❌ 数据格式错误")
            return None
        
        # 解析数据
        parts = data.split('=')
        if len(parts) < 2:
            print("❌ 数据解析失败")
            return None
        
        content = parts[1].strip().strip('";')
        values = content.split(',')
        
        if len(values) < 10:
            print("❌ 数据不完整")
            return None
        
        name = values[0]
        open_price = values[1]
        yesterday_close = values[2]
        current_price = values[3]
        high_price = values[4]
        low_price = values[5]
        
        print()
        print("=" * 50)
        print(f"📈 {name} ({code.upper()})")
        print("=" * 50)
        print(f"当前价格：¥{current_price}")
        print(f"开盘价：¥{open_price}")
        print(f"昨收：¥{yesterday_close}")
        print(f"最高：¥{high_price}")
        print(f"最低：¥{low_price}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

print("测试 600323 股票数据...")
print()
get_stock_data("600323")
