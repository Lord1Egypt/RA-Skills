#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: CmdAutomator 类继承自 BaseAutomator，是一个专门用于在 Windows 上自动打开命令提示符（CMD） 的实用自动化类。
主要功能：
    open_cmd_with_retry(folder: Path, max_retries: int = 3)
    该方法的核心功能是：打开指定文件夹，并在该文件夹路径下自动启动 CMD 命令提示符窗口，并提供失败重试机制。
执行流程：
1、打开目标文件夹
    使用 explorer.exe 打开指定的文件夹路径。
2、切换到英文输入法（继承自父类）
    调用 self.ensure_english_input() 确保输入法为英文，避免中文输入法导致命令输入异常。
3、模拟键盘操作启动 CMD：
    按 Alt + D 激活地址栏
    输入 cmd /K 并按回车（/K 参数使 CMD 窗口打开后不自动关闭）
    再次按回车确认
4、验证 CMD 是否成功打开：
    使用 pygetwindow 遍历所有窗口，查找标题中包含 “cmd” 或 “命令” 的窗口
    如果找到，则激活该窗口并返回窗口对象
    如果未找到，则进行重试（默认最多重试 3 次）
5、失败处理：
    所有重试失败后，记录错误日志并调用 sys.exit(1) 终止程序
"""
import sys
import subprocess
import ensure_package
import gradient_overlay
from pathlib import Path
from base_automator import BaseAutomator
ensure_package.pip("pyautogui")
ensure_package.pip("pygetwindow")
import pyautogui
import pygetwindow as gw

# 工具函数
# 这部分在引擎里，所有工作流都能用
class CmdAutomator(BaseAutomator):

    def open_cmd_with_retry(self,folder: Path, max_retries: int = 3):
        """打开文件夹并启动CMD"""
        self.log_info(f"打开文件夹并启动CMD: {folder}")
        gradient_overlay.update_overlay_text("打开文件夹")
        subprocess.Popen(['explorer.exe', str(folder)])
        gradient_overlay.safe_sleep(2.0)

        for attempt in range(1, max_retries + 1):
            self.log_info(f"第 {attempt}/{max_retries} 次尝试打开CMD...")
            self.ensure_english_input()

            pyautogui.hotkey('alt', 'd')
            gradient_overlay.safe_sleep(1.0)
            gradient_overlay.update_overlay_text("启动命令提示符")
            pyautogui.write('cmd /K', interval=0.08)
            gradient_overlay.safe_sleep(0.8)
            pyautogui.press('enter')
            gradient_overlay.safe_sleep(1.2)
            pyautogui.press('enter')

            gradient_overlay.safe_sleep(1.0)

            cmd_windows = [w for w in gw.getAllWindows() if w.title and (
                'cmd' in w.title.lower() or '命令' in w.title
            )]

            if cmd_windows:
                cmd_win = cmd_windows[0]
                self.log_info(f"✅ CMD已打开: {cmd_win.title}")
                try:
                    cmd_win.activate()
                except:
                    pass
                return cmd_win
            else:
                self.log_info(f"⚠️ 未找到CMD窗口，重试中...")

        self.log_info("❌ 无法打开CMD")
        sys.exit(1)