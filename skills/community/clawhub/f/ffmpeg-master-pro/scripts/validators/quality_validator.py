"""
质量验证器
验证转码后的视频质量
"""

import subprocess
import json
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class QualityMetrics:
    """质量指标数据类"""

    file_size_mb: float
    duration: float
    width: int
    height: int
    fps: float
    video_bitrate: float
    audio_bitrate: float
    video_codec: str
    audio_codec: str
    pixel_format: str
    vmaf_score: Optional[float] = None  # Netflix VMAF 评分
    ssim_score: Optional[float] = None  # 结构相似性
    psnr_score: Optional[float] = None  # 峰值信噪比


class QualityValidator:
    """质量验证器"""

    def __init__(self):
        """初始化质量验证器"""

    def get_video_info(self, video_path: str) -> Dict:
        """
        获取视频信息

        Args:
            video_path: 视频文件路径

        Returns:
            视频信息字典
        """
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            video_path,
        ]

        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            return info
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            raise Exception(f"获取视频信息失败: {e}")

    def extract_metrics(self, video_path: str) -> QualityMetrics:
        """
        提取视频质量指标

        Args:
            video_path: 视频文件路径

        Returns:
            质量指标对象
        """
        info = self.get_video_info(video_path)
        format_info = info.get("format", {})

        # 获取视频流
        video_stream = None
        audio_stream = None

        for stream in info.get("streams", []):
            if stream["codec_type"] == "video" and video_stream is None:
                video_stream = stream
            elif stream["codec_type"] == "audio" and audio_stream is None:
                audio_stream = stream

        # 提取指标
        file_size_mb = float(format_info.get("size", 0)) / (1024 * 1024)
        duration = float(format_info.get("duration", 0))

        if video_stream:
            width = int(video_stream.get("width", 0))
            height = int(video_stream.get("height", 0))
            fps = self._parse_fps(video_stream.get("r_frame_rate", "0/1"))
            video_bitrate = (
                int(video_stream.get("bit_rate", 0)) if video_stream.get("bit_rate") else 0
            )
            video_codec = video_stream.get("codec_name", "")
            pixel_format = video_stream.get("pix_fmt", "")
        else:
            width = height = fps = video_bitrate = 0
            video_codec = ""
            pixel_format = ""

        if audio_stream:
            audio_bitrate = (
                int(audio_stream.get("bit_rate", 0)) if audio_stream.get("bit_rate") else 0
            )
            audio_codec = audio_stream.get("codec_name", "")
        else:
            audio_bitrate = 0
            audio_codec = ""

        return QualityMetrics(
            file_size_mb=file_size_mb,
            duration=duration,
            width=width,
            height=height,
            fps=fps,
            video_bitrate=video_bitrate / 1000,  # 转换为 Kbps
            audio_bitrate=audio_bitrate / 1000,
            video_codec=video_codec,
            audio_codec=audio_codec,
            pixel_format=pixel_format,
        )

    def _parse_fps(self, fps_str: str) -> float:
        """解析帧率"""
        try:
            num, den = fps_str.split("/")
            return float(num) / float(den)
        except (ValueError, ZeroDivisionError):
            return 0.0

    def compare_videos(self, original_path: str, processed_path: str) -> Dict:
        """
        比较原始视频和处理后视频的质量

        Args:
            original_path: 原始视频路径
            processed_path: 处理后视频路径

        Returns:
            比较结果字典
        """
        original_metrics = self.extract_metrics(original_path)
        processed_metrics = self.extract_metrics(processed_path)

        comparison = {
            "file_size": {
                "original_mb": original_metrics.file_size_mb,
                "processed_mb": processed_metrics.file_size_mb,
                "compression_ratio": (
                    original_metrics.file_size_mb / processed_metrics.file_size_mb
                    if processed_metrics.file_size_mb > 0
                    else 0
                ),
                "space_saved_percent": (
                    (1 - processed_metrics.file_size_mb / original_metrics.file_size_mb) * 100
                    if original_metrics.file_size_mb > 0
                    else 0
                ),
            },
            "resolution": {
                "original": f"{original_metrics.width}x{original_metrics.height}",
                "processed": f"{processed_metrics.width}x{processed_metrics.height}",
                "changed": original_metrics.width != processed_metrics.width
                or original_metrics.height != processed_metrics.height,
            },
            "duration": {
                "original": original_metrics.duration,
                "processed": processed_metrics.duration,
                "difference": abs(original_metrics.duration - processed_metrics.duration),
            },
            "bitrate": {
                "original_kbps": original_metrics.video_bitrate,
                "processed_kbps": processed_metrics.video_bitrate,
                "reduction_percent": (
                    (1 - processed_metrics.video_bitrate / original_metrics.video_bitrate) * 100
                    if original_metrics.video_bitrate > 0
                    else 0
                ),
            },
            "codec": {
                "original": original_metrics.video_codec,
                "processed": processed_metrics.video_codec,
            },
        }

        return comparison

    def calculate_vmaf(
        self, reference_path: str, distorted_path: str, model_path: Optional[str] = None
    ) -> float:
        """
        计算 VMAF 评分（Netflix 视频质量评估）

        Args:
            reference_path: 参考视频路径
            distorted_path: 失真视频路径
            model_path: VMAF 模型路径（可选）

        Returns:
            VMAF 评分（0-100）
        """
        # 构建 libvmaf 滤镜命令
        filter_complex = f"[0:v][1:v]libvmaf"

        if model_path:
            filter_complex += f":model_path={model_path}"

        cmd = [
            "ffmpeg",
            "-i",
            reference_path,
            "-i",
            distorted_path,
            "-filter_complex",
            filter_complex,
            "-f",
            "null",
            "-",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # 从输出中提取 VMAF 评分
            for line in result.stderr.split("\n"):
                if "VMAF" in line or "score" in line:
                    # 尝试解析评分
                    import re

                    match = re.search(r"(\d+\.?\d*)", line)
                    if match:
                        return float(match.group(1))

            return 0.0

        except subprocess.CalledProcessError as e:
            print(f"VMAF 计算失败（可能未安装 libvmaf）: {e.stderr}")
            return 0.0

    def calculate_psnr(self, reference_path: str, distorted_path: str) -> float:
        """
        计算 PSNR（峰值信噪比）

        Args:
            reference_path: 参考视频路径
            distorted_path: 失真视频路径

        Returns:
            PSNR 值（越高越好）
        """
        filter_complex = "[0:v][1:v]psnr"

        cmd = [
            "ffmpeg",
            "-i",
            reference_path,
            "-i",
            distorted_path,
            "-filter_complex",
            filter_complex,
            "-f",
            "null",
            "-",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # 从输出中提取 PSNR 值
            for line in result.stderr.split("\n"):
                if "PSNR" in line:
                    import re

                    match = re.search(r"PSNR\s*:\s*(\d+\.?\d*)", line)
                    if match:
                        return float(match.group(1))

            return 0.0

        except subprocess.CalledProcessError as e:
            print(f"PSNR 计算失败: {e.stderr}")
            return 0.0

    def calculate_ssim(self, reference_path: str, distorted_path: str) -> float:
        """
        计算 SSIM（结构相似性指数）

        Args:
            reference_path: 参考视频路径
            distorted_path: 失真视频路径

        Returns:
            SSIM 值（0-1，越高越好）
        """
        filter_complex = "[0:v][1:v]ssim"

        cmd = [
            "ffmpeg",
            "-i",
            reference_path,
            "-i",
            distorted_path,
            "-filter_complex",
            filter_complex,
            "-f",
            "null",
            "-",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # 从输出中提取 SSIM 值
            for line in result.stderr.split("\n"):
                if "SSIM" in line:
                    import re

                    match = re.search(r"All\s*:\s*(\d+\.?\d*)", line)
                    if match:
                        return float(match.group(1))

            return 0.0

        except subprocess.CalledProcessError as e:
            print(f"SSIM 计算失败: {e.stderr}")
            return 0.0

    def validate(
        self, original_path: str, processed_path: str, requirements: Optional[Dict] = None
    ) -> Dict:
        """
        验证处理后的视频是否符合要求

        Args:
            original_path: 原始视频路径
            processed_path: 处理后视频路径
            requirements: 验证要求字典

        Returns:
            验证结果字典
        """
        comparison = self.compare_videos(original_path, processed_path)
        processed_metrics = self.extract_metrics(processed_path)

        validation_results = {
            "passed": True,
            "checks": [],
            "comparison": comparison,
        }

        # 默认要求
        if requirements is None:
            requirements = {}

        # 检查文件大小
        if "max_size_mb" in requirements:
            max_size = requirements["max_size_mb"]
            passed = processed_metrics.file_size_mb <= max_size
            validation_results["checks"].append(
                {
                    "name": "文件大小",
                    "required": f"≤ {max_size} MB",
                    "actual": f"{processed_metrics.file_size_mb:.2f} MB",
                    "passed": passed,
                }
            )
            if not passed:
                validation_results["passed"] = False

        # 检查分辨率
        if "min_resolution" in requirements:
            min_width, min_height = requirements["min_resolution"]
            passed = processed_metrics.width >= min_width and processed_metrics.height >= min_height
            validation_results["checks"].append(
                {
                    "name": "分辨率",
                    "required": f"≥ {min_width}x{min_height}",
                    "actual": f"{processed_metrics.width}x{processed_metrics.height}",
                    "passed": passed,
                }
            )
            if not passed:
                validation_results["passed"] = False

        # 检查时长
        if "max_duration_diff" in requirements:
            max_diff = requirements["max_duration_diff"]
            actual_diff = comparison["duration"]["difference"]
            passed = actual_diff <= max_diff
            validation_results["checks"].append(
                {
                    "name": "时长",
                    "required": f"差异 ≤ {max_diff} 秒",
                    "actual": f"差异 {actual_diff:.2f} 秒",
                    "passed": passed,
                }
            )
            if not passed:
                validation_results["passed"] = False

        # 检查码率
        if "max_bitrate_kbps" in requirements:
            max_bitrate = requirements["max_bitrate_kbps"]
            passed = processed_metrics.video_bitrate <= max_bitrate
            validation_results["checks"].append(
                {
                    "name": "视频码率",
                    "required": f"≤ {max_bitrate} Kbps",
                    "actual": f"{processed_metrics.video_bitrate:.2f} Kbps",
                    "passed": passed,
                }
            )
            if not passed:
                validation_results["passed"] = False

        return validation_results


# 使用示例
if __name__ == "__main__":
    validator = QualityValidator()

    print("=== 质量验证器测试 ===\n")

    # 示例：提取视频指标
    print("提取视频指标:")
    print("metrics = validator.extract_metrics('test.mp4')")
    print('print(f"分辨率: {metrics.width}x{metrics.height}")')
    print('print(f"码率: {metrics.video_bitrate} Kbps")')
    print()

    # 示例：比较视频
    print("比较原始视频和处理后视频:")
    print("comparison = validator.compare_videos('original.mp4', 'processed.mp4')")
    print("print(f\"压缩率: {comparison['file_size']['compression_ratio']:.2f}x\")")
    print("print(f\"节省空间: {comparison['file_size']['space_saved_percent']:.1f}%\")")
    print()

    # 示例：验证质量
    print("验证视频质量:")
    print("requirements = {'max_size_mb': 500, 'max_duration_diff': 1}")
    print("results = validator.validate('original.mp4', 'processed.mp4', requirements)")
    print("print(f\"验证通过: {results['passed']}\")")
