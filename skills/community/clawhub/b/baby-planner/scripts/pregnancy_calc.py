#!/usr/bin/env python3
"""
孕周/预产期/易孕期计算器
用法: python3 pregnancy_calc.py 2026-01-15 [28]
     第二个参数为月经周期长度（默认28天）
"""

import sys
from datetime import datetime, timedelta

def calculate_pregnancy(lmp_str: str, cycle_length: int = 28):
    lmp = datetime.strptime(lmp_str, "%Y-%m-%d")
    today = datetime.today()

    # 预产期 (Naegele公式: LMP + 280天)
    edd = lmp + timedelta(days=280)

    # 当前孕周
    days_pregnant = (today - lmp).days
    weeks = days_pregnant // 7
    days = days_pregnant % 7

    # 排卵日 (假设周期28天，排卵在第14天)
    ovulation_day = lmp + timedelta(days=cycle_length // 2 - 1)
    fertile_start = ovulation_day - timedelta(days=5)
    fertile_end = ovulation_day + timedelta(days=1)

    # 孕中期/晚期分界
    second_trimester = lmp + timedelta(weeks=13)
    third_trimester = lmp + timedelta(weeks=27)

    # 孕周对应胎儿发育描述
    stage_info = {}
    for week in range(4, 41, 4):
        stage_info[week] = _get_fetal_description(week)

    print(f"\n{'='*40}")
    print(f"  📅 末次月经日期 (LMP): {lmp_str}")
    print(f"  📊 月经周期: {cycle_length} 天")
    print(f"{'='*40}")
    print(f"\n  🏥 预产期 (EDD): {edd.strftime('%Y-%m-%d')} ({edd.strftime('%A')})")
    print(f"     距今还有 {(edd - today).days} 天（约 {(edd - today).days // 7} 周）")
    print(f"\n  🤰 当前孕周: 孕 {weeks} 周 + {days} 天")
    print(f"     第 {weeks + 1} 周进行中")
    print(f"\n  🩺 所处阶段:")
    if today < second_trimester:
        print(f"     ✅ 孕早期 (0-13周)")
    elif today < third_trimester:
        print(f"     ✅ 孕中期 (14-27周)")
    else:
        remaining = (edd - today).days
        print(f"     ✅ 孕晚期 (28周+) — 还剩约 {remaining} 天")
    print(f"\n  💕 易孕期窗口:")
    print(f"     排卵日: {ovulation_day.strftime('%Y-%m-%d')}")
    print(f"     易孕期: {fertile_start.strftime('%Y-%m-%d')} ~ {fertile_end.strftime('%Y-%m-%d')}")
    print(f"\n  📝 近期产检提醒:")
    for week, desc in stage_info.items():
        target_date = lmp + timedelta(weeks=week)
        if target_date > today:
            days_until = (target_date - today).days
            print(f"     · 孕{week}周: {desc} （约{days_until}天后）")
            break

    print(f"\n{'='*40}\n")

def _get_fetal_description(week: int) -> str:
    descriptions = {
        4: "确认宫内孕，可见孕囊",
        8: "器官形成关键期，胎儿有心跳",
        12: "NT筛查时间窗，性别无法分辨",
        16: "唐筛/无创时间窗，可能感受到胎动",
        20: "大排畸B超，胎儿结构基本形成",
        24: "糖耐量试验，胎儿约西瓜大小",
        28: "进入孕晚期，开始数胎动",
        32: "小排畸，每2周产检一次",
        36: "足月临近，准备待产包",
        40: "预产期，胎儿已完全成熟",
    }
    return descriptions.get(week, "")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 pregnancy_calc.py 2026-01-15 [28]")
        sys.exit(1)
    cycle = int(sys.argv[2]) if len(sys.argv) > 2 else 28
    calculate_pregnancy(sys.argv[1], cycle)
