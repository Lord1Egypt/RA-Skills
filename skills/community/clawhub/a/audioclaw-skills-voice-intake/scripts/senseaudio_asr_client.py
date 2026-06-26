#!/usr/bin/env python3
import json
import mimetypes
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union


API_URL = "https://api.senseaudio.cn/v1/audio/transcriptions"
SUPPORTED_SUFFIXES = {".wav", ".mp3", ".ogg", ".opus", ".flac", ".aac", ".m4a", ".mp4"}
MAX_BYTES = 10 * 1024 * 1024
MAX_SECONDS = 7200
VALID_MODELS = {"sense-asr-lite", "sense-asr", "sense-asr-pro", "sense-asr-deepthink"}


class SenseAudioASRError(RuntimeError):
    pass


@dataclass
class ASRRequest:
    audio_path: Path
    model: str
    language: str = ""
    target_language: str = ""
    response_format: str = "json"
    stream: bool = False
    enable_itn: Optional[bool] = None
    enable_punctuation: Optional[bool] = None
    enable_speaker_diarization: Optional[bool] = None
    max_speakers: Optional[int] = None
    enable_sentiment: Optional[bool] = None
    timestamp_granularities: Optional[List[str]] = None
    hotwords: str = ""
    recognize_mode: str = ""


@dataclass
class ASRResult:
    raw_response: Union[dict, str]
    transcript: str
    request_fields: Dict[str, object]


def detect_duration_seconds(path: Path) -> float:
    try:
        output = subprocess.check_output(["/usr/bin/afinfo", str(path)], stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0.0
    for raw_line in output.decode("utf-8", "ignore").splitlines():
        if "estimated duration:" not in raw_line:
            continue
        fragment = raw_line.split("estimated duration:", 1)[1].strip()
        seconds = fragment.split()[0]
        try:
            return float(seconds)
        except ValueError:
            return 0.0
    return 0.0


def validate_input(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise SystemExit(
            "Unsupported file type. Expected one of: .wav, .mp3, .ogg, .opus, .flac, .aac, .m4a, .mp4"
        )
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit("Input file exceeds the official HTTP API 10MB limit.")
    duration = detect_duration_seconds(path)
    if duration and duration > MAX_SECONDS:
        raise SystemExit("Input audio exceeds the official 2-hour limit.")
    return {
        "size_bytes": size,
        "duration_seconds": duration,
    }


def choose_model(request: ASRRequest, explicit_model: bool) -> Tuple[str, str]:
    model = request.model
    if explicit_model:
        return model, "explicit"

    if request.enable_sentiment or request.enable_speaker_diarization or request.timestamp_granularities or request.enable_punctuation or request.max_speakers:
        return "sense-asr-pro", "rich_structure_features"
    if request.hotwords:
        return "sense-asr-lite", "hotwords"
    if request.language:
        return "sense-asr", "language_hint"
    return "sense-asr-deepthink", "default_voice_understanding"


def validate_model_support(request: ASRRequest) -> None:
    model = request.model
    if model not in VALID_MODELS:
        raise SystemExit(f"Unsupported model: {model}")

    if model == "sense-asr-lite":
        if request.stream:
            raise SystemExit("sense-asr-lite does not support stream mode.")
        if request.target_language:
            raise SystemExit("sense-asr-lite does not support target_language.")
        if request.enable_speaker_diarization or request.enable_sentiment or request.timestamp_granularities:
            raise SystemExit("sense-asr-lite does not support diarization, sentiment, or timestamps.")
    elif model == "sense-asr":
        if request.hotwords:
            raise SystemExit("sense-asr does not support hotwords.")
        if request.max_speakers:
            raise SystemExit("max_speakers is only supported by sense-asr-pro.")
    elif model == "sense-asr-pro":
        if request.hotwords:
            raise SystemExit("sense-asr-pro does not support hotwords.")
    elif model == "sense-asr-deepthink":
        if request.language:
            raise SystemExit("sense-asr-deepthink does not support language.")
        if request.hotwords:
            raise SystemExit("sense-asr-deepthink does not support hotwords.")
        if request.enable_itn is not None:
            raise SystemExit("sense-asr-deepthink does not support enable_itn.")
        if request.enable_punctuation:
            raise SystemExit("sense-asr-deepthink does not support enable_punctuation.")
        if request.enable_speaker_diarization or request.enable_sentiment or request.timestamp_granularities:
            raise SystemExit("sense-asr-deepthink does not support diarization, sentiment, or timestamps.")
        if request.recognize_mode and not request.stream:
            raise SystemExit("recognize_mode is only useful in deepthink stream mode.")


def _iter_field_items(fields: Dict[str, object]) -> Sequence[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for key, value in fields.items():
        if value is None or value == "" or value == []:
            continue
        if isinstance(value, list):
            for entry in value:
                items.append((key, str(entry)))
        elif isinstance(value, bool):
            items.append((key, "true" if value else "false"))
        else:
            items.append((key, str(value)))
    return items


def build_multipart(fields: Dict[str, object], file_field: str, path: Path) -> Tuple[bytes, str]:
    boundary = f"----CodexSenseAudio{uuid.uuid4().hex}"
    chunks = []
    for key, value in _iter_field_items(fields):
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    chunks.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{file_field}"; filename="{path.name}"\r\n'.encode("utf-8"),
            f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
            path.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return b"".join(chunks), boundary


def parse_response(body: str, response_format: str) -> Union[dict, str]:
    if response_format == "text":
        return body
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"text": body}


def extract_transcript(response: Union[dict, str]) -> str:
    if isinstance(response, str):
        return response.strip()
    if "text" in response and isinstance(response["text"], str):
        return response["text"].strip()
    if "result" in response and isinstance(response["result"], str):
        return response["result"].strip()
    return ""


def transcribe(request: ASRRequest, api_key: str) -> ASRResult:
    fields: Dict[str, object] = {
        "model": request.model,
        "response_format": request.response_format,
        "stream": request.stream,
        "language": request.language,
        "target_language": request.target_language,
        "enable_itn": request.enable_itn,
        "enable_punctuation": request.enable_punctuation,
        "enable_speaker_diarization": request.enable_speaker_diarization,
        "max_speakers": request.max_speakers,
        "enable_sentiment": request.enable_sentiment,
        "timestamp_granularities[]": request.timestamp_granularities or [],
        "hotwords": request.hotwords,
        "recognize_mode": request.recognize_mode,
    }
    body, boundary = build_multipart(fields, "file", request.audio_path)
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "Codex-SenseAudio-OpenClaw-ASR/1.0",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                text = response.read().decode("utf-8", "replace")
                parsed = parse_response(text, request.response_format)
                return ASRResult(
                    raw_response=parsed,
                    transcript=extract_transcript(parsed),
                    request_fields=fields,
                )
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(body_text)
            except json.JSONDecodeError:
                payload = {"message": body_text}
            if exc.code == 429 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = SenseAudioASRError(f"HTTP {exc.code}: {json.dumps(payload, ensure_ascii=False)}")
            break
        except urllib.error.URLError as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            last_error = SenseAudioASRError(f"Network error: {exc}")
            break

    if last_error:
        raise last_error
    raise SenseAudioASRError("Unknown ASR request failure.")
