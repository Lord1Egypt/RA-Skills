#!/usr/bin/env python3
"""
统一入口：检查所有平台限免游戏
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epic_free import get_epic_free_games, format_output as format_epic
from steam_free import get_steam_free_games, format_output as format_steam

def check_all():
    """检查所有平台"""
    print("🔍 正在查询限免游戏...\n")
    
    # Epic
    print(format_epic(get_epic_free_games()))
    print("\n")
    
    # Steam
    print(format_steam(get_steam_free_games()))
    print("\n✅ 查询完成！")

if __name__ == "__main__":
    check_all()
