#!/usr/bin/env python3
"""
从自选股移除股票
用法：python remove_stock.py <股票代码>
"""
import sys
import os
from config import WATCHLIST_FILE


def remove_stock(code: str) -> bool:
    """
    从自选股移除指定股票
    
    Args:
        code: 6 位股票代码
        
    Returns:
        是否成功移除
    """
    if not os.path.exists(WATCHLIST_FILE):
        print(f"❌ {code} 不在自选股中 (列表为空)")
        return False
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        stocks = [line.strip() for line in f if line.strip()]
    
    # 查找并删除
    found = False
    new_stocks = []
    
    for stock in stocks:
        parts = stock.split('|')
        if len(parts) >= 1 and parts[0].upper() == code.upper():
            found = True
        else:
            new_stocks.append(stock)
    
    if not found:
        print(f"❌ {code} 不在自选股中")
        return False
    
    # 保存更新后的列表
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        for stock in new_stocks:
            f.write(stock + '\n')
    
    print(f"✅ 已移除：{code}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python remove_stock.py <股票代码>")
        print("\n示例:")
        print("  python remove_stock.py 600919")
        sys.exit(1)
    
    code = sys.argv[1]
    
    if not code.isdigit() or len(code) != 6:
        print(f"❌ 无效的股票代码格式：{code}")
        sys.exit(1)
    
    remove_stock(code)
