"""
内容类型检测器
只负责检测内容类型（电影、动画、屏幕录制等）
"""

from enum import Enum
from typing import Dict


class ContentType(Enum):
    """内容类型常量"""

    MOVIE = "movie"  # 电影/电视剧
    ANIMATION = "animation"  # 动画/动漫
    SCREEN_RECORDING = "screen_recording"  # 屏幕录制
    SPORTS = "sports"  # 体育/运动
    MUSIC_VIDEO = "music_video"  # 音乐视频
    GAMEPLAY = "gameplay"  # 游戏实况
    TALKING_HEAD = "talking_head"  # 说话头部（访谈、演讲）
    UNKNOWN = "unknown"  # 未知


class ContentDetector:
    """内容类型检测器"""

    def __init__(self, preset_manager=None):
        """
        初始化内容检测器

        Args:
            preset_manager: 预设管理器（可选），用于加载内容类型预设
        """
        self.preset_manager = preset_manager

    def detect(self, video_info: Dict) -> ContentType:
        """
        检测内容类型

        基于视频特征进行推断：
        - 分辨率和帧率
        - 运动程度（通过文件大小和码率推断）
        - 编码特征

        Args:
            video_info: 视频信息字典

        Returns:
            ContentType: 检测到的内容类型
        """
        video = video_info.get("video")
        if not video:
            return ContentType.UNKNOWN

        width = video["width"]
        height = video["height"]
        fps = video["fps"]
        bitrate = video.get("bitrate", 0)

        # 1920x1080 @ 24fps -> 电影
        if width >= 1920 and abs(fps - 24.0) < 1:
            return ContentType.MOVIE

        # 屏幕录制特征
        if fps >= 30 and bitrate < 5000000:
            return ContentType.SCREEN_RECORDING

        # 体育/运动特征
        if fps >= 50 or fps >= 60:
            return ContentType.SPORTS

        # 动画特征（推断）
        if bitrate < 3000000 and fps <= 30:
            return ContentType.ANIMATION

        return ContentType.UNKNOWN

    def estimate_complexity(self, video_info: Dict) -> str:
        """
        估算内容复杂度

        基于码率和分辨率的关系估算

        Args:
            video_info: 视频信息字典

        Returns:
            str: 复杂度级别 ("simple", "medium", "complex")
        """
        video = video_info.get("video")
        if not video or not video.get("bitrate"):
            return "medium"

        width = video["width"]
        height = video["height"]
        bitrate = video["bitrate"]

        pixels = width * height
        bpp = bitrate * 1000 / pixels  # bits per pixel

        # BPP 阈值（经验值）
        if bpp < 0.05:
            return "simple"  # 简单（低运动、低细节）
        elif bpp < 0.15:
            return "medium"  # 中等
        else:
            return "complex"  # 复杂（高运动、高细节）
