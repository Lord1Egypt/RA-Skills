#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
import pytz

def simple_recommend():
    """简单推荐测试"""
    tz = pytz.timezone('Asia/Shanghai')
    
    # 基础时间
    base = tz.localize(datetime(2026, 3, 17, 9, 0, 0))
    
    recommendations = []
    
    # 生成一些测试推荐
    days = ["周一", "周二", "周三", "周四", "周五"]
    for day_offset in range(5):
        for hour in [10, 14, 15]:  # 推荐的小时
            dt = base + timedelta(days=day_offset, hours=hour)
            end_dt = dt + timedelta(minutes=60)
            
            priority = 5
            if days[day_offset] in ["周二", "周三", "周四"]:
                priority += 2
            if hour == 10:  # 上午更好
                priority += 1
            
            recommendations.append({
                "start_time": dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "priority": priority,
                "weekday": days[day_offset],
                "time_of_day": "上午" if hour < 12 else "下午"
            })
    
    # 排序
    recommendations.sort(key=lambda x: x["priority"], reverse=True)
    
    return recommendations[:5]

if __name__ == "__main__":
    recs = simple_recommend()
    print(json.dumps({
        "success": True,
        "recommendations": recs
    }, ensure_ascii=False, indent=2))