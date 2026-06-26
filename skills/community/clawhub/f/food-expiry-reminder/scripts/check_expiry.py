#!/usr/bin/env python3
"""
检查食品过期状态
"""

import os
import json
from datetime import datetime, timedelta

def load_food_data():
    """加载食品数据"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    data_file = os.path.join(data_dir, 'food_data.json')
    
    if not os.path.exists(data_file):
        print("❌ 数据文件不存在，请先运行 init_data.py")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_expiry_status():
    """检查所有食品的过期状态"""
    data = load_food_data()
    if data is None:
        return
    
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    two_weeks_later = today + timedelta(days=14)
    
    expired_foods = []
    expiring_soon_foods = []  # 一周内过期
    expiring_later_foods = []  # 两周内过期
    safe_foods = []
    
    for food in data['foods']:
        try:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            
            if expiry_date < today:
                expired_foods.append(food)
            elif expiry_date <= one_week_later:
                expiring_soon_foods.append(food)
            elif expiry_date <= two_weeks_later:
                expiring_later_foods.append(food)
            else:
                safe_foods.append(food)
        except ValueError:
            print(f"⚠️  食品 '{food.get('name', '未知')}' 的过期日期格式错误: {food.get('expiry_date')}")
    
    # 打印结果
    print("=" * 60)
    print("📊 食品过期状态检查")
    print(f"📅 检查日期: {today.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    if expired_foods:
        print("\n🔴 已过期的食品:")
        for food in expired_foods:
            days_overdue = (today - datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()).days
            print(f"   • {food['name']} ({food['quantity']}个) - 过期 {days_overdue} 天")
            print(f"     位置: {food['location']}, 过期日期: {food['expiry_date']}")
    
    if expiring_soon_foods:
        print("\n🟡 一周内将过期的食品:")
        for food in expiring_soon_foods:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            print(f"   • {food['name']} ({food['quantity']}个) - {days_left} 天后过期")
            print(f"     位置: {food['location']}, 过期日期: {food['expiry_date']}")
    
    if expiring_later_foods:
        print("\n🟠 两周内将过期的食品:")
        for food in expiring_later_foods:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            print(f"   • {food['name']} ({food['quantity']}个) - {days_left} 天后过期")
            print(f"     位置: {food['location']}, 过期日期: {food['expiry_date']}")
    
    if safe_foods:
        print("\n🟢 安全的食品 (两周后过期):")
        for food in safe_foods:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            print(f"   • {food['name']} ({food['quantity']}个) - {days_left} 天后过期")
            print(f"     位置: {food['location']}")
    
    # 统计信息
    print("\n" + "=" * 60)
    print("📈 统计信息:")
    print(f"   总计食品: {len(data['foods'])} 种")
    print(f"   已过期: {len(expired_foods)} 种")
    print(f"   一周内过期: {len(expiring_soon_foods)} 种")
    print(f"   两周内过期: {len(expiring_later_foods)} 种")
    print(f"   安全: {len(safe_foods)} 种")
    print("=" * 60)
    
    # 返回提醒信息
    reminders = []
    if expired_foods:
        reminders.append(f"有 {len(expired_foods)} 种食品已过期，请立即处理！")
    if expiring_soon_foods:
        reminders.append(f"有 {len(expiring_soon_foods)} 种食品一周内将过期，请优先食用！")
    
    return reminders

def main():
    """主函数"""
    reminders = check_expiry_status()
    
    if reminders:
        print("\n🔔 提醒:")
        for reminder in reminders:
            print(f"   • {reminder}")

if __name__ == "__main__":
    main()