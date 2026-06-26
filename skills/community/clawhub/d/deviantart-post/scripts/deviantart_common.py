from __future__ import annotations

import gzip
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DEFAULT_OPENCLAW_DIR = Path.home() / ".openclaw"
APP_CREDENTIALS_PATH = Path(os.environ.get("DEVIANTART_APP_CREDENTIALS", DEFAULT_OPENCLAW_DIR / "deviantart-app-credentials.json"))
TOKEN_PATH = Path(os.environ.get("DEVIANTART_TOKEN_PATH", DEFAULT_OPENCLAW_DIR / "deviantart-token.json"))
API_BASE = "https://www.deviantart.com/api/v1/oauth2"
TOKEN_URL = "https://www.deviantart.com/oauth2/token"
USER_AGENT = "OpenClaw-DeviantArt-Post/0.2"


class DeviantArtError(Exception):
    pass


def _decode_bytes(raw: bytes, encoding_header: str = "") -> str:
    encoding = (encoding_header or "").lower()
    if "gzip" in encoding:
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", errors="replace")


def read_response_text(resp) -> str:
    raw = resp.read()
    return _decode_bytes(raw, resp.headers.get("Content-Encoding") or "")


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise DeviantArtError(f"Required file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_app_credentials() -> Dict[str, Any]:
    data = load_json(APP_CREDENTIALS_PATH)
    if not data.get("client_id"):
        raise DeviantArtError("client_id missing in app credentials file")
    if not data.get("redirect_uri"):
        raise DeviantArtError("redirect_uri missing in app credentials file")
    return data


def load_token(required: bool = True) -> Optional[Dict[str, Any]]:
    if not TOKEN_PATH.exists():
        if required:
            raise DeviantArtError(
                f"Token file not found: {TOKEN_PATH}. Run deviantart_auth.py first."
            )
        return None
    return load_json(TOKEN_PATH)


def token_is_expired(token: Dict[str, Any], skew_seconds: int = 60) -> bool:
    expires_at = token.get("expires_at")
    if not expires_at:
        return True
    return time.time() >= float(expires_at) - skew_seconds


def _json_request(url: str, *, method: str = "GET", data: Optional[bytes] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    req_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
    }
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = read_response_text(resp)
    except urllib.error.HTTPError as e:
        body = _decode_bytes(e.read(), e.headers.get("Content-Encoding") or "")
        raise DeviantArtError(f"HTTP {e.code} from {url}: {body}") from e
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as e:
        raise DeviantArtError(f"Non-JSON response from {url}: {body}") from e
    _raise_if_api_error(parsed)
    return parsed


def _form_urlencode_post(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    encoded = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
    return _json_request(
        url,
        method="POST",
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def _raise_if_api_error(payload: Dict[str, Any]) -> None:
    if isinstance(payload, dict):
        if payload.get("error"):
            detail = payload.get("error_description") or payload.get("error_message") or payload.get("error")
            raise DeviantArtError(str(detail))
        if payload.get("status") == "error":
            detail = payload.get("error") or payload.get("error_description") or payload
            raise DeviantArtError(f"API error payload: {detail}")


def refresh_access_token_if_needed() -> Dict[str, Any]:
    app = load_app_credentials()
    token = load_token(required=True)
    if token and not token_is_expired(token):
        return token

    refresh_token = token.get("refresh_token") if token else None
    if not refresh_token:
        raise DeviantArtError("No refresh token available. Run deviantart_auth.py again.")

    payload: Dict[str, Any] = {
        "grant_type": "refresh_token",
        "client_id": str(app["client_id"]),
        "refresh_token": refresh_token,
    }
    if app.get("client_secret"):
        payload["client_secret"] = app["client_secret"]

    refreshed = _form_urlencode_post(TOKEN_URL, payload)
    refreshed["refresh_token"] = refreshed.get("refresh_token", refresh_token)
    refreshed["obtained_at"] = time.time()
    refreshed["expires_at"] = time.time() + int(refreshed.get("expires_in", 3600))
    refreshed["scope"] = refreshed.get("scope", token.get("scope"))
    save_json(TOKEN_PATH, refreshed)
    return refreshed


def get_bearer_token() -> str:
    token = refresh_access_token_if_needed()
    access_token = token.get("access_token")
    if not access_token:
        raise DeviantArtError("No access_token available after refresh")
    return str(access_token)


def _encode_multipart(fields: List[Tuple[str, str]], files: List[Tuple[str, Path]]) -> Tuple[bytes, str]:
    boundary = f"----OpenClawDA{int(time.time() * 1000)}"
    body = bytearray()

    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    for field_name, file_path in files:
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {mime}\r\n\r\n".encode())
        body.extend(file_path.read_bytes())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return bytes(body), boundary


def api_post_form(endpoint: str, form: Dict[str, Any]) -> Dict[str, Any]:
    token = get_bearer_token()
    clean_form: Dict[str, Any] = {}
    for key, value in dict(form).items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)) and not value:
            continue
        if value == "":
            continue
        clean_form[key] = value
    clean_form["access_token"] = token
    return _form_urlencode_post(f"{API_BASE}/{endpoint.lstrip('/')}" , clean_form)


def api_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    token = get_bearer_token()
    clean_params: List[Tuple[str, str]] = []
    for key, value in (params or {}).items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                clean_params.append((key, str(item)))
        else:
            clean_params.append((key, str(value)))
    query = urllib.parse.urlencode(clean_params, doseq=True)
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    if query:
        url = f"{url}?{query}"
    return _json_request(url, headers={"Authorization": f"Bearer {token}"})


def list_gallery_folders() -> List[Dict[str, Any]]:
    payload = api_get("gallery/folders")
    results = payload.get("results") or payload.get("folders") or []
    if not isinstance(results, list):
        raise DeviantArtError(f"Unexpected gallery folder payload: {payload}")
    return results


def resolve_gallery_names(names: Iterable[str]) -> List[str]:
    requested = [name.strip() for name in names if name and name.strip()]
    if not requested:
        return []
    folders = list_gallery_folders()
    by_name: Dict[str, List[Dict[str, Any]]] = {}
    for folder in folders:
        candidates = [
            folder.get("name"),
            folder.get("title"),
            folder.get("foldername"),
        ]
        for candidate in candidates:
            if candidate:
                by_name.setdefault(str(candidate).strip().lower(), []).append(folder)
    resolved: List[str] = []
    for wanted in requested:
        matches = by_name.get(wanted.lower(), [])
        if not matches:
            available = sorted({k for k in by_name.keys() if k})
            preview = ", ".join(available[:20])
            raise DeviantArtError(
                f"Gallery folder not found: {wanted}. Available names include: {preview}"
            )
        if len(matches) > 1:
            ids = [str(m.get('folderid') or m.get('uuid') or m.get('id')) for m in matches]
            raise DeviantArtError(f"Gallery folder name is ambiguous: {wanted}. Matching IDs: {', '.join(ids)}")
        folder = matches[0]
        folder_id = folder.get("folderid") or folder.get("uuid") or folder.get("id")
        if not folder_id:
            raise DeviantArtError(f"Gallery folder has no usable ID: {folder}")
        resolved.append(str(folder_id))
    return resolved


def api_post_multipart(endpoint: str, fields: Dict[str, Any], file_fields: Iterable[Tuple[str, Path]]) -> Dict[str, Any]:
    token = get_bearer_token()
    flat_fields: List[Tuple[str, str]] = [("access_token", token)]
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            for item in value:
                flat_fields.append((key, str(item)))
        else:
            flat_fields.append((key, str(value)))

    files_list = list(file_fields)
    payload, boundary = _encode_multipart(flat_fields, files_list)
    req = urllib.request.Request(
        f"{API_BASE}/{endpoint.lstrip('/')}",
        data=payload,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = read_response_text(resp)
    except urllib.error.HTTPError as e:
        body = _decode_bytes(e.read(), e.headers.get("Content-Encoding") or "")
        raise DeviantArtError(f"HTTP {e.code} from upload: {body}") from e

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as e:
        raise DeviantArtError(f"Non-JSON response from upload: {body}") from e

    _raise_if_api_error(parsed)
    return parsed


def normalize_bool(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return "true"
    if text in {"0", "false", "no", "n", "off"}:
        return "false"
    raise DeviantArtError(f"Invalid boolean value: {value}")


def sanitize_tags(tags: Iterable[str]) -> List[str]:
    cleaned: List[str] = []
    for tag in tags:
        normalized = tag.strip().replace("-", "_").replace(" ", "_")
        normalized = "".join(ch for ch in normalized if ch.isalnum() or ch == "_")
        if normalized:
            cleaned.append(normalized)
    return cleaned
