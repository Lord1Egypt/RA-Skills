#!/usr/bin/env python3
"""
gaokao-tutor: 备考计划生成脚本
用法:
  python3 study_plan.py --days 90 --weak 数学 物理 --strong 英语 语文 --type 新高考
"""

import argparse
import json
from datetime import date, timedelta


def get_phase(days):
    if days > 120:
        return "基础巩固期", "梳理所有知识点，消灭知识盲区"
    elif days > 60:
        return "专项突破期", "攻克薄弱科目，大量刷专项真题"
    else:
        return "综合冲刺期", "全真模拟 + 查漏补缺 + 调整备考状态"


def get_daily_hours(subject, is_weak):
    if is_weak:
        return 90  # 分钟
    else:
        return 30  # 保温


def generate_weekly_plan(days, weak_subjects, strong_subjects, phase):
    plan = {}

    if phase == "基础巩固期":
        days_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        tasks = []
        # 弱科轮换
        for i, s in enumerate(weak_subjects[:4]):
            tasks.append(f"{s} 知识点梳理 + 基础题×20道")
        # 补强科保温
        for s in strong_subjects[:1]:
            tasks.append(f"{s} 保温练习×15道 + 错题复习")
        tasks.append("综合模拟半套卷（3科限时）")
        tasks.append("错题本复习 + 制定下周计划")

        for i, day in enumerate(days_map):
            plan[day] = tasks[i] if i < len(tasks) else "自由复习/休息"

    elif phase == "专项突破期":
        days_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        tasks = []
        for s in weak_subjects[:2]:
            tasks.append(f"{s} 真题专项×30道 + 错题归因")
        for s in strong_subjects[:1]:
            tasks.append(f"{s} 压轴题训练×10道")
        for s in weak_subjects[:2]:
            tasks.append(f"{s} 模拟题综合练习")
        tasks.append("全科综合套卷（严格限时）")
        tasks.append("对答案 + 错题本 + 知识点补漏")

        for i, day in enumerate(days_map):
            plan[day] = tasks[i] if i < len(tasks) else "自由复习"

    else:  # 综合冲刺期
        for day in ["周一", "周二", "周三", "周四", "周五"]:
            plan[day] = "全真模拟套卷（严格限时3小时）+ 对答案整理错题"
        plan["周六"] = "集中攻克本周高频错题 + 薄弱知识点速查"
        plan["周日"] = "轻度复习（不超过2小时）+ 调整心态 + 早睡"

    return plan


def generate_plan(days, weak_subjects, strong_subjects, exam_type):
    phase, milestone = get_phase(days)
    exam_date = date.today() + timedelta(days=days)

    weekly_plan = generate_weekly_plan(days, weak_subjects, strong_subjects, phase)

    # 每日时间分配
    daily_hours = {}
    all_subjects = list(set(weak_subjects + strong_subjects))
    for s in all_subjects:
        is_weak = s in weak_subjects
        daily_hours[s] = get_daily_hours(s, is_weak)

    result = {
        "generated_at": date.today().isoformat(),
        "exam_date": exam_date.isoformat(),
        "days_remaining": days,
        "exam_type": exam_type,
        "phase": phase,
        "phase_milestone": milestone,
        "weekly_plan": weekly_plan,
        "daily_minutes": daily_hours,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects
    }

    return result


def print_plan(plan):
    print(f"\n📅 高考备考计划\n{'='*40}")
    print(f"距高考：{plan['days_remaining']}天（预计 {plan['exam_date']}）")
    print(f"当前阶段：【{plan['phase']}】")
    print(f"本阶段目标：{plan['phase_milestone']}\n")

    print("【本周计划】")
    for day, task in plan['weekly_plan'].items():
        print(f"  {day}：{task}")

    print("\n【每日科目时间分配（分钟）】")
    for subj, mins in sorted(plan['daily_minutes'].items(),
                              key=lambda x: x[1], reverse=True):
        bar = "▓" * (mins // 10)
        label = "重点攻克" if subj in plan['weak_subjects'] else "保温维持"
        print(f"  {subj:4s}：{mins:3d}分钟  {bar}  [{label}]")

    print(f"\n⚡ 提示：弱科优先，每天保证{max(plan['daily_minutes'].values())}分钟投入最薄弱科目")
    print("发送「今日复习」可查看到期错题，配合计划一起用效果更好！\n")


def main():
    parser = argparse.ArgumentParser(description="高考备考计划生成器")
    parser.add_argument("--days", type=int, required=True, help="距高考天数")
    parser.add_argument("--weak", nargs="+", default=[], help="薄弱科目")
    parser.add_argument("--strong", nargs="+", default=[], help="较强科目")
    parser.add_argument("--type", default="新高考",
                        choices=["新高考", "全国卷"], help="考试类型")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")

    args = parser.parse_args()

    if not args.weak and not args.strong:
        print("请至少指定薄弱科目或强势科目")
        parser.print_help()
        return

    plan = generate_plan(args.days, args.weak, args.strong, args.type)

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print_plan(plan)


if __name__ == "__main__":
    main()
