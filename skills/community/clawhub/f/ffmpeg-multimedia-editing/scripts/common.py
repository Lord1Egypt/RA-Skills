# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "outputs" / "ffmpeg"

VIDEO_EXTS = {".mp4", ".webm", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".ts", ".m4v", ".3gp"}
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma", ".opus", ".ape"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}
SUBTITLE_EXTS = {".srt", ".ass", ".ssa", ".vtt"}

FORMAT_TO_EXT = {
    "mp4": ".mp4", "webm": ".webm", "avi": ".avi", "mkv": ".mkv",
    "mov": ".mov", "flv": ".flv", "gif": ".gif",
    "mp3": ".mp3", "wav": ".wav", "flac": ".flac", "ogg": ".ogg",
    "aac": ".aac", "m4a": ".m4a", "opus": ".opus",
    "png": ".png", "jpg": ".jpg",
}

RESOLUTION_MAP = {
    "2160p": 2160, "1080p": 1080, "720p": 720, "480p": 480,
    "360p": 360, "240p": 240,
}

XFADER_TRANSITIONS = [
    "fade", "fadeblack", "fadewhite", "dissolve",
    "slideleft", "slideright", "slideup", "slidedown",
    "circlecrop", "circleopen", "radial",
    "smoothleft", "smoothright", "smoothup", "smoothdown",
    "distance", "wipetl", "wipetr", "wipebl", "wipebr",
    "squeezeH", "squeezeV", "zoomin",
]

logger = logging.getLogger("ffmpeg")


def log_params(event: str, **kwargs: Any) -> None:
    """Log an event with a provider prefix and JSON payload."""
    params_str = json.dumps(kwargs, ensure_ascii=False, default=str)
    logger.info("FFmpeg - %s | %s", event, params_str)


_trace_id: str = ""


def get_trace_id() -> str:
    global _trace_id
    if not _trace_id:
        _trace_id = uuid4().hex
    return _trace_id


class _TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


LOG_DIR = OUTPUT_ROOT / "outputs" / "logs"


def _ensure_logging() -> None:
    """Lazy init logging on first use."""
    if logger.handlers:
        return
    trace_filter = _TraceIdFilter()
    log_fmt = "%(asctime)s [%(trace_id)s] %(levelname)s %(message)s"
    fmt = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(trace_filter)
    logger.addHandler(file_handler)
    error_handler = logging.FileHandler(LOG_DIR / f"{today}.error.log", encoding="utf-8")
    error_handler.setFormatter(fmt)
    error_handler.addFilter(trace_filter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class FFProbeInfo:
    path: str
    format_name: str
    duration: float
    size: int
    bitrate: int
    video_streams: list[dict[str, Any]] = field(default_factory=list)
    audio_streams: list[dict[str, Any]] = field(default_factory=list)
    subtitle_streams: list[dict[str, Any]] = field(default_factory=list)

    @property
    def has_video(self) -> bool:
        return len(self.video_streams) > 0

    @property
    def has_audio(self) -> bool:
        return len(self.audio_streams) > 0

    @property
    def width(self) -> int | None:
        if self.video_streams:
            return self.video_streams[0].get("width")
        return None

    @property
    def height(self) -> int | None:
        if self.video_streams:
            return self.video_streams[0].get("height")
        return None

    @property
    def video_codec(self) -> str | None:
        if self.video_streams:
            return self.video_streams[0].get("codec_name")
        return None

    @property
    def audio_codec(self) -> str | None:
        if self.audio_streams:
            return self.audio_streams[0].get("codec_name")
        return None

    @property
    def fps(self) -> float | None:
        if self.video_streams:
            r = self.video_streams[0].get("r_frame_rate", "0/1")
            num, den = r.split("/")
            if float(den) > 0:
                return float(num) / float(den)
        return None

    @property
    def sample_rate(self) -> int | None:
        if self.audio_streams:
            return self.audio_streams[0].get("sample_rate")
        return None


# ---------------------------------------------------------------------------
# FFmpeg / FFprobe Execution
# ---------------------------------------------------------------------------

def _check_binaries() -> None:
    for bin_name in ("ffmpeg", "ffprobe"):
        if not shutil.which(bin_name):
            raise FileNotFoundError(f"未找到 {bin_name}，请确保已安装 FFmpeg 且在 PATH 中")


def run_ffprobe(input_path: Path) -> FFProbeInfo:
    _check_binaries()
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(input_path),
    ]
    _ensure_logging()
    log_params("FFprobe 执行", input=str(input_path))
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    fmt = data.get("format", {})
    video_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    subtitle_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "subtitle"]

    duration = float(fmt.get("duration", 0))
    size = int(fmt.get("size", 0))
    bitrate = int(fmt.get("bit_rate", 0))

    info = FFProbeInfo(
        path=str(input_path),
        format_name=fmt.get("format_name", ""),
        duration=duration,
        size=size,
        bitrate=bitrate,
        video_streams=video_streams,
        audio_streams=audio_streams,
        subtitle_streams=subtitle_streams,
    )
    log_params("FFprobe 完成", format=info.format_name, duration=info.duration, has_video=info.has_video, has_audio=info.has_audio)
    return info


def run_ffmpeg(
    cmd: list[str],
    *,
    capture_output: bool = False,
) -> subprocess.CompletedProcess:
    _check_binaries()
    # Ensure -y is present for overwrite
    if "-y" not in cmd:
        idx = cmd.index("ffmpeg") + 1
        cmd.insert(idx, "-y")

    _ensure_logging()
    log_params("FFmpeg 执行开始", cmd=" ".join(cmd))

    start = time.monotonic()
    if capture_output:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = round(time.monotonic() - start, 3)
        if result.returncode != 0:
            print(f"FFmpeg stderr:\n{result.stderr}", file=sys.stderr)
            log_params("FFmpeg 执行失败", elapsed=elapsed, returncode=result.returncode)
            raise subprocess.CalledProcessError(result.returncode, cmd)
        log_params("FFmpeg 执行完成", elapsed=elapsed)
        return result
    else:
        result = subprocess.run(cmd)
        elapsed = round(time.monotonic() - start, 3)
        if result.returncode != 0:
            log_params("FFmpeg 执行失败", elapsed=elapsed, returncode=result.returncode)
            raise subprocess.CalledProcessError(result.returncode, cmd)
        log_params("FFmpeg 执行完成", elapsed=elapsed)
        return result


# ---------------------------------------------------------------------------
# Input Validation
# ---------------------------------------------------------------------------

def validate_input_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"文件不存在: {resolved}")
    if not resolved.is_file():
        raise ValueError(f"不是文件: {resolved}")
    return resolved


def validate_video_file(path: Path) -> Path:
    resolved = validate_input_file(path)
    probe = run_ffprobe(resolved)
    if not probe.has_video:
        raise ValueError(f"文件不包含视频流: {resolved}")
    return resolved


def validate_audio_file(path: Path) -> Path:
    resolved = validate_input_file(path)
    probe = run_ffprobe(resolved)
    if not probe.has_audio:
        raise ValueError(f"文件不包含音频流: {resolved}")
    return resolved


# ---------------------------------------------------------------------------
# Output Path
# ---------------------------------------------------------------------------

def ensure_output_dir(*parts: str) -> Path:
    target_dir = DEFAULT_OUTPUT_DIR.joinpath(*parts)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def build_output_path(
    operation: str,
    input_path: Path | None = None,
    *,
    suffix: str = ".mp4",
    subdir: str | None = None,
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_parts = [operation] if subdir is None else [operation, subdir]
    out_dir = ensure_output_dir(*dir_parts)
    if input_path:
        stem = input_path.stem
        return out_dir / f"{timestamp}_{stem}_{operation}{suffix}"
    return out_dir / f"{timestamp}_{operation}{suffix}"


def build_segment_path(operation: str, index: int, suffix: str = ".mp4") -> Path:
    out_dir = ensure_output_dir(operation)
    return out_dir / f"segment_{index:03d}{suffix}"


# ---------------------------------------------------------------------------
# Result Emission
# ---------------------------------------------------------------------------

def emit_result(
    *,
    type: str,
    operation: str,
    local_path: Path,
    input_path: Path | str | None = None,
    elapsed: float | None = None,
    **extra: Any,
) -> None:
    _ensure_logging()
    log_params("输出结果", type=type, operation=operation, local_path=str(local_path), elapsed_seconds=round(elapsed, 2) if elapsed is not None else None)
    result: dict[str, Any] = {
        "type": type,
        "operation": operation,
        "local_path": str(local_path),
    }
    if input_path:
        result["input_path"] = str(input_path)
    if elapsed is not None:
        result["elapsed_seconds"] = round(elapsed, 2)
    result.update(extra)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def emit_multi_result(
    *,
    type: str,
    operation: str,
    local_paths: list[Path],
    input_path: Path | str | None = None,
    elapsed: float | None = None,
    **extra: Any,
) -> None:
    _ensure_logging()
    log_params("输出结果", type=type, operation=operation, count=len(local_paths), elapsed_seconds=round(elapsed, 2) if elapsed is not None else None)
    result: dict[str, Any] = {
        "type": type,
        "operation": operation,
        "local_paths": [str(p) for p in local_paths],
        "count": len(local_paths),
    }
    if input_path:
        result["input_path"] = str(input_path)
    if elapsed is not None:
        result["elapsed_seconds"] = round(elapsed, 2)
    result.update(extra)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

@contextmanager
def timer():
    start = time.monotonic()
    elapsed = [0.0]
    try:
        yield lambda: elapsed[0]
    finally:
        elapsed[0] = time.monotonic() - start


def forward_slash(path: Path | str) -> str:
    """Convert path to forward slashes for FFmpeg filter compatibility on Windows."""
    return str(path).replace("\\", "/")


def filter_path(path: Path | str) -> str:
    """Escape a file path for use inside FFmpeg filter expressions on Windows.

    Wraps in single quotes and escapes backslashes so the filter parser
    treats the entire string as one argument (avoids C: being split).
    E.g. C:\\Users\\test.srt → 'C\:/Users/test.srt'
    """
    s = str(path).replace("\\", "/")
    # Escape backslashes inside quotes for FFmpeg filter parser
    s = s.replace("/", "/")
    return f"'{s}'"


def parse_time_to_seconds(time_str: str) -> float:
    """Parse HH:MM:SS or MM:SS or seconds into float seconds."""
    parts = time_str.strip().split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    else:
        return float(parts[0])


def build_fade_filter(
    duration: float,
    fade_in: float = 0,
    fade_out: float = 0,
) -> str:
    filters = []
    if fade_in > 0:
        filters.append(f"fade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        st = max(0, duration - fade_out)
        filters.append(f"fade=t=out:st={st}:d={fade_out}")
    return ",".join(filters)


def build_volume_filter(
    volume: float | None = None,
    fade_in: float | None = None,
    fade_out: float | None = None,
    duration: float | None = None,
) -> str:
    filters = []
    if volume is not None and volume != 1.0:
        filters.append(f"volume={volume}")
    if fade_in is not None and fade_in > 0:
        filters.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out is not None and fade_out > 0:
        st = max(0, (duration or 0) - fade_out)
        filters.append(f"afade=t=out:st={st}:d={fade_out}")
    return ",".join(filters)


def format_duration(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"


def format_size(bytes_count: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} TB"
