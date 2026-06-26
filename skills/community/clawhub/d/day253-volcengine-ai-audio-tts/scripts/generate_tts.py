#!/usr/bin/env python3
"""Generate speech audio using Volcengine (ByteDance) TTS HTTP API.

Usage:
  python scripts/generate_tts.py --request '{"text":"你好","voice_type":"BV700_streaming"}'
  python scripts/generate_tts.py --file request.json --output output/volcengine-ai-audio-tts/audio/out.mp3

Env: VOLCENGINE_TTS_APP_ID, VOLCENGINE_TTS_TOKEN, VOLCENGINE_TTS_CLUSTER
API: https://openspeech.bytedance.com/api/v1/tts
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests is not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

TTS_API_URL = "https://openspeech.bytedance.com/api/v1/tts"
DEFAULT_VOICE = "BV700_streaming"
DEFAULT_CLUSTER = "volcano_tts"


def _find_repo_root(start: Path) -> Path | None:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_dotenv(Path.cwd() / ".env")
    repo_root = _find_repo_root(Path(__file__).resolve())
    if repo_root:
        _load_dotenv(repo_root / ".env")
    script_dir = Path(__file__).resolve().parent
    _load_dotenv(script_dir / ".env")


def load_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.request:
        return json.loads(args.request)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError("Either --request or --file must be provided")


def build_tts_body(req: dict[str, Any]) -> dict[str, Any]:
    """Build request body for openspeech.bytedance.com/api/v1/tts."""
    app_id = req.get("app_id") or os.environ.get("VOLCENGINE_TTS_APP_ID")
    token = req.get("token") or os.environ.get("VOLCENGINE_TTS_TOKEN")
    cluster = req.get("cluster") or os.environ.get("VOLCENGINE_TTS_CLUSTER", DEFAULT_CLUSTER)
    if not app_id or not token:
        raise ValueError(
            "app_id and token are required. Set VOLCENGINE_TTS_APP_ID and VOLCENGINE_TTS_TOKEN, or pass in request."
        )

    text = req.get("text")
    if not text:
        raise ValueError("text is required")

    voice_type = req.get("voice_type", req.get("voice", DEFAULT_VOICE))
    encoding = req.get("encoding", "mp3")
    rate = req.get("rate", 24000)
    speed_ratio = req.get("speed_ratio", 1.0)
    volume_ratio = req.get("volume_ratio", 1.0)
    pitch_ratio = req.get("pitch_ratio", 1.0)
    language = req.get("language", "")

    body = {
        "app": {
            "appid": app_id,
            "token": token,
            "cluster": cluster,
        },
        "user": {"uid": req.get("uid", "volcengine-tts-skill")},
        "audio": {
            "voice_type": voice_type,
            "encoding": encoding,
            "rate": rate,
            "speed_ratio": speed_ratio,
            "volume_ratio": volume_ratio,
            "pitch_ratio": pitch_ratio,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": req.get("text_type", "plain"),
            "operation": "query",
            "silence_duration": req.get("silence_duration", 125),
        },
    }
    if language:
        body["audio"]["language"] = language
    if "emotion" in req:
        body["audio"]["emotion"] = req["emotion"]
    return body


def call_tts(req: dict[str, Any]) -> dict[str, Any]:
    """Call Volcengine TTS API and return normalized result with audio bytes."""
    body = build_tts_body(req)
    token = body["app"]["token"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer;{token}",
    }
    resp = requests.post(TTS_API_URL, json=body, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    code = data.get("code")
    message = data.get("message", "")
    if code != 3000:
        raise RuntimeError(f"TTS API error: code={code}, message={message}")

    audio_b64 = data.get("data")
    if not audio_b64:
        raise RuntimeError("TTS API returned no audio data")

    addition = data.get("addition") or {}
    duration_ms = addition.get("duration", "")

    return {
        "code": code,
        "message": message,
        "audio_bytes": base64.b64decode(audio_b64),
        "sample_rate": req.get("rate", 24000),
        "format": req.get("encoding", "mp3"),
        "duration_ms": duration_ms,
        "reqid": data.get("reqid"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate audio with Volcengine TTS")
    parser.add_argument("--request", help="Inline JSON request string")
    parser.add_argument("--file", help="Path to JSON request file")
    default_output_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "volcengine-ai-audio-tts" / "audio"
    parser.add_argument(
        "--output",
        default=str(default_output_dir / "output.mp3"),
        help="Output audio path",
    )
    parser.add_argument("--print-response", action="store_true", help="Print normalized response JSON")
    args = parser.parse_args()

    _load_env()
    if not os.environ.get("VOLCENGINE_TTS_APP_ID") or not os.environ.get("VOLCENGINE_TTS_TOKEN"):
        print(
            "Error: VOLCENGINE_TTS_APP_ID and VOLCENGINE_TTS_TOKEN are not set.",
            file=sys.stderr,
        )
        print(
            "Get them from Volcengine 豆包语音控制台: https://www.volcengine.com/docs/6561/196768",
            file=sys.stderr,
        )
        print("Example .env:\n  VOLCENGINE_TTS_APP_ID=your_app_id\n  VOLCENGINE_TTS_TOKEN=your_token\n  VOLCENGINE_TTS_CLUSTER=volcano_tts", file=sys.stderr)
        sys.exit(1)

    req = load_request(args)
    result = call_tts(req)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(result["audio_bytes"])

    out = {
        "audio_path": str(output_path.resolve()),
        "sample_rate": result["sample_rate"],
        "format": result["format"],
        "duration_ms": result["duration_ms"],
        "code": result["code"],
    }
    if args.print_response:
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
