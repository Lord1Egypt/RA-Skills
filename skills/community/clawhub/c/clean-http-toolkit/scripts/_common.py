"""
Shared helpers for clean-http-toolkit.

Pure Python 3 standard library. No `requests`, no `httpx`, no remote calls
besides the ones the user explicitly asks for.
"""

from __future__ import annotations

import gzip
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple


SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")
DEFAULT_USER_AGENT = "clean-http-toolkit/0.1.0 (+https://clawhub.ai/gopendrasharma89-tech/clean-http-toolkit)"
DEFAULT_TIMEOUT = 30.0
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def safe_url(u: str) -> str:
    """Reject obviously malformed URLs and anything that isn't http(s)://."""
    if not isinstance(u, str) or not u:
        raise ValueError("URL is required")
    p = urllib.parse.urlparse(u)
    if p.scheme not in ("http", "https"):
        raise ValueError(f"URL must be http:// or https://, got: {p.scheme!r}")
    if not p.netloc:
        raise ValueError(f"URL has no host: {u!r}")
    return u


def parse_headers(specs) -> Dict[str, str]:
    """Parse a list of 'Header: value' strings into a dict."""
    out: Dict[str, str] = {}
    if not specs:
        return out
    for s in specs:
        if ":" not in s:
            raise ValueError(f"--header expects 'Name: value', got: {s!r}")
        name, _, value = s.partition(":")
        name = name.strip()
        value = value.strip()
        if not name:
            raise ValueError(f"empty header name in: {s!r}")
        out[name] = value
    return out


def fetch(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[bytes] = None,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = 3,
    backoff: float = 0.5,
    follow_redirects: bool = True,
    allow_insecure: bool = False,
) -> Tuple[int, Dict[str, str], bytes, list]:
    """Make an HTTP request with retries and return (status, headers, body, trail).

    `trail` is a list of (status, url) tuples showing the redirect chain
    (always at least one entry: the final response).
    """
    safe_url(url)
    final_headers = {"User-Agent": DEFAULT_USER_AGENT, "Accept-Encoding": "gzip"}
    if headers:
        final_headers.update(headers)

    trail: list = []
    last_err: Optional[Exception] = None

    handlers = []
    if not follow_redirects:
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **kw):
                return None
        handlers.append(NoRedirect())
    if allow_insecure:
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            handlers.append(urllib.request.HTTPSHandler(context=ctx))
        except Exception:
            pass

    opener = urllib.request.build_opener(*handlers)

    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=body, method=method, headers=final_headers
        )
        try:
            with opener.open(req, timeout=timeout) as resp:
                status = resp.status
                resp_headers = {k: v for k, v in resp.getheaders()}
                raw = resp.read()
                if resp_headers.get("Content-Encoding", "").lower() == "gzip":
                    try:
                        raw = gzip.decompress(raw)
                    except OSError:
                        pass
                trail.append((status, resp.geturl()))
                return status, resp_headers, raw, trail
        except urllib.error.HTTPError as e:
            status = e.code
            resp_headers = {k: v for k, v in (e.headers.items() if e.headers else [])}
            try:
                raw = e.read()
            except Exception:
                raw = b""
            trail.append((status, url))
            if status in RETRY_STATUSES and attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            return status, resp_headers, raw, trail
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            raise

    raise RuntimeError(f"unreachable: retries exhausted ({last_err})")


def write_or_print(out_path: Optional[Path], data: bytes,
                   text: bool = True) -> None:
    if out_path is None:
        if text:
            try:
                sys.stdout.write(data.decode("utf-8"))
            except UnicodeDecodeError:
                sys.stdout.buffer.write(data)
        else:
            sys.stdout.buffer.write(data)
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)


def headers_to_json(h: Dict[str, str]) -> str:
    return json.dumps(h, indent=2, ensure_ascii=False)
