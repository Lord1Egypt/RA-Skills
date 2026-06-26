"""
编码参数优化器
只负责优化编码参数
"""

from typing import Dict, Optional, Any


class EncoderParams:
    """编码参数数据类"""

    def __init__(
        self,
        encoder: str,
        preset: str,
        crf: int,
        profile: str = "high",
        level: str = "4.1",
        **kwargs
    ):
        """
        初始化编码参数

        Args:
            encoder: 编码器名称
            preset: 编码预设
            crf: CRF值
            profile: 编码配置文件
            level: 编码级别
            **kwargs: 其他参数
        """
        self.encoder = encoder
        self.preset = preset
        self.crf = crf
        self.profile = profile
        self.level = level
        self.extra_params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "encoder": self.encoder,
            "preset": self.preset,
            "crf": self.crf,
            "profile": self.profile,
            "level": self.level,
        }
        result.update(self.extra_params)
        return result


class EncoderOptimizer:
    """编码参数优化器"""

    def __init__(self, preset_manager=None):
        """
        初始化编码参数优化器

        Args:
            preset_manager: 预设管理器（可选）
        """
        self.preset_manager = preset_manager
        # 默认内容类型预设（如果没有preset_manager，使用这些）
        self._default_presets = self._load_default_presets()

    def _load_default_presets(self) -> Dict[str, Dict]:
        """加载默认内容类型预设"""
        # 使用绝对导入路径
        from detectors.content_detector.content_detector import ContentType

        return {
            ContentType.MOVIE.value: {
                "encoder": "libx264",
                "preset": "slow",
                "crf": 23,
                "tune": "film",
                "profile": "high",
                "level": "4.1",
            },
            ContentType.ANIMATION.value: {
                "encoder": "libx264",
                "preset": "medium",
                "crf": 20,
                "tune": "animation",
                "profile": "high",
                "level": "4.1",
            },
            ContentType.SCREEN_RECORDING.value: {
                "encoder": "libx264",
                "preset": "veryfast",
                "crf": 18,
                "tune": "zerolatency",
                "profile": "high",
                "level": "4.1",
            },
            ContentType.SPORTS.value: {
                "encoder": "libx264",
                "preset": "fast",
                "crf": 22,
                "tune": "film",
                "profile": "high",
                "level": "4.2",
            },
            ContentType.MUSIC_VIDEO.value: {
                "encoder": "libx264",
                "preset": "medium",
                "crf": 21,
                "tune": "film",
                "profile": "high",
                "level": "4.1",
            },
            ContentType.GAMEPLAY.value: {
                "encoder": "libx264",
                "preset": "fast",
                "crf": 20,
                "tune": "zerolatency",
                "profile": "high",
                "level": "4.1",
            },
            ContentType.TALKING_HEAD.value: {
                "encoder": "libx264",
                "preset": "slow",
                "crf": 24,
                "tune": "film",
                "profile": "high",
                "level": "4.0",
            },
            ContentType.UNKNOWN.value: {
                "encoder": "libx264",
                "preset": "medium",
                "crf": 23,
                "tune": "film",
                "profile": "high",
                "level": "4.1",
            },
        }

    def optimize(
        self,
        content_type: str,
        gpu_info: Dict,
        user_params: Optional[Dict] = None,
        video_info: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        优化编码参数

        Args:
            content_type: 内容类型
            gpu_info: GPU信息字典
            user_params: 用户提供的参数（可选）
            video_info: 视频信息（可选，用于计算码率等）

        Returns:
            优化后的编码参数字典
        """
        # 获取内容类型预设
        presets = self._get_content_presets()
        params = presets.get(content_type, presets.get("unknown", {}))

        # 复制参数以避免修改原始预设
        params = params.copy()

        # 检测 GPU 加速
        if gpu_info.get("available", False):
            # 使用 GPU 编码器
            params["encoder"] = gpu_info["encoder"]
            params["gpu"] = True
        else:
            params["gpu"] = False

        # 处理用户参数
        if user_params:
            params = self._apply_user_params(params, user_params, video_info)

        return params

    def _get_content_presets(self) -> Dict[str, Dict]:
        """获取内容类型预设"""
        # 如果有preset_manager，从配置加载
        if self.preset_manager:
            try:
                # 尝试从preset_manager加载内容类型预设
                custom_presets = self.preset_manager.load_preset("content_types")
                if custom_presets:
                    return custom_presets.video.get("content_types", self._default_presets)
            except Exception:
                pass

        # 否则使用默认预设
        return self._default_presets

    def _apply_user_params(
        self, base_params: Dict, user_params: Dict, video_info: Optional[Dict]
    ) -> Dict:
        """
        应用用户参数到基础参数

        Args:
            base_params: 基础参数
            user_params: 用户参数
            video_info: 视频信息

        Returns:
            应用用户参数后的参数字典
        """
        params = base_params.copy()

        # 计算目标码率
        if "target_size_mb" in user_params and video_info:
            from analyzers.bitrate_calculator import BitrateCalculator

            calculator = BitrateCalculator()
            duration = video_info.get("duration", 0)
            target_bitrate = calculator.calculate_by_target_size(
                user_params["target_size_mb"], duration
            )
            params["bitrate"] = target_bitrate
            params["mode"] = "vbr"  # Variable Bitrate
        else:
            # 使用 CRF 模式
            params["crf"] = params.get("crf", 23)
            params["mode"] = "crf"

        # 处理分辨率调整
        if "resolution" in user_params:
            target_width, target_height = user_params["resolution"]
            params["width"] = target_width
            params["height"] = target_height

        # 处理帧率调整
        if "fps" in user_params:
            params["fps"] = user_params["fps"]

        # 音频参数
        if video_info and video_info.get("audio"):
            params["audio_codec"] = "aac"
            params["audio_bitrate"] = "128k"
        else:
            params["audio_codec"] = None

        return params
