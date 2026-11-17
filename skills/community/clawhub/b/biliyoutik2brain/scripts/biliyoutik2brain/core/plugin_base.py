"""
BiliYouTik2Brain — 插件基类 (v4.0)

所有插件必须继承自对应的基类，实现必需方法。
支持三类插件：
  - PlatformPlugin: 平台适配器（B站/YouTube/抖音/小红书 + 社区扩展）
  - ASRPlugin: 转录引擎（faster-whisper/百炼/openai + 社区扩展）
  - OutputPlugin: 输出模板（Markdown/HTML/JSON/Obsidian + 社区扩展）
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


# ═══════════════════════════════════════════════════════════
#  插件元数据
# ═══════════════════════════════════════════════════════════

@dataclass
class PluginMeta:
    """插件元信息"""
    name: str                    # 插件唯一标识
    version: str                 # 语义化版本号
    author: str = ""             # 作者
    description: str = ""        # 描述
    is_core: bool = False        # 是否核心插件（随技能内置）
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他插件


# ═══════════════════════════════════════════════════════════
#  PlatformPlugin — 平台适配器基类
# ═══════════════════════════════════════════════════════════

class PlatformPlugin(ABC):
    """平台适配器插件基类

    每个平台必须实现 5 个核心方法 + 1 个反爬配置。
    反爬配置是必填项（一等公民设计）。
    """

    @property
    @abstractmethod
    def meta(self) -> PluginMeta:
        """插件元信息"""
        ...

    @property
    @abstractmethod
    def domain_regex(self) -> str:
        """匹配该平台 URL 的正则表达式"""
        ...

    @abstractmethod
    async def get_video_info(self, url: str) -> Dict:
        """获取视频元信息（标题/UP主/时长/简介）"""
        ...

    @abstractmethod
    async def download_audio(self, url: str, output_path: str) -> str:
        """下载音频到指定路径，返回实际路径"""
        ...

    @abstractmethod
    async def download_video(self, url: str, output_path: str) -> str:
        """下载视频到指定路径（用于 OCR 抽帧），返回实际路径"""
        ...

    @abstractmethod
    async def fetch_subtitles(self, url: str) -> List[Dict]:
        """获取字幕列表，返回 [{lang, url, format}]"""
        ...

    @abstractmethod
    async def fetch_comments(self, url: str, limit: int = 100) -> List[Dict]:
        """获取评论列表，返回 [{author, content, likes, reply_to, timestamp}]"""
        ...

    @abstractmethod
    def get_anti_crawl_config(self) -> Dict:
        """反爬配置（必填！一等公民设计）

        返回该平台的反爬策略配置：
        {
            "ua_pool": [...],           # UA 池（可选，默认用通用池）
            "cookie_strategy": "browser_extract | manual | none",
            "cookie_browser": "edge | chrome",  # cookie 来源浏览器
            "proxy_required": bool,      # 是否必须走代理
            "proxy_ports": [7890, 7897, 9981],  # 候选代理端口
            "referer": str,             # Referer header
            "prechecks": [...],         # 下载前预检列表
            "heal_actions": [...],      # 预检失败自愈动作
            "throttle_cooldown": 900,   # 熔断冷却时间（秒）
            "throttle_threshold": 3,    # 连续失败阈值
            "rate_limit": float,        # 请求间隔（秒），0=不限
            "session_warmup": bool,     # 是否需要 Session 预热
        }
        """
        ...

    def get_priority(self) -> int:
        """平台优先级（数字越小越优先匹配 URL）"""
        return 100


# ═══════════════════════════════════════════════════════════
#  ASRPlugin — 转录引擎基类
# ═══════════════════════════════════════════════════════════

class ASRPlugin(ABC):
    """转录引擎插件基类

    支持本地/云端引擎，统一输出带 token 级置信度。
    """

    @property
    @abstractmethod
    def meta(self) -> PluginMeta:
        ...

    @property
    @abstractmethod
    def is_local(self) -> bool:
        """是否本地引擎（本地 = 免费，云端 = 按量计费）"""
        ...

    @abstractmethod
    async def transcribe(self, audio_path: str, language: str = "zh") -> Dict:
        """转录音频，返回标准化结果

        返回格式:
        {
            "text": str,                    # 全文
            "segments": [...],              # 分段 [{start, end, text, confidence}]
            "tokens": [...],                # token 级 [{word, confidence, start, end}]
            "low_confidence_regions": [...], # 低置信区域 [{char_start, char_end, text}]
            "engine": str,                  # 引擎名
            "duration": float,              # 音频时长（秒）
            "chars_per_second": float,      # 处理速度
        }
        """
        ...

    @abstractmethod
    def get_cost_per_minute(self) -> float:
        """每分钟成本（元），本地引擎返回 0.0"""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """引擎是否可用（依赖已安装 + 配置已就绪）"""
        ...

    def get_time_per_minute(self) -> float:
        """每分钟音频处理时间（秒），用于成本预估"""
        return 20.0  # 默认 20 秒/分钟


# ═══════════════════════════════════════════════════════════
#  OutputPlugin — 输出模板基类
# ═══════════════════════════════════════════════════════════

class OutputPlugin(ABC):
    """输出模板插件基类

    定义转录结果的输出格式，支持多格式。
    """

    @property
    @abstractmethod
    def meta(self) -> PluginMeta:
        ...

    @property
    @abstractmethod
    def format_name(self) -> str:
        """格式名（如 "markdown", "html", "json", "obsidian"）"""
        ...

    @abstractmethod
    def render(self, data: Dict) -> str:
        """渲染输出

        data 包含:
        {
            "video_info": {...},
            "transcript": str,
            "analysis": {...},
            "comments_analysis": {...},  # 评论分析（如有）
            "ocr_results": [...],        # OCR 结果（如有）
            "knowledge": {...},          # 知识提取
        }
        """
        ...

    @property
    def file_extension(self) -> str:
        """输出文件扩展名"""
        return ".md"

    @property
    def content_type(self) -> str:
        """MIME 类型"""
        return "text/markdown"
