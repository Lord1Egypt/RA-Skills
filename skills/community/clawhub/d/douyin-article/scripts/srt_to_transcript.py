#!/usr/bin/env python3
"""v4.0 新增：SRT 字幕 → transcript_N.json 转换器。

把平台字幕（YouTube/B站等）的 SRT 文件转换为与 Whisper 输出同构的 transcript 格式，
让下游 pack/build 零改动复用。

输入：SRT 文件路径 + 元数据
输出：transcript_N.json（与 02_transcribe.py 输出同构）

用法：
  CLI:
    python srt_to_transcript.py \
      --srt path/to/subtitle.srt \
      --output transcript/transcript_1.json \
      --title "视频标题" \
      --author "作者" \
      --source-url "https://..." \
      --source-type subtitle \
      --model youtube-auto

  函数调用（被 fetch_subtitles.py 导入）:
    from srt_to_transcript import srt_to_transcript
    transcript = srt_to_transcript(srt_path, title, author, source_url, ...)
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import parse_srt, detect_language, write_json, probe_media_duration


def srt_to_transcript(
    srt_path: Path,
    title: str = "未知标题",
    author: str = "未知作者",
    source_url: str = "",
    source_type: str = "subtitle",
    model: str = "platform-subtitle",
    duration_sec: float | None = None,
    video_id: str | None = None,
) -> dict:
    """把 SRT 文件转换为 transcript 格式。

    Args:
        srt_path: SRT 文件路径
        title: 视频标题
        author: 作者
        source_url: 原始链接
        source_type: "subtitle"（平台字幕）或 "whisper"（Whisper 转录）
        model: 字幕来源标识（如 "youtube-auto", "bilibili-cc", "whisper-small"）
        duration_sec: 视频时长（秒）。None 时用最后一个 segment 的 end。
        video_id: 视频编号（用于 03_pack 索引）。None 时从 srt_path 文件名提取。

    Returns:
        与 02_transcribe.py 输出同构的 transcript dict:
        {
            "video_id": str,
            "segments": [{"start", "end", "text"}, ...],
            "language": str,
            "model": str,
            "source_type": str,
            "title": str,
            "author": str,
            "source_url": str,
            "duration_sec": float,
        }
    """
    # 1. 读取并解析 SRT
    srt_content = srt_path.read_text(encoding="utf-8")
    segments = parse_srt(srt_content)

    if not segments:
        raise ValueError(f"SRT 文件无有效 segments: {srt_path}")

    # 2. 检测语言（采样前 10 个 segment）
    sample_text = " ".join(seg["text"] for seg in segments[:10])
    language = detect_language(sample_text)

    # 3. 推断时长
    if duration_sec is None or duration_sec <= 0:
        duration_sec = segments[-1]["end"]

    # 4. 提取 video_id（从文件名，如 subtitle_1.srt → 1）
    if video_id is None:
        stem = srt_path.stem  # 如 "subtitle_1"
        # 提取末尾的数字
        import re
        m = re.search(r"(\d+)$", stem)
        video_id = m.group(1) if m else "1"

    return {
        "video_id": video_id,
        "segments": segments,
        "language": language,
        "model": model,
        "source_type": source_type,
        "title": title,
        "author": author,
        "source_url": source_url,
        "duration_sec": round(duration_sec, 3),
    }


def main():
    parser = argparse.ArgumentParser(
        description="v4.0: SRT 字幕 → transcript_N.json 转换"
    )
    parser.add_argument("--srt", required=True, help="SRT 文件路径")
    parser.add_argument("--output", required=True, help="输出 transcript_N.json 路径")
    parser.add_argument("--title", default="未知标题", help="视频标题")
    parser.add_argument("--author", default="未知作者", help="作者")
    parser.add_argument("--source-url", default="", help="原始链接")
    parser.add_argument(
        "--source-type",
        default="subtitle",
        choices=["subtitle", "whisper"],
        help="字幕来源类型",
    )
    parser.add_argument("--model", default="platform-subtitle", help="来源标识")
    parser.add_argument("--video", default=None, help="视频文件路径（用于探测时长）")
    parser.add_argument("--video-id", default=None, help="视频编号（用于 03_pack 索引，默认从文件名提取）")
    args = parser.parse_args()

    srt_path = Path(args.srt)
    output_path = Path(args.output)

    if not srt_path.exists():
        print(f"❌ SRT 文件不存在: {srt_path}", file=sys.stderr)
        sys.exit(1)

    # 探测视频时长（如果提供了视频文件）
    duration_sec = None
    if args.video:
        video_path = Path(args.video)
        if video_path.exists():
            duration_sec = probe_media_duration(video_path)

    # 转换
    transcript = srt_to_transcript(
        srt_path=srt_path,
        title=args.title,
        author=args.author,
        source_url=args.source_url,
        source_type=args.source_type,
        model=args.model,
        duration_sec=duration_sec,
        video_id=args.video_id,
    )

    # 写入
    write_json(output_path, transcript)
    print(
        f"✅ 转换完成: {output_path.name} "
        f"({len(transcript['segments'])} segments, language={transcript['language']}, "
        f"source_type={transcript['source_type']})",
        flush=True,
    )


if __name__ == "__main__":
    main()
