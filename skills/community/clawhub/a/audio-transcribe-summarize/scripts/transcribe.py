#!/usr/bin/env python3
"""
Transcribe audio/video files using SenseAudio ASR API.
Handles files >10MB by auto-splitting with ffmpeg.

Usage:
    python transcribe.py <audio_file> [options]

Options:
    --model MODEL           ASR model (default: sense-asr-pro)
    --language LANG         Language code, e.g. zh, en, ja (default: auto-detect)
    --speakers              Enable speaker diarization
    --max-speakers N        Max speakers (1-20, requires --speakers, asr-pro only)
    --sentiment             Enable sentiment/emotion analysis
    --timestamps TYPE       Timestamp granularity: word, segment, or both
    --translate LANG        Translate to target language code
    --hotwords WORDS        Comma-separated hotwords (sense-asr-lite only)
    --output FILE           Output file path (default: <input>.transcript.txt)
    --format FORMAT         Response format: json, text, verbose_json (default: verbose_json)

Requires:
    - SENSEAUDIO_API_KEY environment variable
    - requests: pip install requests
    - ffmpeg (only for files >10MB)
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

_bin_cache: dict[str, str | None] = {}

# IDE/GUI 启动的进程常缺少 Homebrew 等路径，需主动搜索
_EXTRA_SEARCH_PATHS = [
    "/opt/homebrew/bin",        # macOS Homebrew (Apple Silicon)
    "/usr/local/bin",           # macOS Homebrew (Intel) / Linux common
    "/usr/bin",                 # Linux system
    "/snap/bin",                # Linux snap
]


def find_bin(name: str) -> str:
    """Find executable by name, searching PATH + common install locations."""
    if name in _bin_cache:
        return _bin_cache[name]

    found = shutil.which(name)
    if not found:
        for d in _EXTRA_SEARCH_PATHS:
            candidate = os.path.join(d, name)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                found = candidate
                break
    if not found:
        # Windows: also try common locations
        if sys.platform == "win32":
            for win_dir in [
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "ffmpeg", "bin"),
                os.path.join(os.environ.get("ProgramFiles", ""), "ffmpeg", "bin"),
                r"C:\ffmpeg\bin",
            ]:
                candidate = os.path.join(win_dir, f"{name}.exe")
                if os.path.isfile(candidate):
                    found = candidate
                    break

    _bin_cache[name] = found
    return found


def get_api_key():
    """Load API key from environment variable."""
    key = os.environ.get("SENSEAUDIO_API_KEY")
    if not key:
        print("Error: SENSEAUDIO_API_KEY not found in environment variables.")
        sys.exit(1)
    return key


def get_audio_duration(filepath):
    """Get audio duration in seconds using ffprobe."""
    ffprobe = find_bin("ffprobe")
    if not ffprobe:
        return None
    try:
        result = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", filepath],
            capture_output=True, text=True
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return None


def split_audio(filepath, chunk_duration=300):
    """Split audio into chunks using ffmpeg. Returns list of chunk file paths."""
    duration = get_audio_duration(filepath)
    ffmpeg = find_bin("ffmpeg")
    if duration is None or not ffmpeg:
        hint = ""
        if not find_bin("ffprobe"):
            hint = ("\nHint: ffmpeg may be installed but not in PATH. "
                    "Try running from a terminal, or set the full path in your PATH env var.")
        print(f"Error: ffmpeg/ffprobe not found.{hint}")
        sys.exit(1)

    num_chunks = math.ceil(duration / chunk_duration)
    tmp_dir = tempfile.mkdtemp(prefix="senseaudio_")
    ext = Path(filepath).suffix
    chunks = []

    print(f"Splitting {duration:.0f}s audio into {num_chunks} chunks of ~{chunk_duration}s each...")

    for i in range(num_chunks):
        start = i * chunk_duration
        chunk_path = os.path.join(tmp_dir, f"chunk_{i:04d}{ext}")
        subprocess.run(
            [ffmpeg, "-y", "-i", filepath, "-ss", str(start), "-t", str(chunk_duration),
             "-acodec", "copy", "-vn", chunk_path],
            capture_output=True
        )
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)

    return chunks, tmp_dir


def transcribe_file(filepath, args, api_key):
    """Transcribe a single audio file via SenseASR API."""
    headers = {"Authorization": f"Bearer {api_key}"}

    files = {"file": (os.path.basename(filepath), open(filepath, "rb"))}

    data = {"model": args.model}

    resp_format = getattr(args, "format", "verbose_json")
    data["response_format"] = resp_format

    if args.language:
        data["language"] = args.language
    if args.speakers:
        data["enable_speaker_diarization"] = "true"
    if args.max_speakers:
        data["max_speakers"] = str(args.max_speakers)
    if args.sentiment:
        data["enable_sentiment"] = "true"
    if args.translate:
        data["target_language"] = args.translate
    if args.hotwords:
        data["hotwords"] = args.hotwords

    if args.timestamps:
        if args.timestamps == "both":
            data["timestamp_granularities[]"] = ["word", "segment"]
        else:
            data["timestamp_granularities[]"] = args.timestamps

    response = requests.post(API_URL, headers=headers, files=files, data=data, timeout=300)

    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        return None

    return response.json() if resp_format != "text" else {"text": response.text}


def format_verbose_result(result):
    """Format verbose_json result into readable text."""
    lines = []
    segments = result.get("segments") or []

    if segments:
        for seg in segments:
            parts = []
            if seg.get("start") is not None:
                start = seg["start"]
                end = seg.get("end", start)
                parts.append(f"[{start:.1f}s - {end:.1f}s]")
            if seg.get("speaker"):
                parts.append(f"({seg['speaker']})")
            if seg.get("sentiment"):
                parts.append(f"[{seg['sentiment']}]")

            prefix = " ".join(parts)
            text = seg.get("text", "")
            translation = seg.get("translation")

            if prefix:
                lines.append(f"{prefix} {text}")
            else:
                lines.append(text)

            if translation:
                lines.append(f"  -> {translation}")
            lines.append("")
    else:
        lines.append(result.get("text", ""))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using SenseAudio ASR API")
    parser.add_argument("audio_file", help="Path to audio/video file")
    parser.add_argument("--model", default="sense-asr-pro",
                        choices=["sense-asr-lite", "sense-asr", "sense-asr-pro", "sense-asr-deepthink"])
    parser.add_argument("--language", default=None)
    parser.add_argument("--speakers", action="store_true")
    parser.add_argument("--max-speakers", type=int, default=None)
    parser.add_argument("--sentiment", action="store_true")
    parser.add_argument("--timestamps", choices=["word", "segment", "both"], default=None)
    parser.add_argument("--translate", default=None)
    parser.add_argument("--hotwords", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--format", default="verbose_json",
                        choices=["json", "text", "verbose_json"])

    args = parser.parse_args()
    audio_path = args.audio_file

    if not os.path.exists(audio_path):
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    api_key = get_api_key()
    file_size = os.path.getsize(audio_path)

    output_path = args.output or str(Path(audio_path).with_suffix(".transcript.txt"))

    if file_size <= MAX_FILE_SIZE:
        print(f"Transcribing {audio_path} ({file_size / 1024 / 1024:.1f}MB) with {args.model}...")
        result = transcribe_file(audio_path, args, api_key)
        if result is None:
            sys.exit(1)
        results = [result]
    else:
        print(f"File {file_size / 1024 / 1024:.1f}MB exceeds 10MB limit. Splitting...")
        chunks, tmp_dir = split_audio(audio_path)
        results = []
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
            result = transcribe_file(chunk, args, api_key)
            if result:
                results.append(result)
            os.remove(chunk)
        os.rmdir(tmp_dir)

    full_text_parts = []
    raw_results = []

    for result in results:
        if args.format == "verbose_json":
            full_text_parts.append(format_verbose_result(result))
        else:
            full_text_parts.append(result.get("text", ""))
        raw_results.append(result)

    full_transcript = "\n".join(full_text_parts).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)

    json_path = str(Path(output_path).with_suffix(".json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(raw_results if len(raw_results) > 1 else raw_results[0], f, ensure_ascii=False, indent=2)

    duration_info = ""
    if raw_results and isinstance(raw_results[0], dict):
        dur = raw_results[0].get("duration") or (raw_results[0].get("audio_info") or {}).get("duration")
        if dur:
            total_sec = dur / 1000 if dur > 1000 else dur
            duration_info = f" ({total_sec:.0f}s)"

    print(f"\nDone! Transcript saved to: {output_path}{duration_info}")
    print(f"Raw JSON saved to: {json_path}")
    print(f"\nPreview (first 500 chars):\n{full_transcript[:500]}")


if __name__ == "__main__":
    main()
