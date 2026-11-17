#!/usr/bin/env python3

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


EXIT_OK = 0
EXIT_ARGUMENT = 1
EXIT_AUDIO_EXTRACT = 2
EXIT_NO_HIGHLIGHT = 3

SUPPORTED_METHODS = {"audio", "scene", "hybrid", "combined", "asr"}
SUPPORTED_EXTENSIONS = {".mp4", ".webm", ".mov"}
DEFAULT_METHOD = "hybrid"
DEFAULT_THRESHOLD = 1.5
DEFAULT_SCENE_THRESHOLD = 0.1
DEFAULT_MIN_CLIP_DURATION = 5.0
DEFAULT_PADDING = 2.0
DEFAULT_OUTPUT_DIR = "./highlights"
DEFAULT_MERGE = True
MERGE_GAP_SECONDS = 3.0
FRAME_LENGTH = 2048
HOP_LENGTH = 512
ASR_WINDOW_SECONDS = 8.0
ASR_TOP_N = 8

KEYWORD_PATTERNS: Dict[str, List[str]] = {
    "price": [r"¥\s*\d+(?:\.\d+)?", r"只要", r"到手价", r"多少钱"],
    "action": [r"上链接", r"去拍", r"最后", r"限时", r"福利"],
    "interaction": [r"扣1", r"打公屏", r"想要的举手"],
}


@dataclass
class Segment:
    start: float
    end: float
    score: float = 0.0
    source: str = ""

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)


def log(prefix: str, message: str) -> None:
    print(f"{prefix}: {message}")


def fail(message: str, code: int) -> None:
    log("ERROR", message)
    sys.exit(code)


def parse_bool(value: str) -> bool:
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"布尔参数仅支持 true/false，收到: {value}")


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError(f"数值必须 >= 0，收到: {value}")
    return parsed


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError(f"整数必须 > 0，收到: {value}")
    return parsed


def import_analysis_dependencies():
    try:
        import librosa  # type: ignore
        import numpy as np  # type: ignore
    except ModuleNotFoundError as error:
        fail(
            f"缺少 Python 依赖: {error.name}。请先安装 pydub、librosa、numpy 后再执行。",
            EXIT_AUDIO_EXTRACT,
        )
    return librosa, np


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="从直播录屏中自动提取高光片段")
    parser.add_argument("--input", required=True, help="输入视频绝对路径")
    parser.add_argument("--method", default=DEFAULT_METHOD, help="audio / scene / hybrid / combined / asr")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="音频能量阈值倍数")
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=DEFAULT_SCENE_THRESHOLD,
        help="场景变化阈值，默认 0.1",
    )
    parser.add_argument(
        "--min-clip-duration",
        dest="min_clip_duration",
        type=positive_float,
        default=DEFAULT_MIN_CLIP_DURATION,
        help="最小片段时长（秒）",
    )
    parser.add_argument(
        "--padding",
        type=positive_float,
        default=DEFAULT_PADDING,
        help="前后扩展秒数",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument(
        "--merge",
        type=parse_bool,
        default=DEFAULT_MERGE,
        help="是否输出合并版视频，true/false",
    )
    parser.add_argument("--asr-file", help="ASR 转写结果文件路径，method=asr 时必填")
    parser.add_argument(
        "--asr-window",
        type=positive_float,
        default=ASR_WINDOW_SECONDS,
        help="ASR 关键词聚合窗口大小（秒）",
    )
    parser.add_argument(
        "--top-n",
        type=positive_int,
        default=ASR_TOP_N,
        help="ASR 法最多保留的 Top-N 候选窗口数",
    )
    return parser


def ensure_command_available(name: str) -> None:
    if shutil.which(name) is None:
        fail(f"未找到可执行命令: {name}", EXIT_AUDIO_EXTRACT)


def probe_duration(video_path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"ffprobe 获取时长失败: {result.stderr.strip() or result.stdout.strip()}", EXIT_AUDIO_EXTRACT)

    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise RuntimeError("无法解析 ffprobe 返回的视频时长") from exc


def validate_args(args: argparse.Namespace) -> Tuple[Path, str, Path, Optional[Path]]:
    input_path = Path(args.input).expanduser()
    if not input_path.is_absolute():
        fail("--input 必须为绝对路径", EXIT_ARGUMENT)
    if not input_path.exists() or not input_path.is_file():
        fail(f"输入视频不存在: {input_path}", EXIT_ARGUMENT)
    if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        fail("仅支持 .mp4 / .webm / .mov 输入文件", EXIT_ARGUMENT)

    method = str(args.method).strip().lower()
    if method not in SUPPORTED_METHODS:
        fail("--method 仅支持 audio / scene / hybrid / combined / asr", EXIT_ARGUMENT)
    if args.threshold < 0:
        fail("--threshold 必须 >= 0", EXIT_ARGUMENT)
    if args.scene_threshold < 0:
        fail("--scene-threshold 必须 >= 0", EXIT_ARGUMENT)

    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir

    asr_path: Optional[Path] = None
    if args.asr_file:
        asr_path = Path(args.asr_file).expanduser()
        if not asr_path.is_absolute():
            asr_path = Path.cwd() / asr_path
        if not asr_path.exists() or not asr_path.is_file():
            fail(f"ASR 文件不存在: {asr_path}", EXIT_ARGUMENT)

    if method == "asr" and asr_path is None:
        fail("--method asr 时必须提供 --asr-file", EXIT_ARGUMENT)

    return input_path, method, output_dir, asr_path


def extract_audio(video_path: Path, wav_path: Path) -> None:
    log("STEP", "提取视频音频为 WAV")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "22050",
        "-c:a",
        "pcm_s16le",
        str(wav_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"音频提取失败: {result.stderr.strip() or result.stdout.strip()}", EXIT_AUDIO_EXTRACT)
    log("OK", f"音频提取完成: {wav_path}")


def detect_audio_highlights(wav_path: Path, threshold_factor: float) -> Tuple[List[Segment], dict]:
    log("STEP", "分析音频 RMS 能量曲线")
    librosa, np = import_analysis_dependencies()
    samples, sample_rate = librosa.load(str(wav_path), sr=22050, mono=True)
    if samples.size == 0:
        fail("提取到的音频为空，无法分析", EXIT_AUDIO_EXTRACT)

    rms = librosa.feature.rms(y=samples, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sample_rate, hop_length=HOP_LENGTH)

    mean_energy = float(np.mean(rms))
    std_energy = float(np.std(rms))
    threshold = mean_energy + threshold_factor * std_energy
    active_indices = np.where(rms > threshold)[0]

    analysis = {
        "sample_rate": sample_rate,
        "frame_length": FRAME_LENGTH,
        "hop_length": HOP_LENGTH,
        "mean_energy": mean_energy,
        "std_energy": std_energy,
        "threshold": threshold,
        "active_window_count": int(active_indices.size),
    }

    if active_indices.size == 0:
        return [], analysis

    window_seconds = HOP_LENGTH / sample_rate
    segments: List[Segment] = []
    start_index = int(active_indices[0])
    previous_index = int(active_indices[0])

    for raw_index in active_indices[1:]:
        index = int(raw_index)
        gap_seconds = (index - previous_index) * window_seconds
        if gap_seconds > MERGE_GAP_SECONDS:
            segments.append(
                Segment(
                    start=float(times[start_index]),
                    end=float(times[previous_index] + window_seconds),
                    source="audio",
                )
            )
            start_index = index
        previous_index = index

    segments.append(
        Segment(
            start=float(times[start_index]),
            end=float(times[previous_index] + window_seconds),
            source="audio",
        )
    )
    log("OK", f"检测到 {len(segments)} 个音频候选高光段")
    return segments, analysis


def detect_scene_highlights(video_path: Path, scene_threshold: float, min_clip_duration: float) -> Tuple[List[Segment], dict]:
    log("STEP", f"执行场景变化检测，阈值: {scene_threshold}")
    filter_expr = f"select='gt(scene,{scene_threshold})',showinfo"
    command = ["ffmpeg", "-i", str(video_path), "-filter:v", filter_expr, "-f", "null", "-"]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0 and not result.stderr:
        fail("场景检测执行失败", EXIT_AUDIO_EXTRACT)

    stderr = result.stderr
    timestamp_matches = re.findall(r"pts_time:(\d+(?:\.\d+)?)", stderr)
    timestamps = sorted({float(item) for item in timestamp_matches})

    segments: List[Segment] = []
    for timestamp in timestamps:
        half_window = max(min_clip_duration / 2.0, 2.0)
        segments.append(
            Segment(
                start=max(0.0, timestamp - half_window),
                end=timestamp + half_window,
                source="scene",
            )
        )

    analysis = {
        "scene_threshold": scene_threshold,
        "scene_cut_count": len(timestamps),
        "timestamps": timestamps,
    }
    log("OK", f"检测到 {len(timestamps)} 个场景切换点")
    return merge_close_segments(segments, MERGE_GAP_SECONDS), analysis


def time_overlap(left: Segment, right: Segment) -> float:
    return max(0.0, min(left.end, right.end) - max(left.start, right.start))


def combine_hybrid_segments(audio_segments: Sequence[Segment], scene_segments: Sequence[Segment]) -> List[Segment]:
    hybrid_segments: List[Segment] = []
    for audio_segment in audio_segments:
        overlaps = [scene_segment for scene_segment in scene_segments if time_overlap(audio_segment, scene_segment) > 0]
        if overlaps:
            start = min([audio_segment.start] + [segment.start for segment in overlaps])
            end = max([audio_segment.end] + [segment.end for segment in overlaps])
            hybrid_segments.append(Segment(start=start, end=end, source="hybrid", score=len(overlaps) + 1.0))

    if hybrid_segments:
        log("OK", f"hybrid 方法得到 {len(hybrid_segments)} 个音画重叠候选段")
        return merge_close_segments(hybrid_segments, MERGE_GAP_SECONDS)

    log("WARN", "未找到音频高能与场景变化重叠区域，回退为音频候选段")
    return [Segment(start=item.start, end=item.end, source="hybrid-fallback") for item in audio_segments]


def combine_union_segments(audio_segments: Sequence[Segment], scene_segments: Sequence[Segment]) -> List[Segment]:
    union_segments: List[Segment] = []
    for segment in audio_segments:
        union_segments.append(
            Segment(start=segment.start, end=segment.end, score=segment.score, source=segment.source or "audio")
        )
    for segment in scene_segments:
        union_segments.append(
            Segment(start=segment.start, end=segment.end, score=segment.score, source=segment.source or "scene")
        )

    log("OK", f"combined 方法合并 audio({len(audio_segments)}) + scene({len(scene_segments)}) 候选段")
    return merge_close_segments(union_segments, MERGE_GAP_SECONDS)


def normalize_text_payload(raw: object) -> List[dict]:
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict):
        for key in ("segments", "items", "results", "utterances"):
            value = raw.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def load_asr_entries(asr_path: Path) -> List[dict]:
    raw_text = asr_path.read_text(encoding="utf-8")
    if asr_path.suffix.lower() == ".json":
        payload = json.loads(raw_text)
        entries = normalize_text_payload(payload)
    else:
        entries = []
        for line in raw_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                entries.append(item)
    if not entries:
        fail("ASR 文件中未解析到可用转写片段", EXIT_ARGUMENT)
    return entries


def extract_entry_time(entry: dict) -> Optional[Tuple[float, float, str]]:
    text = str(entry.get("text") or entry.get("sentence") or entry.get("content") or "").strip()
    if not text:
        return None

    start = entry.get("start")
    end = entry.get("end")
    if start is None:
        start = entry.get("start_time")
    if end is None:
        end = entry.get("end_time")

    try:
        if start is None:
            return None
        start_value = float(start)
        end_value = float(end) if end is not None else start_value + 2.0
    except (TypeError, ValueError):
        return None

    if end_value <= start_value:
        end_value = start_value + 2.0
    return start_value, end_value, text


def detect_asr_highlights(asr_path: Path, window_seconds: float, top_n: int) -> Tuple[List[Segment], dict]:
    log("STEP", f"分析 ASR 关键词密集区域: {asr_path}")
    entries = load_asr_entries(asr_path)
    windows: Dict[int, dict] = {}

    for entry in entries:
        parsed = extract_entry_time(entry)
        if parsed is None:
            continue
        start, end, text = parsed
        score = 0
        matched_labels: List[str] = []
        for label, patterns in KEYWORD_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                if matches:
                    score += len(matches)
                    matched_labels.append(label)
        if score <= 0:
            continue

        window_index = int(start // window_seconds)
        window = windows.setdefault(
            window_index,
            {
                "start": window_index * window_seconds,
                "end": (window_index + 1) * window_seconds,
                "score": 0,
                "match_count": 0,
                "labels": set(),
            },
        )
        window["score"] += score
        window["match_count"] += 1
        window["labels"].update(matched_labels)
        window["end"] = max(window["end"], end)

    ordered = sorted(windows.values(), key=lambda item: (item["score"], item["match_count"]), reverse=True)
    selected = ordered[:top_n]
    segments = [
        Segment(start=float(item["start"]), end=float(item["end"]), score=float(item["score"]), source="asr")
        for item in selected
    ]

    analysis = {
        "asr_file": str(asr_path),
        "window_seconds": window_seconds,
        "top_n": top_n,
        "candidate_window_count": len(windows),
        "selected_windows": [
            {
                "start": round(float(item["start"]), 3),
                "end": round(float(item["end"]), 3),
                "score": item["score"],
                "match_count": item["match_count"],
                "labels": sorted(item["labels"]),
            }
            for item in selected
        ],
    }
    log("OK", f"检测到 {len(segments)} 个 ASR 候选高光窗口")
    return merge_close_segments(segments, MERGE_GAP_SECONDS), analysis


def merge_close_segments(segments: Sequence[Segment], max_gap: float) -> List[Segment]:
    if not segments:
        return []

    ordered = sorted(segments, key=lambda item: item.start)
    merged: List[Segment] = [
        Segment(start=ordered[0].start, end=ordered[0].end, score=ordered[0].score, source=ordered[0].source)
    ]

    for current in ordered[1:]:
        last = merged[-1]
        if current.start - last.end < max_gap:
            last.end = max(last.end, current.end)
            last.score = max(last.score, current.score)
            if last.source != current.source and current.source:
                last.source = f"{last.source}+{current.source}".strip("+")
        else:
            merged.append(
                Segment(start=current.start, end=current.end, score=current.score, source=current.source)
            )
    return merged


def filter_and_pad_segments(
    segments: Sequence[Segment],
    min_duration: float,
    padding: float,
    video_duration: float,
) -> List[Segment]:
    prepared: List[Segment] = []
    for segment in segments:
        if segment.duration < min_duration:
            continue
        start = max(0.0, segment.start - padding)
        end = min(video_duration, segment.end + padding)
        if end - start >= min_duration:
            prepared.append(
                Segment(start=start, end=end, score=segment.score, source=segment.source)
            )
    return merge_close_segments(prepared, 0.1)


def seconds_to_token(value: float) -> str:
    millis = int(round(value * 1000))
    seconds = millis // 1000
    remainder = millis % 1000
    return f"{seconds:04d}_{remainder:03d}"


def run_ffmpeg(command: List[str], error_prefix: str) -> None:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"{error_prefix}: {result.stderr.strip() or result.stdout.strip()}", EXIT_AUDIO_EXTRACT)


def export_segments(video_path: Path, output_dir: Path, segments: Sequence[Segment]) -> List[Path]:
    clip_paths: List[Path] = []
    for index, segment in enumerate(segments, start=1):
        clip_name = (
            f"clip_{index:02d}_{seconds_to_token(segment.start)}_{seconds_to_token(segment.end)}.mp4"
        )
        clip_path = output_dir / clip_name
        log(
            "STEP",
            f"输出片段 {index}: {segment.start:.2f}s - {segment.end:.2f}s ({segment.source or 'unknown'})",
        )
        command = [
            "ffmpeg",
            "-y",
            "-ss",
            f"{segment.start:.3f}",
            "-i",
            str(video_path),
            "-t",
            f"{segment.duration:.3f}",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(clip_path),
        ]
        run_ffmpeg(command, f"输出片段失败 {clip_name}")
        clip_paths.append(clip_path)
        log("OK", f"片段已输出: {clip_path}")
    return clip_paths


def merge_segments(output_dir: Path, clip_paths: Sequence[Path]) -> Path:
    merged_path = output_dir / "merged_highlights.mp4"
    concat_path = output_dir / "concat_list.txt"
    concat_lines = []
    for clip_path in clip_paths:
        escaped_name = clip_path.name.replace("'", r"'\''")
        concat_lines.append(f"file '{escaped_name}'")
    concat_content = "\n".join(concat_lines)
    concat_path.write_text(concat_content + "\n", encoding="utf-8")

    log("STEP", "合并所有高光片段")
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-c",
        "copy",
        str(merged_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=output_dir)
    if result.returncode != 0:
        log("WARN", "无损 concat 合并失败，回退到重新编码合并")
        fallback = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(merged_path),
        ]
        run_ffmpeg(fallback, "合并高光片段失败")
    log("OK", f"合并版已输出: {merged_path}")
    return merged_path


def write_metadata(
    output_dir: Path,
    source_video: Path,
    method: str,
    threshold_factor: float,
    scene_threshold: float,
    min_clip_duration: float,
    padding: float,
    merge_output: bool,
    analysis: dict,
    segments: Sequence[Segment],
    clip_paths: Sequence[Path],
) -> None:
    payload = {
        "source_video": str(source_video),
        "method": method,
        "threshold_factor": threshold_factor,
        "scene_threshold": scene_threshold,
        "min_clip_duration": min_clip_duration,
        "padding": padding,
        "merge": merge_output,
        "analysis": analysis,
        "segments": [
            {
                "index": index,
                "start": round(segment.start, 3),
                "end": round(segment.end, 3),
                "duration": round(segment.duration, 3),
                "score": round(segment.score, 3),
                "source": segment.source,
                "file": str(path.name),
            }
            for index, (segment, path) in enumerate(zip(segments, clip_paths), start=1)
        ],
    }
    metadata_path = output_dir / "segments.json"
    metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log("OK", f"元数据已写入: {metadata_path}")


def analyze_candidates(
    method: str,
    input_path: Path,
    temp_dir: Path,
    threshold: float,
    scene_threshold: float,
    min_clip_duration: float,
    asr_path: Optional[Path],
    asr_window: float,
    top_n: int,
) -> Tuple[List[Segment], dict]:
    combined_analysis: dict = {"method": method}

    if method == "audio":
        wav_path = temp_dir / "audio.wav"
        extract_audio(input_path, wav_path)
        return detect_audio_highlights(wav_path, threshold)

    if method == "scene":
        return detect_scene_highlights(input_path, scene_threshold, min_clip_duration)

    if method == "hybrid":
        wav_path = temp_dir / "audio.wav"
        extract_audio(input_path, wav_path)
        audio_segments, audio_analysis = detect_audio_highlights(wav_path, threshold)
        scene_segments, scene_analysis = detect_scene_highlights(input_path, scene_threshold, min_clip_duration)
        hybrid_segments = combine_hybrid_segments(audio_segments, scene_segments)
        combined_analysis["audio"] = audio_analysis
        combined_analysis["scene"] = scene_analysis
        combined_analysis["hybrid_candidate_count"] = len(hybrid_segments)
        return hybrid_segments, combined_analysis

    if method == "combined":
        wav_path = temp_dir / "audio.wav"
        extract_audio(input_path, wav_path)
        audio_segments, audio_analysis = detect_audio_highlights(wav_path, threshold)
        scene_segments, scene_analysis = detect_scene_highlights(input_path, scene_threshold, min_clip_duration)
        union_segments = combine_union_segments(audio_segments, scene_segments)
        combined_analysis["audio"] = audio_analysis
        combined_analysis["scene"] = scene_analysis
        combined_analysis["combined_candidate_count"] = len(union_segments)
        return union_segments, combined_analysis

    if method == "asr":
        assert asr_path is not None
        return detect_asr_highlights(asr_path, asr_window, top_n)

    fail(f"不支持的分析方法: {method}", EXIT_ARGUMENT)
    return [], combined_analysis


def main() -> None:
    parser = build_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else EXIT_ARGUMENT
        raise SystemExit(code)

    input_path, method, output_dir, asr_path = validate_args(args)
    ensure_command_available("ffmpeg")
    ensure_command_available("ffprobe")

    output_dir.mkdir(parents=True, exist_ok=True)
    video_duration = probe_duration(input_path)

    with tempfile.TemporaryDirectory(prefix="highlight_slicer_") as temp_dir:
        candidate_segments, analysis = analyze_candidates(
            method=method,
            input_path=input_path,
            temp_dir=Path(temp_dir),
            threshold=args.threshold,
            scene_threshold=args.scene_threshold,
            min_clip_duration=args.min_clip_duration,
            asr_path=asr_path,
            asr_window=args.asr_window,
            top_n=args.top_n,
        )

    merged_segments = merge_close_segments(candidate_segments, MERGE_GAP_SECONDS)
    final_segments = filter_and_pad_segments(
        merged_segments,
        min_duration=args.min_clip_duration,
        padding=args.padding,
        video_duration=video_duration,
    )

    if not final_segments:
        fail("未检测到满足条件的高光片段", EXIT_NO_HIGHLIGHT)

    log("OK", f"最终保留 {len(final_segments)} 个高光片段")
    clip_paths = export_segments(input_path, output_dir, final_segments)
    write_metadata(
        output_dir=output_dir,
        source_video=input_path,
        method=method,
        threshold_factor=args.threshold,
        scene_threshold=args.scene_threshold,
        min_clip_duration=args.min_clip_duration,
        padding=args.padding,
        merge_output=args.merge,
        analysis=analysis,
        segments=final_segments,
        clip_paths=clip_paths,
    )

    if args.merge:
        merge_segments(output_dir, clip_paths)

    log("OK", f"处理完成，输出目录: {output_dir}")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    try:
        main()
    except argparse.ArgumentTypeError as error:
        fail(str(error), EXIT_ARGUMENT)
    except ValueError as error:
        fail(str(error), EXIT_ARGUMENT)
    except RuntimeError as error:
        fail(str(error), EXIT_AUDIO_EXTRACT)
