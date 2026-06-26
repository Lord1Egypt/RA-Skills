#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: claw-windows-automator
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: AutomationOverlay 是一个功能强大的 Windows 自动化可视化提示与安全退出模块，使用 tkinter 实现半透明全屏遮罩 + 实时文字提示，专门为长时间运行的自动化脚本提供友好交互和紧急停止能力。
核心功能：
    双层全屏遮罩：
        底层：半透明黑色全屏遮罩（α=0.5），阻止用户误操作
        上层：透明文字显示层，显示当前任务状态和大标题
    实时动态提示：
        支持随时更新任务标题文字（update_overlay_text）
        支持设置提示文字位置（居中、左上、右上、左下、右下五种位置）
        支持动态调整字体大小（标题和提示文字可分别设置）
    鼠标单击强制退出（核心安全机制）：
        用户点击鼠标左键即可立即终止整个自动化程序
        支持设置外部终止回调函数（on_terminate），让主程序能及时感知并清理资源
    安全睡眠函数（safe_sleep）：
        在等待过程中持续刷新界面，防止界面卡死
        同时保持对鼠标单击退出的响应能力
主要特性：
    高兼容性：通过 ctypes 处理 DPI 感知问题，适配高分辨率屏幕
    点击穿透：底层遮罩层设置为点击穿透（鼠标可穿透操作下方窗口）
    优雅清理：退出时自动解绑事件、销毁控件、垃圾回收
    外部友好接口：提供了简洁的函数式接口（start_overlay、update_overlay_text、stop_overlay、set_position、set_font_size、safe_sleep），便于其他模块调用
    实时刷新：refresh() 方法保证界面在长时间运行时不会假死
"""
import tkinter as tk
import ctypes
import gc
import sys
import time
from typing import Optional, Callable
from logger_manager import LoggerManager
logger = LoggerManager.setup_logger(logger_name="claw-windows-automator")

class AutomationOverlay:
    def __init__(self):
        self.root: Optional[tk.Tk] = None
        self.text_win: Optional[tk.Tk] = None
        self.frame = None
        self.label1 = None          # 任务标题标签（支持动态更新）
        self.label2 = None
        self.terminate_callback: Optional[Callable] = None
        #当前位置，默认居中
        self.current_position: str = "bottom-right"
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()

    def set_terminate_callback(self, callback: Optional[Callable] = None):
        if callable(callback):
            self.terminate_callback = callback
            logger.info("✅ 已设置鼠标单击终止回调函数")
        else:
            self.terminate_callback = None

    def show(self, task_name: str = "自动化运行中"):
        """task_name: 不传或传空字符串时使用默认文本"""
        if self.root or self.text_win:
            return

        # 全屏遮罩层（保持不变）
        self.root = tk.Tk()
        self.root.title("Overlay_Bg")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)
        self.root.configure(bg="black")
        self.root.update_idletasks()
        self._set_click_through(self.root.winfo_id())

        # 文字显示层
        self.text_win = tk.Tk()
        self.text_win.title("Overlay_Text")
        self.text_win.geometry(f"{screen_w}x{screen_h}+0+0")
        self.text_win.overrideredirect(True)
        self.text_win.attributes("-topmost", True)
        self.text_win.attributes("-transparentcolor", "black")
        self.text_win.configure(bg="black")

        self.frame = tk.Frame(self.text_win, bg="black")
        #self.frame.place(relx=0.5, rely=0.45, anchor="center")

        # 初始位置显示
        self._place_frame()
        # ==================== 关键修改：支持动态更新 ====================
        default_text = "🚀 自动化运行中" if not task_name or task_name.strip() == "" else f"{task_name}"

        self.label1 = tk.Label(
            self.frame, 
            text=default_text,                    # 默认文本
            font=("Microsoft YaHei", 60, "bold"),
            fg="#00ff41", bg="black"
        )
        self.label1.pack()

        # 🔴 修改1：更新提示文字为鼠标单击
        self.label2 = tk.Label(
            self.frame, 
            text="正在自动化操作，请勿移动鼠标/键盘...\n单击鼠标左键可强制退出",
            font=("Microsoft YaHei", 20),
            fg="white", bg="black", pady=20
        )
        self.label2.pack()

        # 🔴 修改2：绑定鼠标左键单击事件
        self.root.bind("<Button-1>", self._force_exit)
        self.text_win.bind("<Button-1>", self._force_exit)

        self.root.update()
        self.text_win.update()
        logger.info("✅ Overlay 已启动")

    # ====================== 新增：实时更新 label1 文本 ======================
    def update_task_text(self, new_text: str):
        """外部实时动态更新任务标题文本（不传或空字符串会恢复默认）"""
        if self.label1:
            try:
                display_text = "🚀 自动化运行中" if not new_text or new_text.strip() == "" else f"{new_text}"
                self.label1.config(text=display_text)
                # 强制立即刷新显示
                if self.text_win:
                    self.text_win.update_idletasks()
                logger.info(f"🔄 任务文本已更新 → {display_text}")
            except Exception as e:
                logger.info(f"⚠️ 更新任务文本失败: {e}")

    def _set_click_through(self, hwnd):
        try:
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style | 0x80000 | 0x20)
        except Exception:
            pass

    def _force_exit(self, event=None):
        """【修改】鼠标单击：先通知外部 → 关闭UI → 强制终止整个程序"""
        logger.info("\n🚨 单击鼠标，强制终止所有任务！")

        # 【核心修改】先调用外部回调，通知“程序已终止”
        if self.terminate_callback:
            try:
                self.terminate_callback()
                logger.info("✅ 已通过回调通知外部：当前程序已终止")
            except Exception as e:
                logger.info(f"⚠️ 回调函数执行异常: {e}")

        self.hide()
        gc.collect()
        sys.exit(0)  # 保持原有强制退出行为

    def refresh(self):
        try:
            if self.root: self.root.update()
            if self.text_win: self.text_win.update()
        except tk.TclError:
            self.hide()

    def hide(self):
        try:
            # 🔴 修改3：解绑鼠标单击事件
            if self.root: self.root.unbind("<Button-1>")
            if self.text_win: self.text_win.unbind("<Button-1>")
            if self.label2: self.label2.destroy()
            if self.label1: self.label1.destroy()
            if self.frame: self.frame.destroy()
            if self.text_win: self.text_win.destroy()
            if self.root: self.root.destroy()
        except:
            pass
        
        self.label1 = self.label2 = self.frame = self.text_win = self.root = None
        self.terminate_callback = None  # 清理回调
        gc.collect()

    def set_position(self, position: str = "center"):
        """
        将文本显示位置设置为屏幕指定角落
        支持: "center", "top-left", "top-right", "bottom-left", "bottom-right"
        """
        if not self.frame or not self.text_win:
            logger.warning("⚠️ 请先调用 show() 后再设置位置")
            return

        pos = position.strip().lower()
        valid_positions = {"center", "top-left", "top-right", "bottom-left", "bottom-right"}

        if pos not in valid_positions:
            logger.warning(f"⚠️ 无效位置 '{position}'，已回退到 center")
            pos = "center"

        self.current_position = pos
        self._place_frame()
        self.text_win.update_idletasks()
        logger.info(f"📍 文本位置已切换 → {pos}")

    def _place_frame(self):
        """内部方法：根据当前 position 重新放置 frame"""
        if self.current_position == "center":
            self.frame.place(relx=0.5, rely=0.45, anchor="center")
        elif self.current_position == "top-left":
            self.frame.place(relx=0.02, rely=0.05, anchor="nw")   # 左上角，留一点边距
        elif self.current_position == "top-right":
            self.frame.place(relx=0.98, rely=0.05, anchor="ne")   # 右上角
        elif self.current_position == "bottom-left":
            self.frame.place(relx=0.02, rely=0.95, anchor="sw")   # 左下角
        elif self.current_position == "bottom-right":
            self.frame.place(relx=0.98, rely=0.95, anchor="se")   # 右下角

    def set_font_size(self, title_size: int = 60, tip_size: int = 20):
            """
            动态设置字体大小
            title_size: 第一行大标题字体大小（默认60）
            tip_size:   第二行提示文字字体大小（默认20）
            """
            # 更新内部记录
            self.current_title_size = max(20, int(title_size))   # 防止设置过小
            self.current_tip_size = max(10, int(tip_size))

            # 如果已经显示，则立即应用新字体大小
            if self.label1 and self.label2:
                try:
                    self.label1.config(font=("Microsoft YaHei", self.current_title_size, "bold"))
                    self.label2.config(font=("Microsoft YaHei", self.current_tip_size))
                    
                    if self.text_win:
                        self.text_win.update_idletasks()
                    
                    logger.info(f"🔠 字体大小已更新 → 标题: {self.current_title_size}，提示: {self.current_tip_size}")
                except Exception as e:
                    logger.warning(f"⚠️ 设置字体大小失败: {e}")

overlay = AutomationOverlay()

# ====================== 调用接口（已优化） ======================
def start_overlay(task_name: str = "🚀自动化运行中", on_terminate: Optional[Callable] = None):
    if on_terminate:
        overlay.set_terminate_callback(on_terminate)
    overlay.show(task_name)


def update_overlay_text(new_text: str):
    """外部随时调用此函数实时更新上方大标题"""
    overlay.update_task_text(new_text)

def stop_overlay():
    overlay.hide()

def set_position(position: str = "center"):
    overlay.set_position(position)

def set_font_size(title_size: int = 60, tip_size: int = 20):
    overlay.set_font_size(title_size,tip_size)

def safe_sleep(seconds: float):
    start = time.time()
    while time.time() - start < seconds:
        overlay.refresh()
        time.sleep(0.01)

if __name__ == "__main__":
    terminated_flag = [False]

    def on_overlay_terminated():
        """ESC按下时，外部程序会立刻收到通知"""
        terminated_flag[0] = True
        print("\n🔴 【外部收到通知】AutomationOverlay 已通过ESC强制终止！")
        print("   → 正在停止所有后续任务...")

    start_overlay("正在批量处理报表...",
                  on_terminate=on_overlay_terminated)   # 可以不传，或传空字符串使用默认

    print("正在执行自动化逻辑...")
    try:
        for i in range(8):
            if terminated_flag[0]:
                break

            print(f"处理第 {i+1} 步...")
            
            # 示例：实时动态更新文本
            if i == 2:
                update_overlay_text("正在读取数据...")
                set_position("bottom-right")
            elif i == 4:
                update_overlay_text("正在生成报表...")
            elif i == 6:
                update_overlay_text("正在保存文件...")

            safe_sleep(1.5)
    except Exception as e:
        print(f"任务被异常终止: {e}")

    # 结束处理
    if not terminated_flag[0]:
        stop_overlay()
        print("✅ 任务正常完成，遮罩已关闭")
    else:
        print("🚨 程序已被ESC强制终止，无需再次关闭遮罩")