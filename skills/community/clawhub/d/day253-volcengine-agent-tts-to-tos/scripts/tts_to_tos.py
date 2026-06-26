#!/usr/bin/env python3
"""TTS → TOS → Presigned URL: synthesize speech, upload to TOS, return temp link.

Usage:
  python agents/tts-to-tos/scripts/tts_to_tos.py \
    --text "你好" --bucket my-bucket

  python agents/tts-to-tos/scripts/tts_to_tos.py \
    --text "欢迎使用" --bucket my-bucket --key-prefix audio/ --expires 7200 --print-json

Env (TTS): VOLCENGINE_TTS_APP_ID, VOLCENGINE_TTS_TOKEN, VOLCENGINE_TTS_CLUSTER
Env (TOS): VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY, VOLCENGINE_TOS_ENDPOINT, VOLCENGINE_TOS_REGION
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Dependency checks ────────────────────────────────────────────────────────

try:
    import requests
except ImportError:
    print("Error: requests is not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import tos
except ImportError:
    print("Error: tos SDK is not installed. Run: pip install tos", file=sys.stderr)
    sys.exit(1)

# ── Constants ────────────────────────────────────────────────────────────────

TTS_API_URL = "https://openspeech.bytedance.com/api/v1/tts"
DEFAULT_VOICE = "BV700_streaming"
DEFAULT_CLUSTER = "volcano_tts"

ENCODING_TO_EXT = {"mp3": ".mp3", "wav": ".wav", "pcm": ".pcm", "ogg_opus": ".ogg"}
ENCODING_TO_MIME = {
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "pcm": "audio/pcm",
    "ogg_opus": "audio/ogg",
}


# ── Env loading ──────────────────────────────────────────────────────────────

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


# ── Step 1: TTS ──────────────────────────────────────────────────────────────

def synthesize_speech(
    text: str,
    voice_type: str = DEFAULT_VOICE,
    encoding: str = "mp3",
    speed_ratio: float = 1.0,
    volume_ratio: float = 1.0,
    pitch_ratio: float = 1.0,
    language: str = "",
) -> dict[str, Any]:
    """Call Volcengine TTS API and return audio bytes + metadata."""
    app_id = os.environ.get("VOLCENGINE_TTS_APP_ID")
    token = os.environ.get("VOLCENGINE_TTS_TOKEN")
    cluster = os.environ.get("VOLCENGINE_TTS_CLUSTER", DEFAULT_CLUSTER)

    if not app_id or not token:
        raise RuntimeError(
            "VOLCENGINE_TTS_APP_ID and VOLCENGINE_TTS_TOKEN must be set. "
            "See: https://www.volcengine.com/docs/6561/196768"
        )

    body: dict[str, Any] = {
        "app": {"appid": app_id, "token": token, "cluster": cluster},
        "user": {"uid": "tts-to-tos-agent"},
        "audio": {
            "voice_type": voice_type,
            "encoding": encoding,
            "rate": 24000,
            "speed_ratio": speed_ratio,
            "volume_ratio": volume_ratio,
            "pitch_ratio": pitch_ratio,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "silence_duration": 125,
        },
    }
    if language:
        body["audio"]["language"] = language

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer;{token}"}
    resp = requests.post(TTS_API_URL, json=body, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    code = data.get("code")
    if code != 3000:
        raise RuntimeError(f"TTS error: code={code}, message={data.get('message')}")

    audio_b64 = data.get("data")
    if not audio_b64:
        raise RuntimeError("TTS returned no audio data")

    addition = data.get("addition") or {}
    return {
        "audio_bytes": base64.b64decode(audio_b64),
        "duration_ms": addition.get("duration", ""),
        "reqid": data.get("reqid", ""),
        "encoding": encoding,
    }


# ── Step 2: Upload to TOS ───────────────────────────────────────────────────

def _get_tos_client() -> tos.TosClientV2:
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
    sk = os.environ.get("VOLCENGINE_SECRET_KEY", "")
    endpoint = os.environ.get("VOLCENGINE_TOS_ENDPOINT", "")
    region = os.environ.get("VOLCENGINE_TOS_REGION", "")

    missing = [k for k, v in [
        ("VOLCENGINE_ACCESS_KEY", ak),
        ("VOLCENGINE_SECRET_KEY", sk),
        ("VOLCENGINE_TOS_ENDPOINT", endpoint),
        ("VOLCENGINE_TOS_REGION", region),
    ] if not v]
    if missing:
        raise RuntimeError(f"Missing TOS env vars: {', '.join(missing)}")

    return tos.TosClientV2(ak, sk, endpoint, region)


def upload_to_tos(
    audio_bytes: bytes,
    bucket: str,
    key: str,
    content_type: str,
) -> dict[str, Any]:
    """Upload audio bytes to TOS and return metadata."""
    client = _get_tos_client()
    resp = client.put_object(bucket, key, content=audio_bytes, content_type=content_type)
    return {
        "bucket": bucket,
        "key": key,
        "etag": getattr(resp, "etag", ""),
        "status_code": getattr(resp, "status_code", 200),
        "size": len(audio_bytes),
    }


# ── Step 3: Presign URL ─────────────────────────────────────────────────────

def generate_presigned_url(bucket: str, key: str, expires: int = 3600) -> str:
    """Generate a GET presigned URL for the uploaded object."""
    client = _get_tos_client()
    result = client.pre_signed_url("GET", bucket, key, expires=expires)
    return result.signed_url


# ── Pipeline ─────────────────────────────────────────────────────────────────

def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    """Execute TTS → TOS upload → presign pipeline."""
    # Step 1: Synthesize
    print(f"[1/3] Synthesizing: \"{args.text[:50]}{'...' if len(args.text) > 50 else ''}\"")
    tts_result = synthesize_speech(
        text=args.text,
        voice_type=args.voice_type,
        encoding=args.encoding,
        speed_ratio=args.speed_ratio,
        volume_ratio=args.volume_ratio,
        pitch_ratio=args.pitch_ratio,
        language=args.language,
    )
    audio_bytes = tts_result["audio_bytes"]
    print(f"      Audio: {len(audio_bytes)} bytes, duration={tts_result['duration_ms']}ms")

    # Build TOS key
    ext = ENCODING_TO_EXT.get(args.encoding, ".mp3")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    short_id = uuid.uuid4().hex[:8]
    tos_key = f"{args.key_prefix.rstrip('/')}/{ts}-{short_id}{ext}"

    # Optionally save local copy
    local_path = None
    if args.keep_local:
        out_dir = Path(os.getenv("OUTPUT_DIR", "output")) / "tts-to-tos"
        out_dir.mkdir(parents=True, exist_ok=True)
        local_path = out_dir / f"{ts}-{short_id}{ext}"
        local_path.write_bytes(audio_bytes)
        print(f"      Local: {local_path}")

    # Step 2: Upload
    content_type = ENCODING_TO_MIME.get(args.encoding, "application/octet-stream")
    print(f"[2/3] Uploading to tos://{args.bucket}/{tos_key}")
    upload_result = upload_to_tos(audio_bytes, args.bucket, tos_key, content_type)
    print(f"      ETag: {upload_result['etag']}")

    # Step 3: Presign
    print(f"[3/3] Generating presigned URL (expires={args.expires}s)")
    presigned_url = generate_presigned_url(args.bucket, tos_key, args.expires)
    print(f"      URL: {presigned_url}")

    return {
        "text": args.text,
        "voice_type": args.voice_type,
        "encoding": args.encoding,
        "duration_ms": tts_result["duration_ms"],
        "audio_size": len(audio_bytes),
        "tos_bucket": args.bucket,
        "tos_key": tos_key,
        "etag": upload_result["etag"],
        "presigned_url": presigned_url,
        "expires_seconds": args.expires,
        "local_path": str(local_path) if local_path else None,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tts_to_tos",
        description="TTS → TOS → Presigned URL pipeline",
    )
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--bucket", required=True, help="TOS bucket name")
    parser.add_argument("--voice-type", default=DEFAULT_VOICE, help="TTS voice (default: BV700_streaming)")
    parser.add_argument("--encoding", default="mp3", choices=["mp3", "wav", "pcm", "ogg_opus"])
    parser.add_argument("--speed-ratio", type=float, default=1.0, help="Speed [0.2, 3]")
    parser.add_argument("--volume-ratio", type=float, default=1.0, help="Volume [0.1, 3]")
    parser.add_argument("--pitch-ratio", type=float, default=1.0, help="Pitch [0.1, 3]")
    parser.add_argument("--language", default="", help="Language hint, e.g. cn")
    parser.add_argument("--key-prefix", default="tts/", help="TOS key prefix (default: tts/)")
    parser.add_argument("--expires", type=int, default=3600, help="Presigned URL expiry seconds (default: 3600)")
    parser.add_argument("--keep-local", action="store_true", help="Keep local audio file")
    parser.add_argument("--print-json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    _load_env()

    try:
        result = run_pipeline(args)
    except tos.exceptions.TosClientError as e:
        print(f"TOS client error: {e}", file=sys.stderr)
        sys.exit(1)
    except tos.exceptions.TosServerError as e:
        print(f"TOS server error: code={e.code}, message={e.message}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.print_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\nDone.")


if __name__ == "__main__":
    main()
