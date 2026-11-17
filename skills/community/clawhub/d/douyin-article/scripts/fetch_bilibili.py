#!/usr/bin/env python3
"""B 站视频音频获取模块（v2.0 新增，v4.1 升级）。

基于 yt-dlp（B 站下载金标准）：
- 一行命令下载，无需浏览器自动化
- 支持分 P 下载（--playlist-items）
- 自动提取标题/作者/时长元数据
- 比抖音的 agent-browser + curl 流程轻量得多

v4.1 升级（三层字幕探测）：
- 字幕优先策略三层回退：
  1. B站公共 API 直连探测字幕（api.bilibili.com，无需登录，最快）
  2. yt-dlp --list-subs 探测 + 下载字幕（更广覆盖，支持 412 回退）
  3. 音频下载 + Whisper 转录（最终 fallback）

设计依据：
- B站公共 API 字幕直连（api.bilibili.com，无需登录）
- yt-dlp 是社区公认的 B 站下载最优解
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _cert_flags() -> list[str]:
    """v4.1.1: TLS 证书校验控制。

    默认启用证书校验（安全）。仅当用户明确设置 SKIP_CERT_CHECK=1 时禁用，
    用于应对偶发的 B 站证书过期问题。禁用为用户显式选择，非默认行为。
    """
    if os.environ.get("SKIP_CERT_CHECK") == "1":
        return ["--no-check-certificates"]
    return []

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import (
    find_command, md5_file, run_cmd, write_json, probe_media_duration,
    extract_bvid, extract_p, detect_language,
)
from fetch_subtitles import fetch_subtitle as _ytdlp_fetch_subtitle
from bilibili_subtitle_api import (
    get_video_metadata as _bili_get_meta,
    fetch_bilibili_subtitle_via_api as _bili_fetch_subtitle_api,
)


def _probe_bilibili_metadata(url: str) -> dict:
    """v4.0: 用 yt-dlp --dump-json 拿元数据（不下载）。"""
    cmd = [
        find_command("yt-dlp"),
        "--dump-json",
        "--no-warnings",
        *_cert_flags(),
        url,
    ]
    ok, out = run_cmd(cmd, timeout=60)
    if not ok or not out.strip():
        return {}
    try:
        data = json.loads(out.strip().splitlines()[0])
        return {
            "title": data.get("title", ""),
            "uploader": data.get("uploader") or data.get("channel") or "",
            "duration_sec": data.get("duration", 0),
        }
    except Exception:
        return {}


def fetch_one_bilibili(
    idx: int,
    item: dict,
    audio_dir: Path,
    raw_dir: Path,
    seen_md5: set[str],
    transcript_dir: Path | None = None,  # v4.0: 字幕优先
) -> dict:
    """下载单个 B 站视频并提取 16kHz 单声道 MP3。

    v4.1: 三层字幕优先策略：
      Layer 1: B站公共 API 直连探测字幕（无需登录，最快）
      Layer 2: yt-dlp --list-subs 探测 + 下载字幕（412 回退后备用）
      Layer 3: 音频下载 + Whisper 转录（最终 fallback）

    流程：
      v4.1: 公共 API 探测字幕 → 成功则跳过音频
      → v4.0: yt-dlp 字幕拉取 → 成功则跳过音频
      → fallback: yt-dlp 下载音频 → ffmpeg 提取 MP3 → MD5 去重 → 返回 metadata
    """
    url = item["url"]
    bvid = extract_bvid(url) or ""
    p = extract_p(url)
    print(f"\n[{idx}] B站处理: BV={bvid} p={p}", flush=True)
    print(f"     URL: {url}", flush=True)

    # v4.1: 字幕优先策略 - Layer 1: B站公共 API 直连
    if transcript_dir is not None:
        print(f"     v4.1: Layer 1 - B站公共 API 字幕探测...", flush=True)
        api_result = _bili_fetch_subtitle_api(
            bvid=bvid,
            p=p,
            video_id=str(idx),
            transcript_dir=transcript_dir,
        )
        if api_result and api_result["success"]:
            return {
                "idx": idx,
                "success": True,
                "title": api_result["title"],
                "author": api_result["author"],
                "source_url": url,
                "platform": "bilibili",
                "bvid": bvid,
                "p": p,
                "audio_path": "",
                "duration_sec": float(api_result["duration_sec"]),
                "skip_transcribe": True,
                "transcript_path": str(api_result["transcript_path"]),
                "transcript_source": f"bilibili-{api_result['subtitle_kind']}",
                "source_type": "subtitle",
                "source_language": api_result["language"],
                "needs_translation": api_result["language"] != "zh" and api_result["language"] != "unknown",
            }
        print(f"     v4.1: Layer 1 无字幕，尝试 Layer 2...", flush=True)

        # v4.0: Layer 2 - yt-dlp 字幕拉取（更广覆盖，作为 fallback）
        print(f"     v4.0: Layer 2 - yt-dlp 字幕探测...", flush=True)
        probe = _probe_bilibili_metadata(url)
        title = probe.get("title") or f"B站视频_{bvid}_p{p}"
        uploader = probe.get("uploader") or "未知"
        duration_sec = probe.get("duration_sec", 0)

        subs_dir = transcript_dir.parent / "subs"
        sub_result = _ytdlp_fetch_subtitle(
            url=url,
            output_dir=subs_dir,
            video_id=str(idx),
            title=title,
            author=uploader,
            source_url=url,
            platform="bilibili",
        )
        if sub_result["success"]:
            return {
                "idx": idx,
                "success": True,
                "title": sub_result["title"],
                "author": sub_result["author"],
                "source_url": url,
                "platform": "bilibili",
                "bvid": bvid,
                "p": p,
                "audio_path": "",
                "duration_sec": float(sub_result["duration_sec"]),
                "skip_transcribe": True,
                "transcript_path": str(sub_result["transcript_path"]),
                "transcript_source": "bilibili-cc",
                "source_type": "subtitle",
                "source_language": sub_result["language"],
                "needs_translation": sub_result["language"] != "zh" and sub_result["language"] != "unknown",
            }
        print(f"     v4.0: Layer 2 无字幕，fallback 到音频下载", flush=True)

    # yt-dlp 下载（仅音频流，最高质量）
    raw_path = raw_dir / f"raw_{idx}.m4a"
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    # yt-dlp 参数：
    # -f bestaudio：选最佳音频流
    # --extract-audio：直接提取音频（不保留视频）
    # --audio-format mp3：转 MP3
    # --audio-quality 5：VBR ~130kbps（够用）
    # --no-playlist：避免误下载整个合集（除非显式 --playlist-items）
    # --playlist-items N：指定分 P
    # --write-info-json：保存元数据（标题/作者/时长）
    # --no-warnings：减少日志噪声
    info_path = raw_dir / f"info_{idx}.json"
    mp3_path_direct = audio_dir / f"audio_{idx}.mp3"

    cmd = [
        find_command("yt-dlp"),
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "--no-playlist",
        "--playlist-items", str(p),
        "--write-info-json",
        "-o", str(raw_dir / f"raw_{idx}.%(ext)s"),
        "--no-warnings",
        *_cert_flags(),
        url,
    ]
    print(f"     yt-dlp 下载中...", flush=True)
    ok, out = run_cmd(cmd, timeout=300)
    if not ok:
        return {"idx": idx, "success": False, "error": f"yt-dlp 下载失败: {out[:200]}"}

    # 查找 yt-dlp 输出的实际文件
    # yt-dlp 会把 raw_{idx}.m4a 转成 raw_{idx}.mp3
    actual_mp3 = raw_dir / f"raw_{idx}.mp3"
    if not actual_mp3.is_file():
        # 尝试查找任何 raw_{idx}.* 文件
        candidates = list(raw_dir.glob(f"raw_{idx}.*"))
        if not candidates:
            return {"idx": idx, "success": False, "error": "yt-dlp 未生成输出文件"}
        actual_mp3 = candidates[0]

    # 查找 info json
    info_candidates = list(raw_dir.glob(f"raw_{idx}.info.json"))
    if not info_candidates:
        info_candidates = list(raw_dir.glob(f"info_{idx}.json"))
    info_data = {}
    if info_candidates:
        try:
            info_data = json.loads(info_candidates[0].read_text(encoding="utf-8"))
        except Exception:
            pass

    # 提取元数据
    title = info_data.get("title") or f"B站视频_{bvid}_p{p}"
    uploader = info_data.get("uploader") or info_data.get("channel") or "未知"
    duration_sec = info_data.get("duration") or probe_media_duration(actual_mp3)

    # 转换为 16kHz 单声道 MP3（Whisper 推荐格式）
    if not mp3_path_direct.is_file():
        ffmpeg_cmd = [
            find_command("ffmpeg"),
            "-y",
            "-i", str(actual_mp3),
            "-ar", "16000",
            "-ac", "1",
            "-c:a", "libmp3lame",
            "-q:a", "5",
            str(mp3_path_direct),
        ]
        ok2, _ = run_cmd(ffmpeg_cmd, timeout=120)
        if not ok2 or not mp3_path_direct.is_file():
            return {"idx": idx, "success": False, "error": "ffmpeg 转换 16kHz MP3 失败"}

    # MD5 去重
    file_md5 = md5_file(mp3_path_direct)
    if file_md5 in seen_md5:
        return {"idx": idx, "success": False, "error": "MD5 重复，疑似下载到相同文件"}
    seen_md5.add(file_md5)

    size_kb = mp3_path_direct.stat().st_size // 1024
    print(f"     ✅ 完成: {mp3_path_direct.name} ({size_kb} KB, {duration_sec:.1f}s)", flush=True)
    print(f"     标题: {title}", flush=True)
    print(f"     UP主: {uploader}", flush=True)

    return {
        "idx": idx,
        "success": True,
        "title": title,
        "author": uploader,
        "source_url": url,
        "platform": "bilibili",
        "bvid": bvid,
        "p": p,
        "audio_path": str(mp3_path_direct),
        "duration_sec": float(duration_sec),
        "md5": file_md5,
        "skip_transcribe": False,
        "source_type": "whisper",        # v4.0
        "source_language": "unknown",    # v4.0: Whisper 转录后检测
        "needs_translation": False,       # v4.0: 转录后由 03_pack 重新判断
    }
