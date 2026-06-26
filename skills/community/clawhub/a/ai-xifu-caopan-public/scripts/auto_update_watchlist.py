#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新关注列表脚本
当用户做任何股票方案时，询问用户是否将该股票加入早安报关注列表
"""

import os
import json
from datetime import datetime

# 配置文件路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHLIST_FILE = os.path.join(SKILL_DIR, "config/watchlist.json")
MAX_WATCHLIST_SIZE = 10  # 最多保留10只股票

# ============================================================
# 安全机制：所有修改关注列表的操作均需要用户确认
# 本脚本不会在无人确认的情况下自动修改关注列表
# ============================================================

def load_watchlist():
    """加载当前关注列表"""
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"stocks": [], "indices": []}

def save_watchlist(watchlist):
    """保存关注列表"""
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(watchlist, f, ensure_ascii=False, indent=2)

def get_set_code(code):
    """根据股票代码判断交易所"""
    if code.startswith('6'):
        return "1"  # 上海
    else:
        return "0"  # 深圳

def check_before_add(code, name):
    """
    在添加股票前检查并返回确认信息
    
    Args:
        code: 股票代码
        name: 股票名称
    
    Returns:
        dict: 包含确认所需的信息
    """
    watchlist = load_watchlist()
    
    # 检查是否已存在
    for stock in watchlist["stocks"]:
        if stock["code"] == code:
            return {
                "need_confirm": True,
                "action": "already_exists",
                "message": f"{name}({code})已在您的关注列表中，是否需要将其移到最前面？",
                "code": code,
                "name": name
            }
    
    # 检查是否超出上限
    if len(watchlist["stocks"]) >= MAX_WATCHLIST_SIZE:
        oldest = watchlist["stocks"][-1]
        return {
            "need_confirm": True,
            "action": "over_capacity",
            "message": f"关注列表已达上限({MAX_WATCHLIST_SIZE}只)。添加{name}({code})将移除最旧的{oldest['name']}({oldest['code']})，是否继续？",
            "code": code,
            "name": name,
            "will_remove": oldest
        }
    
    return {
        "need_confirm": True,
        "action": "add_new",
        "message": f"是否将{name}({code})添加到您的关注列表？(回复 是/否)",
        "code": code,
        "name": name
    }

def add_stock_to_watchlist(code, name, confirmed=False):
    """
    将股票添加到关注列表（需用户确认后调用）
    
    Args:
        code: 股票代码（如：000980）
        name: 股票名称（如：众泰汽车）
        confirmed: 是否已获得用户确认
    
    Returns:
        bool: 是否成功添加
    """
    if not confirmed:
        print(f"⚠️ 安全提示：添加 {name}({code}) 到关注列表需要用户确认。")
        return False
    
    watchlist = load_watchlist()
    
    # 检查是否已存在
    for stock in watchlist["stocks"]:
        if stock["code"] == code:
            watchlist["stocks"].remove(stock)
            watchlist["stocks"].insert(0, stock)
            save_watchlist(watchlist)
            print(f"✅ 已将 {name}({code}) 移到关注列表最前面")
            return True
    
    # 新股票，添加到最前面
    new_stock = {
        "code": code,
        "name": name,
        "set_code": get_set_code(code),
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    watchlist["stocks"].insert(0, new_stock)
    
    # 超过最大数量，移除最旧的
    if len(watchlist["stocks"]) > MAX_WATCHLIST_SIZE:
        removed = watchlist["stocks"].pop()
        print(f"⚠️ 已自动移除最旧的关注项：{removed['name']}({removed['code']})")
    
    save_watchlist(watchlist)
    print(f"✅ 已将 {name}({code}) 添加到关注列表")
    return True

def remove_stock_from_watchlist(code, confirmed=False):
    """从关注列表移除股票"""
    if not confirmed:
        return False
    
    watchlist = load_watchlist()
    
    for stock in watchlist["stocks"]:
        if stock["code"] == code:
            watchlist["stocks"].remove(stock)
            save_watchlist(watchlist)
            print(f"✅ 已将 {code} 从关注列表移除")
            return True
    
    print(f"⚠️ {code} 不在关注列表中")
    return False

def get_watchlist_summary():
    """获取关注列表摘要"""
    watchlist = load_watchlist()
    
    if not watchlist["stocks"]:
        return "当前关注列表为空"
    
    summary = "📋 当前关注列表：\n"
    for i, stock in enumerate(watchlist["stocks"], 1):
        summary += f"{i}. {stock['name']}({stock['code']})\n"
    
    return summary

def main():
    """主函数 - 用于命令行调用"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  检查添加: python auto_update_watchlist.py check <代码> <名称>")
        print("  确认添加: python auto_update_watchlist.py confirm_add <代码> <名称>")
        print("  移除股票: python auto_update_watchlist.py confirm_remove <代码>")
        print("  查看列表: python auto_update_watchlist.py list")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "check" and len(sys.argv) >= 4:
        code = sys.argv[2]
        name = sys.argv[3]
        result = check_before_add(code, name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "confirm_add" and len(sys.argv) >= 4:
        code = sys.argv[2]
        name = sys.argv[3]
        add_stock_to_watchlist(code, name, confirmed=True)
    elif action == "confirm_remove" and len(sys.argv) >= 3:
        code = sys.argv[2]
        remove_stock_from_watchlist(code, confirmed=True)
    elif action == "list":
        print(get_watchlist_summary())
    elif action == "add":
        # 旧接口保留但强制要求确认参数
        if "--force" in sys.argv:
            if len(sys.argv) >= 4:
                code = sys.argv[2]
                name = sys.argv[3]
                add_stock_to_watchlist(code, name, confirmed=True)
        else:
            print("❌ 错误：请使用 'check' 模式先获取用户确认")
            sys.exit(1)
    else:
        print("❌ 参数错误")
        sys.exit(1)

if __name__ == "__main__":
    main()
