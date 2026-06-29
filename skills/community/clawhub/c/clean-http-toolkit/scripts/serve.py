#!/usr/bin/env python3
"""
serve.py - A tiny local HTTP server for AI agents that need to share files
or run a one-shot mock endpoint.

Two modes:

    --mode static (default)
        Serve a directory over HTTP. Like `python3 -m http.server` but with
        a --max-requests cutoff (so CI tests can run the server and have it
        exit cleanly).

    --mode echo
        Reply to every request with a JSON envelope describing the request
        itself: method, path, headers, query string, body. Useful for
        webhook smoke tests and for inspecting what an agent is actually
        sending.

Usage:
    serve.py [--mode static|echo] [--directory PATH] [--port N] [--bind HOST]
             [--max-requests N] [--quiet]

Options:
    --mode static|echo    server mode (default: static)
    --directory PATH      for static: root directory (default: cwd)
    --port N              listen port (default: 0 = pick a free port)
    --bind HOST           bind address (default: 127.0.0.1)
    --max-requests N      exit after N requests (default: 0 = run forever)
    --quiet               suppress access logs on stderr
    -h, --help            show this help

Security: binds to 127.0.0.1 only by default. Pass --bind 0.0.0.0 explicitly
to expose the server (use at your own risk).

Exit codes:
    0   --max-requests reached or interrupted cleanly
    2   bad arguments / unsafe path / cannot bind port
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import socketserver
import sys
import threading
import time
import urllib.parse
from typing import Any, Dict

from _common import safe_path


_STATE = {"counter": 0, "max": 0, "shutdown": None, "quiet": False}


def _maybe_shutdown() -> None:
    _STATE["counter"] += 1
    if _STATE["max"] and _STATE["counter"] >= _STATE["max"]:
        ev = _STATE["shutdown"]
        if ev is not None:
            ev.set()


class _StaticHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if _STATE["quiet"]:
            return
        sys.stderr.write(f"serve [{self.address_string()}] {fmt % args}\n")
        sys.stderr.flush()

    def end_headers(self):
        super().end_headers()
        _maybe_shutdown()


class _EchoHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if _STATE["quiet"]:
            return
        sys.stderr.write(f"serve [{self.address_string()}] {fmt % args}\n")
        sys.stderr.flush()

    def _envelope(self) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        cl = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(cl) if cl > 0 else b""
        try:
            body_repr: Any = json.loads(body.decode("utf-8")) if body else None
        except Exception:
            try:
                body_repr = body.decode("utf-8")
            except UnicodeDecodeError:
                body_repr = f"<{len(body)} bytes binary>"
        return {
            "method": self.command,
            "path": parsed.path,
            "query": query,
            "headers": {k: v for k, v in self.headers.items()},
            "body": body_repr,
        }

    def _respond(self):
        env = self._envelope()
        payload = json.dumps(env, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
        _maybe_shutdown()

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _respond


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--mode", choices=("static", "echo"), default="static")
    p.add_argument("--directory", default=".")
    p.add_argument("--port", type=int, default=0)
    p.add_argument("--bind", default="127.0.0.1")
    p.add_argument("--max-requests", dest="max_requests", type=int, default=0)
    p.add_argument("--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help:
        print(__doc__)
        return 0

    try:
        directory = safe_path(args.directory)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    if args.mode == "static" and not directory.is_dir():
        print(f"Error: --directory is not a directory: {directory}",
              file=sys.stderr)
        return 2

    _STATE["max"] = args.max_requests
    _STATE["shutdown"] = threading.Event()
    _STATE["quiet"] = args.quiet
    _STATE["counter"] = 0

    cls = _StaticHandler if args.mode == "static" else _EchoHandler
    if args.mode == "static":
        os.chdir(str(directory))

    try:
        httpd = socketserver.ThreadingTCPServer((args.bind, args.port), cls)
    except OSError as e:
        print(f"Error: cannot bind {args.bind}:{args.port}: {e}",
              file=sys.stderr)
        return 2
    httpd.daemon_threads = True
    actual_port = httpd.server_address[1]
    if not args.quiet:
        suffix = f" -> {directory}" if args.mode == "static" else ""
        cap = f" (max-requests={args.max_requests})" if args.max_requests else ""
        print(f"serve ({args.mode}): http://{args.bind}:{actual_port}{suffix}{cap}",
              file=sys.stderr)

    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        if args.max_requests:
            _STATE["shutdown"].wait()
        else:
            while True:
                time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        httpd.server_close()

    if not args.quiet:
        print(f"serve: exited after {_STATE['counter']} request(s)",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
