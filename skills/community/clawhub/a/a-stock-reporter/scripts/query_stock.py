#!/usr/bin/env python3
"""
A股个股查询脚本
支持单股/多股查询，自动识别市场
"""

import sys
import json
from typing import List, Dict, Optional

try:
    import easyquotation
except ImportError:
    print("❌ 请先安装依赖: pip install easyquotation")
    sys.exit(1)


def format_stock_data(code: str, data: Dict) -> str:
    """格式化个股数据为易读文本"""
    name = data.get('name', '未知')
    price = data.get('now', 0)
    close = data.get('close', price)
    change = data.get('change', 0)
    
    if close and close != 0:
        pct_change = (price - close) / close * 100
    else:
        pct_change = 0
    
    # 涨跌标识
    if pct_change > 0:
        trend = "📈"
        sign = "+"
    elif pct_change < 0:
        trend = "📉"
        sign = ""
    else:
        trend = "➡️"
        sign = ""
    
    # 格式化金额
    volume = data.get('volume', 0)
    amount = data.get('amount', 0)
    
    if volume >= 10000:
        volume_str = f"{volume/10000:.1f}万手"
    else:
        volume_str = f"{volume}手"
    
    if amount >= 100000000:
        amount_str = f"{amount/100000000:.1f}亿元"
    elif amount >= 10000:
        amount_str = f"{amount/10000:.1f}万元"
    else:
        amount_str = f"{amount}元"
    
    output = f"""
📈 {name} ({code})
━━━━━━━━━━━━━━━━━━━━
最新价: ¥{price:.2f}
涨跌幅: {sign}{pct_change:.2f}% {trend}
成交量: {volume_str}
成交额: {amount_str}
振幅: {data.get('amplitude', 0):.2f}%
涨跌额: {sign}{change:.2f}
"""
    return output.strip()


def get_stock_info(codes: List[str]) -> Dict:
    """获取股票信息"""
    quotation = easyquotation.use('sina')
    
    # 标准化代码格式
    formatted_codes = []
    for code in codes:
        code = code.strip()
        if len(code) == 6 and code.isdigit():
            formatted_codes.append(code)
        else:
            formatted_codes.append(code)
    
    try:
        result = quotation.stocks(formatted_codes)
        return result
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return {}


def main():
    if len(sys.argv) < 2:
        print("""
用法: python query_stock.py <股票代码1> [股票代码2] ...

示例:
  python query_stock.py 600519      # 查茅台
  python query_stock.py 600519 000858 300750  # 查多只股票
  
代码格式:
  个股: 600519 (茅台), 000858 (五粮液), 300750 (宁德时代)
  指数: sh000001 (上证), sz399001 (深证), sz399006 (创业板)
""")
        sys.exit(1)
    
    codes = sys.argv[1:]
    print(f"🔍 正在查询 {len(codes)} 只股票...\n")
    
    data = get_stock_info(codes)
    
    if not data:
        print("❌ 未获取到数据，请检查股票代码是否正确")
        sys.exit(1)
    
    for code in codes:
        code = code.strip()
        if code in data:
            print(format_stock_data(code, data[code]))
            print("\n" + "─" * 40 + "\n")
        else:
            print(f"⚠️ 未找到股票 {code} 的数据")


if __name__ == "__main__":
    main()
