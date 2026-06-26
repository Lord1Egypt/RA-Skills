#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_task.py — 注册 Windows 计划任务，实现证书自动续期

功能：
  - 创建每日定时任务，自动运行 scheduler.py --once
  - 任务名称：BCE-CertRenew
  - 默认每天 03:00 执行

用法（需要管理员权限）：
  python setup_task.py install    # 注册计划任务
  python setup_task.py uninstall  # 删除计划任务
  python setup_task.py status     # 查看任务状态
"""

import sys
import os
import subprocess
from pathlib import Path

TASK_NAME = "BCE-CertRenew"
TASK_TIME = "03:00"  # 每天凌晨 3 点执行


def get_python_exe() -> str:
    return sys.executable


def get_script_path() -> str:
    return str(Path(__file__).parent / "scheduler.py")


def install_task():
    python = get_python_exe()
    script = get_script_path()
    script_dir = str(Path(__file__).parent)

    # 构造 schtasks 命令
    cmd = [
        "schtasks", "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{python}" "{script}" --once --log-dir "{script_dir}\\logs"',
        "/sc", "DAILY",
        "/st", TASK_TIME,
        "/ru", "SYSTEM",
        "/rl", "HIGHEST",
        "/f",  # 强制覆盖已有任务
    ]

    print(f"注册计划任务: {TASK_NAME}")
    print(f"执行时间: 每天 {TASK_TIME}")
    print(f"执行命令: {python} {script} --once")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 计划任务注册成功！")
        print(result.stdout)
    else:
        print("❌ 注册失败（可能需要管理员权限）:")
        print(result.stderr)
        sys.exit(1)


def uninstall_task():
    cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 计划任务 [{TASK_NAME}] 已删除")
    else:
        print(f"❌ 删除失败: {result.stderr}")


def status_task():
    cmd = ["schtasks", "/query", "/tn", TASK_NAME, "/fo", "LIST"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="gbk", errors="replace")
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"任务 [{TASK_NAME}] 不存在或查询失败")


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "install":
        install_task()
    elif action == "uninstall":
        uninstall_task()
    elif action == "status":
        status_task()
    else:
        print("用法: python setup_task.py [install|uninstall|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
