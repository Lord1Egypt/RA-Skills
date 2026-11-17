#!/usr/bin/env python3
"""Minimal credential-file-backed Beatra Streamable HTTP client."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import io
import json
import locale
import math
import os
import re
import shutil
import stat
import sys
import sysconfig
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar

PROTOCOL_VERSION = "2025-11-25"
PACKAGE_SLUG = "fund-report-talking"
PACKAGE_DISPLAY_NAME = "Fund Quarterly Report Talking Clips"
PACKAGE_VERSION = "0.1.9"
PACKAGE_CHANNEL = "clawhub"
PACKAGE_LOCALE = "en"
PACKAGE_DISCOVERY_URL = "https://beatra.ai/skills/fund-report-talking/channels/clawhub/install.json"
PACKAGE_CDN_BASE_TEMPLATE = "https://cdn.beatra.ai/agent-packages/fund-report-talking/channels/clawhub/v{version}"
PACKAGE_ROUTE_POLICY = "auto"
CLIENT_INFO = {"name": f"beatra-skill-{PACKAGE_SLUG}", "version": PACKAGE_VERSION}
_PLATFORM_VALUE = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}\Z")
REGISTRATION_TIMEOUT_SECONDS = 10.0
HTTP_USER_AGENT = f"Beatra-Skill/{PACKAGE_SLUG}/{PACKAGE_VERSION}"
CANONICAL_MCP_URL = "https://mcp.beatra.ai/mcp"
#: Transport hosts per network route, as (mcp, api, site, cdn). Identity never
#: comes from this table: the credential, the token resource and the update
#: discovery stay bound to the constants above, and only a request's host
#: follows the route (spec 2026-10-09 §5.1). The cn channel ships the second
#: row in place of the first.
ROUTE_HOSTS = {
    "ai": ("mcp.beatra.ai", "api.beatra.ai", "beatra.ai", "cdn.beatra.ai"),
    "cn": ("mcp.beatra.cn", "api.beatra.cn", "www.beatra.cn", "cdn.beatra.cn"),
}
ROUTE_POLICIES = ("auto", "ai", "cn")
NETWORK_FILE = "network.json"
NETWORK_SCHEMA_VERSION = 1
MAX_NETWORK_BYTES = 4096
ROUTE_PROBE_PATH = "/skill-route"
ROUTE_PROBE_USER_AGENT = "Beatra-Skill-Route/1"
ROUTE_PROBE_CN_AFTER_SECONDS = 1.0
ROUTE_PROBE_DEADLINE_SECONDS = 2.5
ROUTE_SHORT_TTL_SECONDS = 10 * 60
ROUTE_MIN_TTL_SECONDS = 60 * 60
ROUTE_MAX_TTL_SECONDS = 7 * 24 * 60 * 60
ROUTE_POLICY_VERSION = 1
ROUTE_REPROBE_INTERVAL_SECONDS = 2 * 60
GATEWAY_FAILURE_STATUSES = frozenset({502, 503, 504})
MAX_ROUTE_ANSWER_BYTES = 4096
_COUNTRY_SOURCES = ("cloudflare", "ip2region", "unknown", "disabled")
_COUNTRY_CODE = re.compile(r"[A-Z]{2}\Z")
#: Ask one network ("ai" or "cn") for its /skill-route answer: the decoded JSON
#: body, or None when nothing usable came back.
RouteProbe = Callable[[str], object]
REGISTRATION_MAX_AGE_SECONDS = 24 * 60 * 60
REGISTRATION_CACHE_FILE = "registration.json"
MAX_LOCAL_RECORD_BYTES = 4096
INSTALL_SOURCES = ("website", "github", "skillhub", "skillatlas", "modelscope", "workbuddy", "clawhub")
GUESSABLE_SOURCES = (*INSTALL_SOURCES, "other")
INSTALL_SOURCE_FILE = "install-source.json"
MAX_INSTALL_SOURCE_BYTES = 1024
SOURCE_RECORD_FILE = "source.json"
_SOURCE_BASIS_RANK = {"inferred": 1, "store_marker": 2, "stamp": 3}
#: The ClawHub CLI's own record of an install (`readSkillOrigin`, clawhub
#: 0.23.3 dist/skills.js); the legacy directory name comes second.
_CLAWHUB_ORIGINS = (".clawhub/origin.json", ".clawdhub/origin.json")
_CHANNEL_VALUE = re.compile(r"[a-z][a-z0-9]{0,31}\Z")
_LOCALE_TAG = re.compile(r"[a-z]{2,3}(?:-[A-Z]{2})?\Z")
_OS_VERSION = re.compile(r"[A-Za-z0-9._ -]{1,40}\Z")
_ARCH_VALUE = re.compile(r"[a-z0-9._-]{1,48}\Z")
_OS_NAMES = {"darwin": "darwin", "linux": "linux", "win32": "windows"}
_ROUTE_BASES = ("server", "cn_geoip", "cn_unreachable", "undecided")
#: A registration is sent again when any of these change, or after a day.
_REGISTRATION_KEY = (
    "external_installation_ref",
    "package_version",
    "platform",
    "channel",
    "channel_locale",
    "route",
    "install_source",
    "install_source_basis",
)
UPDATE_CHECK_MAX_AGE_SECONDS = 24 * 60 * 60
UPDATE_LOCK_MAX_AGE_SECONDS = 10 * 60
UPDATE_DISCOVERY_TIMEOUT_SECONDS = 3.0
UPDATE_DOWNLOAD_TIMEOUT_SECONDS = 60.0
MAX_UPDATE_DISCOVERY_BYTES = 64 * 1024
MAX_UPDATE_MANIFEST_BYTES = 1024 * 1024
MAX_UPDATE_ARCHIVE_BYTES = 50 * 1024 * 1024
MAX_UPDATE_FILES = 512
MAX_UPDATE_FILE_BYTES = 16 * 1024 * 1024
MAX_UPDATE_TOTAL_BYTES = 64 * 1024 * 1024
_SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
PostJson = Callable[
    [str, dict[str, str], dict[str, Any], float],
    tuple[int, dict[str, str], dict[str, Any] | None],
]
PutBytes = Callable[[str, dict[str, str], bytes], dict[str, Any]]
GetBytes = Callable[[str, float, int], bytes]
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
AUTH_REQUIRED_CODE = "BEATRA_AUTH_REQUIRED"
RECONNECT_GUIDANCE = (
    "Reconnect with `python3 scripts/authorize.py` and follow "
    'its output until it prints "Beatra is ready".'
)
T = TypeVar("T")
AUTH_REQUIRED_MESSAGE = f"{AUTH_REQUIRED_CODE}: Beatra authorization is no longer valid. {RECONNECT_GUIDANCE}"


class AuthenticationRequired(RuntimeError):
    """The remote MCP endpoint definitively rejected the bearer credential."""


class CredentialsMissing(RuntimeError):
    """No usable credential file: this computer has not connected yet."""


def _allowlisted_unauthorized_message(raw: bytes) -> str | None:
    """Take only error.message from a Beatra 401 envelope. Never dump the body."""

    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
        return None
    if not isinstance(payload, dict):
        return None
    error = payload.get("error")
    if not isinstance(error, dict):
        return None
    details = error.get("details")
    reason = details.get("reason") if isinstance(details, dict) else None
    if error.get("code") != "mcp_connection_required" and reason != "mcp_connection_required":
        return None
    message = error.get("message")
    if not isinstance(message, str):
        return None
    cleaned = message.strip()
    return cleaned or None


def _authentication_required_message(raw: bytes) -> str:
    message = _allowlisted_unauthorized_message(raw)
    if message is None:
        return AUTH_REQUIRED_MESSAGE
    return f"{AUTH_REQUIRED_CODE}: {message} {RECONNECT_GUIDANCE}"


def _require_status(status: int, accepted: set[int], operation: str) -> None:
    if status == 401:
        raise AuthenticationRequired(AUTH_REQUIRED_MESSAGE)
    if status not in accepted:
        raise RuntimeError(f"{operation} returned HTTP {status}")


class _RejectRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, operation: str = "Beatra MCP") -> None:
        super().__init__()
        self.operation = operation

    def redirect_request(
        self,
        _request: urllib.request.Request,
        _file_pointer: Any,
        code: int,
        _message: str,
        _headers: Any,
        _new_url: str,
    ) -> None:
        raise RuntimeError(f"{self.operation} refused HTTP redirect ({code})")


def _default_post_json(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: float = 60.0,
) -> tuple[int, dict[str, str], dict[str, Any] | None]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        headers={**headers, "User-Agent": HTTP_USER_AGENT},
        method="POST",
    )
    opener = urllib.request.build_opener(_RejectRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            status = int(response.status)
            response_headers = dict(response.headers.items())
            raw = response.read()
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        if status in GATEWAY_FAILURE_STATUSES:
            note_route_failure()
        raw = b""
        try:
            raw = exc.read() or b""
        except Exception:
            raw = b""
        if status == 401:
            raise AuthenticationRequired(_authentication_required_message(raw)) from None
        _require_status(status, set(), "Beatra MCP")
        raise AssertionError("unreachable") from exc
    except urllib.error.URLError as exc:
        note_route_failure()
        raise RuntimeError("Beatra MCP is unreachable") from exc
    except (OSError, http.client.HTTPException):
        note_route_failure()
        raise
    if not raw:
        return status, response_headers, None
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Beatra MCP returned HTTP {status} with an invalid response") from exc
    if not isinstance(body, dict):
        raise RuntimeError(f"Beatra MCP returned HTTP {status} with an invalid response")
    return status, response_headers, body


def _default_put_bytes(
    url: str,
    headers: dict[str, str],
    content: bytes,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=content,
        headers={**headers, "User-Agent": HTTP_USER_AGENT},
        method="PUT",
    )
    opener = urllib.request.build_opener(_RejectRedirectHandler("Beatra upload"))
    try:
        with opener.open(request, timeout=120) as response:
            status = int(response.status)
            raw = response.read()
    except urllib.error.HTTPError as exc:
        if int(exc.code) in GATEWAY_FAILURE_STATUSES:
            note_route_failure()
        raise RuntimeError(f"Beatra upload returned HTTP {int(exc.code)}") from exc
    except urllib.error.URLError as exc:
        note_route_failure()
        raise RuntimeError("Beatra upload host is unreachable") from exc
    except (OSError, http.client.HTTPException):
        note_route_failure()
        raise
    if not 200 <= status < 300:
        raise RuntimeError(f"Beatra upload returned HTTP {status}")
    try:
        body = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Beatra upload returned an invalid response") from exc
    if not isinstance(body, dict):
        raise RuntimeError("Beatra upload returned an invalid response")
    return body


def _default_get_bytes(url: str, timeout: float, max_bytes: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json, application/zip",
            "User-Agent": HTTP_USER_AGENT,
        },
        method="GET",
    )
    opener = urllib.request.build_opener(_RejectRedirectHandler("Beatra update"))
    try:
        with opener.open(request, timeout=timeout) as response:
            if int(response.status) != 200:
                raise RuntimeError(f"Beatra update returned HTTP {int(response.status)}")
            declared = response.headers.get("Content-Length")
            if declared is not None:
                try:
                    declared_bytes = int(declared)
                except ValueError as exc:
                    raise RuntimeError("Beatra update returned an invalid content length") from exc
                if declared_bytes < 0 or declared_bytes > max_bytes:
                    raise RuntimeError("Beatra update exceeded the download limit")
            content = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        if int(exc.code) in GATEWAY_FAILURE_STATUSES:
            note_route_failure()
        raise RuntimeError(f"Beatra update returned HTTP {int(exc.code)}") from exc
    except urllib.error.URLError as exc:
        note_route_failure()
        raise RuntimeError("Beatra update host is unreachable") from exc
    except (OSError, http.client.HTTPException):
        note_route_failure()
        raise
    if len(content) > max_bytes:
        raise RuntimeError("Beatra update exceeded the download limit")
    return content


def _read_local_upload(path: Path) -> tuple[str, bytes]:
    candidate = path.expanduser()
    descriptor = -1
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(candidate, flags)
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_size < 1
            or before.st_size > MAX_UPLOAD_BYTES
        ):
            raise RuntimeError(
                f"Local upload must be one regular file between 1 and {MAX_UPLOAD_BYTES} bytes"
            )
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            content = handle.read(MAX_UPLOAD_BYTES + 1)
            after = os.fstat(handle.fileno())
        stable_fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
        if (
            len(content) != before.st_size
            or len(content) > MAX_UPLOAD_BYTES
            or any(getattr(before, field) != getattr(after, field) for field in stable_fields)
        ):
            raise RuntimeError("Local upload changed while it was being read")
    except RuntimeError:
        raise
    except OSError as exc:
        raise RuntimeError("Local upload must be one readable regular file") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return candidate.name, content


def _header_value(headers: dict[str, str], name: str) -> str | None:
    return next((value for key, value in headers.items() if key.lower() == name.lower()), None)


def _complete_upload(
    result: dict[str, Any],
    *,
    mime_type: str,
    content: bytes,
    put_bytes: PutBytes,
) -> dict[str, str]:
    structured = result.get("structuredContent")
    instruction = structured.get("upload") if isinstance(structured, dict) else None
    if not isinstance(instruction, dict) or instruction.get("method") != "PUT":
        raise RuntimeError("Beatra upload instructions are invalid")
    url = instruction.get("url")
    headers = instruction.get("headers")
    if not isinstance(url, str) or not isinstance(headers, dict):
        raise RuntimeError("Beatra upload instructions are invalid")
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise RuntimeError("Beatra upload instructions are invalid")
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in headers.items()):
        raise RuntimeError("Beatra upload instructions are invalid")
    content_type = _header_value(headers, "Content-Type")
    content_length = _header_value(headers, "Content-Length")
    if content_type != mime_type or content_length != str(len(content)):
        raise RuntimeError("Beatra upload instructions are invalid")
    response = put_bytes(url, dict(headers), content)
    artifact_id = response.get("artifact_id")
    if not isinstance(artifact_id, str) or not artifact_id:
        raise RuntimeError("Beatra upload returned an invalid response")
    return {"type": "artifact", "artifact_id": artifact_id}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _semver(value: object) -> tuple[int, int, int]:
    if not isinstance(value, str):
        raise RuntimeError("Beatra update returned an invalid version")
    matched = _SEMVER.fullmatch(value)
    if matched is None:
        raise RuntimeError("Beatra update returned an invalid version")
    return (
        int(matched.group(1)),
        int(matched.group(2)),
        int(matched.group(3)),
    )


_ACTIVE_ROUTE: str | None = None
_ROUTE_STATE_DIR: Path | None = None


def route_policy() -> str:
    """How this build picks its network: `auto` decides per computer, `ai` and
    `cn` are fixed. Anything unrendered or unknown is the fixed `ai`."""

    return PACKAGE_ROUTE_POLICY if PACKAGE_ROUTE_POLICY in ROUTE_POLICIES else "ai"


def _read_network(state_dir: Path) -> dict[str, Any]:
    """`~/.beatra/network.json`, or {} when it is missing, unreadable, too large,
    or written in a schema this helper does not know."""

    try:
        with (state_dir.expanduser() / NETWORK_FILE).open("rb") as handle:
            content = handle.read(MAX_NETWORK_BYTES + 1)
        if len(content) > MAX_NETWORK_BYTES:
            return {}
        value = json.loads(content.decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return {}
    if not isinstance(value, dict):
        return {}
    version = value.get("schema_version")
    if isinstance(version, bool) or version != NETWORK_SCHEMA_VERSION:
        return {}
    return value


def current_route(state_dir: Path | None = None) -> str:
    """The network this process sends requests over. It never asks Beatra:
    `resolve_route` decides once at process start and records the answer."""

    policy = route_policy()
    if policy != "auto":
        return policy
    if _ACTIVE_ROUTE in ROUTE_HOSTS:
        return _ACTIVE_ROUTE
    if state_dir is not None:
        recorded = _read_network(state_dir).get("route")
        if isinstance(recorded, str) and recorded in ROUTE_HOSTS:
            return recorded
    return "ai"


def route_mcp_url(route: str) -> str:
    return f"https://{ROUTE_HOSTS[route][0]}/mcp"


def route_api_origin(route: str) -> str:
    return f"https://{ROUTE_HOSTS[route][1]}"


def _with_host(url: str, host: str) -> str:
    return urllib.parse.urlunsplit(urllib.parse.urlsplit(url)._replace(netloc=host))


def _site_url(url: str, route: str) -> str:
    return _with_host(url, ROUTE_HOSTS[route][2])


def _cdn_url(url: str, route: str) -> str:
    return _with_host(url, ROUTE_HOSTS[route][3])


def _update_get(
    url: str,
    transport: Callable[[str, str], str],
    *,
    route: str | None,
    timeout: float,
    limit: int,
    get_bytes: GetBytes,
) -> bytes:
    """GET one update object, named by its identity URL, over the route. Update
    objects are verified by checksum, so under the auto policy a failure may
    retry once over the other route (spec §5.5); business requests never do."""

    chosen = route or current_route()
    try:
        return get_bytes(transport(url, chosen), timeout, limit)
    except Exception:  # any failure on this route may be tried on the other
        if route_policy() != "auto":
            raise
        other = "cn" if chosen == "ai" else "ai"
        return get_bytes(transport(url, other), timeout, limit)


def _route_answer(value: object) -> dict[str, Any] | None:
    """A structurally valid /skill-route answer, else None (spec §5.2)."""

    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return None
    route = value.get("route")
    country = value.get("country_code")
    ttl = value.get("ttl_seconds")
    if (
        route not in ("ai", "cn", None)
        or value.get("country_source") not in _COUNTRY_SOURCES
        or not (country is None or (isinstance(country, str) and _COUNTRY_CODE.fullmatch(country)))
        or isinstance(ttl, bool)
        or not isinstance(ttl, int)
    ):
        return None
    return {
        "route": route,
        "country_code": country,
        "country_source": value["country_source"],
        "ttl_seconds": ttl,
    }


def _default_route_probe(route: str) -> object:
    """GET /skill-route on one network. It carries no credential, package or
    installation identity: only its own fixed User-Agent (spec §5.2, D1)."""

    request = urllib.request.Request(
        f"{route_api_origin(route)}{ROUTE_PROBE_PATH}",
        headers={"Accept": "application/json", "User-Agent": ROUTE_PROBE_USER_AGENT},
        method="GET",
    )
    opener = urllib.request.build_opener(_RejectRedirectHandler("Beatra route check"))
    try:
        with opener.open(request, timeout=ROUTE_PROBE_DEADLINE_SECONDS) as response:
            if int(response.status) != 200:
                return None
            raw = response.read(MAX_ROUTE_ANSWER_BYTES + 1)
        if len(raw) > MAX_ROUTE_ANSWER_BYTES:
            return None
        return json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, RuntimeError, http.client.HTTPException):
        return None


def _probe_routes(
    probe: RouteProbe,
    *,
    cn_after_seconds: float,
    deadline_seconds: float,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Ask .ai first, and .cn at once when .ai says cn, fails, or is still
    silent after `cn_after_seconds`; stop as soon as the result cannot change,
    and never later than the hard deadline (spec §5.2, §5.8). Each probe runs
    in a daemon thread because getaddrinfo ignores urllib's timeout."""

    answers: dict[str, dict[str, Any] | None] = {}
    changed = threading.Condition()

    def ask(route: str) -> None:
        try:
            reply = _route_answer(probe(route))
        except Exception:  # a probe that raised gave no answer
            reply = None
        with changed:
            answers[route] = reply
            changed.notify_all()

    def launch(route: str) -> None:
        threading.Thread(target=ask, args=(route,), name=f"beatra-route-{route}", daemon=True).start()

    started = time.monotonic()
    cn_asked = False
    launch("ai")
    with changed:
        while True:
            elapsed = time.monotonic() - started
            ai_known = "ai" in answers
            if ai_known and (answers["ai"] or {}).get("route") == "ai":
                break
            if not cn_asked and (ai_known or elapsed >= cn_after_seconds):
                cn_asked = True
                launch("cn")
            if ai_known and "cn" in answers:
                break
            remaining = deadline_seconds - elapsed
            if remaining <= 0:
                break
            wait = remaining if cn_asked else min(remaining, cn_after_seconds - elapsed)
            changed.wait(max(wait, 0.001))
        return answers.get("ai"), answers.get("cn")


def _clamp_ttl(value: int) -> int:
    return max(ROUTE_MIN_TTL_SECONDS, min(ROUTE_MAX_TTL_SECONDS, value))


def decide_route(
    ai: dict[str, Any] | None,
    cn: dict[str, Any] | None,
    *,
    previous: str | None,
) -> dict[str, Any]:
    """The §5.2 table. Only a mainland verdict with a reachable .cn switches to
    cn; with no usable answer the computer keeps the route it had, so a relay
    blip never pushes a blocked mainland computer back to .ai."""

    def decided(route: str, basis: str, reply: dict[str, Any] | None, lifetime: int) -> dict[str, Any]:
        return {
            "route": route,
            "basis": basis,
            "country_code": reply["country_code"] if reply else None,
            "country_source": reply["country_source"] if reply else "unknown",
            "lifetime": lifetime,
        }

    if ai is not None and ai["route"] == "cn":
        if cn is not None:
            return decided("cn", "server", ai, _clamp_ttl(ai["ttl_seconds"]))
        return decided("ai", "cn_unreachable", ai, ROUTE_SHORT_TTL_SECONDS)
    if ai is not None and ai["route"] == "ai":
        return decided("ai", "server", ai, _clamp_ttl(ai["ttl_seconds"]))
    if cn is not None and cn["route"] in ROUTE_HOSTS:
        return decided(cn["route"], "cn_geoip", cn, _clamp_ttl(cn["ttl_seconds"]))
    fallback = previous if previous in ROUTE_HOSTS else "ai"
    return decided(fallback, "undecided", None, ROUTE_SHORT_TTL_SECONDS)


def _still_valid(record: dict[str, Any], now: float) -> bool:
    expires_at = record.get("expires_at")
    return isinstance(expires_at, (int, float)) and not isinstance(expires_at, bool) and now < expires_at


def _update_network(
    state_dir: Path,
    changes: dict[str, Any],
    *,
    remove: tuple[str, ...] = (),
) -> None:
    """Read-modify-write `network.json`, keeping `approval_link` and any key a
    newer helper added. Concurrent processes: the last writer wins."""

    record = _read_network(state_dir)
    record.update(changes)
    for key in remove:
        record.pop(key, None)
    record["schema_version"] = NETWORK_SCHEMA_VERSION
    _write_private_json(state_dir.expanduser() / NETWORK_FILE, record)


def resolve_route(
    state_dir: Path | None = None,
    *,
    now: float | None = None,
    probe: RouteProbe | None = None,
    cn_after_seconds: float = ROUTE_PROBE_CN_AFTER_SECONDS,
    deadline_seconds: float = ROUTE_PROBE_DEADLINE_SECONDS,
) -> str:
    """Decide once per process which network this computer uses (spec §5.2).

    Only `auto` builds decide; the cn channel is fixed and never asks. Every
    outcome is recorded so an offline computer does not ask on every command,
    and nothing here can fail the command that follows.
    """

    global _ACTIVE_ROUTE, _ROUTE_STATE_DIR
    policy = route_policy()
    if policy != "auto":
        _ACTIVE_ROUTE = policy
        return policy
    resolved = (state_dir or Path.home() / ".beatra").expanduser()
    _ROUTE_STATE_DIR = resolved
    observed = time.time() if now is None else now
    record = _read_network(resolved)
    recorded = record.get("route")
    # A route another helper wrote may be any JSON value: only a known name counts.
    previous = recorded if isinstance(recorded, str) and recorded in ROUTE_HOSTS else None
    if previous is not None and (record.get("pinned") is True or _still_valid(record, observed)):
        _ACTIVE_ROUTE = previous
        return previous
    try:
        ai, cn = _probe_routes(
            probe or _default_route_probe,
            cn_after_seconds=cn_after_seconds,
            deadline_seconds=deadline_seconds,
        )
        decision = decide_route(ai, cn, previous=previous)
    except Exception:
        decision = decide_route(None, None, previous=previous)
    _ACTIVE_ROUTE = decision["route"]
    with suppress(Exception):
        _update_network(
            resolved,
            {
                "route": decision["route"],
                "basis": decision["basis"],
                "pinned": False,
                "country_code": decision["country_code"],
                "country_source": decision["country_source"],
                "decided_at": int(observed),
                "expires_at": int(observed) + decision["lifetime"],
                "last_probe_at": int(observed),
                "policy_version": ROUTE_POLICY_VERSION,
            },
        )
    return decision["route"]


def note_route_failure(state_dir: Path | None = None, *, now: float | None = None) -> None:
    """A connection failure or gateway error on this computer's route: let the
    next process decide again (spec §5.5), at most once every two minutes and
    never for a route the user pinned. The failed request itself is never
    resent; it returns the error it always did."""

    if route_policy() != "auto":
        return
    resolved = state_dir or _ROUTE_STATE_DIR
    if resolved is None:
        return
    observed = time.time() if now is None else now
    with suppress(Exception):
        record = _read_network(resolved)
        if record.get("route") not in ROUTE_HOSTS or record.get("pinned") is True:
            return
        expires = record.get("expires_at")
        if isinstance(expires, (int, float)) and not isinstance(expires, bool) and expires <= observed:
            return  # already due for a new decision; later failures add nothing
        last = record.get("last_probe_at")
        if (
            isinstance(last, (int, float))
            and not isinstance(last, bool)
            and observed - last < ROUTE_REPROBE_INTERVAL_SECONDS
        ):
            return
        _update_network(resolved, {"expires_at": int(observed)})


_ROUTE_NAMES = {"ai": "the international network", "cn": "the mainland China network"}


def approval_link_preference(state_dir: Path) -> str:
    """`ai` when the user chose to open approval links on Beatra's international
    site (`authorize.py --approval-link ai`), else `auto` (spec §5.7)."""

    return "ai" if _read_network(state_dir).get("approval_link") == "ai" else "auto"


def set_approval_link_preference(state_dir: Path, choice: str) -> None:
    if choice == "ai":
        _update_network(state_dir, {"approval_link": "ai"})
    elif choice == "auto":
        _update_network(state_dir, {}, remove=("approval_link",))
    else:
        raise RuntimeError("Choose ai or auto for the approval link")


def _probe_one(probe: RouteProbe, route: str, *, deadline_seconds: float) -> dict[str, Any] | None:
    replies: list[dict[str, Any] | None] = []
    done = threading.Event()

    def ask() -> None:
        try:
            replies.append(_route_answer(probe(route)))
        except Exception:
            replies.append(None)
        finally:
            done.set()

    threading.Thread(target=ask, name=f"beatra-route-{route}", daemon=True).start()
    done.wait(deadline_seconds)
    return replies[0] if replies else None


def pin_route(
    choice: str,
    state_dir: Path,
    *,
    now: float | None = None,
    probe: RouteProbe | None = None,
    deadline_seconds: float = ROUTE_PROBE_DEADLINE_SECONDS,
) -> str:
    """`network --use`: keep one network until `--use auto` (spec §5.4). A
    network that does not answer right now is refused, so a computer is never
    locked onto a route it cannot reach."""

    global _ACTIVE_ROUTE
    if route_policy() != "auto":
        raise RuntimeError("This installation always uses the mainland China network; its network cannot be changed.")
    observed = time.time() if now is None else now
    if choice == "auto":
        _update_network(state_dir, {"pinned": False, "expires_at": 0})
        _ACTIVE_ROUTE = None
        return resolve_route(state_dir, now=observed, probe=probe)
    if choice not in ROUTE_HOSTS:
        raise RuntimeError("Choose cn, ai or auto")
    reply = _probe_one(probe or _default_route_probe, choice, deadline_seconds=deadline_seconds)
    if reply is None:
        raise RuntimeError(
            f"Beatra did not answer over {_ROUTE_NAMES[choice]} just now, so it was not selected. "
            "Check the connection and try again."
        )
    _update_network(
        state_dir,
        {
            "route": choice,
            "basis": "pinned",
            "pinned": True,
            "country_code": reply["country_code"],
            "country_source": reply["country_source"],
            "decided_at": int(observed),
            "expires_at": None,
            "last_probe_at": int(observed),
            "policy_version": ROUTE_POLICY_VERSION,
        },
    )
    _ACTIVE_ROUTE = choice
    return choice


def network_status(state_dir: Path) -> dict[str, Any]:
    policy = route_policy()
    status: dict[str, Any] = {
        "policy": policy,
        "route": current_route(state_dir),
        "approval_link": approval_link_preference(state_dir),
    }
    if policy != "auto":
        status["basis"] = "channel"
        return status
    record = _read_network(state_dir)
    if record.get("route") in ROUTE_HOSTS:
        for key in ("basis", "pinned", "country_code", "expires_at"):
            if key in record:
                status[key] = record[key]
    return status


def _network_command(choice: str | None, state_dir: Path) -> None:
    try:
        route = pin_route(choice, state_dir) if choice is not None else None
    except OSError as exc:
        raise RuntimeError(f"Could not save the network choice: {exc}") from exc
    if choice == "auto":
        print(f"Beatra chooses this computer's network automatically again; it now uses {_ROUTE_NAMES[route]}.")
    elif choice is not None:
        print(
            f"Beatra will use {_ROUTE_NAMES[route]} until you run "
            "`python3 scripts/mcp_client.py network --use auto`."
        )
    print(json.dumps(network_status(state_dir), ensure_ascii=False, separators=(",", ":")))


def _discovery_url() -> str:
    return PACKAGE_DISCOVERY_URL


def _json_object(content: bytes, operation: str) -> dict[str, Any]:
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{operation} returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{operation} returned invalid JSON")
    return value


def _release_urls(discovery: dict[str, Any]) -> tuple[str, str]:
    version = discovery.get("version")
    archive = discovery.get("archive")
    manifest = discovery.get("manifest")
    base_url = discovery.get("base_url")
    expected_base = PACKAGE_CDN_BASE_TEMPLATE.format(version=version)
    expected_archive = f"{PACKAGE_SLUG}-skill-{version}.zip"
    if (
        discovery.get("schema_version") != 1
        or discovery.get("package") != PACKAGE_SLUG
        or discovery.get("channel") != PACKAGE_CHANNEL
        or discovery.get("locale") != PACKAGE_LOCALE
        or not isinstance(version, str)
        or archive != expected_archive
        or manifest != "skill-manifest.json"
        or base_url != expected_base
        or not isinstance(discovery.get("archive_sha256"), str)
        or _SHA256.fullmatch(discovery["archive_sha256"]) is None
        or not isinstance(discovery.get("manifest_sha256"), str)
        or _SHA256.fullmatch(discovery["manifest_sha256"]) is None
    ):
        raise RuntimeError("Beatra update discovery is invalid")
    parsed = urllib.parse.urlsplit(expected_base)
    if (
        parsed.scheme != "https"
        or parsed.hostname not in {hosts[3] for hosts in ROUTE_HOSTS.values()}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise RuntimeError("Beatra update discovery is invalid")
    return f"{expected_base}/{archive}", f"{expected_base}/{manifest}"


def check_update(
    *,
    get_bytes: GetBytes = _default_get_bytes,
    route: str | None = None,
) -> dict[str, Any]:
    discovery = _json_object(
        _update_get(
            _discovery_url(),
            _site_url,
            route=route,
            timeout=UPDATE_DISCOVERY_TIMEOUT_SECONDS,
            limit=MAX_UPDATE_DISCOVERY_BYTES,
            get_bytes=get_bytes,
        ),
        "Beatra update discovery",
    )
    current = _semver(PACKAGE_VERSION)
    available = _semver(discovery.get("version"))
    _release_urls(discovery)
    if available < current:
        raise RuntimeError("Beatra update discovery attempted a version downgrade")
    return {
        "current_version": PACKAGE_VERSION,
        "available_version": discovery["version"],
        "update_available": available > current,
        "discovery": discovery,
    }


def _manifest_files(
    manifest: dict[str, Any],
    *,
    discovery: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if (
        manifest.get("schema_version") != 1
        or manifest.get("package") != PACKAGE_SLUG
        or manifest.get("channel") != PACKAGE_CHANNEL
        or manifest.get("locale") != PACKAGE_LOCALE
        or manifest.get("version") != discovery["version"]
        or manifest.get("archive") != discovery["archive"]
        or manifest.get("archive_sha256") != discovery["archive_sha256"]
    ):
        raise RuntimeError("Beatra update manifest is invalid")
    listed = manifest.get("files")
    if not isinstance(listed, list) or not listed or len(listed) > MAX_UPDATE_FILES:
        raise RuntimeError("Beatra update manifest is invalid")
    files: dict[str, dict[str, Any]] = {}
    folded: set[str] = set()
    total = 0
    prefix = f"{PACKAGE_SLUG}/"
    for item in listed:
        if not isinstance(item, dict):
            raise RuntimeError("Beatra update manifest is invalid")
        path = item.get("path")
        size = item.get("bytes")
        digest = item.get("sha256")
        if (
            not isinstance(path, str)
            or not path.startswith(prefix)
            or not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
            or size > MAX_UPDATE_FILE_BYTES
            or not isinstance(digest, str)
            or _SHA256.fullmatch(digest) is None
        ):
            raise RuntimeError("Beatra update manifest is invalid")
        relative = path[len(prefix) :]
        parts = relative.split("/")
        if (
            not relative
            or "\\" in relative
            or "\x00" in relative
            or any(part in {"", ".", ".."} for part in parts)
            or Path(relative).is_absolute()
        ):
            raise RuntimeError("Beatra update manifest contains an unsafe path")
        collision = relative.casefold()
        if relative in files or collision in folded:
            raise RuntimeError("Beatra update manifest contains duplicate paths")
        total += size
        if total > MAX_UPDATE_TOTAL_BYTES:
            raise RuntimeError("Beatra update manifest exceeded the extraction limit")
        folded.add(collision)
        files[relative] = {"bytes": size, "sha256": digest}
    return files


def _validated_archive(
    archive: bytes,
    *,
    manifest_files: dict[str, dict[str, Any]],
) -> dict[str, bytes]:
    extracted: dict[str, bytes] = {}
    folded: set[str] = set()
    prefix = f"{PACKAGE_SLUG}/"
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            members = bundle.infolist()
            if not members or len(members) > MAX_UPDATE_FILES:
                raise RuntimeError("Beatra update archive has an invalid file count")
            for member in members:
                name = member.filename
                mode = member.external_attr >> 16
                if (
                    member.is_dir()
                    or member.flag_bits & 0x1
                    or stat.S_ISLNK(mode)
                    or not name.startswith(prefix)
                    or "\\" in name
                    or "\x00" in name
                ):
                    raise RuntimeError("Beatra update archive contains an unsafe member")
                relative = name[len(prefix) :]
                parts = relative.split("/")
                if (
                    not relative
                    or any(part in {"", ".", ".."} for part in parts)
                    or Path(relative).is_absolute()
                    or relative not in manifest_files
                    or relative.casefold() in folded
                ):
                    raise RuntimeError("Beatra update archive contains an unsafe member")
                expected = manifest_files[relative]
                if member.file_size != expected["bytes"] or member.file_size > MAX_UPDATE_FILE_BYTES:
                    raise RuntimeError("Beatra update archive does not match its manifest")
                content = bundle.read(member)
                if len(content) != expected["bytes"] or _sha256(content) != expected["sha256"]:
                    raise RuntimeError("Beatra update archive does not match its manifest")
                folded.add(relative.casefold())
                extracted[relative] = content
    except zipfile.BadZipFile as exc:
        raise RuntimeError("Beatra update archive is invalid") from exc
    if set(extracted) != set(manifest_files):
        raise RuntimeError("Beatra update archive does not match its manifest")
    return extracted


def download_update(
    discovery: dict[str, Any],
    *,
    get_bytes: GetBytes = _default_get_bytes,
    route: str | None = None,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    archive_url, manifest_url = _release_urls(discovery)
    manifest_content = _update_get(
        manifest_url,
        _cdn_url,
        route=route,
        timeout=UPDATE_DOWNLOAD_TIMEOUT_SECONDS,
        limit=MAX_UPDATE_MANIFEST_BYTES,
        get_bytes=get_bytes,
    )
    if _sha256(manifest_content) != discovery["manifest_sha256"]:
        raise RuntimeError("Beatra update manifest checksum does not match discovery")
    manifest = _json_object(manifest_content, "Beatra update manifest")
    manifest_files = _manifest_files(manifest, discovery=discovery)
    archive = _update_get(
        archive_url,
        _cdn_url,
        route=route,
        timeout=UPDATE_DOWNLOAD_TIMEOUT_SECONDS,
        limit=MAX_UPDATE_ARCHIVE_BYTES,
        get_bytes=get_bytes,
    )
    if _sha256(archive) != discovery["archive_sha256"]:
        raise RuntimeError("Beatra update archive checksum does not match discovery")
    return manifest, _validated_archive(archive, manifest_files=manifest_files)


def _current_install_root() -> Path:
    try:
        return Path(__file__).resolve().parent.parent
    except NameError as exc:
        raise RuntimeError("Beatra package installation path is unavailable") from exc


def _ensure_private_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if os.name == "posix":
        with suppress(OSError):
            path.chmod(0o700)


def _update_home(state_dir: Path, install_root: Path) -> Path:
    identity = hashlib.sha256(str(install_root.resolve()).encode("utf-8")).hexdigest()[:24]
    root = state_dir.expanduser() / "updates" / identity
    _ensure_private_directory(root)
    return root


def _read_update_state(update_home: Path) -> dict[str, Any]:
    path = update_home / "state.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": 1, "auto_update": True}
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return {"schema_version": 1, "auto_update": True}
    return value


def _write_private_json(path: Path, value: dict[str, Any]) -> None:
    _ensure_private_directory(path.parent)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{os.urandom(4).hex()}.tmp")
    descriptor = -1
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            json.dump(value, handle, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def set_auto_update(
    enabled: bool,
    *,
    state_dir: Path | None = None,
    install_root: Path | None = None,
) -> None:
    resolved_state = state_dir or Path.home() / ".beatra"
    resolved_root = (install_root or _current_install_root()).resolve()
    update_home = _update_home(resolved_state, resolved_root)
    state = _read_update_state(update_home)
    state["auto_update"] = bool(enabled)
    _write_private_json(update_home / "state.json", state)


def _safe_destination(install_root: Path, relative: str) -> Path:
    parts = relative.split("/")
    if (
        not relative
        or "\\" in relative
        or any(part in {"", ".", ".."} for part in parts)
        or Path(relative).is_absolute()
    ):
        raise RuntimeError("Beatra update contains an unsafe destination")
    current = install_root
    for part in parts[:-1]:
        current = current / part
        if current.exists() or current.is_symlink():
            try:
                mode = os.lstat(current).st_mode
            except OSError as exc:
                raise RuntimeError("Beatra update cannot inspect its destination") from exc
            if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
                raise RuntimeError("Beatra update refused a linked destination")
    destination = install_root.joinpath(*parts)
    if destination.exists() or destination.is_symlink():
        try:
            mode = os.lstat(destination).st_mode
        except OSError as exc:
            raise RuntimeError("Beatra update cannot inspect its destination") from exc
        if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
            raise RuntimeError("Beatra update refused a non-file destination")
    return destination


def _nearest_existing_parent(path: Path, install_root: Path) -> Path:
    candidate = path.parent
    while candidate != install_root and not candidate.exists():
        candidate = candidate.parent
    if not candidate.exists() or not candidate.is_dir():
        raise RuntimeError("Beatra update destination is unavailable")
    return candidate


def _write_probe(directory: Path) -> None:
    probe = directory / f".beatra-update-probe-{os.getpid()}-{os.urandom(4).hex()}"
    descriptor = -1
    try:
        descriptor = os.open(probe, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError as exc:
        raise RuntimeError("Beatra package installation is not writable") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        probe.unlink(missing_ok=True)


def _transaction_temporary(destination: Path, nonce: str) -> Path:
    if re.fullmatch(r"[0-9a-f]{16}", nonce) is None:
        raise RuntimeError("Beatra update recovery journal is invalid")
    return destination.with_name(f".{destination.name}.beatra-update-{nonce}.tmp")


def _copy_to_destination(
    content: bytes,
    destination: Path,
    *,
    mode: int = 0o644,
    temporary: Path | None = None,
) -> None:
    temporary = temporary or destination.with_name(
        f".{destination.name}.beatra-update-{os.getpid()}-{os.urandom(4).hex()}.tmp"
    )
    descriptor = -1
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        if os.name == "posix":
            destination.chmod(mode)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def _remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def _rollback_transaction(update_home: Path, install_root: Path) -> None:
    transaction = update_home / "transaction"
    journal_path = transaction / "journal.json"
    if not journal_path.exists():
        _remove_tree(transaction)
        return
    try:
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Beatra update recovery journal is invalid") from exc
    if (
        not isinstance(journal, dict)
        or journal.get("schema_version") != 1
        or journal.get("install_root") != str(install_root)
        or not isinstance(journal.get("nonce"), str)
        or re.fullmatch(r"[0-9a-f]{16}", journal["nonce"]) is None
        or not isinstance(journal.get("entries"), list)
    ):
        raise RuntimeError("Beatra update recovery journal is invalid")
    for entry in reversed(journal["entries"]):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise RuntimeError("Beatra update recovery journal is invalid")
        destination = _safe_destination(install_root, entry["path"])
        temporary = _transaction_temporary(destination, journal["nonce"])
        temporary.unlink(missing_ok=True)
        if entry.get("existed") is True:
            backup = transaction / "backup" / entry["path"]
            if not backup.is_file():
                raise RuntimeError("Beatra update recovery backup is missing")
            destination.parent.mkdir(parents=True, exist_ok=True)
            _copy_to_destination(
                backup.read_bytes(),
                destination,
                mode=int(entry.get("mode", 0o644)),
                temporary=temporary,
            )
        elif destination.exists():
            destination.unlink()
    created = journal.get("created_dirs")
    if isinstance(created, list):
        for relative in reversed(created):
            if not isinstance(relative, str):
                continue
            directory = install_root / relative
            with suppress(OSError):
                directory.rmdir()
    _remove_tree(transaction)


def recover_update(
    *,
    state_dir: Path | None = None,
    install_root: Path | None = None,
) -> None:
    resolved_state = state_dir or Path.home() / ".beatra"
    resolved_root = (install_root or _current_install_root()).resolve()
    update_home = _update_home(resolved_state, resolved_root)
    if (update_home / "transaction").exists():
        _rollback_transaction(update_home, resolved_root)


def _lock_update(update_home: Path, *, now: float) -> str | None:
    path = update_home / "update.lock"
    nonce = os.urandom(16).hex()
    for attempt in range(2):
        descriptor = -1
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                descriptor = -1
                json.dump(
                    {"schema_version": 1, "nonce": nonce, "created_at": now},
                    handle,
                    separators=(",", ":"),
                )
                handle.write("\n")
            return nonce
        except FileExistsError:
            try:
                current = json.loads(path.read_text(encoding="utf-8"))
                created = float(current["created_at"])
            except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
                try:
                    created = path.stat().st_mtime
                except OSError:
                    created = now
            if attempt == 0 and now - created > UPDATE_LOCK_MAX_AGE_SECONDS:
                path.unlink(missing_ok=True)
                continue
            return None
        finally:
            if descriptor >= 0:
                os.close(descriptor)
    return None


def _unlock_update(update_home: Path, nonce: str) -> None:
    path = update_home / "update.lock"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("nonce") == nonce:
            path.unlink(missing_ok=True)
    except (OSError, AttributeError, json.JSONDecodeError):
        return


def _ensure_owned_baseline(
    *,
    install_root: Path,
    update_home: Path,
    get_bytes: GetBytes,
    route: str | None = None,
) -> None:
    state = _read_update_state(update_home)
    if isinstance(state.get("owned_files"), dict):
        return
    version = PACKAGE_VERSION
    archive = f"{PACKAGE_SLUG}-skill-{version}.zip"
    base_url = PACKAGE_CDN_BASE_TEMPLATE.format(version=version)
    manifest_content = _update_get(
        f"{base_url}/skill-manifest.json",
        _cdn_url,
        route=route,
        timeout=UPDATE_DOWNLOAD_TIMEOUT_SECONDS,
        limit=MAX_UPDATE_MANIFEST_BYTES,
        get_bytes=get_bytes,
    )
    manifest = _json_object(manifest_content, "Beatra installed package manifest")
    archive_sha256 = manifest.get("archive_sha256")
    if not isinstance(archive_sha256, str) or _SHA256.fullmatch(archive_sha256) is None:
        raise RuntimeError("Beatra installed package manifest is invalid")
    manifest_files = _manifest_files(
        manifest,
        discovery={
            "version": version,
            "archive": archive,
            "archive_sha256": archive_sha256,
            "channel": PACKAGE_CHANNEL,
            "locale": PACKAGE_LOCALE,
        },
    )
    owned: dict[str, dict[str, Any]] = {}
    for relative, metadata in manifest_files.items():
        destination = _safe_destination(install_root, relative)
        if not destination.is_file():
            continue
        try:
            if _sha256(destination.read_bytes()) == metadata["sha256"]:
                owned[relative] = metadata
        except OSError:
            continue
    state["installed_version"] = version
    state["owned_files"] = owned
    _write_private_json(update_home / "state.json", state)


def _apply_update(
    *,
    install_root: Path,
    update_home: Path,
    discovery: dict[str, Any],
    manifest: dict[str, Any],
    new_files: dict[str, bytes],
) -> None:
    state = _read_update_state(update_home)
    previous_owned = state.get("owned_files")
    previous = previous_owned if isinstance(previous_owned, dict) else {}
    previous_paths = {
        relative
        for relative, metadata in previous.items()
        if isinstance(relative, str)
        and isinstance(metadata, dict)
        and isinstance(metadata.get("sha256"), str)
        and _SHA256.fullmatch(metadata["sha256"]) is not None
    }
    obsolete: list[str] = []
    for relative, metadata in previous.items():
        if relative in new_files or not isinstance(relative, str) or not isinstance(metadata, dict):
            continue
        destination = _safe_destination(install_root, relative)
        digest = metadata.get("sha256")
        if destination.is_file() and isinstance(digest, str):
            try:
                if _sha256(destination.read_bytes()) == digest:
                    obsolete.append(relative)
            except OSError:
                continue

    ordered_new = sorted(
        new_files,
        key=lambda path: (path == "scripts/mcp_client.py", path),
    )
    touched = [*ordered_new, *sorted(obsolete)]
    destinations = {relative: _safe_destination(install_root, relative) for relative in touched}
    collisions = [
        relative
        for relative in ordered_new
        if destinations[relative].exists() and relative not in previous_paths
    ]
    if collisions:
        raise RuntimeError(
            "Beatra update refused to replace an unowned installation file: "
            f"{collisions[0]}"
        )
    for directory in {_nearest_existing_parent(destination, install_root) for destination in destinations.values()}:
        _write_probe(directory)

    existing_bytes = sum(destination.stat().st_size for destination in destinations.values() if destination.exists())
    required_bytes = sum(len(content) for content in new_files.values()) + existing_bytes + 1024 * 1024
    try:
        if shutil.disk_usage(install_root).free < required_bytes:
            raise RuntimeError("Beatra package installation has insufficient free space")
    except OSError as exc:
        raise RuntimeError("Beatra package free space could not be verified") from exc

    transaction = update_home / "transaction"
    if transaction.exists():
        raise RuntimeError("Beatra update recovery is still pending")
    backup_root = transaction / "backup"
    _ensure_private_directory(backup_root)
    transaction_nonce = os.urandom(8).hex()
    entries: list[dict[str, Any]] = []
    created_dirs: set[str] = set()
    try:
        for relative in touched:
            destination = destinations[relative]
            existed = destination.exists()
            mode = stat.S_IMODE(os.lstat(destination).st_mode) if existed else 0o644
            entries.append({"path": relative, "existed": existed, "mode": mode})
            if existed:
                backup = backup_root / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(destination, backup)
            parent = destination.parent
            while parent != install_root and not parent.exists():
                created_dirs.add(parent.relative_to(install_root).as_posix())
                parent = parent.parent
        journal = {
            "schema_version": 1,
            "install_root": str(install_root),
            "nonce": transaction_nonce,
            "from_version": PACKAGE_VERSION,
            "to_version": discovery["version"],
            "entries": entries,
            "created_dirs": sorted(created_dirs, key=lambda value: (value.count("/"), value)),
        }
        _write_private_json(transaction / "journal.json", journal)
        for relative in journal["created_dirs"]:
            (install_root / relative).mkdir(exist_ok=True)
        for relative in ordered_new:
            destination = destinations[relative]
            _copy_to_destination(
                new_files[relative],
                destination,
                temporary=_transaction_temporary(destination, transaction_nonce),
            )
        for relative in obsolete:
            destinations[relative].unlink(missing_ok=True)
    except Exception as exc:
        try:
            _rollback_transaction(update_home, install_root)
        except Exception as recovery_exc:
            raise RuntimeError("Beatra update failed and requires recovery on the next start") from recovery_exc
        if isinstance(exc, RuntimeError):
            raise
        raise RuntimeError("Beatra update could not replace the package safely") from exc

    _remove_tree(transaction)
    files = manifest.get("files")
    owned = {
        str(item["path"])[len(PACKAGE_SLUG) + 1 :]: {
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        for item in files
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    state["installed_version"] = discovery["version"]
    state["owned_files"] = owned
    with suppress(OSError):
        _write_private_json(update_home / "state.json", state)
        # Package bytes are already committed and independently verifiable.
        # Losing this local cache only means obsolete files are preserved on a
        # future update; it must not turn a successful update into a rollback.


def update_package(
    *,
    state_dir: Path | None = None,
    install_root: Path | None = None,
    get_bytes: GetBytes = _default_get_bytes,
) -> dict[str, Any]:
    resolved_state = state_dir or Path.home() / ".beatra"
    resolved_root = (install_root or _current_install_root()).resolve()
    if not resolved_root.is_dir():
        raise RuntimeError("Beatra package installation path is invalid")
    update_home = _update_home(resolved_state, resolved_root)
    route = current_route(resolved_state)
    nonce = _lock_update(update_home, now=time.time())
    if nonce is None:
        raise RuntimeError("Another Beatra package update is already running")
    try:
        recover_update(state_dir=resolved_state, install_root=resolved_root)
        checked = check_update(get_bytes=get_bytes, route=route)
        if not checked["update_available"]:
            return checked
        _ensure_owned_baseline(
            install_root=resolved_root,
            update_home=update_home,
            get_bytes=get_bytes,
            route=route,
        )
        discovery = checked["discovery"]
        manifest, new_files = download_update(discovery, get_bytes=get_bytes, route=route)
        _apply_update(
            install_root=resolved_root,
            update_home=update_home,
            discovery=discovery,
            manifest=manifest,
            new_files=new_files,
        )
        return checked
    finally:
        _unlock_update(update_home, nonce)


def maybe_auto_update(
    *,
    state_dir: Path | None = None,
    install_root: Path | None = None,
    get_bytes: GetBytes = _default_get_bytes,
    now: float | None = None,
) -> bool:
    """Best-effort silent update. Never block the requested MCP command."""

    resolved_state = state_dir or Path.home() / ".beatra"
    try:
        resolved_root = (install_root or _current_install_root()).resolve()
        update_home = _update_home(resolved_state, resolved_root)
        route = current_route(resolved_state)
        observed_at = time.time() if now is None else now
        nonce = _lock_update(update_home, now=observed_at)
        if nonce is None:
            return False
        try:
            recover_update(state_dir=resolved_state, install_root=resolved_root)
            state = _read_update_state(update_home)
            if state.get("auto_update", True) is False:
                return False
            last_checked = state.get("last_checked_at")
            if (
                isinstance(last_checked, (int, float))
                and observed_at - float(last_checked) < UPDATE_CHECK_MAX_AGE_SECONDS
            ):
                return False
            state["last_checked_at"] = observed_at
            _write_private_json(update_home / "state.json", state)
            checked = check_update(get_bytes=get_bytes, route=route)
            if not checked["update_available"]:
                return False
            _ensure_owned_baseline(
                install_root=resolved_root,
                update_home=update_home,
                get_bytes=get_bytes,
                route=route,
            )
            discovery = checked["discovery"]
            manifest, new_files = download_update(discovery, get_bytes=get_bytes, route=route)
            _apply_update(
                install_root=resolved_root,
                update_home=update_home,
                discovery=discovery,
                manifest=manifest,
                new_files=new_files,
            )
            return True
        finally:
            _unlock_update(update_home, nonce)
    except Exception:
        return False


def _credentials(state_dir: Path) -> tuple[str, str]:
    state_dir = state_dir.expanduser()
    path = state_dir / "credentials.json"
    if not path.is_file():
        # Not connected yet (or the file is gone): the caller may still find
        # an approval waiting to be collected.
        raise CredentialsMissing(f"Beatra credentials are missing. {RECONNECT_GUIDANCE}")
    try:
        value = json.loads(_read_private_credentials(state_dir, path))
        mcp_url = value["mcp_url"]
        token = value["access_token"]
        token_type = value["token_type"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise CredentialsMissing(f"Beatra credentials are missing. {RECONNECT_GUIDANCE}") from exc
    if (
        not isinstance(mcp_url, str)
        or mcp_url != CANONICAL_MCP_URL
        or not isinstance(token, str)
        or not token
        or token_type != "Bearer"
    ):
        raise CredentialsMissing("Beatra credential file is invalid; authorize again")
    return mcp_url, token


def _read_private_credentials(state_dir: Path, path: Path) -> str:
    if os.name == "nt":
        # The state directory lives under the user profile, whose default
        # ACL is already private to the user (the gh/aws/gcloud posture).
        # The former custom DACL verification was dropped deliberately: its
        # command patterns read as hostile to agent safety policies and
        # endpoint security, failing installs while adding nothing an
        # elevated administrator could not bypass.
        return path.read_text(encoding="utf-8")
    if os.name != "posix":
        raise RuntimeError("Beatra credential permissions are unsupported on this platform")
    try:
        directory_stat = os.lstat(state_dir)
        if (
            not stat.S_ISDIR(directory_stat.st_mode)
            or stat.S_IMODE(directory_stat.st_mode) != 0o700
            or directory_stat.st_uid != os.getuid()
        ):
            raise RuntimeError("Beatra credential permissions are unsafe; authorize again")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        try:
            file_stat = os.fstat(descriptor)
            if (
                not stat.S_ISREG(file_stat.st_mode)
                or stat.S_IMODE(file_stat.st_mode) != 0o600
                or file_stat.st_uid != os.getuid()
            ):
                raise RuntimeError("Beatra credential permissions are unsafe; authorize again")
            with os.fdopen(descriptor, encoding="utf-8") as handle:
                descriptor = -1
                return handle.read()
        finally:
            if descriptor >= 0:
                os.close(descriptor)
    except RuntimeError:
        raise
    except OSError as exc:
        raise RuntimeError("Beatra credential permissions are unsafe; authorize again") from exc


def _message_result(body: dict[str, Any] | None, request_id: int) -> dict[str, Any]:
    if body is None or body.get("jsonrpc") != "2.0" or body.get("id") != request_id:
        raise RuntimeError("Beatra MCP returned an invalid protocol response")
    error = body.get("error")
    if isinstance(error, dict):
        code = error.get("code")
        raise RuntimeError(f"Beatra MCP protocol request failed ({code})")
    result = body.get("result")
    if not isinstance(result, dict):
        raise RuntimeError("Beatra MCP returned an invalid protocol response")
    return result


def _tool_failure_message(result: dict[str, Any]) -> str | None:
    """Return complete agent-readable diagnostics for tool or terminal Task failure."""

    structured = result.get("structuredContent")
    structured_mapping = structured if isinstance(structured, dict) else {}
    task = structured_mapping.get("task")
    task_mapping = task if isinstance(task, dict) else {}
    is_tool_error = result.get("isError") is True
    status = structured_mapping.get("status") or task_mapping.get("status")
    if not is_tool_error and status != "failed":
        return None

    error = structured_mapping.get("error")
    if not isinstance(error, dict):
        error = task_mapping.get("error")
    content = result.get("content")
    content_items = content if isinstance(content, list) else []
    readable = " ".join(
        str(item["text"])
        for item in content_items
        if isinstance(item, dict)
        and item.get("type") == "text"
        and isinstance(item.get("text"), str)
    )
    details = (
        json.dumps(error, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        if isinstance(error, dict)
        else ""
    )
    if readable and details:
        return f"{readable} {details}"
    if readable:
        return readable
    if details:
        return details
    return "Beatra tool call failed without structured diagnostics."


_HOST_PLATFORM: str | None = None


def host_platform(state_dir: Path | None = None) -> str:
    """The agent environment this process runs inside, resolved once per
    process (docs/device-model.md): env signatures > host.json written at
    authorize time > unknown. Never a per-request cost."""
    global _HOST_PLATFORM
    if _HOST_PLATFORM is None:
        _HOST_PLATFORM = _detect_host_platform(state_dir or Path.home() / ".beatra")
    return _HOST_PLATFORM


def _detect_host_platform(state_dir: Path) -> str:
    env = os.environ
    if env.get("CLAUDECODE") == "1" or "CLAUDE_CODE_ENTRYPOINT" in env:
        return "claude-code"
    if any(key.startswith("CODEX_") for key in env):
        return "codex"
    ai_agent = env.get("AI_AGENT", "").lower()
    matched = re.match(r"([a-z0-9-]+)_", ai_agent)
    if matched and _PLATFORM_VALUE.fullmatch(matched.group(1)):
        return matched.group(1)
    try:
        value = json.loads((state_dir / "host.json").read_text(encoding="utf-8"))
        candidate = value.get("platform")
        if isinstance(candidate, str) and _PLATFORM_VALUE.fullmatch(candidate):
            return candidate
    except (OSError, ValueError, AttributeError):
        pass
    return "unknown"


class Session:
    def __init__(self, *, state_dir: Path, post_json: PostJson) -> None:
        _identity_url, token = _credentials(state_dir)
        self.url = route_mcp_url(current_route(state_dir))
        self.headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        }
        token = ""
        self.post_json = post_json

    def send(self, payload: dict[str, Any], timeout: float = 60.0) -> tuple[int, dict[str, Any] | None]:
        status, response_headers, body = self.post_json(self.url, dict(self.headers), payload, timeout)
        session_id = next(
            (value for name, value in response_headers.items() if name.lower() == "mcp-session-id"),
            None,
        )
        if session_id:
            self.headers["MCP-Session-Id"] = session_id
        return status, body

    def initialize(self) -> None:
        status, body = self.send(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": CLIENT_INFO,
                },
            }
        )
        _require_status(status, {200}, "Beatra MCP initialize")
        result = _message_result(body, 1)
        negotiated_version = result.get("protocolVersion")
        if negotiated_version != PROTOCOL_VERSION:
            raise RuntimeError("Beatra MCP returned an unsupported protocol version")
        self.headers["MCP-Protocol-Version"] = negotiated_version
        status, _ = self.send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        _require_status(status, {200, 202}, "Beatra MCP initialization")

    def request(
        self,
        request_id: int,
        method: str,
        params: dict[str, Any],
        timeout: float = 60.0,
    ) -> dict[str, Any]:
        if method == "tools/call":
            arguments = params.get("arguments")
            if isinstance(arguments, dict):
                # Source attribution (docs/device-model.md): every business call
                # names the package and host environment that initiated it. The
                # server strips these before schema validation; they never
                # change a retry's idempotency identity.
                arguments.setdefault("source_package_slug", PACKAGE_SLUG)
                arguments.setdefault("source_platform", host_platform())
        status, body = self.send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            },
            timeout,
        )
        _require_status(status, {200}, "Beatra MCP request")
        return _message_result(body, request_id)


def _registration_reference(state_dir: Path) -> str:
    try:
        value = json.loads((state_dir / "installation.json").read_text(encoding="utf-8"))
        reference = value["external_installation_ref"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Beatra installation state is invalid; authorize again") from exc
    if not isinstance(reference, str) or not reference.startswith("beatra:"):
        raise RuntimeError("Beatra installation state is invalid; authorize again")
    return reference


def _small_regular_json(path: Path, limit: int) -> Any:
    """The JSON value of a regular file no larger than `limit` bytes, else None.
    Symbolic links, directories, oversized or undecodable files are ignored."""

    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            return None
        with path.open("rb") as handle:
            raw = handle.read(limit + 1)
    except OSError:
        return None
    if len(raw) > limit:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, RecursionError):
        return None


def _channel_identity() -> tuple[str, str] | None:
    """The channel and locale fixed at build time, when this build has a real
    one (the WorkBuddy connector keeps placeholders and reports none)."""

    channel = globals().get("PACKAGE_CHANNEL")
    locale_name = globals().get("PACKAGE_LOCALE")
    if (
        isinstance(channel, str)
        and isinstance(locale_name, str)
        and _CHANNEL_VALUE.fullmatch(channel)
        and _LOCALE_TAG.fullmatch(locale_name)
    ):
        return channel, locale_name
    return None


def _route_report(state_dir: Path) -> tuple[str, str] | None:
    policy = route_policy()
    if policy != "auto":
        return policy, "channel"
    record = _read_network(state_dir)
    route = record.get("route")
    if route not in ROUTE_HOSTS:
        return None
    if record.get("pinned") is True:
        return route, "pinned"
    basis = record.get("basis")
    return (route, basis) if basis in _ROUTE_BASES else None


def _os_release(system: str | None) -> str | None:
    if system == "darwin":
        # macOS only. On Windows the platform module may query WMI or start a
        # shell, which endpoint security reads as reconnaissance (spec §7).
        import platform

        return platform.mac_ver()[0] or None
    if system == "windows":
        version = sys.getwindowsversion()
        return f"{version.major}.{version.minor}.{version.build}"
    if system == "linux":
        return os.uname().release
    return None


def _environment() -> dict[str, Any]:
    """Coarse runtime facts for distribution analytics (spec §7): no user name,
    path, environment variable or address. A fact outside the shape Beatra
    records is left out rather than sent."""

    facts: dict[str, Any] = {}
    system = _OS_NAMES.get(sys.platform) or ("linux" if sys.platform.startswith("linux") else None)
    if system is not None:
        facts["os"] = system
    with suppress(Exception):
        release = _os_release(system)
        if isinstance(release, str) and _OS_VERSION.fullmatch(release):
            facts["os_version"] = release
    with suppress(Exception):
        arch = sysconfig.get_platform().lower()
        if _ARCH_VALUE.fullmatch(arch):
            facts["arch"] = arch
    facts["python"] = ".".join(str(part) for part in sys.version_info[:3])
    with suppress(Exception):
        language = locale.getlocale()[0]
        if isinstance(language, str):
            tag = language.replace("_", "-")
            if _LOCALE_TAG.fullmatch(tag):
                facts["locale"] = tag
    with suppress(Exception):
        offset = datetime.now().astimezone().utcoffset()
        if offset is not None:
            minutes = int(offset.total_seconds() // 60)
            if -720 <= minutes <= 840:
                facts["tz_offset_minutes"] = minutes
    return facts


def _own_install_root() -> Path | None:
    try:
        return _current_install_root()
    except RuntimeError:
        return None


def _stamped_source(install_root: Path) -> str | None:
    """The `install-source.json` Beatra adds to a copy it hands to a store or
    site (spec §6.1). It is in no manifest, so updates leave it in place."""

    value = _small_regular_json(install_root / INSTALL_SOURCE_FILE, MAX_INSTALL_SOURCE_BYTES)
    if isinstance(value, dict) and value.get("schema_version") == 1 and value.get("source") in INSTALL_SOURCES:
        return value["source"]
    return None


def _store_marker_source(install_root: Path) -> str | None:
    """A store client's own record inside this installation, for the stores
    whose record format is verified (spec §6.3: ClawHub only)."""

    for relative in _CLAWHUB_ORIGINS:
        value = _small_regular_json(install_root / relative, MAX_LOCAL_RECORD_BYTES)
        if value is None:
            continue  # unreadable or unparsable: the CLI tries the legacy name
        # A file that parses decides, as in the CLI's `readSkillOrigin`.
        if not isinstance(value, dict) or value.get("version") != 1:
            return None
        installed_at = value.get("installedAt")
        if (
            all(isinstance(value.get(key), str) and value[key] for key in ("registry", "slug", "installedVersion"))
            and isinstance(installed_at, (int, float))
            and not isinstance(installed_at, bool)
            and math.isfinite(installed_at)
        ):
            return "github" if value.get("sourceKind") == "skills-sh" else "clawhub"
        return None
    return None


def _read_source_record(update_home: Path) -> dict[str, Any] | None:
    value = _small_regular_json(update_home / SOURCE_RECORD_FILE, MAX_LOCAL_RECORD_BYTES)
    if not isinstance(value, dict):
        return None
    basis, source = value.get("basis"), value.get("value")
    if not isinstance(basis, str) or not isinstance(source, str) or basis not in _SOURCE_BASIS_RANK:
        return None
    if source in INSTALL_SOURCES or (source == "other" and basis == "inferred"):
        return value
    return None


def record_install_source(value: str, basis: str, *, update_home: Path, now: float) -> dict[str, Any]:
    """Keep the strongest evidence (spec §6.3): a stamp always wins because the
    file is the current fact; otherwise only a stronger basis replaces."""

    stored = _read_source_record(update_home)
    if stored is not None:
        same = stored["value"] == value and stored["basis"] == basis
        not_stronger = _SOURCE_BASIS_RANK[basis] <= _SOURCE_BASIS_RANK[stored["basis"]]
        if same or (basis != "stamp" and not_stronger):
            return stored
    record = {"value": value, "basis": basis, "recorded_at": int(now)}
    _write_private_json(update_home / SOURCE_RECORD_FILE, record)
    return record


def _install_source(state_dir: Path, install_root: Path, *, now: float) -> tuple[str, str] | None:
    # Evidence in the installation decides, even when the state directory is
    # read-only; saving the record is best effort (spec §6.3).
    stamped = _stamped_source(install_root)
    marker = None if stamped is not None else _store_marker_source(install_root)
    found = (stamped, "stamp") if stamped is not None else (marker, "store_marker") if marker is not None else None
    if found is not None:
        with suppress(Exception):
            kept = record_install_source(found[0], found[1], update_home=_update_home(state_dir, install_root), now=now)
            return kept["value"], kept["basis"]
        return found
    record = _read_source_record(_update_home(state_dir, install_root))
    return (record["value"], record["basis"]) if record else None


def guess_install_source(
    value: str,
    *,
    state_dir: Path | None = None,
    install_root: Path | None = None,
    now: float | None = None,
) -> dict[str, Any]:
    """`install-source --guess`: the agent's reading of how this Skill was
    installed, from the conversation. It never replaces a stamp or a store
    record (spec §6.3)."""

    if value not in GUESSABLE_SOURCES:
        raise RuntimeError("Unknown install source")
    resolved_state = state_dir or Path.home() / ".beatra"
    root = (install_root or _current_install_root()).resolve()
    observed = time.time() if now is None else now
    return record_install_source(value, "inferred", update_home=_update_home(resolved_state, root), now=observed)


def _registration_arguments(
    state_dir: Path,
    install_root: Path | None,
    *,
    now: float,
) -> dict[str, Any]:
    arguments: dict[str, Any] = {
        "package_slug": PACKAGE_SLUG,
        "package_version": PACKAGE_VERSION,
        "platform": host_platform(state_dir),
        "external_installation_ref": _registration_reference(state_dir),
    }
    identity = _channel_identity()
    if identity is not None:
        arguments["channel"], arguments["channel_locale"] = identity
    with suppress(Exception):
        route = _route_report(state_dir)
        if route is not None:
            arguments["route"], arguments["route_basis"] = route
    if install_root is not None:
        with suppress(Exception):
            source = _install_source(state_dir, install_root, now=now)
            if source is not None:
                arguments["install_source"], arguments["install_source_basis"] = source
    with suppress(Exception):
        environment = _environment()
        if environment:
            arguments["environment"] = environment
    return arguments


def _registration_key(arguments: dict[str, Any]) -> dict[str, Any]:
    return {key: arguments.get(key) for key in _REGISTRATION_KEY}


def _registration_is_fresh(
    state_dir: Path,
    install_root: Path,
    arguments: dict[str, Any],
    *,
    now: float,
) -> bool:
    value = _small_regular_json(
        _update_home(state_dir, install_root) / REGISTRATION_CACHE_FILE, MAX_LOCAL_RECORD_BYTES
    )
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return False
    registered_at = value.get("registered_at")
    return (
        value.get("key") == _registration_key(arguments)
        and isinstance(registered_at, (int, float))
        and not isinstance(registered_at, bool)
        and now - float(registered_at) < REGISTRATION_MAX_AGE_SECONDS
    )


def _write_registration_cache(
    state_dir: Path,
    install_root: Path,
    arguments: dict[str, Any],
    *,
    now: float,
    recognized: bool | None,
) -> None:
    _write_private_json(
        _update_home(state_dir, install_root) / REGISTRATION_CACHE_FILE,
        {
            "schema_version": 1,
            "key": _registration_key(arguments),
            "registered_at": now,
            "recognized": recognized,
        },
    )


def _record_skill_inventory(state_dir: Path) -> None:
    """Keep this package present in the device-local skill inventory.

    ~/.beatra/skills.json is what the uninstall flow consults before it may
    revoke the shared credential — recording on every use (not only at
    authorize time) means an install that skipped or predates the authorize
    step still becomes visible before anyone decides it does not exist.
    Best-effort: inventory failure never blocks the requested operation.
    """

    try:
        try:
            root = Path(__file__).resolve().parent.parent
        except NameError:
            return
        resolved = str(root)
        path = state_dir / "skills.json"
        entries: list[dict[str, Any]] = []
        if path.exists():
            value = json.loads(path.read_text(encoding="utf-8"))
            loaded = value.get("skills") if isinstance(value, dict) else None
            if isinstance(loaded, list):
                entries = [entry for entry in loaded if isinstance(entry, dict)]
        if any(
            entry.get("slug") == PACKAGE_SLUG and entry.get("install_path") == resolved
            for entry in entries
        ):
            return
        entries.append(
            {
                "slug": PACKAGE_SLUG,
                "platform": host_platform(state_dir),
                "install_path": resolved,
                "recorded_at": datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            }
        )
        temporary = path.with_name(f".{path.name}.inventory.tmp")
        temporary.write_text(
            json.dumps(
                {"schema_version": 1, "skills": entries},
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
        with suppress(OSError):
            temporary.chmod(0o600)
        temporary.replace(path)
    except Exception:
        pass


def register_installation(
    session: Session,
    *,
    state_dir: Path,
    now: float | None = None,
    install_root: Path | None = None,
) -> None:
    """Best-effort registration of this installation (spec 2026-10-09 §7), the
    one report the Skill sends: package, channel, network route, install source
    and coarse runtime facts. It never blocks the requested creative operation."""

    _record_skill_inventory(state_dir)
    observed_at = time.time() if now is None else now
    try:
        root = install_root or _own_install_root()
        arguments = _registration_arguments(state_dir, root, now=observed_at)
        cached = dict(arguments)
        fresh = False
        if root is not None:
            # An unreadable or unwritable state directory means "not fresh":
            # the registration is still sent.
            with suppress(Exception):
                fresh = _registration_is_fresh(state_dir, root, cached, now=observed_at)
        if fresh:
            return
        result = session.request(
            2,
            "tools/call",
            {"name": "beatra.installations.register", "arguments": arguments},
            # Registration does not get the business-call time budget: a
            # degraded backend may cost the user at most this long, once per
            # cache window, before their real work proceeds.
            timeout=REGISTRATION_TIMEOUT_SECONDS,
        )
        if _tool_failure_message(result):
            return
        structured = result.get("structuredContent")
        recognized = structured.get("recognized") if isinstance(structured, dict) else None
        if root is not None:
            # The cache is best effort; its failure never undoes a sent registration.
            with suppress(Exception):
                _write_registration_cache(
                    state_dir,
                    root,
                    cached,
                    now=observed_at,
                    recognized=recognized if isinstance(recognized, bool) else None,
                )
    except Exception:
        # Registration is deliberately best effort. No transport, protocol,
        # cache, or future client error may block the creative call that follows.
        return


def _session_with_registration(
    *,
    state_dir: Path,
    post_json: PostJson,
) -> Session:
    session = Session(state_dir=state_dir, post_json=post_json)
    session.initialize()
    register_installation(session, state_dir=state_dir)
    return session


def verify(
    *,
    state_dir: Path | None = None,
    post_json: PostJson = _default_post_json,
) -> None:
    resolved_state_dir = state_dir or Path.home() / ".beatra"
    session = _session_with_registration(state_dir=resolved_state_dir, post_json=post_json)
    result = session.request(
        2,
        "tools/call",
        {"name": "beatra.tasks.list", "arguments": {}},
    )
    if failure := _tool_failure_message(result):
        raise RuntimeError(f"Beatra connection verification was rejected: {failure}")
    print("Beatra connection verified with the non-billable task list.")


def upload(
    path: Path,
    *,
    mime_type: str,
    state_dir: Path | None = None,
    post_json: PostJson = _default_post_json,
    put_bytes: PutBytes = _default_put_bytes,
) -> dict[str, str]:
    if re.fullmatch(r"[a-z0-9][a-z0-9.+-]*/[a-z0-9][a-z0-9.+-]*", mime_type) is None:
        raise RuntimeError("Local upload MIME type is invalid")
    filename, content = _read_local_upload(path)
    resolved_state_dir = state_dir or Path.home() / ".beatra"
    session = _session_with_registration(state_dir=resolved_state_dir, post_json=post_json)
    result = session.request(
        2,
        "tools/call",
        {
            "name": "beatra.assets.upload",
            "arguments": {
                "filename": filename,
                "mime_type": mime_type,
                "size_bytes": len(content),
            },
        },
    )
    if failure := _tool_failure_message(result):
        raise RuntimeError(f"Beatra rejected the upload grant request: {failure}")
    return _complete_upload(
        result,
        mime_type=mime_type,
        content=content,
        put_bytes=put_bytes,
    )


def _read_tool_arguments() -> dict[str, Any]:
    try:
        arguments = json.load(os.sys.stdin)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Tool arguments on stdin must be one JSON object") from exc
    if not isinstance(arguments, dict):
        raise RuntimeError("Tool arguments on stdin must be one JSON object")
    return arguments


def _run_command(
    command: str,
    tool_name: str | None = None,
    arguments: dict[str, Any] | None = None,
) -> dict[str, Any]:
    session = _session_with_registration(
        state_dir=Path.home() / ".beatra",
        post_json=_default_post_json,
    )
    if command == "tools":
        return session.request(2, "tools/list", {})
    if arguments is None:
        arguments = _read_tool_arguments()
    assert tool_name is not None
    return session.request(
        2,
        "tools/call",
        {"name": tool_name, "arguments": arguments},
    )


CollectApproval = Callable[[Path], tuple[str, str | None]]


def _default_collect_approval(state_dir: Path) -> tuple[str, str | None]:
    """The helper's one-check collection, when this package has it."""

    import authorize  # the package's own helper, beside this file

    collect = getattr(authorize, "collect_saved_approval", None)
    if collect is None:
        return "none", None
    return collect(state_dir)


def _connect_waiting_approval(
    state_dir: Path,
    collect: CollectApproval | None = None,
) -> tuple[str, str | None]:
    """Before giving up on a call with no working credential: an approval the
    user already gave on this computer may be waiting to be collected (the
    agent was stopped while they selected Allow). One quick check; anything
    unexpected reads as nothing waiting, so the call fails as it always did."""

    try:
        outcome, link = (collect or _default_collect_approval)(state_dir)
    except Exception:
        return "none", None
    if outcome not in {"collected", "pending", "unreachable", "none"}:
        return "none", None
    return outcome, link


def _with_waiting_approval(
    operation: Callable[[], T],
    *,
    state_dir: Path,
    collect: CollectApproval | None = None,
) -> T:
    """Run one command; if it has no working credential, collect an approval
    that is waiting and run it once more."""

    try:
        return operation()
    except (AuthenticationRequired, CredentialsMissing) as exc:
        outcome, link = _connect_waiting_approval(state_dir, collect)
        if outcome == "collected":
            return operation()
        if outcome == "pending" and link:
            raise AuthenticationRequired(
                f"{AUTH_REQUIRED_CODE}: Beatra is waiting for the user to select Allow on "
                f"the approval page: {link}\nShow this link to the user if you have not "
                "already, then run `python3 scripts/authorize.py`: it continues this same "
                "approval and waits for Allow."
            ) from exc
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Beatra through Streamable HTTP")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("verify", help="Run the non-billable connection check")
    subparsers.add_parser("tools", help="List available Beatra tools")
    call = subparsers.add_parser("call", help="Call one tool with a JSON object on stdin")
    call.add_argument("tool_name")
    local_upload = subparsers.add_parser(
        "upload",
        help="Upload one local regular file and print its artifact reference",
    )
    local_upload.add_argument("path", type=Path)
    local_upload.add_argument(
        "--mime-type",
        required=True,
        help="Exact media MIME type, such as image/png, audio/mpeg, or video/mp4",
    )
    update = subparsers.add_parser(
        "update",
        help="Check, install, or configure Beatra package self-updates",
    )
    update.add_argument(
        "--check",
        action="store_true",
        help="Check the official discovery document without changing files",
    )
    update.add_argument(
        "--auto",
        choices=("on", "off"),
        help="Enable or disable automatic silent updates for this installation",
    )
    network = subparsers.add_parser("network", help="Show or choose the Beatra network this computer uses")
    network.add_argument(
        "--use",
        choices=("cn", "ai", "auto"),
        help="Keep the mainland China (cn) or international (ai) network until --use auto",
    )
    source = subparsers.add_parser(
        "install-source",
        help="Record where this Skill was installed from, when the conversation shows it",
    )
    source.add_argument("--guess", required=True, choices=GUESSABLE_SOURCES)
    args = parser.parse_args()
    try:
        state_dir = Path.home() / ".beatra"
        # One route decision per process, before the update check and any
        # request (spec §5.2).
        resolve_route(state_dir)
        if args.command == "update":
            if args.check and args.auto is not None:
                raise RuntimeError("Use either --check or --auto, not both")
            if args.auto is not None:
                enabled = args.auto == "on"
                set_auto_update(enabled)
                print(f"Automatic Beatra package updates are {'enabled' if enabled else 'disabled'}.")
            elif args.check:
                checked = check_update()
                if checked["update_available"]:
                    print(
                        "Beatra package update available: "
                        f"{checked['current_version']} -> {checked['available_version']}."
                    )
                else:
                    print(f"Beatra package is current at {checked['current_version']}.")
            else:
                checked = update_package()
                if checked["update_available"]:
                    print(
                        "Beatra package updated to "
                        f"{checked['available_version']}; the next process will use it."
                    )
                else:
                    print(f"Beatra package is current at {checked['current_version']}.")
        elif args.command == "network":
            _network_command(args.use, state_dir)
        elif args.command == "install-source":
            try:
                recorded = guess_install_source(args.guess, state_dir=state_dir)
            except OSError as exc:
                raise RuntimeError(f"Could not save the install source: {exc}") from exc
            if (recorded["value"], recorded["basis"]) == (args.guess, "inferred"):
                print(f"Recorded where this Skill was installed from: {args.guess}.")
            else:
                print(f"Kept the recorded install source: {recorded['value']} ({recorded['basis']}).")
        else:
            maybe_auto_update()
        if args.command == "verify":
            _with_waiting_approval(verify, state_dir=state_dir)
        elif args.command == "upload":
            result = _with_waiting_approval(
                lambda: upload(args.path, mime_type=args.mime_type),
                state_dir=state_dir,
            )
            print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        elif args.command in {"tools", "call"}:
            # Read once: a call retried after collecting an approval reuses them.
            arguments = _read_tool_arguments() if args.command == "call" else None
            result = _with_waiting_approval(
                lambda: _run_command(args.command, getattr(args, "tool_name", None), arguments),
                state_dir=state_dir,
            )
            print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
            if failure := _tool_failure_message(result):
                print(failure, file=os.sys.stderr)
                return 1
    except AuthenticationRequired as exc:
        print(str(exc), file=os.sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=os.sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # authorize.py's `import mcp_client` must get this running module, not run
    # a second copy that cannot see the route this process decided (one host
    # per process, spec §5.5).
    os.sys.modules["mcp_client"] = os.sys.modules[__name__]
    raise SystemExit(main())
