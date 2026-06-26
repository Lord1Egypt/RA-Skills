"""
FFmpeg 进度跟踪器
解析 FFmpeg 输出，实时跟踪处理进度
"""

import re
import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class ProgressUpdate:
    """进度更新数据类"""

    progress: float  # 进度百分比 (0-100)
    current_time: float  # 当前处理时间（秒）
    elapsed: float  # 已用时间（秒）
    speed: float  # 处理速度（倍速）
    remaining_seconds: float  # 预计剩余时间（秒）


class ProgressTracker:
    """FFmpeg 处理进度跟踪器"""

    def __init__(self):
        """初始化进度跟踪器"""
        self.start_time = None
        self.duration = None
        self.last_update_time = None
        self.last_current_time = None

        # FFmpeg 时间输出正则表达式：time=HH:MM:SS.MS
        self.progress_regex = re.compile(r"time=\s*(\d+):(\d+):(\d+\.\d+)")

    def start_tracking(self, duration_seconds: float) -> None:
        """
        开始跟踪

        Args:
            duration_seconds: 视频总时长（秒）
        """
        self.start_time = time.time()
        self.duration = duration_seconds
        self.last_update_time = self.start_time
        self.last_current_time = 0.0

    def update(self, ffmpeg_output: str) -> Optional[ProgressUpdate]:
        """
        解析 FFmpeg 输出，更新进度

        Args:
            ffmpeg_output: FFmpeg 输出的一行文本

        Returns:
            ProgressUpdate 对象，如果无法解析则返回 None
        """
        if self.start_time is None or self.duration is None:
            return None

        # 搜索时间信息
        match = self.progress_regex.search(ffmpeg_output)
        if not match:
            return None

        # 解析当前时间
        hours, minutes, seconds = map(float, match.groups())
        current_time = hours * 3600 + minutes * 60 + seconds

        # 防止时间倒流
        if current_time < self.last_current_time:
            return None

        # 计算进度
        if self.duration > 0:
            progress_pct = (current_time / self.duration) * 100
        else:
            progress_pct = 0.0

        # 计算已用时间
        now = time.time()
        elapsed = now - self.start_time

        # 计算处理速度（倍速）
        if elapsed > 0:
            speed = current_time / elapsed
        else:
            speed = 0.0

        # 计算预计剩余时间
        remaining = None
        if speed > 0 and self.duration > current_time:
            remaining = (self.duration - current_time) / speed

        # 更新最后的状态
        self.last_update_time = now
        self.last_current_time = current_time

        return ProgressUpdate(
            progress=progress_pct,
            current_time=current_time,
            elapsed=elapsed,
            speed=speed,
            remaining_seconds=remaining if remaining is not None else 0.0,
        )

    def get_progress(self) -> float:
        """
        获取当前进度百分比

        Returns:
            进度百分比 (0-100)
        """
        if self.duration is None or self.last_current_time is None:
            return 0.0

        return (self.last_current_time / self.duration) * 100 if self.duration > 0 else 0.0

    def reset(self) -> None:
        """重置跟踪器状态"""
        self.start_time = None
        self.duration = None
        self.last_update_time = None
        self.last_current_time = None

    def finish(self) -> None:
        """标记跟踪完成"""
        self.last_current_time = self.duration


# 使用示例
if __name__ == "__main__":
    print("=== 进度跟踪器测试 ===\n")

    tracker = ProgressTracker()

    # 示例 1：开始跟踪
    print("示例 1：开始跟踪")
    tracker.start_tracking(duration_seconds=3600)  # 1 小时视频
    print(f"开始跟踪 1 小时视频")
    print()

    # 示例 2：解析 FFmpeg 输出
    print("示例 2：解析 FFmpeg 输出")
    test_outputs = [
        "frame=  123 fps= 25 q=28.0 size=    1234kB time=00:10:30.50 bitrate= 1234.5kbits/s speed=1.23x",
        "frame=  456 fps= 30 q=25.0 size=    5678kB time=00:30:15.75 bitrate= 2345.6kbits/s speed=1.45x",
        "frame=  789 fps= 28 q=26.0 size=   12345kB time=01:00:00.00 bitrate= 3456.7kbits/s speed=1.50x",
    ]

    for i, output in enumerate(test_outputs, 1):
        print(f"\n测试输出 {i}:")
        update = tracker.update(output)
        if update:
            print(f"  进度: {update.progress:.2f}%")
            print(f"  当前时间: {update.current_time:.2f} 秒 ({update.current_time/60:.2f} 分钟)")
            print(f"  已用时间: {update.elapsed:.2f} 秒")
            print(f"  处理速度: {update.speed:.2f}x")
            print(
                f"  预计剩余: {update.remaining_seconds:.2f} 秒 ({update.remaining_seconds/60:.2f} 分钟)"
            )
        else:
            print("  无法解析进度")

    print()

    # 示例 3：获取当前进度
    print("示例 3：获取当前进度")
    current_progress = tracker.get_progress()
    print(f"当前进度: {current_progress:.2f}%")
    print()

    # 示例 4：重置
    print("示例 4：重置跟踪器")
    tracker.reset()
    print(f"重置后进度: {tracker.get_progress():.2f}%")
