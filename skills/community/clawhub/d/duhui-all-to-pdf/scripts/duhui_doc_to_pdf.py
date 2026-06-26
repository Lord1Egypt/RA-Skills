#!/usr/bin/env python3
"""Convert one local document to PDF through the Duhui async API."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import http.client
import json
import mimetypes
import os
import shutil
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from email.utils import formatdate
from pathlib import Path
from typing import Any
from uuid import uuid4

APP_CODE_ENV = "DUHUI_ALI_APPCODE"
ALIYUN_MARKET_URL = "https://market.aliyun.com/detail/cmapi00044564"

OSS_BUCKET_HOST = "fmtmp.oss-cn-shanghai.aliyuncs.com"
OSS_BUCKET_NAME = "fmtmp"
OSS_OBJECT_PREFIX = "up/"
OSS_CREDENTIALS_URL = "https://file.duhuitech.com/k/tmp_up.json"

CONVERT_ASYNC_URL = "https://doc2pdf.market.alicloudapi.com/v2/convert_async"
QUERY_URL = "https://api.duhuitech.com/q"

POLL_INTERVAL_SECONDS = 2
POLL_TIMEOUT_SECONDS = 60 * 60
HTTP_TIMEOUT_SECONDS = 60
DOWNLOAD_TIMEOUT_SECONDS = 300
VERIFIED_SSL_CONTEXT = ssl.create_default_context()

RESERVED_EXTRA_PARAMS = {"callbackurl", "input", "type"}


class SkillError(Exception):
    """Structured error for consistent JSON output."""

    def __init__(self, stage: str, reason: str, token: str | None = None) -> None:
        super().__init__(reason)
        self.stage = stage
        self.reason = reason
        self.token = token


@dataclass(frozen=True)
class OssCredentials:
    access_key_id: str
    access_key_secret: str


_CACHED_OSS_CREDENTIALS: OssCredentials | None = None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert one local document to PDF through Duhui's async API.",
    )
    parser.add_argument("input_path", help="Path to the local source file")
    parser.add_argument("--output", help="Destination path for the converted PDF")
    parser.add_argument("--type", dest="source_type", help="Explicit source file type")
    parser.add_argument(
        "--extra-params",
        help="JSON object with additional v2 convert_async parameters",
    )
    return parser.parse_args(argv)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def emit_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False), flush=True)


def fail(stage: str, reason: str, token: str | None = None) -> int:
    emit_json(
        {
            "status": "error",
            "stage": stage,
            "token": token,
            "reason": reason,
        }
    )
    return 1


def build_missing_appcode_reason() -> str:
    return (
        f"Environment variable {APP_CODE_ENV} is required. "
        f"Get AppCode from Alibaba Cloud Marketplace: {ALIYUN_MARKET_URL}. "
        f"Ensure your agent or execution environment injects {APP_CODE_ENV} before "
        "running this script. This skill does not prescribe how the secret is stored, "
        "retrieved, or persisted."
    )


def resolve_input_path(raw_path: str) -> Path:
    input_path = Path(raw_path).expanduser().resolve()
    if not input_path.exists():
        raise SkillError("validation", f"Input file does not exist: {input_path}")
    if not input_path.is_file():
        raise SkillError("validation", f"Input path is not a file: {input_path}")
    return input_path


def resolve_output_path(input_path: Path, raw_output: str | None) -> Path:
    if raw_output:
        output_path = Path(raw_output).expanduser()
        if not output_path.is_absolute():
            output_path = (Path.cwd() / output_path).resolve()
        else:
            output_path = output_path.resolve()
    else:
        output_path = input_path.with_suffix(".pdf")
        # Avoid clobbering the source when the input is already a PDF.
        if output_path == input_path:
            output_path = input_path.with_name(f"{input_path.stem}.converted.pdf")

    if output_path == input_path:
        raise SkillError("validation", f"Output path cannot be the same as input: {output_path}")
    if output_path.exists() and not output_path.is_file():
        raise SkillError("validation", f"Output path is not a file: {output_path}")
    return output_path


def parse_extra_params(raw_params: str | None) -> dict[str, Any]:
    if raw_params is None:
        return {}
    try:
        parsed = json.loads(raw_params)
    except json.JSONDecodeError as exc:
        raise SkillError(
            "validation",
            f"Invalid JSON for --extra-params: {exc.msg}",
        ) from exc
    if not isinstance(parsed, dict):
        raise SkillError("validation", "--extra-params must decode to a JSON object")

    forbidden = sorted(RESERVED_EXTRA_PARAMS.intersection(parsed))
    if forbidden:
        raise SkillError(
            "validation",
            "--extra-params cannot override reserved fields: "
            + ", ".join(forbidden),
        )
    return parsed


def normalize_source_type(raw_type: str) -> str:
    source_type = raw_type.strip().lower()
    if not source_type:
        raise SkillError("validation", "Source type cannot be empty")
    if any(char.isspace() for char in source_type):
        raise SkillError("validation", f"Source type cannot contain whitespace: {raw_type!r}")
    return source_type


def resolve_source_type(input_path: Path, raw_type: str | None) -> str:
    if raw_type is not None:
        return normalize_source_type(raw_type)

    suffix = input_path.suffix.lower().lstrip(".")
    if not suffix:
        raise SkillError(
            "validation",
            "Could not infer source type from file suffix. Use --type explicitly.",
        )
    return normalize_source_type(suffix)


def build_object_key(input_path: Path) -> str:
    suffix = input_path.suffix.lower()
    return f"{OSS_OBJECT_PREFIX}{uuid4()}{suffix}"


def build_object_url(object_key: str) -> str:
    encoded_key = urllib.parse.quote(object_key, safe="/")
    return f"https://{OSS_BUCKET_HOST}/{encoded_key}"


def cache_oss_credentials(credentials: OssCredentials) -> OssCredentials:
    global _CACHED_OSS_CREDENTIALS
    _CACHED_OSS_CREDENTIALS = credentials
    return credentials


def parse_oss_credentials(payload: dict[str, Any]) -> OssCredentials:
    access_key_id = payload.get("key")
    access_key_secret = payload.get("secret")

    if not isinstance(access_key_id, str) or not access_key_id.strip():
        raise SkillError(
            "credentials",
            "Credential JSON must include a non-empty string field: key",
        )
    if not isinstance(access_key_secret, str) or not access_key_secret.strip():
        raise SkillError(
            "credentials",
            "Credential JSON must include a non-empty string field: secret",
        )

    return OssCredentials(
        access_key_id=access_key_id.strip(),
        access_key_secret=access_key_secret.strip(),
    )


def fetch_oss_credentials_from_remote() -> OssCredentials:
    log(f"[oss-auth] fetching temporary OSS upload credentials from {OSS_CREDENTIALS_URL}")
    payload = request_json(OSS_CREDENTIALS_URL, "credentials")
    return cache_oss_credentials(parse_oss_credentials(payload))


def resolve_oss_credentials(*, force_refresh: bool = False) -> OssCredentials:
    if not force_refresh and _CACHED_OSS_CREDENTIALS is not None:
        return _CACHED_OSS_CREDENTIALS
    return fetch_oss_credentials_from_remote()


def build_oss_authorization(
    method: str,
    object_key: str,
    *,
    credentials: OssCredentials,
    date: str,
    content_type: str = "",
    content_md5: str = "",
) -> str:
    canonical_resource = f"/{OSS_BUCKET_NAME}/{object_key}"
    string_to_sign = "\n".join([method, content_md5, content_type, date, canonical_resource])
    digest = hmac.new(
        credentials.access_key_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    signature = base64.b64encode(digest).decode("ascii")
    return f"OSS {credentials.access_key_id}:{signature}"


def decode_body(body: bytes, fallback_charset: str = "utf-8") -> str:
    try:
        return body.decode(fallback_charset)
    except UnicodeDecodeError:
        return body.decode("utf-8", errors="replace")


def request_json(
    url: str,
    stage: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = HTTP_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)

    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")

    request = urllib.request.Request(
        url,
        data=data,
        headers=request_headers,
        method=method.upper(),
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=VERIFIED_SSL_CONTEXT,
        ) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as exc:
        error_body = decode_body(exc.read())
        raise SkillError(stage, f"HTTP {exc.code}: {error_body or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise SkillError(stage, f"Request failed: {exc.reason}") from exc

    try:
        decoded = decode_body(body, charset)
        parsed = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise SkillError(stage, f"Invalid JSON response: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise SkillError(stage, "JSON response must be an object")
    return parsed


def send_oss_request_once(
    method: str,
    object_key: str,
    *,
    credentials: OssCredentials,
    stage: str,
    body_path: Path | None = None,
    content_type: str = "",
) -> tuple[int, str]:
    encoded_key = urllib.parse.quote(object_key, safe="/")
    path = f"/{encoded_key}"
    date = formatdate(usegmt=True)
    headers = {
        "Date": date,
        "Authorization": build_oss_authorization(
            method,
            object_key,
            credentials=credentials,
            date=date,
            content_type=content_type,
        ),
    }

    if content_type:
        headers["Content-Type"] = content_type
    if body_path is not None:
        headers["Content-Length"] = str(body_path.stat().st_size)

    connection = http.client.HTTPSConnection(
        OSS_BUCKET_HOST,
        timeout=HTTP_TIMEOUT_SECONDS,
        context=VERIFIED_SSL_CONTEXT,
    )

    try:
        connection.putrequest(method, path)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()

        if body_path is not None:
            with body_path.open("rb") as source_file:
                while True:
                    chunk = source_file.read(1024 * 1024)
                    if not chunk:
                        break
                    connection.send(chunk)

        response = connection.getresponse()
        body = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return response.status, decode_body(body, charset)
    except OSError as exc:
        raise SkillError(stage, f"OSS {method} request failed: {exc}") from exc
    finally:
        connection.close()


def send_oss_request(
    method: str,
    object_key: str,
    *,
    stage: str,
    body_path: Path | None = None,
    content_type: str = "",
) -> tuple[int, str]:
    credentials = resolve_oss_credentials()

    try:
        status, body = send_oss_request_once(
            method,
            object_key,
            credentials=credentials,
            stage=stage,
            body_path=body_path,
            content_type=content_type,
        )
    except SkillError:
        log("[oss-auth] OSS request failed; refreshing credentials and retrying once")
        refreshed_credentials = resolve_oss_credentials(force_refresh=True)
        return send_oss_request_once(
            method,
            object_key,
            credentials=refreshed_credentials,
            stage=stage,
            body_path=body_path,
            content_type=content_type,
        )

    if 200 <= status < 300:
        return status, body

    log(
        f"[oss-auth] OSS request returned status {status}; "
        "refreshing credentials and retrying once"
    )
    refreshed_credentials = resolve_oss_credentials(force_refresh=True)
    return send_oss_request_once(
        method,
        object_key,
        credentials=refreshed_credentials,
        stage=stage,
        body_path=body_path,
        content_type=content_type,
    )


def upload_source_and_get_url(input_path: Path, object_key: str) -> str:
    content_type = mimetypes.guess_type(str(input_path))[0] or "application/octet-stream"
    status, body = send_oss_request(
        "PUT",
        object_key,
        stage="upload",
        body_path=input_path,
        content_type=content_type,
    )
    if status < 200 or status >= 300:
        raise SkillError(
            "upload",
            f"OSS upload failed with status {status}: {body or 'empty response'}",
        )

    object_url = build_object_url(object_key)
    parsed_url = urllib.parse.urlparse(object_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise SkillError("upload", "OSS object URL is invalid")
    return object_url


def request_conversion(appcode: str, source_url: str, source_type: str, extra_params: dict[str, Any]) -> str:
    payload: dict[str, Any] = {
        "input": [source_url],
        "type": source_type,
    }
    payload.update(extra_params)

    response = request_json(
        CONVERT_ASYNC_URL,
        "request",
        method="POST",
        payload=payload,
        headers={"Authorization": f"APPCODE {appcode}"},
    )

    code = response.get("code")
    if code != 10000:
        raise SkillError(
            "request",
            f"Conversion request failed with code {code}: {response.get('msg') or 'unknown error'}",
        )

    result = response.get("result")
    if not isinstance(result, dict):
        raise SkillError("request", "Conversion request succeeded without a result object")

    token = result.get("token")
    if not isinstance(token, str) or not token:
        raise SkillError("request", "Conversion request succeeded without a token")
    return token


def poll_conversion(token: str) -> dict[str, Any]:
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    query_string = urllib.parse.urlencode({"token": token})

    while time.monotonic() <= deadline:
        response = request_json(f"{QUERY_URL}?{query_string}", "poll")

        code = response.get("code")
        if code != 10000:
            raise SkillError(
                "poll",
                f"Query failed with code {code}: {response.get('msg') or 'unknown error'}",
                token=token,
            )

        result = response.get("result")
        if not isinstance(result, dict):
            raise SkillError("poll", "Query response did not include a result object", token=token)

        status = result.get("status")
        if status == "Done":
            pdf_url = result.get("pdfurl")
            if not isinstance(pdf_url, str) or not pdf_url:
                raise SkillError("poll", "Conversion completed without pdfurl", token=token)
            return result

        if status == "Failed":
            reason = result.get("reason") or response.get("msg") or "Conversion failed"
            raise SkillError("poll", str(reason), token=token)

        if status in {"Pending", "Doing"}:
            progress = result.get("progress")
            if isinstance(progress, (int, float)):
                log(f"[poll] status={status} progress={progress:.0%}")
            else:
                log(f"[poll] status={status}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        raise SkillError("poll", f"Unknown conversion status: {status!r}", token=token)

    raise SkillError(
        "poll",
        f"Timed out after {POLL_TIMEOUT_SECONDS} seconds while waiting for conversion",
        token=token,
    )


def download_pdf(pdf_url: str, output_path: Path, token: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb",
            delete=False,
            dir=output_path.parent,
            prefix=f"{output_path.name}.",
            suffix=".part",
        ) as temp_file:
            temp_path = Path(temp_file.name)
            try:
                with urllib.request.urlopen(
                    pdf_url,
                    timeout=DOWNLOAD_TIMEOUT_SECONDS,
                    context=VERIFIED_SSL_CONTEXT,
                ) as response:
                    shutil.copyfileobj(response, temp_file)
            except urllib.error.HTTPError as exc:
                error_body = decode_body(exc.read())
                raise SkillError(
                    "download",
                    f"HTTP {exc.code}: {error_body or exc.reason}",
                    token=token,
                ) from exc
            except urllib.error.URLError as exc:
                raise SkillError("download", f"Download failed: {exc.reason}", token=token) from exc

        temp_path.replace(output_path)
        return output_path
    except SkillError:
        raise
    except OSError as exc:
        raise SkillError("download", f"Failed to write output PDF: {exc}", token=token) from exc
    finally:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def cleanup_object(object_key: str) -> None:
    try:
        status, body = send_oss_request("DELETE", object_key, stage="cleanup")
    except SkillError as exc:
        log(
            "[cleanup] warning: failed to delete OSS object "
            f"{object_key}: {exc.reason}; remote source file may remain temporarily"
        )
        return

    if status >= 400:
        log(
            "[cleanup] warning: failed to delete OSS object "
            f"{object_key}, status={status}, host={OSS_BUCKET_HOST}, "
            f"body={body!r}; remote source file may remain temporarily"
        )


def main(argv: list[str]) -> int:
    token: str | None = None
    object_key: str | None = None

    try:
        args = parse_args(argv)
        input_path = resolve_input_path(args.input_path)
        output_path = resolve_output_path(input_path, args.output)
        source_type = resolve_source_type(input_path, args.source_type)
        extra_params = parse_extra_params(args.extra_params)

        appcode = os.environ.get(APP_CODE_ENV, "").strip()
        if not appcode:
            raise SkillError(
                "validation",
                build_missing_appcode_reason(),
            )

        object_key = build_object_key(input_path)

        log(
            "[privacy] source file will be uploaded to temporary OSS storage in cn-shanghai; "
            "cleanup is best-effort"
        )
        log(f"[upload] uploading {input_path} to OSS as {object_key}")
        source_url = upload_source_and_get_url(input_path, object_key)

        log("[request] submitting convert_async request")
        token = request_conversion(appcode, source_url, source_type, extra_params)

        log(f"[poll] token={token}")
        result = poll_conversion(token)

        pdf_url = str(result["pdfurl"])
        log(f"[download] saving PDF to {output_path}")
        download_pdf(pdf_url, output_path, token)

        emit_json(
            {
                "status": "success",
                "token": token,
                "output_path": str(output_path),
                "pdf_url": pdf_url,
                "page_count": result.get("count"),
                "filesize": result.get("filesize"),
                "source_object_key": object_key,
            }
        )
        return 0
    except SkillError as exc:
        return fail(exc.stage, exc.reason, exc.token or token)
    finally:
        if object_key is not None:
            cleanup_object(object_key)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
