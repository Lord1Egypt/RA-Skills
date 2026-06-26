"""
FFmpeg Master - 全能视频处理技能
脚本模块初始化文件
"""

__version__ = "2.0.0"
__author__ = "FFmpeg Master Team"

# 核心引擎
from .core.nlu_engine import NLUEngine
from .core.decision_engine import DecisionEngine
from .core.gpu_detector import GPUDetector

# 分析器
from .analyzers.bitrate_calculator import BitrateCalculator
from .analyzers.video_type_analyzer import VideoTypeAnalyzer
from .analyzers import VideoContentType, VideoAnalysisResult

# 编码器
from .encoders.param_optimizer import ParamOptimizer, EncodingParams

# 构建器
from .builders.ffmpeg_builder import FFmpegBuilder

# 处理器
from .processors.subtitle_processor import SubtitleProcessor
from .processors.batch_processor import BatchProcessor

# 验证器
from .validators.quality_validator import QualityValidator

__all__ = [
    # 核心引擎
    "NLUEngine",
    "DecisionEngine",
    "GPUDetector",
    # 分析器
    "BitrateCalculator",
    "VideoTypeAnalyzer",
    "VideoContentType",
    "VideoAnalysisResult",
    # 编码器
    "ParamOptimizer",
    "EncodingParams",
    # 构建器
    "FFmpegBuilder",
    # 处理器
    "SubtitleProcessor",
    "BatchProcessor",
    # 验证器
    "QualityValidator",
]
