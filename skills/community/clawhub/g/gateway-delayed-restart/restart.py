#!/usr/bin/env python3
"""Gateway Delayed Restart - 延迟重启网关（带通知）"""

import subprocess
import time
import sys
from datetime import datetime, timedelta

def restart_gateway(delay_minutes=2, notify=True):
    """
    延迟重启网关，完成后主动通知
    
    Args:
        delay_minutes: 延迟分钟数
        notify: 是否发送通知
    """
    start_time = datetime.now()
    restart_time = start_time + timedelta(minutes=delay_minutes)
    
    print(f"⏰ 将在 {delay_minutes} 分钟后重启 Gateway")
    print(f"📅 重启时间：{restart_time.strftime('%H:%M:%S')}")
    print("")
    
    # 倒计时
    for remaining in range(delay_minutes * 60, 0, -1):
        mins = remaining // 60
        secs = remaining % 60
        print(f"\r⏳ 剩余：{mins}分{secs}秒", end='', flush=True)
        time.sleep(1)
    
    print("\n🔄 正在重启 Gateway...")
    result = subprocess.run(
        ['openclaw', 'gateway', 'restart'],
        capture_output=True,
        text=True
    )
    
    end_time = datetime.now()
    duration = (end_time - restart_time).total_seconds()
    
    # 输出结果
    print("")
    print("=" * 50)
    print("📊 重启报告")
    print("=" * 50)
    print(f"✅ Gateway 重启完成！")
    print(f"📅 完成时间：{end_time.strftime('%H:%M:%S')}")
    print(f"⏱️ 实际耗时：{duration:+.1f}秒")
    print(f"🔧 进程 PID: {get_gateway_pid()}")
    print("=" * 50)
    
    # 发送通知
    if notify:
        send_notification(end_time, duration, result.returncode == 0)
    
    return result.returncode == 0

def get_gateway_pid():
    """获取 Gateway 进程 PID"""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'openclaw-gateway'],
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().split('\n')
        return pids[-1] if pids and pids[0] else '未知'
    except:
        return '未知'

def send_notification(complete_time, duration, success):
    """发送完成通知"""
    status = "✅ 成功" if success else "❌ 失败"
    duration_text = f"{duration:+.1f}秒"
    
    message = f"""
🎉 Gateway 重启完成通知

📊 状态：{status}
⏰ 完成时间：{complete_time.strftime('%H:%M:%S')}
⏱️ 耗时：{duration_text}
🔧 PID: {get_gateway_pid()}

🚀 可以开始使用了！
"""
    
    print(message)
    
    # 尝试发送飞书通知（如果配置了）
    try:
        subprocess.run([
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--target', 'ou_6650e2645a6e8f4c7363cbbfd6bbcf33',
            '--message', f"🎉 Gateway 重启{status}！时间：{complete_time.strftime('%H:%M:%S')}"
        ], capture_output=True, timeout=10)
        print("📱 通知已发送")
    except Exception as e:
        print(f"⚠️ 通知发送失败：{e}")

if __name__ == '__main__':
    delay = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    restart_gateway(delay)
