#!/usr/bin/env python3
"""
清空所有自选股
"""
import os
from config import WATCHLIST_FILE


def clear_watchlist() -> bool:
    """清空自选股列表"""
    
    if not os.path.exists(WATCHLIST_FILE):
        print("📭 自选股已经为空")
        return False
    
    with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
        count = sum(1 for line in f if line.strip())
    
    # 清空文件
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        pass  # 写入空内容
    
    print(f"✅ 已清空 {count} 只股票")
    return True


if __name__ == "__main__":
    confirm = input("⚠️ 确定要清空所有自选股吗？(y/n): ")
    if confirm.lower() == 'y':
        clear_watchlist()
    else:
        print("❌ 已取消操作")
