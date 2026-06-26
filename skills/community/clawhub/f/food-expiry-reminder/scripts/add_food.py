#!/usr/bin/env python3
"""
添加新食品到数据库
"""

import os
import json
import sys
from datetime import datetime, timedelta
import uuid

def load_food_data():
    """加载食品数据"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    data_file = os.path.join(data_dir, 'food_data.json')
    
    if not os.path.exists(data_file):
        print("❌ 数据文件不存在，请先运行 init_data.py")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_food_data(data):
    """保存食品数据"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    data_file = os.path.join(data_dir, 'food_data.json')
    
    data['updated_at'] = datetime.now().isoformat()
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_food(name, production_date, expiry_days, location, quantity=1, notes=""):
    """添加新食品"""
    try:
        # 验证生产日期格式
        prod_date = datetime.strptime(production_date, "%Y-%m-%d")
        
        # 计算过期日期
        expiry_date = prod_date + timedelta(days=int(expiry_days))
        
        # 创建食品记录
        food_item = {
            "id": str(uuid.uuid4())[:8],  # 使用UUID前8位作为ID
            "name": name,
            "production_date": production_date,
            "expiry_days": int(expiry_days),
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "location": location,
            "quantity": int(quantity),
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 加载现有数据
        data = load_food_data()
        if data is None:
            return False
        
        # 添加新食品
        data['foods'].append(food_item)
        data['updated_at'] = datetime.now().isoformat()
        
        # 保存数据
        save_food_data(data)
        
        print(f"✅ 已添加食品: {name}")
        print(f"  生产日期: {production_date}")
        print(f"  保质期: {expiry_days}天")
        print(f"  过期日期: {expiry_date.strftime('%Y-%m-%d')}")
        print(f"  存放位置: {location}")
        print(f"  数量: {quantity}")
        if notes:
            print(f"  备注: {notes}")
        
        return True
        
    except ValueError as e:
        print(f"❌ 日期格式错误: {e}")
        print("请使用 YYYY-MM-DD 格式 (例如: 2024-03-04)")
        return False
    except Exception as e:
        print(f"❌ 添加食品时出错: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("使用方法: python add_food.py <名称> <生产日期> <保质期天数> <存放位置> [数量] [备注]")
        print("示例: python add_food.py \"牛奶\" \"2024-03-01\" 7 \"冰箱\" 2 \"全脂牛奶\"")
        return
    
    name = sys.argv[1]
    production_date = sys.argv[2]
    expiry_days = sys.argv[3]
    location = sys.argv[4]
    
    quantity = sys.argv[5] if len(sys.argv) > 5 else 1
    notes = sys.argv[6] if len(sys.argv) > 6 else ""
    
    add_food(name, production_date, expiry_days, location, quantity, notes)

if __name__ == "__main__":
    main()