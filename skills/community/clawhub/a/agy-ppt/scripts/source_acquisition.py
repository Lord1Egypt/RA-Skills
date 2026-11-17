#!/usr/bin/env python3
"""Bounded public HTTP/HTTPS source acquisition (Phase 13.5).

This module fetches **one explicitly supplied public URL** and writes the
response body, unmodified, to a caller-chosen directory outside this
repository. It then hands that local payload to the existing Phase 13
ingestion layer:

    explicit public URL
      -> validation + bounded acquisition        <-- this module
      -> immutable downloaded bytes
      -> source digest (Phase 12 authority)
      -> repository-external local payload
      -> source_ingestion.ingest_source()
      -> normalized extraction blocks
      -> AGY semantic segmentation
      -> Phase 12 grounding

Two boundaries are kept strictly separate:

    acquisition != extraction
    extraction  != semantic understanding

Acquisition owns network behaviour and nothing else: it never parses the
payload, never decides its format, and never makes a semantic judgement. Format
detection stays in ``source_ingestion.py``, and every semantic decision stays
with AGY.

What this module deliberately does **not** do: crawl, follow links, mirror a
site, fetch embedded assets or iframes, render HTML, execute JavaScript, submit
forms, or authenticate. It sends exactly one ``GET`` per redirect hop for the
one URL it was given.

Security scope, stated plainly
------------------------------
This is a **user-run CLI guardrail** for fetching sources the operator chose on
purpose. It blocks the obvious foot-guns: non-HTTP schemes, credentials in the
URL, loopback/private/link-local/reserved destinations, unvalidated redirect
hops, unbounded responses, and disabled TLS verification.

It is **not** a hardened multi-tenant SSRF sandbox. Host validation resolves the
hostname and checks every returned address, but the subsequent HTTP connection
performs its own resolution, so a hostile DNS server that answers differently
between those two lookups could still steer the connection elsewhere. That
DNS-rebinding / TOCTOU window is a real residual limitation and is documented
rather than papered over. Do not put this behind an untrusted URL input in a
web service and assume it is safe.
"""

from __future__ import annotations

import ipaddress
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SCRIPTS_DIR = Path(__file__).resolve().parent
import sys  # noqa: E402

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# The one canonical source-fingerprint definition lives in Phase 12; remote
# acquisition delegates to it rather than inventing a URL/ETag-based identity.
from source_grounding import compute_source_digest  # noqa: E402

SCHEMA_VERSION = "1"

#: Only these schemes are ever eligible. HTTPS is preferred in documentation.
ALLOWED_SCHEMES = ("https", "http")

#: Hard cap on the response body. Enforced from Content-Length *and* while
#: streaming, because Content-Length is advisory and may be absent or wrong.
DEFAULT_MAX_BYTES = 25 * 1024 * 1024

#: Redirect hops followed before failing. Finite and small by design.
DEFAULT_MAX_REDIRECTS = 5

#: Socket timeout applied to connect and to each read, in seconds.
DEFAULT_TIMEOUT_SECONDS = 30.0

#: Transport compression is refused so the stored bytes are the source entity.
ACCEPT_ENCODING = "identity"

_ACCEPTABLE_CONTENT_ENCODINGS = ("", "identity", "none")

_SOURCE_ID_RE = re.compile(r"^src_[A-Za-z0-9._-]+$")

#: Suffixes that may be reused verbatim for the local payload filename.
_SAFE_SUFFIXES = (".pdf", ".md", ".markdown", ".mdown", ".txt", ".text", ".docx", ".html", ".htm")

#: Advisory Content-Type -> payload suffix. Never a format authority.
_CONTENT_TYPE_SUFFIX = {
    "application/pdf": ".pdf",
    "application/x-pdf": ".pdf",
    "text/markdown": ".md",
    "text/x-markdown": ".md",
    "text/plain": ".txt",
    "text/html": ".html",
    "application/xhtml+xml": ".html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}

# ---------------------------------------------------------------------------
# Error taxonomy
# ---------------------------------------------------------------------------
# Deliberately disjoint from the Phase 13 extraction codes and from the Phase 12
# grounding / image-worker codes: a network problem must never surface as a
# traceability, coverage, or image-generation failure.
ERROR_REMOTE_URL_INVALID = "REMOTE_URL_INVALID"
ERROR_REMOTE_SCHEME_UNSUPPORTED = "REMOTE_SCHEME_UNSUPPORTED"
ERROR_REMOTE_CREDENTIALS_UNSUPPORTED = "REMOTE_CREDENTIALS_UNSUPPORTED"
ERROR_REMOTE_HOST_BLOCKED = "REMOTE_HOST_BLOCKED"
ERROR_REMOTE_REDIRECT_BLOCKED = "REMOTE_REDIRECT_BLOCKED"
ERROR_REMOTE_TOO_MANY_REDIRECTS = "REMOTE_TOO_MANY_REDIRECTS"
ERROR_REMOTE_HTTP_ERROR = "REMOTE_HTTP_ERROR"
ERROR_REMOTE_TIMEOUT = "REMOTE_TIMEOUT"
ERROR_REMOTE_RESPONSE_TOO_LARGE = "REMOTE_RESPONSE_TOO_LARGE"
ERROR_REMOTE_CONTENT_ENCODING_UNSUPPORTED = "REMOTE_CONTENT_ENCODING_UNSUPPORTED"
ERROR_REMOTE_TLS_FAILED = "REMOTE_TLS_FAILED"
ERROR_REMOTE_ACQUISITION_FAILED = "REMOTE_ACQUISITION_FAILED"


class SourceAcquisitionError(Exception):
    """Base error carrying a stable error_code, matching project_state.py."""

    error_code = ERROR_REMOTE_ACQUISITION_FAILED

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        if error_code is not None:
            self.error_code = error_code


class RemoteUrlInvalid(SourceAcquisitionError):
    error_code = ERROR_REMOTE_URL_INVALID


class RemoteSchemeUnsupported(SourceAcquisitionError):
    error_code = ERROR_REMOTE_SCHEME_UNSUPPORTED


class RemoteCredentialsUnsupported(SourceAcquisitionError):
    error_code = ERROR_REMOTE_CREDENTIALS_UNSUPPORTED


class RemoteHostBlocked(SourceAcquisitionError):
    error_code = ERROR_REMOTE_HOST_BLOCKED


class RemoteRedirectBlocked(SourceAcquisitionError):
    error_code = ERROR_REMOTE_REDIRECT_BLOCKED


class RemoteTooManyRedirects(SourceAcquisitionError):
    error_code = ERROR_REMOTE_TOO_MANY_REDIRECTS


class RemoteHttpError(SourceAcquisitionError):
    error_code = ERROR_REMOTE_HTTP_ERROR

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class RemoteTimeout(SourceAcquisitionError):
    error_code = ERROR_REMOTE_TIMEOUT


class RemoteResponseTooLarge(SourceAcquisitionError):
    error_code = ERROR_REMOTE_RESPONSE_TOO_LARGE


class RemoteContentEncodingUnsupported(SourceAcquisitionError):
    error_code = ERROR_REMOTE_CONTENT_ENCODING_UNSUPPORTED


class RemoteTlsFailed(SourceAcquisitionError):
    error_code = ERROR_REMOTE_TLS_FAILED


# ---------------------------------------------------------------------------
# URL validation
# ---------------------------------------------------------------------------
_BLOCKED_HOSTNAMES = frozenset({"localhost", "localhost.localdomain", "ip6-localhost"})


def validate_remote_url(url: str) -> urllib.parse.SplitResult:
    """Validate scheme, credentials and host shape before any network access.

    Rejects anything that is not ``http``/``https``, anything carrying embedded
    credentials, and anything without a usable host. This runs before the first
    connection and again for every redirect hop.
    """
    if not isinstance(url, str) or not url.strip():
        raise RemoteUrlInvalid("url must be a non-empty string")

    try:
        parts = urllib.parse.urlsplit(url.strip())
    except ValueError as exc:
        raise RemoteUrlInvalid(f"url could not be parsed: {exc}")

    if not parts.scheme:
        raise RemoteSchemeUnsupported(
            f"url has no scheme; only {', '.join(ALLOWED_SCHEMES)} are supported"
        )
    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        raise RemoteSchemeUnsupported(
            f"scheme {parts.scheme!r} is not supported; only "
            f"{', '.join(ALLOWED_SCHEMES)} are eligible"
        )
    if parts.username or parts.password or "@" in (parts.netloc or ""):
        # Never echo the credential material back.
        raise RemoteCredentialsUnsupported(
            "url contains embedded credentials; Phase 13.5 acquires public "
            "unauthenticated sources only"
        )
    try:
        hostname = parts.hostname
    except ValueError as exc:
        raise RemoteUrlInvalid(f"url host could not be parsed: {exc}")
    if not hostname:
        raise RemoteUrlInvalid("url has no host")
    return parts


def _effective_ip(raw: str) -> ipaddress._BaseAddress:
    """Return the address to classify, unwrapping IPv4-mapped IPv6."""
    address = ipaddress.ip_address(raw)
    mapped = getattr(address, "ipv4_mapped", None)
    return mapped or address


def _address_is_blocked(address: ipaddress._BaseAddress) -> bool:
    return bool(
        address.is_loopback
        or address.is_private
        or address.is_link_local
        or address.is_multicast
        or address.is_unspecified
        or address.is_reserved
    )


def check_host_allowed(
    hostname: str,
    *,
    resolver: Callable[..., list[Any]] | None = None,
) -> list[str]:
    """Resolve a hostname and reject non-public destinations.

    Every address returned for the hostname must be public: if any one of them
    is loopback, private, link-local, multicast, unspecified or reserved, the
    whole host is refused. Failing closed matters because a name can resolve to
    several addresses, and cloud metadata endpoints live on link-local space.

    ``resolver`` exists as a test seam; it defaults to ``socket.getaddrinfo``.
    """
    name = (hostname or "").strip().rstrip(".").lower()
    if not name:
        raise RemoteUrlInvalid("url has no host")

    if name in _BLOCKED_HOSTNAMES or name.endswith(".localhost"):
        raise RemoteHostBlocked(f"host {name!r} is a local alias and is blocked")

    # A literal IP needs no DNS lookup.
    literal = name.strip("[]")
    try:
        address = _effective_ip(literal)
    except ValueError:
        pass
    else:
        if _address_is_blocked(address):
            raise RemoteHostBlocked(
                f"destination {literal} is not a public address "
                "(loopback/private/link-local/reserved) and is blocked"
            )
        return [str(address)]

    resolve = resolver or socket.getaddrinfo
    try:
        infos = resolve(name, None)
    except socket.gaierror as exc:
        raise RemoteHostBlocked(f"host {name!r} could not be resolved: {exc}")
    except OSError as exc:
        raise RemoteHostBlocked(f"host {name!r} could not be resolved: {exc}")

    resolved: list[str] = []
    for info in infos:
        sockaddr = info[4]
        if not sockaddr:
            continue
        raw = str(sockaddr[0])
        try:
            address = _effective_ip(raw)
        except ValueError:
            raise RemoteHostBlocked(f"host {name!r} resolved to an unusable address")
        if _address_is_blocked(address):
            raise RemoteHostBlocked(
                f"host {name!r} resolves to non-public address {raw} "
                "(loopback/private/link-local/reserved) and is blocked"
            )
        resolved.append(str(address))

    if not resolved:
        raise RemoteHostBlocked(f"host {name!r} did not resolve to any address")
    return resolved


# ---------------------------------------------------------------------------
# Payload naming
# ---------------------------------------------------------------------------
def safe_payload_name(source_id: str, *, url: str = "", content_type: str = "") -> str:
    """A payload filename derived only from trusted inputs.

    Built from the validated ``source_id`` plus a suffix chosen from a fixed
    allowlist. A ``Content-Disposition`` filename or a URL basename is **never**
    used to build the path -- both are attacker-controlled and are the classic
    route to path traversal. Content-Disposition may be recorded as metadata,
    but it never decides where bytes land.
    """
    if not _SOURCE_ID_RE.match(source_id or ""):
        raise RemoteUrlInvalid(
            f"invalid source_id: {source_id!r} (expected ^src_[A-Za-z0-9._-]+$)"
        )

    suffix = ""
    try:
        path = urllib.parse.urlsplit(url).path if url else ""
    except ValueError:
        path = ""
    candidate = Path(path).suffix.lower() if path else ""
    if candidate in _SAFE_SUFFIXES:
        suffix = candidate
    if not suffix:
        base_type = (content_type or "").split(";", 1)[0].strip().lower()
        suffix = _CONTENT_TYPE_SUFFIX.get(base_type, "")
    if not suffix:
        suffix = ".bin"

    # source_id is regex-validated, so it holds no separators; strip defensively
    # anyway so this function is safe in isolation.
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", source_id).lstrip(".") or "source"
    return f"{stem}{suffix}"


# ---------------------------------------------------------------------------
# Result contract
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AcquisitionResult:
    """Provenance for one acquired remote source."""

    schema_version: str
    source_id: str
    requested_url: str
    final_url: str
    content_type: str | None
    declared_content_length: int | None
    downloaded_bytes: int
    source_digest: str
    local_payload_path: str
    redirect_count: int
    retrieved_at: str
    content_disposition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_id": self.source_id,
            "requested_url": self.requested_url,
            "final_url": self.final_url,
            "content_type": self.content_type,
            "declared_content_length": self.declared_content_length,
            "downloaded_bytes": self.downloaded_bytes,
            "source_digest": self.source_digest,
            "local_payload_path": self.local_payload_path,
            "redirect_count": self.redirect_count,
            "retrieved_at": self.retrieved_at,
            "content_disposition": self.content_disposition,
        }


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------
class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Stop urllib from following redirects so each hop can be revalidated."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


def build_opener() -> urllib.request.OpenerDirector:
    """An opener that can *only* speak HTTP and HTTPS, with no ambient proxy.

    Deliberately assembled by hand rather than via
    ``urllib.request.build_opener()``, because the convenience builder installs
    ``FileHandler``, ``FTPHandler`` and ``DataHandler`` by default. Those give the
    opener the latent ability to open ``file:``, ``ftp:`` and ``data:`` URLs.
    URL validation already refuses those schemes, but defence in depth is worth
    more here than convenience: if the handlers are never installed, a validation
    gap cannot become a local-file read.

    No ``ProxyHandler`` is installed either, so ``http_proxy`` / ``https_proxy``
    in the environment cannot silently reroute acquisition to a different
    destination than the one the SSRF checks were applied to. Explicit proxy
    support is deliberately future work.

    TLS uses urllib's default context, which verifies certificates and hostnames.
    Nothing here weakens verification.
    """
    opener = urllib.request.OpenerDirector()
    for handler in (
        urllib.request.HTTPHandler(),
        urllib.request.HTTPSHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.HTTPErrorProcessor(),
        _NoRedirectHandler(),
        urllib.request.UnknownHandler(),
    ):
        opener.add_handler(handler)
    return opener


_REDIRECT_CODES = (301, 302, 303, 307, 308)


def _header(headers: Any, name: str) -> str | None:
    if headers is None:
        return None
    getter = getattr(headers, "get", None)
    return getter(name) if getter else None


# ---------------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------------
def acquire_remote_source(
    url: str,
    source_id: str,
    output_dir: str | Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    opener: Any | None = None,
    resolver: Callable[..., list[Any]] | None = None,
) -> AcquisitionResult:
    """Fetch one public URL into ``output_dir`` and describe what was fetched.

    Only ``GET`` is issued, once per redirect hop. Every hop is revalidated for
    scheme, credentials, hostname and resolved address, so a public URL that
    redirects to loopback, private space, link-local metadata or a non-HTTP
    scheme is refused. The body is streamed with a hard byte cap and written to
    a temporary file, then atomically renamed only after the status, size and
    digest are all settled; a failed attempt leaves no payload behind.

    Bytes are stored exactly as received: no newline conversion, no charset
    normalization, no decompression. ``retrieved_at`` is recorded for audit and
    deliberately has no influence on the source digest or on any identifier.

    ``opener`` and ``resolver`` are test seams so the deterministic suite never
    needs the internet.
    """
    if not _SOURCE_ID_RE.match(source_id or ""):
        raise RemoteUrlInvalid(
            f"invalid source_id: {source_id!r} (expected ^src_[A-Za-z0-9._-]+$)"
        )
    if max_bytes <= 0:
        raise RemoteUrlInvalid("max_bytes must be positive")
    if max_redirects < 0:
        raise RemoteUrlInvalid("max_redirects must not be negative")

    out_dir = Path(os.path.realpath(os.path.expanduser(str(output_dir))))
    out_dir.mkdir(parents=True, exist_ok=True)

    requested_url = url.strip()
    current_url = requested_url
    client = opener if opener is not None else build_opener()
    redirect_count = 0

    while True:
        parts = validate_remote_url(current_url)
        check_host_allowed(parts.hostname or "", resolver=resolver)

        request = urllib.request.Request(
            current_url,
            method="GET",
            headers={
                "Accept-Encoding": ACCEPT_ENCODING,
                "User-Agent": "agy-ppt-source-acquisition/1",
            },
        )

        try:
            response = client.open(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            location = _header(exc.headers, "Location")
            if exc.code in _REDIRECT_CODES and location:
                try:
                    exc.close()
                except Exception:
                    pass
                if redirect_count >= max_redirects:
                    raise RemoteTooManyRedirects(
                        f"exceeded the {max_redirects}-redirect limit while acquiring "
                        "the source"
                    )
                next_url = urllib.parse.urljoin(current_url, location)
                # Revalidate the hop before trusting it at all.
                try:
                    next_parts = validate_remote_url(next_url)
                    check_host_allowed(next_parts.hostname or "", resolver=resolver)
                except SourceAcquisitionError as inner:
                    raise RemoteRedirectBlocked(
                        f"redirect target was refused: {inner}"
                    )
                current_url = next_url
                redirect_count += 1
                continue
            status = exc.code
            try:
                exc.close()
            except Exception:
                pass
            raise RemoteHttpError(
                f"remote source returned HTTP {status}", status=status
            )
        except urllib.error.URLError as exc:
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, socket.timeout) or isinstance(exc, socket.timeout):
                raise RemoteTimeout(f"remote acquisition timed out: {reason}")
            name = type(reason).__name__
            if "SSL" in name or "Certificate" in name:
                raise RemoteTlsFailed(f"TLS verification failed: {reason}")
            raise SourceAcquisitionError(f"remote acquisition failed: {reason}")
        except socket.timeout as exc:
            raise RemoteTimeout(f"remote acquisition timed out: {exc}")

        with response:
            status = getattr(response, "status", None)
            if status is None:
                status = getattr(response, "code", 200)
            if not (200 <= int(status) < 300):
                raise RemoteHttpError(
                    f"remote source returned HTTP {status}", status=int(status)
                )

            headers = getattr(response, "headers", None)
            encoding = (_header(headers, "Content-Encoding") or "").strip().lower()
            if encoding not in _ACCEPTABLE_CONTENT_ENCODINGS:
                raise RemoteContentEncodingUnsupported(
                    f"server returned Content-Encoding {encoding!r}; identity "
                    "encoding was requested so the stored bytes would not be the "
                    "source entity"
                )

            declared_length: int | None = None
            raw_length = _header(headers, "Content-Length")
            if raw_length is not None:
                try:
                    declared_length = int(str(raw_length).strip())
                except (TypeError, ValueError):
                    declared_length = None
            if declared_length is not None and declared_length > max_bytes:
                raise RemoteResponseTooLarge(
                    f"declared Content-Length {declared_length} exceeds the "
                    f"{max_bytes}-byte limit"
                )

            content_type = _header(headers, "Content-Type")
            disposition = _header(headers, "Content-Disposition")
            final_url = str(getattr(response, "url", current_url) or current_url)

            payload_name = safe_payload_name(
                source_id, url=final_url, content_type=content_type or ""
            )
            payload_path = (out_dir / payload_name).resolve()
            # Defence in depth: the payload can never escape output_dir.
            if out_dir not in payload_path.parents and payload_path.parent != out_dir:
                raise RemoteUrlInvalid("resolved payload path escapes the output directory")

            partial_path = out_dir / f"{payload_name}.part"
            total = 0
            try:
                with open(partial_path, "wb") as handle:
                    while True:
                        try:
                            chunk = response.read(65536)
                        except socket.timeout as exc:
                            raise RemoteTimeout(
                                f"remote acquisition timed out while reading: {exc}"
                            )
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > max_bytes:
                            raise RemoteResponseTooLarge(
                                f"response body exceeded the {max_bytes}-byte limit "
                                "while streaming"
                            )
                        handle.write(chunk)
                payload_bytes = partial_path.read_bytes()
                digest = compute_source_digest(payload_bytes)
                os.replace(partial_path, payload_path)
            except BaseException:
                # Never leave a truncated payload that looks complete.
                try:
                    partial_path.unlink(missing_ok=True)
                except OSError:
                    pass
                raise

        return AcquisitionResult(
            schema_version=SCHEMA_VERSION,
            source_id=source_id,
            requested_url=requested_url,
            final_url=final_url,
            content_type=content_type,
            declared_content_length=declared_length,
            downloaded_bytes=total,
            source_digest=digest,
            local_payload_path=str(payload_path),
            redirect_count=redirect_count,
            retrieved_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            content_disposition=disposition,
        )


def acquire_and_ingest(
    url: str,
    source_id: str,
    output_dir: str | Path,
    **kwargs: Any,
) -> tuple[AcquisitionResult, Any]:
    """Convenience handoff: acquire, then run the existing Phase 13 ingestion.

    There is no second parser here. Format detection and extraction remain
    entirely inside ``source_ingestion``, so a server's declared Content-Type is
    advisory metadata and never overrides what the bytes actually are. An
    unsupported payload therefore fails with the existing ingestion error rather
    than being granted support because HTTP happened to succeed.
    """
    from source_ingestion import ingest_source

    acquisition = acquire_remote_source(url, source_id, output_dir, **kwargs)
    extraction = ingest_source(acquisition.local_payload_path, source_id)
    return acquisition, extraction


__all__ = [
    "AcquisitionResult",
    "SourceAcquisitionError",
    "acquire_and_ingest",
    "acquire_remote_source",
    "build_opener",
    "check_host_allowed",
    "safe_payload_name",
    "validate_remote_url",
]
