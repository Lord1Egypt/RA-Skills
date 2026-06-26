# FILE_META
# INPUT:  server_url, secret_key, adapter_name, scope_type, scope_id, zip_bytes
# OUTPUT: server response dict (parsed JSON) or {"error": ...}
# POS:    skill lib harness — HTTP client for POST /upload-harness
# MISSION: Multipart upload of a harness zip with scope metadata.

"""Upload a harness bundle to the ClawTraces server's /upload-harness endpoint."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from lib.auth import _format_connection_error, get_ssl_context, handle_401
    from lib.version import default_headers, exit_if_upgrade_required
except ImportError:
    from ..auth import _format_connection_error, get_ssl_context, handle_401  # type: ignore
    from ..version import default_headers, exit_if_upgrade_required  # type: ignore

_BOUNDARY = "----ClawTracesHarnessBoundary9876543210"


def _build_multipart(
    adapter_name: str,
    scope_type: str,
    scope_id: str,
    zip_bytes: bytes,
    filename: str,
) -> bytes:
    parts: list[bytes] = []

    for name, value in [
        ("adapter_name", adapter_name),
        ("scope_type", scope_type),
        ("scope_id", scope_id),
    ]:
        parts.append(
            (
                f"--{_BOUNDARY}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{value}\r\n"
            ).encode("utf-8")
        )

    parts.append(
        (
            f"--{_BOUNDARY}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/zip\r\n\r\n"
        ).encode("utf-8")
    )
    parts.append(zip_bytes)
    parts.append(b"\r\n")
    parts.append(f"--{_BOUNDARY}--\r\n".encode("utf-8"))

    return b"".join(parts)


def upload_harness(
    server_url: str,
    secret_key: str,
    adapter_name: str,
    scope_type: str,
    scope_id: str,
    zip_bytes: bytes,
) -> dict:
    """POST a harness zip to the server."""
    filename = f"harness-{adapter_name}-{scope_type}-{scope_id}.zip"
    body = _build_multipart(adapter_name, scope_type, scope_id, zip_bytes, filename)

    req = Request(
        f"{server_url}/upload-harness",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={_BOUNDARY}",
            **default_headers(secret_key),
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=60, context=get_ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 401:
            handle_401()
            return {"error": "unauthorized"}
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body_text)
            exit_if_upgrade_required(parsed)
            parsed.setdefault("error", f"HTTP {e.code}")
            return parsed
        except (json.JSONDecodeError, ValueError):
            return {"error": f"HTTP {e.code}", "detail": body_text}
    except URLError as e:
        return {"error": _format_connection_error(e.reason)}
