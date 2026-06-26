#!/usr/bin/env python3
# Author: SQ
"""
佳明快捷响应 - OpenClaw集成
自动识别用户意图并调用相应的查询脚本

触发词：
- 健康/状态/身体情况 → health_quick.py
- 睡眠/睡觉 → sleep_quick.py
- 运动/锻炼 → workout_quick.py

使用：在对话处理中调用 handle_garmin_query(message)
"""

import os
import sys
from pathlib import Path

# 脚本路径
SCRIPT_DIR = Path.home() / '.clawdbot' / 'garmin'
HEALTH_QUICK = SCRIPT_DIR / 'health_quick.py'
SLEEP_QUICK = SCRIPT_DIR / 'sleep_quick.py'
WORKOUT_QUICK = SCRIPT_DIR / 'workout_quick.py'


def handle_garmin_query(message):
    """
    处理佳明健康数据查询

    参数：
        message: 用户消息字符串

    返回：
        str: 查询结果（格式化的文本），如果不匹配则返回None
    """
    if not message or not isinstance(message, str):
        return None

    message_lower = message.lower()

    # 健康状态查询
    if any(keyword in message for keyword in ['健康', '状态', '身体情况', '身体数据', '身体状况']):
        return run_quick_script(HEALTH_QUICK)

    # 睡眠查询
    elif any(keyword in message for keyword in ['睡眠', '睡觉', '昨晚睡', '睡得怎么样', '睡得如何']):
        return run_quick_script(SLEEP_QUICK)

    # 运动查询
    elif any(keyword in message for keyword in ['运动', '锻炼', '健身', '跑步', '活动']):
        return run_quick_script(WORKOUT_QUICK)

    return None


def run_quick_script(script_path):
    """
    运行快捷查询脚本

    参数：
        script_path: 脚本路径

    返回：
        str: 脚本输出结果
    """
    try:
        if not script_path.exists():
            return f"❌ 脚本不存在：{script_path}"

        result = os.popen(f'python3 {script_path}').read()

        if not result:
            return "❌ 暂无数据"

        return result

    except Exception as e:
        return f"❌ 查询失败：{e}"


# 测试代码
if __name__ == '__main__':
    test_messages = [
        "看一下我的健康状态",
        "我最近睡得怎么样",
        "最近有什么运动记录",
        "今天天气怎么样",  # 不匹配
    ]

    print("🧪 佳明快捷响应测试")
    print("=" * 60)

    for msg in test_messages:
        print(f"\n📝 用户：{msg}")
        result = handle_garmin_query(msg)
        if result:
            print(f"✅ 匹配成功")
            print(f"📊 返回：\n{result}")
        else:
            print("❌ 不匹配（不处理）")
