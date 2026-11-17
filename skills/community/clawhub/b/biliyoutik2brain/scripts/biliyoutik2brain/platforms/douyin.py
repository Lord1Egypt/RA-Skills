"""
BiliYouTik2Brain — 抖音平台适配器（Web Scraping + yt-dlp 下载）

采集方案：
  1. Web scraping 获取视频元信息和真实下载地址（无需 cookie）
  2. yt-dlp 通过真实地址下载音频
  3. 无公开字幕，无评论 API
"""

from typing import Optional
import os, subprocess, re, json, tempfile, urllib.request, urllib.error

from .base import BaseExtractor
from ..core.schemas import (
    Platform, VideoInfo, AudioResult, SubtitleResult,
    CommentResult, CollectResult
)


class DouyinExtractor(BaseExtractor):
    """抖音视频采集适配器（Web Scraping 驱动）"""

    platform = Platform.DOUYIN
    domain_regex = r'(douyin\.com|iesdouyin\.com)'

    def __init__(self):
        super().__init__()
        self._mcp_available = False
        # Check MCP availability
        try:
            result = subprocess.run(
                ["mcporter", "call", "douyin.parse_douyin_video_info", "share_link=https://v.douyin.com/test/"],
                capture_output=True, text=True, timeout=10
            )
            if "Unknown MCP server" not in result.stderr:
                self._mcp_available = True
        except Exception:
            pass
        
        if self._mcp_available:
            print("  [抖音] MCP 可用")
        else:
            print("  [抖音] 使用 Web Scraping 模式")

    def _fetch_page(self, url: str) -> str:
        """抓取抖音分享页面HTML"""
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')

    def _extract_router_data(self, html: str) -> dict:
        """从页面提取 window._ROUTER_DATA JSON"""
        idx = html.find('window._ROUTER_DATA')
        if idx < 0:
            return {}
        start = html.find('{', idx)
        depth = 0
        end = start
        for i in range(start, min(start + 200000, len(html))):
            if html[i] == '{':
                depth += 1
            elif html[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        try:
            return json.loads(html[start:end])
        except json.JSONDecodeError:
            return {}

    def _get_video_play_url(self, html: str, video_id: str) -> str:
        """从页面提取视频播放地址"""
        # 尝试从 RENDER_DATA 找
        data = self._extract_router_data(html)
        if data:
            loader = data.get('loaderData', {})
            for k, v in loader.items():
                if 'video' in k and isinstance(v, dict):
                    items = v.get('videoInfoRes', {}).get('item_list', [])
                    if items:
                        video = items[0].get('video', {})
                        play = video.get('play_addr', {})
                        urls = play.get('url_list', [])
                        if urls:
                            return urls[0]
        
        # Fallback: 从页面直接找 playwm URL
        m = re.search(r'https://aweme\.snssdk\.com/aweme/v1/playwm/\?[^"\']+', html)
        if m:
            return m.group(0)
        
        return ""

    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """通过 Web Scraping 获取视频元信息"""
        try:
            html = self._fetch_page(url)
            data = self._extract_router_data(html)
            
            if data:
                loader = data.get('loaderData', {})
                for k, v in loader.items():
                    if 'video' in k and isinstance(v, dict):
                        items = v.get('videoInfoRes', {}).get('item_list', [])
                        if items:
                            item = items[0]
                            author = item.get('author', {})
                            stats = item.get('statistics', {})
                            video = item.get('video', {})
                            
                            return VideoInfo(
                                platform=Platform.DOUYIN,
                                video_id=item.get('aweme_id', ''),
                                title=item.get('desc', '(抖音视频)'),
                                duration=int(video.get('duration', 0) or 0) // 1000,  # ms -> s
                                uploader=author.get('nickname', ''),
                                uploader_id=author.get('uid', ''),
                                url=url,
                                view_count=stats.get('play_count', 0) or 0,
                                like_count=stats.get('digg_count', 0) or 0,
                            )
        except Exception as e:
            print(f"  [抖音] Web Scraping 获取信息失败: {e}")
        
        return VideoInfo(
            platform=Platform.DOUYIN,
            video_id="douyin_fallback",
            title="(抖音视频)",
            duration=0,
            uploader="",
            uploader_id="",
            url=url,
        )

    def _get_download_url(self, url: str, video_id: str) -> str:
        """获取视频下载地址（优先 Web Scraping 获取 playwm URL）"""
        html = self._fetch_page(url)
        play_url = self._get_video_play_url(html, video_id)
        if play_url:
            return play_url
        
        # Fallback: 尝试 MCP
        try:
            from . import douyin as _dy
            return _dy._mcp_get_download_url(url)
        except Exception:
            pass
        
        return ""

    def extract_audio(self, video: VideoInfo) -> AudioResult:
        """下载音频（Web Scraping 获取真实地址 → yt-dlp 下载）"""
        try:
            video_id = video.video_id or "douyin"
            dl_url = self._get_download_url(video.url, video_id)
            
            if not dl_url:
                return AudioResult(
                    success=False,
                    error="无法获取视频下载地址（需要cookie或MCP）",
                )
            
            out_dir = "/tmp/douyin_b2b"
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"douyin_{video_id}.%(ext)s")

            cmd = [
                "yt-dlp",
                "-x", "--audio-format", "m4a",
                "-o", out_path,
                "--no-playlist",
                "--socket-timeout", "30",
                dl_url,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if proc.returncode != 0:
                print(f"  [抖音] yt-dlp 警告: {proc.stderr[:200]}")
            
            # 找到下载的文件
            for fname in os.listdir(out_dir):
                if fname.startswith(f"douyin_{video_id}") and fname.endswith((".m4a", ".mp3", ".webm", ".mp4")):
                    filepath = os.path.join(out_dir, fname)
                    if not fname.endswith(".m4a"):
                        m4a_path = os.path.join(out_dir, f"douyin_{video_id}.m4a")
                        subprocess.run([
                            "ffmpeg", "-y", "-i", filepath,
                            "-c:a", "aac", "-b:a", "128k",
                            m4a_path
                        ], capture_output=True, timeout=60)
                        if os.path.exists(m4a_path):
                            return AudioResult(
                                success=True,
                                file_path=m4a_path,
                                format="m4a",
                                duration_s=0,
                            )
                    return AudioResult(
                        success=True,
                        file_path=filepath,
                        format="m4a",
                        duration_s=0,
                    )

            return AudioResult(
                success=False,
                error=f"yt-dlp 下载完成但未找到音频文件",
            )
        except Exception as e:
            return AudioResult(
                success=False,
                error=f"抖音音频下载失败: {str(e)}",
            )

    def extract_subtitle(self, video: VideoInfo) -> SubtitleResult:
        """抖音无公开字幕"""
        return SubtitleResult(success=False, error="抖音无字幕")

    def extract_comments(self, video: VideoInfo) -> CommentResult:
        """抖音评论（暂未支持）"""
        return CommentResult(success=False, error="抖音评论待实现")


# ─── 注册 ────────────────────────────────────────────────

from ..core.config import PlatformRegistry
PlatformRegistry.register(DouyinExtractor)
