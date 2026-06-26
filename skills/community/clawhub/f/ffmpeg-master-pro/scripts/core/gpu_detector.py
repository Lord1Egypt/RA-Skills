"""
GPU 检测器
检测可用的硬件加速（NVENC/AMF/QSV）
"""

import shutil
import subprocess
import platform
from typing import Dict, Optional, List
from enum import Enum


class GPUType(Enum):
    """GPU 类型枚举"""

    NVIDIA = "nvidia"
    AMD = "amd"
    INTEL = "intel"
    NONE = "none"


class GPUDetector:
    """GPU 检测器"""

    def __init__(self):
        """初始化 GPU 检测器"""
        self.system = platform.system()

    def detect(self) -> Dict:
        """
        检测可用的 GPU 加速

        Returns:
            包含 GPU 信息的字典
        """
        result = {"available": False, "gpu_type": GPUType.NONE, "encoder": None, "details": {}}

        # 检测 NVIDIA GPU
        nvidia_info = self._detect_nvidia()
        if nvidia_info["available"]:
            result.update(
                {
                    "available": True,
                    "gpu_type": GPUType.NVIDIA,
                    "encoder": "h264_nvenc",
                    "details": nvidia_info,
                }
            )
            return result

        # 检测 AMD GPU
        amd_info = self._detect_amd()
        if amd_info["available"]:
            result.update(
                {
                    "available": True,
                    "gpu_type": GPUType.AMD,
                    "encoder": "h264_amf",
                    "details": amd_info,
                }
            )
            return result

        # 检测 Intel QSV
        intel_info = self._detect_intel()
        if intel_info["available"]:
            result.update(
                {
                    "available": True,
                    "gpu_type": GPUType.INTEL,
                    "encoder": "h264_qsv",
                    "details": intel_info,
                }
            )
            return result

        return result

    def _detect_nvidia(self) -> Dict:
        """检测 NVIDIA GPU（NVENC）"""
        result = {"available": False, "gpu_name": "", "driver_version": "", "cuda_version": ""}

        # Check if nvidia-smi is available before attempting to run it
        if not shutil.which("nvidia-smi"):
            return result

        try:
            # 检查 nvidia-smi
            cmd = [
                "nvidia-smi",
                "--query-gpu=name,driver_version,cuda_version",
                "--format=csv,noheader",
            ]
            output = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)

            if output.returncode == 0:
                lines = output.stdout.strip().split("\n")
                if lines and lines[0]:
                    parts = [p.strip() for p in lines[0].split(",")]
                    result["gpu_name"] = parts[0] if len(parts) > 0 else ""
                    result["driver_version"] = parts[1] if len(parts) > 1 else ""
                    result["cuda_version"] = parts[2] if len(parts) > 2 else ""
                    result["available"] = True

        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 验证 FFmpeg 是否支持 NVENC
        if result["available"]:
            if self._check_ffmpeg_encoder("h264_nvenc"):
                return result
            else:
                result["available"] = False
                result["note"] = "NVIDIA GPU 检测到，但 FFmpeg 不支持 NVENC"

        return result

    def _detect_amd(self) -> Dict:
        """检测 AMD GPU（AMF）"""
        result = {"available": False, "gpu_name": "", "driver_version": ""}

        try:
            # Windows: 检查 AMD GPU
            if self.system == "Windows":
                cmd = ["wmic", "path", "win32_VideoController", "get", "name"]
                output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

                if "AMD" in output.stdout or "Radeon" in output.stdout:
                    lines = output.stdout.strip().split("\n")
                    for line in lines:
                        if "AMD" in line or "Radeon" in line:
                            result["gpu_name"] = line.strip()
                            result["available"] = True
                            break

            # Linux: 检查 AMD GPU
            elif self.system == "Linux":
                try:
                    cmd = ["lsmod"]
                    output = subprocess.run(cmd, capture_output=True, text=True, check=True)

                    if "amdgpu" in output.stdout:
                        result["available"] = True

                        # 尝试获取 GPU 名称
                        try:
                            cmd = ["cat", "/sys/class/drm/card0/device/microcode_version"]
                            gpu_output = subprocess.run(cmd, capture_output=True, text=True)
                            if gpu_output.returncode == 0:
                                result["gpu_name"] = "AMD GPU"
                        except:
                            pass

                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

        except (subprocess.TimeoutExpired, Exception):
            pass

        # 验证 FFmpeg 是否支持 AMF
        if result["available"]:
            if self._check_ffmpeg_encoder("h264_amf"):
                return result
            else:
                result["available"] = False
                result["note"] = "AMD GPU 检测到，但 FFmpeg 不支持 AMF"

        return result

    def _detect_intel(self) -> Dict:
        """检测 Intel QSV"""
        result = {"available": False, "gpu_name": "", "api_version": ""}

        try:
            # 检查是否支持 Intel QSV
            if self.system == "Linux":
                # 检查 i915 驱动
                try:
                    cmd = ["lsmod"]
                    output = subprocess.run(cmd, capture_output=True, text=True, check=True)

                    if "i915" in output.stdout:
                        result["available"] = True
                        result["gpu_name"] = "Intel Integrated Graphics"

                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            elif self.system == "Windows":
                # 检查 Intel GPU
                try:
                    cmd = ["wmic", "path", "win32_VideoController", "get", "name"]
                    output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

                    if "Intel" in output.stdout:
                        lines = output.stdout.strip().split("\n")
                        for line in lines:
                            if "Intel" in line:
                                result["gpu_name"] = line.strip()
                                result["available"] = True
                                break

                except (subprocess.TimeoutExpired, Exception):
                    pass

            elif self.system == "Darwin":  # macOS
                # VideoToolbox (硬件加速)
                result["available"] = True
                result["gpu_name"] = "VideoToolbox (macOS)"

        except Exception:
            pass

        # 验证 FFmpeg 是否支持 QSV
        if result["available"]:
            if self._check_ffmpeg_encoder("h264_qsv"):
                return result
            elif self._check_ffmpeg_encoder("h264_videotoolbox"):
                result["encoder"] = "h264_videotoolbox"
                return result
            else:
                result["available"] = False
                result["note"] = "Intel GPU 检测到，但 FFmpeg 不支持 QSV"

        return result

    def _check_ffmpeg_encoder(self, encoder_name: str) -> bool:
        """
        检查 FFmpeg 是否支持指定的编码器

        Args:
            encoder_name: 编码器名称

        Returns:
            是否支持
        """
        try:
            cmd = ["ffmpeg", "-encoders"]
            output = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)

            return encoder_name in output.stdout

        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_supported_encoders(self) -> List[str]:
        """
        获取 FFmpeg 支持的所有硬件加速编码器

        Returns:
            支持的编码器列表
        """
        hardware_encoders = [
            "h264_nvenc",
            "hevc_nvenc",
            "av1_nvenc",
            "h264_amf",
            "hevc_amf",
            "h264_qsv",
            "hevc_qsv",
            "vp9_qsv",
            "h264_videotoolbox",
            "hevc_videotoolbox",
            "h264_vdpau",
            "hevc_vdpau",
            "h264_vaapi",
            "hevc_vaapi",
        ]

        supported = []

        for encoder in hardware_encoders:
            if self._check_ffmpeg_encoder(encoder):
                supported.append(encoder)

        return supported

    def recommend_encoder(
        self, codec: str = "h264", quality_priority: bool = False
    ) -> Optional[str]:
        """
        推荐最优的编码器

        Args:
            codec: 编解码器类型（h264/h265/av1）
            quality_priority: 质量优先还是速度优先

        Returns:
            推荐的编码器名称
        """
        gpu_info = self.detect()

        if not gpu_info["available"]:
            # 无 GPU，使用 CPU 编码器
            if quality_priority:
                return "libx264" if codec == "h264" else "libx265"
            else:
                return "libx264" if codec == "h264" else "libx265"

        # 有 GPU，根据 GPU 类型推荐
        gpu_type = gpu_info["gpu_type"]

        if gpu_type == GPUType.NVIDIA:
            # NVIDIA NVENC
            if codec == "h265":
                return "hevc_nvenc"
            elif codec == "av1":
                return "av1_nvenc"
            else:
                return "h264_nvenc"

        elif gpu_type == GPUType.AMD:
            # AMD AMF
            if codec == "h265":
                return "hevc_amf"
            else:
                return "h264_amf"

        elif gpu_type == GPUType.INTEL:
            # Intel QSV
            if codec == "h265":
                return "hevc_qsv"
            else:
                return "h264_qsv"

        return None


# 使用示例
if __name__ == "__main__":
    detector = GPUDetector()

    print("=== GPU 检测器测试 ===\n")

    # 检测 GPU
    print("检测 GPU 加速:")
    gpu_info = detector.detect()

    if gpu_info["available"]:
        print(f"GPU 类型: {gpu_info['gpu_type'].value}")
        print(f"推荐编码器: {gpu_info['encoder']}")
        print(f"详细信息: {gpu_info['details']}")
    else:
        print("未检测到可用的 GPU 加速")
        print("将使用 CPU 编码（libx264/libx265）")

    print()

    # 获取支持的编码器
    print("支持的硬件编码器:")
    encoders = detector.get_supported_encoders()
    for encoder in encoders:
        print(f"  - {encoder}")

    print()

    # 推荐编码器
    print("推荐编码器:")
    print(f"H.264: {detector.recommend_encoder('h264')}")
    print(f"H.265: {detector.recommend_encoder('h265')}")
    print(f"AV1: {detector.recommend_encoder('av1')}")
