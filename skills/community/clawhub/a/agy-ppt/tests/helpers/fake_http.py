#!/usr/bin/env python3
"""Deterministic fake HTTP transport for the Phase 13.5 acquisition tests.

Nothing here opens a socket, resolves a real hostname, or reaches the internet,
so the ordinary unit suite never depends on network or DNS availability.

``FakeOpener`` mimics the small slice of ``urllib.request.OpenerDirector`` that
``source_acquisition`` actually uses: ``open(request, timeout=...)`` returning a
context-manager response with ``status``, ``headers``, ``url`` and an
incremental ``read(size)``. Redirects are surfaced the same way the real
no-redirect opener surfaces them: as an ``HTTPError`` carrying ``Location``.
"""

from __future__ import annotations

import email.message
import io
import socket
import urllib.error
from dataclasses import dataclass, field
from typing import Any


def make_headers(pairs: dict[str, str] | None = None) -> email.message.Message:
    """A real ``Message`` so header lookups behave like urllib's."""
    message = email.message.Message()
    for key, value in (pairs or {}).items():
        message[key] = value
    return message


class FakeResponse:
    """Minimal urllib-like response with incremental reads."""

    def __init__(
        self,
        body: bytes,
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
        url: str = "",
        chunk_size: int | None = None,
        read_timeout_after: int | None = None,
    ) -> None:
        self.status = status
        self.code = status
        self.headers = make_headers(headers)
        self.url = url
        self._stream = io.BytesIO(body)
        self._chunk_size = chunk_size
        self._read_timeout_after = read_timeout_after
        self._reads = 0
        self.closed = False

    def read(self, size: int = -1) -> bytes:
        self._reads += 1
        if (
            self._read_timeout_after is not None
            and self._reads > self._read_timeout_after
        ):
            raise socket.timeout("fake read timeout")
        if self._chunk_size is not None and size and size > 0:
            size = min(size, self._chunk_size)
        return self._stream.read(size)

    def close(self) -> None:
        self.closed = True

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


@dataclass
class FakeOpener:
    """Serves scripted responses keyed by URL, recording every request.

    ``routes`` maps a URL to either a :class:`FakeResponse`, a
    :class:`urllib.error.HTTPError` (for redirects and HTTP failures), or an
    exception instance to raise.
    """

    routes: dict[str, Any] = field(default_factory=dict)
    requested: list[str] = field(default_factory=list)
    default: Any | None = None

    def open(self, request: Any, timeout: float | None = None):  # noqa: A003
        url = request.full_url if hasattr(request, "full_url") else str(request)
        self.requested.append(url)
        outcome = self.routes.get(url, self.default)
        if outcome is None:
            raise AssertionError(f"FakeOpener has no route for {url!r}")
        if isinstance(outcome, BaseException):
            raise outcome
        if callable(outcome) and not isinstance(outcome, FakeResponse):
            outcome = outcome()
            if isinstance(outcome, BaseException):
                raise outcome
        if isinstance(outcome, FakeResponse) and not outcome.url:
            outcome.url = url
        return outcome


def redirect(location: str, *, status: int = 302, url: str = "") -> urllib.error.HTTPError:
    """An HTTPError shaped like a blocked-redirect response."""
    return urllib.error.HTTPError(
        url or "http://example.test/",
        status,
        "Found",
        make_headers({"Location": location}),
        io.BytesIO(b""),
    )


def http_error(status: int, *, url: str = "") -> urllib.error.HTTPError:
    """An HTTPError for a non-success final response."""
    return urllib.error.HTTPError(
        url or "http://example.test/",
        status,
        "Error",
        make_headers({}),
        io.BytesIO(b"<html>error page</html>"),
    )


def public_resolver(*_args: object, **_kwargs: object) -> list[tuple]:
    """Resolver stub that always returns one public address."""
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]


def resolver_for(mapping: dict[str, str]):
    """Resolver stub returning a chosen address per hostname."""

    def resolve(host: str, *_args: object, **_kwargs: object) -> list[tuple]:
        address = mapping.get(host)
        if address is None:
            raise socket.gaierror(f"no fake DNS entry for {host!r}")
        family = socket.AF_INET6 if ":" in address else socket.AF_INET
        return [(family, socket.SOCK_STREAM, 6, "", (address, 0))]

    return resolve
