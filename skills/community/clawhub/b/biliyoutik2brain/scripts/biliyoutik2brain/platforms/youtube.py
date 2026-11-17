"""
BiliYouTik2Brain — YouTube平台适配器

基于 yt-dlp，支持字幕优先管线（YouTube字幕质量高，可做fast lane）

功能:
  - yt-dlp 命令拼接
  - 字幕质量 >=0.7 时跳过whisper
  - 评论采集 (Phase 3.1)
"""

from typing import Optional, List, Dict
import os, subprocess, json, tempfile

from .base import BaseExtractor
from ..core.schemas import (
    Platform, VideoInfo, AudioResult, SubtitleResult,
    CommentResult, CollectResult
)


COOKIES_FILE = os.environ.get("YTDLP_COOKIES_FILE", "")

# 如果没有显式设置 cookies，尝试从 Edge 浏览器读取（需要在Edge关闭时运行）
_COOKIES_FROM_BROWSER = (
    not COOKIES_FILE
    and os.environ.get("YTDLP_COOKIES_FROM_BROWSER", "") != "0"
    and not os.environ.get("YTDLP_NO_BROWSER_COOKIES")
)

if _COOKIES_FROM_BROWSER:
    try:
        import subprocess as _sp
        _test = _sp.run(
            ["yt-dlp", "--cookies-from-browser", "edge", "--dump-json",
             "--no-download", "--playlist-end", "1",
             "https://www.youtube.com/watch?v=jNQXAC9IVRw"],
            capture_output=True, text=True, timeout=15
        )
        if "login required" not in _test.stderr.lower() and "sign in" not in _test.stderr.lower():
            COOKIES_FILE = "edge"  # 标记：走 cookies-from-browser
    except Exception:
        pass


def _yt_cookies_arg() -> list:
    """返回 yt-dlp cookies 参数。

    优先级：环境变量 YTDLP_COOKIES_FILE → 自动检测 Edge cookies-from-browser
    返回空列表表示无可用 cookies（yt-dlp 以访客模式运行）。
    """
    if COOKIES_FILE == "edge":
        return ["--cookies-from-browser", "edge"]
    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
        return ["--cookies", COOKIES_FILE]
    return []


def _yt_js_runtime_args() -> list:
    """启用 Node.js 运行时解 YouTube n-challenge（2025.11+ 必须）
    
    参见：https://github.com/yt-dlp/yt-dlp/issues/15012
    """
    return ["--js-runtimes", "node", "--remote-components", "ejs:github"]


def _yt_work_dir() -> str:
    """跨平台临时工作目录"""
    return os.path.join(tempfile.gettempdir(), "yt_work")


class YouTubeExtractor(BaseExtractor):
    """YouTube视频采集适配器"""

    platform = Platform.YOUTUBE
    domain_regex = r'(youtube\.com|youtu\.be)'

    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """使用 yt-dlp 获取视频元信息"""
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download",
                 *_yt_cookies_arg(), *_yt_js_runtime_args(), url],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0 or not result.stdout.strip():
                raise ValueError(f"yt-dlp获取信息失败: {result.stderr[:200]}")
            
            data = json.loads(result.stdout.strip().split("\n")[0])
            return VideoInfo(
                platform=Platform.YOUTUBE,
                video_id=data.get("id", ""),
                title=data.get("title", ""),
                duration=data.get("duration", 0),
                uploader=data.get("uploader", ""),
                uploader_id=data.get("channel_id", ""),
                url=data.get("webpage_url", url),
                description=data.get("description", ""),
                view_count=data.get("view_count", 0),
                like_count=data.get("like_count", 0),
                publish_time=None,
                tags=data.get("tags", []),
                raw=data,
            )
        except Exception as e:
            raise ValueError(f"YouTube信息获取失败: {e}")

    def extract_audio(self, video: VideoInfo) -> AudioResult:
        """用 yt-dlp 提取音频"""
        tmp_dir = _yt_work_dir()
        os.makedirs(tmp_dir, exist_ok=True)
        save_path = os.path.join(tmp_dir, f"{video.video_id}.m4a")
        
        try:
            result = subprocess.run(
                ["yt-dlp", "-x", "--audio-format", "m4a",
                 "-o", save_path, *_yt_cookies_arg(), *_yt_js_runtime_args(), video.url],
                capture_output=True, text=True, timeout=600
            )
            if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
                return AudioResult(
                    success=True,
                    file_path=save_path,
                    duration_s=video.duration,
                    format="m4a"
                )
            return AudioResult(success=False, error=result.stderr[:200])
        except Exception as e:
            return AudioResult(success=False, error=str(e))

    def extract_video(self, video: VideoInfo) -> Optional[str]:
        """下载低分辨率视频（供 OCR 抽帧使用）

        用 yt-dlp 下载 720p/480p 视频，分辨率够 OCR 识别即可。
        返回视频文件路径，失败返回 None（OCR 降级跳过，不阻塞管线）。
        """
        import glob
        tmp_dir = _yt_work_dir()
        os.makedirs(tmp_dir, exist_ok=True)
        base = os.path.join(tmp_dir, video.video_id)
        # 检查已有缓存（不限制扩展名）
        existing = glob.glob(f"{base}.*")
        for p in existing:
            if os.path.getsize(p) > 10000 and not p.endswith('.m4a'):
                return p
        try:
            save_tpl = f"{base}.%(ext)s"
            result = subprocess.run(
                ["yt-dlp", "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
                 "-o", save_tpl, "--no-playlist", "--merge-output-format", "mp4",
                 *_yt_cookies_arg(), *_yt_js_runtime_args(), video.url],
                capture_output=True, text=True, timeout=600
            )
            # 找生成的视频文件
            after = glob.glob(f"{base}*")
            for p in after:
                if os.path.getsize(p) > 10000 and not p.endswith('.m4a'):
                    # 重命名为 .mp4
                    if not p.endswith('.mp4'):
                        new_p = f"{base}.mp4"
                        os.rename(p, new_p)
                        return new_p
                    return p
            return None
        except Exception:
            return None

    def extract_subtitle(self, video: VideoInfo) -> SubtitleResult:
        """用 yt-dlp 获取字幕（YouTube字幕质量通常很好）
        
        这是YouTube的fast lane —— 字幕质量>=0.7可跳过whisper
        """
        tmp_dir = _yt_work_dir()
        os.makedirs(tmp_dir, exist_ok=True)
        
        try:
            result = subprocess.run(
                ["yt-dlp", "--write-subs", "--sub-langs", "zh-Hans,zh,en",
                 "--skip-download", "-o", os.path.join(tmp_dir, f"{video.video_id}"),
                 *_yt_cookies_arg(), *_yt_js_runtime_args(), video.url],
                capture_output=True, text=True, timeout=60
            )
            
            # 检查字幕文件
            for ext in [".zh-Hans.vtt", ".zh.vtt", ".en.vtt", ".vtt"]:
                sub_path = os.path.join(tmp_dir, f"{video.video_id}{ext}")
                if os.path.exists(sub_path):
                    with open(sub_path, encoding="utf-8") as f:
                        text = f.read()
                    # 简单质量分
                    quality = min(1.0, len(text) / (max(1, video.duration) * 0.3))
                    return SubtitleResult(
                        success=True,
                        text=text,
                        quality=max(0.7, quality),
                        source="yt-dlp"
                    )
            
            return SubtitleResult(success=False, error="无可用字幕")
        except Exception as e:
            return SubtitleResult(success=False, error=str(e))

    def extract_comments(self, video: VideoInfo, max_comments: int = 100) -> CommentResult:
        """采集YouTube评论（Phase 3.1）
        
        用 yt-dlp --write-comments 采集评论，
        按热度排序分出 hot/new，
        提取高互动评论中的关键术语作为说话人知识补充。
        
        Args:
            video: 视频元信息
            max_comments: 最多采集数量（默认100条）
        
        Returns:
            CommentResult with hot/new/insights
        """
        try:
            # yt-dlp 写评论到 infojson
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--write-comments",
                 "--max-comments", str(max_comments),
                 "--no-download", *_yt_cookies_arg(), *_yt_js_runtime_args(), video.url],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                return CommentResult(
                    success=False,
                    error=f"yt-dlp评论采集失败: {result.stderr[:200]}"
                )
            
            # 解析 JSON
            data = json.loads(result.stdout.strip().split("\n")[0])
            comments_raw = data.get("comments", [])
            
            if not comments_raw:
                return CommentResult(
                    success=True,
                    hot=[],
                    new=[],
                    total=0,
                    insights=["该视频无可用评论"]
                )
            
            # 规范化评论条目
            parsed = []
            for c in comments_raw:
                if not isinstance(c, dict):
                    continue
                parsed.append({
                    "id": c.get("id", ""),
                    "author": c.get("author", c.get("user", "")),
                    "text": c.get("text", c.get("message", "")).strip(),
                    "timestamp": c.get("timestamp", 0),
                    "like_count": c.get("like_count", c.get("votes", 0)),
                    "is_favorited": c.get("is_favorited", False),
                    "reply_count": c.get("reply_count", 0),
                })
            
            # 过滤空白评论
            parsed = [c for c in parsed if c["text"]]
            
            # 按点赞数排序（热门）
            hot_sorted = sorted(parsed, key=lambda c: c["like_count"], reverse=True)
            # 按时序（新到旧）
            new_sorted = sorted(parsed, key=lambda c: c["timestamp"], reverse=True)
            
            # 取 top 20 热门和 top 20 最新
            hot = hot_sorted[:20]
            new = new_sorted[:20]
            
            # ── 提取洞察 ──
            insights = self._extract_comment_insights(hot, video)
            
            return CommentResult(
                success=True,
                hot=hot,
                new=new,
                total=len(parsed),
                insights=insights,
            )
            
        except subprocess.TimeoutExpired:
            return CommentResult(success=False, error="评论采集超时(120s)")
        except Exception as e:
            return CommentResult(success=False, error=f"评论采集失败: {e}")

    def _extract_comment_insights(self, hot_comments: List[Dict], video: VideoInfo) -> List[str]:
        """从热门评论中提取关键洞察
        
        提取高互动评论中可能包含的关键术语/话题，
        作为说话人知识补充源（适用于知识库冷启动）。
        
        Returns:
            insight 字符串列表
        """
        insights = []
        
        # 如果有高赞评论且有文本内容
        high_engagement = [c for c in hot_comments if c.get("like_count", 0) > 10]
        if high_engagement:
            insights.append(f"该视频有 {len(high_engagement)} 条高互动评论")
        
        # 提取评论中可能的关键术语（长词/专业词汇）
        key_terms = set()
        for c in hot_comments[:10]:  # 只看前10条
            text = c.get("text", "")
            # 简单提取：取英文中长度>=5的词（可能是术语）
            import re
            words = re.findall(r'\b[a-zA-Z]{5,}\b', text)
            for w in words:
                if w.lower() not in {"there", "their", "about", "which", "would",
                                      "could", "should", "really", "thing",
                                      "things", "people", "because"}:
                    key_terms.add(w)
        
        if key_terms:
            terms_list = list(key_terms)[:10]
            insights.append(f"评论中提取到关键术语: {', '.join(terms_list)}")
        
        return insights


# ─── 注册 ────────────────────────────────────────────────

from ..core.config import PlatformRegistry
PlatformRegistry.register(YouTubeExtractor)
