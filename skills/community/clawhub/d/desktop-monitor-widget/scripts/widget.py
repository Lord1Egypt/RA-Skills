#!/usr/bin/env python3
"""
桌面监控悬浮球 - System Monitor Widget
可以贴在屏幕边缘的实时监控组件
"""

import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
import sys

class MonitorWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("系统监控")
        self.root.overrideredirect(True)  # 无边框窗口
        self.root.attributes('-topmost', True)  # 置顶
        self.root.attributes('-alpha', 0.9)  # 透明度
        
        # 窗口状态
        self.is_expanded = True
        self.last_x = 0
        self.last_y = 0
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # 创建 UI
        self.create_widgets()
        
        # 绑定事件
        self.setup_bindings()
        
        # 初始位置 - 右上角
        self.root.geometry(f"+{self.screen_width - 200}+10")
        
        # 开始更新
        self.update_data()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e', padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        self.title_label = tk.Label(
            self.main_frame,
            text="🖥️ 系统监控",
            bg='#1a1a2e',
            fg='#ffffff',
            font=('Arial', 12, 'bold')
        )
        self.title_label.pack(anchor='w')
        
        # 分隔线
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # 监控数据框架
        self.data_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        self.data_frame.pack(fill=tk.BOTH, expand=True)
        
        # CPU
        self.cpu_label = tk.Label(
            self.data_frame,
            text="CPU: --%",
            bg='#1a1a2e',
            fg='#00ff00',
            font=('Arial', 10),
            anchor='w'
        )
        self.cpu_label.pack(fill='x', pady=2)
        
        # 内存
        self.mem_label = tk.Label(
            self.data_frame,
            text="内存：--%",
            bg='#1a1a2e',
            fg='#00ffff',
            font=('Arial', 10),
            anchor='w'
        )
        self.mem_label.pack(fill='x', pady=2)
        
        # 磁盘
        self.disk_label = tk.Label(
            self.data_frame,
            text="磁盘：--%",
            bg='#1a1a2e',
            fg='#ff9900',
            font=('Arial', 10),
            anchor='w'
        )
        self.disk_label.pack(fill='x', pady=2)
        
        # 温度
        self.temp_label = tk.Label(
            self.data_frame,
            text="温度：--°C",
            bg='#1a1a2e',
            fg='#ff6666',
            font=('Arial', 10),
            anchor='w'
        )
        self.temp_label.pack(fill='x', pady=2)
        
        # 运行时间
        self.uptime_label = tk.Label(
            self.data_frame,
            text="运行：--",
            bg='#1a1a2e',
            fg='#aaaaaa',
            font=('Arial', 9),
            anchor='w'
        )
        self.uptime_label.pack(fill='x', pady=2)
        
        # 底部状态栏
        self.status_label = tk.Label(
            self.main_frame,
            text="● 实时监控中",
            bg='#1a1a2e',
            fg='#666666',
            font=('Arial', 8)
        )
        self.status_label.pack(anchor='w', pady=(10, 0))
    
    def setup_bindings(self):
        """绑定鼠标事件"""
        self.main_frame.bind('<Button-1>', self.start_move)
        self.main_frame.bind('<B1-Motion>', self.on_move)
        self.main_frame.bind('<ButtonRelease-1>', self.end_move)
        
        # 双击切换展开/折叠
        self.main_frame.bind('<Double-Button-1>', self.toggle_expand)
        
        # 鼠标悬停检测
        self.root.bind('<Enter>', self.on_enter)
        self.root.bind('<Leave>', self.on_leave)
    
    def start_move(self, event):
        """开始拖动"""
        self.last_x = event.x
        self.last_y = event.y
    
    def on_move(self, event):
        """拖动中"""
        x = self.root.winfo_x() + event.x - self.last_x
        y = self.root.winfo_y() + event.y - self.last_y
        self.root.geometry(f"+{x}+{y}")
        
        # 检查是否在边缘
        self.check_edge_position()
    
    def end_move(self, event):
        """拖动结束"""
        self.check_edge_position()
    
    def check_edge_position(self):
        """检查并处理贴边逻辑"""
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 检测是否靠近左右边缘
        edge_threshold = 50
        
        if x < edge_threshold or x + width > self.screen_width - edge_threshold:
            if self.is_expanded:
                self.collapse()
        else:
            if not self.is_expanded:
                self.expand()
    
    def collapse(self):
        """折叠窗口"""
        self.is_expanded = False
        self.data_frame.pack_forget()
        self.status_label.pack_forget()
        self.root.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")
    
    def expand(self):
        """展开窗口"""
        self.is_expanded = True
        self.data_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.status_label.pack(anchor='w', pady=(10, 0))
    
    def toggle_expand(self, event=None):
        """切换展开/折叠"""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
    
    def on_enter(self, event):
        """鼠标进入窗口"""
        self.root.attributes('-alpha', 1.0)
        if not self.is_expanded:
            self.expand()
    
    def on_leave(self, event):
        """鼠标离开窗口"""
        self.root.attributes('-alpha', 0.9)
    
    def get_cpu_temp(self):
        """获取 CPU 温度"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                            return entry.current
                for name, entries in temps.items():
                    for entry in entries:
                        return entry.current
        except:
            pass
        return None
    
    def update_data(self):
        """更新数据"""
        def update():
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_label.config(text=f"CPU: {cpu_percent}%")
            
            # 内存
            mem = psutil.virtual_memory()
            self.mem_label.config(text=f"内存：{mem.percent}%")
            
            # 磁盘
            disk = psutil.disk_usage('/')
            self.disk_label.config(text=f"磁盘：{disk.percent}%")
            
            # 温度
            temp = self.get_cpu_temp()
            if temp:
                self.temp_label.config(text=f"温度：{temp}°C")
            
            # 运行时间
            uptime = time.time() - psutil.boot_time()
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            mins = int((uptime % 3600) // 60)
            uptime_str = f"{days}天{hours}小时{mins}分" if days > 0 else f"{hours}小时{mins}分"
            self.uptime_label.config(text=f"运行：{uptime_str}")
            
            # 继续更新
            self.root.after(2000, update)
        
        update()
        self.root.mainloop()

def main():
    widget = MonitorWidget()

if __name__ == '__main__':
    main()
