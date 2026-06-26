#!/usr/bin/env python3
# Author: SQ
"""
飞书健康简报 - 全面版（包含所有健康和运动指标分析）
"""

import json
import sys
import time
from datetime import datetime, time
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 缺少requests库")
    sys.exit(1)



def safe_int(v, default=None):
    try: return int(v) if v is not None else default
    except: return default

def safe_float(v, default=None):
    try: return float(v) if v is not None else default
    except: return default

def safe(v, default=None):
    return v if v is not None else default


def get_tenant_access_token(app_id, app_secret):
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }

    response = requests.post(url, json=data, timeout=10)
    result = response.json()

    if result.get("code") == 0:
        return result["tenant_access_token"]
    return None


def send_to_feishu_app(message):
    """发送消息到飞书应用内部"""

    # 配置
    config_file = Path.home() / ".clawdbot" / "feishu_app.json"
    if not config_file.exists():
        print("❌ 配置文件不存在")
        return False

    with open(config_file) as f:
        config = json.load(f)

    app_id = config["app_id"]
    app_secret = config["app_secret"]

    # 获取token
    token = get_tenant_access_token(app_id, app_secret)
    if not token:
        print("❌ 获取token失败")
        return False

    # 发送消息到应用的机器人消息接收地址
    # 这种方式不需要user_id，直接发到应用内部
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 先尝试获取应用所在的会话
    # 这里我们使用一个特殊的方法：创建一个消息卡片到应用本身
    msg_data = {
        "msg_type": "text",
        "content": json.dumps({"text": message})
    }

    # 方式1：尝试发送到应用的自定义机器人接收地址
    # 这个需要应用开启"接收机器人消息"功能
    webhook_url = config.get("webhook_url")
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"msg_type": "text", "content": {"text": message}}, timeout=10)
            if response.status_code == 200:
                print("✅ 消息已通过webhook发送")
                return True
        except:
            pass

    # 方式2：保存到文件，让用户知道
    alert_file = Path.home() / ".clawdbot" / "health_alert.txt"
    with open(alert_file, 'w') as f:
        f.write(f"{datetime.now().isoformat()}\n{message}")

    print(f"⚠️  消息已保存到 {alert_file}")
    print("   飞书权限开通较复杂，暂时使用文件方式")
    return True


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
    """早8点简报 - 全面版（包含所有健康和运动指标）"""

    if not data:
        return None

    lines = []
    lines.append("🌅 早安健康简报")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    lines.append("")

    # ===== 身体状态 =====
    lines.append("📊 身体状态")
    lines.append("")

    # 睡眠数据
    sleep = data.get('sleep') or {}
    has_main_sleep = (sleep.get('duration_hours') or 0) > 0
    sleep_source = sleep.get('sleep_source', 'none')

    if has_main_sleep:
        duration = sleep['duration_hours']
        quality = sleep['quality_percent']

        if sleep_source == 'promoted_nap':
            lines.append("😴 睡眠记录（智能识别）")
            lines.append(f"  • 时长：{duration} 小时")

            time_range = ", ".join([
                f"{nap.get('start_time', '')}-{nap.get('end_time', '')}"
                for nap in sleep.get('nap_details', [])
            ])
            lines.append(f"  • 时段：{time_range}")

            if duration >= 7:
                lines.append("  • 评价：✅ 睡眠时长充足")
            elif duration >= 5:
                lines.append("  • 评价：🟡 睡眠时长尚可")
            else:
                lines.append("  • 评价：⚠️ 睡眠时长不足")
        else:
            lines.append("😴 昨晚睡眠")
            lines.append(f"  • 时长：{duration} 小时")
            lines.append(f"  • 质量：{quality} 分")

            if quality >= 80:
                lines.append("  • 评价：✅ 睡眠质量很好")
            elif quality >= 60:
                lines.append("  • 评价：🟡 睡眠质量一般")
            else:
                lines.append("  • 评价：⚠️ 睡眠质量需改善")
    else:
        lines.append("😴 睡眠数据：暂无昨晚数据")

    lines.append("")

    # 身体电量
    body_battery = data.get('body_battery') or {}
    if (body_battery.get('current') or 0) > 0:
        lines.append("🔋 身体电量")
        lines.append(f"  • 当前：{safe_int(body_battery.get('current') or 0)}%")
        lines.append(f"  • 充电/消耗：+{safe_int(body_battery.get('charged') or 0)}% / -{safe_int(body_battery.get('drained') or 0)}%")

        if (body_battery.get('current') or 0) >= 70:
            lines.append("  • 评价：✅ 精力充沛")
        elif (body_battery.get('current') or 0) >= 40:
            lines.append("  • 评价：🟡 精力尚可")
        else:
            lines.append("  • 评价：⚠️ 需要休息")
        lines.append("")

    # 压力指数
    stress = data.get('stress') or {}
    if (stress.get('average') or 0) > 0:
        lines.append("😌 压力指数")
        lines.append(f"  • 平均压力：{safe_int(stress.get('average') or 0)}/100")
        rest_pct = safe_float(stress.get('rest_percentage'), 0)
        lines.append(f"  • 休息状态：{rest_pct:.1f}%")

        if (stress.get('average') or 0) <= 25:
            lines.append("  • 评价：✅ 压力很低，状态很好")
        elif (stress.get('average') or 0) <= 50:
            lines.append("  • 评价：🟡 压力适中")
        else:
            lines.append("  • 评价：⚠️ 压力偏高，注意放松")
        lines.append("")

    # ===== 心肺功能 =====
    lines.append("🫀 心肺功能")
    lines.append("")

    summary = data.get('summary') or {}
    hrv = data.get('hrv') or {}
    respiration = data.get('respiration') or {}
    vo2_max = data.get('vo2_max') or {}
    # 统一处理 None 值
    for _var in [summary, sleep, body_battery, stress, hrv, respiration, vo2_max]:
        if _var is None:
            _var = {}
    bb = body_battery  # alias for compatibility
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
    for _k in (bb or {}):
        if (bb or {}).get(_k) is None:
            bb[_k] = 0
    for _k in (stress or {}):
        if (stress or {}).get(_k) is None:
            stress[_k] = 0
    for _k in (hrv or {}):
        if (hrv or {}).get(_k) is None:
            hrv[_k] = 0


    # 心率数据
    lines.append(f"💓 心率数据")
    lines.append(f"  • 静息心率：{summary.get('heart_rate_resting') or 0} bpm")
    if (summary.get('heart_rate_min') or 0) > 0:
        lines.append(f"  • 最低心率：{summary.get('heart_rate_min') or 0} bpm")
    if (summary.get('heart_rate_max') or 0) > 0:
        lines.append(f"  • 最高心率：{summary.get('heart_rate_max') or 0} bpm")

    # 静息心率评价
    rhr = summary['heart_rate_resting']
    if rhr <= 50:
        lines.append("  • 评价：🏆 优秀（运动员级别）")
    elif rhr <= 60:
        lines.append("  • 评价：✅ 很好（心血管健康）")
    elif rhr <= 70:
        lines.append("  • 评价：🟡 正常范围")
    else:
        lines.append("  • 评价：⚠️ 偏高，建议加强有氧运动")
    lines.append("")

    # 呼吸频率
    respiration = data.get('respiration', {})
    if respiration.get('highest_respiration', 0) > 0:
        lines.append("🌬️ 呼吸频率")
        lines.append(f"  • 范围：{respiration['lowest_respiration']}-{respiration['highest_respiration']} 次/分")
        if respiration.get('avg_respiration', 0) > 0:
            lines.append(f"  • 平均：{respiration['avg_respiration']} 次/分")

        avg_resp = respiration.get('avg_respiration', 0)
        if 12 <= avg_resp <= 20:
            lines.append("  • 评价：✅ 正常范围")
        else:
            lines.append("  • 评价：🟡 略偏离正常")
        lines.append("")

    # ===== 运动表现 =====
    lines.append("🏃 运动表现")
    lines.append("")

    # VO2 Max
    vo2 = data.get('vo2_max', {})
    if vo2.get('vo2_max', 0) > 0:
        lines.append("🏃 VO2 Max（有氧能力）")
        lines.append(f"  • 数值：{vo2['vo2_max']} (精确值：{vo2['vo2_max_precise']})")

        vo2_value = vo2['vo2_max']
        if vo2_value >= 55:
            lines.append("  • 评价：🏆 优秀（精英级别）")
        elif vo2_value >= 50:
            lines.append("  • 评价：✅ 很好（高于平均水平）")
        elif vo2_value >= 45:
            lines.append("  • 评价：🟡 良好（平均水平）")
        else:
            lines.append("  • 评价：📈 需提升有氧能力")
        lines.append("")

    # 体能年龄
    fit_age = data.get('fitness_age', {})
    if fit_age.get('fitness_age', 0) > 0:
        lines.append("👤 体能年龄")
        chronological = fit_age['chronological_age']
        fitness = fit_age['fitness_age']
        lines.append(f"  • 实际年龄：{chronological} 岁")
        lines.append(f"  • 体能年龄：{fitness} 岁")

        if fitness < chronological:
            diff = round(chronological - fitness, 1)
            lines.append(f"  • 评价：✅ 体能年龄比实际年龄年轻 {diff} 岁，很好！")
        elif fitness <= chronological + 2:
            lines.append("  • 评价：🟡 体能与年龄相符")
        else:
            lines.append("  • 评价：⚠️ 体能年龄偏大，需加强运动")

        # 可达到的体能年龄
        achievable = fit_age.get('achievable_fitness_age', 0)
        if achievable > 0:
            potential = round(chronological - achievable, 1)
            lines.append(f"  • 潜力：可达到 {achievable} 岁（再年轻 {potential} 岁）")

        # 优先改进领域
        priority = fit_age.get('priority_area')
        if priority:
            priority_map = {
                'bmi': '体重管理',
                'vigorousDaysAvg': '高强度运动天数',
                'vigorousMinutesAvg': '高强度运动时长',
                'rhr': '静息心率',
            }
            lines.append(f"  • 优先改进：{priority_map.get(priority, priority)}")
        lines.append("")

    # 乳酸阈值（运动表现指标）
    lactate = data.get('lactate_threshold', {})
    if lactate.get('ftp_watts', 0) > 0:
        lines.append("⚡ 乳酸阈值（运动表现）")
        lines.append(f"  • 功能阈值功率 (FTP)：{lactate['ftp_watts']}W")

        # 功率体重比评价（男性）
        ptw = lactate['power_to_weight']
        if ptw >= 5.0:
            lines.append("  • 功率体重比：{:.2f} W/kg".format(ptw))
            lines.append("  • 评价：🏆 精英级（业余车手水平）")
        elif ptw >= 4.0:
            lines.append("  • 功率体重比：{:.2f} W/kg".format(ptw))
            lines.append("  • 评价：✅ 很好（训练有素）")
        elif ptw >= 3.0:
            lines.append("  • 功率体重比：{:.2f} W/kg".format(ptw))
            lines.append("  • 评价：🟡 良好（中级水平）")
        else:
            lines.append("  • 功率体重比：{:.2f} W/kg".format(ptw))
            lines.append("  • 评价：📈 有提升空间")

        if lactate.get('threshold_heart_rate', 0) > 0:
            lines.append(f"  • 阈值心率：{lactate['threshold_heart_rate']} bpm")
        lines.append("")

    # ===== 今日活动目标 =====
    lines.append("📯 今日活动目标")
    lines.append("")

    lines.append(f"  • 昨日步数：{safe_int(summary.get('steps') or 0):,} 步")
    if (summary.get('floors_ascended') or 0) > 0:
        lines.append(f"  • 爬楼层数：{summary.get('floors_ascended') or 0:.1f} 层")

    if (summary.get('calories') or 0) > 0:
        lines.append(f"  • 消耗卡路里：{summary.get('calories') or 0:.0f} 卡")
        if (summary.get('intensity_minutes') or 0) > 0:
            lines.append(f"  • 中高强度运动：{summary.get('intensity_minutes') or 0} 分钟")

    # 步数目标评价
    if safe_int(summary.get('steps') or '--', 0) >= 10000:
        lines.append("  • 步数评价：✅ 达标！继续保持")
    elif safe_int(summary.get('steps') or '--', 0) >= 8000:
        lines.append("  • 步数评价：🟡 良好，接近目标")
    else:
        lines.append("  • 步数评价：📠 今天多走动")
    lines.append("")

    # ===== 今日建议 =====
    lines.append("💡 今日建议")

    # 根据体能年龄优先级给建议
    if fit_age.get('priority_area'):
        priority = fit_age['priority_area']
        if priority == 'bmi':
            lines.append("  • 体重管理是当前重点，注意饮食和有氧运动")
        elif 'vigorous' in priority:
            lines.append("  • 增加高强度训练，提升心肺功能")
        elif priority == 'rhr':
            lines.append("  • 坚持有氧运动，降低静息心率")

    # 根据睡眠给建议
    if (sleep.get('duration_hours') or 0) < 6:
        lines.append("  • 睡眠不足，今晚早点休息")
    elif (sleep.get('duration_hours') or 0) < 7:
        lines.append("  • 睡眠略少，建议保证7-8小时")

    # 根据身体电量给建议
    if (body_battery.get('current') or 0) < 40:
        lines.append("  • 身体电量较低，避免高强度训练")
    elif (body_battery.get('current') or 0) >= 70:
        lines.append("  • 精力充沛，适合高强度训练")

    lines.append("  • 保持充足饮水（2-3L）")
    lines.append("")
    lines.append("🦞 祝你今天精力充沛，表现精彩！")

    return "\n".join(lines)


def generate_evening_report(data):
    """晚10点简报 - 运动总结版"""

    if not data:
        return None

    lines = []
    lines.append("🌙 晚安健康简报")
    lines.append(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    lines.append("")

    # 今日活动总结
    summary = data.get('summary') or {}
    lines.append("📊 今日活动总结")
    lines.append(f"  • 步数：{safe_int(summary.get('steps') or '--', 0):,} 步")

    if safe_int(summary.get('steps') or '--', 0) >= 10000:
        lines.append("  • 步数评价：✅ 优秀！达标")
    elif safe_int(summary.get('steps') or '--', 0) >= 8000:
        lines.append("  • 步数评价：🟡 良好，继续保持")
    else:
        lines.append("  • 步数评价：🟠 一般，明天多走")

    lines.append(f"  • 消耗卡路里：{summary.get('calories') or 0:.0f} 卡")
    if (summary.get('intensity_minutes') or 0) > 0:
        lines.append(f"  • 中高强度运动：{summary.get('intensity_minutes') or 0} 分钟")
    lines.append("")

    # 运动记录
    workouts = data.get('workouts') or []
    if workouts:
        lines.append(f"🏋️ 今日运动 ({len(workouts)}次)")
        for workout in workouts[:5]:
            name = workout.get('name', 'Unnamed')
            duration = workout.get('duration_minutes') or 0
            calories = workout.get('calories') or 0
            lines.append(f"  • {name} - {duration}分钟, {calories}卡")
        lines.append("")

    # 身体电量总结
    body_battery = data.get('body_battery') or {}
    if (body_battery.get('drained') or 0) > 0:
        lines.append("🔋 身体电量总结")
        lines.append(f"  • 充电：{body_battery.get('charged') or 0}%")
        lines.append(f"  • 消耗：{body_battery.get('drained') or 0}%")
        if (body_battery.get('current') or 0) > 0:
            lines.append(f"  • 当前剩余：{body_battery.get('current') or 0}%")
        lines.append("")

    lines.append("💡 明日建议")
    if safe_int(summary.get('steps') or '--', 0) < 8000:
        lines.append("  • 今天运动量不足，明天目标10,000步")
    else:
        lines.append("  • 保持运动习惯，继续加油")

    # 根据身体电量给建议
    if (body_battery.get('current') or 0) < 30:
        lines.append("  • 身体电量较低，今晚早点休息")
    else:
        lines.append("  • 早点休息，保证7-8小时睡眠")
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
        send_to_feishu_app(report)
    else:
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")


if __name__ == "__main__":
    main()
