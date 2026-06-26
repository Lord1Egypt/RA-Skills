#!/usr/bin/env python3
"""
Herdsman Text-to-Speech (TTS) script.

Supports VoiceDesign (voice_description) and VoiceClone (ref_audio / ref_text) modes,
as well as streaming TTS (--stream returns stream_url for pulling).
"""

import argparse
import json
import os
import sys
from datetime import datetime

from herdsman_client import HerdsmanAPIError, HerdsmanClient, prepare_media_input


def default_output_dir() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def auto_output_path() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(default_output_dir(), f"tts_{timestamp}.wav")


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman TTS Synthesis")
    parser.add_argument("input", help="Input text")
    parser.add_argument("--model", required=True, help="Model ID, e.g., qwen3-tts-customvoice / edge-tts")
    parser.add_argument("--voice", help="Voice type / name, e.g., Cherry / zh-CN-YunxiNeural")
    parser.add_argument("--speaker", help="Speaker ID (uses voice if not set)")
    parser.add_argument("--voice-description", help="VoiceDesign mode natural language voice description")
    parser.add_argument("--ref-audio", help="VoiceClone mode reference audio (path, URL, or base64)")
    parser.add_argument("--ref-text", help="VoiceClone mode reference audio text")
    parser.add_argument("--language", default="Chinese", help="Language")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--stream", action="store_true", help="Enable streaming mode (returns stream_url)")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="Herdsman API base URL")
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--output", "-o", help="Output file path (non-streaming only)")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    parser.add_argument("--auto-save", action="store_true", help="Auto save to outputs/ (non-streaming only)")
    parser.add_argument("--download", action="store_true", help="Try curl download if stream_url returned")
    args = parser.parse_args()

    if args.stream and (args.auto_save or args.output):
        print("Cannot save audio file directly in --stream mode; stream_url will be returned", file=sys.stderr)
        sys.exit(1)

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=120)

    # Prepare optional VoiceClone ref_audio
    ref_audio = None
    if args.ref_audio:
        try:
            ref_audio = prepare_media_input(args.ref_audio, default_mime_type="audio/wav")
        except (OSError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)

    payload = {
        "model": args.model,
        "input": args.input,
        "voice": args.voice,
        "speaker": args.speaker,
        "voice_description": args.voice_description,
        "ref_audio": ref_audio,
        "ref_text": args.ref_text,
        "language": args.language,
        "speed": args.speed,
        "stream": args.stream,
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    try:
        result = client.audio_speech(
            model=args.model,
            input_text=args.input,
            voice=args.voice,
            speaker=args.speaker,
            voice_description=args.voice_description,
            ref_audio=ref_audio,
            ref_text=args.ref_text,
            language=args.language,
            speed=args.speed,
            stream=args.stream,
        )
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Stream mode: show stream_url
    if args.stream:
        stream_url = result.get("stream_url", "")
        if stream_url:
            full_url = f"{args.base_url.rstrip('/')}{stream_url}"
            print(f"Stream URL: {full_url}")
            if args.download:
                import subprocess
                subprocess.run(["curl", "-o", auto_output_path(), full_url], check=False)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Non-stream mode: show audio info and optionally save
    audio_url = result.get("audio_url", "")
    duration = result.get("duration")
    sample_rate = result.get("sample_rate")

    if args.output or args.auto_save:
        target_path = args.output or auto_output_path()
        # Build full URL for download
        full_url = f"{args.base_url.rstrip('/')}{audio_url}"
        try:
            saved = client.download_to_file(full_url, target_path, timeout=120)
            print(f"Audio saved: {saved}")
        except HerdsmanAPIError as exc:
            print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Audio URL: {args.base_url.rstrip('/')}{audio_url}")

    if sample_rate:
        print(f"Sample rate: {sample_rate} Hz")
    if duration is not None:
        print(f"Duration: {duration}s")


if __name__ == "__main__":
    main()