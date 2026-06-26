#!/usr/bin/env python3
# Author: SQ
"""
健康简报增强版 - 支持新的23个字段
新增：目标完成度、压力百分比、身体电量、时间范围等
"""

import json
import sys
import sqlite3
from datetime import datetime, time, timedelta
from pathlib import Path

ALERT_FILE = Path.home() / ".clawdbot" / "feishu_health_alert.json"
DB_PATH = Path.home() / ".clawdbot" / "garmin" / "data.db"



def safe_int(v, default=None):
    try: return int(v) if v is not None else default
    except: return default

def safe_float(v, default=None):
    try: return float(v) if v is not None else default
    except: return default

def safe(v, default=None):
    return v if v is not None else default


def load_complete_data():
    """加载完整数据（包含新增的23个字段）"""
    if not DB_PATH.exists():
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 获取今天的数据
        now = datetime.now()
        beijing_tz = timedelta(hours=8)

        # 判断今天还是昨天
        hour = now.hour
        if hour < 5:
            target_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            target_date = now.strftime("%Y-%m-%d")

        # 查询所有字段（81个）
        cursor.execute("SELECT * FROM daily_metrics WHERE date = ?", (target_date,))
        row = cursor.fetchone()

        if not row:
            return None

        # 获取列名
        cursor.execute("PRAGMA table_info(daily_metrics)")
        columns = [desc[1] for desc in cursor.fetchall()]

        data = dict(zip(columns, row))

        # 获取睡眠数据
        cursor.execute("""
            SELECT * FROM sleep_data
            WHERE date = ? OR date = ?
            ORDER BY date DESC LIMIT 1
        """, (target_date, (now - timedelta(days=1)).strftime("%Y-%m-%d")))
        sleep_row = cursor.fetchone()

        sleep_data = {}
        if sleep_row:
            sleep_columns = [desc[1] for desc in cursor.description]
            sleep_data = dict(zip(sleep_columns, sleep_row))

        # 获取今日运动
        cursor.execute("""
            SELECT * FROM workouts
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
        """, (int(now.timestamp() - 86400),))
        workout_rows = cursor.fetchall()

        workouts = []
        if workout_rows:
            workout_columns = [desc[1] for desc in cursor.description]
            for wr in workout_rows:
                workouts.append(dict(zip(workout_columns, wr)))

        conn.close()

        return {
            'daily': data,
            'sleep': sleep_data,
            'workouts': workouts
        }

    except Exception as e:
        print(f"❌ 加载数据失败: {e}", file=sys.stderr)
        return None


def generate_morning_report_enhanced(data):
    """早报增强版"""
    if not data:
        return None

    daily = data.get('daily', {})
    sleep = data.get('sleep', {})

    lines = []
    lines.append("🌅 早安健康简报")
    lines.append(f"📅 {daily.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    lines.append("")

    # 睡眠部分（增强）
    if sleep.get('duration_hours', 0) > 0:
        lines.append("😴 昨晚睡眠")
        duration = sleep['duration_hours']
        score = sleep.get('sleep_score', 0)
        deep = sleep.get('deep_sleep_hours', 0)
        rem = sleep.get('rem_sleep_hours', 0)
        light = sleep.get('light_sleep_hours', 0)

        lines.append(f"  • 时长：{duration:.1f}小时")
        score = sleep.get('sleep_score') or 0
        lines.append(f"  • 评分：{score}分")

        if deep or rem or light:
            total = deep + rem + light
            if total > 0:
                lines.append(f"  • 结构：深睡{deep/total*100:.0f}% | REM{rem/total*100:.0f}% | 浅睡{light/total*100:.0f}%")

        # 评价
        if duration >= 7 and score >= 70:
            lines.append("  • 评价：✅ 睡眠充足且质量好")
        elif duration >= 6:
            lines.append("  • 评价：🟡 时长尚可，可再早睡")
        else:
            lines.append("  • 评价：⚠️ 睡眠不足，今晚补回来")

    lines.append("")
    lines.append("📊 今日初始状态")

    # 身体电量（新增）
    bb = daily.get('body_battery_current', 0)
    bb_highest = daily.get('body_battery_highest', 0)
    bb_lowest = daily.get('body_battery_lowest', 0)

    lines.append(f"  • 身体电量：{bb}（最高{bb_highest}，最低{bb_lowest}）")
    if bb >= 70:
        lines.append("    状态：✅ 精力充沛")
    elif bb >= 40:
        lines.append("    状态：🟡 正常水平")
    else:
        lines.append("    状态：⚠️ 电量不足，注意休息")

    # 心率
    hr_resting = daily.get('heart_rate_resting', 0)
    hr_min = daily.get('heart_rate_min', 0)
    hr_max = daily.get('heart_rate_max', 0)
    lines.append(f"  • 静息心率：{hr_resting} bpm（范围：{hr_min}-{hr_max}）")

    # 压力（新增）
    stress_avg = daily.get('stress_average', 0)
    stress_pct = daily.get('stress_percentage', 0)
    lines.append(f"  • 平均压力：{stress_avg}（压力时间占比{stress_pct:.1f}%）")

    # 昨日活动
    steps_yesterday = daily.get('steps', 0)
    lines.append(f"  • 昨日步数：{steps_yesterday:,}步")

    lines.append("")
    lines.append("🎯 今日目标")

    # 步数目标（新增）
    step_goal = daily.get('daily_step_goal', 0)
    if step_goal > 0:
        lines.append(f"  • 步数目标：{step_goal:,}步")

    # 运动目标（新增）
    intensity_goal = daily.get('intensity_minutes_goal', 0)
    if intensity_goal > 0:
        lines.append(f"  • 运动目标：{intensity_goal}分钟（中强度+高强度）")

    # 爬楼目标（新增）
    floors_goal = daily.get('user_floors_goal', 0)
    if floors_goal > 0:
        lines.append(f"  • 爬楼目标：{floors_goal}层")

    lines.append("")
    lines.append("💡 **今日建议**")

    # 根据睡眠情况给建议
    if sleep.get('duration_hours', 0) > 0 and safe_float(sleep.get('duration_hours'), 0) < 6:
        lines.append("  🚨 **昨晚睡眠不足，优先补觉**")
        lines.append("  • 中午午休20-30分钟")
        lines.append("  • 今晚22:00前上床，23:00前入睡")
        lines.append("  • 避免剧烈运动，以恢复为主")
    elif bb < 40:
        lines.append("  ⚠️ **身体电量较低**")
        lines.append("  • 注意休息，避免过度劳累")
        lines.append("  • 可以小憩20分钟恢复")
    elif steps_yesterday < 5000:
        lines.append("  • 昨天运动量少，今天多走走")
        lines.append("  • 目标10,000步或30分钟运动")
    else:
        lines.append("  • 保持规律作息")
        lines.append("  • 饮食均衡，充足饮水")

    lines.append("")
    lines.append("🦞 祝你今天精力充沛！")

    return "\n".join(lines)


def generate_evening_report_enhanced(data):
    """晚报增强版"""
    if not data:
        return None

    daily = data.get('daily', {})
    workouts = data.get('workouts', [])

    lines = []
    lines.append("🌙 晚安健康简报")
    lines.append(f"📅 {daily.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    lines.append("")

    lines.append("📊 今日活动总结")

    # 步数与目标（增强）
    steps = daily.get('steps', 0)
    step_goal = daily.get('daily_step_goal', 0)

    if step_goal > 0:
        pct = steps / step_goal * 100
        lines.append(f"  • 步数：{steps:,} / {step_goal:,}（{pct:.1f}%）")
        if pct >= 100:
            lines.append("    ✅ 目标达成！")
        elif pct >= 80:
            lines.append("    🟡 接近目标")
        else:
            lines.append(f"    🟠 差{step_goal - steps:,}步")
    else:
        lines.append(f"  • 步数：{steps:,}")

    # 运动目标完成度（新增）
    moderate = daily.get('moderate_intensity_minutes', 0)
    vigorous = daily.get('vigorous_intensity_minutes', 0)
    total_intensity = moderate + vigorous
    intensity_goal = daily.get('intensity_minutes_goal', 0)

    if intensity_goal > 0:
        pct = total_intensity / intensity_goal * 100 if intensity_goal > 0 else 0
        lines.append(f"  • 运动：{total_intensity} / {intensity_goal}分钟（{pct:.1f}%）")
        lines.append(f"    （中强度{moderate}分钟 + 高强度{vigorous}分钟）")

    # 爬楼目标（新增）
    floors = daily.get('floors', 0) or 0  # DB uses 'floors' for floors_ascended
    floors_goal = 0  # not in DB schema, skip

    if floors_goal > 0 and floors > 0:
        pct = floors / floors_goal * 100
        lines.append(f"  • 爬楼：{floors:.0f} / {floors_goal}层（{pct:.1f}%）")

    # 卡路里
    calories = daily.get('calories', 0)
    calories_active = daily.get('calories_active', 0)
    lines.append(f"  • 卡路里：{calories:,}（活动消耗{calories_active}）")

    lines.append("")

    # 身体电量总结（新增）
    bb = daily.get('body_battery_current', 0)
    bb_charged = daily.get('body_battery_charged', 0)
    bb_drained = daily.get('body_battery_drained', 0)

    lines.append("🔋 身体电量")
    lines.append(f"  • 当前：{bb}")
    lines.append(f"  • 充电：{bb_charged}")
    lines.append(f"  • 消耗：{bb_drained}")

    # 压力分析（新增）
    stress_pct = daily.get('avg_stress') or 0  # DB has avg_stress, not stress_percentage
    low_pct = daily.get('low_stress_percentage') or 0  # not in DB, will be 0
    rest_pct = daily.get('rest_stress_percentage') or 0  # not in DB, will be 0

    lines.append("")
    lines.append("😰 压力分析")
    lines.append(f"  • 平均压力：{stress_pct}")
    lines.append(f"  • 低压状态：{low_pct:.1f}%")
    lines.append(f"  • 休息状态：{rest_pct:.1f}%")

    if stress_pct > 20:
        lines.append("  • 评价：⚠️ 压力较大，注意放松")
    else:
        lines.append("  • 评价：✅ 压力正常")

    lines.append("")

    # 运动记录
    if workouts:
        lines.append(f"🏋️ 今日运动（{len(workouts)}次）")
        for wo in workouts[:5]:
            name = wo.get('name', wo.get('type', 'Unknown'))
            duration = wo.get('duration_minutes', 0)
            calories = wo.get('calories', 0)
            lines.append(f"  • {name} - {duration}分钟, {calories}卡")
        lines.append("")

    lines.append("💡 明日建议")

    # 根据今日情况给建议
    if steps < step_goal * 0.5:
        lines.append(f"  • 步数未达标，明天目标{step_goal:,}步")
    elif total_intensity < intensity_goal * 0.5 and intensity_goal > 0:
        lines.append(f"  • 运动不足，明天目标{intensity_goal}分钟")
    else:
        lines.append("  • 保持运动习惯，继续加油")

    # 睡眠建议
    if bb < 30:
        lines.append("  • 身体电量低，今晚务必早睡")
        lines.append("  • 目标：22:30上床，23:00入睡")
    else:
        lines.append("  • 早点休息，保证7-8小时睡眠")

    lines.append("")
    lines.append("⏰ 数据采集时间")
    start_time = daily.get('wellness_start_time_local', '')
    end_time = daily.get('wellness_end_time_local', '')
    if start_time and end_time:
        lines.append(f"  • {start_time} → {end_time}")

    lines.append("")
    lines.append("🦞 晚安，好梦！")

    return "\n".join(lines)


def save_alert(message, report_type):
    """保存到alert文件"""
    ALERT_FILE.parent.mkdir(exist_ok=True)

    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": f"health_report_{report_type}",
        "message": message
    }

    with open(ALERT_FILE, 'w', encoding='utf-8') as f:
        json.dump(alert, f, indent=2, ensure_ascii=False)

    print(f"✅ {report_type}已保存: {ALERT_FILE}")


def main():
    """主函数"""
    data = load_complete_data()
    if not data:
        print("❌ 无法加载数据")
        sys.exit(1)

    now = datetime.now()
    current_time = now.time()

    report = None
    report_type = None

    # 早报：6:00-12:00
    if time(6, 0) <= current_time < time(12, 0):
        report = generate_morning_report_enhanced(data)
        report_type = "早报"
    # 晚报：18:00-23:59
    elif time(18, 0) <= current_time:
        report = generate_evening_report_enhanced(data)
        report_type = "晚报"

    if report:
        print(f"📊 {report_type}已生成（增强版）")
        print("=" * 60)
        print(report)
        print("=" * 60)

        save_alert(report, report_type)
    else:
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")


if __name__ == "__main__":
    main()
