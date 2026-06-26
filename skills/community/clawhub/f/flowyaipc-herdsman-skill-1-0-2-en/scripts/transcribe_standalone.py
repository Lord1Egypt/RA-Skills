#!/usr/bin/env python3
"""
Herdsman audio transcription script: uses Herdsman ASR models for speech recognition.
Supports whisper-base, sherpa-onnx-paraformer-zh-small, funasr (WebSocket), sherpa-onnx-streaming-zipformer, etc.

Usage:
    uv run python transcribe_audio.py <audio_path> --model <model_id> [--language <language>] [--output <absolute_path>]

Parameters:
    audio_path - Input audio file path (local file, supports .wav .mp3 .m4a etc.)
    --model    - ASR model ID (required)
    --language - Language code (optional, auto-detect by default)
    --output   - Output result file (absolute path, optional, prints to terminal if not specified)

Tested models:
    - whisper-base                     ✅ General high accuracy
    - sherpa-onnx-paraformer-zh-small  ✅ Fast, best for Simplified Chinese
    - funasr                           ⚠️ WebSocket streaming only (HTTP not supported)
    - sherpa-onnx-streaming-zipformer-zh-14m ⚠️ Streaming only (HTTP does not support full transcription)

Output:
    When --output is specified: writes recognition text to file and prints absolute path
    When not specified: prints to terminal only
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def transcribe_audio(audio_path: str, model: str, language: str | None = None, timeout: int = 300) -> dict:
    """Call the Herdsman OpenAI-compatible transcription endpoint."""

    if not os.path.isfile(audio_path):
        print(f"Error: audio file not found -> {audio_path}", file=sys.stderr)
        sys.exit(1)

    # Read audio file and convert to base64 data URL
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # Infer MIME type from extension
    ext = os.path.splitext(audio_path)[1].lower()
    mime_map = {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
        ".aac": "audio/aac",
    }
    mime = mime_map.get(ext, "audio/wav")
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_data_url = f"data:{mime};base64,{audio_b64}"

    payload = {
        "model": model,
        "audio": audio_data_url,
    }
    if language:
        payload["language"] = language

    url = "http://127.0.0.1:8080/v1/audio/transcriptions"
    headers = {
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API request failed (HTTP {e.code}): {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"API connection failed: {e.reason}\nEnsure Herdsman service is running at http://127.0.0.1:8080", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"API returned non-JSON response", file=sys.stderr)
        sys.exit(1)

    return result


def main():
    parser = argparse.ArgumentParser(description="Herdsman Audio Transcription Script")
    parser.add_argument("audio", help="Input audio file path (local path)")
    parser.add_argument("--model", required=True, help="ASR model ID (e.g., whisper-base, sherpa-onnx-paraformer-zh-small)")
    parser.add_argument("--language", help="Language code (e.g., zh, en; optional, auto-detect by default)")
    parser.add_argument("--output", "-o", help="Output result file (absolute path, optional)")
    parser.add_argument("--timeout", type=int, default=300, help="API timeout in seconds, default 300")

    args = parser.parse_args()

    # Transcribe
    print(f"Calling Herdsman ASR model [{args.model}] ...", file=sys.stderr)
    result = transcribe_audio(args.audio, args.model, args.language, args.timeout)

    text = result.get("text", "")
    language = result.get("language", "")
    duration = result.get("duration")

    # Output to file
    if args.output:
        output_path = os.path.abspath(args.output)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Recognized text saved: {output_path}")

        # Also save full JSON (same directory with .json suffix)
        json_path = os.path.splitext(output_path)[0] + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Full result saved: {json_path}")
    else:
        # Print only
        if text:
            print(text)

    # Print metadata
    info_parts = []
    if language:
        info_parts.append(f"Detected language: {language}")
    if duration is not None:
        info_parts.append(f"Audio duration: {duration}s")
    if info_parts:
        print(" | ".join(info_parts), file=sys.stderr)


if __name__ == "__main__":
    main()