from __future__ import annotations

import json
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

from .common import APIError, Conflict, ManagerError, NetworkError, canonical
from . import __version__

API_BASE = "https://api.flowus.cn/v2"
MAX_FILE = 100 * 1024 * 1024


def check_file_url(url: str):
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.port not in (None, 443)
            or not any(host == suffix or host.endswith("." + suffix)
                       for suffix in ("flowus.cn", "flowus.app", "myqcloud.com", "aliyuncs.com"))):
        raise ManagerError("File URL is outside the documented FlowUs storage hosts")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ManagerError("Unexpected redirect; refusing to forward credentials or file data")


def connection_error(exc, network_mode, operation):
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, ssl.SSLCertVerificationError):
        kind = "tls_certificate"
    elif isinstance(reason, ssl.SSLEOFError):
        kind = "tls_eof"
    elif isinstance(reason, ssl.SSLError):
        kind = "tls"
    elif isinstance(reason, socket.gaierror):
        kind = "dns"
    elif isinstance(reason, (TimeoutError, socket.timeout)):
        kind = "timeout"
    else:
        kind = "network"
    return NetworkError(kind, network_mode, operation=operation)


def build_opener(network_mode):
    if network_mode not in ("system", "direct"):
        raise ManagerError("network_mode must be system or direct")
    context = ssl.create_default_context()
    context.set_alpn_protocols(["http/1.1"])
    handlers = [NoRedirect(), urllib.request.HTTPSHandler(context=context)]
    if network_mode == "direct":
        # Explicit per-tool opt-in. Never silently retry through a different network route.
        handlers.append(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener(*handlers)


class HTTP:
    """Only API requests receive credentials. Object storage requests never do."""

    def __init__(self, credential: str, *, opener=None, sleep=time.sleep, network_mode="system"):
        if not credential:
            raise ManagerError("Missing FlowUs environment credential; see setup instructions")
        self._credential = credential
        if network_mode not in ("system", "direct"):
            raise ManagerError("network_mode must be system or direct")
        self.network_mode = network_mode
        self.opener = opener or build_opener(network_mode)
        self.sleep = sleep

    def request(self, method, path, body=None, *, etag=None, idempotency=None):
        if not path.startswith("/") or "://" in path or ".." in path:
            raise ManagerError("Invalid API resource path")
        headers = {"Authorization": "Bearer " + self._credential, "Accept": "application/json",
                   "User-Agent": "flowus-version-manager/" + __version__}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if etag:
            headers["If-Match"] = etag
        if idempotency:
            headers["Idempotency-Key"] = idempotency
        payload = canonical(body).encode() if body is not None else None
        # POST database creation and PATCH are not blindly replayed after ambiguous failures.
        replayable = method == "GET" or (method == "POST" and (idempotency or path.endswith("/query")))
        for attempt in range(3):
            try:
                req = urllib.request.Request(API_BASE + path, payload, headers, method=method)
                with self.opener.open(req, timeout=30) as response:
                    raw = response.read(8 * 1024 * 1024 + 1)
                    if len(raw) > 8 * 1024 * 1024:
                        raise ManagerError("API response exceeds safety bound")
                    return json.loads(raw or b"{}"), dict(response.headers)
            except urllib.error.HTTPError as exc:
                exc.close()
                if exc.code in (409, 412):
                    raise Conflict("Cloud record changed or idempotency key was reused with different content") from None
                if exc.code == 429 and attempt < 2:
                    retry = exc.headers.get("Retry-After", "1")
                    self.sleep(min(8, max(1, int(retry) if retry.isdigit() else 2 ** attempt)))
                    continue
                if exc.code >= 500 and replayable and attempt < 2:
                    self.sleep(2 ** attempt)
                    continue
                raise APIError(exc.code) from None
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                error = connection_error(exc, self.network_mode, "api_request")
                if replayable and attempt < 2 and error.kind != "tls_certificate":
                    self.sleep(2 ** attempt)
                    continue
                raise error from None

    def transfer(self, method, url, data=None, headers=None):
        check_file_url(url)
        safe_headers = {}
        for name, value in (headers or {}).items():
            if name.lower() in {"authorization", "cookie", "proxy-authorization", "host", "content-length"}:
                raise ManagerError("Unexpected sensitive header in storage response")
            safe_headers[name] = value
        # FlowUs CDN downloads enforce a page-origin check even for signed URLs.
        # Limit this default to the observed CDN and GET; keep upload contracts intact.
        if (method == "GET" and urllib.parse.urlsplit(url).hostname == "cdn2.flowus.cn"
                and not any(name.lower() == "referer" for name in safe_headers)):
            safe_headers["Referer"] = "https://flowus.cn/"
        req = urllib.request.Request(url, data, safe_headers, method=method)
        try:
            with self.opener.open(req, timeout=60) as response:
                if not 200 <= response.status < 300:
                    raise ManagerError("Object storage transfer did not succeed")
                content = response.read(MAX_FILE + 1)
                if len(content) > MAX_FILE:
                    raise ManagerError("Download exceeds the API single-file limit")
                return content
        except urllib.error.HTTPError as exc:
            exc.close()
            raise APIError(exc.code, "Object storage transfer failed; source remains unchanged") from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise connection_error(exc, self.network_mode, "object_transfer") from None
