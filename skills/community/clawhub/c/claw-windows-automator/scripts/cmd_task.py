#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: cmd_task 是一个高容错的 CMD 命令执行任务模块，用于在自动化工作流中自动打开指定目录下的命令提示符（CMD），并执行指定的命令或 .bat 脚本。
基本信息：
    模块名称：NAME = "cmd_task"
    功能描述：打开目录 → 启动CMD → 执行bat/脚本命令（支持容错继续）
核心功能（execute 函数）：
    该函数的主要作用是在指定工作目录下自动启动 CMD 并执行用户提供的命令，整个过程设计了多重容错机制，确保自动化流程更加稳定。
执行步骤：
    1、路径处理
        将传入的 work_path 转换为绝对路径（Path.resolve()）。
    2、打开 CMD 窗口（带重试）
        调用 utils.open_cmd_with_retry()（来自 CmdAutomator）打开目标文件夹下的 CMD，最多重试 max_retries 次（默认 2 次）。
    3、环境准备
        强制切换到英文输入法（ensure_english_input）
        等待窗口稳定（默认延迟 2 秒，可配置）
        设置渐变叠加提示位置到右下角
    4、执行命令
        使用 pyautogui.typewrite() 以较慢的速度逐字符输入命令（interval=0.13），避免输入过快导致丢失字符，最后按下 Enter 执行。
    5、结果处理与容错机制（核心亮点）：
        执行成功时：返回 success=True，并记录输出信息。
        执行失败时：
                    详细记录错误信息和完整 traceback
                    根据 continue_on_error 参数决定行为：
                                                    False（默认旧行为）：直接抛出异常，中断整个工作流
                                                    True（推荐）：仅记录日志，不抛异常，继续执行后续任务（强容错模式）
"""
from pathlib import Path
import pyautogui
import traceback
import gradient_overlay

# 固定必须写的
NAME = "cmd_task"
DESCRIPTION = "打开目录 → 启动CMD → 执行bat/脚本命令（支持容错继续）"

# 核心执行函数 - 增强容错版
def execute(
    work_path: str,
    script: str,
    utils,
    # 新增参数：是否继续（默认推荐开启）
    continue_on_error: bool = True,
    max_retries: int = 2,           # 自动重试次数
    delay_after_open: float = 2.0,
):
    result = {
        "success": False,
        "error": None,
        "error_type": None,
        "output": "",
        "work_path": work_path,
        "script": script
    }

    try:
        # 1. 路径解析
        oc_path = Path(work_path).resolve()

        # 2. 打开CMD（带重试）
        for attempt in range(max_retries + 1):
            try:
                cmd_window = utils.open_cmd_with_retry(oc_path)
                break
            except Exception as e:
                if attempt == max_retries:
                    raise
                utils.log_info(f"打开CMD失败，第{attempt+1}次重试...")
                pyautogui.sleep(1.5)

        # 3. 确保输入法 + 等待窗口稳定
        utils.ensure_english_input()
        utils.log_info("✅ CMD窗口已打开")
        pyautogui.sleep(delay_after_open)
        gradient_overlay.set_position("bottom-right")  
        
        # 4. 输入并执行命令
        utils.log_info(f"输入命令: {script}")
        pyautogui.typewrite(script, interval=0.13)
        pyautogui.sleep(1.0)
        pyautogui.press('enter')

        utils.log_info("✅ 命令执行完成")
        result["success"] = True
        result["output"] = "命令已成功发送至CMD"

    except Exception as e:
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        result["error"] = error_msg
        result["error_type"] = type(e).__name__
        result["output"] = error_trace

        utils.log_info(f"❌ cmd_task 执行出错: {error_msg}")
        utils.log_info(f"错误类型: {result['error_type']}")

        # 关键：根据 continue_on_error 参数决定是否抛出异常
        if not continue_on_error:
            raise  # 仍然中断工作流（兼容旧行为）

        # 如果 continue_on_error=True，就只记录日志，不抛异常
        utils.log_info("⚠️  已开启容错模式，继续执行后续步骤...")

    return result   # ← 必须返回这个字典！