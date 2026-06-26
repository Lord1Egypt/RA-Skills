#!/usr/bin/env python3
"""
Audio format conversion script: convert any audio format to 16kHz mono WAV.
Used for preprocessing reference audio for Herdsman qwen3-tts-voiceclone.

Usage:
    uv run python convert_audio.py <input_path> [output_path]

Parameters:
    input_path  - Input audio file path (e.g., .mp3 .m4a .wav .ogg)
    output_path - Output WAV file path (optional, defaults to same directory as input with .wav extension)

Output:
    16kHz mono PCM s16le WAV file
"""

import subprocess
import sys
import os


def convert_to_wav(input_path: str, output_path: str | None = None) -> str:
    """Convert any audio to 16kHz mono WAV."""

    if not os.path.isfile(input_path):
        print(f"Error: input file not found -> {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".wav"

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg not found, please install it and add to PATH", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-sample_fmt", "s16",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ffmpeg conversion failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(output_path)
    print(f"Conversion successful: {output_path} ({file_size} bytes)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    convert_to_wav(input_path, output_path)