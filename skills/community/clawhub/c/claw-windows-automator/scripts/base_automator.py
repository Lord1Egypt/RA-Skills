#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这是一个 Windows 自动化基础类（BaseAutomator），主要用于构建需要精确控制键盘和鼠标的 Windows 自动化脚本。
日志管理：
    使用 LoggerManager 初始化专用日志记录器（claw-windows-automator），方便后续追踪自动化执行过程。
英文输入法强制切换（ensure_english_input）：
    这是该类目前最核心的功能。
"""
import ctypes
import time
import ensure_package
from logger_manager import LoggerManager
ensure_package.pip("pyautogui")
import pyautogui

logger = LoggerManager.setup_logger(logger_name="claw-windows-automator")

class BaseAutomator:
    def __init__(self):
        pass

    def log_info(self,msg:str):
        logger.info(msg)

    def ensure_english_input(self):
        """强制切换到英文输入法"""
        logger.info("正在强制切换到英文输入法（Windows API）...")
        try:
            user32 = ctypes.windll.user32
            hkl = user32.LoadKeyboardLayoutW("00000409", 0x0001)
            if hkl:
                hwnd = user32.GetForegroundWindow()
                user32.PostMessageW(hwnd, 0x0050, 0, hkl)
                time.sleep(0.5)
                logger.info("✅ 已切换为英文输入法")
                return True
        except Exception as e:
            logger.info(f"API 切换失败: {e}")

        pyautogui.hotkey('win', 'space')
        time.sleep(0.8)
        logger.info("✅ 已切换英文输入法（热键）")
        return False