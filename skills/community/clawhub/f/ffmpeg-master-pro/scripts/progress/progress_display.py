"""
进度显示器
提供简洁的终端进度显示
"""

from typing import Optional


class SimpleProgressDisplay:
    """简洁的进度显示器"""

    def __init__(self, bar_width: int = 20):
        """
        初始化进度显示器

        Args:
            bar_width: 进度条宽度（字符数）
        """
        self.bar_width = bar_width
        self.last_width = 0

    def show(
        self, current: int, total: int, filename: str, remaining: Optional[float] = None
    ) -> None:
        """
        显示简洁的进度信息

        Args:
            current: 当前进度（已完成数量）
            total: 总数量
            filename: 当前处理的文件名
            remaining: 预计剩余时间（秒）
        """
        # 计算进度百分比
        progress_pct = (current / total) * 100 if total > 0 else 0

        # 生成进度条
        filled = int(self.bar_width * current / total) if total > 0 else 0
        bar = "=" * filled + "." * (self.bar_width - filled)

        # 格式化剩余时间
        time_str = self._format_time(remaining)

        # 构建输出
        # 处理 3/10 | video.mp4 | [=====.......] 50% | 预计 2分钟
        output = (
            f"\r处理 {current}/{total} | {filename} | [{bar}] {progress_pct:.0f}% | 预计 {time_str}"
        )

        # 清除之前的输出（处理长度变化）
        if self.last_width > len(output):
            output += " " * (self.last_width - len(output))

        self.last_width = len(output)

        # 输出到终端
        print(output, end="", flush=True)

    def clear(self) -> None:
        """清除进度显示"""
        if self.last_width > 0:
            print("\r" + " " * self.last_width + "\r", end="", flush=True)
            self.last_width = 0

    def _format_time(self, seconds: Optional[float]) -> str:
        """
        格式化时间

        Args:
            seconds: 时间（秒）

        Returns:
            格式化的时间字符串
        """
        if seconds is None:
            return "计算中..."

        if seconds < 0:
            return "未知"

        if seconds < 60:
            return f"{int(seconds)}秒"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}分钟"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}小时{minutes}分钟"


class BatchProgressDisplay:
    """批量处理进度显示器"""

    def __init__(self):
        """初始化批量进度显示器"""
        self.main_display = SimpleProgressDisplay()
        self.completed = 0
        self.failed = 0
        self.total = 0

    def start_batch(self, total: int) -> None:
        """
        开始批量处理

        Args:
            total: 总任务数
        """
        self.total = total
        self.completed = 0
        self.failed = 0
        print(f"\n开始批量处理 {total} 个文件...\n")

    def update_progress(
        self, filename: str, success: bool = True, remaining: Optional[float] = None
    ) -> None:
        """
        更新批量处理进度

        Args:
            filename: 当前文件名
            success: 是否成功
            remaining: 预计剩余时间（秒）
        """
        current = self.completed + self.failed + 1

        if success:
            self.completed += 1
        else:
            self.failed += 1

        # 显示进度
        self.main_display.show(current, self.total, filename, remaining)

    def finish_file(self, filename: str, success: bool) -> None:
        """
        完成单个文件的处理

        Args:
            filename: 文件名
            success: 是否成功
        """
        if success:
            self.completed += 1
        else:
            self.failed += 1

        # 更新显示
        current = self.completed + self.failed
        self.main_display.show(current, self.total, filename)

    def show_summary(self, total_elapsed: float = 0, total_size_mb: float = 0) -> None:
        """
        显示批量处理摘要

        Args:
            total_elapsed: 总耗时（秒）
            total_size_mb: 总输出大小（MB）
        """
        # 清除进度条
        self.main_display.clear()

        print(f"\n{'='*60}")
        print(f"批量处理完成")
        print(f"{'='*60}")
        print(f"  总计:     {self.total} 个文件")
        print(f"  成功:     {self.completed} 个")
        if self.failed > 0:
            print(f"  失败:     {self.failed} 个")
        print(
            f"  成功率:   {(self.completed/self.total*100):.1f}%"
            if self.total > 0
            else "  成功率:   0%"
        )

        if total_elapsed > 0:
            print(f"  总耗时:   {self._format_duration(total_elapsed)}")
            if self.completed > 0:
                avg_time = total_elapsed / self.completed
                print(f"  平均:     {self._format_duration(avg_time)}/文件")

        if total_size_mb > 0:
            print(f"  总大小:   {total_size_mb:.2f} MB")
            if self.completed > 0:
                avg_size = total_size_mb / self.completed
                print(f"  平均:     {avg_size:.2f} MB/文件")

        print(f"{'='*60}\n")

    def show_error(self, filename: str, error_message: str) -> None:
        """
        显示错误信息

        Args:
            filename: 文件名
            error_message: 错误信息
        """
        # 清除进度条
        self.main_display.clear()

        print(f"\n❌ 错误: {filename}")
        print(f"   {error_message}\n")

        # 重新显示进度
        current = self.completed + self.failed
        if current > 0:
            self.main_display.show(current, self.total, filename)

    def _format_duration(self, seconds: float) -> str:
        """
        格式化持续时间

        Args:
            seconds: 秒数

        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}分{secs}秒"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}小时{minutes}分"


# 使用示例
if __name__ == "__main__":
    print("=== 进度显示器测试 ===\n")

    # 示例 1：SimpleProgressDisplay
    print("示例 1：SimpleProgressDisplay")
    display = SimpleProgressDisplay()

    import time

    for i in range(1, 11):
        remaining = (10 - i) * 0.5  # 假设每个文件需要 0.5 秒
        display.show(i, 10, f"video_{i}.mp4", remaining)
        time.sleep(0.3)

    display.clear()
    print("\n")

    # 示例 2：BatchProgressDisplay
    print("示例 2：BatchProgressDisplay")
    batch_display = BatchProgressDisplay()

    batch_display.start_batch(5)

    for i in range(1, 6):
        filename = f"test_video_{i}.mp4"
        remaining = (5 - i) * 1.0
        batch_display.finish_file(filename, success=True)
        time.sleep(0.3)

    batch_display.show_summary(total_elapsed=5.0, total_size_mb=125.5)

    # 示例 3：显示错误
    print("示例 3：显示错误")
    batch_display2 = BatchProgressDisplay()
    batch_display2.start_batch(3)
    batch_display2.finish_file("video1.mp4", success=True)
    batch_display2.show_error("video2.mp4", "编码失败：码率超出范围")
    batch_display2.show_summary(total_elapsed=3.0)
