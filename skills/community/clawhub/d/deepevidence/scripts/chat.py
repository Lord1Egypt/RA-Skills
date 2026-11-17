#!/usr/bin/env python3
"""
DeepEvidence canonical public API chat helper.

stdout: medical answer content only.
stderr: stable error codes and operational metadata.
"""

import argparse
import json
import os
import socket
import sys
import time
from typing import Iterable, List, Optional, Tuple
from urllib import error as urllib_error
from urllib import request as urllib_request


BASE_URL = "https://deepevid.medsci.cn/api/v1"
CHAT_COMPLETIONS_URL = f"{BASE_URL}/chat/completions"
DEFAULT_MODEL = "DeepEvidence-V1"
DEFAULT_IMAGE_DETAIL = "auto"
DEFAULT_TIMEOUT_SECONDS = 60

TEMP_UNAVAILABLE_MSG = (
    "Temporarily unable to retrieve evidence-based results. "
    "Please try again later or consult a licensed clinician."
)


class DeepEvidenceError(Exception):
    def __init__(self, code: str, message: str, *, status: Optional[int] = None, request_id: Optional[str] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.request_id = request_id


def debug_enabled() -> bool:
    return os.environ.get("DEEPEVIDENCE_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}


def normalize_user_id(user: Optional[str]) -> Optional[str]:
    user = (user or os.environ.get("DEEPEVIDENCE_USER_ID") or "").strip()
    if not user:
        return None
    return user if user.startswith("skill_") else f"skill_{user}"


def build_user_content(query: str, image_urls: Optional[List[str]] = None):
    if not image_urls:
        return query

    content = []
    if query:
        content.append({"type": "text", "text": query})
    for image_url in image_urls:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": DEFAULT_IMAGE_DETAIL,
                },
            }
        )
    return content


def build_request_body(
    *,
    query: str,
    model: str = DEFAULT_MODEL,
    user: Optional[str] = None,
    image_urls: Optional[List[str]] = None,
    stream: bool = False,
    include_usage: bool = False,
) -> dict:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": build_user_content(query, image_urls)}],
        "stream": stream,
    }

    normalized_user = normalize_user_id(user)
    if normalized_user:
        body["user"] = normalized_user
    if stream and include_usage:
        body["stream_options"] = {"include_usage": True}
    return body


def require_api_key() -> str:
    api_key = os.environ.get("DEEPEVIDENCE_API_KEY", "").strip()
    if not api_key:
        raise DeepEvidenceError(
            "DE_CONFIG_ERROR",
            "DEEPEVIDENCE_API_KEY is not set. Apply for an API key at: "
            "https://deepevid.medsci.cn/platform/api-keys",
        )
    return api_key


def make_request(body: dict, api_key: str) -> urllib_request.Request:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    return urllib_request.Request(
        CHAT_COMPLETIONS_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )


def map_http_error(status: int) -> str:
    if status == 400:
        return "DE_BAD_REQUEST"
    if status == 401:
        return "DE_AUTH_ERROR"
    if status == 403:
        return "DE_PERMISSION_ERROR"
    if status == 429:
        return "DE_RATE_LIMIT"
    if status >= 500:
        return "DE_UPSTREAM_ERROR"
    return "DE_UPSTREAM_ERROR"


def request_id_from_headers(headers) -> Optional[str]:
    for name in ("x-request-id", "X-Request-Id", "request-id", "Request-Id"):
        value = headers.get(name)
        if value:
            return value
    return None


def load_json_response(response) -> Tuple[dict, Optional[str]]:
    request_id = request_id_from_headers(response.headers)
    try:
        payload = json.loads(response.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "Invalid JSON response from DeepEvidence.", request_id=request_id) from exc
    if not isinstance(payload, dict):
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "Invalid response shape from DeepEvidence.", request_id=request_id)
    return payload, request_id


def call_api(body: dict, *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> Tuple[dict, Optional[str], float]:
    api_key = require_api_key()
    request = make_request(body, api_key)
    started = time.monotonic()
    try:
        with urllib_request.urlopen(request, timeout=timeout) as response:
            payload, request_id = load_json_response(response)
    except urllib_error.HTTPError as exc:
        request_id = request_id_from_headers(exc.headers)
        raise DeepEvidenceError(map_http_error(exc.code), f"DeepEvidence API returned HTTP {exc.code}.", status=exc.code, request_id=request_id) from exc
    except (urllib_error.URLError, TimeoutError, socket.timeout) as exc:
        raise DeepEvidenceError("DE_TIMEOUT", TEMP_UNAVAILABLE_MSG) from exc
    return payload, request_id, time.monotonic() - started


def extract_answer(payload: dict) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "DeepEvidence response did not include choices.")
    first = choices[0]
    if not isinstance(first, dict):
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "DeepEvidence response choice was invalid.")
    message = first.get("message")
    if not isinstance(message, dict):
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "DeepEvidence response did not include a message.")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "DeepEvidence response content was empty.")
    return content


def iter_stream_events(raw: bytes) -> Iterable[dict]:
    for line in raw.decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if not data or data == "[DONE]":
            continue
        try:
            event = json.loads(data)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            yield event


def call_stream(body: dict, *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> Tuple[Optional[str], float]:
    api_key = require_api_key()
    request = make_request(body, api_key)
    started = time.monotonic()
    try:
        with urllib_request.urlopen(request, timeout=timeout) as response:
            request_id = request_id_from_headers(response.headers)
            raw = response.read()
    except urllib_error.HTTPError as exc:
        request_id = request_id_from_headers(exc.headers)
        raise DeepEvidenceError(map_http_error(exc.code), f"DeepEvidence API returned HTTP {exc.code}.", status=exc.code, request_id=request_id) from exc
    except (urllib_error.URLError, TimeoutError, socket.timeout) as exc:
        raise DeepEvidenceError("DE_TIMEOUT", TEMP_UNAVAILABLE_MSG) from exc

    emitted = False
    for event in iter_stream_events(raw):
        usage = event.get("usage")
        if usage:
            print_usage(usage, prefix="stream_")
        choices = event.get("choices")
        if isinstance(choices, list) and choices:
            delta = choices[0].get("delta") if isinstance(choices[0], dict) else None
            content = delta.get("content") if isinstance(delta, dict) else None
            if content:
                emitted = True
                print(content, end="", flush=True)
    if emitted:
        print()
    else:
        raise DeepEvidenceError("DE_INVALID_RESPONSE", "DeepEvidence stream did not include content.", request_id=request_id)
    return request_id, time.monotonic() - started


def print_usage(usage, *, prefix: str = "") -> None:
    if not isinstance(usage, dict):
        return
    prompt = usage.get("prompt_tokens")
    completion = usage.get("completion_tokens")
    total = usage.get("total_tokens")
    parts = []
    if prompt is not None:
        parts.append(f"{prefix}prompt_tokens={prompt}")
    if completion is not None:
        parts.append(f"{prefix}completion_tokens={completion}")
    if total is not None:
        parts.append(f"{prefix}total_tokens={total}")
    if parts:
        print(" ".join(parts), file=sys.stderr)


def print_metadata(*, request_id: Optional[str], latency: float, usage=None) -> None:
    parts = [f"latency_ms={int(latency * 1000)}"]
    if request_id:
        parts.append(f"request_id={request_id}")
    print(" ".join(parts), file=sys.stderr)
    print_usage(usage)


def print_error(exc: DeepEvidenceError) -> None:
    parts = [exc.code]
    if exc.status is not None:
        parts.append(f"status={exc.status}")
    if exc.request_id:
        parts.append(f"request_id={exc.request_id}")
    print(" ".join(parts) + f": {exc.message}", file=sys.stderr)
    if debug_enabled() and exc.__cause__ is not None:
        print(f"debug_exception={type(exc.__cause__).__name__}", file=sys.stderr)


def chat(
    query: str,
    *,
    model: str = DEFAULT_MODEL,
    user: Optional[str] = None,
    image_urls: Optional[List[str]] = None,
    stream: bool = False,
    include_usage: bool = False,
):
    body = build_request_body(
        query=query,
        model=model,
        user=user,
        image_urls=image_urls,
        stream=stream,
        include_usage=include_usage,
    )
    if stream:
        request_id, latency = call_stream(body)
        print_metadata(request_id=request_id, latency=latency)
        return None

    payload, request_id, latency = call_api(body)
    answer = extract_answer(payload)
    print(answer)
    print_metadata(request_id=request_id, latency=latency, usage=payload.get("usage"))
    return payload


def parse_args(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="DeepEvidence canonical public API chat helper")
    parser.add_argument("positional_query", nargs="?", help="Medical evidence question to ask")
    parser.add_argument("--query", help="Medical evidence question to ask")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID. Default: {DEFAULT_MODEL}")
    parser.add_argument("--user", default=None, help="Stable opaque end-user ID. Defaults to DEEPEVIDENCE_USER_ID.")
    parser.add_argument(
        "--image-url",
        action="append",
        dest="image_urls",
        help="HTTPS image URL or data:image/... base64 URL. Repeat for multiple images.",
    )
    parser.add_argument("--stream", action="store_true", help="Use streaming response output")
    parser.add_argument("--include-usage", action="store_true", help="When streaming, request usage chunks")
    args = parser.parse_args(argv)
    args.query = args.query or args.positional_query
    if not args.query:
        parser.error("missing required --query")
    return args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        chat(
            args.query,
            model=args.model,
            user=args.user,
            image_urls=args.image_urls,
            stream=args.stream,
            include_usage=args.include_usage,
        )
    except DeepEvidenceError as exc:
        print_error(exc)
        return 2 if exc.code == "DE_CONFIG_ERROR" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
