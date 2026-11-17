#!/usr/bin/env python3
"""Launch the local single-user workbench: python -m workbench.serve --project PATH."""
import argparse
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mimetypes
import os
from pathlib import Path
import secrets
import sys
from urllib.parse import urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbench.service import Service
from workbench.store import Conflict

STATIC = Path(__file__).with_name("static")


def make_server(service, port=0):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # URLs and business inputs are not diagnostic logs.

        def response(self, status, body, mime="application/json; charset=utf-8", filename=None):
            if not isinstance(body, bytes):
                body = json.dumps(body, ensure_ascii=False, allow_nan=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            if filename:
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(body)

        def guard(self, api=False):
            hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in hosts:
                raise PermissionError("只接受本机工作台地址")
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://" + h for h in hosts}:
                raise PermissionError("拒绝跨站请求")
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                raise PermissionError("拒绝跨站访问")
            if api and not hmac.compare_digest(self.headers.get("X-Workbench-Token", ""), token):
                raise PermissionError("会话已变更，请重新打开工作台页面")

        def do_GET(self):
            try:
                path = urlsplit(self.path).path
                self.guard(path.startswith("/api/"))
                if path == "/api/state":
                    return self.response(200, service.state())
                if path == "/api/review":
                    return self.response(200, service.review_html(), "text/html; charset=utf-8", "human-review.html")
                if path in {"/api/export", "/api/backup"}:
                    return self.response(200, service.export(path.endswith("backup")), "application/zip", "project-backup.zip" if path.endswith("backup") else "semantic-delivery.zip")
                if path == "/":
                    body = (STATIC / "index.html").read_bytes().replace(b"__SESSION_TOKEN__", token.encode())
                    return self.response(200, body, "text/html; charset=utf-8")
                if path in {"/app.js", "/style.css"}:
                    return self.response(200, (STATIC / path[1:]).read_bytes(), "text/javascript; charset=utf-8" if path.endswith("js") else "text/css; charset=utf-8")
                self.response(404, {"error": "页面不存在"})
            except PermissionError as exc:
                self.response(403, {"error": str(exc)})
            except Exception as exc:
                self.response(400, {"error": str(exc)})

        def do_POST(self):
            try:
                self.guard(True)
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("请使用 JSON 请求")
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > 46 * 1024 * 1024:
                    raise ValueError("请求体为空或超过 46 MB")
                req = json.loads(self.rfile.read(size))
                if not isinstance(req, dict):
                    raise ValueError("请求必须是对象")
                routes = {"/api/import": service.import_file, "/api/edit": service.edit, "/api/answer": service.answer,
                          "/api/scene": service.scene, "/api/query": service.query, "/api/feedback": service.feedback,
                          "/api/consumer": service.consumer, "/api/context": service.context,
                          "/api/bundle": service.bundle, "/api/check": lambda _: service.check(),
                          "/api/resolve-feedback": service.resolve_feedback, "/api/derive": service.derive,
                          "/api/layout": lambda r: service.store.save_layout(r["positions"]),
                          "/api/restore": lambda r: service.store.restore(r["target"], r["revision"])}
                action = routes.get(urlsplit(self.path).path)
                if action is None:
                    return self.response(404, {"error": "操作不存在"})
                self.response(200, action(req) or {"ok": True})
            except PermissionError as exc:
                self.response(403, {"error": str(exc)})
            except Conflict as exc:
                self.response(409, {"error": str(exc)})
            except Exception as exc:
                self.response(400, {"error": str(exc)})

    return HTTPServer(("127.0.0.1", port), Handler)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, help="本地项目目录，自动创建 project.sqlite")
    ap.add_argument("--port", type=int, default=0, help="默认自动选取可用端口")
    args = ap.parse_args(argv)
    service = Service(args.project)
    server = make_server(service, args.port)
    address = f"http://127.0.0.1:{server.server_port}"
    (service.store.directory / "server.json").write_text(json.dumps({"url": address, "pid": os.getpid()}), encoding="utf-8")
    print(f"语义工作台已启动：{address}\n项目：{service.store.directory}\n按 Ctrl+C 停止。", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
