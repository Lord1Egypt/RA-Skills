# -*- coding: utf-8 -*-
"""
inspect_audio.py — 探测音频文件的时长、采样率、声道数等元信息。

用法:
  python3 inspect_audio.py <audio_file_or_url>

探测优先级:
  1. ffprobe（最全面，支持本地文件和 URL）
  2. macOS afinfo（仅本地文件，仅 macOS）
  3. Python wave 模块（仅 .wav 文件）

返回 JSON:
  成功: {duration_seconds, sample_rate, channels, codec_name, container_format, probe_tool}
  失败: {error, message, recommended_next_step?}

"""

import json
import os
import platform
import re
import subprocess
import sys
import wave


FFPROBE_URL_TIMEOUT_SECONDS = 15


def print_json(payload, exit_code=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if exit_code:
        sys.exit(exit_code)


def is_http_url(input_value):
    return input_value.startswith("http://") or input_value.startswith("https://")


def run_command(command, timeout_seconds=None):
    try:
        return subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as e:
        return e
    except subprocess.TimeoutExpired as e:
        return e


def inspect_with_ffprobe(input_value):
    """使用 ffprobe 探测音频文件元信息。"""
    timeout_seconds = FFPROBE_URL_TIMEOUT_SECONDS if is_http_url(input_value) else None
    command = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_streams", "-show_format",
        input_value,
    ]
    result = run_command(command, timeout_seconds=timeout_seconds)
    if result is None:
        return None
    if isinstance(result, subprocess.CalledProcessError):
        error_result = {
            "error": "FFPROBE_FAILED",
            "message": f"ffprobe execution failed. stderr: {result.stderr.strip()}",
            "probe_tool": "ffprobe",
        }
        if is_http_url(input_value):
            error_result["recommended_next_step"] = (
                "Verify that the URL is publicly reachable. If the URL is known-good and you plan "
                "to use standard async recognition, you may still try asr_standard.py directly."
            )
        return error_result
    if isinstance(result, subprocess.TimeoutExpired):
        error_result = {
            "error": "FFPROBE_TIMEOUT",
            "message": f"ffprobe timed out after {FFPROBE_URL_TIMEOUT_SECONDS} seconds.",
            "probe_tool": "ffprobe",
            "recommended_next_step": (
                "If the input is already a public URL and you plan to use standard async recognition, "
                "you may call asr_standard.py directly instead of blocking on local probing."
            ),
        }
        if is_http_url(input_value):
            error_result["direct_url_async_allowed"] = True
        return error_result

    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    audio_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "audio"), None
    )
    if not audio_stream:
        return {
            "error": "NO_AUDIO_STREAM",
            "message": "No audio stream found in input.",
            "probe_tool": "ffprobe",
        }

    format_info = payload.get("format", {})
    duration = audio_stream.get("duration") or format_info.get("duration")
    sample_rate = audio_stream.get("sample_rate")
    channels = audio_stream.get("channels")
    file_size = format_info.get("size")

    inspected = {
        "duration_seconds": float(duration) if duration is not None else None,
        "sample_rate": int(sample_rate) if sample_rate else None,
        "channels": int(channels) if channels else None,
        "codec_name": audio_stream.get("codec_name"),
        "container_format": format_info.get("format_name"),
        "file_size_bytes": int(file_size) if file_size else None,
        "probe_tool": "ffprobe",
    }
    return inspected


def inspect_with_afinfo(input_value):
    """macOS 专用：通过 afinfo 探测音频文件。"""
    if platform.system() != "Darwin" or not os.path.isfile(input_value):
        return None

    result = run_command(["afinfo", input_value])
    if result is None or isinstance(
        result, (subprocess.CalledProcessError, subprocess.TimeoutExpired)
    ):
        return None

    stdout = result.stdout
    duration_match = re.search(r"estimated duration:\s*([0-9.]+)", stdout)
    sample_rate_match = re.search(r"([0-9.]+)\s*Hz", stdout)
    channels_match = re.search(r"([0-9]+)\s*channel", stdout)

    inspected = {
        "duration_seconds": float(duration_match.group(1)) if duration_match else None,
        "sample_rate": int(float(sample_rate_match.group(1))) if sample_rate_match else None,
        "channels": int(channels_match.group(1)) if channels_match else None,
        "codec_name": None,
        "container_format": os.path.splitext(input_value)[1].lstrip(".").lower() or None,
        "probe_tool": "afinfo",
    }
    return inspected


def inspect_wav_with_wave(input_value):
    """通过 Python 标准库 wave 模块探测 .wav 文件。"""
    if not os.path.isfile(input_value) or not input_value.lower().endswith(".wav"):
        return None

    try:
        with wave.open(input_value, "rb") as wav_file:
            frames = wav_file.getnframes()
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
    except wave.Error:
        return None

    inspected = {
        "duration_seconds": frames / float(sample_rate) if sample_rate else None,
        "sample_rate": sample_rate,
        "channels": channels,
        "codec_name": "pcm",
        "container_format": "wav",
        "probe_tool": "python-wave",
    }
    return inspected


def main():
    if len(sys.argv) != 2:
        print_json(
            {
                "error": "NO_INPUT",
                "message": "Usage: python3 inspect_audio.py <audio_file_or_url>",
            },
            exit_code=1,
        )

    input_value = sys.argv[1]

    # 如果是本地文件，补充文件大小
    file_size_bytes = None
    if os.path.isfile(input_value):
        file_size_bytes = os.path.getsize(input_value)

    inspected = inspect_with_ffprobe(input_value)
    if inspected:
        if file_size_bytes and not inspected.get("file_size_bytes"):
            inspected["file_size_bytes"] = file_size_bytes
        exit_code = 1 if inspected.get("error") else 0
        print_json(inspected, exit_code=exit_code)

    inspected = inspect_with_afinfo(input_value)
    if inspected:
        if file_size_bytes:
            inspected["file_size_bytes"] = file_size_bytes
        print_json(inspected)

    inspected = inspect_wav_with_wave(input_value)
    if inspected:
        if file_size_bytes:
            inspected["file_size_bytes"] = file_size_bytes
        print_json(inspected)

    print_json(
        {
            "error": "REQUIRES_FFPROBE",
            "message": (
                "Unable to reliably inspect duration, sample rate, and channels "
                "with available built-in tools."
            ),
            "file_size_bytes": file_size_bytes,
            "recommended_next_step": (
                "Run ensure_ffmpeg.py --execute first, then rerun inspect_audio.py. "
                "If the input is already a public URL and you plan to use standard async "
                "recognition, you may call asr_standard.py directly."
            ),
            "direct_url_async_allowed": is_http_url(input_value),
        },
        exit_code=1,
    )


if __name__ == "__main__":
    main()
