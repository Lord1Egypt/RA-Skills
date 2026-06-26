#!/usr/bin/env python3
"""
Herdsman Python client helpers.

Only uses the Python standard library so other agents can copy or reuse it
without adding dependencies.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Dict, Generator, Iterable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "http://127.0.0.1:8080"
DEFAULT_TIMEOUT = 300


class HerdsmanAPIError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        error: Optional[dict] = None,
        body: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error = error or {}
        self.body = body or ""

    def to_dict(self) -> dict:
        return {
            "message": str(self),
            "status_code": self.status_code,
            "error": self.error,
            "body": self.body,
        }


def normalize_base_url(base_url: str) -> str:
    return (base_url or DEFAULT_BASE_URL).rstrip("/")


def join_api_url(base_url: str, path: str) -> str:
    base = normalize_base_url(base_url) + "/"
    return urljoin(base, path.lstrip("/"))


def env_api_key() -> str:
    return os.environ.get("HERDSMAN_API_KEY", "").strip()


def ensure_parent(output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def write_bytes(output_path: str, data: bytes) -> str:
    ensure_parent(output_path)
    with open(output_path, "wb") as handle:
        handle.write(data)
    return os.path.abspath(output_path)


def decode_base64_payload(raw_value: str) -> bytes:
    value = (raw_value or "").strip()
    if not value:
        raise ValueError("empty base64 payload")
    if "," in value and "base64" in value.split(",", 1)[0]:
        value = value.split(",", 1)[1]
    return base64.b64decode(value)


def file_to_data_url(file_path: str, default_mime_type: str = "application/octet-stream") -> str:
    mime_type = mimetypes.guess_type(file_path)[0] or default_mime_type
    with open(file_path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def prepare_media_input(value: str, *, default_mime_type: str) -> str:
    raw_value = (value or "").strip()
    if not raw_value:
        raise ValueError("empty media input")
    if raw_value.startswith(("http://", "https://", "data:")):
        return raw_value

    candidate = Path(raw_value)
    if candidate.exists() and candidate.is_file():
        return file_to_data_url(str(candidate), default_mime_type=default_mime_type)
    return raw_value


class HerdsmanClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = normalize_base_url(base_url)
        self.api_key = (api_key or env_api_key()).strip()
        self.timeout = timeout

    def _headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = "Bearer " + self.api_key
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: Optional[dict] = None,
        timeout: Optional[int] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> bytes:
        body = None
        headers = self._headers(extra_headers)
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers.setdefault("Content-Type", "application/json")

        request = Request(
            join_api_url(self.base_url, path),
            data=body,
            headers=headers,
            method=method.upper(),
        )
        actual_timeout = timeout if timeout is not None else self.timeout
        try:
            with urlopen(request, timeout=actual_timeout) as response:
                return response.read()
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            parsed_error = None
            try:
                parsed_error = json.loads(raw)
            except json.JSONDecodeError:
                parsed_error = None
            message = raw
            if isinstance(parsed_error, dict):
                message = parsed_error.get("error", {}).get("message", raw)
            raise HerdsmanAPIError(
                message or f"http error {exc.code}",
                status_code=exc.code,
                error=parsed_error.get("error", {}) if isinstance(parsed_error, dict) else None,
                body=raw,
            ) from exc
        except URLError as exc:
            raise HerdsmanAPIError(f"request failed: {exc}") from exc

    def request_json(
        self,
        method: str,
        path: str,
        *,
        payload: Optional[dict] = None,
        timeout: Optional[int] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> dict:
        raw = self._request(
            method,
            path,
            payload=payload,
            timeout=timeout,
            extra_headers=extra_headers,
        )
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def request_bytes(
        self,
        method: str,
        path: str,
        *,
        payload: Optional[dict] = None,
        timeout: Optional[int] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> bytes:
        return self._request(
            method,
            path,
            payload=payload,
            timeout=timeout,
            extra_headers=extra_headers,
        )

    def stream_sse_json(
        self,
        path: str,
        *,
        payload: dict,
        timeout: Optional[int] = None,
    ) -> Generator[dict, None, None]:
        headers = self._headers(
            {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            }
        )
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = Request(join_api_url(self.base_url, path), data=data, headers=headers, method="POST")
        actual_timeout = timeout if timeout is not None else self.timeout

        try:
            with urlopen(request, timeout=actual_timeout) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="replace").strip()
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        yield json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise HerdsmanAPIError(raw or f"http error {exc.code}", status_code=exc.code, body=raw) from exc
        except URLError as exc:
            raise HerdsmanAPIError(f"request failed: {exc}") from exc

    def download_to_file(
        self,
        url: str,
        output_path: str,
        *,
        timeout: Optional[int] = None,
    ) -> str:
        request = Request(url, headers=self._headers())
        actual_timeout = timeout if timeout is not None else self.timeout
        try:
            with urlopen(request, timeout=actual_timeout) as response:
                data = response.read()
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise HerdsmanAPIError(raw or f"http error {exc.code}", status_code=exc.code, body=raw) from exc
        except URLError as exc:
            raise HerdsmanAPIError(f"download failed: {exc}") from exc
        return write_bytes(output_path, data)

    def save_base64_file(self, raw_value: str, output_path: str) -> str:
        return write_bytes(output_path, decode_base64_payload(raw_value))

    # ── Model discovery ──────────────────────────────────────────────

    def list_models(self) -> dict:
        return self.request_json("GET", "/v1/models", timeout=20)

    def find_model(self, model_id: str) -> Optional[dict]:
        result = self.list_models()
        for item in result.get("data", []):
            if item.get("id") == model_id:
                return item
        return None

    # ── Chat ─────────────────────────────────────────────────────────

    def chat_completions(
        self,
        *,
        model: str,
        messages: Iterable[dict],
        **extra: object,
    ) -> dict:
        payload = {"model": model, "messages": list(messages)}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/chat/completions", payload=payload)

    # ── Embeddings ───────────────────────────────────────────────────

    def embeddings(
        self,
        *,
        model: str,
        input_text: str | list[str],
        **extra: object,
    ) -> dict:
        payload = {"model": model, "input": input_text}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/embeddings", payload=payload)

    # ── Rerank ───────────────────────────────────────────────────────

    def rerank(
        self,
        *,
        model: str,
        query: str,
        documents: list[str],
        **extra: object,
    ) -> dict:
        payload = {"model": model, "query": query, "documents": documents}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/rerank", payload=payload)

    # ── Image ────────────────────────────────────────────────────────

    def create_image(
        self,
        *,
        model: str,
        prompt: str,
        **extra: object,
    ) -> dict:
        payload = {"model": model, "prompt": prompt}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/images/generations", payload=payload, timeout=120)

    def edit_image(
        self,
        *,
        model: str,
        image: str,
        prompt: str,
        **extra: object,
    ) -> dict:
        payload = {"model": model, "image": image, "prompt": prompt}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/images/edits", payload=payload, timeout=120)

    def img2img(
        self,
        *,
        model: str,
        image: str,
        prompt: str,
        **extra: object,
    ) -> dict:
        payload = {"model": model, "image": image, "prompt": prompt}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/images/img2img", payload=payload, timeout=120)

    def image_cache_url(self, filename: str) -> str:
        """Return the full URL for a cached image file."""
        return join_api_url(self.base_url, f"/v1/images/cache/{filename}")

    # ── OCR ──────────────────────────────────────────────────────────

    def ocr(
        self,
        *,
        model: str,
        image_base64: str,
        **extra: object,
    ) -> dict:
        """Recognize text in an image using OCR.

        Args:
            model: OCR model ID, e.g. 'paddleocr-ppocrv5-server'.
            image_base64: Base64-encoded image data. Supports pure base64
                          or ``data:image/...;base64,...`` format.

        Returns:
            dict with ``text`` (full page text), ``lines`` (per-line results
            with text, score, box coordinates), ``image_width``,
            ``image_height``, and ``elapsed_ms``.
        """
        payload = {"model": model, "image_base64": image_base64}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/ocr", payload=payload, timeout=120)

    def ocr_image_file(
        self,
        *,
        model: str,
        image_path: str,
        **extra: object,
    ) -> dict:
        """Convenience: read a local image file, base64-encode it, and call ocr().

        Args:
            model: OCR model ID.
            image_path: Path to a local image file (PNG, JPG, etc.).

        Returns:
            Same as :meth:`ocr`.
        """
        image_base64 = file_to_data_url(image_path, default_mime_type="image/png")
        return self.ocr(model=model, image_base64=image_base64, **extra)

    # ── Audio ────────────────────────────────────────────────────────

    def transcribe_audio(
        self,
        *,
        model: str,
        audio: str,
        **extra: object,
    ) -> dict:
        payload = {"model": model, "audio": audio}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/audio/transcriptions", payload=payload, timeout=300)

    def audio_speech(
        self,
        *,
        model: str,
        input_text: str,
        **extra: object,
    ) -> dict:
        payload = {"model": model, "input": input_text}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/audio/speech", payload=payload, timeout=120)

    def audio_info(self, model: str) -> dict:
        """Query audio service capabilities for a model."""
        return self.request_json("GET", f"/v1/audio/info?model={model}", timeout=20)

    # ── Anthropic ────────────────────────────────────────────────────

    def anthropic_messages(
        self,
        *,
        model: str,
        messages: Iterable[dict],
        **extra: object,
    ) -> dict:
        payload = {"model": model, "messages": list(messages)}
        payload.update({key: value for key, value in extra.items() if value is not None})
        return self.request_json("POST", "/v1/anthropic/messages", payload=payload)