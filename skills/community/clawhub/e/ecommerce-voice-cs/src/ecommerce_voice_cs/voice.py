from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests


class VoiceCloneService:
    """SenseAudio adapter for public TTS and an optional private clone endpoint."""

    API_DOCS_URL = "https://senseaudio.cn/docs/api-key"
    TTS_DOCS_URL = "https://senseaudio.cn/docs/text_to_speech_api"
    TTS_API_URL = "https://api.senseaudio.cn/v1/t2a_v2"
    MODEL_NAME = "SenseAudio-TTS-1.0"
    SUPPORTED_AUDIO_FORMATS = {"mp3", "wav", "pcm", "flac"}
    SUPPORTED_SAMPLE_RATES = {8000, 16000, 22050, 24000, 32000, 44100}
    SUPPORTED_CHANNELS = {1, 2}
    MP3_BITRATES = {32000, 64000, 128000, 256000}

    def __init__(
        self,
        *,
        api_key: str | None = None,
        clone_api_url: str | None = None,
    ) -> None:
        self.api_key = (api_key or os.getenv("SENSEAUDIO_API_KEY", "")).strip() or None
        self.clone_api_url = (
            clone_api_url or os.getenv("SENSEAUDIO_CLONE_API_URL", "")
        ).strip() or None

    def has_api_key(self) -> bool:
        return bool(self.api_key or os.getenv("SENSEAUDIO_API_KEY", "").strip())

    def set_api_key(self, api_key: str) -> None:
        normalized = api_key.strip()
        if not normalized:
            raise ValueError("API key cannot be empty")
        self.api_key = normalized

    def set_clone_api_url(self, clone_api_url: str) -> None:
        normalized = clone_api_url.strip()
        if not normalized:
            raise ValueError("clone_api_url cannot be empty")
        self.clone_api_url = normalized

    def missing_api_key_message(self) -> str:
        return (
            "请先提供 SenseAudio API Key，或设置环境变量 SENSEAUDIO_API_KEY。"
            f"文档：{self.API_DOCS_URL}"
        )

    def upload_sample(self, file_path: str) -> str:
        if not self.has_api_key():
            raise RuntimeError(self.missing_api_key_message())
        if not self.clone_api_url:
            raise RuntimeError(
                "当前未配置音色克隆接口。请直接提供已有 voice_id，"
                "或设置私有克隆端点 SENSEAUDIO_CLONE_API_URL。"
            )

        sample_path = Path(file_path)
        if not sample_path.exists():
            raise FileNotFoundError(f"Audio sample not found: {sample_path}")
        if sample_path.suffix.lower() not in {".wav", ".mp3"}:
            raise ValueError("Only .wav and .mp3 samples are supported")

        raise NotImplementedError(
            "请根据你的私有音色克隆接口协议实现 upload_sample()。"
            "当前公开文档未提供可直接接入的样本上传克隆 API。"
        )

    def synthesize_to_file(
        self,
        *,
        text: str,
        voice_handle: str,
        output_dir: str | Path,
        file_ext: str = ".wav",
        sample_rate: int = 32000,
        bitrate: int = 128000,
        channel: int = 1,
        speed: float = 1,
        volume: float = 1,
        pitch: float = 0,
    ) -> Path:
        if not self.has_api_key():
            raise RuntimeError(self.missing_api_key_message())
        if not text.strip():
            raise ValueError("TTS input text cannot be empty")
        if not voice_handle:
            raise ValueError("voice_handle is required for TTS")

        destination_dir = Path(output_dir)
        destination_dir.mkdir(parents=True, exist_ok=True)

        safe_ext = file_ext if file_ext.startswith(".") else f".{file_ext}"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = destination_dir / f"cs_reply_{timestamp}{safe_ext}"

        audio_bytes = self._request_tts_audio(
            text=text,
            voice_handle=voice_handle,
            audio_format=safe_ext.lstrip("."),
            sample_rate=sample_rate,
            bitrate=bitrate,
            channel=channel,
            speed=speed,
            volume=volume,
            pitch=pitch,
        )
        output_file.write_bytes(audio_bytes)
        return output_file

    def _request_tts_audio(
        self,
        *,
        text: str,
        voice_handle: str,
        audio_format: str,
        sample_rate: int,
        bitrate: int,
        channel: int,
        speed: float,
        volume: float,
        pitch: float,
    ) -> bytes:
        if not self.api_key:
            self.api_key = os.getenv("SENSEAUDIO_API_KEY", "").strip() or None

        normalized_format = self._normalize_audio_format(audio_format)
        payload = self._build_tts_payload(
            text=text,
            voice_handle=voice_handle,
            audio_format=normalized_format,
            sample_rate=sample_rate,
            bitrate=bitrate,
            channel=channel,
            speed=speed,
            volume=volume,
            pitch=pitch,
        )

        response = self._post_tts(payload)
        if response.status_code >= 500:
            fallback_payload = self._build_minimal_tts_payload(
                text=text,
                voice_handle=voice_handle,
            )
            if fallback_payload != payload:
                fallback_response = self._post_tts(fallback_payload)
                if fallback_response.status_code < 500:
                    return self._parse_tts_response(fallback_response, fallback_payload)
                response = fallback_response

        return self._parse_tts_response(response, payload)

    def _build_tts_payload(
        self,
        *,
        text: str,
        voice_handle: str,
        audio_format: str,
        sample_rate: int,
        bitrate: int,
        channel: int,
        speed: float,
        volume: float,
        pitch: float,
    ) -> dict[str, object]:
        self._validate_voice_handle(voice_handle)
        self._validate_text(text)
        self._validate_numeric_param("speed", speed, min_value=0.5, max_value=2.0)
        self._validate_numeric_param("volume", volume, min_value=0.0, max_value=10.0)
        self._validate_numeric_param("pitch", pitch, min_value=-12, max_value=12)
        self._validate_sample_rate(sample_rate)
        self._validate_channel(channel)

        voice_setting: dict[str, object] = {"voice_id": voice_handle.strip()}
        if speed != 1:
            voice_setting["speed"] = speed
        if volume != 1:
            voice_setting["vol"] = volume
        if int(pitch) != 0:
            voice_setting["pitch"] = int(pitch)

        audio_setting: dict[str, object] = {}
        if audio_format != "mp3":
            audio_setting["format"] = audio_format
        if sample_rate != 32000:
            audio_setting["sample_rate"] = sample_rate
        if channel != 1:
            audio_setting["channel"] = channel
        if audio_format == "mp3" and bitrate != 128000:
            self._validate_bitrate(bitrate)
            audio_setting["bitrate"] = bitrate
        elif audio_format == "mp3":
            self._validate_bitrate(bitrate)
        elif bitrate != 128000:
            # Non-mp3 requests should not forward bitrate because the API only accepts it for mp3.
            pass

        payload: dict[str, object] = {
            "model": self.MODEL_NAME,
            "text": text.strip(),
            "stream": False,
            "voice_setting": voice_setting,
        }
        if audio_setting:
            payload["audio_setting"] = audio_setting
        return payload

    def _build_minimal_tts_payload(
        self,
        *,
        text: str,
        voice_handle: str,
    ) -> dict[str, object]:
        self._validate_voice_handle(voice_handle)
        self._validate_text(text)
        return {
            "model": self.MODEL_NAME,
            "text": text.strip(),
            "stream": False,
            "voice_setting": {"voice_id": voice_handle.strip()},
        }

    def _post_tts(self, payload: dict[str, object]) -> requests.Response:
        try:
            return requests.post(
                self.TTS_API_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=60,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"SenseAudio TTS request failed: {exc}") from exc

    def _parse_tts_response(
        self, response: requests.Response, payload: dict[str, object]
    ) -> bytes:
        response_bytes = response.content
        content_type = response.headers.get("Content-Type", "")
        body_text = response_bytes.decode("utf-8", errors="replace") if response_bytes else ""

        if response.status_code >= 400:
            detail = self._extract_error_detail(body_text)
            raise RuntimeError(
                f"SenseAudio TTS request failed with HTTP {response.status_code}: "
                f"{detail}. request={json.dumps(payload, ensure_ascii=False)}"
            )

        if not response_bytes:
            raise RuntimeError("SenseAudio TTS returned an empty response body")
        if "json" not in content_type.lower():
            raise RuntimeError(
                "SenseAudio TTS returned unexpected content type "
                f"{content_type}. body={body_text[:300]}"
            )

        try:
            parsed = json.loads(body_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "SenseAudio TTS returned invalid JSON: "
                f"{body_text[:300]}"
            ) from exc

        base_resp = parsed.get("base_resp", {})
        status_code = base_resp.get("status_code")
        if status_code not in (0, None):
            status_msg = base_resp.get("status_msg", "unknown error")
            raise RuntimeError(
                "SenseAudio TTS failed: "
                f"status_code={status_code}, status_msg={status_msg}, response={parsed}"
            )

        audio_hex = parsed.get("data", {}).get("audio")
        if not audio_hex:
            raise RuntimeError(f"SenseAudio TTS returned no audio field: {parsed}")

        try:
            return bytes.fromhex(audio_hex)
        except ValueError as exc:
            raise RuntimeError(
                "SenseAudio TTS returned a non-hex audio payload"
            ) from exc

    @classmethod
    def _normalize_audio_format(cls, audio_format: str) -> str:
        normalized = audio_format.strip().lower().lstrip(".")
        if normalized not in cls.SUPPORTED_AUDIO_FORMATS:
            supported = ", ".join(sorted(cls.SUPPORTED_AUDIO_FORMATS))
            raise ValueError(
                f"Unsupported audio format '{audio_format}'. Supported values: {supported}"
            )
        return normalized

    @staticmethod
    def _validate_voice_handle(voice_handle: str) -> None:
        if not voice_handle.strip():
            raise ValueError("voice_handle is required for TTS")

    @staticmethod
    def _validate_text(text: str) -> None:
        normalized = text.strip()
        if not normalized:
            raise ValueError("TTS input text cannot be empty")
        if len(normalized) > 10000:
            raise ValueError("TTS input text exceeds 10000 characters")

    @classmethod
    def _validate_sample_rate(cls, sample_rate: int) -> None:
        if sample_rate not in cls.SUPPORTED_SAMPLE_RATES:
            allowed = ", ".join(str(item) for item in sorted(cls.SUPPORTED_SAMPLE_RATES))
            raise ValueError(
                f"Unsupported sample_rate '{sample_rate}'. Supported values: {allowed}"
            )

    @classmethod
    def _validate_channel(cls, channel: int) -> None:
        if channel not in cls.SUPPORTED_CHANNELS:
            allowed = ", ".join(str(item) for item in sorted(cls.SUPPORTED_CHANNELS))
            raise ValueError(
                f"Unsupported channel '{channel}'. Supported values: {allowed}"
            )

    @classmethod
    def _validate_bitrate(cls, bitrate: int) -> None:
        if bitrate not in cls.MP3_BITRATES:
            allowed = ", ".join(str(item) for item in sorted(cls.MP3_BITRATES))
            raise ValueError(
                f"Unsupported mp3 bitrate '{bitrate}'. Supported values: {allowed}"
            )

    @staticmethod
    def _validate_numeric_param(
        name: str,
        value: float,
        *,
        min_value: float,
        max_value: float,
    ) -> None:
        if not (min_value <= value <= max_value):
            raise ValueError(
                f"Unsupported {name} '{value}'. Supported range: [{min_value}, {max_value}]"
            )

    @staticmethod
    def _extract_error_detail(body_text: str) -> str:
        if not body_text:
            return "empty response body"
        try:
            parsed = json.loads(body_text)
        except json.JSONDecodeError:
            return body_text[:300]

        if isinstance(parsed, dict):
            base_resp = parsed.get("base_resp")
            if isinstance(base_resp, dict):
                status_msg = base_resp.get("status_msg")
                status_code = base_resp.get("status_code")
                if status_msg or status_code is not None:
                    return f"status_code={status_code}, status_msg={status_msg}"
            message = parsed.get("message") or parsed.get("msg") or parsed.get("error")
            if message:
                return str(message)
        return body_text[:300]

    @staticmethod
    def is_probably_url(value: str) -> bool:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)
