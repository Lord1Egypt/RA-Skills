#!/usr/bin/env python3
"""Serve a review workbench with workspace-restricted local actions / 提供仅限 workspace 的本地 review workbench actions。"""

from __future__ import annotations

import argparse
import hmac
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from html.parser import HTMLParser
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
from typing import Type
from urllib import parse


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ADAPTER = SCRIPT_DIR / "mixed_folder_adapter.py"
DEFAULT_PIPELINE = SCRIPT_DIR / "asset_pipeline.py"
MAX_BODY_BYTES = 8 * 1024 * 1024
MAX_DECISIONS = 10000
MAX_WORKBENCH_BYTES = MAX_BODY_BYTES + 64 * 1024
TOKEN_MARKER = '<meta name="review-token" content="">'
DECISIONS = {"review", "keep", "delete", "archive_only", "generate_asset", "metadata_only"}


class RequestError(ValueError):
    def __init__(self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status = status


def loopback_host(value: str) -> str:
    """Validate before binding; never resolve arbitrary hostnames through DNS."""
    address = ipaddress.ip_address("127.0.0.1" if value == "localhost" else value)
    if not address.is_loopback:
        raise ValueError("workbench host must be a loopback address")
    return str(address)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise RequestError("duplicate JSON key")
        result[key] = value
    return result


class WorkbenchDataParser(HTMLParser):
    """Extract data only; none of the input markup becomes executable output."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.found = False
        self.collecting = False
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if ("id", "asset-data") not in attrs:
            return
        fields = dict(attrs)
        if self.found or tag != "script" or len(fields) != len(attrs) or fields.get("type") != "application/json":
            raise ValueError("expected a unique asset-data JSON script")
        self.found = True
        self.collecting = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.collecting = False

    def handle_data(self, data):
        if self.collecting:
            self.parts.append(data)


def workbench_rows(page: str) -> list[dict[str, object]]:
    parser = WorkbenchDataParser()
    parser.feed(page)
    parser.close()
    if not parser.found or parser.collecting:
        raise ValueError("missing or incomplete asset-data")
    payload = json.loads("".join(parser.parts), object_pairs_hook=unique_object)
    json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    rows = payload.get("assets") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or len(rows) > MAX_DECISIONS:
        raise ValueError("expected an assets list")
    list_fields = {"source_paths", "semantic_paths", "original_directories", "source_formats", "insights", "suggestion_signals"}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("expected an asset object")
        for key in list_fields & row.keys():
            if not isinstance(row[key], list) or any(not isinstance(item, str) for item in row[key]):
                raise ValueError("expected a list of strings")
    return rows


def installed_renderer():
    """Load by installed file path, never from the workspace or sys.path."""
    spec = importlib.util.spec_from_file_location("_agent_asset_renderer", SCRIPT_DIR / "review_workbench.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("installed workbench renderer unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.render_workbench


def inside(root: Path, target: Path) -> bool:
    try:
        target.resolve(strict=False).relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_review_path(root: Path, raw_path: str) -> Path:
    if not raw_path:
        raise ValueError("missing path")
    candidate = Path(raw_path)
    target = candidate.resolve(strict=False) if candidate.is_absolute() else (root / candidate).resolve(strict=False)
    if not inside(root, target):
        raise ValueError(f"path escapes workspace: {raw_path}")
    if not target.exists():
        raise FileNotFoundError(str(target))
    return target


def resolve_scope(root: Path, raw_scope: str) -> Path:
    scope = (root / raw_scope).resolve(strict=False) if raw_scope else root.resolve()
    if not inside(root, scope) or not scope.is_dir():
        raise ValueError(f"invalid scope: {raw_scope}")
    return scope


def imported_decision_path(root: Path, scope: str) -> Path:
    resolve_scope(root, scope)
    label = hashlib.sha256(scope.encode("utf-8")).hexdigest()[:12]
    return root / ".cleanup-extracted" / "imported-decisions" / f"{label}.json"


def pipeline_apply_result(stdout: str) -> dict[str, object]:
    """Extract stable apply/writeback details from pipeline JSON for the browser."""
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return {}
    results = payload.get("results", []) if isinstance(payload, dict) else []
    if not isinstance(results, list):
        return {}
    response: dict[str, object] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        stage = str(item.get("stage", ""))
        if stage == "apply":
            try:
                apply_payload = json.loads(str(item.get("stdout", "")))
            except json.JSONDecodeError:
                apply_payload = {}
            if isinstance(apply_payload, dict):
                for key in ("workbench", "report", "summary", "success"):
                    if key in apply_payload:
                        response[key] = apply_payload[key]
        elif stage == "post-apply-index":
            response["post_apply_index"] = {
                "status": item.get("status", ""),
                "blocked_reason": item.get("blocked_reason", ""),
            }
    return response


def is_loopback_host(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def valid_session_token(headers: object, expected: str) -> bool:
    getter = getattr(headers, "get", None)
    supplied = getter("X-Agent-Asset-Token", "") if getter else ""
    return bool(expected and supplied) and hmac.compare_digest(str(supplied), expected)


class ReviewHandler(SimpleHTTPRequestHandler):
    workspace_root: Path
    adapter_path: Path
    pipeline_path: Path
    scope_path: Path
    workbench_path: Path
    archive_scope_path: Path
    request_token: str
    allow_write = False
    allow_apply = False
    allow_file_open = False
    session_token = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(self.workspace_root), **kwargs)

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(10)

    def authorized(self, *, mutation: bool = False) -> bool:
        """Check peer/authority on every route, and origin/capability on writes."""
        try:
            loopback_host(self.client_address[0])
            address, port = self.server.server_address[:2]
            address = loopback_host(address)
            host = self.headers.get("Host", "")
            names = {"localhost", f"[{address}]" if ":" in address else address}
            authorities = {f"{name}:{port}" for name in names}
            if port == 80:
                authorities.update(names)
            if len(self.headers.get_all("Host", [])) != 1 or host not in authorities:
                raise ValueError("invalid host")
            origins = self.headers.get_all("Origin", [])
            if (mutation or origins) and origins != [f"http://{host}"]:
                raise ValueError("invalid origin")
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                raise ValueError("cross-site request")
            if mutation:
                tokens = self.headers.get_all("X-Review-Token", [])
                if len(tokens) != 1 or not secrets.compare_digest(
                    tokens[0].encode("utf-8"), self.request_token.encode("ascii")
                ):
                    raise ValueError("invalid token")
        except ValueError:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "request not authorized"})
            return False
        return True

    def do_OPTIONS(self) -> None:
        if self.authorized():
            self.send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "preflight not supported"})

    def do_GET(self) -> None:
        self.serve_workbench()

    def do_HEAD(self) -> None:
        self.serve_workbench()

    def serve_workbench(self) -> None:
        if not self.authorized():
            return
        try:
            parsed = parse.urlsplit(self.path)
            expected = "/" + self.workbench_path.relative_to(self.workspace_root).as_posix()
            if parsed.scheme or parsed.netloc or parsed.fragment or parse.unquote(parsed.path, errors="strict") != expected:
                raise RequestError("file not served", HTTPStatus.NOT_FOUND)
            target = resolve_review_path(self.workspace_root, expected[1:])
            if target != self.workbench_path or not target.is_file():
                raise RequestError("file not served", HTTPStatus.NOT_FOUND)
            with target.open("rb") as source:
                raw_page = source.read(MAX_WORKBENCH_BYTES + 1)
            try:
                if len(raw_page) > MAX_WORKBENCH_BYTES:
                    raise ValueError("workbench too large")
                rows = workbench_rows(raw_page.decode("utf-8"))
            except (ValueError, RecursionError) as exc:
                raise RequestError("invalid workbench asset data; regenerate the workbench", HTTPStatus.CONFLICT) from exc
            # Only JSON rows survive. HTML, scripts and supplied configuration are discarded.
            page = self.render_workbench(
                root=self.workspace_root,
                scope=self.scope_path.relative_to(self.workspace_root).as_posix(),
                rows=rows,
                adapter_path=self.adapter_path,
                pipeline_path=self.pipeline_path,
                shortcut_available=False,
            )
            page = page.replace(TOKEN_MARKER, f'<meta name="review-token" content="{self.request_token}">', 1)
            self.send_body(HTTPStatus.OK, page.encode("utf-8"), "text/html; charset=utf-8")
        except (OSError, ValueError) as exc:
            status = exc.status if isinstance(exc, RequestError) else HTTPStatus.NOT_FOUND
            message = str(exc) if isinstance(exc, RequestError) else "file not served"
            self.send_json(status, {"error": message})

    def do_POST(self) -> None:
        if not self.authorized(mutation=True):
            return
        if self.path not in {"/__save_decisions", "/__apply_decisions", "/__open"}:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "unknown endpoint"})
            return
        required = {
            "/__save_decisions": self.allow_write,
            "/__apply_decisions": self.allow_write and self.allow_apply,
            "/__open": self.allow_file_open,
        }
        if not required[self.path]:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "action capability disabled"})
            return
        try:
            payload = self.read_payload()
            if self.path == "/__open":
                if set(payload) != {"path"} or not isinstance(payload["path"], str) or not 0 < len(payload["path"]) <= 4096:
                    raise RequestError("expected a file path")
                target = self.resolve_open_path(payload["path"])
                result = subprocess.run(["open", str(target)], check=False, timeout=10)
                if result.returncode != 0:
                    self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "open failed"})
                else:
                    self.send_json(HTTPStatus.OK, {"status": "opened", "path": str(target)})
                return
            self.validate_decisions(payload)
            decision_path = self.save_payload(payload)
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            status = exc.status if isinstance(exc, RequestError) else HTTPStatus.BAD_REQUEST
            message = str(exc) if isinstance(exc, RequestError) else "invalid request or unavailable path"
            self.send_json(status, {"error": message})
            return
        if self.path == "/__save_decisions":
            self.send_json(HTTPStatus.OK, {"status": "saved", "path": str(decision_path)})
            return
        scope = str(payload["scope"])
        result = subprocess.run(
            [
                sys.executable,
                str(self.pipeline_path),
                "--root",
                str(self.workspace_root),
                "--scope",
                scope,
                "--cleanup-tool",
                str(self.adapter_path),
                "--stage",
                "apply",
                "--decisions",
                str(decision_path),
                "--execute-decisions",
                "--after-apply-index",
                "auto",
                "--json",
            ],
            cwd=self.workspace_root,
            text=True,
            capture_output=True,
            check=False,
        )
        status = HTTPStatus.OK if result.returncode == 0 else HTTPStatus.INTERNAL_SERVER_ERROR
        self.send_json(
            status,
            {
                "status": "executed" if result.returncode == 0 else "failed",
                "path": str(decision_path),
                "apply": pipeline_apply_result(result.stdout),
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )

    def resolve_open_path(self, raw_path: str) -> Path:
        target = resolve_review_path(self.workspace_root, raw_path)
        # Keep configured boundaries pinned: resolving an archive symlink must not widen them.
        if not any(target.is_relative_to(boundary) for boundary in (self.scope_path, self.archive_scope_path)):
            raise RequestError("path is outside the selected scope and its archive")
        return target

    def read_payload(self) -> dict[str, object]:
        if len(self.headers.get_all("Content-Type", [])) != 1 or self.headers.get_content_type() != "application/json":
            raise RequestError("expected application/json", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        if self.headers.get_content_charset("utf-8") != "utf-8":
            raise RequestError("expected UTF-8 JSON", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_all("Transfer-Encoding") or len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].isdecimal():
            raise RequestError("invalid request framing")
        if len(lengths[0]) > 10 or int(lengths[0]) > MAX_BODY_BYTES:
            raise RequestError("request body too large", HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        length = int(lengths[0])
        if length == 0:
            raise RequestError("empty request body")
        body = self.rfile.read(length)
        if len(body) != length:
            raise RequestError("incomplete request body")
        try:
            value = json.loads(body.decode("utf-8"), object_pairs_hook=unique_object)
            # Reject lone surrogates and non-JSON numbers before any filesystem write.
            json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except (ValueError, RecursionError) as exc:
            raise RequestError("invalid JSON") from exc
        if not isinstance(value, dict):
            raise RequestError("expected JSON object")
        return value

    def validate_decisions(self, payload: dict[str, object]) -> None:
        if set(payload) != {"scope", "decisions"} or not isinstance(payload["scope"], str) or not isinstance(payload["decisions"], list):
            raise RequestError("expected scope and decisions JSON payload")
        if resolve_scope(self.workspace_root, payload["scope"]) != self.scope_path:
            raise RequestError("scope does not match the served workbench")
        rows = payload["decisions"]
        if len(rows) > MAX_DECISIONS:
            raise RequestError("too many decisions")
        seen = set()
        text_fields = {"asset_id", "path", "decision", "asset_mode", "pii_label", "category", "reason"}
        list_fields = {"source_paths", "semantic_paths"}
        for row in rows:
            if not isinstance(row, dict) or set(row) - text_fields - list_fields - {"review_index"}:
                raise RequestError("invalid decision row")
            if any(not isinstance(row[key], str) or len(row[key]) > 65536 for key in text_fields & row.keys()):
                raise RequestError("invalid decision field")
            asset_id = row.get("asset_id", "")
            if not asset_id or len(asset_id) > 512 or asset_id in seen or row.get("decision") not in DECISIONS:
                raise RequestError("invalid or duplicate asset decision")
            seen.add(asset_id)
            if row.get("pii_label", "unknown") not in {"unknown", "pii", "non_pii"}:
                raise RequestError("invalid privacy label")
            if "asset_mode" in row and row["asset_mode"] != row["decision"]:
                raise RequestError("conflicting decision fields")
            if "review_index" in row and (type(row["review_index"]) is not int or row["review_index"] < 1):
                raise RequestError("invalid review index")
            for key in list_fields & row.keys():
                if not isinstance(row[key], list) or any(not isinstance(path, str) or len(path) > 4096 for path in row[key]):
                    raise RequestError("expected a list of file paths")
        payload["scope"] = self.scope_path.relative_to(self.workspace_root).as_posix()

    def save_payload(self, payload: dict[str, object]) -> Path:
        scope = str(payload["scope"])
        output = imported_decision_path(self.workspace_root, scope)
        state = self.workspace_root / ".cleanup-extracted"
        if (state.is_symlink() or not inside(state, output) or output.is_symlink()
                or output.parent.is_symlink()):
            raise RequestError("decision output escapes controlled run state")
        output.parent.mkdir(parents=True, exist_ok=True)
        # Replace the directory entry, never write through a pre-existing hardlink.
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        try:
            os.replace(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
        return output

    def send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_body(status, body, "application/json; charset=utf-8")

    def send_body(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.close_connection = True
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "frame-ancestors 'none'; base-uri 'none'; object-src 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


def configured_handler(
    root: Path, adapter: Path, pipeline: Path, scope: str = ".", *,
    allow_write: bool = False, allow_apply: bool = False,
    allow_file_open: bool = False, session_token: str = "",
) -> Type[ReviewHandler]:
    class Handler(ReviewHandler):
        workspace_root = root.resolve()
        adapter_path = adapter.resolve()
        pipeline_path = pipeline.resolve()
        scope_path = resolve_scope(root, scope)
        workbench_path = scope_path / "cleanup-asset-review-workbench.html"
        archive_scope_path = workspace_root / "Archived" / scope_path.relative_to(workspace_root)
        render_workbench = staticmethod(installed_renderer())
        request_token = secrets.token_urlsafe(32)

    Handler.allow_write = allow_write or allow_apply
    Handler.allow_apply = allow_apply
    Handler.allow_file_open = allow_file_open
    # Retain the configuration attribute for callers; request capabilities are fresh per server.
    Handler.session_token = session_token
    return Handler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--scope", default=".")
    parser.add_argument("--adapter", type=Path, default=DEFAULT_ADAPTER)
    parser.add_argument("--pipeline", type=Path, default=DEFAULT_PIPELINE)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--enable-write", action="store_true", help="Allow saving decisions through the local server / 允许通过本地 server 保存 decisions。")
    parser.add_argument("--enable-apply", action="store_true", help="Allow applying decisions and enable writes / 允许应用 decisions，并同时启用写入。")
    parser.add_argument("--enable-file-open", action="store_true", help="Allow opening reviewed files through the local server / 允许通过本地 server 打开已 review 的文件。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        host = loopback_host(args.host)
    except ValueError as exc:
        raise SystemExit("--host must be a loopback IP address or localhost") from exc
    root = args.root.expanduser().resolve()
    scope = resolve_scope(root, args.scope)
    adapter = args.adapter.expanduser().resolve()
    pipeline = args.pipeline.expanduser().resolve()
    if not adapter.is_file():
        raise SystemExit(f"missing adapter: {adapter}")
    if not pipeline.is_file():
        raise SystemExit(f"missing pipeline: {pipeline}")
    relative_workbench = (scope / "cleanup-asset-review-workbench.html").relative_to(root).as_posix()
    server_type = ThreadingHTTPServer
    if ":" in host:
        class IPv6Server(ThreadingHTTPServer):
            address_family = socket.AF_INET6
        server_type = IPv6Server
    server = server_type((host, args.port), configured_handler(
        root, adapter, pipeline, args.scope,
        allow_write=args.enable_write or args.enable_apply,
        allow_apply=args.enable_apply, allow_file_open=args.enable_file_open,
    ))
    authority = f"[{host}]" if ":" in host else host
    url = f"http://{authority}:{server.server_address[1]}/{parse.quote(relative_workbench)}"
    print(f"Serving review workbench / 正在提供 review workbench: {url}", flush=True)
    if args.open:
        subprocess.run(["open", url], check=False)
    server.serve_forever()


if __name__ == "__main__":
    main()
