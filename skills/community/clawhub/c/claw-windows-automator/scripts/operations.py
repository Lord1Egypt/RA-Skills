#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是整个 Windows 自动化引擎的主入口模块（Main Entry / Runner），负责统筹调度所有自动化任务的执行流程，提供统一的任务管理、Overlay 可视化提示和安全退出机制。
核心功能：
    1、任务注册与调度系统（OPERATIONS 字典）
        将所有自动化任务集中管理，支持通过任务名称动态执行（例如 cmd_task、github_download 等）。
    2、全屏 Overlay 可视化管理
        在任务执行前自动启动 AutomationOverlay（半透明遮罩 + 大标题提示），让用户清晰看到当前正在执行什么任务。
        支持鼠标左键单击强制终止整个程序。
    3、终止回调机制（on_overlay_terminated）
        当用户单击鼠标强制退出时：
            1、立即记录日志
            2、执行清理工作（如关闭 Overlay、清理残留进程等）
            3、调用 os._exit(0) 强制安全退出程序，避免残留进程
    4、任务执行流程（run_operation）：
        1、启动全屏 Overlay 并等待其完全渲染
        2、执行对应的任务函数
        3、无论成功或失败，最终都会关闭 Overlay（finally 块保证）
    5、辅助功能：
        1、list_operations()：列出当前支持的所有任务及其描述
        2、CLI 命令行接口：
            1、ist：显示所有可用任务
            2、run --task <任务名>：执行指定任务（支持额外参数如 --path、--script、--url）
"""

import argparse
import os
import sys
from pathlib import Path
import env_manager
import ensure_package
import gradient_overlay
from logger_manager import LoggerManager
import tkinter as tk
import cmd_task
import github_download
from cmd_automator import CmdAutomator

logger = LoggerManager.setup_logger(logger_name="claw-windows-automator")
cmd_auto=CmdAutomator()

# 强制 UTF-8 输出
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# 操作注册表
OPERATIONS = {}

def register_operation(name: str, description: str):
    def decorator(func):
        OPERATIONS[name] = {"func": func, "desc": description}
        return func
    return decorator

# ====================== 核心操作 ======================

@register_operation(cmd_task.NAME, "打开目录并执行bat")
def exec_cmd_task():
    if not (args.path and args.script):
        logger.info("⚠️ 终止程序：必须同时指定 path 和 script 参数。")
        on_overlay_terminated()   
    cmd_task.execute(args.path,args.script,cmd_auto)

@register_operation(github_download.NAME, "打开目录并执行bat")
def exec_github_download():
    if not (args.url):
        logger.info("❌ 请通过 --url 传入 GitHub 地址")
        on_overlay_terminated()      
    github_download.execute(args.url,cmd_auto)

# ====================== 运行入口 ======================
def on_overlay_terminated():
    """ESC按下时，外部程序会立刻收到通知"""
    logger.info("\n🔴 【外部收到通知】AutomationOverlay 已通过ESC强制终止！")
    logger.info("   → 正在停止所有后续任务...")
    try:
        # 这里放你想做的清理工作（尽量简短）
        gradient_overlay.stop_overlay()   # 如果需要
        # 可以加：杀掉可能残留的 CMD 进程等
        logger.info("   → 已执行清理")
    except Exception as e:
        logger.info(f"清理时出错: {e}")
    # 最后强制退出
    os._exit(0)

def run_operation(task_name: str):
    if task_name not in OPERATIONS:
        on_overlay_terminated()
        raise ValueError(f"未知任务: {task_name}")

    try:
        logger.info(f"【第一步】启动全屏Overlay特效...")
        # ==============================================
        # 核心：先弹出UI，强制刷新，等待完全显示
        # ==============================================
        gradient_overlay.start_overlay(on_terminate=on_overlay_terminated)
        gradient_overlay.overlay.refresh()
        gradient_overlay.safe_sleep(0.8)  # 等待UI完全渲染
        logger.info(f"✅ Overlay已显示，开始执行任务: {task_name}")

        # UI显示完成后，再执行核心任务
        OPERATIONS[task_name]["func"]()
        logger.info(f"任务完成")
    finally:
        gradient_overlay.stop_overlay()
        logger.info("✅ Overlay已关闭")

def list_operations():
    logger.info("支持的任务：")
    for k, v in sorted(OPERATIONS.items()):
        logger.info(f"  • {k:<25} | {v['desc']}")

# ====================== CLI ======================
def main():
    if args.command == "list":
        list_operations()

    elif args.command == "run":
        run_operation(args.task)

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()    
    parser = argparse.ArgumentParser(description="Windows自动化工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="列出所有任务")
    
    run_p = subparsers.add_parser("run", help="执行任务")
    run_p.add_argument("--task", required=True, help="任务名")
    run_p.add_argument("--path", help="目录路径")
    run_p.add_argument("--script", help="执行的脚本")
    run_p.add_argument("--url", help="连接地址")
    args = parser.parse_args()
   
    main()