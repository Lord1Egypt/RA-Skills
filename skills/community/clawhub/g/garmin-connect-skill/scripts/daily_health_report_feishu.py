#!/usr/bin/env python3
# Author: SQ
"""
主动发送健康简报到飞书
使用飞书开放平台API（App ID + App Secret）
"""

import json
import os
import sys
import time
from datetime import datetime, time
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 缺少requests库，请运行: pip install requests")
    sys.exit(1)


class FeishuAPI:
    """飞书开放平台API客户端"""

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expires_at = 0

    def get_tenant_access_token(self):
        """获取tenant_access_token"""

        # 如果token还有效，直接返回
        if self.tenant_access_token and time.time() < self.token_expires_at:
            return self.tenant_access_token

        # 获取新token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result.get("code") == 0:
                self.tenant_access_token = result["tenant_access_token"]
                self.token_expires_at = time.time() + result["expire"] - 300  # 提前5分钟刷新
                return self.tenant_access_token
            else:
                print(f"❌ 获取token失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None

    def send_message(self, user_id, message):
        """发送消息到指定用户"""

        token = self.get_tenant_access_token()
        if not token:
            return False

        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "receive_id": user_id,
            "msg_type": "text",
            "content": json.dumps({"text": message})
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()

            if result.get("code") == 0:
                print("✅ 消息已发送到飞书")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False



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


def setup_feishu_app():
    """交互式配置飞书应用"""

    print("🔗 配置飞书开放平台应用")
    print("\n1. 打开飞书开放平台: https://open.feishu.cn/")
    print("2. 创建应用或使用现有应用")
    print("3. 启用机器人能力")
    print("4. 获取App ID和App Secret\n")

    app_id = input("App ID (已输入: cli_a93b2fe33db85bce): ").strip()
    if not app_id:
        app_id = "cli_a93b2fe33db85bce"

    app_secret = input("App Secret (已输入): ").strip()
    if not app_secret:
        app_secret = "sXYUTkNRSSBFxYTTS8UNfe7koyZwS8PB"

    user_id = input("你的User ID (open_id或user_id): ").strip()

    if not user_id:
        print("\n❌ 需要User ID才能发送消息")
        print("可以通过以下方式获取:")
        print("  1. 在飞书中查看你的个人资料")
        print("  2. 或者让管理员在管理后台查看")
        return False

    # 保存配置
    config_file = Path.home() / ".clawdbot" / "feishu_app.json"
    config_file.parent.mkdir(exist_ok=True)

    config = {
        "app_id": app_id,
        "app_secret": app_secret,
        "user_id": user_id
    }

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    os.chmod(config_file, 0o600)

    # 测试发送
    print("\n正在发送测试消息...")
    feishu = FeishuAPI(app_id, app_secret)
    test_message = "🦞 龙虾健康大脑已激活！\n\n这是测试消息，如果你看到这条消息，说明配置成功！"

    if feishu.send_message(user_id, test_message):
        print("\n✅ 配置成功！健康简报将自动发送到飞书。")
        return True
    else:
        print("\n❌ 测试失败，请检查配置是否正确。")
        return False


def main():
    """主函数"""

    # 设置模式
    if "--setup" in sys.argv:
        setup_feishu_app()
        return

    # 加载配置
    config_file = Path.home() / ".clawdbot" / "feishu_app.json"

    if not config_file.exists():
        print("❌ 未配置飞书应用")
        print("请运行: python3 scripts/daily_health_report_feishu.py --setup")
        sys.exit(1)

    with open(config_file) as f:
        config = json.load(f)

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
        feishu = FeishuAPI(config["app_id"], config["app_secret"])
        feishu.send_message(config["user_id"], report)
    else:
        print(f"⏰ 当前时间 {now.strftime('%H:%M')} 不在发送时段")


if __name__ == "__main__":
    main()
