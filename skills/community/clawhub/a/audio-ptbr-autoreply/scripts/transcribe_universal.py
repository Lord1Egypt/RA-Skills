#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from transformers import pipeline
except ImportError as exc:
    raise SystemExit("transformers not installed in this environment") from exc


MODEL_NAME = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
_PIPELINE = None


def get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        print("Loading ASR model...", file=sys.stderr)
        _PIPELINE = pipeline("automatic-speech-recognition", model=MODEL_NAME)
    return _PIPELINE


def transcribe(audio_path: str) -> dict[str, Any]:
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    result = get_pipeline()(str(path))
    text = str(result.get("text", "")).strip()

    return {
        "success": True,
        "text": text,
        "model": MODEL_NAME,
        "language": "pt-BR",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path")
    parser.add_argument("--text", action="store_true", help="Print only transcribed text")
    args = parser.parse_args()

    try:
        data = transcribe(args.audio_path)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}), file=sys.stderr)
        return 1

    if args.text:
        print(data["text"])
    else:
        print(json.dumps(data, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
