"""
FFmpeg Master - 分析器模块
包含视频类型分析器、质量评估器、码率计算器和关键帧分析器
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional

from .bitrate_calculator import BitrateCalculator
from .keyframe_analyzer import KeyFrameAnalyzer, KeyFrame, TrimStrategy


class VideoContentType(Enum):
    """视频内容类型枚举"""

    SCREEN_RECORDING = "screen_recording"  # 屏幕录制
    ANIME = "anime"  # 动漫
    SPORTS = "sports"  # 体育
    MUSIC_VIDEO = "music_video"  # 音乐视频
    MOVIE = "movie"  # 电影/电视剧
    OLD_VIDEO = "old_video"  # 老旧视频


@dataclass
class VideoAnalysisResult:
    """视频分析结果数据类"""

    content_type: VideoContentType
    confidence: float  # 置信度 (0-1)
    motion_score: float  # 运动幅度分数 (0-1)
    complexity_score: float  # 复杂度分数 (0-1)
    color_score: float  # 色彩分数 (0-1)
    analysis_notes: Optional[str] = None  # 分析备注


__all__ = [
    "BitrateCalculator",
    "VideoContentType",
    "VideoAnalysisResult",
    "KeyFrameAnalyzer",
    "KeyFrame",
    "TrimStrategy",
]
