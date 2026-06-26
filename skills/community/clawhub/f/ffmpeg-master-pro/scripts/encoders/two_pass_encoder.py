"""
两遍编码器 - 精确控制文件大小
使用两遍编码策略实现精确的码率控制和文件大小管理
"""

import os
import shlex
import subprocess
import tempfile
from typing import Optional, Callable, Tuple, List
from dataclasses import dataclass
import time
import sys


@dataclass
class EncodeResult:
    """编码结果"""

    success: bool
    output_file: str = ""
    actual_size_mb: float = 0.0
    target_size_mb: float = 0.0
    error: str = ""
    pass1_time: float = 0.0
    pass2_time: float = 0.0
    video_bitrate: int = 0
    audio_bitrate: int = 0


@dataclass
class EncodeProgress:
    """编码进度"""

    pass_number: int
    current_time: float
    total_time: float
    speed: float
    percentage: float


class TwoPassEncoder:
    """两遍编码器 - 精确控制文件大小"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """
        初始化两遍编码器

        Args:
            ffmpeg_path: FFmpeg 可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.temp_dir = tempfile.gettempdir()

    def calculate_target_bitrate(
        self, target_size_mb: float, duration_seconds: float, audio_bitrate_kbps: int = 128
    ) -> int:
        """
        计算目标视频码率

        Args:
            target_size_mb: 目标文件大小（MB）
            duration_seconds: 视频时长（秒）
            audio_bitrate_kbps: 音频码率（kbps）

        Returns:
            目标视频码率（kbps）

        公式：
        目标码率 = (目标大小 * 8192) / 时长 - 音频码率
        留出 5% 的安全余量
        """
        # 目标大小转换为 KB
        target_size_kb = target_size_mb * 1024

        # 总码率（包含音频和视频），单位 kbps
        # (MB * 1024) = KB
        # (KB * 8) = Kb
        # (Kb / 秒) = kbps
        total_bitrate = (target_size_kb * 8) / duration_seconds

        # 先留出 5% 的安全余量（考虑容器开销）
        total_bitrate = total_bitrate * 0.95

        # 视频码率 = 总码率 - 音频码率
        video_bitrate = total_bitrate - audio_bitrate_kbps

        # 限制码率范围（防止极端值）
        video_bitrate = max(500, min(int(video_bitrate), 50000))

        return int(video_bitrate)

    def build_two_pass_commands(
        self,
        input_file: str,
        output_file: str,
        target_bitrate: int,
        preset: str = "medium",
        codec: str = "libx264",
        audio_codec: str = "aac",
        audio_bitrate: str = "128k",
        pixel_format: str = "yuv420p",
        extra_params: Optional[List[str]] = None,
    ) -> Tuple[str, str]:
        """
        构建两遍编码命令

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            target_bitrate: 目标视频码率（kbps）
            preset: 编码预设（ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow）
            codec: 视频编解码器
            audio_codec: 音频编解码器
            audio_bitrate: 音频码率
            pixel_format: 像素格式
            extra_params: 额外编码参数

        Returns:
            (pass1_cmd, pass2_cmd) - 两遍编码的命令
        """
        # 基础参数
        base_params = [
            self.ffmpeg_path,
            "-y",
            "-i",
            input_file,
            "-c:v",
            codec,
            "-b:v",
            f"{target_bitrate}k",
            "-preset",
            preset,
            "-pix_fmt",
            pixel_format,
        ]

        # 码率控制参数
        bitrate_params = [
            "-maxrate",
            f"{int(target_bitrate * 1.2)}k",
            "-bufsize",
            f"{int(target_bitrate * 2)}k",
        ]

        # 添加额外参数
        if extra_params:
            base_params.extend(extra_params)

        # 第一遍：分析（不输出文件）
        pass1_params = base_params.copy()
        pass1_params.extend(["-pass", "1", "-an", "-f", "null"])  # 禁用音频

        # Windows 和 Unix 的 null 设备不同
        if os.name == "nt":
            pass1_params.append("NUL")
        else:
            pass1_params.append("/dev/null")

        pass1_cmd = " ".join(pass1_params)

        # 第二遍：实际编码
        pass2_params = base_params.copy()
        pass2_params.extend(
            [
                "-pass",
                "2",
                "-passlogfile",
                os.path.join(self.temp_dir, "ffmpeg2pass"),
                "-c:a",
                audio_codec,
                "-b:a",
                audio_bitrate,
                output_file,
            ]
        )

        pass2_cmd = " ".join(pass2_params)

        return pass1_cmd, pass2_cmd

    def encode(
        self,
        input_file: str,
        output_file: str,
        target_size_mb: float,
        duration_seconds: float,
        audio_bitrate_kbps: int = 128,
        preset: str = "medium",
        codec: str = "libx264",
        progress_callback: Optional[Callable[[EncodeProgress], None]] = None,
    ) -> EncodeResult:
        """
        执行两遍编码

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            target_size_mb: 目标文件大小（MB）
            duration_seconds: 视频时长（秒）
            audio_bitrate_kbps: 音频码率（kbps）
            preset: 编码预设
            codec: 视频编解码器
            progress_callback: 进度回调函数

        Returns:
            EncodeResult 编码结果
        """
        # 验证输入文件
        if not os.path.exists(input_file):
            return EncodeResult(success=False, error=f"输入文件不存在: {input_file}")

        # 计算目标码率
        target_bitrate = self.calculate_target_bitrate(
            target_size_mb, duration_seconds, audio_bitrate_kbps
        )

        # 构建两遍编码命令
        pass1_cmd, pass2_cmd = self.build_two_pass_commands(
            input_file,
            output_file,
            target_bitrate,
            preset,
            codec,
            audio_codec="aac",
            audio_bitrate=f"{audio_bitrate_kbps}k",
        )

        print(f"开始两遍编码...")
        print(f"目标大小: {target_size_mb:.2f} MB")
        print(f"目标码率: {target_bitrate} kbps")
        print(f"编码预设: {preset}")

        # 如果有进度回调，导入进度显示器
        progress_display = None
        if progress_callback:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
                from progress import SimpleProgressDisplay

                progress_display = SimpleProgressDisplay()
            except ImportError:
                pass

        print()

        # 第一遍编码
        print(f"第一遍编码（分析）...")
        start_time = time.time()
        pass1_result = self._execute_pass(
            pass1_cmd, 1, progress_callback, duration_seconds, progress_display
        )
        pass1_time = time.time() - start_time

        if not pass1_result:
            return EncodeResult(success=False, error=f"第一遍编码失败")

        print(f"第一遍完成，耗时: {pass1_time:.2f} 秒")

        # 第二遍编码
        print(f"第二遍编码（实际编码）...")
        start_time = time.time()
        pass2_result = self._execute_pass(
            pass2_cmd, 2, progress_callback, duration_seconds, progress_display
        )
        pass2_time = time.time() - start_time

        if not pass2_result:
            return EncodeResult(success=False, error=f"第二遍编码失败")

        print(f"第二遍完成，耗时: {pass2_time:.2f} 秒")

        # 验证输出文件
        if not os.path.exists(output_file):
            return EncodeResult(success=False, error="输出文件未生成")

        # 获取实际文件大小
        actual_size_mb = os.path.getsize(output_file) / (1024 * 1024)

        # 清理临时文件
        self._cleanup_temp_files()

        return EncodeResult(
            success=True,
            output_file=output_file,
            actual_size_mb=actual_size_mb,
            target_size_mb=target_size_mb,
            pass1_time=pass1_time,
            pass2_time=pass2_time,
            video_bitrate=target_bitrate,
            audio_bitrate=audio_bitrate_kbps,
        )

    def _execute_pass(
        self,
        command: str,
        pass_number: int,
        progress_callback: Optional[Callable[[EncodeProgress], None]],
        total_duration: float,
        progress_display=None,
    ) -> bool:
        """
        执行一遍编码

        Args:
            command: FFmpeg 命令
            pass_number: 编码遍数（1 或 2）
            progress_callback: 进度回调
            total_duration: 总时长
            progress_display: 进度显示器

        Returns:
            是否成功
        """
        try:
            # 执行命令
            process = subprocess.Popen(
                shlex.split(command),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # 实时解析进度
            if progress_callback:
                self._parse_progress(
                    process.stderr, pass_number, total_duration, progress_callback, progress_display
                )

            # 等待完成
            stdout, stderr = process.communicate()

            # 检查返回码
            if process.returncode != 0:
                print(f"编码失败（第 {pass_number} 遍）:")
                print(stderr)
                return False

            return True

        except Exception as e:
            print(f"编码异常: {str(e)}")
            return False

    def _parse_progress(
        self,
        stderr_output,
        pass_number: int,
        total_duration: float,
        callback: Callable[[EncodeProgress], None],
        progress_display=None,
    ):
        """
        解析 FFmpeg 输出，提取进度信息

        Args:
            stderr_output: FFmpeg 标准错误输出
            pass_number: 当前遍数
            total_duration: 总时长
            callback: 进度回调函数
            progress_display: 进度显示器（可选）
        """
        import re

        # 匹配时间信息：time=HH:MM:SS.MS
        time_regex = re.compile(r"time=\s*(\d+):(\d+):(\d+\.\d+)")

        start_time = time.time()
        last_percentage = 0

        for line in iter(stderr_output.readline, ""):
            if not line:
                break

            match = time_regex.search(line)
            if match:
                # 解析当前时间
                hours, minutes, seconds = map(float, match.groups())
                current_time = hours * 3600 + minutes * 60 + seconds

                # 计算进度
                if total_duration > 0:
                    percentage = (current_time / total_duration) * 100
                else:
                    percentage = 0.0

                # 限制在 0-100 范围内
                percentage = min(100.0, max(0.0, percentage))

                # 计算速度
                elapsed = time.time() - start_time
                speed = current_time / elapsed if elapsed > 0 else 0.0

                # 计算剩余时间
                remaining = None
                if speed > 0 and total_duration > current_time:
                    remaining = (total_duration - current_time) / speed

                # 显示进度（每 5% 更新一次，避免过于频繁）
                if progress_display and int(percentage) > int(last_percentage):
                    pass_name = f"第{pass_number}遍"
                    progress_display.show(int(percentage), 100, f"{pass_name}编码", remaining)
                    last_percentage = percentage

                # 调用回调
                callback(
                    EncodeProgress(
                        pass_number=pass_number,
                        current_time=current_time,
                        total_time=total_duration,
                        speed=speed,
                        percentage=percentage,
                    )
                )

        # 清除进度显示
        if progress_display:
            progress_display.clear()

    def encode_batch(
        self,
        tasks: List[Tuple[str, str, float, float]],
        preset: str = "medium",
        codec: str = "libx264",
        progress_callback: Optional[Callable[[str, EncodeProgress], None]] = None,
    ) -> List[EncodeResult]:
        """
        批量两遍编码

        Args:
            tasks: 编码任务列表 [(input_file, output_file, target_size_mb, duration_seconds), ...]
            preset: 编码预设
            codec: 视频编解码器
            progress_callback: 进度回调函数 (filename, progress)

        Returns:
            编码结果列表
        """
        results = []

        for i, (input_file, output_file, target_size_mb, duration) in enumerate(tasks):
            print(f"\n处理 {i+1}/{len(tasks)}: {os.path.basename(input_file)}")

            def wrapper_callback(progress: EncodeProgress):
                if progress_callback:
                    progress_callback(os.path.basename(input_file), progress)

            result = self.encode(
                input_file,
                output_file,
                target_size_mb,
                duration,
                preset=preset,
                codec=codec,
                progress_callback=wrapper_callback,
            )

            results.append(result)

            # 显示统计信息
            if result.success:
                size_error = (
                    abs(result.actual_size_mb - result.target_size_mb) / result.target_size_mb * 100
                )
                print(
                    f"完成: 目标 {result.target_size_mb:.2f} MB -> 实际 {result.actual_size_mb:.2f} MB (误差 {size_error:.2f}%)"
                )
            else:
                print(f"失败: {result.error}")

        return results

    def _cleanup_temp_files(self):
        """清理两遍编码的临时文件"""
        temp_files = [
            os.path.join(self.temp_dir, "ffmpeg2pass-0.log"),
            os.path.join(self.temp_dir, "ffmpeg2pass-0.log.mbtree"),
        ]

        for file in temp_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except:
                    pass


# 使用示例
if __name__ == "__main__":
    print("=== 两遍编码器测试 ===\n")

    encoder = TwoPassEncoder()

    # 示例 1：计算目标码率
    print("示例 1：计算目标码率")
    target_bitrate = encoder.calculate_target_bitrate(
        target_size_mb=100, duration_seconds=3600, audio_bitrate_kbps=128
    )
    print(f"目标大小: 100 MB, 时长: 1 小时")
    print(f"计算得到视频码率: {target_bitrate} kbps")
    print()

    # 示例 2：构建两遍编码命令
    print("示例 2：构建两遍编码命令")
    pass1_cmd, pass2_cmd = encoder.build_two_pass_commands(
        input_file="input.mp4", output_file="output.mp4", target_bitrate=1500, preset="medium"
    )
    print(f"第一遍命令:\n{pass1_cmd}\n")
    print(f"第二遍命令:\n{pass2_cmd}\n")

    # 示例 3：进度回调
    print("示例 3：进度回调测试")

    def progress_handler(progress: EncodeProgress):
        print(
            f"第 {progress.pass_number} 遍: {progress.percentage:.1f}% - 速度: {progress.speed:.2f}x"
        )

    print("（需要实际视频文件才能测试）")
