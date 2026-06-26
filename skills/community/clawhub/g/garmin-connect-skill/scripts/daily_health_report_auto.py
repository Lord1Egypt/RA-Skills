#!/usr/bin/env python3
# Author: SQ
"""
主动发送健康简报到飞书
通过OpenClaw的message工具发送
"""

import json
import subprocess
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
        return None

    lines = []
    lines.append("🌅 **早安健康简报**")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')} {datetime.now().strftime('%H:%M')}")
    lines.append("")

    # 睡眠数据
    sleep = data.get('sleep', {})
    if sleep.get('duration_hours', 0) > 0:
        lines.append("😴 **昨晚睡眠**")
        lines.append(f"  • 时长：{safe(sleep.get('duration_hours'), 0)} 小时")
        lines.append(f"  • 质量：{safe(sleep.get('quality_percent'), 0)} 分")

        if safe_float(sleep.get('quality_percent'), 0) >= 80:
            lines.append("  • 评价：✅ 睡眠质量很好")
        elif safe_float(sleep.get('quality_percent'), 0) >= 60:
            lines.append("  • 评价：🟡 睡眠质量一般")
        else:
            lines.append("  • 评价：⚠️ 睡眠质量需改善")

        lines.append(f"  • 深睡：{safe_float(sleep.get('deep_sleep_hours'), 0)}h | REM：{safe_float(sleep.get('rem_sleep_hours'), 0)}h")
    else:
        lines.append("😴 **睡眠数据**：暂无昨晚数据")

    lines.append("")

    # 今日状态
    summary = data.get('summary', {})
    lines.append("📊 **今日初始状态**")
    lines.append(f"  • 静息心率：{safe(summary.get('heart_rate_resting'), 0)} bpm")
    lines.append(f"  • 昨日步数：{safe_int(summary.get('steps'), 0):,} 步")

    lines.append("")
    lines.append("💡 **今日建议**")
    lines.append("  • 保持充足饮水（2-3L）")
    lines.append("  • 注意工作间隙休息")
    lines.append("")
    lines.append("🦞 祝你今天精力充沛！")

    return "\n".join(lines)


def generate_evening_report(data):
    """晚10点简报：全天总结+明日建议"""

    if not data:
        return None

    lines = []
    lines.append("🌙 **晚安健康简报**")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日')} {datetime.now().strftime('%H:%M')}")
    lines.append("")

    # 今日活动总结
    summary = data.get('summary', {})
    lines.append("📊 **今日活动总结**")
    lines.append(f"  • 步数：{safe_int(summary.get('steps'), 0):,} 步")

    if safe_int(summary.get('steps'), 0) >= 10000:
        lines.append("  • 步数评价：✅ 优秀！达标")
    elif safe_int(summary.get('steps'), 0) >= 8000:
        lines.append("  • 步数评价：🟡 良好，继续保持")
    elif safe_int(summary.get('steps'), 0) >= 5000:
        lines.append("  • 步数评价：🟠 一般，明天多走")
    else:
        lines.append("  • 步数评价：⚠️ 偏少，明天加油")

    lines.append(f"  • 消耗卡路里：{summary['calories']:.0f} 卡")
    lines.append(f"  • 静息心率：{safe(summary.get('heart_rate_resting'), 0)} bpm")
    lines.append("")

    # 运动记录
    workouts = data.get('workouts', [])
    if workouts:
        lines.append(f"🏋️ **今日运动** ({len(workouts)}次)")
        for workout in workouts[:5]:
            name = workout.get('name', 'Unnamed')
            duration = workout.get('duration_minutes', 0)
            calories = workout.get('calories', 0)
            lines.append(f"  • {name} - {duration}分钟, {calories}卡")
        lines.append("")
    else:
        lines.append("🏋️ **运动记录**：今天没有运动记录")
        lines.append("")

    lines.append("💡 **明日建议**")
    if safe_int(summary.get('steps'), 0) < 8000:
        lines.append("  • 今天运动量不足，明天目标10,000步")
    else:
        lines.append("  • 保持运动习惯，继续加油")
    lines.append("  • 早点休息，保证7-8小时睡眠")
    lines.append("")
    lines.append("🦞 晚安，好梦！")

    return "\n".join(lines)


def send_to_feishu(message):
    """发送消息到飞书（通过OpenClaw）"""

    # 保存消息到临时文件，由OpenClaw读取并发送
    temp_file = Path.home() / ".clawdbot" / "feishu_queue.json"
    temp_file.parent.mkdir(exist_ok=True)

    # 读取现有队列
    queue = []
    if temp_file.exists():
        try:
            with open(temp_file, 'r') as f:
                queue = json.load(f)
        except:
            pass

    # 添加新消息
    queue.append({
        "timestamp": datetime.now().isoformat(),
        "message": message
    })

    # 保存队列
    with open(temp_file, 'w') as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

    print(f"✅ 消息已加入发送队列: {temp_file}")


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

    report = None
    report_type = None

    # 早报：6:00-12:00
    if time(6, 0) <= current_time < time(12, 0):
        report = generate_morning_report(data)
        report_type = "早报"
    # 晚报：18:00-23:59
    elif time(18, 0) <= current_time:
        report = generate_evening_report(data)
        report_type = "晚报"

    if report:
        print(f"📊 {report_type}已生成")
        print("=" * 50)
        print(report)
        print("=" * 50)

        # 发送到飞书
        send_to_feishu(report)
        print(f"✅ {report_type}已发送到飞书队列")
    else:
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")


if __name__ == "__main__":
    main()
