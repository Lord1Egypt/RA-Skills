#!/usr/bin/env python3
"""YouTube 视频获取模块（v3.0 新增）。

双保险策略：
1. 优先用 youtube-transcript-api 直接拿字幕（几秒完成，与 youtube-watcher 一致）
   - 字幕拿到则直接生成 transcript_N.json，跳过 Whisper 转录
   - metadata 标记 skip_transcribe=True
2. 字幕不可用时 fallback 到 yt-dlp 下载音频 + Whisper 转录
   - metadata 标记 skip_transcribe=False

网络代理：
- 自动读取 HTTP_PROXY / HTTPS_PROXY 环境变量
- 用户配置一次代理后所有 YouTube 请求自动走代理

参考：
- youtube-transcript-api: https://pypi.org/project/youtube-transcript-api/
- youtube-watcher skill (53,969 下载量，同类最稳)
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


def _cert_flags() -> list[str]:
    """v4.1.1: TLS 证书校验控制。

    默认启用证书校验（安全）。仅当用户明确设置 SKIP_CERT_CHECK=1 时禁用。
    """
    if os.environ.get("SKIP_CERT_CHECK") == "1":
        return ["--no-check-certificates"]
    return []

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import (
    find_command, md5_file, run_cmd, write_json, probe_media_duration,
    extract_youtube_id, format_timestamp, detect_language,
)
from fetch_subtitles import fetch_subtitle as _ytdlp_fetch_subtitle


def _get_proxies() -> Optional[dict]:
    """读取环境变量中的代理配置。"""
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    proxies = {}
    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy
    return proxies if proxies else None


def _fetch_transcript_api(video_id: str) -> Optional[list[dict]]:
    """用 youtube-transcript-api 拿字幕。

    返回 [{start, end, text}, ...] 或 None（无字幕）
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print(f"     ⚠️ youtube-transcript-api 未安装，将 fallback 到 yt-dlp", file=sys.stderr)
        return None

    proxies = _get_proxies()
    # 新版 API（>=1.0）：用 fetch
    try:
        ytt_api = YouTubeTranscriptApi()
        if proxies:
            # youtube-transcript-api 通过 cookies/proxies 参数支持
            try:
                # 新版接受 proxies 参数
                transcript = ytt_api.fetch(video_id, languages=["zh-Hans", "zh", "zh-CN", "en", "en-US"])
            except Exception:
                # 旧版 API
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=["zh-Hans", "zh", "zh-CN", "en", "en-US"],
                    proxies=proxies,
                )
                # 旧版返回 [{'text': ..., 'start': ..., 'duration': ...}]
                return [
                    {
                        "start": float(s["start"]),
                        "end": float(s["start"]) + float(s.get("duration", 0)),
                        "text": s["text"].strip(),
                    }
                    for s in transcript_list if s.get("text", "").strip()
                ]
        else:
            transcript = ytt_api.fetch(video_id, languages=["zh-Hans", "zh", "zh-CN", "en", "en-US"])
    except Exception as e:
        # 尝试不指定语言（自动生成字幕）
        try:
            print(f"     字幕精确语言未命中，尝试自动生成字幕...", flush=True)
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)
        except Exception as e2:
            print(f"     ⚠️ youtube-transcript-api 拿字幕失败: {e2}", file=sys.stderr)
            return None

    # 新版 API：FetchedTranscriptSnippet 对象
    segments = []
    for snippet in transcript:
        text = (snippet.text or "").strip()
        if text:
            segments.append({
                "start": float(snippet.start),
                "end": float(snippet.start) + float(getattr(snippet, "duration", 0) or 0),
                "text": text,
            })
    return segments if segments else None


def _fetch_video_metadata(video_id: str) -> dict:
    """用 yt-dlp 拿元数据（不下载视频）。

    yt-dlp --dump-json 输出元数据 JSON，比 HTML 抓取更稳。
    """
    cmd = [
        find_command("yt-dlp"),
        "--dump-json",
        "--no-warnings",
        *_cert_flags(),
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    ok, out = run_cmd(cmd, timeout=60)
    if not ok or not out.strip():
        return {}
    try:
        data = json.loads(out.strip().splitlines()[0])
        return {
            "title": data.get("title"),
            "author": data.get("uploader") or data.get("channel") or "未知",
            "duration_sec": data.get("duration"),
            "description": (data.get("description") or "")[:500],
        }
    except Exception:
        return {}


def _save_transcript_as_json(
    segments: list[dict],
    metadata: dict,
    video_id: str,
    url: str,
    transcript_dir: Path,
    idx: int,
) -> Path:
    """把字幕 segments 保存为 transcript_N.json（与阶段 2 输出格式一致）。"""
    transcript_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcript_dir / f"transcript_{idx}.json"

    transcript_obj = {
        "video_id": str(idx),
        "title": metadata.get("title") or f"YouTube_{video_id}",
        "author": metadata.get("author", "未知"),
        "source_url": url,
        "duration_sec": metadata.get("duration_sec", 0),
        "model": "youtube-transcript-api",  # 标记来源
        "language": detect_language(" ".join(s.get("text", "") for s in segments[:10])),
        "source_type": "subtitle",  # v4.0: 标记字幕来源
        "segments": segments,
    }
    write_json(out_path, transcript_obj)
    return out_path


def _download_audio_ytdlp(
    video_id: str,
    url: str,
    idx: int,
    audio_dir: Path,
    raw_dir: Path,
) -> tuple[Optional[Path], Optional[float]]:
    """用 yt-dlp 下载音频并转为 16kHz 单声道 MP3。返回 (mp3_path, duration_sec) 或 (None, None)。"""
    raw_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        find_command("yt-dlp"),
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "--no-playlist",
        "--write-info-json",
        "-o", str(raw_dir / f"raw_{idx}.%(ext)s"),
        "--no-warnings",
        *_cert_flags(),
        url,
    ]
    print(f"     yt-dlp 下载音频...", flush=True)
    ok, _ = run_cmd(cmd, timeout=600)
    if not ok:
        return None, None

    # 查找 yt-dlp 输出的文件
    actual_mp3 = raw_dir / f"raw_{idx}.mp3"
    if not actual_mp3.is_file():
        candidates = list(raw_dir.glob(f"raw_{idx}.*"))
        if not candidates:
            return None, None
        actual_mp3 = candidates[0]

    # 转 16kHz 单声道 MP3
    mp3_path = audio_dir / f"audio_{idx}.mp3"
    ffmpeg_cmd = [
        find_command("ffmpeg"),
        "-y",
        "-i", str(actual_mp3),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "libmp3lame",
        "-q:a", "5",
        str(mp3_path),
    ]
    ok2, _ = run_cmd(ffmpeg_cmd, timeout=180)
    if not ok2 or not mp3_path.is_file():
        return None, None

    duration = probe_media_duration(mp3_path)
    return mp3_path, duration


def fetch_one_youtube(
    idx: int,
    item: dict,
    audio_dir: Path,
    raw_dir: Path,
    transcript_dir: Path,
    seen_md5: set[str],
) -> dict:
    """获取单个 YouTube 视频的内容。

    策略：字幕API优先（快），无字幕时 yt-dlp 下载音频（走 Whisper）。
    """
    url = item["url"]
    vid = extract_youtube_id(url) or ""
    print(f"\n[{idx}] YouTube 处理: video_id={vid}", flush=True)
    print(f"     URL: {url}", flush=True)

    # 1. 拿元数据（用 yt-dlp --dump-json，更稳）
    print(f"     抓取视频元数据...", flush=True)
    meta = _fetch_video_metadata(vid)
    title = meta.get("title") or f"YouTube_{vid}"
    author = meta.get("author", "未知")
    duration_sec = meta.get("duration_sec", 0)
    print(f"     标题: {title}", flush=True)
    print(f"     作者: {author}", flush=True)
    if duration_sec:
        print(f"     时长: {format_timestamp(duration_sec)}", flush=True)

    # 2. 尝试字幕 API（优先）
    print(f"     尝试 youtube-transcript-api 拿字幕...", flush=True)
    segments = _fetch_transcript_api(vid)
    if segments:
        print(f"     ✅ 字幕拿到: {len(segments)} 个片段", flush=True)
        # 保存为 transcript_N.json
        out_path = _save_transcript_as_json(segments, meta, vid, url, transcript_dir, idx)
        word_count = sum(len(s["text"]) for s in segments)
        print(f"     字幕已保存: {out_path.name} ({word_count} 字)", flush=True)
        # v4.0: 检测语言，标记 source_type
        source_lang = detect_language(" ".join(s.get("text", "") for s in segments[:10]))
        return {
            "idx": idx,
            "success": True,
            "title": title,
            "author": author,
            "source_url": url,
            "platform": "youtube",
            "video_id": vid,
            "audio_path": "",  # 无音频（字幕路径）
            "duration_sec": float(duration_sec),
            "skip_transcribe": True,  # 阶段 2 跳过 Whisper
            "transcript_path": str(out_path),
            "transcript_source": "youtube-transcript-api",
            "source_type": "subtitle",         # v4.0
            "source_language": source_lang,     # v4.0
            "needs_translation": source_lang != "zh" and source_lang != "unknown",  # v4.0
        }

    # 2.5 v4.0: youtube-transcript-api 失败 → 尝试 yt-dlp 字幕拉取
    print(f"     youtube-transcript-api 失败，尝试 yt-dlp 字幕拉取...", flush=True)
    subs_dir = transcript_dir.parent / "subs"
    sub_result = _ytdlp_fetch_subtitle(
        url=url,
        output_dir=subs_dir,
        video_id=str(idx),
        title=title,
        author=author,
        source_url=url,
        platform="youtube",
    )
    if sub_result["success"]:
        return {
            "idx": idx,
            "success": True,
            "title": sub_result["title"],
            "author": sub_result["author"],
            "source_url": url,
            "platform": "youtube",
            "video_id": vid,
            "audio_path": "",
            "duration_sec": float(sub_result["duration_sec"]),
            "skip_transcribe": True,
            "transcript_path": str(sub_result["transcript_path"]),
            "transcript_source": "ytdlp-subtitle",
            "source_type": "subtitle",                                     # v4.0
            "source_language": sub_result["language"],                      # v4.0
            "needs_translation": sub_result["language"] != "zh" and sub_result["language"] != "unknown",  # v4.0
        }

    # 3. 字幕不可用 → fallback 到 yt-dlp 下载音频
    print(f"     字幕不可用，fallback 到 yt-dlp 下载音频...", flush=True)
    mp3_path, audio_duration = _download_audio_ytdlp(vid, url, idx, audio_dir, raw_dir)
    if not mp3_path:
        return {"idx": idx, "success": False, "error": "字幕获取失败且 yt-dlp 下载也失败（检查网络/代理配置）"}

    # 用音频时长兜底（如果元数据没有时长）
    if not duration_sec and audio_duration:
        duration_sec = audio_duration

    # MD5 去重
    file_md5 = md5_file(mp3_path)
    if file_md5 in seen_md5:
        return {"idx": idx, "success": False, "error": "MD5 重复，疑似下载到相同文件"}
    seen_md5.add(file_md5)

    size_kb = mp3_path.stat().st_size // 1024
    print(f"     ✅ 音频下载完成: {mp3_path.name} ({size_kb} KB, {duration_sec:.1f}s)", flush=True)

    return {
        "idx": idx,
        "success": True,
        "title": title,
        "author": author,
        "source_url": url,
        "platform": "youtube",
        "video_id": vid,
        "audio_path": str(mp3_path),
        "duration_sec": float(duration_sec),
        "skip_transcribe": False,  # 阶段 2 走 Whisper
        "md5": file_md5,
        "source_type": "whisper",        # v4.0
        "source_language": "unknown",    # v4.0: Whisper 转录后由 02_transcribe 检测
        "needs_translation": False,       # v4.0: 转录后由 03_pack 重新判断
    }
