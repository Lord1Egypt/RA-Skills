"""
BiliYouTik2Brain — 统一数据模型
所有模块之间通过这些Schema通信，不耦合具体的平台实现
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum, auto
from datetime import datetime


# ─── 平台枚举 ───────────────────────────────────────────

class Platform(Enum):
    BILIBILI     = "bilibili"
    YOUTUBE      = "youtube"
    DOUYIN       = "douyin"
    XIAOHONGSHU  = "xiaohongshu"
    UNKNOWN      = "unknown"


# ─── 视频元信息 ──────────────────────────────────────────

@dataclass
class VideoInfo:
    """从平台获取的原始视频元信息"""
    platform: Platform
    video_id: str           # BV号 / YouTube ID / 抖音ID
    title: str
    duration: int           # 秒
    uploader: str           # UP主名
    uploader_id: str        # UP主ID
    url: str                # 原始链接
    error: str = ""
    description: str = ""
    view_count: int = 0
    like_count: int = 0
    publish_time: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)  # 平台原始返回

    def to_dict(self) -> Dict:
        return asdict(self)


# ─── 音频/字幕/评论 ──────────────────────────────────────

@dataclass
class AudioResult:
    """音频获取结果"""
    success: bool = False
    file_path: Optional[str] = None     # 本地音频文件路径
    duration_s: int = 0
    format: str = "m4a"
    error: Optional[str] = None


@dataclass
class SubtitleResult:
    """字幕获取结果（可选fast lane）"""
    success: bool = False
    text: str = ""
    quality: float = 0.0        # 0~1，≥0.7可跳过whisper
    segments: List[Dict] = field(default_factory=list)
    source: str = ""            # "api" / "ai" / "none"
    error: Optional[str] = None


@dataclass 
class CommentResult:
    """评论采集结果"""
    success: bool = False
    hot: List[Dict] = field(default_factory=list)
    new: List[Dict] = field(default_factory=list)
    total: int = 0
    insights: List[str] = field(default_factory=list)
    error: Optional[str] = None


# ─── 转录结果 ────────────────────────────────────────────

@dataclass
class TranscriptionResult:
    """转录+修复+分析的完整结果"""
    video: VideoInfo
    raw_text: str = ""              # 原始whisper输出
    corrected_text: str = ""        # LLM修复后文本
    confidence: float = 0.0         # 整体置信度
    segments: List[Dict] = field(default_factory=list)  # 每段置信度
    
    subtitle: SubtitleResult = field(default_factory=SubtitleResult)
    audio: AudioResult = field(default_factory=AudioResult)
    comments: CommentResult = field(default_factory=CommentResult)
    
    analysis: Optional[Dict] = None     # 结构化分析结果
    file_path: Optional[str] = None     # 转录文件保存路径
    
    duration_s: int = 0
    model_used: str = ""
    pipeline_time_s: float = 0.0
    error: Optional[str] = None


# ─── 知识文档 ────────────────────────────────────────────

@dataclass
class KnowledgeDoc:
    """结构化知识条目"""
    title: str
    domain: str                 # "trading" / "programming" / "finance"
    rules: List[Dict] = field(default_factory=list)
    summary: str = ""
    sources: List[str] = field(default_factory=list)  # BV号列表
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.0     # 交叉验证置信度
    version: str = "1.0"


# ─── 采集结果（平台适配器输出） ───────────────────────────

@dataclass
class CollectResult:
    """平台适配器的完整采集输出"""
    video: VideoInfo
    audio: AudioResult
    subtitle: SubtitleResult
    comments: CommentResult
    video_file: str = ""  # P0: 视频文件路径（用于OCR辅助纠错），非所有平台都有

    def to_dict(self) -> Dict:
        return {
            "video": self.video.to_dict(),
            "audio": asdict(self.audio),
            "subtitle": asdict(self.subtitle),
            "comments": asdict(self.comments),
        }


# ─── 路由决策 ────────────────────────────────────────────

@dataclass
class RouteDecision:
    """assess_and_route() 的输出"""
    target: str = "cloud"           # "cloud" | "local" | "pending"
    use_vad: bool = False
    use_chunked: bool = False
    skip_sampling: bool = False
    model: str = "base"
    reason: str = ""
    
    # 资源信息（当 target="pending" 时）
    estimated_workload: float = 0.0
    cloud_capacity: float = 0.0
    local_capacity: float = 0.0
    cloud_available: bool = True
    local_available: bool = False
    required_cores: int = 4
    required_ram_gb: float = 4.0

    def to_dict(self) -> Dict:
        return asdict(self)


# ─── 待处理工作流 ─────────────────────────────────────────

@dataclass
class PendingWorkflow:
    """因算力不足暂存的工作流任务"""
    id: str = ""
    url: str = ""
    created_at: str = ""
    duration_s: int = 0
    estimated_workload: float = 0.0
    status: str = "pending"  # pending | scheduled | processing | done
    scheduled_at: Optional[str] = None
    notes: str = ""
