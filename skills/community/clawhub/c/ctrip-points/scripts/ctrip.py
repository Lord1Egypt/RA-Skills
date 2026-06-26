#!/usr/bin/env python3
"""
携程积分助手 - 主脚本
用于查询积分余额、商品推荐等功能
"""

import os
import json
import sys
from datetime import datetime

# 数据目录
DATA_DIR = os.path.expanduser("~/.openclaw/data")
COOKIE_FILE = os.path.join(DATA_DIR, "ctrip-cookie.txt")
PRODUCTS_FILE = os.path.join(DATA_DIR, "ctrip-products.json")
POINTS_FILE = os.path.join(DATA_DIR, "ctrip-points.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

def load_products():
    """加载商品列表"""
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_products(products):
    """保存商品列表"""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def save_points(points_info):
    """保存积分信息"""
    with open(POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(points_info, f, ensure_ascii=False, indent=2)

def load_points():
    """加载积分信息"""
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_points():
    """获取积分余额"""
    points = load_points()
    if points and 'points' in points:
        return int(points['points'])
    return None

def get_points_display():
    """获取积分显示信息"""
    points = get_points()
    if points:
        # 估值约为积分的1%
        value = points * 0.01
        return points, value
    return None, None

def get_affordable_products():
    """获取买得起的商品"""
    points = get_points()
    if not points:
        return []
    
    products = load_products()
    affordable = [p for p in products if int(p['points']) <= points]
    affordable.sort(key=lambda x: int(x['points']), reverse=True)
    return affordable

def cmd_points():
    """查询积分"""
    points, value = get_points_display()
    if points:
        print(f"🎯 当前积分: {points:,}")
        print(f"💰 估值约: ¥{value:.2f}")
    else:
        print("❓ 还未设置积分")
        print("   使用: python ctrip.py set-points <数量>")

def cmd_products():
    """查看商品列表"""
    products = load_products()
    if not products:
        print("📦 商品列表为空，请先更新商品数据")
        return
    
    print("🎁 积分商城商品:")
    print("-" * 50)
    for p in products:
        print(f"  • {p['name']}")
        print(f"    所需积分: {p['points']}")
        print()

def cmd_affordable():
    """查看可兑换商品"""
    affordable = get_affordable_products()
    points = get_points()
    
    if not points:
        print("❓ 请先设置积分: python ctrip.py set-points <数量>")
        return
    
    if not affordable:
        print("😔 没有买得起的商品")
        return
    
    print(f"💡 你有 {points:,} 积分，可以兑换：")
    print("=" * 50)
    for i, p in enumerate(affordable[:10], 1):
        remaining = points - int(p['points'])
        print(f"{i}. {p['name']}")
        print(f"   所需积分: {p['points']} | 剩余: {remaining:,}")
        print()

def cmd_recommend():
    """推荐商品"""
    affordable = get_affordable_products()
    points = get_points()
    
    if not points:
        print("❓ 请先设置积分")
        return
    
    if not affordable:
        print("😔 没有买得起的商品")
        return
    
    print("🌟 为你推荐：")
    print("=" * 50)
    
    # 最贵的买得起
    if affordable:
        top = affordable[0]
        print(f"🏆 最贵可兑换: {top['name']}")
        print(f"   所需积分: {top['points']} | 剩余: {points - int(top['points']):,}")
        print()
    
    # 性价比高的（低积分高价值）
    print("💎 超值推荐（低积分兑换）：")
    for p in affordable[:5]:
        ratio = int(p['points']) / 100  # 简单估算
        print(f"  • {p['name']} - {p['points']}积分")

def cmd_set_points(args):
    """设置积分"""
    if not args:
        print("用法: python ctrip.py set-points <积分数量>")
        return
    
    try:
        points = int(args[0])
    except ValueError:
        print("错误: 请输入数字")
        return
    
    save_points({
        "points": points,
        "updated": datetime.now().isoformat()
    })
    print(f"✅ 已保存积分余额: {points:,}")

def cmd_add_product(args):
    """添加商品"""
    if len(args) < 2:
        print("用法: python ctrip.py add-product \"<商品名称>\" <积分>")
        return
    
    name = args[0]
    try:
        points = int(args[1])
    except ValueError:
        print("错误: 积分必须是数字")
        return
    
    products = load_products()
    new_id = f"prod_{len(products) + 1}"
    products.append({
        "id": new_id,
        "name": name,
        "points": str(points),
        "added": datetime.now().isoformat()
    })
    save_products(products)
    print(f"✅ 已添加: {name} - {points}积分")

def cmd_check_new():
    """检查新品（占位符）"""
    products = load_products()
    print(f"📦 当前商品数量: {len(products)}")
    print("🔄 检查新品需要访问积分商城页面")
    print("   手动更新请使用 add-product 命令")

def cmd_update():
    """更新数据（提示）"""
    print("📝 数据更新方式：")
    print("   1. 打开携程积分商城网页")
    print("   2. 使用 add-product 添加商品")
    print("   3. 使用 set-points 更新积分")

def main():
    if len(sys.argv) < 2:
        print("""
携程积分助手
============
用法: python ctrip.py <command>

命令:
  points        - 查询当前积分和估值
  products      - 查看所有商品列表
  affordable    - 查看买得起的商品
  recommend     - 推荐最值得兑换的商品
  set-points    - 设置积分余额
  add-product   - 添加商品到列表
  check-new     - 检查新品（占位）
  update        - 更新数据说明

示例:
  python ctrip.py points
  python ctrip.py recommend
  python ctrip.py set-points 39426
  python ctrip.py add-product \"商品名称\" 5000
""")
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "points":
        cmd_points()
    elif command == "products":
        cmd_products()
    elif command == "affordable":
        cmd_affordable()
    elif command == "recommend":
        cmd_recommend()
    elif command == "set-points":
        cmd_set_points(args)
    elif command == "add-product":
        cmd_add_product(args)
    elif command == "check-new":
        cmd_check_new()
    elif command == "update":
        cmd_update()
    else:
        print(f"未知命令: {command}")
        print("使用 python ctrip.py 查看帮助")

if __name__ == "__main__":
    main()
