#!/usr/bin/env python3
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, Optional


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


class SenseAudioError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        raw_body: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.raw_body = raw_body
        self.trace_id = trace_id


@dataclass
class TTSResult:
    audio_bytes: bytes
    trace_id: Optional[str]
    extra_info: Optional[Dict[str, object]]
    model_used: Optional[str] = None


def _parse_sse_audio(response, *, model_used: Optional[str] = None) -> TTSResult:
    audio_parts = []
    trace_id = None
    extra_info = None

    for raw_line in response:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line or not line.startswith("data: "):
            continue

        payload = json.loads(line[6:])
        base_resp = payload.get("base_resp") or {}
        status_code = base_resp.get("status_code")
        status_msg = base_resp.get("status_msg")
        if status_code not in (None, 0):
            raise SenseAudioError(
                status_msg or "SenseAudio returned an error.",
                status_code=status_code,
                trace_id=payload.get("trace_id"),
                raw_body=json.dumps(payload, ensure_ascii=False),
            )

        trace_id = payload.get("trace_id") or trace_id
        if payload.get("extra_info"):
            extra_info = payload["extra_info"]

        data = payload.get("data") or {}
        audio_hex = data.get("audio")
        if audio_hex:
            audio_parts.append(bytes.fromhex(audio_hex))

    audio_bytes = b"".join(audio_parts)
    if not audio_bytes:
        raise SenseAudioError("No audio data returned.", trace_id=trace_id)
    return TTSResult(audio_bytes=audio_bytes, trace_id=trace_id, extra_info=extra_info, model_used=model_used)


def _parse_json_audio(body: str, *, model_used: Optional[str] = None) -> TTSResult:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SenseAudioError("Failed to parse non-stream TTS response.", raw_body=body) from exc

    base_resp = payload.get("base_resp") or {}
    status_code = base_resp.get("status_code")
    status_msg = base_resp.get("status_msg")
    trace_id = payload.get("trace_id")
    if status_code not in (None, 0):
        raise SenseAudioError(
            status_msg or "SenseAudio returned an error.",
            status_code=status_code,
            trace_id=trace_id,
            raw_body=body,
        )

    data = payload.get("data") or {}
    audio_hex = data.get("audio")
    if not audio_hex:
        raise SenseAudioError("No audio data returned.", trace_id=trace_id, raw_body=body)
    return TTSResult(
        audio_bytes=bytes.fromhex(audio_hex),
        trace_id=trace_id,
        extra_info=payload.get("extra_info"),
        model_used=model_used,
    )


def _candidate_models(requested_model: str, voice_id: str) -> list[str]:
    if requested_model != "auto":
        return [requested_model]
    if voice_id.startswith("vc-"):
        return ["SenseAudio-TTS-1.5", "SenseAudio-TTS-1.0"]
    return ["SenseAudio-TTS-1.0"]


def _supports_capability_error(exc: SenseAudioError) -> bool:
    haystack = f"{exc} {exc.raw_body or ''}".lower()
    return "model does not support this capability" in haystack


def synthesize(
    *,
    api_key: str,
    text: str,
    voice_id: str,
    audio_format: str = "mp3",
    sample_rate: int = 32000,
    model: str = "auto",
    speed: float = 1.0,
    volume: float = 1.0,
    pitch: int = 0,
    stream: bool = False,
    timeout: int = 120,
) -> TTSResult:
    last_exc: Optional[SenseAudioError] = None
    for candidate_model in _candidate_models(model, voice_id):
        payload = {
            "model": candidate_model,
            "text": text,
            "stream": stream,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": volume,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": audio_format,
                "sample_rate": sample_rate,
            },
        }

        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Codex-SenseAudio-OpenClaw-Voice/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if stream:
                    return _parse_sse_audio(response, model_used=candidate_model)
                body = response.read().decode("utf-8", "replace")
                return _parse_json_audio(body, model_used=candidate_model)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            error = SenseAudioError(
                f"HTTP {exc.code}: {body}",
                status_code=exc.code,
                raw_body=body,
            )
            last_exc = error
            if voice_id.startswith("vc-") and _supports_capability_error(error):
                continue
            raise error from exc
        except urllib.error.URLError as exc:
            raise SenseAudioError(f"Network error: {exc}") from exc
    raise last_exc or SenseAudioError("No compatible TTS model found.")
