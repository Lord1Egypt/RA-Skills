#!/usr/bin/env python3
"""
跑步配速和心率区间计算器
基于 Jack Daniels VDOT 理论和极化训练原则
"""

import argparse
import json
import sys

def vdot_to_pace(vdot, distance_km=42.195):
    """
    根据 VDOT 值计算各配速区间
    
    基于 Daniels VDOT 表（全马）:
    VDOT 40: E=5:47, M=5:12, T=4:51, I=4:24, R=4:04
    VDOT 44: E=5:29, M=4:56, T=4:37, I=4:11, R=3:52
    VDOT 50: E=5:05, M=4:35, T=4:19, I=3:54, R=3:36
    VDOT 54: E=4:51, M=4:23, T=4:08, I=3:44, R=3:26
    """
    # VDOT 到配速的近似公式（基于 Daniels 表线性回归）
    pace_easy = -2.5 * vdot + 440      # 轻松跑配速 (秒/km)
    pace_marp = -2.8 * vdot + 445      # 马拉松配速
    pace_threshold = -3.0 * vdot + 450 # 阈值配速
    pace_interval = -3.5 * vdot + 480  # 间歇配速
    pace_rep = -3.8 * vdot + 500       # 重复跑配速
    
    return {
        "easy": {"min": pace_easy, "max": pace_easy + 30},
        "marathon": {"min": pace_marp - 10, "max": pace_marp + 10},
        "threshold": {"min": pace_threshold - 5, "max": pace_threshold + 5},
        "interval": {"min": pace_interval - 5, "max": pace_interval + 5},
        "repetition": {"min": pace_rep - 5, "max": pace_rep + 5}
    }

def pace_to_vdot(race_time_min, distance_km):
    """
    根据比赛成绩反推 VDOT
    
    race_time_min: 比赛时间（分钟）
    distance_km: 比赛距离（公里）
    
    基于 Daniels VDOT 表线性回归：
    - 全马 3:00 (4:16/km) → VDOT ≈ 54
    - 全马 3:30 (5:00/km) → VDOT ≈ 46
    - 全马 3:38 (5:11/km) → VDOT ≈ 44
    - 全马 4:00 (5:41/km) → VDOT ≈ 40
    """
    pace_min_per_km = race_time_min / distance_km
    
    # 基于 Daniels 表的经验公式（线性回归）
    if distance_km == 42.195:  # 全马
        vdot = -9.93 * pace_min_per_km + 96.4
    elif distance_km == 21.0975:  # 半马
        vdot = -9.5 * pace_min_per_km + 93
    elif distance_km == 10:  # 10K
        vdot = -9.0 * pace_min_per_km + 90
    else:
        vdot = -9.5 * pace_min_per_km + 93
    
    return max(30, min(85, vdot))  # 限制在合理范围

def calculate_heart_rate_zones(max_hr, resting_hr=None):
    """
    计算心率区间
    
    方法 1: 最大心率百分比法
    方法 2: 储备心率法 (Karvonen) - 更准确
    """
    zones = {}
    
    if resting_hr:
        # 储备心率法 (更准确)
        hrr = max_hr - resting_hr
        zones = {
            "Z1": {"min": int(resting_hr + hrr * 0.5), "max": int(resting_hr + hrr * 0.6), "name": "恢复区"},
            "Z2": {"min": int(resting_hr + hrr * 0.6), "max": int(resting_hr + hrr * 0.7), "name": "有氧区"},
            "Z3": {"min": int(resting_hr + hrr * 0.7), "max": int(resting_hr + hrr * 0.8), "name": " tempo 区"},
            "Z4": {"min": int(resting_hr + hrr * 0.8), "max": int(resting_hr + hrr * 0.9), "name": "阈值区"},
            "Z5": {"min": int(resting_hr + hrr * 0.9), "max": int(max_hr), "name": "最大摄氧区"}
        }
    else:
        # 最大心率百分比法
        zones = {
            "Z1": {"min": int(max_hr * 0.5), "max": int(max_hr * 0.6), "name": "恢复区"},
            "Z2": {"min": int(max_hr * 0.6), "max": int(max_hr * 0.7), "name": "有氧区"},
            "Z3": {"min": int(max_hr * 0.7), "max": int(max_hr * 0.8), "name": "tempo 区"},
            "Z4": {"min": int(max_hr * 0.8), "max": int(max_hr * 0.9), "name": "阈值区"},
            "Z5": {"min": int(max_hr * 0.9), "max": int(max_hr), "name": "最大摄氧区"}
        }
    
    return zones

def sec_to_pace_str(seconds):
    """秒/km 转换为 分：秒/km 格式"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def main():
    parser = argparse.ArgumentParser(description="跑步配速和心率区间计算器")
    parser.add_argument("--vdot", type=float, help="VDOT 值")
    parser.add_argument("--race-time", type=float, help="比赛时间 (分钟)")
    parser.add_argument("--distance", type=float, default=42.195, help="比赛距离 (公里)")
    parser.add_argument("--max-hr", type=int, help="最大心率")
    parser.add_argument("--resting-hr", type=int, help="静息心率")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    result = {}
    
    # 计算 VDOT
    if args.vdot:
        vdot = args.vdot
    elif args.race_time and args.distance:
        vdot = pace_to_vdot(args.race_time, args.distance)
    else:
        print("请提供 --vdot 或 --race-time + --distance")
        sys.exit(1)
    
    result["vdot"] = round(vdot, 1)
    
    # 计算配速区间
    pace_zones = vdot_to_pace(vdot)
    result["pace_zones"] = {}
    for zone, paces in pace_zones.items():
        result["pace_zones"][zone] = {
            "min": sec_to_pace_str(paces["min"]),
            "max": sec_to_pace_str(paces["max"])
        }
    
    # 计算心率区间
    if args.max_hr:
        result["heart_rate_zones"] = calculate_heart_rate_zones(args.max_hr, args.resting_hr)
    
    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*50}")
        print(f"VDOT: {result['vdot']}")
        print(f"{'='*50}")
        print("\n配速区间:")
        for zone, paces in result["pace_zones"].items():
            print(f"  {zone.upper()}: {paces['min']} - {paces['max']} /km")
        if "heart_rate_zones" in result:
            print("\n心率区间:")
            for zone, hr in result["heart_rate_zones"].items():
                print(f"  {zone} ({hr['name']}): {hr['min']} - {hr['max']} bpm")
        print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
