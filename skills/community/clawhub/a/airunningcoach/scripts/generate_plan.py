#!/usr/bin/env python3
"""
马拉松训练计划生成器
基于 VDOT 和周期化训练理论
"""

import argparse
import json
from datetime import datetime, timedelta

def generate_weekly_plan(week_num, phase, vdot, weekly_km):
    """
    生成单周训练计划
    
    phase: base(基础), build(强化), peak(巅峰), taper(减量)
    vdot: 当前 VDOT 值
    weekly_km: 周跑量目标
    """
    
    # 配速参考 (基于 VDOT)
    easy_pace = -2.5 * vdot + 280  # 秒/km
    marathon_pace = -2.8 * vdot + 290
    threshold_pace = -3.0 * vdot + 300
    interval_pace = -3.2 * vdot + 310
    
    plan = {
        "week": week_num,
        "phase": phase,
        "target_km": weekly_km,
        "schedule": []
    }
    
    if phase == "base":
        # 基础期：80% 有氧 + 20% 强度
        plan["schedule"] = [
            {"day": "周一", "type": "休息", "description": "休息或交叉训练"},
            {"day": "周二", "type": "轻松跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2"},
            {"day": "周三", "type": "轻松跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2"},
            {"day": "周四", "type": "节奏跑", "km": round(weekly_km * 0.2), "pace": f"{sec_to_pace(threshold_pace - 10)}", "hr_zone": "Z3", "note": "热身 2km + 节奏 5-8km + 冷身 2km"},
            {"day": "周五", "type": "休息", "description": "休息或核心力量"},
            {"day": "周六", "type": "长距离", "km": round(weekly_km * 0.35), "pace": f"{sec_to_pace(easy_pace + 20)}", "hr_zone": "Z2", "note": "最后 2km 马拉松配速"},
            {"day": "周日", "type": "恢复跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace + 30)}", "hr_zone": "Z1"}
        ]
    
    elif phase == "build":
        # 强化期：70% 有氧 + 20% 强度 + 10% 马拉松配速
        plan["schedule"] = [
            {"day": "周一", "type": "休息", "description": "休息或交叉训练"},
            {"day": "周二", "type": "间歇跑", "km": round(weekly_km * 0.18), "pace": f"{sec_to_pace(interval_pace)}", "hr_zone": "Z4-Z5", "note": "热身 3km + 间歇 6-8x800m + 冷身 2km"},
            {"day": "周三", "type": "轻松跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2"},
            {"day": "周四", "type": "阈值跑", "km": round(weekly_km * 0.2), "pace": f"{sec_to_pace(threshold_pace)}", "hr_zone": "Z3-Z4", "note": "热身 2km + 阈值 8-10km + 冷身 2km"},
            {"day": "周五", "type": "休息", "description": "休息或核心力量"},
            {"day": "周六", "type": "长距离", "km": round(weekly_km * 0.35), "pace": f"{sec_to_pace(easy_pace + 15)}", "hr_zone": "Z2", "note": "后 1/3 马拉松配速"},
            {"day": "周日", "type": "恢复跑", "km": round(weekly_km * 0.12), "pace": f"{sec_to_pace(easy_pace + 30)}", "hr_zone": "Z1"}
        ]
    
    elif phase == "peak":
        # 巅峰期：强度最大，最长 LSD
        plan["schedule"] = [
            {"day": "周一", "type": "休息", "description": "休息或交叉训练"},
            {"day": "周二", "type": "间歇跑", "km": round(weekly_km * 0.18), "pace": f"{sec_to_pace(interval_pace)}", "hr_zone": "Z5", "note": "热身 3km + 间歇 5-6x1000m + 冷身 2km"},
            {"day": "周三", "type": "轻松跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2"},
            {"day": "周四", "type": "马拉松配速", "km": round(weekly_km * 0.22), "pace": f"{sec_to_pace(marathon_pace)}", "hr_zone": "Z3", "note": "热身 3km + MP 12-15km + 冷身 2km"},
            {"day": "周五", "type": "休息", "description": "休息或核心力量"},
            {"day": "周六", "type": "长距离", "km": round(weekly_km * 0.35), "pace": f"{sec_to_pace(easy_pace + 10)}", "hr_zone": "Z2", "note": "后 1/2 马拉松配速"},
            {"day": "周日", "type": "恢复跑", "km": round(weekly_km * 0.1), "pace": f"{sec_to_pace(easy_pace + 30)}", "hr_zone": "Z1"}
        ]
    
    elif phase == "taper":
        # 减量期：跑量减少，保持强度
        plan["schedule"] = [
            {"day": "周一", "type": "休息", "description": "休息"},
            {"day": "周二", "type": "短间歇", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(interval_pace)}", "hr_zone": "Z4", "note": "热身 2km + 间歇 4x400m + 冷身 2km"},
            {"day": "周三", "type": "轻松跑", "km": round(weekly_km * 0.15), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2"},
            {"day": "周四", "type": "马拉松配速", "km": round(weekly_km * 0.18), "pace": f"{sec_to_pace(marathon_pace)}", "hr_zone": "Z3", "note": "热身 2km + MP 6-8km + 冷身 2km"},
            {"day": "周五", "type": "休息", "description": "休息"},
            {"day": "周六", "type": "短长距离", "km": round(weekly_km * 0.3), "pace": f"{sec_to_pace(easy_pace)}", "hr_zone": "Z2", "note": "轻松跑，最后 1km MP"},
            {"day": "周日", "type": "恢复跑", "km": round(weekly_km * 0.22), "pace": f"{sec_to_pace(easy_pace + 30)}", "hr_zone": "Z1"}
        ]
    
    return plan

def sec_to_pace(seconds):
    """秒/km 转换为 分：秒/km 格式"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def generate_marathon_plan(
    current_pb_min,
    target_time_min,
    weeks=24,
    current_weekly_km=300
):
    """
    生成完整马拉松训练计划
    
    current_pb_min: 当前全马 PB（分钟）
    target_time_min: 目标时间（分钟）
    weeks: 训练周期（周）
    current_weekly_km: 当前周跑量
    """
    
    # 计算 VDOT（基于 Daniels 表）
    current_pace = current_pb_min / 42.195
    target_pace = target_time_min / 42.195
    current_vdot = -9.93 * current_pace + 96.4
    target_vdot = -9.93 * target_pace + 96.4
    
    plan = {
        "runner_info": {
            "current_pb": f"{int(current_pb_min//60)}:{int(current_pb_min%60):02d}",
            "target_time": f"{int(target_time_min//60)}:{int(target_time_min%60):02d}",
            "current_vdot": round(current_vdot, 1),
            "target_vdot": round(target_vdot, 1)
        },
        "phases": [],
        "weekly_plans": []
    }
    
    # 阶段划分
    phase_weeks = {
        "base": 6,
        "build": 8,
        "peak": 6,
        "taper": 2
    }
    
    # 周跑量规划
    base_km = current_weekly_km
    peak_km = current_weekly_km * 1.3  # 峰值跑量增加 30%
    
    week_num = 1
    for phase_name, phase_duration in phase_weeks.items():
        phase_data = {
            "name": phase_name,
            "weeks": phase_duration,
            "focus": get_phase_focus(phase_name)
        }
        plan["phases"].append(phase_data)
        
        for i in range(phase_duration):
            if phase_name == "base":
                weekly_km = base_km + (peak_km - base_km) * (i / phase_duration) * 0.5
            elif phase_name == "build":
                weekly_km = base_km + (peak_km - base_km) * (0.5 + i / phase_duration * 0.5)
            elif phase_name == "peak":
                weekly_km = peak_km * (1 - i * 0.05)  # 逐渐减少
            else:  # taper
                weekly_km = peak_km * (0.6 - i * 0.2)
            
            # 渐进增加 VDOT
            vdot_progress = min(1.0, (week_num - 1) / (weeks - 2))
            current_vdot_adj = current_vdot + (target_vdot - current_vdot) * vdot_progress
            
            weekly_plan = generate_weekly_plan(
                week_num,
                phase_name,
                current_vdot_adj,
                weekly_km
            )
            plan["weekly_plans"].append(weekly_plan)
            week_num += 1
    
    return plan

def get_phase_focus(phase):
    """获取阶段训练重点"""
    focuses = {
        "base": "有氧基础 + 力量",
        "build": "乳酸阈值 + 间歇",
        "peak": "马拉松配速 + 最长 LSD",
        "taper": "恢复 + 保持状态"
    }
    return focuses.get(phase, "")

def main():
    parser = argparse.ArgumentParser(description="马拉松训练计划生成器")
    parser.add_argument("--current-pb", type=str, help="当前 PB (格式：HH:MM 或 分钟数)", required=True)
    parser.add_argument("--target", type=str, help="目标时间 (格式：HH:MM 或 分钟数)", required=True)
    parser.add_argument("--weeks", type=int, default=24, help="训练周期 (周)")
    parser.add_argument("--weekly-km", type=float, default=300, help="当前周跑量 (km)")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 解析时间
    def parse_time(time_str):
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
        return float(time_str)
    
    current_pb = parse_time(args.current_pb)
    target = parse_time(args.target)
    
    # 生成计划
    plan = generate_marathon_plan(current_pb, target, args.weeks, args.weekly_km)
    
    if args.output == "json":
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print("马拉松训练计划")
        print(f"{'='*60}")
        print(f"当前 PB: {plan['runner_info']['current_pb']}")
        print(f"目标时间：{plan['runner_info']['target_time']}")
        print(f"当前 VDOT: {plan['runner_info']['current_vdot']}")
        print(f"目标 VDOT: {plan['runner_info']['target_vdot']}")
        print(f"\n训练周期：{args.weeks}周")
        print(f"\n阶段划分:")
        for phase in plan['phases']:
            print(f"  - {phase['name'].upper()}: {phase['weeks']}周 ({phase['focus']})")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
