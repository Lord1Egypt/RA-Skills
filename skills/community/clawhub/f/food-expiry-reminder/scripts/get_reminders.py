#!/usr/bin/env python3
"""
获取一周内将过期的食品提醒
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

def get_weekly_reminders():
    """获取一周内将过期的食品提醒"""
    data = load_food_data()
    if data is None:
        return []
    
    today = datetime.now().date()
    one_week_later = today + timedelta(days=7)
    
    expiring_foods = []
    
    for food in data['foods']:
        try:
            expiry_date = datetime.strptime(food['expiry_date'], "%Y-%m-%d").date()
            
            # 只获取一周内将过期的食品
            if today <= expiry_date <= one_week_later:
                days_left = (expiry_date - today).days
                expiring_foods.append({
                    'food': food,
                    'days_left': days_left
                })
        except ValueError:
            continue
    
    # 按过期时间排序
    expiring_foods.sort(key=lambda x: x['days_left'])
    
    return expiring_foods

def main():
    """主函数"""
    print("=" * 60)
    print("🔔 一周内将过期的食品提醒")
    print("=" * 60)
    
    expiring_foods = get_weekly_reminders()
    
    if not expiring_foods:
        print("\n🎉 好消息！没有一周内将过期的食品。")
        print("所有食品都安全，可以放心食用。")
    else:
        print(f"\n⚠️  发现 {len(expiring_foods)} 种食品一周内将过期：")
        
        for item in expiring_foods:
            food = item['food']
            days_left = item['days_left']
            
            if days_left == 0:
                day_text = "今天过期"
            elif days_left == 1:
                day_text = "明天过期"
            else:
                day_text = f"{days_left} 天后过期"
            
            print(f"\n📌 {food['name']} ({food['quantity']}个)")
            print(f"   {day_text} - 过期日期: {food['expiry_date']}")
            print(f"   存放位置: {food['location']}")
            
            if food.get('notes'):
                print(f"   备注: {food['notes']}")
        
        print("\n💡 建议:")
        print("   1. 优先食用这些即将过期的食品")
        print("   2. 检查是否可以冷冻保存延长保质期")
        print("   3. 考虑分享给家人朋友")
        print("   4. 如果已变质，请及时丢弃")
    
    print("\n" + "=" * 60)
    print(f"📅 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()