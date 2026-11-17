"""
BiliYouTik2Brain — 平台适配器抽象基类

每个平台实现自己的 Extractor，继承 BaseExtractor。
类似 yt-dlp 的 InfoExtractor 架构。
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import re

from ..core.schemas import (
    Platform, VideoInfo, AudioResult, SubtitleResult, 
    CommentResult, CollectResult
)


class BaseExtractor(ABC):
    """平台适配器抽象基类
    
    每个平台一个子类，必须实现:
    - extract_video_info()
    - extract_audio()
    - extract_subtitle()
    - extract_comments() [可选]
    
    统一输出: CollectResult
    """

    # ⚠️ 子类必须设置
    platform: Platform = Platform.UNKNOWN
    domain_regex: str = r""  # 匹配URL的正则

    @classmethod
    def match(cls, url: str) -> bool:
        """判断是否匹配此平台的URL（使用search而非match，匹配URL中任意位置）"""
        return bool(re.search(cls.domain_regex, url))

    @abstractmethod
    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """获取视频元信息"""
        ...

    @abstractmethod
    def extract_audio(self, video_info: VideoInfo) -> AudioResult:
        """下载/获取音频"""
        ...

    @abstractmethod
    def extract_subtitle(self, video_info: VideoInfo) -> SubtitleResult:
        """获取字幕（可选fast lane）"""
        ...

    def extract_comments(self, video_info: VideoInfo) -> CommentResult:
        """获取评论（可选）"""
        return CommentResult(success=False, error="not implemented")

    def collect(self, url: str) -> CollectResult:
        """完整采集流程（元信息+音频+字幕+评论+视频）"""
        video = self.extract_video_info(url)
        if not video:
            raise ValueError(f"无法获取视频信息: {url}")

        audio = self.extract_audio(video)
        subtitle = self.extract_subtitle(video)
        comments = self.extract_comments(video)

        # 视频文件（供 OCR 抽帧，可选）
        video_file = ""
        if hasattr(self, 'extract_video'):
            try:
                vf = self.extract_video(video)
                if vf:
                    video_file = vf
            except Exception:
                pass  # 视频下载失败不阻塞管线

        return CollectResult(
            video=video,
            audio=audio,
            subtitle=subtitle,
            comments=comments,
            video_file=video_file,
        )
