#!/usr/bin/env python3
"""
自动类目查询模块
当用户未提供有效类目ID时，自动查询并显示所有一级类目
"""

import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.category import get_categories

def auto_list_all_categories():
    """自动列出所有一级类目（不省略）"""
    try:
        print("🔍 正在查询1688所有一级类目...")
        result = get_categories(0, 'en')
        
        if result.get('result', {}).get('success') == 'true':
            categories = result['result']['result']['children']
            print(f"\n📋 找到 {len(categories)} 个一级类目：")
            print("=" * 80)
            
            # 完整列出所有类目，不省略
            for category in categories:
                cate_id = category.get('categoryId', 'N/A')
                chinese_name = category.get('chineseName', 'N/A')
                english_name = category.get('translatedName', 'N/A')
                print(f"• ID: {cate_id:12} | 中文: {chinese_name:20} | 英文: {english_name}")
            
            print("=" * 80)
            print("💡 请使用上述类目ID进行商品榜单或热搜词查询")
            return categories
        else:
            print("❌ 获取类目列表失败")
            return []
            
    except Exception as e:
        print(f"❌ 自动类目查询失败: {e}")
        return []

if __name__ == "__main__":
    auto_list_all_categories()