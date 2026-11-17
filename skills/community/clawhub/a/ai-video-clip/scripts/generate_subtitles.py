#!/usr/bin/env python3
"""Generate Subtitles — 生成 SRT 字幕文件。

支持:
  - Whisper 转录 + SRT 输出
  - 词级时间戳 -> 动态字幕（两词一组 UPPERCASE 模式）
  - 自定义字幕分割规则

使用:
  python3 generate_subtitles.py --input video.mp4 --output subs.srt
  python3 generate_subtitles.py --input video.mp4 --output subs.srt --mode word_chunk
  python3 generate_subtitles.py --input video.mp4 --output subs.srt --style netflix
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import timedelta


def transcribe_whisper(video_path: str, language: str = None,
                        model: str = "medium") -> list:
    """使用 Whisper 转录并返回词级时间戳。"""
    try:
        import whisper
    except ImportError:
        print("错误: openai-whisper 未安装", file=sys.stderr)
        sys.exit(1)

    model_instance = whisper.load_model(model)
    result = model_instance.transcribe(
        video_path,
        word_timestamps=True,
        language=language,
        verbose=False,
    )

    words_data = []
    for segment in result.get("segments", []):
        for w in segment.get("words", []):
            words_data.append({
                "word": w["word"].strip(),
                "start": w["start"],
                "end": w["end"],
                "confidence": w.get("confidence", 0),
            })

    return words_data


def srt_timestamp(seconds: float) -> str:
    """秒数转 SRT 时间戳格式。"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def words_to_srt_standard(words: list, max_chars: int = 25,
                           max_gap: float = 0.5) -> str:
    """将词级时间戳转为标准 SRT 字幕（按句子/短语分组）。"""
    entries = []
    current_words = []
    current_start = None

    for w in words:
        if current_start is None:
            current_start = w["start"]

        current_words.append(w)

        # 检查是否需要断句
        text = " ".join(w["word"] for w in current_words)
        is_end_punct = w["word"].strip().endswith((".", "。", "!", "！", "?", "？", ",", "，"))

        next_gap = 999
        idx = words.index(w) if w in words else -1
        if idx >= 0 and idx + 1 < len(words):
            next_gap = words[idx + 1]["start"] - w["end"]

        should_split = (
            len(text) >= max_chars or
            (is_end_punct and len(text) >= 8) or
            next_gap > max_gap
        )

        if should_split and current_words:
            entries.append({
                "start": current_start,
                "end": w["end"],
                "text": text,
            })
            current_words = []
            current_start = None

    if current_words:
        entries.append({
            "start": current_start,
            "end": current_words[-1]["end"],
            "text": " ".join(w["word"] for w in current_words),
        })

    return entries_to_srt(entries)


def words_to_srt_word_chunk(words: list, chunk_size: int = 2) -> str:
    """词级分块模式：每 chunk_size 个词一组，生成快节奏字幕。"""
    entries = []
    for i in range(0, len(words), chunk_size):
        chunk = words[i : i + chunk_size]
        entries.append({
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "text": " ".join(w["word"].upper() for w in chunk),
        })

    return entries_to_srt(entries)


def words_to_srt_sentence(words: list) -> str:
    """基于标点和自然停顿的智能断句。"""
    entries = []
    buffer = []
    start = None

    for w in words:
        if start is None:
            start = w["start"]

        buffer.append(w)

        # 断句条件
        word_text = w["word"].strip()
        is_end = word_text.endswith((".", "。", "!", "！", "?", "？"))
        has_comma = word_text.endswith((",", "，", ";", "；"))

        combined = " ".join(b["word"] for b in buffer)

        should_flush = False
        if is_end:
            should_flush = True
        elif has_comma and len(combined) > 15:
            should_flush = True
        elif len(combined) > 40:
            should_flush = True

        if should_flush:
            entries.append({
                "start": start,
                "end": w["end"],
                "text": combined,
            })
            buffer = []
            start = None

    if buffer:
        entries.append({
            "start": start,
            "end": buffer[-1]["end"],
            "text": " ".join(b["word"] for b in buffer),
        })

    return entries_to_srt(entries)


def entries_to_srt(entries: list) -> str:
    """将条目列表转为 SRT 格式字符串。"""
    lines = []
    for i, entry in enumerate(entries, 1):
        lines.append(str(i))
        lines.append(
            f"{srt_timestamp(entry['start'])} --> {srt_timestamp(entry['end'])}"
        )
        lines.append(entry["text"])
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="生成 SRT 字幕文件")
    p.add_argument("--input", required=True, help="输入视频/音频文件")
    p.add_argument("--output", default="subtitles.srt", help="输出 SRT 文件")
    p.add_argument("--mode", default="sentence",
                   choices=["sentence", "standard", "word_chunk"],
                   help="字幕分割模式")
    p.add_argument("--language", help="语言代码 (zh/en/auto)")
    p.add_argument("--model", default="medium",
                   help="Whisper 模型大小")
    p.add_argument("--chunk-size", type=int, default=2,
                   help="word_chunk 模式的组词数")
    p.add_argument("--style", default="default",
                   choices=["default", "netflix", "douyin", "bilibili", "youtube", "minimal"],
                   help="字幕风格（用于后续烧录参考）")
    p.add_argument("--provider", default="whisper",
                   choices=["whisper", "funclip"],
                   help="ASR 提供商")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"转录: {os.path.basename(args.input)}")
    print(f"模式: {args.mode}, 模型: {args.model}")

    # 转录
    words_data = transcribe_whisper(args.input, args.language, args.model)
    print(f"识别 {len(words_data)} 个词")

    # 生成字幕
    if args.mode == "word_chunk":
        srt_text = words_to_srt_word_chunk(words_data, args.chunk_size)
    elif args.mode == "sentence":
        srt_text = words_to_srt_sentence(words_data)
    else:
        srt_text = words_to_srt_standard(words_data)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(srt_text)

    entries = srt_text.strip().split("\n\n")
    print(f"\n生成 {len(entries)} 条字幕 -> {args.output}")
    print(f"风格: {args.style} (用于后续烧录)")
    print(f"下一步: python3 burn_subtitles.py --input video.mp4 --srt {args.output} --output subtitled.mp4")
