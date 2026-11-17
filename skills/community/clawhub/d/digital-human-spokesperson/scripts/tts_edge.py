#!/usr/bin/env python3
"""Synthesize text to speech using edge-tts (free, no API key required).

Generates an audio file and a sidecar .json carrying the spoken duration
(queried via ffprobe when available) plus the resolved voice and text.
The duration is consumed by compose_bilingual.py for subtitle timing.

Usage:
    python tts_edge.py --text en.txt --lang en-US --voice en-US-AriaNeural --out en.mp3
    python tts_edge.py --text ar.txt --lang ar-EG --voice ar-EG-SalmaNeural --out ar.mp3

Supported --lang defaults:
    en-US -> en-US-AriaNeural
    en-GB -> en-GB-SoniaNeural
    ar-EG -> ar-EG-SalmaNeural
    ar-SA -> ar-SA-ZariyahNeural
"""
import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys


def default_voice(lang: str) -> str:
    return {
        "en-US": "en-US-AriaNeural",
        "en-GB": "en-GB-SoniaNeural",
        "ar-EG": "ar-EG-SalmaNeural",
        "ar-SA": "ar-SA-ZariyahNeural",
    }.get(lang, "en-US-AriaNeural")


def get_duration(path: str):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    try:
        out = subprocess.check_output(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            stderr=subprocess.DEVNULL,
        )
        return float(out.strip())
    except Exception:
        return None


async def synth(text: str, voice: str, out: str):
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out)


def main():
    ap = argparse.ArgumentParser(description="edge-tts text-to-speech for EN/AR")
    ap.add_argument("--text", required=True, help="Input text file (.txt, UTF-8)")
    ap.add_argument("--lang", default="en-US", help="Language tag, e.g. en-US, ar-EG")
    ap.add_argument("--voice", default=None, help="Voice name; default chosen by --lang")
    ap.add_argument("--out", required=True, help="Output audio file (.mp3)")
    args = ap.parse_args()

    with open(args.text, encoding="utf-8") as f:
        raw = f.read().strip()

    # Collapse blank lines into paragraph breaks; keep line grouping for subtitles.
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    text = "\n".join(lines)

    voice = args.voice or default_voice(args.lang)
    try:
        asyncio.run(synth(text, voice, args.out))
    except ImportError:
        sys.exit("edge-tts is not installed. Run: pip install edge-tts")
    except Exception as exc:  # pragma: no cover - network/model failures
        sys.exit(f"TTS failed: {exc}")

    dur = get_duration(args.out)
    sidecar = os.path.splitext(args.out)[0] + ".json"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(
            {"voice": voice, "lang": args.lang, "duration": dur, "text": text},
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"[tts] voice={voice} lang={args.lang} duration={dur} -> {args.out}")


if __name__ == "__main__":
    main()
