"""
BiliYouTik2Brain — 终端任务感知 (Phase 3.2)

轻量级用户活动检测器，纯 stdlib，零依赖。
检测用户当前终端活跃度，使系统在用户活跃时"让路"，
在闲置时"加速"retry/重转录任务。

检测维度:
  1. 系统总进程数 — 用户活跃时进程数通常较高
  2. 最近1分钟CPU负载变化 — 用户操作→CPU波动→活越
  3. 控制台/终端进程活跃 — 是否有活跃shell/cmd
  4. 最近一次检测的时间间隔 — 越久无变化越可能闲置

策略:
  - ACTIVITY_HIGH: 用户正在操作 → 延迟后台任务
  - ACTIVITY_LOW: 用户可能离开 → 加速后台任务
  - ACTIVITY_IDLE: 确定闲置 → 全力后台处理

用法:
  from .activity_monitor get_activity_level
  level = get_activity_level()
"""

from __future__ import annotations

import os
import sys
import time
import subprocess
from typing import Optional, Tuple, Dict

# ── 活动等级 ──
ACTIVITY_HIGH = "high"    # 用户活跃→让路
ACTIVITY_LOW = "low"      # 用户可能离开→适度加速
ACTIVITY_IDLE = "idle"    # 确定闲置→全力处理


def _count_processes() -> int:
    """统计系统运行中进程数（近似用户活动量）
    
    Windows: tasklist /FI "STATUS eq RUNNING"
    Linux/macOS: ps -e | wc -l
    """
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FI", "STATUS eq RUNNING"],
                capture_output=True, text=True, timeout=10,
                errors="replace",
            )
            if result.returncode == 0:
                lines = [l.strip() for l in result.stdout.split("\n") if l.strip()]
                # tasklist 前4行是 header/footer，跳过
                return max(0, len(lines) - 4)
            return 0
        else:
            result = subprocess.run(
                ["ps", "-e"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return len(result.stdout.strip().split("\n"))
            return 0
    except Exception:
        return 0


def _count_console_processes() -> int:
    """统计控制台/终端相关进程数
    
    用户打开终端 = 可能正在操作。
    Windows 检测 conhost.exe, cmd.exe, powershell.exe, WindowsTerminal.exe
    Linux/macOS 检测 bash, zsh, fish, tmux, screen
    """
    console_keywords = []
    if sys.platform == "win32":
        console_keywords = ["conhost.exe", "cmd.exe", "powershell.exe",
                            "WindowsTerminal.exe", "pwsh.exe"]
    else:
        console_keywords = ["bash", "zsh", "fish", "tmux", "screen",
                            "terminal", "alacritty", "kitty"]
    
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FO", "CSV"],
                capture_output=True, text=True, timeout=10,
                errors="replace",
            )
            if result.returncode != 0:
                return 0
            count = 0
            for kw in console_keywords:
                if kw.lower() in result.stdout.lower():
                    # 每行出现计数
                    count += result.stdout.lower().count(kw.lower())
            return count
        else:
            result = subprocess.run(
                ["ps", "-e", "-o", "comm="],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                return 0
            count = 0
            for line in result.stdout.split("\n"):
                cmd = line.strip()
                if any(kw in cmd.lower() for kw in console_keywords):
                    count += 1
            return count
    except Exception:
        return 0


def _get_cpu_avg() -> Tuple[float, float, float]:
    """获取系统CPU负载（1/5/15分钟）
    
    Windows: 无内置平均负载，返回 (0,0,0)
    Linux: /proc/loadavg
    macOS: sysctl vm.loadavg
    """
    if sys.platform == "linux":
        try:
            with open("/proc/loadavg") as f:
                parts = f.read().strip().split()
                return (float(parts[0]), float(parts[1]), float(parts[2]))
        except Exception:
            return (0, 0, 0)
    elif sys.platform == "darwin":
        try:
            result = subprocess.run(
                ["sysctl", "vm.loadavg"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split("{")[1].split("}")[0].split()
                return (float(parts[0]), float(parts[1]), float(parts[2]))
        except Exception:
            return (0, 0, 0)
    else:
        return (0, 0, 0)


class ActivityMonitor:
    """终端活动检测器
    
    用法:
        monitor = ActivityMonitor()
        level = monitor.get_level()  # "high" | "low" | "idle"
        stats = monitor.get_stats()  # 详细统计
    """

    def __init__(self, idle_threshold: int = 5, active_threshold: int = 20):
        """
        Args:
            idle_threshold: 闲置判定阈值（连续多少次检测保持低活动）
            active_threshold: 活跃判定阈值（进程数超过此值）
        """
        self._last_level = ACTIVITY_LOW
        self._idle_count = 0
        self._active_count = 0
        self._last_check = time.time()
        self._history: Dict[str, list] = {
            "processes": [],
            "consoles": [],
            "timestamps": [],
        }
        
        self._idle_threshold = idle_threshold
        self._active_threshold = active_threshold
        
        # 基线校准（第一次检测建立基线）
        self._baseline_processes = _count_processes()
        self._baseline_consoles = _count_console_processes()

    def get_level(self) -> str:
        """获取当前活动等级
        
        Returns:
            ACTIVITY_HIGH | ACTIVITY_LOW | ACTIVITY_IDLE
        """
        proc_count = _count_processes()
        console_count = _count_console_processes()
        now = time.time()
        
        # 记录历史
        self._history["processes"].append(proc_count)
        self._history["consoles"].append(console_count)
        self._history["timestamps"].append(now)
        
        # 保留最近 5 个样本
        max_history = 5
        for k in self._history:
            if len(self._history[k]) > max_history:
                self._history[k] = self._history[k][-max_history:]
        
        # 判定标准
        proc_delta = proc_count - self._baseline_processes
        time_delta = now - self._last_check
        
        # 1. 活跃判定：进程数显著多于基线 或 有活跃终端
        if proc_delta > self._active_threshold or console_count > 2:
            self._last_level = ACTIVITY_HIGH
            self._idle_count = 0
            self._active_count += 1
        # 2. 闲置判定：连续多次检测无变化
        elif proc_delta < 5 and console_count <= 1 and time_delta > 30:
            self._idle_count += 1
            self._active_count = 0
            if self._idle_count >= self._idle_threshold:
                self._last_level = ACTIVITY_IDLE
            else:
                self._last_level = ACTIVITY_LOW
        else:
            # 适度
            self._idle_count = 0
            self._active_count = 0
            self._last_level = ACTIVITY_LOW
        
        self._last_check = now
        return self._last_level

    def get_stats(self) -> dict:
        """获取详细统计"""
        return {
            "level": self._last_level,
            "level_label": {
                ACTIVITY_HIGH: "硬件操作中",
                ACTIVITY_LOW: "可能闲置",
                ACTIVITY_IDLE: "已闲置",
            }.get(self._last_level, "未知"),
            "processes": _count_processes(),
            "consoles": _count_console_processes(),
            "baseline_processes": self._baseline_processes,
            "baseline_consoles": self._baseline_consoles,
            "idle_count": self._idle_count,
            "active_count": self._active_count,
            "idle_threshold": self._idle_threshold,
            "active_threshold": self._active_threshold,
            "seconds_since_last_check": round(time.time() - self._last_check, 1),
            "history_sample_count": len(self._history["timestamps"]),
        }

    def suggest_throttle(self) -> dict:
        """基于活动等级给出限速建议
        
        Returns:
            dict with:
                - sleep_between_tasks: float (秒)
                - max_concurrent: int
                - allow_retry: bool
                - reason: str
        """
        level = self.get_level()
        
        if level == ACTIVITY_HIGH:
            return {
                "sleep_between_tasks": 3.0,
                "max_concurrent": 1,
                "allow_retry": False,
                "reason": "用户活跃，后台任务让路，只做低优先级轻活",
            }
        elif level == ACTIVITY_LOW:
            return {
                "sleep_between_tasks": 1.0,
                "max_concurrent": 2,
                "allow_retry": True,
                "reason": "用户可能闲置，适度加速后台处理",
            }
        else:  # ACTIVITY_IDLE
            return {
                "sleep_between_tasks": 0.0,
                "max_concurrent": 4,
                "allow_retry": True,
                "reason": "用户已闲置，全力进行后台重转录和升级",
            }


# ═══════════════════════════════════════════════════════════════
# 便捷单例 — 推荐使用
# ═══════════════════════════════════════════════════════════════

_global_monitor: Optional[ActivityMonitor] = None


def get_activity_monitor() -> ActivityMonitor:
    """获取全局 ActivityMonitor 单例"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = ActivityMonitor()
    return _global_monitor


def get_activity_level() -> str:
    """快捷获取当前活动等级"""
    return get_activity_monitor().get_level()


def suggest_throttle() -> dict:
    """快捷获取当前限速建议"""
    return get_activity_monitor().suggest_throttle()
