#!/usr/bin/env python3
# Author: SQ
"""
主动发送健康简报到飞书
使用飞书webhook直接发送
"""

import json
import os
import sys
import subprocess
from datetime import datetime, time
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 缺少requests库，请运行: pip install requests")
    sys.exit(1)



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
    """早8点简报"""

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
    """晚10点简报"""

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
    else:
        lines.append("  • 步数评价：🟠 一般，明天多走")

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

    lines.append("💡 **明日建议**")
    if safe_int(summary.get('steps'), 0) < 8000:
        lines.append("  • 今天运动量不足，明天目标10,000步")
    else:
        lines.append("  • 保持运动习惯，继续加油")
    lines.append("  • 早点休息，保证7-8小时睡眠")
    lines.append("")
    lines.append("🦞 晚安，好梦！")

    return "\n".join(lines)


def send_feishu_webhook(message, webhook_url=None):
    """通过飞书webhook发送消息"""

    if not webhook_url:
        # 从配置文件读取
        config_file = Path.home() / ".clawdbot" / "feishu_webhook.json"
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                webhook_url = config.get("webhook_url")

    if not webhook_url:
        print("❌ 未配置飞书webhook URL")
        print("请运行: python3 scripts/daily_health_report_webhook.py --setup-webhook")
        return False

    # 飞书消息格式
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 消息已发送到飞书")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False


def setup_webhook():
    """交互式设置webhook"""

    print("🔗 配置飞书Webhook")
    print("\n1. 打开飞书群组")
    print("2. 点击群组设置 → 群机器人 → 添加机器人")
    print("3. 自定义机器人 → 复制Webhook URL\n")

    webhook_url = input("粘贴Webhook URL: ").strip()

    if webhook_url:
        # 保存配置
        config_file = Path.home() / ".clawdbot" / "feishu_webhook.json"
        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, 'w') as f:
            json.dump({"webhook_url": webhook_url}, f, indent=2)

        os.chmod(config_file, 0o600)

        # 测试发送
        test_message = "🦞 龙虾健康大脑已激活！\n\n这是测试消息，如果你看到这条消息，说明配置成功！"
        print("\n正在发送测试消息...")
        if send_feishu_webhook(test_message, webhook_url):
            print("\n✅ 配置成功！健康简报将自动发送到此群组。")
            return True
        else:
            print("\n❌ 测试失败，请检查webhook URL是否正确。")
            return False
    else:
        print("⏭️  跳过配置")
        return False


def main():
    """主函数"""

    # 设置模式
    if "--setup-webhook" in sys.argv:
        setup_webhook()
        return

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
        send_feishu_webhook(report)
    else:
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")


if __name__ == "__main__":
    main()
