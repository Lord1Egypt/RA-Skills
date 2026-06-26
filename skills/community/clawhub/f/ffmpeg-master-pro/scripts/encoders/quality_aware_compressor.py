"""
质量感知压缩器 - 智能压缩到目标文件大小同时保证质量
结合两遍编码和自适应码率控制，实现精确的文件大小控制和质量保证
"""

import os
import subprocess
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from .two_pass_encoder import TwoPassEncoder
from .adaptive_bitrate import AdaptiveBitrateController


class QualityMetric(Enum):
    """质量评估指标类型"""

    PSNR = "psnr"  # 峰值信噪比
    SSIM = "ssim"  # 结构相似性
    VMAF = "vmaf"  # Netflix VMAF
    BASIC = "basic"  # 基础检查（文件大小、码率）


@dataclass
class QualityScore:
    """质量评分"""

    metric: QualityMetric
    score: float  # 质量分数（0-100 或 0-1）
    passed: bool  # 是否通过最低质量要求
    details: str = ""
    psnr: Optional[float] = None
    ssim: Optional[float] = None
    vmaf: Optional[float] = None


@dataclass
class CompressResult:
    """压缩结果"""

    success: bool
    output_file: str = ""
    actual_size_mb: float = 0.0
    target_size_mb: float = 0.0
    error_pct: float = 0.0
    quality_score: Optional[QualityScore] = None
    attempts: int = 0
    final_bitrate: int = 0
    error: str = ""
    encoding_time: float = 0.0


class QualityAwareCompressor:
    """质量感知压缩器"""

    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        """
        初始化质量感知压缩器

        Args:
            ffmpeg_path: FFmpeg 可执行文件路径
            ffprobe_path: FFprobe 可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self.encoder = TwoPassEncoder(ffmpeg_path)
        self.adaptive_controller = AdaptiveBitrateController(ffmpeg_path)

        # 质量阈值
        self.quality_thresholds = {
            QualityMetric.PSNR: 30.0,  # PSNR > 30dB 认为可接受
            QualityMetric.SSIM: 0.90,  # SSIM > 0.90 认为可接受
            QualityMetric.VMAF: 70.0,  # VMAF > 70 认为可接受
            QualityMetric.BASIC: 0.0,  # 基础检查不设阈值
        }

    def compress_to_size(
        self,
        input_file: str,
        target_size_mb: float,
        min_quality: float = 0.7,
        max_attempts: int = 3,
        duration_seconds: float = 0.0,
        audio_bitrate_kbps: int = 128,
        preset: str = "medium",
        codec: str = "libx264",
        enable_quality_check: bool = False,
    ) -> CompressResult:
        """
        压缩到目标文件大小，同时保证最低质量

        Args:
            input_file: 输入文件路径
            target_size_mb: 目标文件大小（MB）
            min_quality: 最低可接受质量（0-1）
            max_attempts: 最大尝试次数
            duration_seconds: 视频时长（秒），如果为 0 则自动检测
            audio_bitrate_kbps: 音频码率（kbps）
            preset: 编码预设
            codec: 视频编解码器
            enable_quality_check: 是否启用质量检查（PSNR/SSIM/VMAF）

        Returns:
            CompressResult 压缩结果
        """
        import time

        # 验证输入文件
        if not os.path.exists(input_file):
            return CompressResult(success=False, error=f"输入文件不存在: {input_file}")

        # 获取视频时长
        if duration_seconds <= 0:
            duration_seconds = self._get_video_duration(input_file)
            if duration_seconds <= 0:
                return CompressResult(success=False, error="无法获取视频时长")

        # 判断是否需要两遍编码
        if not self._should_use_two_pass(target_size_mb, duration_seconds):
            print("文件较小或压缩比低，使用单遍编码即可")

            # 使用单遍编码
            return self._single_pass_compress(
                input_file, target_size_mb, duration_seconds, audio_bitrate_kbps, preset, codec
            )

        # 使用两遍编码 + 自适应码率调整
        print("使用两遍编码 + 自适应码率控制")

        start_time = time.time()

        optimize_result = self.adaptive_controller.optimize_bitrate(
            input_file,
            input_file.replace(".mp4", "_compressed.mp4"),
            target_size_mb,
            duration_seconds,
            audio_bitrate_kbps,
            max_attempts=max_attempts,
            preset=preset,
            codec=codec,
        )

        encoding_time = time.time() - start_time

        if not optimize_result.success:
            return CompressResult(
                success=False, error=optimize_result.error, attempts=optimize_result.attempts
            )

        # 质量检查（如果启用）
        quality_score = None
        if enable_quality_check:
            quality_score = self.assess_quality(
                input_file, optimize_result.output_file, QualityMetric.BASIC
            )

        return CompressResult(
            success=True,
            output_file=optimize_result.output_file,
            actual_size_mb=optimize_result.actual_size_mb,
            target_size_mb=optimize_result.target_size_mb,
            error_pct=optimize_result.error_pct,
            quality_score=quality_score,
            attempts=optimize_result.attempts,
            final_bitrate=optimize_result.final_bitrate,
            encoding_time=encoding_time,
        )

    def assess_quality(
        self,
        input_file: str,
        output_file: str,
        metric: QualityMetric = QualityMetric.BASIC,
        reference_quality: Optional[float] = None,
    ) -> QualityScore:
        """
        评估视频质量

        Args:
            input_file: 原始视频文件
            output_file: 压缩后的视频文件
            metric: 使用的质量评估指标
            reference_quality: 参考质量分数（用于比较）

        Returns:
            QualityScore 质量评分
        """
        if metric == QualityMetric.BASIC:
            return self._basic_quality_check(input_file, output_file)
        elif metric == QualityMetric.PSNR:
            return self._calculate_psnr(input_file, output_file)
        elif metric == QualityMetric.SSIM:
            return self._calculate_ssim(input_file, output_file)
        elif metric == QualityMetric.VMAF:
            return self._calculate_vmaf(input_file, output_file)
        else:
            return QualityScore(
                metric=QualityMetric.BASIC,
                score=0.0,
                passed=False,
                details=f"不支持的质量指标: {metric}",
            )

    def _should_use_two_pass(self, target_size_mb: float, duration_seconds: float) -> bool:
        """
        判断是否应该使用两遍编码

        Args:
            target_size_mb: 目标文件大小
            duration_seconds: 视频时长

        Returns:
            是否使用两遍编码
        """
        # 计算平均码率
        avg_bitrate = (target_size_mb * 8 * 1024) / duration_seconds

        # 判断标准：
        # 1. 文件较大（> 50MB）
        # 2. 压缩比较高（平均码率 < 2000 kbps）
        # 3. 时长足够（> 60 秒）

        should_use = target_size_mb > 50 or avg_bitrate < 2000 or duration_seconds > 60

        return should_use

    def _single_pass_compress(
        self,
        input_file: str,
        target_size_mb: float,
        duration_seconds: float,
        audio_bitrate_kbps: int,
        preset: str,
        codec: str,
    ) -> CompressResult:
        """
        单遍编码压缩（适用于小文件或低压缩比场景）

        Args:
            input_file: 输入文件
            target_size_mb: 目标大小
            duration_seconds: 时长
            audio_bitrate_kbps: 音频码率
            preset: 预设
            codec: 编解码器

        Returns:
            压缩结果
        """
        import time

        start_time = time.time()

        # 计算目标码率
        target_bitrate = self.encoder.calculate_target_bitrate(
            target_size_mb, duration_seconds, audio_bitrate_kbps
        )

        output_file = input_file.replace(".mp4", "_compressed.mp4")

        # 构建单遍编码命令（使用 CRF 模式）
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i",
            input_file,
            "-c:v",
            codec,
            "-b:v",
            f"{target_bitrate}k",
            "-maxrate",
            f"{int(target_bitrate * 1.2)}k",
            "-bufsize",
            f"{int(target_bitrate * 2)}k",
            "-preset",
            preset,
            "-c:a",
            "aac",
            "-b:a",
            f"{audio_bitrate_kbps}k",
            "-pix_fmt",
            "yuv420p",
            output_file,
        ]

        # 执行命令
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            encoding_time = time.time() - start_time

            if result.returncode != 0:
                return CompressResult(success=False, error=f"编码失败: {result.stderr}", attempts=1)

            # 验证输出
            if not os.path.exists(output_file):
                return CompressResult(success=False, error="输出文件未生成", attempts=1)

            actual_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            error_pct = abs(actual_size_mb - target_size_mb) / target_size_mb

            return CompressResult(
                success=True,
                output_file=output_file,
                actual_size_mb=actual_size_mb,
                target_size_mb=target_size_mb,
                error_pct=error_pct,
                attempts=1,
                final_bitrate=target_bitrate,
                encoding_time=encoding_time,
            )

        except Exception as e:
            return CompressResult(success=False, error=f"编码异常: {str(e)}", attempts=1)

    def _basic_quality_check(self, input_file: str, output_file: str) -> QualityScore:
        """
        基础质量检查（文件大小、码率、分辨率）

        Args:
            input_file: 输入文件
            output_file: 输出文件

        Returns:
            质量评分
        """
        try:
            # 获取文件信息
            input_info = self._get_video_info(input_file)
            output_info = self._get_video_info(output_file)

            # 计算压缩比
            compression_ratio = input_info["size_mb"] / output_info["size_mb"]

            # 检查分辨率
            resolution_preserved = (
                input_info["width"] == output_info["width"]
                and input_info["height"] == output_info["height"]
            )

            # 检查时长
            duration_preserved = abs(input_info["duration"] - output_info["duration"]) < 0.1

            # 综合评分
            score = 0.0
            if compression_ratio > 1.0:
                score += 0.3
            if resolution_preserved:
                score += 0.4
            if duration_preserved:
                score += 0.3

            passed = score >= 0.7

            details = (
                f"压缩比: {compression_ratio:.2f}x, "
                f"分辨率: {'保持' if resolution_preserved else '改变'}, "
                f"时长: {'保持' if duration_preserved else '改变'}"
            )

            return QualityScore(
                metric=QualityMetric.BASIC, score=score, passed=passed, details=details
            )

        except Exception as e:
            return QualityScore(
                metric=QualityMetric.BASIC,
                score=0.0,
                passed=False,
                details=f"质量检查失败: {str(e)}",
            )

    def _calculate_psnr(self, input_file: str, output_file: str) -> QualityScore:
        """
        计算 PSNR（峰值信噪比）

        Args:
            input_file: 输入文件
            output_file: 输出文件

        Returns:
            质量评分
        """
        try:
            # 使用 FFmpeg 的 psnr 滤镜
            cmd = [
                self.ffmpeg_path,
                "-i",
                input_file,
                "-i",
                output_file,
                "-lavfi",
                "psnr",
                "-f",
                "null",
                "-",
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            # 解析输出
            import re

            psnr_match = re.search(r"PSNR.*y:([\d.]+)", result.stderr)

            if psnr_match:
                psnr_value = float(psnr_match.group(1))
                passed = psnr_value >= self.quality_thresholds[QualityMetric.PSNR]

                return QualityScore(
                    metric=QualityMetric.PSNR,
                    score=psnr_value,
                    passed=passed,
                    details=f"PSNR: {psnr_value:.2f} dB",
                    psnr=psnr_value,
                )
            else:
                return QualityScore(
                    metric=QualityMetric.PSNR, score=0.0, passed=False, details="无法解析 PSNR 值"
                )

        except Exception as e:
            return QualityScore(
                metric=QualityMetric.PSNR,
                score=0.0,
                passed=False,
                details=f"PSNR 计算失败: {str(e)}",
            )

    def _calculate_ssim(self, input_file: str, output_file: str) -> QualityScore:
        """
        计算 SSIM（结构相似性）

        Args:
            input_file: 输入文件
            output_file: 输出文件

        Returns:
            质量评分
        """
        try:
            # 使用 FFmpeg 的 ssim 滤镜
            cmd = [
                self.ffmpeg_path,
                "-i",
                input_file,
                "-i",
                output_file,
                "-lavfi",
                "ssim",
                "-f",
                "null",
                "-",
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            # 解析输出
            import re

            ssim_match = re.search(r"All:([\d.]+)", result.stderr)

            if ssim_match:
                ssim_value = float(ssim_match.group(1))
                passed = ssim_value >= self.quality_thresholds[QualityMetric.SSIM]

                return QualityScore(
                    metric=QualityMetric.SSIM,
                    score=ssim_value,
                    passed=passed,
                    details=f"SSIM: {ssim_value:.4f}",
                    ssim=ssim_value,
                )
            else:
                return QualityScore(
                    metric=QualityMetric.SSIM, score=0.0, passed=False, details="无法解析 SSIM 值"
                )

        except Exception as e:
            return QualityScore(
                metric=QualityMetric.SSIM,
                score=0.0,
                passed=False,
                details=f"SSIM 计算失败: {str(e)}",
            )

    def _calculate_vmaf(self, input_file: str, output_file: str) -> QualityScore:
        """
        计算 VMAF（Netflix 视频质量评估）

        Args:
            input_file: 输入文件
            output_file: 输出文件

        Returns:
            质量评分
        """
        try:
            # 检查是否支持 libvmaf
            cmd = [
                self.ffmpeg_path,
                "-i",
                input_file,
                "-i",
                output_file,
                "-lavfi",
                "libvmaf",
                "-f",
                "null",
                "-",
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            if result.returncode != 0:
                return QualityScore(
                    metric=QualityMetric.VMAF,
                    score=0.0,
                    passed=False,
                    details="VMAF 不可用，请确保 FFmpeg 编译时启用了 libvmaf",
                )

            # 解析输出
            import re

            vmaf_match = re.search(r"VMAF score:([\d.]+)", result.stderr)

            if vmaf_match:
                vmaf_value = float(vmaf_match.group(1))
                passed = vmaf_value >= self.quality_thresholds[QualityMetric.VMAF]

                return QualityScore(
                    metric=QualityMetric.VMAF,
                    score=vmaf_value,
                    passed=passed,
                    details=f"VMAF: {vmaf_value:.2f}",
                    vmaf=vmaf_value,
                )
            else:
                return QualityScore(
                    metric=QualityMetric.VMAF, score=0.0, passed=False, details="无法解析 VMAF 值"
                )

        except Exception as e:
            return QualityScore(
                metric=QualityMetric.VMAF,
                score=0.0,
                passed=False,
                details=f"VMAF 计算失败: {str(e)}",
            )

    def _get_video_duration(self, file_path: str) -> float:
        """获取视频时长"""
        try:
            cmd = [
                self.ffprobe_path,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            if result.returncode == 0:
                return float(result.stdout.strip())
            else:
                return 0.0

        except Exception:
            return 0.0

    def _get_video_info(self, file_path: str) -> dict:
        """获取视频信息"""
        try:
            cmd = [
                self.ffprobe_path,
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,duration",
                "-show_entries",
                "format=size",
                "-of",
                "json",
                file_path,
            ]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )

            if result.returncode == 0:
                import json

                info = json.loads(result.stdout)

                # 提取视频流信息
                streams = info.get("streams", [])
                if streams:
                    stream = streams[0]
                    width = int(stream.get("width", 0))
                    height = int(stream.get("height", 0))
                    duration = float(stream.get("duration", 0))
                else:
                    width = height = duration = 0

                # 提取格式信息
                format_info = info.get("format", {})
                size_bytes = int(format_info.get("size", 0))
                size_mb = size_bytes / (1024 * 1024)

                return {"width": width, "height": height, "duration": duration, "size_mb": size_mb}
            else:
                return {}

        except Exception:
            return {}


# 使用示例
if __name__ == "__main__":
    print("=== 质量感知压缩器测试 ===\n")

    compressor = QualityAwareCompressor()

    # 示例 1：判断是否使用两遍编码
    print("示例 1：判断编码策略")
    should_use = compressor._should_use_two_pass(target_size_mb=100, duration_seconds=3600)
    print(f"目标: 100 MB, 时长: 1 小时")
    print(f"使用两遍编码: {should_use}")
    print()

    # 示例 2：基础质量检查（需要实际文件）
    print("示例 2：基础质量检查")
    print("（需要实际视频文件才能测试）")
