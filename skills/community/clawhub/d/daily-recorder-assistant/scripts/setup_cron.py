#!/usr/bin/env python3
"""
setup_cron.py - 为 daily-recorder-assistant 配置 OpenClaw cron 定时任务

仅支持 OpenClaw cron add CLI 模式（推荐方式）

功能:
- 自动生成安装命令
- 【安全设计】不强制删除任何现有 cron job，仅提醒
"""

import os
import subprocess
import json
import sys

# 路径配置（通过 config.py 引用，动态计算）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CURRENT_SKILL_PATH, DEFAULT_CHANNEL
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")

def detect_system_timezone():
    try:
        tz_env = os.environ.get('TZ', '')
        if tz_env:
            return tz_env
    except Exception:
        pass
    return 'Asia/Shanghai'

CURRENT_TZ = detect_system_timezone()

def load_active_channel():
    """加载活跃频道配置"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        return state.get('active_channel', DEFAULT_CHANNEL)
    else:
        return DEFAULT_CHANNEL

def load_user_id_for_channel(channel=None):
    """获取频道对应的用户 ID"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        target_channel = channel or state.get('active_channel', DEFAULT_CHANNEL)
        user_id_by_channel = state.get('user_id_by_channel', {})
        return user_id_by_channel.get(target_channel, None) or '待授权'
    else:
        return '未配置'

def verify_openclaw_cron():
    """验证 OpenClaw cron 任务是否存在"""
    try:
        result = subprocess.run(['openclaw', 'cron', 'list'], capture_output=True, text=True)
        if "daily-recorder-assistant" in result.stdout:
            print("✓ OpenClaw cron jobs found")
            return True
        else:
            print("⚠️ 未找到 daily-recorder-assistant cron jobs")
            return False
    except Exception as e:
        print(f"❌ 无法验证:{e}")
        return False

def check_old_cron_jobs():
    """【安全设计】仅提醒旧 task 存在（不自动执行删除）
    
    重要原则：为了安全，不再强制删除任何 OpenClaw cron 定时任务
    - 只检查并显示现有任务
    - 列出所有任务 ID 供用户参考
    - 建议用户手动清理，但绝不强制执行
    
    Returns:
        bool: True=无旧任务/检查成功; False=检测到旧任务; None=检查失败
    """
    try:
        result = subprocess.run(['openclaw', 'cron', 'list'], capture_output=True, text=True)
        if "daily-recorder-assistant" in result.stdout:
            print("⚠️ 检测到已存在的 daily-recorder-assistant cron 任务")
            
            # 提取所有任务 ID（第一列即为 UUID）
            lines = result.stdout.strip().split('\n')
            task_ids_found = []
            for line in lines:
                if "daily-recorder-assistant" in line:
                    parts = line.split()
                    if len(parts) >= 1 and parts[0]:  # UUID
                        task_ids_found.append(parts[0])
            
            print("⚠️ 旧任务 ID 列表：")
            for job_id in task_ids_found:
                print(f"    - {job_id}")
            
            print("⚠️ 【安全提示】建议手动清理旧任务后再安装，避免重复")
            print("⚠️ 为避免误操作，本脚本不自动执行删除")
            return False  # 返回 False 但继续流程（仅提醒）
        else:
            print("✓ 无旧任务，无需删除")
            return True
    except Exception as e:
        print(f"⚠️ 检查失败:{e}")
        return None

def execute_openclaw_cron(job_name, cron_expr, message):
    """执行 OpenClaw cron add 命令"""
    current_channel = load_active_channel()
    try:
        current_user_id = load_user_id_for_channel(current_channel)
        # 直接执行 openclaw CLI，避免 shell injection
        args = [
            'openclaw', 'cron', 'add',
            '--name', job_name,
            '--cron', cron_expr,
            '--tz', CURRENT_TZ,
            '--session', 'isolated',
            '--wake', 'now',
            '--channel', current_channel,
            '--to', current_user_id,
            '--message', message,
            '--announce'
        ]
        result = subprocess.run(args, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ {job_name} cron job installed")
            try:
                return json.loads(result.stdout.strip())
            except:
                return {"status": "success"}
        else:
            print(f"❌ {job_name} failed:")
            print(result.stderr)
            return None

    except Exception as e:
        print(f"❌ Error executing cron add for {job_name}: {e}")
        return None

def main():
    """Cron 配置主函数
    
    设计原则（2026-04-12 讨论）：
    - 默认使用 OpenClaw cron add CLI 模式（推荐方式优先展示）
    - Cron vs Manual 互不干扰，明确区分两种模式
    - 删除过度自动化逻辑，避免误操作用户任务
    - "精简即美"原则：只保留必要功能
    
    【安全设计】不强制删除任何现有 cron job，仅提醒
    """
    print("=" * 60)
    print("DAILY-RECORDER-ASSISTANT CRON CONFIGURATION SETUP")
    print(f"✓ Detected system timezone: {CURRENT_TZ}")
    print("=" * 60)

    # 【安全设计】避免过度自动化，只提醒不强制删除任何 cron job
    warning_msg = check_old_cron_jobs()
    if warning_msg is None:
        print("⚠️ 检查失败，但仍继续安装流程")
    elif warning_msg is False:  # 检测到旧任务但仅提醒
        print("⚠️ 【安全提示】用户需手动清理旧任务（或忽略重复风险）")
    
    morning_job = execute_openclaw_cron(
        "daily-recorder-assistant-morning",
        "0 8 * * *",
        """每日状态记录与复盘助手：
🌞早上好！昨晚休息得怎么样呀？精力还充沛吗？今天有什么计划吗？
（发送「早反馈」告诉我你的状态）"""
    )

    evening_job = execute_openclaw_cron(
        "daily-recorder-assistant-evening",
        "0 18 * * *",
        """每日状态记录与复盘助手：
🌙晚上好！今天过得怎么样呀？有没有疲惫呢？有什么收获或想改进的吗？
（发送「晚复盘」告诉我你的状态）"""
    )

    if morning_job and evening_job:
        print("\n✓ Both cron jobs installed successfully")
        verify_openclaw_cron()

    print("\n" + "=" * 60)
    print("CRON SCHEDULE SUMMARY:")
    print("=" * 60)
    print("OpenClaw cron jobs:")
    print("  - daily-recorder-assistant-morning: 0 8 * * * (8:00)")
    print("  - daily-recorder-assistant-evening: 0 18 * * * (18:00)")
    print("=" * 60)

if __name__ == "__main__":
    main()
