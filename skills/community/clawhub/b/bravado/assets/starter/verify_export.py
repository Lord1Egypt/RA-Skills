"""Check the delivery contract and decode every frame/sample of an exported MP4.

Usage: python verify_export.py output/film.mp4
Requires ffprobe and ffmpeg on PATH; no Python dependencies are needed.
This checks file integrity, not visual quality, sound quality, or factual claims.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess
import sys


class ExportVerificationError(ValueError):
    """The export is unreadable or violates the requested delivery contract."""


def validate_probe(probe: dict, *, width: int = 1920, height: int = 1080,
                   fps: str | float = 30, duration: float = 31,
                   duration_tolerance: float = 0.05) -> None:
    """Validate ffprobe JSON without launching tools (also useful in tests).

    Check container and both stream durations so a short audio track cannot hide
    behind a full-length video. The default tolerance allows AAC/container
    rounding, but is tighter than two frames at the default frame rate.
    """
    try:
        expected_fps = Fraction(str(fps))
        valid = (width > 0 and height > 0 and expected_fps > 0
                 and math.isfinite(duration) and duration > 0
                 and math.isfinite(duration_tolerance) and duration_tolerance >= 0)
    except (ValueError, TypeError, ZeroDivisionError):
        valid = False
    if not valid:
        raise ExportVerificationError("Expected dimensions, fps and duration must be positive; "
                                      "duration tolerance must be finite and nonnegative")
    if not isinstance(probe, dict):
        raise ExportVerificationError("ffprobe JSON must be an object")

    errors = []
    streams = probe.get("streams", [])
    if not isinstance(streams, list) or any(not isinstance(s, dict) for s in streams):
        raise ExportVerificationError("ffprobe JSON has invalid streams")
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    container = probe.get("format", {})
    if not isinstance(container, dict):
        raise ExportVerificationError("ffprobe JSON has invalid format metadata")
    if "mp4" not in str(container.get("format_name", "")).split(","):
        errors.append("container: expected MP4")

    def expect(label, actual, expected):
        if actual != expected:
            errors.append(f"{label}: expected {expected!r}, got {actual!r}")

    def check_duration(label, raw):
        try:
            actual = float(raw)
        except (ValueError, TypeError):
            actual = float("nan")
        if not math.isfinite(actual) or abs(actual - duration) > duration_tolerance:
            errors.append(f"{label}: expected {duration:g}s ± {duration_tolerance:g}s, got {raw!r}")

    expect("video stream count", len(videos), 1)
    expect("audio stream count", len(audios), 1)
    check_duration("container duration", container.get("duration"))
    if len(videos) == 1:
        video = videos[0]
        expect("video codec", video.get("codec_name"), "h264")
        expect("video width", video.get("width"), width)
        expect("video height", video.get("height"), height)
        for key in ("avg_frame_rate", "r_frame_rate"):
            try:
                actual_fps = Fraction(video.get(key, "0/0"))
            except (ValueError, TypeError, ZeroDivisionError, OverflowError):
                actual_fps = None
            expect(f"video {key}", actual_fps, expected_fps)
        check_duration("video duration", video.get("duration"))
    if len(audios) == 1:
        audio = audios[0]
        expect("audio codec", audio.get("codec_name"), "aac")
        expect("audio channels", audio.get("channels"), 2)
        expect("audio channel layout", audio.get("channel_layout"), "stereo")
        check_duration("audio duration", audio.get("duration"))
    if errors:
        raise ExportVerificationError("Export contract failed:\n- " + "\n- ".join(errors))


def _run(command: list[str], stage: str) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise ExportVerificationError(f"{stage}: {command[0]} is not installed or not on PATH") from exc
    except OSError as exc:
        raise ExportVerificationError(f"{stage}: cannot run {command[0]}: {exc}") from exc
    # Both commands use error-only logging. Some decoder builds can log an error
    # yet exit successfully, so reported errors fail the gate too.
    if result.returncode or result.stderr.strip():
        detail = result.stderr.strip()[-4000:] or "no diagnostic output"
        raise ExportVerificationError(f"{stage} failed (exit {result.returncode}): {detail}")
    return result.stdout


def verify_export(path: str | Path, **contract) -> dict:
    """Probe, validate, and fully decode the video and audio; return metadata.

    Raises ExportVerificationError on failure. No output file is modified.
    The full decode is mandatory, with no seek, duration cap, or stream copying.
    """
    path = Path(path).resolve()
    if not path.is_file():
        raise ExportVerificationError(f"Export does not exist or is not a file: {path}")
    raw = _run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                "-of", "json", str(path)], "ffprobe")
    try:
        probe = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ExportVerificationError(f"ffprobe returned invalid JSON: {exc}") from exc
    validate_probe(probe, **contract)
    _run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-err_detect", "explode",
          "-i", str(path), "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"],
         "Full video/audio decode")
    return probe


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="MP4 export to verify")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", default="30", help="Expected rate, e.g. 30 or 30000/1001")
    parser.add_argument("--duration", type=float, default=31)
    parser.add_argument("--duration-tolerance", type=float, default=0.05, metavar="SECONDS")
    args = vars(parser.parse_args(argv))
    path = args.pop("path")
    try:
        verify_export(path, **args)
    except ExportVerificationError as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 1
    print(f"Verified {path}: MP4, {args['width']}×{args['height']}, {args['fps']} fps, "
          f"H.264 + AAC stereo, {args['duration']:g}s; full video/audio decode passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
