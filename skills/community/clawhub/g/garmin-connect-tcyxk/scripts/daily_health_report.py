#!/usr/bin/env python3
# Author: SQ
"""
每日健康简报 - 早报和晚报
早8点：昨晚睡眠+今日状态
晚10点：全天总结+明日建议
"""

import json
import sys
from datetime import datetime, time
from pathlib import Path



def safe_int(v, default=None):
    try: return int(v) if v is not None else default
    except: return default

def safe_float(v, default=None):
    try: return float(v) if v is not None else default
    except: return default

def safe(v, default=None):
    return v if v is not None else default


def load_garmin_data():
    """加载Garmin数据"""
    cache_file = Path.home() / ".clawdbot" / ".garmin-cache.json"

    if not cache_file.exists():
        return None

    try:
        with open(cache_file) as f:
            return json.load(f)
    except:
        return None


def generate_morning_report(data):
    """早8点简报：昨晚睡眠+今日状态"""

    if not data:
        return "❌ 无法获取健康数据"

    lines = []
    lines.append("🌅 **早安健康简报**")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')} {datetime.now().strftime('%H:%M')}")
    lines.append("")

    # 睡眠数据
    sleep = data.get('sleep') or {}
    if (sleep.get('duration_hours') or 0) > 0:
        lines.append("😴 **昨晚睡眠**")
        lines.append(f"  • 时长：{safe(sleep.get('duration_hours') or '--', 0)} 小时")
        lines.append(f"  • 质量：{safe(sleep.get('quality_percent') or '--', 0)} 分")

        if safe_float(sleep.get('quality_percent') or '--', 0) >= 80:
            lines.append("  • 评价：✅ 睡眠质量很好")
        elif safe_float(sleep.get('quality_percent') or '--', 0) >= 60:
            lines.append("  • 评价：🟡 睡眠质量一般")
        else:
            lines.append("  • 评价：⚠️ 睡眠质量需改善")

        lines.append(f"  • 深睡：{safe_float(sleep.get('deep_sleep_hours') or '--', 0)}h | REM：{safe_float(sleep.get('rem_sleep_hours') or '--', 0)}h")
    else:
        lines.append("😴 **睡眠数据**：暂无昨晚数据")

    lines.append("")

    # 今日状态
    summary = data.get('summary') or {}
    body_battery = data.get('body_battery') or {}
    stress = data.get('stress') or {}
    hrv = data.get('hrv') or {}
    respiration = data.get('respiration') or {}
    vo2_max = data.get('vo2_max') or {}
    # ── 统一处理 None 值 ──
    for _var in [summary, sleep, body_battery, stress, hrv, respiration, vo2_max]:
        if _var is None:
            _var = {}
    # 字符串默认
    for _k in ['sleep_source', 'sleep_quality']:
        if sleep.get(_k) is None:
            sleep[_k] = '--'
    # 数值默认
    for _k in summary:
        if summary[_k] is None:
            summary[_k] = 0
    for _k in sleep:
        if sleep.get(_k) is None:
            sleep[_k] = 0
    bb = body_battery  # alias for compatibility

    lines.append("📊 **今日初始状态**")
    lines.append(f"  • 静息心率：{safe(summary.get('heart_rate_resting') or '--', 0)} bpm")
    lines.append(f"  • 昨日步数：{safe_int(summary.get('steps') or '--', 0):,} 步")

    # 身体电量（如果有）
    if 'body_battery' in data and data['body_battery']:
        bb = data['body_battery'][0] if isinstance(data['body_battery'], list) else data['body_battery']
        if isinstance(bb, dict) and 'charged' in bb:
            lines.append(f"  • 身体电量：充{safe_int(bb.get('charged') or '--', 0)}/耗{safe_int(bb.get('drained') or '--', 0)}")

    lines.append("")

    # 今日建议
    lines.append("💡 **今日建议**")

    if (sleep.get('quality_percent') or 0) < 60:
        lines.append("  • 睡眠质量一般，今天注意休息")
        lines.append("  • 建议午休20-30分钟")

    if safe_int(summary.get('steps') or '--', 0) < 8000:
        lines.append("  • 昨天运动量较少，今天多活动")
    else:
        lines.append("  • 保持运动习惯，继续加油")

    lines.append("  • 保持充足饮水（2-3L）")
    lines.append("  • 注意工作间隙休息")

    lines.append("")
    lines.append("🦞 祝你今天精力充沛！")

    return "\n".join(lines)


def generate_evening_report(data):
    """晚10点简报：全天总结+明日建议"""

    if not data:
        return "❌ 无法获取健康数据"

    lines = []
    lines.append("🌙 **晚安健康简报**")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')} {datetime.now().strftime('%H:%M')}")
    lines.append("")

    # 今日活动总结
    summary = data.get('summary') or {}
    lines.append("📊 **今日活动总结**")
    lines.append(f"  • 步数：{safe_int(summary.get('steps') or '--', 0):,} 步")

    if safe_int(summary.get('steps') or '--', 0) >= 10000:
        lines.append("  • 步数评价：✅ 优秀！达标")
    elif safe_int(summary.get('steps') or '--', 0) >= 8000:
        lines.append("  • 步数评价：🟡 良好，继续保持")
    elif safe_int(summary.get('steps') or '--', 0) >= 5000:
        lines.append("  • 步数评价：🟠 一般，明天多走")
    else:
        lines.append("  • 步数评价：⚠️ 偏少，明天加油")

    lines.append(f"  • 消耗卡路里：{summary['calories']:.0f} 卡")
    lines.append(f"  • 静息心率：{safe(summary.get('heart_rate_resting') or '--', 0)} bpm")
    lines.append("")

    # 运动记录
    workouts = data.get('workouts', [])
    if workouts:
        lines.append(f"🏋️ **今日运动** ({len(workouts)}次)")

        for workout in workouts[:5]:  # 最多显示5条
            name = workout.get('name', 'Unnamed')
            duration = workout.get('duration_minutes', 0)
            calories = workout.get('calories', 0)

            lines.append(f"  • {name} - {duration}分钟, {calories}卡")

        lines.append("")
    else:
        lines.append("🏋️ **运动记录**：今天没有运动记录")
        lines.append("")

    # 压力分析（如果有）
    if 'stress' in data and data['stress']:
        stress = data['stress']
        avg_stress = stress.get('avgStressLevel') or 0
        lines.append("😌 **压力分析**")

        if avg_stress <= 25:
            lines.append(f"  • 平均压力：{avg_stress} - ✅ 压力水平低，状态放松")
        elif avg_stress <= 50:
            lines.append(f"  • 平均压力：{avg_stress} - 🟡 压力适中")
        elif avg_stress <= 75:
            lines.append(f"  • 平均压力：{avg_stress} - 🟠 压力较大，注意放松")
        else:
            lines.append(f"  • 平均压力：{avg_stress} - ⚠️ 压力很大，需要休息")

        lines.append("")

    # 明日建议
    lines.append("💡 **明日建议**")

    if safe_int(summary.get('steps') or '--', 0) < 8000:
        lines.append("  • 今天运动量不足，明天目标10,000步")

    if workouts:
        lines.append("  • 今天运动了，明天安排轻度活动恢复")
    else:
        lines.append("  • 今天没运动，明天安排30分钟运动")

    lines.append("  • 早点休息，保证7-8小时睡眠")
    lines.append("  • 睡前1小时减少手机使用")

    lines.append("")
    lines.append("🦞 晚安，好梦！")

    return "\n".join(lines)


def main():
    """主函数"""

    # 加载数据
    data = load_garmin_data()

    if not data:
        print("❌ 无法加载Garmin数据")
        sys.exit(1)

    # 判断早报还是晚报
    now = datetime.now()
    current_time = now.time()

    # 早报：6:00-12:00
    if time(6, 0) <= current_time < time(12, 0):
        report = generate_morning_report(data)
        report_type = "morning"
    # 晚报：18:00-23:59
    elif time(18, 0) <= current_time:
        report = generate_evening_report(data)
        report_type = "evening"
    else:
        # 其他时间不发送
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")
        sys.exit(0)

    # 输出报告
    print(report)
    print(f"\n[DEBUG] Report type: {report_type}, Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
