#!/usr/bin/env python3
"""v4.0 新增：yt-dlp 字幕拉取（全平台支持）。

用 yt-dlp --skip-download --write-subs 拉取平台字幕，不下载视频/音频。
支持 YouTube/B站/Vimeo/TikTok 等所有 yt-dlp 支持的平台。

优先级：
  1. 手动字幕（--write-subs）
  2. 自动字幕（--write-auto-subs）
  3. 失败 → 返回 None，调用方 fallback 到 Whisper

字幕语言优先级：zh-Hans > zh > zh-CN > en > best

用法：
  CLI:
    python fetch_subtitles.py --url "https://..." --output-dir work/subs/ \\
      --video-id 1 --title "..." --author "..."

  函数调用（被 fetch_youtube.py / fetch_bilibili.py 导入）:
    from fetch_subtitles import fetch_subtitle
    result = fetch_subtitle(url, output_dir, video_id, title, author, source_url)
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import find_command, run_cmd, write_json, read_json
from srt_to_transcript import srt_to_transcript


# 字幕语言优先级（越高越优先）
SUBTITLE_LANG_PRIORITY = [
    "zh-Hans", "zh-CN", "zh", "zh-Hant",
    "en", "en-US", "en-GB",
    "ja", "ko",
]

# yt-dlp 字幕拉取参数
YTDLP_SUBTITLE_ARGS = [
    "--skip-download",           # 不下载视频/音频
    "--write-subs",               # 拉取手动字幕
    "--write-auto-subs",          # 拉取自动字幕
    "--sub-format", "srt/best",   # 优先 SRT
    "--convert-subs", "srt",      # 转换为 SRT
    "--skip-thumbnail",           # 不拉缩略图
    "--no-write-info-json",       # 不写 info.json（单独用 --dump-json）
]

# YouTube 特定参数：跳过翻译字幕
YOUTUBE_EXTRACTOR_ARGS = ["--extractor-args", "youtube:skip=translated_subs"]


def probe_subtitle_list(url: str) -> dict:
    """用 yt-dlp --list-subs 探测可用字幕。

    Returns:
        {"subtitles": {...}, "automatic_captions": {...}, "title": str, "duration": float}
        失败返回空 dict
    """
    ytdlp = find_command("yt-dlp")
    cmd = [
        ytdlp, "--list-subs", "--print-json", "--no-download", url
    ]
    success, output = run_cmd(cmd, timeout=60)
    if not success:
        return {}

    # 提取 JSON（yt-dlp 输出可能有噪声）
    try:
        # --print-json 输出在 stdout，--list-subs 输出在 stderr
        # 找到 JSON 行
        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("{") and '"subtitles"' in line:
                data = json.loads(line)
                return {
                    "subtitles": data.get("subtitles", {}),
                    "automatic_captions": data.get("automatic_captions", {}),
                    "title": data.get("title", ""),
                    "duration": data.get("duration", 0),
                    "uploader": data.get("uploader", data.get("channel", "")),
                }
    except (json.JSONDecodeError, KeyError):
        pass
    return {}


def pick_best_subtitle_lang(
    available: dict, preferred_langs: list[str] | None = None
) -> str | None:
    """从可用字幕中选出最佳语言。

    Args:
        available: {lang: [format_list]} 字典
        preferred_langs: 优先语言列表，None 用默认

    Returns:
        最佳语言代码，无可用返回 None
    """
    if not available:
        return None

    langs = preferred_langs or SUBTITLE_LANG_PRIORITY
    for lang in langs:
        if lang in available:
            return lang

    # fallback: 选第一个可用的
    for lang in available:
        # 跳过 live_chat 和 danmaku
        if lang in ("live_chat", "danmaku"):
            continue
        return lang

    return None


def fetch_subtitle(
    url: str,
    output_dir: Path,
    video_id: str,
    title: str = "",
    author: str = "",
    source_url: str = "",
    target_language: str = "zh-CN",
    platform: str = "",
) -> dict:
    """拉取平台字幕并转换为 transcript 格式。

    Args:
        url: 视频 URL
        output_dir: 输出目录
        video_id: 视频编号（用于文件命名）
        title: 视频标题（空则从 yt-dlp 获取）
        author: 作者（空则从 yt-dlp 获取）
        source_url: 原始链接
        target_language: 目标语言（用于判断是否需要翻译）
        platform: 平台标识（youtube/bilibili/ytdlp-generic）

    Returns:
        {
            "success": bool,
            "transcript_path": Path | None,
            "srt_path": Path | None,
            "language": str,         # 源语言
            "title": str,
            "author": str,
            "duration_sec": float,
            "source_type": str,      # "subtitle"
            "subtitle_kind": str,    # "manual" / "auto" / ""
        }
    """
    result = {
        "success": False,
        "transcript_path": None,
        "srt_path": None,
        "language": "unknown",
        "title": title,
        "author": author,
        "duration_sec": 0.0,
        "source_type": "subtitle",
        "subtitle_kind": "",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    ytdlp = find_command("yt-dlp")

    # 1. 探测可用字幕
    probe = probe_subtitle_list(url)
    if not probe:
        print(f"   ⚠️ 字幕探测失败，将 fallback 到 Whisper", flush=True)
        return result

    manual_subs = probe.get("subtitles", {})
    auto_subs = probe.get("automatic_captions", {})

    # 2. 选最佳字幕
    sub_lang = pick_best_subtitle_lang(manual_subs)
    subtitle_kind = "manual"
    if not sub_lang:
        sub_lang = pick_best_subtitle_lang(auto_subs)
        subtitle_kind = "auto"
    if not sub_lang:
        print(f"   ⚠️ 无可用字幕（手动+自动均无），将 fallback 到 Whisper", flush=True)
        return result

    print(
        f"   📝 找到字幕: lang={sub_lang}, kind={subtitle_kind}",
        flush=True,
    )

    # 3. 补充元数据
    if not title:
        title = probe.get("title", "") or f"video_{video_id}"
    if not author:
        author = probe.get("uploader", "") or "未知作者"
    duration = float(probe.get("duration", 0) or 0)
    result["title"] = title
    result["author"] = author
    result["duration_sec"] = duration

    # 4. 拉取字幕
    output_template = str(output_dir / f"subtitle_{video_id}")
    cmd = [
        ytdlp,
        *YTDLP_SUBTITLE_ARGS,
        "--sub-langs", sub_lang,
        "-o", output_template,
    ]
    if platform == "youtube" or "youtube.com" in url or "youtu.be" in url:
        cmd.extend(YOUTUBE_EXTRACTOR_ARGS)
    cmd.append(url)

    success, output = run_cmd(cmd, timeout=120)
    if not success:
        print(f"   ⚠️ 字幕下载失败，将 fallback 到 Whisper", flush=True)
        return result

    # 5. 查找下载的 SRT 文件
    srt_files = list(output_dir.glob(f"subtitle_{video_id}*.srt"))
    if not srt_files:
        # 尝试其他扩展名（.vtt 等）
        srt_files = list(output_dir.glob(f"subtitle_{video_id}*.vtt"))
        if srt_files:
            # 转换 VTT 为 SRT（简单处理）
            for vtt_path in srt_files:
                srt_path = vtt_path.with_suffix(".srt")
                convert_vtt_to_srt(vtt_path, srt_path)
                srt_files = [srt_path]
                break

    if not srt_files:
        print(f"   ⚠️ 字幕文件未找到，将 fallback 到 Whisper", flush=True)
        return result

    srt_path = srt_files[0]
    result["srt_path"] = srt_path
    result["subtitle_kind"] = subtitle_kind

    # 6. 转换为 transcript
    model_name = f"{platform}-{subtitle_kind}" if platform else f"subtitle-{subtitle_kind}"
    try:
        transcript = srt_to_transcript(
            srt_path=srt_path,
            title=title,
            author=author,
            source_url=source_url or url,
            source_type="subtitle",
            model=model_name,
            duration_sec=duration,
            video_id=video_id,
        )
        result["language"] = transcript["language"]
    except Exception as e:
        print(f"   ⚠️ SRT→transcript 转换失败: {e}", flush=True)
        return result

    # 7. 写入 transcript_N.json
    transcript_path = output_dir.parent / "transcript" / f"transcript_{video_id}.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(transcript_path, transcript)
    result["transcript_path"] = transcript_path
    result["success"] = True

    print(
        f"   ✅ 字幕转录完成: {transcript_path.name} "
        f"({len(transcript['segments'])} segments, lang={transcript['language']})",
        flush=True,
    )

    return result


def convert_vtt_to_srt(vtt_path: Path, srt_path: Path) -> None:
    """简单 VTT → SRT 转换。"""
    content = vtt_path.read_text(encoding="utf-8")
    # 去掉 WEBVTT 头
    content = re.sub(r"^WEBVTT.*?\n", "", content, flags=re.DOTALL)
    # 时间码 . → ,
    content = re.sub(
        r"(\d{2}:\d{2}:\d{2})\.(\d{3})", r"\1,\2", content
    )
    # 去掉行号（VRT 可能没有）
    lines = content.split("\n")
    output = []
    counter = 1
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "-->" in line:
            output.append(str(counter))
            output.append(line)
            counter += 1
            i += 1
            while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                output.append(lines[i].strip())
                i += 1
            output.append("")
        else:
            i += 1
    srt_path.write_text("\n".join(output), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="v4.0: yt-dlp 字幕拉取（全平台）"
    )
    parser.add_argument("--url", required=True, help="视频 URL")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--video-id", required=True, help="视频编号")
    parser.add_argument("--title", default="", help="视频标题")
    parser.add_argument("--author", default="", help="作者")
    parser.add_argument("--source-url", default="", help="原始链接")
    parser.add_argument("--platform", default="", help="平台标识")
    args = parser.parse_args()

    result = fetch_subtitle(
        url=args.url,
        output_dir=Path(args.output_dir),
        video_id=args.video_id,
        title=args.title,
        author=args.author,
        source_url=args.source_url,
        platform=args.platform,
    )

    if result["success"]:
        print(f"\n✅ 字幕拉取成功")
        print(f"   transcript: {result['transcript_path']}")
        print(f"   srt: {result['srt_path']}")
        print(f"   language: {result['language']}")
        print(f"   source_type: {result['source_type']}")
    else:
        print(f"\n❌ 字幕拉取失败，需要 fallback 到 Whisper", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
