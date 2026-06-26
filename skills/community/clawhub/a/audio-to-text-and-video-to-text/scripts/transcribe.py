#!/usr/bin/env python3
"""
transcribe.py — Audio/Video Transcription Script for openclaw.ai
Uses OpenAI Whisper API with ffmpeg for media handling.

Usage:
    python transcribe.py --input <file> [options]

Options:
    --input       Path to the audio/video file (required)
    --output      Output file path (default: transcript.txt next to input)
    --api-key     OpenAI API key (or set OPENAI_API_KEY env var)
    --model       Whisper model: whisper-1 | gpt-4o-transcribe (default: whisper-1)
    --language    ISO 639-1 language code, e.g. en, ar, fr (default: auto-detect)
    --format      Output format: txt | srt | vtt | json (default: txt)
    --timestamps  Include timestamps in txt output (flag)
    --chunk-size  Max chunk size in MB, must be ≤ 25 (default: 20)
    --prompt      Context hint to improve accuracy
    --verbose     Show progress details
"""

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Argument Parsing
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Transcribe audio/video files with Whisper.")
    p.add_argument("--input", required=True, help="Path to media file")
    p.add_argument("--output", default=None, help="Output transcript path")
    p.add_argument("--api-key", default=None, help="OpenAI API key")
    p.add_argument("--model", default="whisper-1",
                   choices=["whisper-1", "gpt-4o-transcribe", "gpt-4o-mini-transcribe"],
                   help="Whisper model to use")
    p.add_argument("--language", default=None, help="Language code (e.g. en, ar, fr)")
    p.add_argument("--format", default="txt",
                   choices=["txt", "srt", "vtt", "json"],
                   help="Output format")
    p.add_argument("--timestamps", action="store_true",
                   help="Include timestamps in txt output")
    p.add_argument("--chunk-size", type=int, default=20,
                   help="Max chunk size in MB (≤ 25)")
    p.add_argument("--prompt", default=None, help="Context hint for accuracy")
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg, verbose=True):
    if verbose:
        print(f"[transcribe] {msg}", flush=True)


def ensure_openai(api_key):
    """Import openai and set the API key."""
    try:
        import openai as _openai
    except ImportError:
        print("Installing openai...", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "openai", "--break-system-packages", "-q"])
        import openai as _openai

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        print("\n❌  OpenAI API key not found.")
        print("    Set OPENAI_API_KEY in your environment or pass --api-key <key>")
        print("    Get a key at: https://platform.openai.com/api-keys")
        sys.exit(1)

    _openai.api_key = key
    return _openai


def check_ffmpeg():
    """Verify ffmpeg is installed."""
    result = subprocess.run(["ffmpeg", "-version"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("❌  ffmpeg not found. Install it:")
        print("    Ubuntu/Debian: sudo apt install ffmpeg")
        print("    macOS:         brew install ffmpeg")
        print("    Windows:       https://ffmpeg.org/download.html")
        sys.exit(1)


def get_duration(file_path: str) -> float:
    """Return audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 0.0
    try:
        info = json.loads(result.stdout)
        return float(info.get("format", {}).get("duration", 0))
    except Exception:
        return 0.0


def extract_audio(input_path: str, output_path: str, start: float = 0, duration: float = None):
    """Extract/convert audio segment to 16kHz mono MP3 using ffmpeg."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]

    if start > 0:
        cmd += ["-ss", str(start)]

    cmd += ["-i", input_path]

    if duration is not None:
        cmd += ["-t", str(duration)]

    cmd += [
        "-vn",                   # no video
        "-ar", "16000",          # 16kHz sample rate
        "-ac", "1",              # mono
        "-b:a", "64k",           # 64kbps bitrate
        "-f", "mp3",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {result.stderr}")


def get_file_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


# ---------------------------------------------------------------------------
# Chunking Logic
# ---------------------------------------------------------------------------

def calculate_chunks(total_duration: float, max_mb: int, input_path: str) -> list:
    """
    Calculate chunk boundaries based on duration and target file size.
    Returns list of (start_seconds, duration_seconds) tuples.
    """
    # Estimate bitrate: 64kbps mono 16kHz → ~0.5 MB/min
    # We use 20 MB target → ~40 min chunks, but we verify empirically
    # Conservative: use total_size / max_mb to figure out how many chunks

    total_size = get_file_size_mb(input_path)

    if total_size <= max_mb:
        return [(0, None)]  # No chunking needed

    num_chunks = math.ceil(total_size / max_mb)
    chunk_duration = total_duration / num_chunks
    overlap = 1.0  # 1-second overlap for context continuity

    chunks = []
    for i in range(num_chunks):
        start = max(0, i * chunk_duration - (overlap if i > 0 else 0))
        duration = chunk_duration + (overlap if i < num_chunks - 1 else 0)
        chunks.append((start, duration))

    return chunks


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def transcribe_chunk(openai, audio_path: str, model: str, language: str,
                     output_format: str, prompt: str, verbose: bool) -> dict:
    """
    Send one audio chunk to Whisper API.
    Returns dict with 'text', optionally 'segments'.
    """
    # For txt with timestamps, use verbose_json to get segment data
    api_format = "verbose_json" if output_format in ("txt", "srt", "vtt") else output_format

    kwargs = {
        "model": model,
        "response_format": api_format,
    }
    if language:
        kwargs["language"] = language
    if prompt:
        kwargs["prompt"] = prompt

    for attempt in range(3):
        try:
            with open(audio_path, "rb") as f:
                response = openai.audio.transcriptions.create(
                    file=f,
                    **kwargs
                )

            # openai SDK returns an object or raw text depending on format
            if api_format == "verbose_json":
                # Response has .text and .segments
                return {
                    "text": response.text,
                    "segments": getattr(response, "segments", [])
                }
            elif api_format == "json":
                return {"text": response.text, "segments": []}
            else:
                return {"text": str(response), "segments": []}

        except Exception as e:
            err_str = str(e)
            if "rate_limit" in err_str.lower() and attempt < 2:
                wait = 30 * (attempt + 1)
                log(f"Rate limit hit — waiting {wait}s...", verbose)
                time.sleep(wait)
            elif "file too large" in err_str.lower():
                raise RuntimeError(
                    f"Chunk too large for Whisper API. "
                    f"Try reducing --chunk-size to 15 or lower."
                )
            else:
                raise


def adjust_timestamps(segments: list, offset: float) -> list:
    """Shift segment start/end times by offset seconds."""
    adjusted = []
    for seg in segments:
        s = dict(seg) if hasattr(seg, "__iter__") else {}
        if hasattr(seg, "start"):
            s = {
                "start": seg.start + offset,
                "end": seg.end + offset,
                "text": seg.text,
            }
        elif isinstance(seg, dict):
            s = {
                "start": seg.get("start", 0) + offset,
                "end": seg.get("end", 0) + offset,
                "text": seg.get("text", ""),
            }
        adjusted.append(s)
    return adjusted


# ---------------------------------------------------------------------------
# Output Formatters
# ---------------------------------------------------------------------------

def format_timestamp_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def format_timestamp_txt(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"


def build_output(all_segments: list, full_text: str, fmt: str,
                 include_timestamps: bool) -> str:
    if fmt == "json":
        return json.dumps({
            "text": full_text,
            "segments": all_segments
        }, indent=2, ensure_ascii=False)

    if fmt == "srt":
        lines = []
        for i, seg in enumerate(all_segments, 1):
            start = format_timestamp_srt(seg.get("start", 0))
            end = format_timestamp_srt(seg.get("end", 0))
            text = seg.get("text", "").strip()
            lines.append(f"{i}\n{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    if fmt == "vtt":
        lines = ["WEBVTT", ""]
        for seg in all_segments:
            start = format_timestamp_vtt(seg.get("start", 0))
            end = format_timestamp_vtt(seg.get("end", 0))
            text = seg.get("text", "").strip()
            lines.append(f"{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    # Plain text
    if include_timestamps and all_segments:
        lines = []
        for seg in all_segments:
            ts = format_timestamp_txt(seg.get("start", 0))
            text = seg.get("text", "").strip()
            lines.append(f"{ts} {text}")
        return "\n".join(lines)
    else:
        return full_text.strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    verbose = args.verbose

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌  File not found: {input_path}")
        sys.exit(1)

    # Default output path
    if args.output is None:
        stem = Path(input_path).stem
        ext = "json" if args.format == "json" else args.format
        args.output = str(Path(input_path).parent / f"{stem}_transcript.{ext}")

    log(f"Input:  {input_path}", verbose)
    log(f"Output: {args.output}", verbose)
    log(f"Model:  {args.model}", verbose)
    log(f"Format: {args.format}", verbose)

    # Checks
    check_ffmpeg()
    openai = ensure_openai(args.api_key)

    # Get duration
    total_duration = get_duration(input_path)
    log(f"Duration: {total_duration:.1f}s ({total_duration/60:.1f} min)", verbose)

    # Work in a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Determine chunks
        chunks = calculate_chunks(total_duration, args.chunk_size, input_path)
        log(f"Chunks: {len(chunks)}", verbose)

        all_segments = []
        full_text_parts = []
        prev_prompt = args.prompt  # carry-forward prompt for context

        for i, (start, duration) in enumerate(chunks):
            log(f"Processing chunk {i+1}/{len(chunks)} (start={start:.1f}s)...", verbose)

            # Extract audio chunk
            chunk_path = os.path.join(tmpdir, f"chunk_{i:04d}.mp3")
            extract_audio(input_path, chunk_path, start=start, duration=duration)

            chunk_mb = get_file_size_mb(chunk_path)
            log(f"  Chunk size: {chunk_mb:.1f} MB", verbose)

            if chunk_mb > 25:
                print(f"⚠️  Chunk {i+1} is {chunk_mb:.1f} MB — exceeds 25 MB limit.")
                print(f"   Try reducing --chunk-size to {args.chunk_size - 5}")
                sys.exit(1)

            # Transcribe
            result = transcribe_chunk(
                openai=openai,
                audio_path=chunk_path,
                model=args.model,
                language=args.language,
                output_format=args.format,
                prompt=prev_prompt,
                verbose=verbose
            )

            # Adjust timestamps relative to original file
            if result.get("segments"):
                adjusted = adjust_timestamps(result["segments"], offset=start)
                all_segments.extend(adjusted)

            chunk_text = result.get("text", "").strip()
            full_text_parts.append(chunk_text)

            # Use end of this transcript as prompt for next chunk (context continuity)
            if chunk_text:
                prev_prompt = chunk_text[-200:]  # last 200 chars

        # Assemble final output
        full_text = " ".join(full_text_parts)
        output_content = build_output(
            all_segments=all_segments,
            full_text=full_text,
            fmt=args.format,
            include_timestamps=args.timestamps
        )

    # Write output
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_content)

    word_count = len(full_text.split())
    print(f"\n✅  Transcription complete!")
    print(f"   Output: {args.output}")
    print(f"   Words:  ~{word_count:,}")
    if total_duration > 0:
        print(f"   Length: {total_duration/60:.1f} minutes")

    return args.output


if __name__ == "__main__":
    main()
