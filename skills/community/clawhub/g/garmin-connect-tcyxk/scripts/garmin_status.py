#!/usr/bin/env python3
# Author: SQ
"""
Quick Garmin data viewer for OpenClaw
Usage: python3 garmin_status.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def load_garmin_data():
    """Load cached Garmin data"""
    cache_file = Path.home() / ".clawdbot" / ".garmin-cache.json"

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except:
        return None

def format_garmin_status():
    """Format Garmin data for display"""

    data = load_garmin_data()

    if not data:
        return "❌ No Garmin data available. Run sync first."

    lines = []
    lines.append("📊 **Garmin 运动数据**")
    lines.append("")

    # Last sync time
    timestamp = data.get('timestamp', 'Unknown')
    lines.append(f"🕐 最后同步: {timestamp}")
    lines.append("")

    # Daily summary
    summary = data.get('summary', {})
    lines.append("📈 **今日活动**")
    lines.append(f"  • 步数: {summary.get('steps', 0):,}")
    lines.append(f"  • 静息心率: {summary.get('heart_rate_resting') or 0} bpm")
    lines.append(f"  • 卡路里: {summary.get('calories', 0):.0f}")
    lines.append(f"  • 活动时长: {summary.get('active_minutes', 0)} 分钟")
    lines.append(f"  • 距离: {summary.get('distance_km', 0):.2f} km")
    lines.append("")

    # Sleep data
    sleep = data.get('sleep', {})
    if sleep.get('duration_hours', 0) > 0:
        lines.append("😴 **睡眠数据**")
        lines.append(f"  • 时长: {sleep.get('duration_hours', 0)} 小时")
        lines.append(f"  • 质量: {sleep.get('quality_percent', 0)}%")
        lines.append(f"  • 深睡: {sleep.get('deep_sleep_hours', 0)}h")
        lines.append(f"  • REM: {sleep.get('rem_sleep_hours', 0)}h")
        lines.append(f"  • 浅睡: {sleep.get('light_sleep_hours', 0)}h")
        lines.append("")
    else:
        lines.append("😴 **睡眠**: 暂无今日数据")
        lines.append("")

    # Recent workouts
    workouts = data.get('workouts') or []
    if workouts:
        lines.append(f"🏋️ **最近运动** (最近{len(workouts)}次)")

        for workout in workouts[:5]:  # Show last 5
            name = workout.get('name', 'Unnamed')
            wtype = workout.get('type', {})
            type_key = wtype.get('typeKey', 'unknown') if isinstance(wtype, dict) else str(wtype) if wtype else 'unknown'
            duration = workout.get('duration_minutes', 0) or 0
            calories = workout.get('calories', 0) or 0

            # Chinese type names
            type_names = {
                'running': '跑步',
                'walking': '步行',
                'cycling': '骑行',
                'strength_training': '力量训练',
                'elliptical': '椭圆机',
            }
            type_cn = type_names.get(type_key, type_key)

            lines.append(f"  • {name} ({type_cn}) - {duration}分钟, {calories}卡")

    return "\n".join(lines)

if __name__ == "__main__":
    print(format_garmin_status())
