#!/usr/bin/env python3
"""
添加股票到自选股列表
用法：python add_stock.py <股票代码> [股票名称]
"""
import sys
import os
from config import WATCHLIST_FILE


def add_stock(code: str, name: str = None) -> bool:
    """
    添加股票到自选股
    
    Args:
        code: 6 位股票代码 (如 600919)
        name: 股票名称 (可选，不填时自动获取)
    
    Returns:
        是否成功添加
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    
    # 读取现有列表
    stocks = []
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
            stocks = [line.strip() for line in f if line.strip()]
    
    # 检查是否已存在
    code_upper = code.upper()
    for stock in stocks:
        if stock.startswith(f"{code_upper}|"):
            print(f"✅ {code} 已在自选股中")
            return False
    
    # 如果没提供名称，使用代码本身作为名称
    stock_name = name if name else "未知"
    
    # 添加到列表并保存
    entry = f"{code_upper}|{stock_name}"
    stocks.append(entry)
    
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        for s in stocks:
            f.write(s + '\n')
    
    print(f"✅ 已添加：{code} - {stock_name}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python add_stock.py <股票代码> [股票名称]")
        print("\n示例:")
        print("  python add_stock.py 600919           # 只输入代码")
        print("  python add_stock.py 600919 江苏银行   # 指定名称")
        sys.exit(1)
    
    code = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 验证股票代码格式
    if not code.isdigit() or len(code) != 6:
        print(f"❌ 无效的股票代码格式：{code} (应为 6 位数字)")
        sys.exit(1)
    
    add_stock(code, name)
