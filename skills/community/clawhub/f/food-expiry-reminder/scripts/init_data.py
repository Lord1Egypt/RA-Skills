#!/usr/bin/env python3
"""
初始化食品数据文件
"""

import os
import json
from datetime import datetime

def init_food_data():
    """初始化food_data.json文件"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    data_file = os.path.join(data_dir, 'food_data.json')
    
    # 创建数据目录
    os.makedirs(data_dir, exist_ok=True)
    
    # 如果文件不存在，创建初始数据结构
    if not os.path.exists(data_file):
        initial_data = {
            "foods": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已创建数据文件: {data_file}")
        print(f"📁 数据目录: {data_dir}")
    else:
        print(f"📁 数据文件已存在: {data_file}")
    
    return data_file

if __name__ == "__main__":
    init_food_data()