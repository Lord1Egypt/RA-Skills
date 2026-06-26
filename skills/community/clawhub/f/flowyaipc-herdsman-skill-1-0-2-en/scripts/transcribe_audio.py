#!/usr/bin/env python3
"""
Herdsman audio transcription script.
"""

import argparse
import json
import sys

from herdsman_client import HerdsmanAPIError, HerdsmanClient, prepare_media_input


def main() -> None:
    parser = argparse.ArgumentParser(description="Herdsman Audio Transcription")
    parser.add_argument("audio", help="Input audio: local path, URL, or data URL")
    parser.add_argument("--model", required=True, help="Model ID")
    parser.add_argument("--language", help="Optional language code, auto-detect if empty")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="Herdsman API base URL")
    parser.add_argument("--api-key", default="", help="Optional API Key")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    args = parser.parse_args()

    try:
        audio = prepare_media_input(args.audio, default_mime_type="audio/wav")
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    client = HerdsmanClient(base_url=args.base_url, api_key=args.api_key, timeout=300)

    try:
        result = client.transcribe_audio(
            model=args.model,
            audio=audio,
            language=args.language,
        )
    except HerdsmanAPIError as exc:
        print(json.dumps(exc.to_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    text = result.get("text", "")
    if text:
        print(text)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    language = result.get("language")
    duration = result.get("duration")
    if language or duration is not None:
        print()
    if language:
        print(f"Detected language: {language}")
    if duration is not None:
        print(f"Audio duration: {duration}")


if __name__ == "__main__":
    main()
