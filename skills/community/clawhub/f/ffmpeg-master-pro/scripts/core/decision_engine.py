"""
智能决策引擎（重构版）
协调各个模块，提供统一的决策接口
"""

import json
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# 导入重构后的模块
try:
    # 模块导入
    from ..analyzers.video_analyzer.video_analyzer import VideoAnalyzer
    from ..detectors.content_detector.content_detector import ContentDetector, ContentType
    from ..optimizers.encoder_optimizer.encoder_optimizer import EncoderOptimizer
    from .gpu_detector_module import GPUDetector
    # 保留原有的其他依赖
    from ..analyzers.bitrate_calculator import BitrateCalculator
    from ..analyzers.video_type_analyzer import VideoTypeAnalyzer, VideoAnalysisResult
    from ..analyzers import VideoContentType
    from ..analyzers.keyframe_analyzer import KeyFrameAnalyzer, TrimStrategy
    from ..encoders.param_optimizer import ParamOptimizer
    from ..utils.preset_manager import PresetManager, PresetConfig
except (ImportError, ValueError):
    try:
        # 独立运行 - 从 scripts 目录
        from analyzers.video_analyzer.video_analyzer import VideoAnalyzer
        from detectors.content_detector.content_detector import ContentDetector, ContentType
        from optimizers.encoder_optimizer.encoder_optimizer import EncoderOptimizer
        from core.gpu_detector_module import GPUDetector
        from analyzers.bitrate_calculator import BitrateCalculator
        from analyzers.video_type_analyzer import VideoTypeAnalyzer, VideoAnalysisResult
        from analyzers import VideoContentType
        from analyzers.keyframe_analyzer import KeyFrameAnalyzer, TrimStrategy
        from encoders.param_optimizer import ParamOptimizer
        from utils.preset_manager import PresetManager, PresetConfig
    except ImportError:
        # 独立运行 - 从 core 目录
        from ..analyzers.video_analyzer.video_analyzer import VideoAnalyzer
        from ..detectors.content_detector.content_detector import ContentDetector, ContentType
        from ..optimizers.encoder_optimizer.encoder_optimizer import EncoderOptimizer
        from .gpu_detector_module import GPUDetector
        from ..analyzers.bitrate_calculator import BitrateCalculator
        from ..analyzers.video_type_analyzer import VideoTypeAnalyzer, VideoAnalysisResult
        from ..analyzers import VideoContentType
        from ..analyzers.keyframe_analyzer import KeyFrameAnalyzer, TrimStrategy
        from ..encoders.param_optimizer import ParamOptimizer
        from ..utils.preset_manager import PresetManager, PresetConfig


# 向后兼容：创建一个包装类来模拟旧的ContentType接口
class ContentTypeLegacy:
    """向后兼容的ContentType类，模拟旧的类属性接口"""

    MOVIE = "movie"
    ANIMATION = "animation"
    SCREEN_RECORDING = "screen_recording"
    SPORTS = "sports"
    MUSIC_VIDEO = "music_video"
    GAMEPLAY = "gameplay"
    TALKING_HEAD = "talking_head"
    UNKNOWN = "unknown"

    @classmethod
    def from_enum(cls, enum_value):
        """从Enum转换为字符串"""
        return enum_value.value


class DecisionEngine:
    """
    智能决策引擎（重构版）

    职责：
    - 协调VideoAnalyzer、ContentDetector、EncoderOptimizer等模块
    - 提供统一的决策接口
    - 保持向后兼容性
    """

    def __init__(self, enable_smart_analysis: bool = True):
        """
        初始化决策引擎

        Args:
            enable_smart_analysis: 是否启用智能视频类型分析（基于运动、复杂度、色彩）
        """
        # 新架构：模块化组件
        self.video_analyzer = VideoAnalyzer()
        self.content_detector = ContentDetector()
        self.gpu_detector = GPUDetector()
        self.encoder_optimizer = EncoderOptimizer()
        self.preset_manager = PresetManager()
        self.bitrate_calculator = BitrateCalculator()
        self.keyframe_analyzer = KeyFrameAnalyzer()

        # 智能分析组件（保留原有功能）
        self.enable_smart_analysis = enable_smart_analysis
        if enable_smart_analysis:
            self.video_type_analyzer = VideoTypeAnalyzer()
            self.param_optimizer = ParamOptimizer()
        else:
            self.video_type_analyzer = None
            self.param_optimizer = None

    def analyze_video(self, video_path: str) -> Dict:
        """
        分析视频文件

        Args:
            video_path: 视频文件路径

        Returns:
            包含视频信息的字典
        """
        # 使用新的VideoAnalyzer
        video_info = self.video_analyzer.analyze(video_path)
        analysis = video_info.to_dict()

        # 使用ContentDetector检测内容类型
        content_type = self.content_detector.detect(analysis)
        analysis["content_type"] = content_type.value

        # 估算复杂度
        complexity = self.content_detector.estimate_complexity(analysis)
        analysis["complexity"] = complexity

        # 智能视频类型分析（如果启用）
        if self.enable_smart_analysis and self.video_type_analyzer:
            try:
                smart_analysis = self.analyze_video_type_deep(video_path)
                analysis["smart_analysis"] = smart_analysis
                # 如果智能分析的置信度够高，则覆盖简单检测的结果
                if smart_analysis.confidence >= 0.7:
                    analysis["content_type"] = smart_analysis.content_type.value
                    analysis["content_confidence"] = smart_analysis.confidence
            except Exception as e:
                # 智能分析失败时，回退到简单检测
                analysis["smart_analysis_error"] = str(e)

        return analysis

    def decide_encoding_params(self, analysis: Dict, user_params: Dict) -> Dict:
        """
        决定最优编码参数

        Args:
            analysis: 视频分析结果
            user_params: 用户提供的参数

        Returns:
            最优的编码参数字典
        """
        # 获取GPU信息
        gpu_info = self.gpu_detector.detect()

        # 使用新的EncoderOptimizer
        params = self.encoder_optimizer.optimize(
            content_type=analysis.get("content_type", "unknown"),
            gpu_info=gpu_info,
            user_params=user_params,
            video_info=analysis,
        )

        return params

    def decide_subtitle_action(self, analysis: Dict, user_params: Dict) -> Dict:
        """
        决定字幕处理方案

        Args:
            analysis: 视频分析结果
            user_params: 用户提供的参数

        Returns:
            字幕处理方案
        """
        subtitles = analysis.get("subtitles", [])
        decision = {
            "has_subtitles": len(subtitles) > 0,
            "subtitle_streams": subtitles,
            "action": None,
            "params": {},
        }

        if not subtitles:
            decision["action"] = "none"
            decision["message"] = "视频中没有字幕流"
            return decision

        # 根据用户意图决定操作
        target_lang = user_params.get("subtitle_lang")

        if target_lang:
            # 过滤指定语言的字幕
            matching_subs = [s for s in subtitles if s["language"] == target_lang]
            if matching_subs:
                decision["selected_streams"] = matching_subs
            else:
                decision["message"] = f"未找到 {target_lang} 字幕"
                return decision
        else:
            decision["selected_streams"] = subtitles

        return decision

    # ==================== 智能分析相关方法 ====================

    def analyze_video_type_deep(self, video_path: str) -> VideoAnalysisResult:
        """
        深度分析视频类型（基于运动、复杂度、色彩）

        Args:
            video_path: 视频文件路径

        Returns:
            VideoAnalysisResult: 详细的分析结果
        """
        if not self.video_type_analyzer:
            raise RuntimeError("智能分析未启用，请在初始化时设置 enable_smart_analysis=True")

        return self.video_type_analyzer.analyze(video_path)

    def get_optimized_encoding_params(
        self,
        video_path: str,
        target_size_mb: Optional[float] = None,
        quality_preference: str = "balanced",
        manual_content_type: Optional[VideoContentType] = None,
    ) -> Dict:
        """
        获取优化的编码参数

        Args:
            video_path: 视频文件路径
            target_size_mb: 目标文件大小（MB），如果指定则使用码率模式
            quality_preference: 质量偏好 ("high", "balanced", "fast")
            manual_content_type: 手动指定的内容类型（覆盖自动检测）

        Returns:
            优化后的编码参数字典
        """
        if not self.param_optimizer:
            raise RuntimeError("参数优化器未启用，请在初始化时设置 enable_smart_analysis=True")

        # 1. 分析视频类型
        if manual_content_type:
            content_type = manual_content_type
        else:
            analysis_result = self.analyze_video_type_deep(video_path)
            content_type = analysis_result.content_type

        # 2. 检测 GPU
        gpu_info = self.gpu_detector.detect()
        gpu_type = gpu_info["type"] if gpu_info["available"] else None

        # 3. 根据是否有目标大小选择优化策略
        if target_size_mb:
            # 获取视频时长
            probe_cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                video_path,
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())

            # 使用目标大小优化
            encoding_params = self.param_optimizer.optimize_for_target_size(
                target_size_mb=target_size_mb,
                duration_seconds=duration,
                content_type=content_type,
                gpu_type=gpu_type,
            )
        else:
            # 使用内容类型优化
            encoding_params = self.param_optimizer.optimize_for_content_type(
                content_type=content_type, gpu_type=gpu_type, quality_preference=quality_preference
            )

        # 4. 转换为字典格式返回
        params_dict = encoding_params.to_dict()
        params_dict["content_type"] = content_type.value
        params_dict["gpu_available"] = gpu_info["available"]
        params_dict["gpu_type"] = gpu_type

        return params_dict

    def list_content_type_presets(self) -> Dict[str, str]:
        """
        列出所有内容类型预设及其描述

        Returns:
            预设名称到描述的映射
        """
        if not self.param_optimizer:
            return {}

        return self.param_optimizer.list_available_presets()

    # ==================== 预设管理相关方法 ====================

    def list_available_presets(
        self, include_builtin: bool = True, include_custom: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        列出所有可用的预设模板

        Args:
            include_builtin: 是否包含内置预设
            include_custom: 是否包含用户自定义预设

        Returns:
            预设字典，格式：{preset_name: {path, type, metadata}}
        """
        return self.preset_manager.list_presets(include_builtin, include_custom)

    def apply_preset(self, preset_name: str, user_params: Optional[Dict] = None) -> Optional[Dict]:
        """
        应用预设模板并生成编码参数

        Args:
            preset_name: 预设名称（如 'youtube', 'bilibili', 'wechat'）
            user_params: 用户参数（可选），用于覆盖预设中的某些参数

        Returns:
            编码参数字典，如果预设不存在返回 None
        """
        # 加载预设配置
        preset_config = self.preset_manager.load_preset(preset_name)
        if not preset_config:
            return None

        # 将预设转换为编码参数
        encoding_params = {
            "encoder": preset_config.video.get("codec", "libx264"),
            "preset": preset_config.video.get("preset", "medium"),
            "crf": preset_config.video.get("crf", 23),
            "profile": preset_config.video.get("profile", "high"),
            "level": preset_config.video.get("level", "4.0"),
            "pixel_format": preset_config.video.get("pixel_format", "yuv420p"),
            "audio_codec": preset_config.audio.get("codec", "aac"),
            "audio_bitrate": preset_config.audio.get("bitrate", "128k"),
            "audio_sample_rate": preset_config.audio.get("sample_rate", 44100),
            "audio_channels": preset_config.audio.get("channels", 2),
            "movflags": preset_config.video.get("movflags", ""),
        }

        # 处理特殊选项（如 faststart）
        if encoding_params["movflags"]:
            encoding_params["extra_flags"] = ["-movflags", encoding_params["movflags"]]
            del encoding_params["movflags"]

        # 如果用户提供了参数，覆盖预设中的对应参数
        if user_params:
            for key, value in user_params.items():
                encoding_params[key] = value

        # 添加预设元数据
        encoding_params["_preset_info"] = {
            "name": preset_config.name,
            "description": preset_config.description,
            "version": preset_config.version,
        }

        return encoding_params

    def get_preset_info(self, preset_name: str) -> Optional[Dict[str, Any]]:
        """
        获取预设详细信息

        Args:
            preset_name: 预设名称

        Returns:
            预设信息字典
        """
        return self.preset_manager.get_preset_info(preset_name)

    def search_presets(self, keyword: str) -> List[str]:
        """
        搜索预设（按名称或描述）

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的预设名称列表
        """
        return self.preset_manager.search_presets(keyword)

    def create_custom_preset(self, preset_name: str, config: PresetConfig) -> bool:
        """
        创建自定义预设

        Args:
            preset_name: 预设名称（不含.json后缀）
            config: PresetConfig 对象

        Returns:
            是否成功创建
        """
        return self.preset_manager.create_custom_preset(preset_name, config)

    def get_preset_names(self) -> List[str]:
        """
        获取所有可用预设名称

        Returns:
            预设名称列表
        """
        return self.preset_manager.get_preset_names()

    def recognize_preset_from_nlu(self, user_input: str) -> Optional[str]:
        """
        从自然语言输入中识别预设名称

        Args:
            user_input: 用户输入文本

        Returns:
            识别的预设名称，如果未识别到返回 None
        """
        user_input_lower = user_input.lower()

        # 定义关键词到预设名称的映射
        preset_keywords = {
            "youtube": ["youtube", "yt", "油管"],
            "bilibili": ["bilibili", "b站", "哔哩哔哩", "bishi"],
            "wechat": ["wechat", "weixin", "微信", "weixin"],
            "douyin": ["douyin", "抖音", "tiktok china"],
            "social_media": ["social", "社交媒体", "instagram", "tiktok", "twitter", "facebook"],
            "archival": ["archive", "archival", "存档", "archive", "收藏"],
            "preview": ["preview", "预览", "快速预览", "draft"],
            "web_optimized": ["web", "网站", "web optimized", "网页", "在线播放", "流媒体"],
        }

        # 搜索匹配的预设
        for preset_name, keywords in preset_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return preset_name

        return None

    # ==================== 两遍编码和质量感知压缩相关方法 ====================

    def compress_to_target_size(
        self,
        input_file: str,
        target_size_mb: float,
        output_file: Optional[str] = None,
        min_quality: float = 0.7,
        max_attempts: int = 3,
        preset: str = "medium",
        codec: str = "libx264",
    ) -> Optional[Dict]:
        """
        压缩视频到目标文件大小（使用两遍编码 + 自适应码率控制）

        Args:
            input_file: 输入文件路径
            target_size_mb: 目标文件大小（MB）
            output_file: 输出文件路径（可选，默认添加 _compressed 后缀）
            min_quality: 最低可接受质量（0-1）
            max_attempts: 最大尝试次数
            preset: 编码预设
            codec: 视频编解码器

        Returns:
            压缩结果字典，包含 success, output_file, actual_size_mb, error_pct 等
        """
        try:
            from ..encoders.quality_aware_compressor import QualityAwareCompressor
        except ImportError:
            from encoders.quality_aware_compressor import QualityAwareCompressor

        # 设置输出文件
        if output_file is None:
            input_path = Path(input_file)
            output_file = str(
                input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
            )

        # 创建压缩器
        compressor = QualityAwareCompressor()

        # 执行压缩
        result = compressor.compress_to_size(
            input_file=input_file,
            target_size_mb=target_size_mb,
            min_quality=min_quality,
            max_attempts=max_attempts,
            preset=preset,
            codec=codec,
            enable_quality_check=False,  # 默认不启用高级质量检查（PSNR/SSIM/VMAF）
        )

        # 转换为字典返回
        return {
            "success": result.success,
            "output_file": result.output_file,
            "actual_size_mb": result.actual_size_mb,
            "target_size_mb": result.target_size_mb,
            "error_pct": result.error_pct,
            "attempts": result.attempts,
            "final_bitrate": result.final_bitrate,
            "encoding_time": result.encoding_time,
            "error": result.error if not result.success else None,
        }

    def optimize_for_size(
        self,
        input_file: str,
        target_size_mb: float,
        output_file: Optional[str] = None,
        max_attempts: int = 3,
        preset: str = "medium",
        codec: str = "libx264",
    ) -> Optional[Dict]:
        """
        优化视频以符合目标文件大小（仅码率优化，不检查质量）

        Args:
            input_file: 输入文件路径
            target_size_mb: 目标文件大小（MB）
            output_file: 输出文件路径（可选）
            max_attempts: 最大尝试次数
            preset: 编码预设
            codec: 视频编解码器

        Returns:
            优化结果字典
        """
        try:
            from ..encoders.adaptive_bitrate import AdaptiveBitrateController
        except ImportError:
            from encoders.adaptive_bitrate import AdaptiveBitrateController

        # 设置输出文件
        if output_file is None:
            input_path = Path(input_file)
            output_file = str(input_path.parent / f"{input_path.stem}_optimized{input_path.suffix}")

        # 获取视频时长
        duration = self._get_video_duration(input_file)
        if duration <= 0:
            return {"success": False, "error": "无法获取视频时长"}

        # 创建自适应码率控制器
        controller = AdaptiveBitrateController()

        # 执行优化
        result = controller.optimize_bitrate(
            input_file=input_file,
            output_file=output_file,
            target_size_mb=target_size_mb,
            duration_seconds=duration,
            max_attempts=max_attempts,
            preset=preset,
            codec=codec,
        )

        return {
            "success": result.success,
            "output_file": result.output_file,
            "actual_size_mb": result.actual_size_mb,
            "target_size_mb": result.target_size_mb,
            "error_pct": result.error_pct,
            "attempts": result.attempts,
            "final_bitrate": result.final_bitrate,
            "error": result.error if not result.success else None,
            "history": result.history,
        }

    def assess_quality(
        self, input_file: str, output_file: str, metric: str = "basic"
    ) -> Optional[Dict]:
        """
        评估视频质量

        Args:
            input_file: 原始视频文件
            output_file: 压缩后的视频文件
            metric: 质量评估指标（basic, psnr, ssim, vmaf）

        Returns:
            质量评分字典
        """
        try:
            from ..encoders.quality_aware_compressor import QualityAwareCompressor, QualityMetric
        except ImportError:
            from encoders.quality_aware_compressor import QualityAwareCompressor, QualityMetric

        # 转换指标
        metric_map = {
            "basic": QualityMetric.BASIC,
            "psnr": QualityMetric.PSNR,
            "ssim": QualityMetric.SSIM,
            "vmaf": QualityMetric.VMAF,
        }

        quality_metric = metric_map.get(metric.lower(), QualityMetric.BASIC)

        # 创建压缩器并评估质量
        compressor = QualityAwareCompressor()
        score = compressor.assess_quality(input_file, output_file, quality_metric)

        return {
            "metric": metric,
            "score": score.score,
            "passed": score.passed,
            "details": score.details,
            "psnr": score.psnr,
            "ssim": score.ssim,
            "vmaf": score.vmaf,
        }

    def _get_video_duration(self, file_path: str) -> float:
        """获取视频时长（内部辅助方法）"""
        try:
            cmd = [
                "ffprobe",
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

    # ==================== 关键帧分析和智能剪辑相关方法 ====================

    def suggest_trim_strategy(
        self,
        start_time: float,
        duration: float,
        video_path: str,
        prefer_mode: str = "auto"
    ) -> TrimStrategy:
        """
        根据关键帧位置建议剪辑策略

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_path: 视频文件路径
            prefer_mode: 偏好模式 ("auto", "fast", "precise")

        Returns:
            TrimStrategy: 剪辑策略建议
        """
        return self.keyframe_analyzer.suggest_trim_strategy(
            start_time=start_time,
            duration=duration,
            video_path=video_path,
            prefer_mode=prefer_mode
        )

    def detect_keyframes(
        self,
        video_path: str,
        max_frames: Optional[int] = None
    ) -> List[Dict]:
        """
        检测视频中的关键帧

        Args:
            video_path: 视频文件路径
            max_frames: 最大检测帧数（None 表示全部检测）

        Returns:
            关键帧信息列表
        """
        keyframes = self.keyframe_analyzer.detect_keyframes(video_path, max_frames)
        if keyframes is None:
            return []
        return [
            {
                "time": kf.time,
                "frame_number": kf.frame_number,
                "keyframe_type": kf.keyframe_type
            }
            for kf in keyframes
        ]

    def should_enable_sync_fix(
        self,
        start_time: Optional[float] = None,
        duration: Optional[float] = None,
        video_duration: Optional[float] = None,
        copy_mode: bool = False
    ) -> Tuple[bool, str]:
        """
        判断是否需要启用音视频同步修复

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_duration: 视频总时长（秒）
            copy_mode: 是否使用流拷贝模式

        Returns:
            (是否需要修复, 原因说明)
        """
        return self.keyframe_analyzer.should_enable_sync_fix(
            start_time=start_time,
            duration=duration,
            video_duration=video_duration,
            copy_mode=copy_mode
        )

    def get_sync_fix_params(self) -> List[str]:
        """
        获取音视频同步修复的 FFmpeg 参数

        Returns:
            FFmpeg 参数列表
        """
        return self.keyframe_analyzer.get_sync_fix_params()

    def analyze_trim_position(
        self,
        start_time: float,
        video_duration: float
    ) -> Dict:
        """
        分析剪辑位置类型和风险

        Args:
            start_time: 起始时间（秒）
            video_duration: 视频总时长（秒）

        Returns:
            位置分析结果
        """
        position = self.keyframe_analyzer.analyze_edit_position(start_time, video_duration)

        risk_level = "low"
        if position == "start":
            risk_level = "low"
            description = "从视频开头开始剪辑"
        elif position == "middle":
            risk_level = "high"
            description = "从视频中间开始剪辑（高风险）"
        else:  # "end"
            risk_level = "medium"
            description = "从视频结尾开始剪辑（中风险）"

        return {
            "position": position,
            "risk_level": risk_level,
            "description": description,
            "recommendations": self._get_position_recommendations(position)
        }

    def _get_position_recommendations(self, position: str) -> List[str]:
        """
        根据剪辑位置获取建议

        Args:
            position: 位置类型 ("start", "middle", "end")

        Returns:
            建议列表
        """
        if position == "start":
            return [
                "可以使用流拷贝模式（-c copy）",
                "通常不需要音视频同步修复",
                "处理速度最快"
            ]
        elif position == "middle":
            return [
                "强烈建议重新编码（不建议使用流拷贝）",
                "必须启用音视频同步修复参数",
                "使用 -avoid_negative_ts make_zero",
                "使用 -fflags +genpts"
            ]
        else:  # "end"
            return [
                "建议重新编码",
                "可能产生负时间戳，建议启用同步修复",
                "使用 -avoid_negative_ts make_zero",
                "使用 -fflags +genpts"
            ]

    def decide_encoding_params_with_sync_fix(
        self,
        analysis: Dict,
        user_params: Dict,
        start_time: Optional[float] = None,
        duration: Optional[float] = None,
        prefer_mode: str = "auto"
    ) -> Dict:
        """
        决定最优编码参数（包含音视频同步修复和关键帧对齐）

        Args:
            analysis: 视频分析结果
            user_params: 用户提供的参数
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            prefer_mode: 剪辑模式偏好 ("auto", "fast", "precise")

        Returns:
            最优的编码参数字典（包含同步修复参数）
        """
        # 获取基础编码参数
        params = self.decide_encoding_params(analysis, user_params)

        # 判断是否需要音视频同步修复
        video_path = analysis.get("file_path", "")
        video_duration = analysis.get("duration", 0)
        copy_mode = user_params.get("copy_streams", False)

        need_sync_fix, sync_fix_reason = self.should_enable_sync_fix(
            start_time=start_time,
            duration=duration,
            video_duration=video_duration,
            copy_mode=copy_mode
        )

        params["need_sync_fix"] = need_sync_fix
        params["sync_fix_reason"] = sync_fix_reason

        if need_sync_fix:
            params["sync_fix_params"] = self.get_sync_fix_params()

        # 如果有剪辑操作，分析关键帧
        if start_time is not None and duration is not None and video_path:
            try:
                trim_strategy = self.suggest_trim_strategy(
                    start_time=start_time,
                    duration=duration,
                    video_path=video_path,
                    prefer_mode=prefer_mode
                )

                params["trim_strategy"] = {
                    "mode": trim_strategy.mode,
                    "reason": trim_strategy.reason,
                    "adjusted_start_time": trim_strategy.adjusted_start_time,
                    "adjusted_end_time": trim_strategy.adjusted_end_time,
                    "distance_to_nearest_keyframe": trim_strategy.distance_to_nearest_keyframe,
                    "recommended_params": trim_strategy.recommended_params
                }

                # 根据策略调整编码参数
                if trim_strategy.mode == "fast" and trim_strategy.recommended_params:
                    params["copy_streams"] = True
                    if "avoid_negative_ts" in trim_strategy.recommended_params:
                        params["avoid_negative_ts"] = trim_strategy.recommended_params["avoid_negative_ts"]
                    if "fflags" in trim_strategy.recommended_params:
                        params["fflags"] = trim_strategy.recommended_params["fflags"]

            except Exception as e:
                params["trim_strategy_error"] = str(e)

        return params


# 向后兼容：导出ContentTypeLegacy作为ContentType
ContentType = ContentTypeLegacy


# 使用示例
if __name__ == "__main__":
    engine = DecisionEngine()

    # 测试视频分析
    print("测试视频分析:")
    print("请提供视频文件路径进行测试")
    # analysis = engine.analyze_video("test.mp4")
    # print(json.dumps(analysis, indent=2, ensure_ascii=False))

    # 测试编码决策
    print("\n测试编码参数决策:")
    mock_analysis = {
        "video": {
            "width": 1920,
            "height": 1080,
            "fps": 24.0,
            "bitrate": 5000000,
        },
        "audio": {
            "codec": "aac",
            "sample_rate": 48000,
            "channels": 2,
        },
        "duration": 3600,
        "content_type": ContentType.MOVIE.value,
        "complexity": "medium",
    }

    mock_user_params = {
        "target_size_mb": 500,
    }

    decision = engine.decide_encoding_params(mock_analysis, mock_user_params)
    print("编码参数决策:")
    print(json.dumps(decision, indent=2, ensure_ascii=False))
