#!/usr/bin/env python3
"""Minimal Affogato API client for coding agents. Python 3.9+, stdlib only.

    export AFFOGATO_API_KEY=afg_...
    python affogato.py models [--feature image-generation] [--output-type video] [--q flux]
    python affogato.py model <model_id>
    python affogato.py estimate <model_id> --input '{"prompt": "a cat"}'
    python affogato.py generate <model_id> --input '{"prompt": "a cat"}' [--wait] [--download DIR]
    python affogato.py get <generation_id> [--wait] [--download DIR]
    python affogato.py cancel <generation_id>
    python affogato.py upload <path> | --url <https://...>
    python affogato.py account

Base URL: AFFOGATO_API_BASE (default https://api.affogato.ai/v1).
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = os.environ.get("AFFOGATO_API_BASE", "https://api.affogato.ai/v1").rstrip("/")
KEY = os.environ.get("AFFOGATO_API_KEY", "")
WAIT_ROUND_S = 25
MAX_WAIT_S = 20 * 60


def _request(method: str, path: str, body: dict | None = None, *, raw: bytes | None = None,
             content_type: str | None = None, params: dict | None = None) -> dict:
    if not KEY:
        sys.exit("AFFOGATO_API_KEY is not set (create one at https://affogato.ai/app/developers)")
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    headers = {"Authorization": f"Bearer {KEY}", "Accept": "application/json",
               "User-Agent": "affogato-skill/0.1"}
    if data is not None:
        headers["Content-Type"] = content_type or "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                text = resp.read().decode()
                return json.loads(text) if text else {}
        except urllib.error.HTTPError as e:
            payload = e.read().decode(errors="replace")
            if e.code == 429 and attempt < 5:
                wait = int(e.headers.get("Retry-After", "5") or 5)
                print(f"rate limited; retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            try:
                err = json.loads(payload)["error"]
                sys.exit(f"HTTP {e.code} {err.get('code')}: {err.get('message')}")
            except (ValueError, KeyError, TypeError):
                sys.exit(f"HTTP {e.code}: {payload[:300]}")
    sys.exit("gave up after repeated 429s")


def _print(obj: object) -> None:
    print(json.dumps(obj, indent=2))


def cmd_models(a: argparse.Namespace) -> None:
    res = _request("GET", "/models", params={"feature": a.feature, "output_type": a.output_type,
                                             "q": a.q})
    for m in res["data"]:
        price = m.get("price_range") or m.get("pricing")
        print(f"{m['id']:<40} {m['output_type']:<6} {m['name']:<32} {json.dumps(price)}")
    print(f"{len(res['data'])} models", file=sys.stderr)


def cmd_model(a: argparse.Namespace) -> None:
    _print(_request("GET", f"/models/{a.model_id}"))


def _input(a: argparse.Namespace) -> dict:
    try:
        return json.loads(a.input) if a.input else {}
    except ValueError as e:
        sys.exit(f"--input must be JSON: {e}")


def cmd_estimate(a: argparse.Namespace) -> None:
    _print(_request("POST", "/generations/estimate", {"model": a.model_id, "input": _input(a)}))


def _download(gen: dict, directory: str) -> None:
    os.makedirs(directory, exist_ok=True)
    for i, out in enumerate(gen.get("outputs") or []):
        url = out.get("url")
        if not url:
            continue
        ext = mimetypes.guess_extension(out.get("mime_type") or "") or ""
        path = os.path.join(directory, f"{gen['id']}-{i}{ext}")
        urllib.request.urlretrieve(url, path)
        print(f"saved {path}", file=sys.stderr)


def _wait(gen: dict) -> dict:
    deadline = time.time() + MAX_WAIT_S
    while gen["status"] in ("queued", "processing") and time.time() < deadline:
        print(f"{gen['status']}…", file=sys.stderr)
        gen = _request("GET", f"/generations/{gen['id']}", params={"wait": WAIT_ROUND_S})
    return gen


def _finish(a: argparse.Namespace, gen: dict) -> None:
    if getattr(a, "wait", False):
        gen = _wait(gen)
    _print({k: gen[k] for k in ("id", "status", "model", "credits_charged", "credits_refunded",
                                 "error", "outputs") if k in gen})
    if getattr(a, "download", None) and gen["status"] == "succeeded":
        _download(gen, a.download)


def cmd_generate(a: argparse.Namespace) -> None:
    body: dict = {"model": a.model_id, "input": _input(a)}
    if a.webhook_url:
        body["webhook_url"] = a.webhook_url
    gen = _request("POST", "/generations", body, params={"wait": WAIT_ROUND_S if a.wait else None})
    _finish(a, gen)


def cmd_get(a: argparse.Namespace) -> None:
    _finish(a, _request("GET", f"/generations/{a.generation_id}"))


def cmd_cancel(a: argparse.Namespace) -> None:
    _print(_request("POST", f"/generations/{a.generation_id}/cancel"))


def cmd_upload(a: argparse.Namespace) -> None:
    if a.url:
        _print(_request("POST", "/files/from-url", {"url": a.url}))
        return
    if not a.path:
        sys.exit("upload needs a path or --url")
    mime = mimetypes.guess_type(a.path)[0] or "application/octet-stream"
    boundary = uuid.uuid4().hex
    with open(a.path, "rb") as fh:
        content = fh.read()
    name = os.path.basename(a.path)
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    _print(_request("POST", "/files", raw=body,
                    content_type=f"multipart/form-data; boundary={boundary}"))


def cmd_account(a: argparse.Namespace) -> None:
    _print(_request("GET", "/account"))


def main() -> None:
    p = argparse.ArgumentParser(description="Affogato API client")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("models"); s.add_argument("--feature"); s.add_argument("--output-type"); s.add_argument("--q"); s.set_defaults(fn=cmd_models)
    s = sub.add_parser("model"); s.add_argument("model_id"); s.set_defaults(fn=cmd_model)
    s = sub.add_parser("estimate"); s.add_argument("model_id"); s.add_argument("--input", default="{}"); s.set_defaults(fn=cmd_estimate)
    s = sub.add_parser("generate"); s.add_argument("model_id"); s.add_argument("--input", default="{}"); s.add_argument("--wait", action="store_true"); s.add_argument("--download"); s.add_argument("--webhook-url"); s.set_defaults(fn=cmd_generate)
    s = sub.add_parser("get"); s.add_argument("generation_id"); s.add_argument("--wait", action="store_true"); s.add_argument("--download"); s.set_defaults(fn=cmd_get)
    s = sub.add_parser("cancel"); s.add_argument("generation_id"); s.set_defaults(fn=cmd_cancel)
    s = sub.add_parser("upload"); s.add_argument("path", nargs="?"); s.add_argument("--url"); s.set_defaults(fn=cmd_upload)
    s = sub.add_parser("account"); s.set_defaults(fn=cmd_account)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
