#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def _bootstrap_shared_senseaudio_env() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "_shared" / "senseaudio_env.py"
        if candidate.exists():
            candidate_dir = str(candidate.parent)
            if candidate_dir not in sys.path:
                sys.path.insert(0, candidate_dir)
            from senseaudio_env import ensure_senseaudio_env
            ensure_senseaudio_env()
            return


_bootstrap_shared_senseaudio_env()

from senseaudio_api_guard import ensure_runtime_api_key
from senseaudio_asr_client import (
    API_URL,
    ASRRequest,
    choose_model,
    transcribe,
    validate_input,
    validate_model_support,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn a user voice message into an OpenClaw-ready text turn.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-json")
    parser.add_argument("--model")
    parser.add_argument("--language", default="")
    parser.add_argument("--target-language", default="")
    parser.add_argument("--response-format", choices=["json", "text", "verbose_json"], default="json")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--enable-itn", dest="enable_itn", action="store_true")
    parser.add_argument("--disable-itn", dest="enable_itn", action="store_false")
    parser.add_argument("--enable-punctuation", action="store_true")
    parser.add_argument("--enable-speaker-diarization", action="store_true")
    parser.add_argument("--max-speakers", type=int)
    parser.add_argument("--enable-sentiment", action="store_true")
    parser.add_argument("--timestamp-granularity", action="append", choices=["word", "segment"])
    parser.add_argument("--hotwords", default="")
    parser.add_argument("--recognize-mode", default="")
    parser.add_argument("--channel")
    parser.add_argument("--user-id")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    parser.set_defaults(enable_itn=None)
    return parser.parse_args()


def normalize_text(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return normalized

    parts = normalized.split(" ")
    if len(parts) == 2 and parts[0] == parts[1]:
        return parts[0]

    sentences = [chunk for chunk in re.findall(r"[^。！？!?；;]+[。！？!?；;]?", normalized) if chunk.strip()]
    if len(sentences) >= 2 and len(sentences) % 2 == 0:
        first_half = sentences[: len(sentences) // 2]
        second_half = sentences[len(sentences) // 2 :]
        if first_half == second_half:
            return "".join(first_half).strip()

    return normalized


def build_understanding(raw_response, normalized_text: str) -> Dict[str, object]:
    clarification_needed = not normalized_text
    segment_count = 0
    if isinstance(raw_response, dict):
        segments = raw_response.get("segments")
        if isinstance(segments, list):
            segment_count = len(segments)
    return {
        "clarification_needed": clarification_needed,
        "clarification_prompt": "这段语音我没有听清楚，请再说一次。" if clarification_needed else "",
        "segment_count": segment_count,
        "input_type": "voice",
    }


def main() -> int:
    args = parse_args()
    api_key = ensure_runtime_api_key(os.getenv(args.api_key_env), args.api_key_env, purpose="asr")

    audio_path = Path(args.input)
    audio_meta = validate_input(audio_path)

    request = ASRRequest(
        audio_path=audio_path,
        model=args.model or "sense-asr-deepthink",
        language=args.language,
        target_language=args.target_language,
        response_format=args.response_format,
        stream=args.stream,
        enable_itn=args.enable_itn,
        enable_punctuation=args.enable_punctuation or None,
        enable_speaker_diarization=args.enable_speaker_diarization or None,
        max_speakers=args.max_speakers,
        enable_sentiment=args.enable_sentiment or None,
        timestamp_granularities=args.timestamp_granularity,
        hotwords=args.hotwords,
        recognize_mode=args.recognize_mode,
    )

    explicit_model = args.model is not None
    selected_model, model_reason = choose_model(request, explicit_model)
    request.model = selected_model
    validate_model_support(request)

    result = transcribe(request, api_key)
    normalized_text = normalize_text(result.transcript)
    understanding = build_understanding(result.raw_response, normalized_text)

    manifest = {
        "request": {
            "input_path": str(audio_path),
            "channel": args.channel or "",
            "user_id": args.user_id or "",
        },
        "routing": {
            "endpoint": API_URL,
            "selected_model": selected_model,
            "model_reason": model_reason,
            "request_fields": result.request_fields,
        },
        "audio": audio_meta,
        "transcript": {
            "raw_text": result.transcript,
            "normalized_text": normalized_text,
            "empty": not bool(normalized_text),
        },
        "understanding": understanding,
        "openclaw": {
            "turn_payload": {
                "role": "user",
                "content": normalized_text,
                "metadata": {
                    "input_type": "voice",
                    "source_audio_path": str(audio_path),
                    "asr_model": selected_model,
                    "channel": args.channel or "",
                    "user_id": args.user_id or "",
                    "clarification_needed": understanding["clarification_needed"],
                },
            }
        },
        "raw_response": result.raw_response,
    }

    if args.out_json:
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    json.dump(manifest, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
