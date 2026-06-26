#!/usr/bin/env python3
"""
列出所有自选股
"""
import sys
import os
from config import WATCHLIST_FILE


def list_stocks() -> bool:
    """显示当前自选股列表"""
    
    if not os.path.exists(WATCHLIST_FILE):
        print("📭 自选股列表为空")
        return False
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        stocks = [line.strip() for line in f if line.strip()]
    
    if not stocks:
        print("📭 自选股列表为空")
        return False
    
    print("📋 你的自选股:")
    print("=" * 50)
    print(f"{'序号':<6} {'代码':<10} {'名称':<20}")
    print("-" * 50)
    
    for i, stock in enumerate(stocks, 1):
        parts = stock.split('|')
        code = parts[0] if len(parts) >= 1 else "未知"
        name = parts[1] if len(parts) >= 2 else "未知"
        print(f"{i:<6} {code:<10} {name:<20}")
    
    print("=" * 50)
    print(f"共计 {len(stocks)} 只股票")
    
    return True


if __name__ == "__main__":
    list_stocks()
