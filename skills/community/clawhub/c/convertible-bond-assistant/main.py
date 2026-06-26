#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债打新助手 - 主入口
免费工具，提供可转债申购日历、新债分析、溢价预测等功能
"""

import sys
import json
from datetime import datetime, timedelta
from cb_calendar import get_subscribable_cbs, get_cb_calendar
from cb_analysis import analyze_cb, compare_industry
from cb_premium_predict import predict_premium_rate
from cb_monitor import check_strong_redemption, check_downward_revision

# ============ 配置 ============
CACHE_FILE = "data/cb_history.csv"
CACHE_EXPIRE_MINUTES = 30

# ============ 主功能函数 ============

def get_today_subscribable():
    """获取今日可申购转债"""
    today = datetime.now().strftime("%Y-%m-%d")
    result = get_subscribable_cbs(today)
    return format_subscribable_output(result, today)

def get_week_subscribable():
    """获取本周可申购转债"""
    today = datetime.now()
    week_end = today + timedelta(days=7)
    result = get_cb_calendar(today.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d"))
    return format_calendar_output(result)

def analyze_new_cb(cb_code):
    """分析新债"""
    result = analyze_cb(cb_code)
    return format_analysis_output(result)

def predict_listing_premium(cb_code):
    """预测上市溢价率"""
    result = predict_premium_rate(cb_code)
    return format_premium_output(result)

def check_all_alerts():
    """检查所有提醒（强赎、下修）"""
    alerts = []
    
    # 强赎提醒
    strong_redemption = check_strong_redemption()
    if strong_redemption:
        alerts.extend(strong_redemption)
    
    # 下修提醒
    downward_rev = check_downward_revision()
    if downward_rev:
        alerts.extend(downward_rev)
    
    return format_alerts_output(alerts)

# ============ 格式化输出 ============

def format_subscribable_output(data, date):
    """格式化申购列表输出"""
    if not data:
        return f"今日 ({date}) 暂无可申购转债"
    
    lines = [f"📅 今日可申购转债 ({date})\n"]
    for i, cb in enumerate(data, 1):
        lines.append(f"{i}. {cb['name']} ({cb['code']})")
        lines.append(f"   - 发行规模：{cb['amount']}亿元")
        lines.append(f"   - 评级：{cb['rating']}")
        lines.append(f"   - 申购上限：{cb['max_subscribe']}万")
        lines.append(f"   - 正股：{cb['stock_name']} ({cb['stock_code']})")
        lines.append(f"   - 行业：{cb['industry']}")
        lines.append("")
    
    return "\n".join(lines)

def format_calendar_output(data):
    """格式化日历输出"""
    if not data:
        return "本周暂无可申购转债"
    
    lines = ["📆 本周可转债申购日历\n"]
    for item in data:
        lines.append(f"{item['date']}: {item['name']} ({item['code']})")
    
    return "\n".join(lines)

def format_analysis_output(data):
    """格式化分析结果输出"""
    lines = [
        f"📊 {data['name']} ({data['code']}) 分析",
        "",
        f"• 发行规模：{data['amount']}亿（{'小规模，易炒作' if data['amount'] < 10 else '中等规模'}）",
        f"• 转股价格：{data['convert_price']}元",
        f"• 正股 PE：{data['stock_pe']}倍（{data['stock_pe_level']}）",
        f"• 行业：{data['industry']}",
        f"• 评级：{data['rating']}",
        f"• 债券余额：{data['balance']}亿元",
        "",
        f"💡 建议：{data['recommendation']}",
    ]
    return "\n".join(lines)

def format_premium_output(data):
    """格式化溢价预测输出"""
    lines = [
        f"📈 {data['name']} 上市溢价预测",
        "",
        f"• 预测溢价率：{data['predicted_premium']}%",
        f"• 合理区间：{data['premium_range'][0]}% - {data['premium_range'][1]}%",
        f"• 预测上市价格：{data['predicted_price']}元",
        f"• 置信度：{data['confidence']}",
        "",
        f"📊 参考依据：",
        f"  - 同行业转债平均溢价：{data['industry_avg_premium']}%",
        f"  - 近 3 月新债平均溢价：{data['recent_avg_premium']}%",
        f"  - 正股估值水平：{data['stock_valuation']}",
    ]
    return "\n".join(lines)

def format_alerts_output(alerts):
    """格式化提醒输出"""
    if not alerts:
        return "✅ 暂无强赎/下修提醒"
    
    lines = ["⚠️ 重要提醒\n"]
    for alert in alerts:
        lines.append(f"• {alert['type']}: {alert['name']} ({alert['code']})")
        lines.append(f"  原因：{alert['reason']}")
        lines.append(f"  截止日：{alert['deadline']}")
        lines.append("")
    
    return "\n".join(lines)

# ============ CLI 入口 ============

def print_help():
    """打印帮助信息"""
    help_text = """
可转债打新助手 - 使用指南

命令:
  today          - 查询今日可申购转债
  week           - 查询本周可申购转债
  analyze <代码>  - 分析指定转债
  predict <代码>  - 预测上市溢价率
  alerts         - 查看强赎/下修提醒
  help           - 显示帮助信息

示例:
  python main.py today
  python main.py analyze 123205
  python main.py predict 123205
  python main.py alerts
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "today":
        print(get_today_subscribable())
    
    elif command == "week":
        print(get_week_subscribable())
    
    elif command == "analyze" and len(sys.argv) >= 3:
        cb_code = sys.argv[2]
        print(analyze_new_cb(cb_code))
    
    elif command == "predict" and len(sys.argv) >= 3:
        cb_code = sys.argv[2]
        print(predict_listing_premium(cb_code))
    
    elif command == "alerts":
        print(check_all_alerts())
    
    elif command == "help":
        print_help()
    
    else:
        print(f"未知命令：{command}")
        print_help()

if __name__ == "__main__":
    main()
