#!/usr/bin/env python3
"""
旅行规划报告生成脚本
整合小红书攻略和飞猪机票信息，生成完整的行程规划报告
"""

import sys
import json
import argparse
from datetime import datetime

def generate_report(travel_info, flight_info, from_city, output_format='markdown'):
    """
    生成整合报告
    
    Args:
        travel_info: 小红书攻略信息
        flight_info: 飞猪机票信息
        from_city: 出发城市
        output_format: 输出格式 (markdown/html/pdf)
    
    Returns:
        str: 格式化的报告
    """
    
    destination = travel_info.get('destination', '目的地')
    
    # 生成 Markdown 报告
    report = f"""# 🌟 {destination} 旅行规划

## 📖 小红书攻略精选

**最佳季节：** {travel_info.get('best_season', '待补充')}  
**推荐天数：** {travel_info.get('recommended_days', '待补充')}  
**预算参考：** {travel_info.get('budget_range', '待补充')}（不含机票）

### 🎯 必去景点
"""
    
    for i, highlight in enumerate(travel_info.get('highlights', []), 1):
        report += f"{i}. {highlight}\n"
    
    report += "\n### 🍜 美食推荐\n"
    for food in travel_info.get('food', []):
        report += f"- {food}\n"
    
    report += "\n### 🏨 住宿建议\n"
    for acc in travel_info.get('accommodation', []):
        report += f"- {acc}\n"
    
    # 添加机票信息
    if flight_info:
        report += f"""
### ✈️ 机票信息（飞猪）

**出发地：** {from_city}  
**目的地：** {destination}

| 去程 | 返程 | 价格 | 预订 |
|------|------|------|------|
| {flight_info.get('departure_flight', '待查询')} | {flight_info.get('return_flight', '待查询')} | ¥{flight_info.get('price', '待查询')} | [立即预订]({flight_info.get('booking_url', '#')}) |

💡 **价格提示：** {flight_info.get('tips', '提前预订更优惠')}
"""
    
    # 添加推荐行程
    if travel_info.get('itinerary'):
        report += "\n### 📝 推荐行程\n\n"
        for day, plan in enumerate(travel_info['itinerary'], 1):
            report += f"**Day {day}:** {plan}\n"
    
    # 添加预算汇总
    report += f"""
---
📊 攻略来源：小红书 Top 高赞笔记  
💰 总预算：{calculate_total_budget(travel_info, flight_info)}（含机票）
"""
    
    return report

def calculate_total_budget(travel_info, flight_info):
    """计算总预算"""
    budget_range = travel_info.get('budget_range', '0-0')
    flight_price = flight_info.get('price', 0) if flight_info else 0
    
    try:
        min_budget = int(budget_range.split('-')[0].replace('元', '').replace(',', ''))
        max_budget = int(budget_range.split('-')[1].replace('元', '').replace(',', ''))
        return f"¥{min_budget + flight_price:,}-{max_budget + flight_price:,}元"
    except:
        return "待计算"

def main():
    parser = argparse.ArgumentParser(description='生成旅行规划报告')
    parser.add_argument('--travel-info', '-t', required=True, help='攻略信息 JSON 文件')
    parser.add_argument('--flight-info', '-f', help='机票信息 JSON 文件')
    parser.add_argument('--from-city', '-c', required=True, help='出发城市')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    parser.add_argument('--format', choices=['markdown', 'html', 'pdf'], default='markdown')
    
    args = parser.parse_args()
    
    # 读取攻略信息
    with open(args.travel_info, 'r', encoding='utf-8') as f:
        travel_info = json.load(f)
    
    # 读取机票信息（可选）
    flight_info = None
    if args.flight_info:
        with open(args.flight_info, 'r', encoding='utf-8') as f:
            flight_info = json.load(f)
    
    # 生成报告
    report = generate_report(travel_info, flight_info, args.from_city, args.format)
    
    # 保存报告
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已生成：{args.output}")
    print("\n" + "="*50 + "\n")
    print(report)

if __name__ == '__main__':
    main()
