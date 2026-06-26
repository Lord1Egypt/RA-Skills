#!/usr/bin/env python3
"""
sync_srt_tts.py - 同步 SRT 字幕时间轴与 TTS 配音时长

用法:
    python sync_srt_tts.py --srt subtitles.srt --audio voice.mp3 --output synced.srt

功能:
    - 分析音频实际时长
    - 调整 SRT 时间戳对齐
    - 处理段落间停顿
"""

import argparse
import re
import subprocess
from pathlib import Path


def parse_srt_timestamp(ts: str) -> float:
    """将 SRT 时间戳转换为秒"""
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", ts)
    if not match:
        raise ValueError(f"Invalid timestamp: {ts}")
    h, m, s, ms = map(int, match.groups())
    return h * 3600 + m * 60 + s + ms / 1000


def format_srt_timestamp(seconds: float) -> str:
    """将秒转换为 SRT 时间戳格式"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(content: str) -> list:
    """解析 SRT 文件内容"""
    blocks = re.split(r"\n\n+", content.strip())
    entries = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # 第一行是序号
        index = int(lines[0])

        # 第二行是时间轴
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1],
        )
        if not time_match:
            continue

        start = parse_srt_timestamp(time_match.group(1))
        end = parse_srt_timestamp(time_match.group(2))

        # 剩余行是字幕文本
        text = "\n".join(lines[2:])

        entries.append({"index": index, "start": start, "end": end, "text": text})

    return entries


def get_audio_duration(audio_path: str) -> float:
    """使用 ffprobe 获取音频时长"""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return float(result.stdout.strip())


def sync_srt_to_audio(entries: list, audio_duration: float, gap: float = 0.3) -> list:
    """
    同步 SRT 时间轴到音频时长

    Args:
        entries: SRT 条目列表
        audio_duration: 音频总时长（秒）
        gap: 字幕条目之间的停顿时间（秒）

    Returns:
        调整后的 SRT 条目列表
    """
    if not entries:
        return entries

    # 计算原始字幕总时长
    original_duration = sum(e["end"] - e["start"] for e in entries)
    total_gaps = gap * (len(entries) - 1) if len(entries) > 1 else 0

    # 计算缩放比例
    available_duration = audio_duration - total_gaps
    scale = available_duration / original_duration if original_duration > 0 else 1

    # 调整时间轴
    current_time = 0
    synced_entries = []

    for entry in entries:
        duration = (entry["end"] - entry["start"]) * scale
        synced_entries.append(
            {
                "index": entry["index"],
                "start": current_time,
                "end": current_time + duration,
                "text": entry["text"],
            }
        )
        current_time += duration + gap

    # 移除最后一个条目后的多余间隙
    if synced_entries:
        synced_entries[-1]["end"] = min(synced_entries[-1]["end"], audio_duration)

    return synced_entries


def generate_srt(entries: list) -> str:
    """生成 SRT 文件内容"""
    lines = []
    for entry in entries:
        lines.append(str(entry["index"]))
        lines.append(
            f"{format_srt_timestamp(entry['start'])} --> {format_srt_timestamp(entry['end'])}"
        )
        lines.append(entry["text"])
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="同步 SRT 字幕与 TTS 配音")
    parser.add_argument("--srt", required=True, help="输入 SRT 字幕文件")
    parser.add_argument("--audio", required=True, help="TTS 音频文件")
    parser.add_argument("--output", required=True, help="输出 SRT 文件")
    parser.add_argument(
        "--gap", type=float, default=0.3, help="字幕条目之间的停顿时间（秒）"
    )
    args = parser.parse_args()

    # 读取 SRT 文件
    srt_path = Path(args.srt)
    if not srt_path.exists():
        raise FileNotFoundError(f"SRT file not found: {args.srt}")

    content = srt_path.read_text(encoding="utf-8")
    entries = parse_srt(content)

    # 获取音频时长
    audio_duration = get_audio_duration(args.audio)
    print(f"Audio duration: {audio_duration:.2f}s")
    print(f"Subtitle entries: {len(entries)}")

    # 同步时间轴
    synced_entries = sync_srt_to_audio(entries, audio_duration, args.gap)

    # 生成输出
    output_content = generate_srt(synced_entries)
    Path(args.output).write_text(output_content, encoding="utf-8")

    print(f"Synced SRT saved to: {args.output}")


if __name__ == "__main__":
    main()
