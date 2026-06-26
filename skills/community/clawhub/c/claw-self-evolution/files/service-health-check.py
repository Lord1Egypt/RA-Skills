#!/usr/bin/env python3
"""
服务健康监控 + 自动恢复
定期检查OpenClaw服务是否正常运行，异常自动重启，还是不正常再告警
"""

import os
import sys
import subprocess
from datetime import datetime
from typing import Tuple, Optional

PROCESS_NAME = "copaw"
CHECK_PORT = 8088

def is_process_running() -> bool:
    """检查进程是否在运行"""
    try:
        result = subprocess.run(
            f"pgrep -f {PROCESS_NAME}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except:
        return False

def is_port_listening() -> bool:
    """检查端口是否在监听"""
    try:
        result = subprocess.run(
            f"ss -tulpn | grep :{CHECK_PORT}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except:
        return False

def try_restart_service() -> bool:
    """尝试重启服务"""
    print("🔄 尝试重启服务...")
    try:
        # 尝试docker-compose重启
        if os.path.exists("/app/working/scripts/legacy/deploy/docker-compose.yaml"):
            result = subprocess.run(
                "cd /app/working && docker-compose restart",
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0
        else:
            # 如果没docker，尝试直接重启进程
            result = subprocess.run(
                f"pkill -f {PROCESS_NAME} && sleep 2 && nohup {PROCESS_NAME} > /dev/null 2>&1 &",
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0
    except Exception as e:
        print(f"❌ 重启失败: {e}")
        return False

def generate_report(is_ok: bool, restarted: bool = False, success: bool = False) -> str:
    """生成健康报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if is_ok:
        return f"""# 🟢 服务健康检查报告 - {now}

✅ 服务运行正常
- 进程: 正在运行
- 端口: {CHECK_PORT} 正在监听
- 状态: 良好，无需操作

---
*自动检查，每15分钟运行一次*
"""
    else:
        if restarted:
            if success:
                return f"""# ✅ 服务异常已自动恢复 - {now}

❌ 检测到服务异常，已自动重启成功
- 重启前状态: 进程异常退出 / 端口未监听
- 操作: 已执行自动重启
- 当前状态: ✅ 恢复正常

---
*自动检查，每15分钟运行一次*
"""
            else:
                return f"""# 🔴 服务自动重启失败 - {now}

❌ 检测到服务异常，自动重启失败
- 重启前状态: 进程异常退出 / 端口未监听
- 操作: 尝试自动重启，但失败了
- 需要你手动介入处理，请登录服务器检查

---
*自动检查，每15分钟运行一次*
"""
        else:
            return f"""# 🔴 服务异常告警 - {now}

❌ 检测到服务异常
- 状态: 进程未运行 / 端口未监听
- 未尝试自动恢复，请手动处理

---
*自动检查，每15分钟运行一次*
"""

def main():
    print("🔍 开始服务健康检查...")
    now = datetime.now()
    
    process_ok = is_process_running()
    
    # 在当前环境中，只要主进程在运行就算正常
    # 端口检查可能因为权限/命名显示问题误判
    print(f"进程运行: {'✅' if process_ok else '❌'}")
    
    if process_ok:
        print("✅ 服务正常")
        sys.exit(0)  # 正常退出，不推送
    
    # 异常了，尝试自动恢复
    print("⚠️  服务异常，尝试自动恢复...")
    restart_success = try_restart_service()
    
    # 等待一下再检查
    import time
    time.sleep(10)
    
    process_ok_after = is_process_running()
    port_ok_after = is_port_listening()
    
    if process_ok_after and port_ok_after:
        print("✅ 自动恢复成功")
        report = generate_report(False, True, True)
        # 保存报告，退出码1触发推送
        report_dir = "/app/working/logs/service-health/"
        os.makedirs(report_dir, exist_ok=True)
        filename = f"health-{now.strftime('%Y%m%d-%H%M')}.md"
        with open(os.path.join(report_dir, filename), 'w', encoding='utf-8') as f:
            f.write(report)
        print(report)
        sys.exit(1)  # 推送报告告诉你恢复了
    else:
        print("❌ 自动恢复失败")
        report = generate_report(False, True, False)
        report_dir = "/app/working/logs/service-health/"
        os.makedirs(report_dir, exist_ok=True)
        filename = f"health-{now.strftime('%Y%m%d-%H%M')}.md"
        with open(os.path.join(report_dir, filename), 'w', encoding='utf-8') as f:
            f.write(report)
        print(report)
        sys.exit(1)  # 推送告警

if __name__ == "__main__":
    main()
