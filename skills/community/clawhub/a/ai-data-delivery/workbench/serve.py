#!/usr/bin/env python3
"""Launch the local single-user workbench: python -m workbench.serve --project PATH."""
import argparse
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http.cookies import SimpleCookie
import json
import mimetypes
import os
from pathlib import Path
import secrets
import socket
import sys
from urllib.parse import parse_qs, urlsplit, urlencode

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbench.knowledge import KnowledgeService
from workbench.store import Store, Conflict

STATIC = Path(__file__).with_name("static")


def open_workspace(project):
    if Path(__file__).with_name("service.py").is_file():
        from workbench.service import Service
        return Service(project)
    return ModelWorkspace(project)


class ModelWorkspace:
    """The installed editor only needs the project store and its semantic graph."""
    def __init__(self, project):
        self.store = Store(project)
        self.knowledge = KnowledgeService(self.store)

    def state(self):
        state = self.store.read()
        return {"revision": state["revision"], "document": {"name": state["document"]["name"]},
                "layout": self.store.layouts(), "runs": [], "model_only": True}

    def backup(self):
        import io, tempfile, zipfile
        result = io.BytesIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "project.sqlite"
            self.store.backup(path)
            with zipfile.ZipFile(result, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.write(path, "project.sqlite")
        return result.getvalue()


def make_server(service, port=0):
    token = secrets.token_urlsafe(32)
    model_only = isinstance(service, ModelWorkspace)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # URLs and business inputs are not diagnostic logs.

        def response(self, status, body, mime="application/json; charset=utf-8", filename=None, download_session=False):
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
            if download_session:
                # Direct browser attachment downloads cannot send the fetch-only
                # token header. Limit this HttpOnly session to immutable downloads.
                self.send_header("Set-Cookie", f"workbench_download_{self.server.server_port}={token}; Path=/api/knowledge/download/; HttpOnly; SameSite=Strict")
            self.end_headers()
            self.wfile.write(body)

        def guard(self, api=False):
            hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in hosts:
                raise PermissionError("只接受本机工作台地址")
            navigation = (not api and urlsplit(self.path).path == "/" and
                          self.headers.get("Sec-Fetch-Mode") == "navigate" and
                          self.headers.get("Sec-Fetch-Dest") == "document")
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://" + h for h in hosts} and not navigation:
                raise PermissionError("拒绝跨站请求")
            if self.headers.get("Sec-Fetch-Site") == "cross-site" and not navigation:
                raise PermissionError("拒绝跨站访问")
            authenticated = hmac.compare_digest(self.headers.get("X-Workbench-Token", ""), token)
            if api and self.command == "GET" and urlsplit(self.path).path.startswith("/api/knowledge/download/"):
                cookies = SimpleCookie()
                cookies.load(self.headers.get("Cookie", ""))
                session = cookies.get(f"workbench_download_{self.server.server_port}")
                authenticated = authenticated or bool(session and hmac.compare_digest(session.value, token))
            if api and not authenticated:
                raise PermissionError("会话已变更，请重新打开工作台页面")

        def do_GET(self):
            try:
                path = urlsplit(self.path).path
                self.guard(path.startswith("/api/"))
                if path == "/api/state":
                    return self.response(200, service.state())
                if path == "/api/knowledge/state":
                    from workbench.semantic_package import ENDPOINT_KINDS, REQUIRED_PROPERTIES
                    from workbench.authoring_inspect import evidence_origin
                    model = service.knowledge.state()
                    formats = {s["id"]: s["format"] for s in model["sources"]}
                    return self.response(200, {**model, "evidence_origins": {a["id"]: evidence_origin(a, formats) for a in model["assets"]}, "editor_contract": {
                        "ends": {k: [sorted(a), sorted(b)] for k, (a,b) in ENDPOINT_KINDS.items()},
                        "confirm_fields": REQUIRED_PROPERTIES}})
                if path == "/api/knowledge/graph-view":
                    from workbench.graph_view import project_view
                    query = parse_qs(urlsplit(self.path).query)
                    rev = query.get("revision", [None])[0]
                    return self.response(200, project_view(service.store.read(rev), query.get("focus", [None])[0],
                                                           query.get("scope") == ["all"],
                                                           all_neighbors=query.get("scope") == ["neighbors"]))
                if path == "/api/knowledge/revision":
                    with service.store.connect() as db:
                        revision = db.execute("SELECT MAX(revision) FROM revisions").fetchone()[0]
                    return self.response(200, {"revision": revision})
                if path.startswith("/api/knowledge/download/"):
                    sid = path.rsplit("/", 1)[-1]
                    if urlsplit(self.path).query == 'format=neo4j':
                        import io, zipfile
                        from workbench.semantic_package import SemanticPackage
                        from workbench.neo4j_export import export_neo4j
                        with zipfile.ZipFile(io.BytesIO(service.knowledge.download(sid))) as z:
                            content, _ = export_neo4j(SemanticPackage({n:z.read(n) for n in z.namelist()}))
                        return self.response(200, content, "application/zip", sid + "-neo4j.zip")
                    return self.response(200, service.knowledge.download(sid), "application/zip", sid + ".zip")
                if path.startswith("/api/knowledge/source/"):
                    attachment = service.store.attachment(path.rsplit("/", 1)[-1])
                    return self.response(200, bytes(attachment["content"]), "application/octet-stream", "source-material")
                if path.startswith("/api/knowledge/operation/"):
                    receipt = service.store.operation(path.rsplit("/", 1)[-1])
                    return self.response(200, {"found": receipt is not None, "receipt": receipt})
                if model_only and path == "/api/backup":
                    return self.response(200, service.backup(), "application/zip", "project-backup.zip")
                if not model_only and path == "/api/review":
                    return self.response(200, service.review_html(), "text/html; charset=utf-8", "human-review.html")
                if not model_only and path in {"/api/export", "/api/backup"}:
                    return self.response(200, service.export(path.endswith("backup")), "application/zip", "project-backup.zip" if path.endswith("backup") else "semantic-delivery.zip")
                if path == "/":
                    view = parse_qs(urlsplit(self.path).query).get("view")
                    page = "graph-view.html" if view == ["3d"] else "index.html"
                    body = (STATIC / page).read_bytes().replace(b"__SESSION_TOKEN__", token.encode())
                    return self.response(200, body, "text/html; charset=utf-8", download_session=True)
                if path == "/ui-en.js":
                    return self.response(200, b"window.UI_EN=" + (STATIC / "ui-en.json").read_bytes() + b";", "text/javascript; charset=utf-8")
                if path in {"/app.js", "/i18n.js", "/style.css", "/knowledge.js", "/knowledge.css", "/scenarios.js", "/metadata.js", "/query-bindings.js", "/graph-layout.js", "/vendor/elk.bundled.js", "/graph-view.css", "/graph-view.js", "/vendor/force-graph-3d.js"}:
                    return self.response(200, (STATIC / path[1:]).read_bytes(), "text/javascript; charset=utf-8" if path.endswith("js") else "text/css; charset=utf-8")
                self.response(404, {"error": "页面不存在"})
            except PermissionError as exc:
                self.response(403, {"error": str(exc)})
            except Exception as exc:
                self.response(400, {"error": str(exc), **({"details": exc.as_dict()} if hasattr(exc, "as_dict") else {})})

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
                routes = {"/api/layout": lambda r: service.store.save_layout(r["positions"])}
                if not model_only:
                    routes.update({"/api/import": service.import_file, "/api/edit": service.edit, "/api/answer": service.answer,
                          "/api/scene": service.scene, "/api/query": service.query, "/api/feedback": service.feedback,
                          "/api/consumer": service.consumer, "/api/context": service.context,
                          "/api/bundle": service.bundle, "/api/check": lambda _: service.check(),
                          "/api/resolve-feedback": service.resolve_feedback, "/api/derive": service.derive,
                          "/api/restore": lambda r: service.store.restore(r["target"], r["revision"]),
                          "/api/knowledge/example": service.knowledge.example})
                routes.update({"/api/knowledge/" + name: action for name, action in {
                    "metadata-connect": service.knowledge.metadata_connect, "metadata-scan": service.knowledge.metadata_scan,
                    "metadata-regress": service.knowledge.metadata_regress,
                    "import": service.knowledge.import_material, "task": service.knowledge.task,
                    "scenario": service.knowledge.scenario, "scenario-check": service.knowledge.scenario_check,
                    "scenario-assess": service.knowledge.scenario_assess, "impact": service.knowledge.impact,
                    "propose": service.knowledge.propose, "review": service.knowledge.review,
                    "edit": service.knowledge.edit, "merge": service.knowledge.merge,
                    "separate": service.knowledge.separate, "retire": service.knowledge.retire,
                    "review-source": service.knowledge.review_source, "undo": service.knowledge.undo,
                    "publish": service.knowledge.publish}.items()})
                action = routes.get(urlsplit(self.path).path)
                if action is None:
                    return self.response(404, {"error": "操作不存在"})
                self.response(200, action(req) or {"ok": True})
            except PermissionError as exc:
                self.response(403, {"error": str(exc)})
            except Conflict as exc:
                self.response(409, {"error": str(exc)})
            except Exception as exc:
                self.response(400, {"error": str(exc), **({"details": exc.as_dict()} if hasattr(exc, "as_dict") else {})})

    class LocalServer(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = os.name != "nt"

        def server_bind(self):
            # Windows SO_REUSEADDR can share a listening port with an unrelated
            # local service, sending the browser to the wrong application.
            if os.name == "nt":
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            super().server_bind()

        def get_request(self):
            connection, address = super().get_request()
            connection.settimeout(30)
            return connection, address

    return LocalServer(("127.0.0.1", port), Handler)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, help="本地项目目录，自动创建 project.sqlite")
    ap.add_argument("--port", type=int, default=0, help="默认自动选取可用端口")
    ap.add_argument("--language", choices=['en', 'zh'], default='en')
    ap.add_argument("--focus", help="Show this asset when the graph opens")
    ap.add_argument("--page", choices=["graph", "knowledge", "review"], default="graph")
    args = ap.parse_args(argv)
    service = open_workspace(args.project)
    server = make_server(service, args.port)
    address = f"http://127.0.0.1:{server.server_port}"
    (service.store.directory / "server.json").write_text(json.dumps({"url": address, "pid": os.getpid()}), encoding="utf-8")
    query = urlencode({"lang": args.language, **({"focus": args.focus} if args.focus else {})})
    print(f"Semantic Workbench / 语义工作台: {address}/?{query}#{args.page}\nProject / 项目: {service.store.directory}\nCtrl+C to stop / 停止。", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
