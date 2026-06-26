from __future__ import annotations

import gzip
import shutil
import subprocess
import time
import urllib.parse
import urllib.request
import zlib
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError

from .constants import AUDIBLE_BLOCK_MARKERS, HTTP_USER_AGENT
from .shared import normalize_space


class AudibleBlockedError(RuntimeError):
    pass


class AudibleFetchError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        backend: str | None = None,
        http_status: int | None = None,
        final_url: str | None = None,
        reason_code: str | None = None,
        attempts: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.backend = backend
        self.http_status = http_status
        self.final_url = final_url
        self.reason_code = reason_code
        self.attempts = list(attempts or [])


AUDIBLE_FETCH_HEADERS = {
    "User-Agent": HTTP_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
SUPPORTED_AUDIBLE_FETCH_BACKENDS = {"auto", "python", "curl"}
CURL_RECOVERABLE_HTTP_STATUSES = {403, 429, 500, 502, 503, 504}
CURL_META_MARKER = "__AUDIBLE_GOODREADS_DEAL_SCOUT_CURL_META__"
ALLOWED_AUDIBLE_HOSTS = {
    "www.audible.com",
    "www.audible.co.uk",
    "www.audible.de",
    "www.audible.ca",
    "www.audible.com.au",
}
ALLOWED_AUDIBLE_PATH_PREFIXES = ("/dailydeal", "/pd/", "/search")


class AudibleFetchResult:
    def __init__(
        self,
        text: str,
        final_url: str,
        *,
        backend: str,
        attempts: list[dict[str, Any]] | None = None,
        warnings: list[str] | None = None,
    ) -> None:
        self.text = text
        self.final_url = final_url
        self.backend = backend
        self.attempts = list(attempts or [])
        self.warnings = list(warnings or [])

    def __iter__(self):
        yield self.text
        yield self.final_url


def curl_available(curl_bin: str = "curl") -> bool:
    return bool(shutil.which(curl_bin) if "/" not in curl_bin else Path(curl_bin).exists())


def validate_audible_fetch_url(url: str, *, allow_unsafe_url: bool = False) -> str:
    normalized_url = normalize_space(url)
    if allow_unsafe_url:
        return normalized_url
    parsed = urllib.parse.urlparse(normalized_url)
    host = normalize_space(parsed.netloc).lower()
    path = parsed.path or "/"
    if parsed.scheme != "https" or host not in ALLOWED_AUDIBLE_HOSTS:
        raise AudibleFetchError(
            f"Refusing to fetch non-Audible URL: {normalized_url}",
            reason_code="error_unsafe_audible_url",
            final_url=normalized_url,
        )
    if not any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in ALLOWED_AUDIBLE_PATH_PREFIXES):
        raise AudibleFetchError(
            f"Refusing to fetch unsupported Audible path: {normalized_url}",
            reason_code="error_unsupported_audible_path",
            final_url=normalized_url,
        )
    return normalized_url


def decode_response_bytes(raw: bytes, content_encoding: str) -> str:
    encoding = normalize_space(content_encoding).lower()
    if encoding == "gzip":
        return gzip.decompress(raw).decode("utf-8", "ignore")
    if encoding == "deflate":
        try:
            return zlib.decompress(raw).decode("utf-8", "ignore")
        except zlib.error:
            return zlib.decompress(raw, -zlib.MAX_WBITS).decode("utf-8", "ignore")
    return raw.decode("utf-8", "ignore")


def _fetch_reason_code(backend: str, http_status: int | None, exc: Exception | None = None) -> str:
    if backend == "python" and http_status == 503:
        return "http_503_python_fetch_rejected"
    if http_status:
        return f"http_{http_status}_{backend}_fetch_failed"
    if isinstance(exc, URLError):
        return f"url_error_{backend}_fetch_failed"
    return f"{backend}_fetch_failed"


def _attempt_payload(
    *,
    backend: str,
    ok: bool,
    url: str,
    final_url: str | None = None,
    http_status: int | None = None,
    reason_code: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"backend": backend, "ok": ok, "url": url}
    if final_url:
        payload["finalUrl"] = final_url
    if http_status is not None:
        payload["httpStatus"] = http_status
    if reason_code:
        payload["reasonCode"] = reason_code
    if error:
        payload["error"] = error
    return payload


def _raise_blocked(
    message: str,
    *,
    backend: str,
    url: str,
    final_url: str | None = None,
    http_status: int | None = None,
    reason_code: str = "audible_block_marker",
) -> None:
    attempt = _attempt_payload(
        backend=backend,
        ok=False,
        url=url,
        final_url=final_url,
        http_status=http_status,
        reason_code=reason_code,
        error=message,
    )
    blocked = AudibleBlockedError(message)
    blocked.backend = backend  # type: ignore[attr-defined]
    blocked.http_status = http_status  # type: ignore[attr-defined]
    blocked.final_url = final_url  # type: ignore[attr-defined]
    blocked.reason_code = reason_code  # type: ignore[attr-defined]
    blocked.attempts = [attempt]  # type: ignore[attr-defined]
    raise blocked


def _validate_audible_response(text: str, url: str, *, backend: str, final_url: str | None = None) -> None:
    lowered = text.lower()
    if any(marker in lowered for marker in AUDIBLE_BLOCK_MARKERS):
        _raise_blocked(
            f"Audible blocked the request for {url}.",
            backend=backend,
            url=url,
            final_url=final_url,
        )


def _fetch_python_once(url: str) -> AudibleFetchResult:
    request = urllib.request.Request(url, headers=AUDIBLE_FETCH_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            text = decode_response_bytes(raw, str(response.headers.get("Content-Encoding") or ""))
            final_url = str(response.geturl() or url)
            _validate_audible_response(text, url, backend="python", final_url=final_url)
            return AudibleFetchResult(
                text,
                final_url,
                backend="python",
                attempts=[
                    _attempt_payload(
                        backend="python",
                        ok=True,
                        url=url,
                        final_url=final_url,
                        http_status=int(getattr(response, "status", 200) or 200),
                    )
                ],
            )
    except HTTPError as exc:
        reason_code = _fetch_reason_code("python", exc.code, exc)
        if exc.code in {403, 429}:
            _raise_blocked(
                f"Audible request blocked with HTTP {exc.code}.",
                backend="python",
                url=url,
                final_url=str(exc.geturl() or url),
                http_status=exc.code,
                reason_code=reason_code,
            )
        raise AudibleFetchError(
            f"Audible request failed for {url}: {exc}",
            backend="python",
            http_status=exc.code,
            final_url=str(exc.geturl() or url),
            reason_code=reason_code,
            attempts=[
                _attempt_payload(
                    backend="python",
                    ok=False,
                    url=url,
                    final_url=str(exc.geturl() or url),
                    http_status=exc.code,
                    reason_code=reason_code,
                    error=str(exc),
                )
            ],
        ) from exc
    except URLError as exc:
        reason_code = _fetch_reason_code("python", None, exc)
        raise AudibleFetchError(
            f"Audible request failed for {url}: {exc}",
            backend="python",
            reason_code=reason_code,
            attempts=[
                _attempt_payload(
                    backend="python",
                    ok=False,
                    url=url,
                    reason_code=reason_code,
                    error=str(exc),
                )
            ],
        ) from exc


def _curl_command(url: str, curl_bin: str) -> list[str]:
    command = [
        curl_bin,
        "--location",
        "--compressed",
        "--silent",
        "--show-error",
        "--max-time",
        "30",
        "--connect-timeout",
        "10",
    ]
    for key, value in AUDIBLE_FETCH_HEADERS.items():
        command.extend(["-H", f"{key}: {value}"])
    command.extend(["-w", f"\n{CURL_META_MARKER}%{{http_code}}\t%{{url_effective}}", url])
    return command


def _run_curl(command: list[str], url: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired as exc:
        raise AudibleFetchError(
            f"Audible curl fallback timed out for {url}.",
            backend="curl",
            reason_code="curl_timeout",
            attempts=[
                _attempt_payload(
                    backend="curl",
                    ok=False,
                    url=url,
                    reason_code="curl_timeout",
                    error=str(exc),
                )
            ],
        ) from exc
    except OSError as exc:
        raise AudibleFetchError(
            f"Audible curl fallback failed for {url}: {exc}",
            backend="curl",
            reason_code="curl_process_failed",
            attempts=[
                _attempt_payload(
                    backend="curl",
                    ok=False,
                    url=url,
                    reason_code="curl_process_failed",
                    error=str(exc),
                )
            ],
        ) from exc


def _split_curl_output(stdout: str, url: str) -> tuple[str, str, int | None]:
    body, marker, meta = stdout.rpartition(CURL_META_MARKER)
    if not marker:
        return stdout, url, None
    raw_status, _, raw_final_url = meta.strip().partition("\t")
    try:
        http_status = int(raw_status)
    except ValueError:
        http_status = None
    return body, normalize_space(raw_final_url) or url, http_status


def _fetch_curl_once(url: str, *, curl_bin: str = "curl") -> AudibleFetchResult:
    if not curl_available(curl_bin):
        raise AudibleFetchError(
            f"Audible curl fallback is unavailable because '{curl_bin}' was not found.",
            backend="curl",
            reason_code="curl_unavailable",
            attempts=[
                _attempt_payload(
                    backend="curl",
                    ok=False,
                    url=url,
                    reason_code="curl_unavailable",
                    error=f"{curl_bin} not found",
                )
            ],
        )
    proc = _run_curl(_curl_command(url, curl_bin), url)
    body, final_url, http_status = _split_curl_output(proc.stdout or "", url)
    if proc.returncode != 0:
        reason_code = "curl_process_failed"
        error = (proc.stderr or "").strip() or f"curl exited {proc.returncode}"
        raise AudibleFetchError(
            f"Audible curl fallback failed for {url}: {error}",
            backend="curl",
            http_status=http_status,
            final_url=final_url,
            reason_code=reason_code,
            attempts=[
                _attempt_payload(
                    backend="curl",
                    ok=False,
                    url=url,
                    final_url=final_url,
                    http_status=http_status,
                    reason_code=reason_code,
                    error=error,
                )
            ],
        )
    if http_status is not None and http_status >= 400:
        reason_code = _fetch_reason_code("curl", http_status)
        if http_status in {403, 429}:
            _raise_blocked(
                f"Audible curl fallback blocked with HTTP {http_status}.",
                backend="curl",
                url=url,
                final_url=final_url,
                http_status=http_status,
                reason_code=reason_code,
            )
        raise AudibleFetchError(
            f"Audible curl fallback failed for {url}: HTTP {http_status}",
            backend="curl",
            http_status=http_status,
            final_url=final_url,
            reason_code=reason_code,
            attempts=[
                _attempt_payload(
                    backend="curl",
                    ok=False,
                    url=url,
                    final_url=final_url,
                    http_status=http_status,
                    reason_code=reason_code,
                    error=f"HTTP {http_status}",
                )
            ],
        )
    _validate_audible_response(body, url, backend="curl", final_url=final_url)
    return AudibleFetchResult(
        body,
        final_url,
        backend="curl",
        attempts=[
            _attempt_payload(
                backend="curl",
                ok=True,
                url=url,
                final_url=final_url,
                http_status=http_status,
            )
        ],
    )


def _fetch_with_retries(
    url: str,
    *,
    backend: str,
    retries: int,
    backoff_seconds: float,
    curl_bin: str,
) -> AudibleFetchResult:
    last_error: Exception | None = None
    attempts: list[dict[str, Any]] = []
    for attempt_index in range(max(0, retries) + 1):
        try:
            result = _fetch_python_once(url) if backend == "python" else _fetch_curl_once(url, curl_bin=curl_bin)
            result.attempts = [*attempts, *result.attempts]
            return result
        except (AudibleFetchError, AudibleBlockedError) as exc:
            last_error = exc
            attempts.extend(list(getattr(exc, "attempts", []) or []))
            if attempt_index >= max(0, retries):
                break
            if backoff_seconds > 0:
                time.sleep(backoff_seconds * (attempt_index + 1))
    if isinstance(last_error, AudibleBlockedError):
        last_error.attempts = attempts  # type: ignore[attr-defined]
        raise last_error
    if isinstance(last_error, AudibleFetchError):
        last_error.attempts = attempts
        raise last_error
    raise AudibleFetchError(f"Audible request failed for {url}: {last_error}", backend=backend, attempts=attempts)


def _can_try_curl_after(error: Exception) -> bool:
    http_status = getattr(error, "http_status", None)
    if http_status in CURL_RECOVERABLE_HTTP_STATUSES:
        return True
    reason_code = normalize_space(str(getattr(error, "reason_code", "") or ""))
    return reason_code.startswith("url_error_") or reason_code in {"python_fetch_failed"}


def fetch_text_with_final_url(
    url: str,
    *,
    retries: int = 2,
    backoff_seconds: float = 1.0,
    backend: str = "auto",
    curl_bin: str = "curl",
    allow_unsafe_url: bool = False,
) -> AudibleFetchResult:
    url = validate_audible_fetch_url(url, allow_unsafe_url=allow_unsafe_url)
    normalized_backend = normalize_space(backend).lower() or "auto"
    if normalized_backend not in SUPPORTED_AUDIBLE_FETCH_BACKENDS:
        raise ValueError(
            f"Unsupported Audible fetch backend '{backend}'. Use one of: auto, curl, python."
        )
    if normalized_backend in {"python", "curl"}:
        return _fetch_with_retries(
            url,
            backend=normalized_backend,
            retries=retries,
            backoff_seconds=backoff_seconds,
            curl_bin=curl_bin,
        )
    try:
        return _fetch_with_retries(
            url,
            backend="python",
            retries=retries,
            backoff_seconds=backoff_seconds,
            curl_bin=curl_bin,
        )
    except (AudibleFetchError, AudibleBlockedError) as python_error:
        if not _can_try_curl_after(python_error):
            raise
        python_attempts = list(getattr(python_error, "attempts", []) or [])
        if not curl_available(curl_bin):
            raise AudibleFetchError(
                f"{python_error}; curl fallback unavailable because '{curl_bin}' was not found.",
                backend="auto",
                http_status=getattr(python_error, "http_status", None),
                final_url=getattr(python_error, "final_url", None),
                reason_code=getattr(python_error, "reason_code", None) or "curl_unavailable",
                attempts=[
                    *python_attempts,
                    _attempt_payload(
                        backend="curl",
                        ok=False,
                        url=url,
                        reason_code="curl_unavailable",
                        error=f"{curl_bin} not found",
                    ),
                ],
            ) from python_error
        try:
            curl_result = _fetch_with_retries(
                url,
                backend="curl",
                retries=0,
                backoff_seconds=0,
                curl_bin=curl_bin,
            )
        except (AudibleFetchError, AudibleBlockedError) as curl_error:
            curl_error.attempts = [*python_attempts, *list(getattr(curl_error, "attempts", []) or [])]  # type: ignore[attr-defined]
            raise curl_error from python_error
        http_status = getattr(python_error, "http_status", None)
        reason_code = getattr(python_error, "reason_code", None) or _fetch_reason_code("python", http_status)
        curl_result.attempts = [*python_attempts, *curl_result.attempts]
        curl_result.warnings.append(
            "Python Audible fetch failed"
            + (f" with HTTP {http_status}" if http_status else "")
            + "; recovered with curl fallback."
        )
        if reason_code:
            curl_result.warnings.append(f"Fetch fallback reason: {reason_code}.")
        return curl_result
