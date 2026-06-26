#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse


PREFERRED_AUDIO_CODEC = "m4a"
DEFAULT_MODEL_SIZE = "base"
DEFAULT_BEAM_SIZE = 3
DEFAULT_LANGUAGE = "zh"
SUPPORTED_HOSTS = ("bilibili.com", "www.bilibili.com", "m.bilibili.com", "b23.tv", "www.b23.tv")
ROUGH_CPU_WALL_SECONDS_PER_AUDIO_SECOND = {
    "tiny": 0.25,
    "base": 0.45,
    "small": 1.10,
    "medium": 2.20,
    "large-v2": 4.50,
    "large-v3": 4.80,
}
BEAM_SIZE_MULTIPLIER = {
    1: 0.70,
    2: 0.85,
    3: 1.00,
    4: 1.45,
    5: 2.20,
}


def check_ffmpeg() -> None:
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path is None or ffprobe_path is None:
        raise EnvironmentError(
            "未找到 ffmpeg 或 ffprobe。\n"
            "请先安装 ffmpeg，并确保 ffmpeg / ffprobe 所在目录已加入 PATH。"
        )


def validate_bilibili_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("链接必须以 http:// 或 https:// 开头。")
    host = (parsed.netloc or "").lower()
    if not any(host == item or host.endswith("." + item) for item in SUPPORTED_HOSTS):
        raise ValueError("该脚本只支持 bilibili.com 或 b23.tv 链接。")


def format_duration(seconds: Optional[float]) -> str:
    if seconds is None or math.isinf(seconds) or math.isnan(seconds):
        return "unknown"
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:d}h {minutes:02d}m {secs:02d}s"
    return f"{minutes:02d}m {secs:02d}s"


def format_srt_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000
    minutes = milliseconds // 60_000
    milliseconds %= 60_000
    secs = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def sanitize_stem(name: str) -> str:
    bad = '<>:"/\\|?*'
    table = str.maketrans({char: "_" for char in bad})
    return name.translate(table).strip().rstrip(".")


def probe_duration(audio_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def rough_eta_seconds(duration_seconds: float, model_size: str, device: str, beam_size: int) -> Optional[float]:
    if device != "cpu":
        return None
    factor = ROUGH_CPU_WALL_SECONDS_PER_AUDIO_SECOND.get(model_size)
    if factor is None:
        return None
    beam_multiplier = BEAM_SIZE_MULTIPLIER.get(beam_size)
    if beam_multiplier is None:
        if beam_size <= 3:
            beam_multiplier = max(0.55, 1.0 - 0.15 * (3 - beam_size))
        else:
            beam_multiplier = 1.0 + 0.60 * (beam_size - 3)
    return duration_seconds * factor * beam_multiplier


def find_latest_candidate(out_dir: Path, stem: str) -> Path:
    candidates = sorted(out_dir.glob(f"{stem}.*"), key=lambda path: path.stat().st_mtime, reverse=True)
    media_candidates = [
        path
        for path in candidates
        if path.suffix.lower() in {".m4a", ".mp3", ".opus", ".webm", ".wav", ".aac", ".mp4"}
    ]
    if media_candidates:
        return media_candidates[0]
    if candidates:
        return candidates[0]
    raise FileNotFoundError("下载完成，但未找到音频文件。")


def download_bilibili_audio(url: str, out_dir: str) -> Tuple[Path, Dict[str, Any]]:
    try:
        from yt_dlp import YoutubeDL
    except ModuleNotFoundError:
        print(
            "缺少 Python 依赖：yt-dlp。请先安装 requirements.txt，或运行 scripts/bootstrap_env.sh。",
            file=sys.stderr,
        )
        raise

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    ydl_opts: Dict[str, Any] = {
        "outtmpl": str(out_path / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "quiet": False,
        "no_warnings": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": PREFERRED_AUDIO_CODEC,
                "preferredquality": "0",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        prepared = Path(ydl.prepare_filename(info))

    title = info.get("title") or "audio"
    video_id = info.get("id") or "unknown"
    stem = sanitize_stem(f"{title} [{video_id}]")
    expected_audio = out_path / f"{stem}.{PREFERRED_AUDIO_CODEC}"
    if expected_audio.exists():
        return expected_audio, info

    prepared_audio = prepared.with_suffix(f".{PREFERRED_AUDIO_CODEC}")
    if prepared_audio.exists():
        return prepared_audio, info

    return find_latest_candidate(out_path, stem), info


def transcribe_audio(
    audio_path: Path,
    model_size: str,
    device: str,
    beam_size: int,
    vad_filter: bool,
    log_progress: bool,
    report_interval_seconds: float,
    language: Optional[str],
) -> Tuple[str, List[Dict[str, Any]], Any, float]:
    try:
        from faster_whisper import WhisperModel
    except ModuleNotFoundError:
        print(
            "缺少 Python 依赖：faster-whisper。请先安装 requirements.txt，或运行 scripts/bootstrap_env.sh。",
            file=sys.stderr,
        )
        raise

    compute_type = "int8" if device == "cpu" else "float16"
    total_duration = probe_duration(audio_path)

    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print(f"音频时长: {format_duration(total_duration)}")
    rough_eta = rough_eta_seconds(total_duration, model_size, device, beam_size)
    if rough_eta is not None:
        print(
            f"初始粗估耗时: {format_duration(rough_eta)} "
            f"（{device}/{model_size}/beam={beam_size}，粗估；实际会随着进度动态修正）"
        )
    else:
        print(f"初始粗估耗时: unknown（{device}/{model_size}/beam={beam_size}，运行中再看 ETA）")

    transcribe_kwargs: Dict[str, Any] = {
        "beam_size": beam_size,
        "vad_filter": vad_filter,
        "log_progress": log_progress,
    }
    if language and language != "auto":
        transcribe_kwargs["language"] = language

    segments, info = model.transcribe(str(audio_path), **transcribe_kwargs)

    full_text_parts: List[str] = []
    segments_list: List[Dict[str, Any]] = []
    start_time = time.time()
    last_report_time = start_time
    last_report_progress = -1.0

    for index, segment in enumerate(segments, start=1):
        text = segment.text.strip()
        if text:
            full_text_parts.append(text)
        segments_list.append(
            {
                "index": index,
                "start": segment.start,
                "end": segment.end,
                "text": text,
            }
        )

        now = time.time()
        processed_seconds = max(segment.end, 0.0)
        progress = min(processed_seconds / total_duration, 1.0) if total_duration > 0 else 0.0
        elapsed = now - start_time
        speed = processed_seconds / elapsed if elapsed > 0 and processed_seconds > 0 else None
        eta_seconds = None
        if speed and speed > 0 and total_duration > processed_seconds:
            eta_seconds = (total_duration - processed_seconds) / speed

        should_report = (
            index == 1
            or now - last_report_time >= report_interval_seconds
            or progress - last_report_progress >= 0.05
            or progress >= 0.999
        )
        if should_report:
            speed_str = f"{speed:.2f}x realtime" if speed else "warming up"
            print(
                "[ASR] "
                f"{progress * 100:5.1f}% | "
                f"已处理 {format_duration(processed_seconds)} / {format_duration(total_duration)} | "
                f"已耗时 {format_duration(elapsed)} | "
                f"速度 {speed_str} | "
                f"ETA {format_duration(eta_seconds)}"
            )
            last_report_time = now
            last_report_progress = progress

    total_elapsed = time.time() - start_time
    full_text = "\n".join(item for item in full_text_parts if item)
    return full_text, segments_list, info, total_elapsed


def save_text(text: str, txt_path: Path) -> None:
    txt_path.write_text(text + "\n", encoding="utf-8")


def save_srt(segments_list: List[Dict[str, Any]], srt_path: Path) -> None:
    lines: List[str] = []
    for segment in segments_list:
        text = segment["text"].strip()
        if not text:
            continue
        lines.append(str(segment["index"]))
        lines.append(f"{format_srt_timestamp(segment['start'])} --> {format_srt_timestamp(segment['end'])}")
        lines.append(text)
        lines.append("")
    srt_path.write_text("\n".join(lines), encoding="utf-8")


def save_segments_json(
    segments_list: List[Dict[str, Any]],
    info: Any,
    audio_path: Path,
    elapsed_seconds: float,
    json_path: Path,
) -> None:
    payload = {
        "audio_path": str(audio_path),
        "language": getattr(info, "language", None),
        "language_probability": getattr(info, "language_probability", None),
        "elapsed_seconds": elapsed_seconds,
        "segments": segments_list,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="下载 B 站音频并转写为 txt/srt/json")
    parser.add_argument("url", nargs="?", help="B 站视频链接")
    parser.add_argument("--out-dir", "--output-dir", default="downloads/bilibili-audio", help="输出目录")
    parser.add_argument(
        "--model-size",
        "--model",
        default=DEFAULT_MODEL_SIZE,
        help="Whisper 模型大小，例如 tiny/base/small/medium/large-v3",
    )
    parser.add_argument("--device", default="cpu", help="cpu / cuda")
    parser.add_argument("--beam-size", type=int, default=DEFAULT_BEAM_SIZE, help="beam size，默认 3")
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        help="语言代码，默认 zh；传 auto 可启用自动识别",
    )
    parser.add_argument("--report-interval", type=float, default=15.0, help="进度打印间隔（秒）")
    parser.add_argument("--no-vad", action="store_true", help="关闭 vad_filter")
    parser.add_argument("--no-log-progress", action="store_true", help="关闭 faster-whisper 内部 log_progress")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    check_ffmpeg()

    url = (args.url or input("请输入 B 站视频链接: ").strip()).strip()
    if not url:
        raise ValueError("链接不能为空。")
    validate_bilibili_url(url)

    print("\n[1/3] 开始下载音频...")
    audio_path, info = download_bilibili_audio(url=url, out_dir=args.out_dir)
    print(f"音频已下载: {audio_path}")
    if info.get("title"):
        print(f"标题: {info['title']}")
    if info.get("duration"):
        print(f"站点元数据时长: {format_duration(float(info['duration']))}")

    print("\n[2/3] 开始语音转文字...")
    print(
        f"参数: model={args.model_size}, device={args.device}, beam_size={args.beam_size}, "
        f"language={args.language}, vad_filter={not args.no_vad}, log_progress={not args.no_log_progress}"
    )
    full_text, segments_list, asr_info, elapsed_seconds = transcribe_audio(
        audio_path=audio_path,
        model_size=args.model_size,
        device=args.device,
        beam_size=args.beam_size,
        vad_filter=not args.no_vad,
        log_progress=not args.no_log_progress,
        report_interval_seconds=args.report_interval,
        language=args.language,
    )

    print("\n[3/3] 保存结果...")
    txt_path = audio_path.with_suffix(".txt")
    srt_path = audio_path.with_suffix(".srt")
    json_path = audio_path.with_suffix(".segments.json")

    save_text(full_text, txt_path)
    save_srt(segments_list, srt_path)
    save_segments_json(segments_list, asr_info, audio_path, elapsed_seconds, json_path)

    print(f"语言识别结果: {asr_info.language} (概率: {asr_info.language_probability:.4f})")
    print(f"共输出分段: {len(segments_list)}")
    print(f"转写耗时: {format_duration(elapsed_seconds)}")
    print(f"文本已保存: {txt_path}")
    print(f"SRT 已保存: {srt_path}")
    print(f"分段 JSON 已保存: {json_path}")
    print("\n完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
