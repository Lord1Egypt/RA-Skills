"""
BiliYouTik2Brain — 统一资源对象 VideoResource

职责：封装视频处理中的核心资源（音频文件/视频文件/字幕文本），
     提供内存优先+磁盘备份的访问接口，消除裸文件路径传递。

v1.0 — 第二阶段：资源抽象
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# ═══════════════════════════════════════════════════════════════
# 错误分级枚举
# ═══════════════════════════════════════════════════════════════

from enum import Enum, auto


class ErrorTier(Enum):
    """错误分级：不同类型走不同恢复策略"""
    RECOVERABLE  = auto()   # 可恢复：网络超时、死锁 → 重试
    BUSINESS     = auto()   # 业务错误：视频下架、字幕缺失 → 终止但汇报
    ENVIRONMENT  = auto()   # 环境错误：磁盘满、内存溢出 → 降级处理


# ═══════════════════════════════════════════════════════════════
# ResourceError — 带分级标识的错误
# ═══════════════════════════════════════════════════════════════

class ResourceError(Exception):
    """带分级的资源错误"""
    def __init__(self, message: str, tier: ErrorTier = ErrorTier.BUSINESS):
        super().__init__(message)
        self.tier = tier


# ═══════════════════════════════════════════════════════════════
# VideoResource — 统一资源封装
# ═══════════════════════════════════════════════════════════════

@dataclass
class VideoResource:
    """视频处理资源封装 — 内存优先，磁盘备份"""

    # 音频
    audio_path: Optional[str] = None        # 本地音频文件路径
    audio_size_bytes: int = 0               # 音频文件大小
    audio_loaded: bool = False              # 是否加载到内存
    audio_data: Optional[bytes] = None      # 内存中的音频数据（小文件）

    # 视频
    video_path: Optional[str] = None        # 本地视频文件路径（OCR用）
    video_size_bytes: int = 0

    # 字幕
    subtitle_text: str = ""                 # 字幕文本内容（内存）
    subtitle_source: str = ""               # "api" | "ai" | "none"

    # 元信息
    disk_free_bytes: int = 0                # 所在磁盘剩余空间
    total_bytes_written: int = 0            # 本次写入总量

    # 健康状态
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def audio_exists(self) -> bool:
        return self.audio_path is not None and os.path.exists(self.audio_path)

    @property
    def video_exists(self) -> bool:
        return self.video_path is not None and os.path.exists(self.video_path)

    def has_audio(self) -> bool:
        """是否有可用音频（内存或磁盘）"""
        return self.audio_loaded or self.audio_exists

    def load_audio(self, max_memory_mb: float = 200) -> bool:
        """将音频加载到内存（小文件适用）"""
        if self.audio_loaded:
            return True
        if not self.audio_exists:
            return False
        fs = os.path.getsize(self.audio_path)
        if fs > max_memory_mb * 1024 * 1024:
            return False  # 太大，不加载
        try:
            with open(self.audio_path, "rb") as f:
                self.audio_data = f.read()
            self.audio_loaded = True
            return True
        except Exception as e:
            self.errors.append(f"加载音频失败: {e}")
            return False

    def free_audio_memory(self):
        """释放内存中的音频数据"""
        self.audio_data = None
        self.audio_loaded = False

    def cleanup_disk(self):
        """清理磁盘音频文件（释放空间）"""
        if self.audio_path and os.path.exists(self.audio_path):
            try:
                os.remove(self.audio_path)
                self.audio_path = None
            except Exception:
                pass
        if self.video_path and os.path.exists(self.video_path):
            try:
                os.remove(self.video_path)
                self.video_path = None
            except Exception:
                pass

    def check_disk_space(self, min_free_bytes: int = 500 * 1024 * 1024) -> bool:
        """检查磁盘空间是否充足"""
        if self.audio_path:
            d = os.path.dirname(self.audio_path)
            stat = os.statvfs(d)
            self.disk_free_bytes = stat.f_frsize * stat.f_bavail
            return self.disk_free_bytes >= min_free_bytes
        return True

    def summary(self) -> str:
        """人类可读的资源摘要"""
        parts = []
        if self.audio_path:
            parts.append(f"音频: {os.path.basename(self.audio_path)} ({self.audio_size_bytes//1024}KB)")
        if self.audio_loaded:
            parts.append(f"音频已在内存")
        if self.video_path:
            parts.append(f"视频: {os.path.basename(self.video_path)} ({self.video_size_bytes//1024//1024}MB)")
        if self.subtitle_text:
            parts.append(f"字幕: {len(self.subtitle_text)}字 [{self.subtitle_source}]")
        if self.errors:
            parts.append(f"错误: {len(self.errors)}条")
        return " | ".join(parts) if parts else "空"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio_path": self.audio_path,
            "video_path": self.video_path,
            "subtitle_text": self.subtitle_text[:200] if self.subtitle_text else "",
            "subtitle_source": self.subtitle_source,
            "disk_free_gb": self.disk_free_bytes / (1024**3),
            "errors": self.errors,
            "warnings": self.warnings,
        }
