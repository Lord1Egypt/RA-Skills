#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度显示 - 完整版
功能：进度条、时间统计、阶段管理
"""

from datetime import datetime
from typing import Optional, Dict, List
import sys
import time


class ProgressDisplay:
    """进度显示类"""
    
    ICONS = {
        "waiting": "⏳",
        "running": "🔄",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }
    
    def __init__(self, show_timestamp: bool = True, show_progress_bar: bool = True):
        self.show_timestamp = show_timestamp
        self.show_progress_bar = show_progress_bar
        self.current_stage = None
        self.stage_count = 0
        self.current_stage_num = 0
        self.start_time = None
        self.stage_times: Dict[int, float] = {}
    
    def _timestamp(self) -> str:
        """获取时间戳字符串"""
        if self.show_timestamp:
            return datetime.now().strftime("%H:%M:%S")
        return ""
    
    def _print(self, icon: str, message: str):
        """打印消息"""
        ts = self._timestamp()
        if ts:
            print(f"[{ts}] {icon} {message}")
        else:
            print(f"{icon} {message}")
        sys.stdout.flush()
    
    def _render_progress_bar(self, current: int, total: int, width: int = 50) -> str:
        """渲染进度条"""
        if not self.show_progress_bar:
            return ""
        
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent:.1%}"
    
    def start(self, total_stages: int, title: str = "EvoMap WorkBench"):
        """开始任务"""
        self.stage_count = total_stages
        self.current_stage_num = 0
        self.start_time = time.time()
        self.stage_times = {}
        
        print("=" * 70)
        print(f"🚀 {title}")
        print("=" * 70)
        print(f"📋 总阶段：{total_stages}")
        print(f"🕐 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
    
    def stage(self, stage_num: int, name: str, message: Optional[str] = None):
        """显示阶段开始"""
        self.current_stage_num = stage_num
        self.current_stage = name
        self.stage_times[stage_num] = time.time()
        
        progress = f"[{stage_num}/{self.stage_count}]"
        
        if self.show_progress_bar:
            bar = self._render_progress_bar(stage_num, self.stage_count)
            self._print(self.ICONS["running"], f"{progress} {name} {bar}")
        else:
            self._print(self.ICONS["running"], f"{progress} {name}")
        
        if message:
            print(f"   {message}")
            print()
    
    def stage_success(self, message: Optional[str] = None, duration: Optional[float] = None):
        """显示阶段成功"""
        extra = ""
        
        if duration:
            extra = f" (耗时：{duration:.1f}s)"
        elif self.current_stage_num in self.stage_times:
            duration = time.time() - self.stage_times[self.current_stage_num]
            extra = f" (耗时：{duration:.1f}s)"
        
        if message:
            extra = f" - {message}{extra}"
        
        self._print(self.ICONS["success"], f"{self.current_stage} 完成{extra}")
        print()
    
    def stage_error(self, error: str, recoverable: bool = True):
        """显示阶段错误"""
        status = "可恢复" if recoverable else "致命"
        self._print(self.ICONS["error"], f"{self.current_stage} 失败 [{status}]")
        print(f"   错误：{error}")
        print()
    
    def stage_warning(self, warning: str):
        """显示阶段警告"""
        self._print(self.ICONS["warning"], f"{self.current_stage} 警告")
        print(f"   {warning}")
        print()
    
    def info(self, message: str):
        """显示信息"""
        self._print(self.ICONS["info"], message)
    
    def finish(self, success: bool, summary: Dict):
        """显示任务完成"""
        print()
        print("=" * 70)
        
        if success:
            self._print(self.ICONS["success"], "任务完成")
        else:
            self._print(self.ICONS["error"], "任务失败")
        
        print()
        print("📊 执行汇总:")
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        if self.start_time:
            total_duration = time.time() - self.start_time
            print(f"   总耗时：{total_duration:.1f}s")
            print(f"   平均阶段耗时：{total_duration/self.stage_count:.1f}s" if self.stage_count > 0 else "")
        
        print()
        print(f"🕐 结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def get_elapsed_time(self) -> float:
        """获取已用时间"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
    
    def get_stage_elapsed_time(self, stage_num: int) -> float:
        """获取阶段已用时间"""
        if stage_num in self.stage_times:
            return time.time() - self.stage_times[stage_num]
        return 0.0


class PublishProgress(ProgressDisplay):
    """发布进度显示"""
    
    def __init__(self):
        super().__init__(show_timestamp=True, show_progress_bar=True)
    
    def start_publish(self, task_count: int):
        """开始发布"""
        self.start(4 + task_count, "EvoMap 资产发布")
    
    def hello_auth(self):
        """Hello 认证"""
        self.stage(1, "Hello 认证")
    
    def validate_assets(self, count: int):
        """验证资产"""
        self.stage(2, f"验证资产 ({count}个)")
    
    def dry_run(self):
        """Dry-Run 验证"""
        self.stage(3, "发布前验证")
    
    def publish_task(self, task_name: str, index: int):
        """发布任务"""
        self.stage(3 + index, f"发布：{task_name}")
    
    def generate_report(self):
        """生成报告"""
        self.stage(-1, "生成报告")


if __name__ == "__main__":
    # 测试进度显示
    progress = PublishProgress()
    progress.start_publish(3)
    
    progress.hello_auth()
    time.sleep(0.5)
    progress.stage_success("认证成功")
    
    progress.validate_assets(4)
    time.sleep(0.3)
    progress.stage_success("验证通过")
    
    progress.dry_run()
    time.sleep(0.3)
    progress.stage_success("Dry-Run 通过")
    
    for i in range(3):
        progress.publish_task(f"task-{i}", i + 1)
        time.sleep(0.5)
        progress.stage_success("发布成功")
    
    progress.generate_report()
    progress.finish(True, {
        "总任务数": 3,
        "成功": 3,
        "失败": 0
    })
