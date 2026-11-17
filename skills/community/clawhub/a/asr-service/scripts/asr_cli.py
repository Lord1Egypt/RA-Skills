#!/usr/bin/env python3
"""asr — ASR Skill CLI"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

# Add skill root to path
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

# Ensure ffmpeg is available (use imageio-ffmpeg bundled binary if system ffmpeg missing)
try:
    import imageio_ffmpeg
    _ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    if _ffmpeg and not any(
        os.access(os.path.join(p, "ffmpeg"), os.X_OK)
        for p in os.environ.get("PATH", "").split(os.pathsep) if p
    ):
        os.environ["PATH"] = os.path.dirname(_ffmpeg) + os.pathsep + os.environ.get("PATH", "")
except (ImportError, RuntimeError, OSError):
    pass

from asr_service import ASRSkill  # noqa: E402


def cmd_transcribe(args: argparse.Namespace) -> None:
    skill = ASRSkill()
    result = skill.transcribe(
        Path(args.audio_file),
        language=args.language,
        response_format=args.format,
        speaker_labels=args.speakers,
    )
    if args.format == "text":
        print(result.text)
    else:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


def cmd_srt(args: argparse.Namespace) -> None:
    skill = ASRSkill()
    print(skill.transcribe_srt(
        Path(args.audio_file),
        language=args.language,
        speaker_labels=args.speakers,
    ))


def cmd_vtt(args: argparse.Namespace) -> None:
    skill = ASRSkill()
    print(skill.transcribe_vtt(
        Path(args.audio_file),
        language=args.language,
        speaker_labels=args.speakers,
    ))


def cmd_serve_status(args: argparse.Namespace) -> None:
    skill = ASRSkill()
    print(json.dumps(skill.serve_status(), indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(prog="asr", description="ASR Skill CLI")
    sub = parser.add_subparsers(dest="command")

    # transcribe
    tr = sub.add_parser("transcribe", help="Transcribe audio file to text")
    tr.add_argument("audio_file", help="Audio file path (mp3, wav, m4a, etc.)")
    tr.add_argument("--language", default=None, help="Language code (zh/en/ja/ko, etc.) — auto if omitted")
    tr.add_argument("--format", default="json", choices=["json", "text", "verbose_json"],
                    help="Response format")
    tr.add_argument("--speakers", action="store_true",
                    help="Enable speaker diarization (spk=true)")

    # srt
    srt = sub.add_parser("srt", help="Transcribe audio file to SRT subtitles")
    srt.add_argument("audio_file", help="Audio file path (mp3, wav, m4a, etc.)")
    srt.add_argument("--language", default=None,
                     help="Language code (zh/en/ja/ko, etc.) — auto if omitted")
    srt.add_argument("--speakers", action="store_true",
                     help="Enable speaker diarization (spk=true)")

    # vtt
    vtt = sub.add_parser("vtt", help="Transcribe audio file to VTT subtitles")
    vtt.add_argument("audio_file", help="Audio file path (mp3, wav, m4a, etc.)")
    vtt.add_argument("--language", default=None,
                     help="Language code (zh/en/ja/ko, etc.) — auto if omitted")
    vtt.add_argument("--speakers", action="store_true",
                     help="Enable speaker diarization (spk=true)")

    # serve-status
    sub.add_parser("serve-status", help="ASR service status")

    args = parser.parse_args()

    if args.command == "transcribe":
        cmd_transcribe(args)
    elif args.command == "srt":
        cmd_srt(args)
    elif args.command == "vtt":
        cmd_vtt(args)
    elif args.command == "serve-status":
        cmd_serve_status(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
