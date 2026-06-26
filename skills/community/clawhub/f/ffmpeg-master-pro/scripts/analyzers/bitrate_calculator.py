"""
智能码率计算器
多模型融合的码率计算算法
"""

from typing import Dict, Optional, Tuple
from enum import Enum


class ComplexityLevel(Enum):
    """内容复杂度等级"""

    SIMPLE = 0.8  # 简单（低运动、低细节）
    MEDIUM = 1.0  # 中等
    COMPLEX = 1.2  # 复杂（高运动、高细节）


class FormatFactor(Enum):
    """格式压缩因子"""

    H264 = 1.0
    H265 = 0.6  # HEVC 比 H.264 节省 40%
    AV1 = 0.5  # AV1 比 H.264 节省 50%
    VP9 = 0.7
    MPEG2 = 1.5  # MPEG2 需要更高码率


class BitrateCalculator:
    """智能码率计算器"""

    def __init__(self):
        """初始化码率计算器"""
        # 分辨率基准码率（单位：Kbps）
        self.resolution_base_bitrate = {
            (3840, 2160): 20000,  # 4K
            (2560, 1440): 12000,  # 2K
            (1920, 1080): 8000,  # 1080p
            (1280, 720): 5000,  # 720p
            (854, 480): 2500,  # 480p
            (640, 360): 1500,  # 360p
            (426, 240): 800,  # 240p
        }

        # 帧率调整因子
        self.fps_factors = {
            24: 1.0,
            25: 1.0,
            30: 1.1,
            50: 1.3,
            60: 1.4,
        }

        # 内容类型调整因子
        self.content_factors = {
            "movie": 1.0,
            "animation": 0.9,
            "screen_recording": 0.8,
            "sports": 1.2,
            "music_video": 1.1,
            "gameplay": 1.1,
            "talking_head": 0.85,
            "unknown": 1.0,
        }

    def calculate(
        self,
        width: int,
        height: int,
        fps: float,
        duration: float,
        target_size_mb: Optional[float] = None,
        content_type: str = "unknown",
        complexity: str = "medium",
        codec: str = "h264",
    ) -> Dict:
        """
        计算最优码率（多模型融合）

        Args:
            width: 视频宽度
            height: 视频高度
            fps: 帧率
            duration: 时长（秒）
            target_size_mb: 目标文件大小（MB），可选
            content_type: 内容类型
            complexity: 复杂度等级（simple/medium/complex）
            codec: 编解码器（h264/h265/av1/vp9）

        Returns:
            包含计算结果的字典
        """
        results = {}

        # 模型 1：基于分辨率的基础码率
        model1_bitrate = self._calculate_by_resolution(width, height, fps)
        results["model1_resolution"] = {
            "bitrate_kbps": model1_bitrate,
            "description": "基于分辨率和帧率的基础码率",
        }

        # 模型 2：基于内容复杂度的调整
        model2_bitrate = self._calculate_by_complexity(model1_bitrate, content_type, complexity)
        results["model2_complexity"] = {
            "bitrate_kbps": model2_bitrate,
            "description": "基于内容复杂度调整后的码率",
        }

        # 模型 3：基于目标大小的反推
        if target_size_mb:
            model3_bitrate = self._calculate_by_target_size(target_size_mb, duration)
            results["model3_target_size"] = {
                "bitrate_kbps": model3_bitrate,
                "description": "基于目标大小反推的码率",
            }

            # 三模型融合
            final_bitrate = self._fuse_models(model1_bitrate, model2_bitrate, model3_bitrate)
        else:
            # 双模型融合
            final_bitrate = self._fuse_models(model1_bitrate, model2_bitrate)

        # 应用格式压缩因子
        format_factor = self._get_format_factor(codec)
        final_bitrate = final_bitrate * format_factor

        results["final"] = {
            "video_bitrate_kbps": final_bitrate,
            "audio_bitrate_kbps": 128,  # 默认音频码率
            "total_bitrate_kbps": final_bitrate + 128,
            "estimated_size_mb": (final_bitrate + 128) * duration / (8 * 1024),
            "format_factor": format_factor,
            "codec": codec,
        }

        return results

    def _calculate_by_resolution(self, width: int, height: int, fps: float) -> float:
        """
        模型 1：基于分辨率的基础码率

        算法：
        1. 找到最接近的标准分辨率基准码率
        2. 根据实际分辨率进行线性插值
        3. 应用帧率调整因子
        """
        # 计算像素数
        pixels = width * height

        # 找到最接近的两个分辨率
        sorted_resolutions = sorted(self.resolution_base_bitrate.keys())
        lower_res = None
        upper_res = None

        for res in sorted_resolutions:
            res_pixels = res[0] * res[1]
            if res_pixels <= pixels:
                lower_res = res
            if res_pixels >= pixels and upper_res is None:
                upper_res = res
                break

        # 线性插值计算基准码率
        if lower_res and upper_res:
            lower_pixels = lower_res[0] * lower_res[1]
            upper_pixels = upper_res[0] * upper_res[1]
            lower_bitrate = self.resolution_base_bitrate[lower_res]
            upper_bitrate = self.resolution_base_bitrate[upper_res]

            if upper_pixels > lower_pixels:
                ratio = (pixels - lower_pixels) / (upper_pixels - lower_pixels)
                base_bitrate = lower_bitrate + (upper_bitrate - lower_bitrate) * ratio
            else:
                base_bitrate = lower_bitrate
        elif lower_res:
            base_bitrate = self.resolution_base_bitrate[lower_res]
        elif upper_res:
            base_bitrate = self.resolution_base_bitrate[upper_res]
        else:
            # 默认值
            base_bitrate = 5000

        # 应用帧率因子
        fps_factor = self._get_fps_factor(fps)
        return base_bitrate * fps_factor

    def _calculate_by_complexity(
        self, base_bitrate: float, content_type: str, complexity: str
    ) -> float:
        """
        模型 2：基于内容复杂度的调整

        算法：
        1. 应用内容类型调整因子
        2. 应用复杂度等级因子
        """
        # 内容类型因子
        content_factor = self.content_factors.get(content_type, 1.0)

        # 复杂度因子
        complexity_factor = ComplexityLevel[complexity.upper()].value

        return base_bitrate * content_factor * complexity_factor

    def _calculate_by_target_size(self, target_size_mb: float, duration: float) -> float:
        """
        模型 3：基于目标大小的反推

        算法：
        1. 目标大小（bits）= 目标大小（MB）× 8 × 1024
        2. 总码率 = 目标大小 / 时长
        3. 视频码率 = 总码率 - 音频码率（预留 128kbps）
        """
        target_bits = target_size_mb * 8 * 1024
        total_bitrate = target_bits / duration
        audio_bitrate = 128  # 预留音频码率
        video_bitrate = total_bitrate - audio_bitrate

        return max(video_bitrate, 500)  # 最小 500kbps

    def _fuse_models(self, *bitrates: float, weights: Optional[Tuple[float, ...]] = None) -> float:
        """
        融合多个模型的结果

        算法：加权平均

        权重分配：
        - 如果有目标大小，模型 3（目标大小）权重最高（40%）
        - 模型 2（复杂度）次之（35%）
        - 模型 1（分辨率）最低（25%）
        """
        if weights is None:
            if len(bitrates) == 3:
                weights = (0.25, 0.35, 0.40)  # 三模型
            elif len(bitrates) == 2:
                weights = (0.40, 0.60)  # 双模型
            else:
                weights = tuple(1.0 / len(bitrates) for _ in bitrates)

        fused = sum(b * w for b, w in zip(bitrates, weights))
        return fused

    def _get_fps_factor(self, fps: float) -> float:
        """获取帧率调整因子"""
        # 找到最接近的标准帧率
        for standard_fps, factor in sorted(self.fps_factors.items()):
            if abs(fps - standard_fps) < 5:
                return factor

        # 线性插值
        if fps <= 24:
            return 0.9
        elif fps >= 60:
            return 1.5
        else:
            return 1.0 + (fps - 24) / 36 * 0.4

    def _get_format_factor(self, codec: str) -> float:
        """获取格式压缩因子"""
        codec_upper = codec.upper().replace(".", "")
        try:
            return FormatFactor[codec_upper].value
        except KeyError:
            return 1.0

    def calculate_by_target_size(self, target_size_mb: float, duration: float) -> float:
        """
        快速计算：仅基于目标大小

        Args:
            target_size_mb: 目标文件大小（MB）
            duration: 时长（秒）

        Returns:
            推荐的视频码率（Kbps）
        """
        result = self._calculate_by_target_size(target_size_mb, duration)
        return result

    def estimate_size(
        self, bitrate_kbps: float, duration: float, audio_bitrate_kbps: float = 128
    ) -> float:
        """
        估算文件大小

        Args:
            bitrate_kbps: 视频码率（Kbps）
            duration: 时长（秒）
            audio_bitrate_kbps: 音频码率（Kbps）

        Returns:
            估算的文件大小（MB）
        """
        total_bitrate = bitrate_kbps + audio_bitrate_kbps
        total_bits = total_bitrate * duration
        size_mb = total_bits / (8 * 1024)
        return size_mb


# 使用示例
if __name__ == "__main__":
    calculator = BitrateCalculator()

    print("=== 智能码率计算器测试 ===\n")

    # 示例 1：压缩到 500MB
    print("示例 1：1080p 视频压缩到 500MB")
    result1 = calculator.calculate(
        width=1920,
        height=1080,
        fps=24.0,
        duration=3600,  # 1 小时
        target_size_mb=500,
        content_type="movie",
        complexity="medium",
        codec="h264",
    )
    print(f"推荐视频码率: {result1['final']['video_bitrate_kbps']:.2f} Kbps")
    print(f"估算文件大小: {result1['final']['estimated_size_mb']:.2f} MB\n")

    # 示例 2：4K 视频转码
    print("示例 2：4K 视频转码（无目标大小限制）")
    result2 = calculator.calculate(
        width=3840,
        height=2160,
        fps=30.0,
        duration=3600,
        content_type="sports",
        complexity="complex",
        codec="h265",
    )
    print(f"推荐视频码率: {result2['final']['video_bitrate_kbps']:.2f} Kbps")
    print(f"使用 H.265 编码，估算文件大小: {result2['final']['estimated_size_mb']:.2f} MB\n")

    # 示例 3：快速计算目标大小
    print("示例 3：快速计算目标 200MB 的码率")
    bitrate = calculator.calculate_by_target_size(200, 1800)  # 30 分钟
    print(f"推荐视频码率: {bitrate:.2f} Kbps\n")

    # 示例 4：估算文件大小
    print("示例 4：估算 5000kbps 码率的文件大小")
    size = calculator.estimate_size(5000, 3600)
    print(f"估算文件大小: {size:.2f} MB")
