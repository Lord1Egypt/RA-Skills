#!/usr/bin/env python3
"""
IHG技能健康检查脚本
检查技能响应时间、数据完整性和基本功能
"""

import sys
import os
import time
import json
sys.path.insert(0, '/home/node/.openclaw/scripts/ihg-monitor-python')

try:
    from query import execute_query
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def check_response_time():
    """检查响应时间"""
    test_cases = [
        {"query": "上海周边", "type": "hotels"},
        {"query": "优惠信息", "type": "hotels"},
        {"query": "", "type": "hotels", "distance_category": "上海市内"}
    ]
    
    print("⏱️  响应时间测试...")
    times = []
    
    for i, test in enumerate(test_cases, 1):
        try:
            start = time.time()
            result = execute_query(test)
            end = time.time()
            elapsed = (end - start) * 1000  # 毫秒
            times.append(elapsed)
            
            if "error" not in result.lower():
                print(f"  ✅ 测试{i}: {elapsed:.1f}ms - 查询 '{test.get('query', '默认')}' 成功")
            else:
                print(f"  ❌ 测试{i}: 查询失败 - {result[:100]}")
                return False
        except Exception as e:
            print(f"  💥 测试{i}: 异常 - {str(e)}")
            return False
    
    avg_time = sum(times) / len(times)
    print(f"📊 平均响应时间: {avg_time:.1f}ms")
    
    # 阈值检查
    if avg_time < 150:
        print("✅ 响应时间符合要求 (<150ms)")
        return True
    else:
        print(f"⚠️ 响应时间较长 ({avg_time:.1f}ms > 150ms)")
        return False

def check_data_integrity():
    """检查数据完整性"""
    print("\n📊 数据完整性检查...")
    
    hotels_file = '/home/node/.openclaw/scripts/ihg-monitor-python/hotels.json'
    try:
        with open(hotels_file, 'r', encoding='utf-8') as f:
            hotels = json.load(f)
        
        total = len(hotels)
        shanghai = sum(1 for h in hotels if h.get('city') == '上海')
        hualuxe = sum(1 for h in hotels if h.get('brand') == '华邑酒店')
        crowne = sum(1 for h in hotels if h.get('brand') == '皇冠假日酒店')
        
        print(f"  ✅ 酒店总数: {total}家")
        print(f"  ✅ 上海酒店: {shanghai}家 ({shanghai/total*100:.1f}%)")
        print(f"  ✅ 华邑酒店: {hualuxe}家 ({hualuxe/total*100:.1f}%)")
        print(f"  ✅ 皇冠假日: {crowne}家 ({crowne/total*100:.1f}%)")
        
        # 基本验证
        if total >= 40 and shanghai >= 8 and hualuxe >= 8 and crowne >= 8:
            print("✅ 数据完整性检查通过")
            return True
        else:
            print("❌ 数据完整性检查失败")
            return False
            
    except Exception as e:
        print(f"❌ 数据文件读取失败: {e}")
        return False

def main():
    print("🔍 IHG技能健康检查")
    print("=" * 50)
    
    # 运行检查
    time_ok = check_response_time()
    data_ok = check_data_integrity()
    
    print("\n" + "=" * 50)
    print("📋 检查总结:")
    
    if time_ok and data_ok:
        print("✅ 所有检查通过！技能状态健康")
        return 0
    else:
        print("❌ 部分检查失败，需要关注")
        return 1

if __name__ == "__main__":
    sys.exit(main())