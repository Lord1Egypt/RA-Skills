"""
GPU检测器
只负责检测GPU可用性和类型
"""

import subprocess
import sys
from typing import Dict, List


class GPUDetector:
    """GPU检测器"""

    def __init__(self):
        """初始化GPU检测器"""
        self._gpu_cache = None

    def detect(self) -> Dict[str, any]:
        """
        检测系统GPU信息

        Returns:
            GPU信息字典，包含:
            - available: 是否可用GPU
            - type: GPU类型 ("nvidia", "amd", "intel", "none")
            - encoder: 推荐的编码器
            - details: 详细信息
        """
        if self._gpu_cache:
            return self._gpu_cache

        # 按优先级检测不同类型的GPU
        gpu_info = self._detect_nvidia()
        if gpu_info["available"]:
            self._gpu_cache = gpu_info
            return gpu_info

        gpu_info = self._detect_amd()
        if gpu_info["available"]:
            self._gpu_cache = gpu_info
            return gpu_info

        gpu_info = self._detect_intel()
        if gpu_info["available"]:
            self._gpu_cache = gpu_info
            return gpu_info

        # 没有检测到GPU
        self._gpu_cache = {
            "available": False,
            "type": "none",
            "encoder": None,
            "details": "No GPU detected",
        }
        return self._gpu_cache

    def _detect_nvidia(self) -> Dict[str, any]:
        """检测NVIDIA GPU"""
        try:
            # 检查nvidia-smi是否可用
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                gpu_names = [line.strip() for line in result.stdout.strip().split("\n")]
                return {
                    "available": True,
                    "type": "nvidia",
                    "encoder": "h264_nvenc",
                    "details": {
                        "count": len(gpu_names),
                        "gpus": gpu_names,
                    },
                }
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return {"available": False, "type": "nvidia", "encoder": None, "details": "Not detected"}

    def _detect_amd(self) -> Dict[str, any]:
        """检测AMD GPU"""
        try:
            # 尝试使用rocm-smi检测AMD GPU
            result = subprocess.run(
                ["rocm-smi", "--showproductname"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0 and "GPU" in result.stdout:
                return {
                    "available": True,
                    "type": "amd",
                    "encoder": "h264_amf",
                    "details": {"info": result.stdout},
                }
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return {"available": False, "type": "amd", "encoder": None, "details": "Not detected"}

    def _detect_intel(self) -> Dict[str, any]:
        """检测Intel GPU"""
        try:
            # 在Linux上检查Intel GPU设备
            if sys.platform.startswith("linux"):
                result = subprocess.run(
                    ["lspci"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if "Intel" in result.stdout and "VGA" in result.stdout:
                    return {
                        "available": True,
                        "type": "intel",
                        "encoder": "h264_qsv",
                        "details": {"info": "Intel GPU detected via lspci"},
                    }
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return {
            "available": False,
            "type": "intel",
            "encoder": None,
            "details": "Not detected",
        }

    def get_available_encoders(self) -> List[str]:
        """
        获取系统中可用的硬件加速编码器列表

        Returns:
            可用编码器名称列表
        """
        gpu_info = self.detect()
        encoders = []

        if gpu_info["available"]:
            encoders.append(gpu_info["encoder"])

        # 可以添加更多编码器检测逻辑
        return encoders

    def clear_cache(self):
        """清除GPU检测缓存"""
        self._gpu_cache = None
