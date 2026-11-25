"""On-demand tool relay. The host calls native MCP; OAuth secrets never enter Python."""
from __future__ import annotations

import atexit
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from .common import APIError, Conflict, ManagerError, NetworkError, canonical
from .transport import HTTP


def validate_reply(response):
    if not isinstance(response, dict) or type(response.get("id")) is not int or type(response.get("ok")) is not bool:
        raise ManagerError("MCP relay accepts only explicit, plain JSON response objects")
    field = "data" if response["ok"] else "error"
    if set(response) != {"id", "ok", field} or not isinstance(response[field], dict):
        raise ManagerError("MCP relay response schema is invalid; encoded frames and commands are refused")
    return response


class MCPRelay:
    @staticmethod
    def page_revision(page):
        timestamp = page.get("last_edited_time", "")
        if isinstance(timestamp, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", timestamp):
            return 'W/"' + timestamp + '"'
        return ""

    def __init__(self, *, network_mode="system", input_stream=None, output_stream=None, transfer_client=None):
        self.input = input_stream or sys.stdin
        self.output = output_stream or sys.stdout
        self.files = transfer_client or HTTP("unused-by-mcp-file-transfer", network_mode=network_mode)
        self.counter, self.identity = 0, None
        self._terminal = None
        if self.input is sys.stdin and self.input.isatty():
            try:
                import termios
                old = termios.tcgetattr(self.input.fileno())
                new = list(old)
                # Canonical TTY input silently truncates long JSON replies (often at 4 KiB).
                # Read newline-delimited JSON ourselves, without echoing signed responses.
                new[3] &= ~(termios.ECHO | termios.ICANON)
                new[6] = list(old[6])
                new[6][termios.VMIN] = 1
                new[6][termios.VTIME] = 0
                termios.tcsetattr(self.input.fileno(), termios.TCSANOW, new)
                self._terminal = (termios, old)
                atexit.register(self.close)
            except (ImportError, OSError):
                raise ManagerError("MCP relay requires pipes or a terminal with input echo disabled") from None

    def close(self):
        if self._terminal:
            module, old = self._terminal
            module.tcsetattr(self.input.fileno(), module.TCSANOW, old)
            self._terminal = None

    def call(self, tool, arguments):
        self.counter += 1
        identifier = self.counter
        request = canonical({"id": identifier, "tool": tool, "arguments": arguments})
        # Ordinary metadata may use a private temporary file. Signed transactions stay on stdin.
        with tempfile.TemporaryDirectory(prefix="cva-mcp-request-") as directory:
            path = Path(directory) / "request.json"
            path.write_text(request, encoding="utf-8")
            print("CVA_MCP_REQUEST " + canonical({"id": identifier, "tool": tool,
                  "request_file": str(path), "request_chars": len(request)}), file=self.output, flush=True)
            raw = self.input.readline(16 * 1024 * 1024 + 1)
            if not raw or len(raw) > 16 * 1024 * 1024:
                raise ManagerError("MCP relay disconnected or response too large; reconcile before retrying")
            try:
                response = json.loads(raw)
                if isinstance(response, dict) and response.get("response_file"):
                    if set(response) != {"id", "response_file"} or response.get("id") != identifier:
                        raise ManagerError("Invalid MCP metadata response reference")
                    response_path = Path(response["response_file"])
                    if response_path != path.with_name("response.json") or response_path.is_symlink():
                        raise ManagerError("Unexpected MCP metadata response path")
                    if response_path.stat().st_size > 16 * 1024 * 1024:
                        raise ManagerError("MCP metadata response exceeds bound")
                    response = json.loads(response_path.read_text(encoding="utf-8"))
                    response_path.unlink()
                response = validate_reply(response)
            except (ValueError, OSError):
                raise ManagerError("Invalid MCP relay response") from None
        if not isinstance(response, dict) or response.get("id") != identifier:
            raise ManagerError("MCP relay response ID mismatch")
        if not response.get("ok"):
            error = response.get("error", {})
            status = error.get("statusCode", error.get("status"))
            if error.get("code") == "mcp_transport_error":
                raise NetworkError("mcp_transport", "native_mcp", operation=tool)
            if status in (409, 412) or error.get("code") in ("conflict", "idempotency_conflict"):
                raise Conflict("Native MCP rejected a stale revision or conflicting request")
            if isinstance(status, int):
                raise APIError(status, "Native MCP request failed")
            raise ManagerError("Native MCP tool call failed; reconcile before retrying")
        value = response.get("data")
        if not isinstance(value, dict):
            raise ManagerError("Native MCP returned an invalid object")
        return value

    def request(self, method, path, body=None, *, etag=None, idempotency=None):
        parsed = urlsplit(path)
        parts = parsed.path.strip("/").split("/")
        query = {key: values[0] for key, values in parse_qs(parsed.query).items()}
        args = {}
        if method == "GET" and parsed.path == "/users/me":
            if self.identity is None:
                self.identity = self.call("flowus_get_current_user", {})
            return self.identity, {}
        if method == "GET" and parsed.path == "/openapi.json":
            # This is a named-tool contract projection, not a fabricated full OpenAPI document.
            guide = self.call("flowus_help", {"query": ["flowus_get_page_markdown"], "detail": "input"})
            paths = {}
            for result in guide.get("results", [guide]):
                operation = result.get("operation", {})
                if result.get("callable") and operation.get("path"):
                    paths.setdefault(operation["path"], {})[operation["method"].lower()] = {}
            return {"x-contract-source": "native_mcp_help", "paths": paths}, {}
        if parts[0] == "pages":
            if method == "POST" and len(parts) == 1:
                tool, args = "flowus_create_page", {"body": body}
                if idempotency:
                    args["idempotency_key"] = idempotency
            elif len(parts) == 2 and method in ("GET", "PATCH"):
                tool = "flowus_get_page" if method == "GET" else "flowus_update_page"
                args = {"page_id": parts[1]}
                if method == "PATCH":
                    if not etag:
                        raise ManagerError("Native MCP page updates require an explicit revision")
                    args.update(body=body, if_match=etag)
            elif method == "PATCH" and len(parts) == 3 and parts[2] == "move":
                tool, args = "flowus_move_page", {"page_id": parts[1], "body": body}
            elif method == "GET" and len(parts) == 4 and parts[2:] == ["content", "markdown"]:
                tool, args = "flowus_get_page_markdown", {"page_id": parts[1]}
            else:
                raise ManagerError("Unsupported native MCP page operation")
        elif parts[0] == "databases":
            if method == "POST" and len(parts) == 1:
                tool, args = "flowus_create_database", {"body": body}
            elif method == "GET" and len(parts) == 2:
                tool, args = "flowus_get_database", {"database_id": parts[1]}
            elif method == "POST" and len(parts) == 3 and parts[2] == "query":
                query_body = dict(body or {})
                args = {"database_id": parts[1]}
                for name in ("page_size", "start_cursor"):
                    if name in query_body:
                        args[name] = query_body.pop(name)
                if query_body:
                    args["body"] = query_body
                tool = "flowus_query_database"
            else:
                raise ManagerError("Unsupported native MCP database operation")
        elif parts[0] == "blocks" and len(parts) in (2, 3):
            args = {"block_id": unquote(parts[1])}
            if len(parts) == 2 and method in ("GET", "PATCH"):
                tool = "flowus_get_block" if method == "GET" else "flowus_update_block"
                if method == "PATCH":
                    args["body"] = body
            elif len(parts) == 3 and parts[2] == "children" and method in ("GET", "PATCH"):
                tool = "flowus_get_block_children" if method == "GET" else "flowus_append_block_children"
                if method == "GET":
                    if "page_size" in query:
                        args["page_size"] = int(query["page_size"])
                    if "start_cursor" in query:
                        args["start_cursor"] = query["start_cursor"]
                else:
                    args["body"] = body
            else:
                raise ManagerError("Unsupported native MCP block operation")
        elif method == "POST" and parsed.path == "/files/upload-url":
            tool = "flowus_create_file_upload"
            args = {"filename": body["filename"], "content_type": body["content_type"],
                    "content_length": body["content_length"], "parent_page_id": body["parent"]["page_id"]}
        else:
            raise ManagerError("No explicit native MCP tool for this operation")
        value = self.call(tool, args)
        headers = {}
        # Official weak-ETag contract; both fresh acceptance and stale rejection must pass doctor.
        if parts[0] == "pages" and len(parts) <= 2 and self.page_revision(value):
            headers["ETag"] = self.page_revision(value)
        return value, headers

    def transfer(self, method, url, data=None, headers=None):
        return self.files.transfer(method, url, data, headers)
