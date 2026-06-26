#!/usr/bin/env python3
import argparse
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from env import get_dashscope_key, get_region_base_url, get_tts_config

try:
    import dashscope
except Exception:  # pragma: no cover
    print("Error: dashscope not installed. pip install dashscope", file=sys.stderr)
    raise SystemExit(1)

import subprocess

try:
    import requests
except Exception:  # pragma: no cover
    print("Error: requests not installed. pip install requests", file=sys.stderr)
    raise SystemExit(1)


def _build_tts_kwargs(text: str, cfg: dict) -> dict:
    kwargs = {
        "text": text,
        "format": "wav",
        "sample_rate": int(cfg.get("sample_rate") or 16000),
    }
    if cfg.get("model"):
        kwargs["model"] = cfg["model"]
    if cfg.get("voice"):
        kwargs["voice"] = cfg["voice"]
    return kwargs


def _extract_audio_url(resp) -> str:
    try:
        return resp["output"]["audio"]["url"]
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Unexpected TTS response format") from exc


def synthesize_wav(text: str) -> bytes:
    cfg = get_tts_config()
    kwargs = _build_tts_kwargs(text, cfg)

    resp = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
        api_key=get_dashscope_key(),
        **kwargs,
    )
    audio_url = _extract_audio_url(resp)
    response = requests.get(audio_url, timeout=60)
    response.raise_for_status()
    return response.content


def play_wav(wav_bytes: bytes) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(wav_bytes)
        tmp.flush()
        try:
            subprocess.run(["ffplay", "-nodisp", "-autoexit", tmp.name], check=True)
        except FileNotFoundError:
            print("Error: ffplay not found. Please install ffmpeg.", file=sys.stderr)
            raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bailian TTS speak")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--output", default=None, help="Output WAV file path (instead of playing)")
    args = parser.parse_args()

    if args.base_url:
        dashscope.base_http_api_url = args.base_url
    else:
        dashscope.base_http_api_url = get_region_base_url()

    try:
        wav_bytes = synthesize_wav(args.text)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    if args.output:
        # Save to file
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(wav_bytes)
        print(f"WAV saved to: {args.output}")
    else:
        play_wav(wav_bytes)
        print("TTS playback finished.")


if __name__ == "__main__":
    main()
