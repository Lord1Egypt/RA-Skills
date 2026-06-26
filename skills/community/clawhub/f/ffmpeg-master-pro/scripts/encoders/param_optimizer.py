"""
参数优化器
根据视频内容类型自动选择最优编码参数
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass

# 条件导入，支持独立运行和模块导入
try:
    from ..analyzers import VideoContentType
except (ImportError, ValueError):
    from analyzers import VideoContentType


@dataclass
class EncodingParams:
    """编码参数数据类"""

    codec: str  # 编解码器 (libx264, libx265, etc.)
    preset: str  # 编码预设 (ultrafast, veryfast, fast, medium, slow, slower, veryslow)
    crf: Optional[int] = None  # 恒定质量因子 (0-51, 越小质量越好)，在目标大小模式下可为 None
    tune: Optional[str] = (
        None  # 内容调优 (film, animation, grain, stillimage, fastdecode, zerolatency)
    )
    profile: Optional[str] = None  # 编码配置 (baseline, main, high)
    level: Optional[str] = None  # 编码级别 (如 4.1)
    bitrate: Optional[str] = None  # 目标码率 (如 "5000k")
    maxrate: Optional[str] = None  # 最大码率
    bufsize: Optional[str] = None  # 缓冲区大小
    pix_fmt: Optional[str] = None  # 像素格式
    audio_codec: str = "aac"  # 音频编解码器
    audio_bitrate: str = "128k"  # 音频码率

    # x264/x265 特定参数
    deblock: Optional[str] = None  # 去块滤波参数
    me_method: Optional[str] = None  # 运动估计算法
    subq: Optional[int] = None  # 子像素运动估计质量
    me_range: Optional[int] = None  # 运动估计范围

    # 滤镜参数
    denoise_filter: Optional[str] = None  # 降噪滤镜
    deinterlace_filter: Optional[str] = None  # 去隔行滤镜

    # 其他参数
    extra_params: Optional[Dict[str, Any]] = None  # 额外参数

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "codec": self.codec,
            "preset": self.preset,
            "crf": self.crf,
            "audio_codec": self.audio_codec,
            "audio_bitrate": self.audio_bitrate,
        }

        # 添加可选参数
        if self.tune:
            result["tune"] = self.tune
        if self.profile:
            result["profile"] = self.profile
        if self.level:
            result["level"] = self.level
        if self.bitrate:
            result["bitrate"] = self.bitrate
        if self.maxrate:
            result["maxrate"] = self.maxrate
        if self.bufsize:
            result["bufsize"] = self.bufsize
        if self.pix_fmt:
            result["pix_fmt"] = self.pix_fmt
        if self.deblock:
            result["deblock"] = self.deblock
        if self.me_method:
            result["me_method"] = self.me_method
        if self.subq:
            result["subq"] = self.subq
        if self.me_range:
            result["me_range"] = self.me_range
        if self.denoise_filter:
            result["denoise_filter"] = self.denoise_filter
        if self.deinterlace_filter:
            result["deinterlace_filter"] = self.deinterlace_filter
        if self.extra_params:
            result.update(self.extra_params)

        return result


class ParamOptimizer:
    """
    参数优化器

    根据视频内容类型、GPU 可用性和用户需求，
    自动选择最优的编码参数组合
    """

    # 内容类型预设参数映射表
    CONTENT_TYPE_PRESETS: Dict[VideoContentType, Dict[str, Any]] = {
        VideoContentType.SCREEN_RECORDING: {
            "codec": "libx264",
            "preset": "veryfast",
            "crf": 18,
            "tune": "zerolatency",
            "profile": "high",
            "pix_fmt": "yuv420p",
            "notes": "屏幕录制需要快速编码和低延迟，使用 veryfast 预设平衡速度和质量",
        },
        VideoContentType.ANIME: {
            "codec": "libx264",
            "preset": "slow",
            "crf": 20,
            "tune": "animation",
            "profile": "high",
            "deblock": "1:0",  # 保留线条清晰度
            "subq": 9,  # 高质量子像素运动估计
            "me_range": 24,  # 更大范围的精确运动估计
            "pix_fmt": "yuv420p",
            "notes": "动漫需要保护线条和色块，使用 animation tune 和 deblock 滤波",
        },
        VideoContentType.MOVIE: {
            "codec": "libx264",
            "preset": "slow",
            "crf": 23,
            "tune": "film",
            "profile": "high",
            "pix_fmt": "yuv420p",
            "notes": "电影平衡质量和文件大小，使用 film tune 优化电影内容",
        },
        VideoContentType.SPORTS: {
            "codec": "libx264",
            "preset": "fast",
            "crf": 22,
            "tune": "fastdecode",  # 快速解码优化
            "profile": "high",
            "pix_fmt": "yuv420p",
            "notes": "体育视频需要处理快速运动，使用 fast 解码优化播放性能",
        },
        VideoContentType.MUSIC_VIDEO: {
            "codec": "libx264",
            "preset": "medium",
            "crf": 21,
            "tune": "film",
            "profile": "high",
            "pix_fmt": "yuv420p",
            "notes": "音乐视频平衡复杂度和质量，适合快速剪辑和色彩丰富的内容",
        },
        VideoContentType.OLD_VIDEO: {
            "codec": "libx264",
            "preset": "veryslow",
            "crf": 19,
            "tune": "grain",  # 胶片颗粒优化
            "profile": "high",
            "denoise_filter": "hqdn3d=4:3:6:4.5",  # 高质量降噪
            "pix_fmt": "yuv420p",
            "notes": "老旧视频需要降噪和颗粒保护，使用 veryslow 预设最大化质量",
        },
    }

    # GPU 加速预设
    GPU_PRESETS: Dict[str, Dict[str, Any]] = {
        "nvidia": {
            "codec": "h264_nvenc",
            "preset": "p4",  # 平衡质量和速度
            "crf": 23,
            "pix_fmt": "yuv420p",
            "notes": "NVIDIA NVENC 硬件加速",
        },
        "amd": {
            "codec": "h264_amf",
            "preset": "balanced",
            "crf": 23,
            "pix_fmt": "yuv420p",
            "notes": "AMD AMF 硬件加速",
        },
        "intel": {
            "codec": "h264_qsv",
            "preset": "medium",
            "crf": 23,
            "pix_fmt": "yuv420p",
            "notes": "Intel Quick Sync Video 硬件加速",
        },
    }

    def __init__(self):
        """初始化参数优化器"""

    def optimize_for_content_type(
        self,
        content_type: VideoContentType,
        gpu_type: Optional[str] = None,
        quality_preference: str = "balanced",
    ) -> EncodingParams:
        """
        为内容类型优化参数

        Args:
            content_type: 视频内容类型
            gpu_type: GPU 类型 ("nvidia", "amd", "intel", None)
            quality_preference: 质量偏好 ("high", "balanced", "fast")

        Returns:
            EncodingParams: 优化后的编码参数
        """
        # 1. 获取基础预设
        if gpu_type and gpu_type.lower() in self.GPU_PRESETS:
            # 使用 GPU 加速
            base_params = self.GPU_PRESETS[gpu_type.lower()].copy()
        else:
            # 使用 CPU 编码
            if content_type not in self.CONTENT_TYPE_PRESETS:
                # 默认使用电影预设
                content_type = VideoContentType.MOVIE
            base_params = self.CONTENT_TYPE_PRESETS[content_type].copy()

        # 2. 根据质量偏好调整
        if quality_preference == "high":
            # 更高质量，更慢速度
            base_params = self._adjust_for_high_quality(base_params)
        elif quality_preference == "fast":
            # 更快速度，略低质量
            base_params = self._adjust_for_fast_encoding(base_params)

        # 3. 移除 notes 字段（不需要在最终参数中）
        base_params.pop("notes", None)

        # 4. 构建 EncodingParams 对象
        return EncodingParams(**base_params)

    def optimize_for_target_size(
        self,
        target_size_mb: float,
        duration_seconds: float,
        content_type: Optional[VideoContentType] = None,
        gpu_type: Optional[str] = None,
    ) -> EncodingParams:
        """
        为目标文件大小优化参数

        Args:
            target_size_mb: 目标文件大小（MB）
            duration_seconds: 视频时长（秒）
            content_type: 内容类型（可选）
            gpu_type: GPU 类型（可选）

        Returns:
            EncodingParams: 包含目标码率的参数
        """
        # 1. 计算目标视频码率
        # 公式：目标码率 = (目标大小 * 8192) / 时长 - 音频码率
        audio_bitrate_kbps = 128
        target_size_kb = target_size_mb * 1024
        total_bitrate_kbps = (target_size_kb * 8) / duration_seconds
        video_bitrate_kbps = int(total_bitrate_kbps - audio_bitrate_kbps)

        # 留出 5% 的安全余量
        video_bitrate_kbps = int(video_bitrate_kbps * 0.95)

        # 2. 如果没有指定内容类型，使用电影类型
        if content_type is None:
            content_type = VideoContentType.MOVIE

        # 3. 获取内容类型预设
        if gpu_type and gpu_type.lower() in self.GPU_PRESETS:
            base_params = self.GPU_PRESETS[gpu_type.lower()].copy()
        else:
            base_params = self.CONTENT_TYPE_PRESETS[content_type].copy()

        # 4. 设置码率参数（替代 CRF）
        base_params.pop("crf", None)  # 移除 CRF
        base_params["bitrate"] = f"{video_bitrate_kbps}k"
        base_params["maxrate"] = f"{int(video_bitrate_kbps * 1.2)}k"
        base_params["bufsize"] = f"{int(video_bitrate_kbps * 2)}k"

        # 5. 移除 notes 字段
        base_params.pop("notes", None)

        # 6. 构建 EncodingParams 对象
        return EncodingParams(**base_params)

    def _adjust_for_high_quality(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """调整为高质量模式"""
        preset_rank = {
            "ultrafast": 0,
            "veryfast": 1,
            "fast": 2,
            "medium": 3,
            "slow": 4,
            "slower": 5,
            "veryslow": 6,
        }

        # 降低预设速度（提高质量）
        current_preset = params.get("preset", "medium")
        current_rank = preset_rank.get(current_preset, 3)
        new_rank = min(6, current_rank + 2)  # 提升 2 级

        for preset, rank in preset_rank.items():
            if rank == new_rank:
                params["preset"] = preset
                break

        # 降低 CRF 值（提高质量）
        if "crf" in params:
            params["crf"] = max(0, params["crf"] - 3)

        return params

    def _adjust_for_fast_encoding(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """调整为快速编码模式"""
        preset_rank = {
            "ultrafast": 0,
            "veryfast": 1,
            "fast": 2,
            "medium": 3,
            "slow": 4,
            "slower": 5,
            "veryslow": 6,
        }

        # 提高预设速度
        current_preset = params.get("preset", "medium")
        current_rank = preset_rank.get(current_preset, 3)
        new_rank = max(0, current_rank - 2)  # 降低 2 级

        for preset, rank in preset_rank.items():
            if rank == new_rank:
                params["preset"] = preset
                break

        # 提高 CRF 值（降低质量，提高速度）
        if "crf" in params:
            params["crf"] = min(51, params["crf"] + 3)

        return params

    def get_preset_description(self, content_type: VideoContentType) -> str:
        """
        获取预设的描述信息

        Returns:
            预设描述字符串
        """
        if content_type in self.CONTENT_TYPE_PRESETS:
            preset = self.CONTENT_TYPE_PRESETS[content_type]
            return preset.get("notes", "无描述")
        return "未知内容类型"

    def list_available_presets(self) -> Dict[str, str]:
        """
        列出所有可用的预设

        Returns:
            预设名称到描述的映射
        """
        presets = {}
        for content_type in VideoContentType:
            name = content_type.value
            description = self.get_preset_description(content_type)
            presets[name] = description

        return presets

    def validate_params(self, params: EncodingParams) -> tuple[bool, list[str]]:
        """
        验证参数的有效性

        Returns:
            (is_valid, errors): (是否有效, 错误列表)
        """
        errors = []

        # 1. 验证 CRF 范围
        if params.crf < 0 or params.crf > 51:
            errors.append(f"CRF 值 {params.crf} 超出范围 [0, 51]")

        # 2. 验证预设
        valid_presets = ["ultrafast", "veryfast", "fast", "medium", "slow", "slower", "veryslow"]
        if params.preset not in valid_presets:
            errors.append(f"无效的预设: {params.preset}")

        # 3. 验证 Profile
        if params.profile:
            valid_profiles = ["baseline", "main", "high", "high10", "high422", "high444"]
            if params.profile not in valid_profiles:
                errors.append(f"无效的 Profile: {params.profile}")

        # 4. 验证 Tune
        if params.tune:
            valid_tunes = ["film", "animation", "grain", "stillimage", "fastdecode", "zerolatency"]
            if params.tune not in valid_tunes:
                errors.append(f"无效的 Tune: {params.tune}")

        # 5. 验证编解码器
        valid_codecs = [
            "libx264",
            "libx265",
            "libaom-av1",
            "libvpx-vp9",
            "h264_nvenc",
            "h264_amf",
            "h264_qsv",
        ]
        if params.codec not in valid_codecs:
            errors.append(f"未知的编解码器: {params.codec}（可能仍然有效）")

        is_valid = len(errors) == 0
        return is_valid, errors


__all__ = ["ParamOptimizer", "EncodingParams"]
