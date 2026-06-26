#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书长图切割工具 - GUI 版本 v2.3
修复：
1. 切割位置偏移问题（坐标计算修正）
2. 小红书比例改为 3:4（竖版）
3. Logo 绿线实时更新

作者：咖啡豆 ☕
日期：2026-03-20
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from PIL import Image, ImageTk, ImageDraw

# 从主脚本导入核心功能
from cropper import (
    process_image, DEFAULT_WIDTH, DEFAULT_HEIGHT, LOGO_HEIGHT
)


class ImageCropperGUI:
    """飞书长图切割工具 GUI - v2.3 修复版"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("飞书长图切割工具 v2.3 - 小红书 3:4 比例")
        self.root.geometry("900x900")
        
        # 变量
        self.input_path = None
        self.output_dir = Path("./output").absolute()
        self.original_image = None
        self.display_image = None  # 缩放后的显示图片
        self.display_scale = 1.0   # 缩放比例
        self.start_y = 0           # 起始位置
        self.logo_height = LOGO_HEIGHT  # Logo 高度
        self.tk_image = None       # Tkinter 图片对象
        self.start_line = None     # 起始切割线
        self.end_line = None       # Logo 顶部线
        self.click_line = None     # 鼠标点击位置的临时线
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(
            title_frame,
            text="飞书长图切割工具 v2.3",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="鼠标点击选择切割位置 | 滚轮滑动查看 | 小红书 3:4 比例",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # 图片上传区域
        upload_frame = ttk.LabelFrame(self.root, text="1. 上传图片", padding=10)
        upload_frame.pack(fill=tk.X, padx=20, pady=10)
        
        btn_frame = ttk.Frame(upload_frame)
        btn_frame.pack()
        
        self.upload_btn = ttk.Button(
            btn_frame,
            text="📁 选择图片",
            command=self.select_image,
            width=20
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.file_label = ttk.Label(btn_frame, text="未选择文件", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # 图片预览区域（带滚动条和鼠标交互）
        preview_frame = ttk.LabelFrame(self.root, text="2. 预览长图（点击选择位置 | 滚轮滑动）", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(preview_frame, bg="#f0f0f0", highlightthickness=0, cursor="crosshair")
        self.scrollbar_y = ttk.Scrollbar(preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # 左键点击
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # 滚轮（Windows）
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_up)  # 滚轮向上（Linux）
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_down)  # 滚轮向下（Linux）
        
        # 图片显示在 Canvas 中
        self.image_on_canvas = None
        
        # 起始位置选择区域
        position_frame = ttk.LabelFrame(self.root, text="3. 切割位置设置（点击图片或拖动滑块）", padding=10)
        position_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 起始位置
        pos_top = ttk.Frame(position_frame)
        pos_top.pack(fill=tk.X)
        
        ttk.Label(pos_top, text="起始位置 Y:").pack(side=tk.LEFT, padx=5)
        
        self.start_y_var = tk.IntVar(value=0)
        self.start_y_scale = ttk.Scale(
            pos_top,
            from_=0,
            to=1000,
            variable=self.start_y_var,
            orient=tk.HORIZONTAL,
            length=400,
            command=self.on_start_y_changed
        )
        self.start_y_scale.pack(side=tk.LEFT, padx=10)
        
        self.start_y_entry = ttk.Entry(position_frame, textvariable=self.start_y_var, width=10)
        self.start_y_entry.pack(side=tk.LEFT, padx=10)
        ttk.Label(position_frame, text="px").pack(side=tk.LEFT)
        
        # Logo 设置
        logo_top = ttk.Frame(position_frame)
        logo_top.pack(fill=tk.X, pady=5)
        
        self.logo_var = tk.BooleanVar(value=True)
        self.logo_check = ttk.Checkbutton(
            logo_top,
            text="去除底部 Logo",
            variable=self.logo_var,
            command=self.on_logo_setting_changed
        )
        self.logo_check.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(logo_top, text="Logo 高度:").pack(side=tk.LEFT, padx=10)
        self.logo_height_var = tk.IntVar(value=160)  # 飞书固定值 160px
        self.logo_height_entry = ttk.Entry(logo_top, textvariable=self.logo_height_var, width=10)
        self.logo_height_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(logo_top, text="px").pack(side=tk.LEFT)
        
        # 绑定回车键事件（按回车实时更新绿线）
        self.logo_height_entry.bind("<Return>", self.on_logo_height_enter)
        
        # 图片信息
        self.info_label = ttk.Label(position_frame, text="", foreground="blue")
        self.info_label.pack(side=tk.RIGHT, padx=10)
        
        # 提示标签
        tip_frame = ttk.Frame(position_frame)
        tip_frame.pack(fill=tk.X, pady=5)
        
        self.tip_label = ttk.Label(
            tip_frame,
            text="💡 提示：在上方图片中点击任意位置，自动设置为切割起始点",
            foreground="green",
            font=("Arial", 9, "italic")
        )
        self.tip_label.pack(side=tk.LEFT)
        
        self.legend_label = ttk.Label(
            tip_frame,
            text="🔴 红线 = 起始位置  🟢 绿线 = Logo 顶部",
            foreground="purple",
            font=("Arial", 9, "bold")
        )
        self.legend_label.pack(side=tk.RIGHT)
        
        # 参数设置区域
        params_frame = ttk.LabelFrame(self.root, text="4. 切割参数（小红书 3:4 比例）", padding=10)
        params_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 第一行：目标尺寸
        ttk.Label(params_frame, text="目标宽度:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.width_var = tk.IntVar(value=1080)  # 小红书推荐宽度
        self.width_entry = ttk.Entry(params_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(params_frame, text="px").grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(params_frame, text="目标高度:").grid(row=0, column=3, sticky=tk.W, padx=5)
        self.height_var = tk.IntVar(value=1440)  # 小红书推荐高度（3:4）
        self.height_entry = ttk.Entry(params_frame, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=0, column=4, sticky=tk.W, padx=5)
        ttk.Label(params_frame, text="px (3:4)").grid(row=0, column=5, sticky=tk.W)
        
        # 第二行：输出格式
        ttk.Label(params_frame, text="输出格式:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.format_var = tk.StringVar(value="png")
        format_combo = ttk.Combobox(params_frame, textvariable=self.format_var, values=["png", "jpg"], width=8)
        format_combo.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 输出目录
        output_frame = ttk.Frame(params_frame)
        output_frame.grid(row=2, column=0, columnspan=6, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_label = ttk.Label(output_frame, text=str(self.output_dir), foreground="gray")
        self.output_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(output_frame, text="更改", command=self.select_output).pack(side=tk.LEFT)
        
        # 状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="就绪", foreground="green", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT)
        
        # 操作按钮区域（突出显示）
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # 用醒目的颜色突出开始按钮
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 开始切割",
            command=self.start_processing,
            width=20,
            bg="#4CAF50",  # 绿色背景
            fg="white",    # 白色文字
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.start_btn.config(state=tk.DISABLED)
        
        # 重置按钮
        ttk.Button(
            button_frame,
            text="🔄 重置",
            command=self.reset,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # 打开目录按钮
        ttk.Button(
            button_frame,
            text="📂 打开输出目录",
            command=self.open_output_dir,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # 绑定 Canvas 大小变化
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
    def on_canvas_resize(self, event):
        """Canvas 大小变化时更新"""
        if self.display_image:
            self.update_preview()
    
    def on_canvas_click(self, event):
        """鼠标点击 Canvas 选择起始位置"""
        if not self.original_image:
            return
        
        # 获取点击位置的 Y 坐标（考虑滚动）
        scroll_offset = self.canvas.yview()[0] * (self.original_image.height * self.display_scale)
        y_display = event.y + scroll_offset
        
        # 转换为原图的 Y 坐标
        y_original = int(y_display / self.display_scale)
        
        # 限制在有效范围内
        y_original = max(0, min(y_original, self.original_image.height))
        
        # 更新起始位置
        self.start_y = y_original
        self.start_y_var.set(y_original)
        
        # 更新信息
        self.update_info_label()
        
        # 绘制切割线
        self.draw_crop_lines(y_display)
        
        self.status_label.config(
            text=f"✅ 已选择起始位置：{y_original} px | 点击'🚀 开始切割'按钮继续",
            foreground="blue"
        )
    
    def on_mouse_wheel(self, event):
        """鼠标滚轮滚动（Windows）"""
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")
    
    def on_mouse_wheel_up(self, event):
        """鼠标滚轮向上（Linux）"""
        self.canvas.yview_scroll(-1, "units")
    
    def on_mouse_wheel_down(self, event):
        """鼠标滚轮向下（Linux）"""
        self.canvas.yview_scroll(1, "units")
    
    def on_start_y_changed(self, value):
        """起始位置变化时更新"""
        self.start_y = int(float(value))
        self.start_y_var.set(self.start_y)
        self.update_info_label()
        
        # 更新切割线位置
        if self.display_image:
            y_display = int(self.start_y * self.display_scale)
            self.draw_crop_lines(y_display)
    
    def on_logo_setting_changed(self):
        """Logo 设置变化时更新"""
        self.update_info_label()
        # 重新绘制切割线
        if self.display_image and self.start_y > 0:
            y_display = int(self.start_y * self.display_scale)
            self.draw_crop_lines(y_display)
    
    def on_logo_height_enter(self, event=None):
        """Logo 高度输入框回车键处理"""
        self.update_info_label()
        # 重新绘制切割线
        if self.display_image and self.start_y > 0:
            y_display = int(self.start_y * self.display_scale)
            self.draw_crop_lines(y_display)
        self.status_label.config(
            text=f"✅ Logo 高度已更新：{self.logo_height_var.get()} px | 绿线已更新",
            foreground="blue"
        )
    
    def update_info_label(self):
        """更新信息标签"""
        if not self.original_image:
            return
        
        logo_height = self.logo_height_var.get() if self.logo_var.get() else 0
        logo_top_y = self.original_image.height - logo_height
        
        self.info_label.config(
            text=f"原图：{self.original_image.width} x {self.original_image.height} px | "
                 f"起始：{self.start_y} px | Logo 顶部：{logo_top_y} px"
        )
    
    def draw_crop_lines(self, y_display_start):
        """绘制双切割线"""
        # 删除旧线
        if self.start_line:
            self.canvas.delete(self.start_line)
        if self.end_line:
            self.canvas.delete(self.end_line)
        if self.click_line:
            self.canvas.delete(self.click_line)
        
        # 获取 Canvas 宽度
        canvas_width = self.canvas.winfo_width()
        
        # 绘制起始位置线（红色虚线）
        self.start_line = self.canvas.create_line(
            0, y_display_start, canvas_width, y_display_start,
            fill="red", width=3, dash=(10, 5)
        )
        
        # 绘制 Logo 顶部线（绿色虚线，如果启用了 Logo 去除）
        if self.logo_var.get():
            logo_height = self.logo_height_var.get()
            logo_top_y_original = self.original_image.height - logo_height
            logo_top_y_display = int(logo_top_y_original * self.display_scale)
            
            self.end_line = self.canvas.create_line(
                0, logo_top_y_display, canvas_width, logo_top_y_display,
                fill="green", width=3, dash=(10, 5)
            )
    
    def select_image(self):
        """选择输入图片"""
        file_path = filedialog.askopenfilename(
            title="选择飞书长图",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.webp"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.input_path = file_path
            self.file_label.config(text=Path(file_path).name, foreground="black")
            self.load_preview(file_path)
            self.start_btn.config(state=tk.NORMAL)
            self.status_label.config(
                text="✅ 图片已加载 | 请点击图片选择起始位置，或直接点击'🚀 开始切割'",
                foreground="blue"
            )
            
    def load_preview(self, file_path):
        """加载完整图片预览"""
        try:
            self.original_image = Image.open(file_path)
            orig_width, orig_height = self.original_image.width, self.original_image.height
            
            # 计算缩放比例（适应 Canvas 宽度）
            canvas_width = self.canvas.winfo_width()
            if canvas_width < 10:
                canvas_width = 800  # 默认宽度
            
            self.display_scale = canvas_width / orig_width
            display_height = int(orig_height * self.display_scale)
            
            # 缩放图片用于显示
            self.display_image = self.original_image.resize(
                (canvas_width, display_height),
                Image.Resampling.LANCZOS
            )
            
            # 转换为 Tkinter 格式
            self.tk_image = ImageTk.PhotoImage(self.display_image)
            
            # 在 Canvas 中显示图片
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
            
            # 配置 Canvas 滚动区域
            self.canvas.configure(scrollregion=(0, 0, canvas_width, display_height))
            
            # 更新起始位置滑块
            self.start_y_scale.config(to=orig_height)
            self.start_y_var.set(0)
            self.start_y = 0
            
            # 更新信息
            self.update_info_label()
            
            # 更新状态
            self.status_label.config(
                text=f"✅ 已加载：{orig_width} x {orig_height} px | 请点击图片选择起始位置",
                foreground="blue"
            )
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片：{e}")
            
    def update_preview(self):
        """更新预览（当 Canvas 大小变化时）"""
        if not self.original_image:
            return
        
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 10:
            return
        
        # 重新计算缩放
        self.display_scale = canvas_width / self.original_image.width
        display_height = int(self.original_image.height * self.display_scale)
        
        # 重新缩放
        self.display_image = self.original_image.resize(
            (canvas_width, display_height),
            Image.Resampling.LANCZOS
        )
        
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        
        # 更新 Canvas 中的图片
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
        self.canvas.configure(scrollregion=(0, 0, canvas_width, display_height))
        
        # 重新绘制切割线
        if self.start_y > 0:
            y_display = int(self.start_y * self.display_scale)
            self.draw_crop_lines(y_display)
        
    def select_output(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir = Path(directory)
            self.output_label.config(text=str(self.output_dir))
            
    def start_processing(self):
        """开始处理图片"""
        if not self.input_path:
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        # 禁用按钮
        self.start_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="🔄 正在处理...", foreground="orange")
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process, daemon=True)
        thread.start()
        
    def process(self):
        """处理图片（在后台线程中运行）"""
        try:
            # 获取参数
            start_y = self.start_y_var.get()
            width = self.width_var.get()
            height = self.height_var.get()
            remove_logo = self.logo_var.get()
            logo_height = self.logo_height_var.get()
            output_format = self.format_var.get()
            
            # 处理图片
            count = process_image(
                input_path=self.input_path,
                output_dir=str(self.output_dir),
                start_y=start_y,
                width=width,
                height=height,
                remove_logo=remove_logo,
                logo_height=logo_height,
                output_format=output_format
            )
            
            # 更新 UI
            self.root.after(0, self.process_complete, count)
            
        except Exception as e:
            self.root.after(0, self.process_error, str(e))
            
    def process_complete(self, count):
        """处理完成回调"""
        self.progress.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.status_label.config(text=f"✅ 完成！生成了 {count} 张图片", foreground="green")
        
        # 自动打开输出目录
        if self.output_dir.exists():
            import os
            os.startfile(self.output_dir)
        
        messagebox.showinfo(
            "完成",
            f"🎉 切割完成！\n\n共生成了 {count} 张图片\n\n输出目录：{self.output_dir}\n\n已自动打开目录，可以直接使用图片了！"
        )
        
    def process_error(self, error_msg):
        """处理错误回调"""
        self.progress.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.status_label.config(text="❌ 处理失败", foreground="red")
        
        messagebox.showerror("错误", f"处理失败：{error_msg}")
        
    def reset(self):
        """重置"""
        self.input_path = None
        self.file_label.config(text="未选择文件", foreground="gray")
        self.canvas.delete("all")
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        self.image_on_canvas = None
        self.start_line = None
        self.end_line = None
        self.click_line = None
        self.start_btn.config(state=tk.DISABLED)
        self.status_label.config(text="就绪", foreground="green")
        self.start_y_var.set(0)
        self.width_var.set(1080)  # 小红书推荐
        self.height_var.set(1440)  # 3:4 比例
        self.logo_var.set(True)
        self.logo_height_var.set(160)  # 飞书固定值
        self.format_var.set("png")
        self.info_label.config(text="")
        
    def open_output_dir(self):
        """打开输出目录"""
        if self.output_dir.exists():
            import os
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("警告", "输出目录不存在")


def main():
    root = tk.Tk()
    app = ImageCropperGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
