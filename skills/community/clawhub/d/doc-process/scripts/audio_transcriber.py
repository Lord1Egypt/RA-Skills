#!/usr/bin/env python3
"""
audio_transcriber.py — Transcribe audio files to text using OpenAI Whisper.

Requires: openai-whisper  (pip install openai-whisper)
          ffmpeg           (system dependency for non-WAV formats)

Supported formats: mp3, mp4, m4a, wav, ogg, flac, webm, mpeg, mpga

Usage:
  python audio_transcriber.py --file meeting.mp3 --output transcript.txt
  python audio_transcriber.py --file meeting.mp3 --output transcript.txt --model small
  python audio_transcriber.py --file meeting.mp3 --output transcript.txt --language en
  python audio_transcriber.py --file meeting.mp3 --output transcript.txt --timestamps
"""

import argparse
import sys
from pathlib import Path


SUPPORTED_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".flac", ".webm", ".mpeg", ".mpga"}

WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]


def _require_whisper():
    try:
        import whisper
        return whisper
    except ImportError:
        print(
            "Error: openai-whisper is not installed.\n"
            "Install it with:  pip install openai-whisper\n"
            "You also need ffmpeg: https://ffmpeg.org/download.html",
            file=sys.stderr,
        )
        sys.exit(1)


def transcribe(
    audio_path: Path,
    model_name: str = "base",
    language: str | None = None,
    include_timestamps: bool = False,
) -> dict:
    """
    Transcribe an audio file using Whisper.

    Returns a dict with:
      text: full transcript string
      language: detected language code
      segments: list of {start, end, text} dicts (if timestamps requested)
    """
    whisper = _require_whisper()

    print(f"Loading Whisper model '{model_name}'…", file=sys.stderr)
    model = whisper.load_model(model_name)

    print(f"Transcribing {audio_path.name}…", file=sys.stderr)
    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(str(audio_path), **options)

    detected_language = result.get("language", "unknown")
    print(f"Detected language: {detected_language}", file=sys.stderr)

    output = {
        "text": result.get("text", "").strip(),
        "language": detected_language,
        "segments": [],
    }

    if include_timestamps:
        for seg in result.get("segments", []):
            output["segments"].append({
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip(),
            })

    return output


def format_transcript(result: dict, include_timestamps: bool = False) -> str:
    """Format the transcription result as plain text."""
    if not include_timestamps or not result["segments"]:
        return result["text"]

    lines = []
    for seg in result["segments"]:
        start = _format_time(seg["start"])
        end = _format_time(seg["end"])
        lines.append(f"[{start} → {end}] {seg['text']}")
    return "\n".join(lines)


def _format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:05.2f}"
    return f"{m:02d}:{s:05.2f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="audio_transcriber",
        description="Transcribe audio files to text using OpenAI Whisper.",
    )
    parser.add_argument("--file", required=True, help="Path to audio file")
    parser.add_argument("--output", required=True, help="Output .txt file path")
    parser.add_argument(
        "--model",
        choices=WHISPER_MODELS,
        default="base",
        help="Whisper model size (default: base). Larger = more accurate but slower.",
    )
    parser.add_argument(
        "--language",
        help="Source language code (e.g. 'en', 'fr', 'ja'). Auto-detected if not provided.",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in output (format: [MM:SS.ss → MM:SS.ss] text)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    audio_path = Path(args.file).expanduser()
    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}", file=sys.stderr)
        return 1

    if audio_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(
            f"Warning: '{audio_path.suffix}' may not be supported. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
            file=sys.stderr,
        )

    try:
        result = transcribe(
            audio_path,
            model_name=args.model,
            language=getattr(args, "language", None),
            include_timestamps=args.timestamps,
        )
    except Exception as e:
        print(f"Transcription failed: {e}", file=sys.stderr)
        return 1

    transcript_text = format_transcript(result, include_timestamps=args.timestamps)

    out_path = Path(args.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(transcript_text, encoding="utf-8")

    word_count = len(transcript_text.split())
    print(
        f"Transcript written to {out_path} "
        f"({word_count} words, language: {result['language']})",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
