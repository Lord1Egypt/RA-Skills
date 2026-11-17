"""
BiliYouTik2Brain — 小红书平台适配器

采集链路：
  1. URL → 提取 note_id
  2. xhs SDK 解析页面 → 获取视频直链
  3. requests 下载视频
  4. ffmpeg 提取音频 (m4a)

依赖: pip install xhs
"""

from typing import Optional
import os, re, subprocess, json, tempfile
import requests

from .base import BaseExtractor
from ..core.schemas import (
    Platform, VideoInfo, AudioResult, SubtitleResult,
    CommentResult, CollectResult
)


# ---- 工具函数 ----

def _extract_note_id(url: str) -> Optional[str]:
    """从小红书URL中提取 note_id (24位hex)"""
    m = re.search(r'xiaohongshu\.com/(?:explore|discovery/item)/([a-f0-9]{24})', url)
    if m:
        return m.group(1)
    return None


def _get_note_info_from_api(note_id: str) -> Optional[dict]:
    """通过 xhs SDK 从 HTML 获取笔记信息"""
    try:
        from xhs import XhsClient
        client = XhsClient()
        result = client.get_note_by_id_from_html(note_id)
        if result and result.get("note_card"):
            return result["note_card"]
        return None
    except ImportError:
        print("  [xhs] 未安装 xhs 库: pip install xhs")
        return None
    except Exception as e:
        print(f"  [xhs] SDK解析失败: {e}")
        return None


def _download_video(video_url: str, output_path: str) -> bool:
    """下载视频文件"""
    try:
        resp = requests.get(video_url, stream=True, timeout=60)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return os.path.getsize(output_path) > 0
    except Exception as e:
        print(f"  [下载] 视频下载失败: {e}")
        return False


def _extract_audio_from_video(video_path: str, output_path: str) -> bool:
    """从视频文件中提取音频"""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "aac",
            "-b:a", "128k",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        return os.path.getsize(output_path) > 0
    except Exception as e:
        print(f"  [音频] ffmpeg提取失败: {e}")
        return False


# ---- 适配器 ----

class XiaoHongShuExtractor(BaseExtractor):
    """小红书视频采集适配器"""

    platform = Platform.XIAOHONGSHU
    domain_regex = r'(xiaohongshu\.com|xhslink\.com)'

    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """获取笔记元信息"""
        note_id = _extract_note_id(url)
        if not note_id:
            return VideoInfo(
                platform=Platform.XIAOHONGSHU,
                video_id="unknown",
                title="(小红书 - 无法识别笔记ID)",
                duration=0,
                uploader="",
                uploader_id="",
                url=url,
            )

        note_info = _get_note_info_from_api(note_id)

        if note_info:
            title = note_info.get("title", "") or note_info.get("display_title", "")
            desc = note_info.get("desc", "") or ""
            user_info = note_info.get("user", {}) or {}
            uploader = user_info.get("nickname", "") if isinstance(user_info, dict) else ""
            uploader_id = user_info.get("user_id", "") if isinstance(user_info, dict) else ""
            video_info = note_info.get("video", {}) or {}
            has_video = bool(video_info and video_info.get("media", {}).get("stream", {}))

            return VideoInfo(
                platform=Platform.XIAOHONGSHU,
                video_id=note_id,
                title=title or desc[:80] or "(无标题)",
                duration=0,
                uploader=uploader,
                uploader_id=uploader_id,
                url=url,
                raw={"note_id": note_id, "desc": desc, "type": "video" if has_video else "image"},
            )
        else:
            return VideoInfo(
                platform=Platform.XIAOHONGSHU,
                video_id=note_id,
                title="(小红书 - SDK解析失败)",
                duration=0,
                uploader="",
                uploader_id="",
                url=url,
                raw={"note_id": note_id},
            )

    def extract_audio(self, video: VideoInfo) -> AudioResult:
        """下载视频并提取音频"""
        note_id = video.video_id
        if not note_id or note_id == "unknown":
            return AudioResult(success=False, error="无法获取note_id")

        note_info = _get_note_info_from_api(note_id)
        if not note_info:
            return AudioResult(success=False, error="获取笔记信息失败")

        # 解析视频流
        video_info = note_info.get("video", {}) or {}
        media = video_info.get("media", {}) or {}
        stream = media.get("stream", {}) or {}
        h264_streams = stream.get("h264", [])

        if not h264_streams:
            # 尝试备选字段
            consumer = video_info.get("consumer", {}) or {}
            origin_key = consumer.get("origin_video_key", "")
            if origin_key:
                from xhs.core import video_cdns
                import random
                video_url = f"{random.choice(video_cdns)}/{origin_key}"
            else:
                return AudioResult(success=False, error="该笔记无视频流（可能是图文笔记）")
        else:
            video_url = h264_streams[0].get("master_url", "")

        if not video_url:
            return AudioResult(success=False, error="无法获取视频下载链接")

        # 下载视频
        tmp_dir = tempfile.mkdtemp(prefix="xhs_video_")
        video_path = os.path.join(tmp_dir, "video.mp4")
        audio_path = os.path.join(tmp_dir, "audio.m4a")

        print(f"  [下载] 下载视频...")
        if not _download_video(video_url, video_path):
            return AudioResult(success=False, error="视频下载失败")

        size = os.path.getsize(video_path)
        print(f"  [下载] 视频 {size // 1024}KB")

        # 提取音频
        if not _extract_audio_from_video(video_path, audio_path):
            return AudioResult(success=True, file_path=video_path, format="mp4", duration_s=0)

        # 获取时长
        duration = 0
        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", audio_path],
                capture_output=True, text=True, timeout=10
            )
            if probe.returncode == 0 and probe.stdout.strip():
                duration = int(float(probe.stdout.strip()))
        except Exception:
            pass

        try:
            os.remove(video_path)
        except Exception:
            pass

        return AudioResult(
            success=True,
            file_path=audio_path,
            format="m4a",
            duration_s=duration,
        )

    def extract_subtitle(self, video: VideoInfo) -> SubtitleResult:
        """小红书无公开字幕"""
        return SubtitleResult(success=False, error="小红书无字幕")

    def extract_comments(self, video: VideoInfo) -> CommentResult:
        return CommentResult(success=False, error="小红书评论待实现")


# ─── 自动注册 ────────────────────────────────────────────

from ..core.config import PlatformRegistry
PlatformRegistry.register(XiaoHongShuExtractor)
