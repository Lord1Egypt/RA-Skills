#!/usr/bin/env python3
"""阶段 1：批量获取视频音频/字幕（全平台）。

v4.0：支持 yt-dlp 1700+ 平台，字幕优先策略。
v2.0 起：自动识别 URL 平台，分派到对应 adapter：
- 抖音：agent-browser + curl（保留 v1.0 实战补丁）
- B站：yt-dlp（v4.0 字幕优先）
- YouTube：youtube-transcript-api + yt-dlp 字幕 + yt-dlp 音频
- 小宇宙：专用 adapter
- v4.0 ytdlp-generic：Vimeo/TikTok/Twitch/Twitter 等通过 yt-dlp 字幕优先 + 音频 fallback

抖音实战补丁：
- agent-browser open（不 close 上一个，避免 close 挂起）
- 等待 40 秒让 blob URL 变成直接 CDN URL
- eval 直接参数模式 + network requests __vid 匹配 fallback
- CLIXML 噪声清理
- curl 下载 + MD5 去重
- ffmpeg 提取 16kHz 单声道 MP3
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import (
    find_command, md5_file, clean_clixml, run_cmd, get_agent_browser_path,
    JS_GET_VIDEO_URL, JS_GET_VIDEO_ID, extract_url_from_eval, extract_url_from_network,
    write_json, read_json, probe_media_duration,
    parse_input_urls_unified,  # v3.0: 四平台统一解析
)
from fetch_bilibili import fetch_one_bilibili  # v2.0: B站 adapter
from fetch_xiaoyuzhou import fetch_one_xiaoyuzhou  # v3.0: 小宇宙 adapter
from fetch_youtube import fetch_one_youtube  # v3.0: YouTube adapter


def open_url(ab_path: str, url: str) -> bool:
    """用 agent-browser open 打开 URL（不 close 上一个）。"""
    ok, _ = run_cmd([ab_path, "open", url], timeout=30)
    return ok


def get_current_vid(ab_path: str) -> Optional[str]:
    """获取当前页面的视频 ID（用于 __vid 匹配）。"""
    ok, out = run_cmd([ab_path, "eval", JS_GET_VIDEO_ID], timeout=10)
    if not ok:
        return None
    out = clean_clixml(out).strip().strip('"').strip("'")
    if out and out != "null":
        return out
    return None


def get_video_url(ab_path: str, vid: Optional[str] = None) -> Optional[str]:
    """双重通道提取 CDN URL：eval + network requests。"""
    # 通道 1: eval 直接参数模式
    ok, out = run_cmd([ab_path, "eval", JS_GET_VIDEO_URL], timeout=10)
    if ok:
        url = extract_url_from_eval(out)
        if url:
            return url

    # 等待 20 秒重试 eval
    time.sleep(20)
    ok, out = run_cmd([ab_path, "eval", JS_GET_VIDEO_URL], timeout=10)
    if ok:
        url = extract_url_from_eval(out)
        if url:
            return url

    # 通道 2: network requests __vid 匹配
    ok, out = run_cmd([ab_path, "network", "requests"], timeout=15)
    if not ok:
        return None
    return extract_url_from_network(out, vid)


def download_audio(url: str, output_path: Path) -> bool:
    """curl 下载音频流。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        find_command("curl"),
        "-L",
        "-H", "Referer: https://www.douyin.com/",
        "-H", "User-Agent: Mozilla/5.0",
        "-o", str(output_path),
        "-s",
        "--max-time", "120",
        url,
    ]
    ok, _ = run_cmd(cmd, timeout=180)
    if ok and output_path.is_file() and output_path.stat().st_size > 1024:
        return True
    return False


def extract_audio_mp3(input_path: Path, output_path: Path) -> bool:
    """用 ffmpeg 提取 16kHz 单声道 MP3。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        find_command("ffmpeg"),
        "-y",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "libmp3lame",
        "-q:a", "5",
        str(output_path),
    ]
    ok, _ = run_cmd(cmd, timeout=120)
    return ok and output_path.is_file() and output_path.stat().st_size > 1024


def process_one(
    idx: int,
    item: dict,
    ab_path: str,
    audio_dir: Path,
    raw_dir: Path,
    seen_md5: set[str],
) -> dict:
    """处理单个视频：open → 等待 → 提取URL → 下载 → 提取MP3。"""
    url = item["url"]
    title = item.get("title") or f"video_{idx}"
    print(f"\n[{idx}] 处理: {title}", flush=True)
    print(f"     URL: {url}", flush=True)

    # 打开页面（不 close 上一个）
    if not open_url(ab_path, url):
        return {"idx": idx, "success": False, "error": "open URL 失败"}

    # 等待 40 秒让 blob URL 变成直接 CDN URL
    print(f"     等待 40 秒让 blob URL 解析...", flush=True)
    time.sleep(40)

    # 获取视频 ID
    vid = get_current_vid(ab_path)
    print(f"     视频 ID: {vid}", flush=True)

    # 提取 CDN URL
    video_url = get_video_url(ab_path, vid)
    if not video_url:
        return {"idx": idx, "success": False, "error": "无法提取 CDN URL"}

    print(f"     CDN URL: {video_url[:80]}...", flush=True)

    # 下载原始流
    raw_path = raw_dir / f"raw_{idx}.mp4"
    if not download_audio(video_url, raw_path):
        return {"idx": idx, "success": False, "error": "下载失败"}

    # MD5 去重
    file_md5 = md5_file(raw_path)
    if file_md5 in seen_md5:
        print(f"     ⚠️ MD5 重复，重新提取...", flush=True)
        time.sleep(15)
        video_url = get_video_url(ab_path, vid)
        if video_url:
            if not download_audio(video_url, raw_path):
                return {"idx": idx, "success": False, "error": "重试下载仍失败"}
            file_md5 = md5_file(raw_path)
            if file_md5 in seen_md5:
                return {"idx": idx, "success": False, "error": "MD5 重复，疑似下载到相同文件"}
    seen_md5.add(file_md5)

    # 提取 16kHz 单声道 MP3
    mp3_path = audio_dir / f"audio_{idx}.mp3"
    if not extract_audio_mp3(raw_path, mp3_path):
        return {"idx": idx, "success": False, "error": "ffmpeg 提取 MP3 失败"}

    duration = probe_media_duration(mp3_path)
    size_kb = mp3_path.stat().st_size // 1024
    print(f"     ✅ 音频提取完成: {mp3_path.name} ({size_kb} KB, {duration:.1f}s)", flush=True)

    return {
        "idx": idx,
        "success": True,
        "title": title,
        "source_url": url,
        "audio_path": str(mp3_path),
        "duration_sec": duration,
        "md5": file_md5,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="阶段 1：批量获取视频音频（抖音/B站/小宇宙/YouTube）")
    parser.add_argument("input_file", type=Path, help="包含抖音/B站/小宇宙/YouTube 链接的文本文件（一行一个或分享文本）")
    parser.add_argument("--output-dir", type=Path, required=True, help="输出根目录")
    parser.add_argument("--ab-path", type=Path, help="agent-browser 路径（自动探测可不传，仅抖音需要）")
    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"❌ 输入文件不存在: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # v3.0: 统一解析四平台链接
    items = parse_input_urls_unified(args.input_file)
    if not items:
        print("❌ 未找到抖音/B站/小宇宙/YouTube 链接", file=sys.stderr)
        sys.exit(1)

    # 统计平台分布
    douyin_count = sum(1 for i in items if i["platform"] == "douyin")
    bili_count = sum(1 for i in items if i["platform"] == "bilibili")
    xyz_count = sum(1 for i in items if i["platform"] == "xiaoyuzhou")
    yt_count = sum(1 for i in items if i["platform"] == "youtube")
    generic_count = sum(1 for i in items if i["platform"] == "ytdlp-generic")  # v4.0
    parts = []
    if douyin_count: parts.append(f"抖音 {douyin_count}")
    if bili_count: parts.append(f"B站 {bili_count}")
    if xyz_count: parts.append(f"小宇宙 {xyz_count}")
    if yt_count: parts.append(f"YouTube {yt_count}")
    if generic_count: parts.append(f"通用平台 {generic_count}")  # v4.0
    print(f"📋 共 {len(items)} 个视频待处理（{' / '.join(parts)}）", flush=True)

    # 准备目录
    audio_dir = args.output_dir / "audio"
    raw_dir = args.output_dir / "raw"
    transcript_dir = args.output_dir / "transcript"  # YouTube 字幕路径直接写入
    audio_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    # 仅当有抖音链接时才需要 agent-browser
    ab_path = None
    if douyin_count > 0:
        ab_path = str(args.ab_path) if args.ab_path else get_agent_browser_path()
        print(f"🔧 agent-browser: {ab_path}", flush=True)

    # YouTube 代理提示
    if yt_count > 0:
        import os
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
        if proxy:
            print(f"🌐 YouTube 走代理: {proxy}", flush=True)
        else:
            print(f"⚠️ YouTube 未配置代理（HTTPS_PROXY/HTTP_PROXY 环境变量为空），可能无法访问", flush=True)

    # 批量处理（按平台分派）
    metadata = []
    seen_md5: set[str] = set()
    for item in items:
        platform = item["platform"]
        if platform == "bilibili":
            # v4.0: 启用字幕优先策略
            result = fetch_one_bilibili(
                item["line"], item, audio_dir, raw_dir, seen_md5,
                transcript_dir=transcript_dir,
            )
        elif platform == "xiaoyuzhou":
            result = fetch_one_xiaoyuzhou(item["line"], item, audio_dir, raw_dir, seen_md5)
        elif platform == "youtube":
            result = fetch_one_youtube(item["line"], item, audio_dir, raw_dir, transcript_dir, seen_md5)
        elif platform == "ytdlp-generic":
            # v4.0: yt-dlp 通用平台（Vimeo/TikTok/Twitter/Twitch 等）
            # 复用 B站 adapter（同为 yt-dlp + 字幕优先 + 音频 fallback）
            print(f"\n[{item['line']}] 通用平台处理: {item['url']}", flush=True)
            result = fetch_one_bilibili(
                item["line"], item, audio_dir, raw_dir, seen_md5,
                transcript_dir=transcript_dir,
            )
            # 修正 platform 字段（B站 adapter 返回 platform="bilibili"）
            if result.get("success"):
                result["platform"] = "ytdlp-generic"
        else:  # douyin
            if not ab_path:
                result = {"idx": item["line"], "success": False, "error": "抖音链接需要 agent-browser，未配置"}
            else:
                result = process_one(item["line"], item, ab_path, audio_dir, raw_dir, seen_md5)
        metadata.append(result)

    # 写入 metadata.json
    meta_path = args.output_dir / "metadata.json"
    write_json(meta_path, {
        "total": len(metadata),
        "success": sum(1 for m in metadata if m.get("success")),
        "failed": sum(1 for m in metadata if not m.get("success")),
        "items": metadata,
    })
    print(f"\n📊 完成: {sum(1 for m in metadata if m.get('success'))}/{len(metadata)} 成功", flush=True)
    print(f"📁 metadata: {meta_path}", flush=True)


if __name__ == "__main__":
    main()
