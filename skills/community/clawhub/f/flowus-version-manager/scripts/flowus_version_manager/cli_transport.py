"""Explicit REST authentication through the installed official FlowUs CLI.

Credentials remain in the CLI. Only ordinary request bodies use private temporary
files; signed response URLs stay in memory and never become process arguments.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .common import APIError, Conflict, GateError, ManagerError, canonical
from .transport import HTTP


class CLIHTTP:
    def __init__(self, *, network_mode="system"):
        self.executable = shutil.which("flowus")
        if not self.executable:
            raise GateError("Install and authorize the official FlowUs CLI before selecting flowus_cli authentication")
        self.files = HTTP("unused-by-cli-file-transfer", network_mode=network_mode)
        self.identity = self.current_identity()

    def _run(self, arguments, *, raw=False):
        try:
            result = subprocess.run([self.executable, "--base-url", "https://api.flowus.cn", "--json", "--no-retry", *arguments],
                                    capture_output=True, text=True, timeout=60, check=False)
            if len(result.stdout) > 16 * 1024 * 1024:
                raise ManagerError("FlowUs CLI response exceeds its safety bound")
            value = json.loads(result.stdout)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            raise ManagerError("FlowUs CLI failed; inspect its login/network locally and reconcile before retrying") from None
        if raw:
            if result.returncode or not isinstance(value, dict):
                raise ManagerError("Official CLI contract lookup failed")
            return value
        if not isinstance(value, dict) or value.get("ok") is not True or result.returncode:
            error = value.get("error", {}) if isinstance(value, dict) else {}
            status = error.get("status", 0)
            if status in (409, 412):
                raise Conflict("FlowUs CLI rejected a stale revision or conflicting request")
            if type(status) is int and status >= 400:
                raise APIError(status, "FlowUs CLI request failed")
            raise ManagerError("FlowUs CLI request failed; no credential or response details were logged")
        if not isinstance(value.get("data"), dict):
            raise ManagerError("FlowUs CLI returned an invalid data object")
        return value["data"]

    def current_identity(self):
        state = self._run(["doctor"])
        if not state.get("authenticated") or not isinstance(state.get("user"), dict) or not state["user"].get("id"):
            raise GateError("FlowUs CLI is not authenticated; complete the explicitly approved login locally")
        return state["user"]

    def verify_identity(self, expected):
        identity = self.current_identity()
        if not expected or identity.get("id") != expected:
            raise GateError("FlowUs CLI identity changed; repeat doctor --verify-writes")
        return identity

    @staticmethod
    def page_revision(page):
        timestamp = page.get("last_edited_time", "")
        return ('W/"' + timestamp + '"') if isinstance(timestamp, str) and re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", timestamp) else ""

    def request(self, method, path, body=None, *, etag=None, idempotency=None):
        if method not in {"GET", "POST", "PATCH"} or not path.startswith("/") or "://" in path or ".." in path:
            raise ManagerError("Unsupported FlowUs CLI operation")
        parsed = urlsplit(path)
        parts = parsed.path.strip("/").split("/")
        query = parse_qs(parsed.query)
        if any(len(values) != 1 for values in query.values()) or set(query) - {"page_size", "start_cursor"}:
            raise ManagerError("Unsupported CLI query parameters")
        if method == "GET" and path == "/users/me":
            return self.verify_identity(self.identity["id"]), {}
        if method == "GET" and path == "/openapi.json":
            spec = self._run(["api", "--spec", "/v2/pages/{page_id}/content/markdown", "-X", "GET"], raw=True)
            return {"x-contract-source": "official_cli_embedded_openapi", "paths": spec.get("paths", {})}, {}
        identifier = parts[1] if len(parts) > 1 else None
        if parts[0] in {"pages", "databases", "blocks"} and identifier and not re.fullmatch(r"[a-fA-F0-9-]{32,36}", identifier):
            raise ManagerError("Invalid CLI resource identifier")
        arguments = None
        if parts[0] == "pages":
            if method == "POST" and len(parts) == 1:
                arguments = ["page", "create"]
                if idempotency:
                    arguments += ["--idempotency-key", idempotency]
            elif len(parts) == 2 and method in {"GET", "PATCH"}:
                arguments = ["page", "get" if method == "GET" else "update", identifier]
                if method == "PATCH":
                    if not etag:
                        raise GateError("CLI page updates require an explicit revision")
                    arguments += ["--if-match", etag]
            elif len(parts) == 4 and parts[2:] == ["content", "markdown"] and method == "GET":
                arguments = ["markdown", "get", identifier]
            elif len(parts) == 3 and parts[2] == "move" and method == "PATCH":
                arguments = ["api", "call", method, "/v2" + parsed.path]
        elif parts[0] == "databases":
            if len(parts) == 1 and method == "POST":
                arguments = ["database", "create"]
            elif len(parts) == 2 and method == "GET":
                arguments = ["database", "get", identifier]
            elif len(parts) == 3 and parts[2] == "query" and method == "POST":
                arguments = ["database", "query", identifier]
        elif parts[0] == "blocks":
            if len(parts) == 2 and method in {"GET", "PATCH"}:
                arguments = ["block", "get" if method == "GET" else "update", identifier]
            elif len(parts) == 3 and parts[2] == "children" and method in {"GET", "PATCH"}:
                arguments = ["block", "children" if method == "GET" else "append", identifier]
                if method == "GET":
                    for key, values in query.items():
                        arguments += ["--" + key.replace("_", "-"), values[0]]
        elif path == "/files/upload-url" and method == "POST":
            # file upload cannot return the pre-transfer transaction required by Store.upload.
            arguments = ["api", "call", method, "/v2/files/upload-url"]
        if arguments is None:
            raise ManagerError("No explicit official CLI command for this operation")
        if method != "GET" and not path.endswith("/query"):
            self.verify_identity(self.identity["id"])
        with tempfile.TemporaryDirectory(prefix="cva-cli-body-") as directory:
            if body is not None:
                body_path = Path(directory) / "body.json"
                body_path.write_text(canonical(body), encoding="utf-8")
                arguments += ["--body", str(body_path)]
            data = self._run(arguments)
        revision = self.page_revision(data) if parts[0] == "pages" else ""
        return data, {"ETag": revision} if revision else {}

    def transfer(self, method, url, data=None, headers=None):
        return self.files.transfer(method, url, data, headers)
