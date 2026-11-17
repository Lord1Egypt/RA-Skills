"""Small HTTP helpers for Open API JSON requests."""

import json
import urllib.error
import urllib.request


def handle_http_error(error, *, error_hints, guide_insufficient_balance, die):
    """Convert HTTPError responses into friendly CLI errors."""
    body = b""
    try:
        body = error.read()
    except Exception:
        pass
    code = None
    msg = ""
    err = {}
    try:
        payload = json.loads(body.decode("utf-8"))
        err = payload.get("error") or payload
        code = err.get("code")
        msg = err.get("message", "")
    except Exception:
        msg = body.decode("utf-8", "replace")
    if error.code == 402 or code in ("insufficient_balance", "insufficient_points"):
        guide_insufficient_balance(err)
        return
    hint = error_hints.get(code, "")
    retry_after = error.headers.get("Retry-After") if error.headers else None
    lines = [f"请求失败 HTTP {error.code}" + (f" [{code}]" if code else "")]
    if msg:
        lines.append(f"  message: {msg}")
    if hint:
        lines.append(f"  → {hint}")
    if retry_after:
        lines.append(f"  → Retry-After: {retry_after}s")
    die("\n".join(lines), code=1)


def request_json(method, url, *, headers=None, data=None, json_body=None, handle_http_error_fn, die, network_error_message):
    """Send an HTTP request and parse a JSON response."""
    hdrs = dict(headers or {})
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8")) if raw else {}
    except urllib.error.HTTPError as e:
        handle_http_error_fn(e)
    except urllib.error.URLError as e:
        die(network_error_message(e), code=1)

