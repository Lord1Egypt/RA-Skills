"""
Calculator - 预算计算逻辑
动态预算机制: 工作日/周末分开计算，过去超支/节省转嫁到剩余日预算
"""
import sys
import os
import datetime
sys.path.insert(0, os.path.dirname(__file__))

from config_manager import get_config, get_budget
from expense_manager import get_expenses, get_date_total

def get_days_info(year_month):
    """
    计算某月份每天是工作日还是周末
    返回: dict, {date: "weekday"|"weekend", ...}
    """
    y, m = map(int, year_month.split("-"))
    days = {}
    day = datetime.date(y, m, 1)
    while day.month == m:
        weekday = day.weekday()
        days[day.isoformat()] = "weekend" if weekday >= 5 else "weekday"
        day += datetime.timedelta(days=1)
    return days

def calculate_budget_status(month=None):
    """
    计算月度预算状态
    
    返回:
    {
        "month": "2026-04",
        "total_budget": 3300,
        "spent": 532.13,
        "remaining": 2767.87,
        "past": {
            "weekday": {"days": 2, "budget": 200, "spent": 200.7},
            "weekend": {"days": 1, "budget": 200, "spent": 240.7}
        },
        "remaining_period": {
            "weekday": {"days": 16, "original": 1600, "dynamic_daily": 100},
            "weekend": {"days": 6, "original": 1200, "dynamic_daily": 200}
        },
        "daily_status": [
            {"date": "2026-04-05", "type": "weekend", "budget": 200, "spent": 240.7, "status": "overspend", "daily_remaining": -40.7},
            ...
        ]
    }
    """
    if month is None:
        month = datetime.datetime.now().strftime("%Y-%m")
    
    config = get_config()
    budget_data = get_budget(month)
    
    # 获取预算规则
    weekday_budget = config.get("budget_rules", {}).get("weekday", 100)
    weekend_budget = config.get("budget_rules", {}).get("weekend", 200)
    dynamic_enabled = config.get("dynamic_budget", {}).get("enabled", True)
    
    # 月总预算
    total_budget = budget_data["total"] if budget_data else (weekday_budget * 22 + weekend_budget * 8)
    
    # 获取本月所有开销
    expenses = get_expenses(month)
    
    # 获取本月日期信息
    days_info = get_days_info(month)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 按日期统计
    daily_spent = {}
    for e in expenses:
        d = e["date"]
        daily_spent[d] = daily_spent.get(d, 0) + e["amount"]
    
    # 分离已过和剩余
    past_weekday_budget = 0
    past_weekend_budget = 0
    past_weekday_spent = 0
    past_weekend_spent = 0
    past_weekday_count = 0
    past_weekend_count = 0
    
    remaining_weekday_count = 0
    remaining_weekend_count = 0
    
    daily_status = []
    
    for date, day_type in sorted(days_info.items()):
        budget = weekday_budget if day_type == "weekday" else weekend_budget
        spent = daily_spent.get(date, 0)
        
        if date <= today:
            # 已过日期
            if day_type == "weekday":
                past_weekday_count += 1
                past_weekday_budget += weekday_budget
                past_weekday_spent += spent
            else:
                past_weekend_count += 1
                past_weekend_budget += weekend_budget
                past_weekend_spent += spent
            
            daily_status.append({
                "date": date,
                "type": day_type,
                "budget": budget,
                "spent": spent,
                "status": "overspend" if spent > budget else ("saved" if spent < budget else "exact"),
                "daily_remaining": budget - spent
            })
        else:
            # 剩余日期
            if day_type == "weekday":
                remaining_weekday_count += 1
            else:
                remaining_weekend_count += 1
    
    # 计算动态日预算
    remaining_weekday_budget = total_budget * (weekday_budget * 22 / (weekday_budget * 22 + weekend_budget * 8)) - past_weekday_budget
    remaining_weekend_budget = total_budget * (weekend_budget * 8 / (weekday_budget * 22 + weekend_budget * 8)) - past_weekend_budget
    
    # 历史超支/节省
    weekday_diff = past_weekday_budget - past_weekday_spent
    weekend_diff = past_weekend_budget - past_weekend_spent
    
    if dynamic_enabled:
        if remaining_weekday_count > 0:
            dynamic_weekday = (remaining_weekday_budget + weekday_diff) / remaining_weekday_count
        else:
            dynamic_weekday = 0
        
        if remaining_weekend_count > 0:
            dynamic_weekend = (remaining_weekend_budget + weekend_diff) / remaining_weekend_count
        else:
            dynamic_weekend = 0
    else:
        dynamic_weekday = weekday_budget
        dynamic_weekend = weekend_budget
    
    total_spent = past_weekday_spent + past_weekend_spent
    total_remaining = total_budget - total_spent
    
    return {
        "month": month,
        "total_budget": total_budget,
        "spent": total_spent,
        "remaining": total_remaining,
        "past": {
            "weekday": {
                "days": past_weekday_count,
                "budget": past_weekday_budget,
                "spent": past_weekday_spent
            },
            "weekend": {
                "days": past_weekend_count,
                "budget": past_weekend_budget,
                "spent": past_weekend_spent
            }
        },
        "remaining_period": {
            "weekday": {
                "days": remaining_weekday_count,
                "original": remaining_weekday_budget,
                "dynamic_daily": round(dynamic_weekday, 2)
            },
            "weekend": {
                "days": remaining_weekend_count,
                "original": remaining_weekend_budget,
                "dynamic_daily": round(dynamic_weekend, 2)
            }
        },
        "daily_status": daily_status
    }

if __name__ == "__main__":
    import json
    result = calculate_budget_status("2026-04")
    print(json.dumps(result, indent=2, ensure_ascii=False))
