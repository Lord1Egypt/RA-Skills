#!/usr/bin/env python3
"""
列出所有食品
"""

import os
import json
from datetime import datetime

def load_food_data():
    """加载食品数据"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    data_file = os.path.join(data_dir, 'food_data.json')
    
    if not os.path.exists(data_file):
        print("❌ 数据文件不存在，请先运行 init_data.py")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_all_foods():
    """列出所有食品"""
    data = load_food_data()
    if data is None:
        return
    
    today = datetime.now().date()
    
    print("=" * 80)
    print("📋 所有食品清单")
    print("=" * 80)
    
    if not data['foods']:
        print("\n📭 还没有添加任何食品。")
        print("使用 'python add_food.py' 命令添加食品。")
        return
    
    # 按过期日期排序
    sorted_foods = sorted(data['foods'], 
                         key=lambda x: datetime.strptime(x['expiry_date'], "%Y-%m-%d").date())
    
    for i, food in enumerate(sorted_foods, 1):
        try:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            
            # 确定状态图标
            if days_left < 0:
                status = "🔴 已过期"
            elif days_left <= 7:
                status = "🟡 即将过期"
            elif days_left <= 14:
                status = "🟠 注意"
            else:
                status = "🟢 安全"
            
            print(f"\n{i}. {food['name']} ({food['quantity']}个) {status}")
            print(f"   ID: {food['id']}")
            print(f"   生产日期: {food['production_date']}")
            print(f"   保质期: {food['expiry_days']} 天")
            print(f"   过期日期: {food['expiry_date']}")
            
            if days_left < 0:
                print(f"   已过期: {-days_left} 天")
            else:
                print(f"   剩余天数: {days_left} 天")
            
            print(f"   存放位置: {food['location']}")
            
            if food.get('notes'):
                print(f"   备注: {food['notes']}")
            
            print(f"   添加时间: {food['created_at'][:10]}")
            
        except ValueError:
            print(f"\n{i}. {food['name']} ⚠️ 日期格式错误")
            print(f"   过期日期: {food.get('expiry_date', '未知')}")
    
    # 统计信息
    print("\n" + "=" * 80)
    print("📊 统计信息:")
    print(f"   食品总数: {len(data['foods'])} 种")
    
    # 按状态统计
    expired = 0
    expiring_soon = 0
    warning = 0
    safe = 0
    
    for food in data['foods']:
        try:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            
            if days_left < 0:
                expired += 1
            elif days_left <= 7:
                expiring_soon += 1
            elif days_left <= 14:
                warning += 1
            else:
                safe += 1
        except ValueError:
            continue
    
    print(f"   🔴 已过期: {expired} 种")
    print(f"   🟡 一周内过期: {expiring_soon} 种")
    print(f"   🟠 两周内过期: {warning} 种")
    print(f"   🟢 安全: {safe} 种")
    
    print("\n💡 提示:")
    print("   使用 'python check_expiry.py' 检查过期状态")
    print("   使用 'python get_reminders.py' 获取提醒")
    print("   使用 'python add_food.py' 添加新食品")
    print("=" * 80)

def main():
    """主函数"""
    list_all_foods()

if __name__ == "__main__":
    main()