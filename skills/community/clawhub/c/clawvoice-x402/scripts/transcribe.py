#!/usr/bin/env python3
"""Transcribe a WAV file with faster-whisper. Prints JSON on stdout."""
import json
import sys


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: transcribe.py <audio-file> [model]"}))
        return 1
    path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "base"
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(json.dumps({"error": "faster-whisper not installed (run: x402-agent-voice install-mic)"}))
        return 1
    try:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, info = model.transcribe(path)
        text = " ".join(s.text.strip() for s in segments).strip()
        print(json.dumps({"text": text, "language": info.language, "durationS": round(info.duration, 2)}))
        return 0
    except Exception as exc:  # noqa: BLE001 - report any failure as JSON
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
