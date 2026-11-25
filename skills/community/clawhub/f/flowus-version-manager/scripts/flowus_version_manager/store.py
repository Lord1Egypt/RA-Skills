from __future__ import annotations

import copy
import hashlib
import html
import mimetypes
import os
import re
import uuid
from dataclasses import dataclass

from . import SCHEMA_VERSION
from .common import APIError, Conflict, GateError, DownloadUnavailable, ManagerError, MissingAttachment, canonical, stable_id, governance_mode, credential_value, network_mode, transport_mode, rest_auth_mode
from .transport import HTTP, MAX_FILE, check_file_url

TABLES = {"documents": "文档目录", "versions": "文件版本", "events": "操作记录", "proposals": "变更提案", "approvals": "审批记录"}
FIELDS = {"Name": "title", "Key": "rich_text", "Status": "rich_text", "Category": "rich_text",
          "Latest": "rich_text", "ApprovalCode": "rich_text", "Payload": "rich_text"}


def rich(value):
    value = str(value)
    return [{"type": "text", "text": {"content": value[i:i + 1800]}} for i in range(0, len(value), 1800)]


def plain(value):
    return "".join(item.get("plain_text", item.get("text", {}).get("content", "")) for item in (value or []))


def schema():
    fields = {name: {"name": name, "type": kind} for name, kind in FIELDS.items()}
    fields["Decision"] = {"name": "Decision", "type": "select", "select": {
        "options": [{"name": name} for name in ("Pending", "Approved", "Rejected")]}}
    return fields


def properties(key, data):
    values = {"Name": data.get("title", key), "Key": key, "Status": data.get("status", ""),
              "Category": data.get("category", ""), "Latest": data.get("latest", ""),
              "ApprovalCode": data.get("approval_code", ""), "Payload": canonical(data)}
    result = {name: {"type": kind, kind: rich(values[name])} for name, kind in FIELDS.items()}
    result["Decision"] = {"type": "select", "select": {"name": data.get("decision", "Pending")}}
    return result


@dataclass
class Record:
    id: str
    key: str
    data: dict
    etag: str
    url: str = ""


class FlowUsStore:
    """Shared storage; governance is explicitly selected in private configuration."""

    def __init__(self, config, *, writer=None, reader=None):
        self.config = config
        if writer is None and rest_auth_mode(config) == "flowus_cli":
            from .cli_transport import CLIHTTP
            writer = CLIHTTP(network_mode=network_mode(config))
        if writer is None and transport_mode(config) == "mcp_relay":
            from .mcp_relay import MCPRelay
            writer = MCPRelay(network_mode=network_mode(config))
        self.writer = writer or HTTP(credential_value("FLOWUS_API_TOKEN"), network_mode=network_mode(config))
        self.reader = reader or (self.writer if governance_mode(config) == "trusted_client"
                                 else HTTP(os.environ.get("FLOWUS_APPROVAL_READ_TOKEN", ""), network_mode=network_mode(config)))
        self._download_spec = None

    def client(self, table):
        return self.reader if table == "approvals" else self.writer

    def database(self, table):
        try:
            return self.config["databases"][table]
        except KeyError:
            raise GateError(f"Missing {table} database; run init --provision") from None

    def decode(self, page, headers=None):
        props = page.get("properties", {})
        raw = plain(props.get("Payload", {}).get("rich_text"))
        data = __import__("json").loads(raw) if raw else {}
        if not isinstance(data, dict):
            raise ManagerError("Cloud Payload must be a JSON object")
        for field, name in [("Name", "title"), ("Status", "status"), ("Category", "category"),
                            ("Latest", "latest"), ("ApprovalCode", "approval_code")]:
            if field in props:
                data[name] = plain(props[field].get(FIELDS[field]))
        if "Decision" in props:
            data["decision"] = (props["Decision"].get("select") or {}).get("name", "Pending")
        key = plain(props.get("Key", {}).get("rich_text")) or page["id"]
        etag = next((v for k, v in (headers or {}).items() if k.lower() == "etag"), "")
        return Record(page["id"], key, data, etag, page.get("url") or "https://flowus.cn/" + page["id"])

    def list(self, table, key=None):
        result, cursor = [], None
        while True:
            body = {"page_size": 100}
            if cursor:
                body["start_cursor"] = cursor
            if key is not None:
                body["filter"] = {"property": "Key", "rich_text": {"equals": key}}
            data, _ = self.client(table).request("POST", f"/databases/{self.database(table)}/query", body)
            for item in data.get("results", []):
                revision = getattr(self.client(table), "page_revision", lambda page: "")(item)
                if revision and item.get("parent", {}).get("database_id") != self.database(table):
                    raise ManagerError("Query returned a record outside the configured database")
                result.append(self.decode(item, {"ETag": revision} if revision else None))
            if not data.get("has_more"):
                return result
            next_cursor = data.get("next_cursor")
            if not next_cursor or next_cursor == cursor:
                raise ManagerError("Invalid pagination cursor")
            cursor = next_cursor

    def get(self, table, key):
        found = self.list(table, key)
        if not found:
            return None
        if len(found) != 1:
            raise Conflict("Duplicate cloud keys; manual reconciliation is required")
        # Native query pages carry the same documented revision as GET /pages.
        # Keep the exact data/revision snapshot; a later edit is rejected by If-Match.
        return found[0] if found[0].etag else self.by_id(table, found[0].id)

    def by_id(self, table, page_id):
        page, headers = self.client(table).request("GET", f"/pages/{page_id}")
        parent = page.get("parent", {})
        if parent.get("database_id") != self.database(table):
            raise ManagerError("Record does not belong to the configured database")
        return self.decode(page, headers)

    def create(self, table, key, data):
        if table == "approvals":
            raise GateError("Only the human owner may create approval records in FlowUs")
        existing = self.get(table, key)
        if existing:
            return existing
        body = {"parent": {"database_id": self.database(table)}, "properties": properties(key, data)}
        try:
            page, headers = self.writer.request("POST", "/pages", body,
                idempotency=stable_id(self.config["vault_id"], table, key))
            record = self.decode(page, headers)
            return record if record.etag else self.by_id(table, record.id)
        except Conflict:
            existing = self.get(table, key)
            if existing:
                return existing
            raise

    def update(self, table, record, data):
        if table == "approvals":
            raise GateError("Approval database is read-only for all ordinary clients")
        if not record.etag:
            raise GateError("FlowUs did not provide ETag; refusing an unprotected update")
        page, headers = self.writer.request("PATCH", f"/pages/{record.id}",
            {"properties": properties(record.key, data)}, etag=record.etag)
        return self.decode(page, headers)

    def children(self, page_id):
        result, cursor = [], None
        while True:
            path = f"/blocks/{page_id}/children?page_size=100"
            if cursor:
                from urllib.parse import quote
                path += "&start_cursor=" + quote(cursor, safe="")
            response, _ = self.writer.request("GET", path)
            result.extend(response.get("results", []))
            if not response.get("has_more"):
                return result
            following = response.get("next_cursor")
            if not following or following == cursor:
                raise ManagerError("Invalid block pagination")
            cursor = following

    def upload(self, record, content, filename):
        if len(content) > MAX_FILE:
            raise ManagerError("FlowUs API supports at most 100 MiB per file")
        # Unrecognized MIME types, e.g. xlsm, are sent as the documented generic binary MIME.
        mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        allowed = {"application/pdf", "application/msword", "application/vnd.ms-excel", "text/plain",
                   "text/csv", "text/markdown", "application/zip", "application/json"}
        if mime not in allowed and not mime.startswith("application/vnd.openxmlformats-officedocument."):
            mime = "application/octet-stream"
        info, _ = self.writer.request("POST", "/files/upload-url", {
            "filename": filename, "content_type": mime, "content_length": len(content),
            "parent": {"type": "page_id", "page_id": record.id}})
        if info.get("method", "PUT") != "PUT" or info.get("size") != len(content) or not info.get("oss_name"):
            raise GateError("Unexpected FlowUs upload contract")
        self.writer.transfer("PUT", info["upload_url"], content, info.get("headers"))
        block = {"object": "block", "type": "file", "file": {
            "type": "file", "file": {"oss_name": info["oss_name"], "size": len(content)},
            "caption": rich(filename)}}
        self.writer.request("PATCH", f"/blocks/{record.id}/children", {"children": [block]})
        downloaded = self.download(record)
        if hashlib.sha256(downloaded).digest() != hashlib.sha256(content).digest():
            raise ManagerError("Uploaded file hash mismatch; latest remains unchanged")
        return {"sha256": hashlib.sha256(content).hexdigest(), "size": len(content)}

    def download(self, record):
        candidates = [item for item in self.children(record.id) if item.get("type") == "file"]
        if not candidates:
            raise MissingAttachment("Version has no downloadable file block")
        # Every retry gets fresh file URLs from FlowUs instead of persisting expiring links.
        for item in reversed(candidates):
            if item.get("file", {}).get("type") == "external":
                continue
            content = self.download_block(item)
            expected = record.data.get("sha256")
            if not expected or hashlib.sha256(content).hexdigest() == expected:
                return content
        raise ManagerError("No internal file block matches the version hash")

    def download_url(self, block):
        info = block.get("file", {})
        if info.get("type") != "file":
            raise GateError("Only internal FlowUs attachments can be ingested")
        file = info.get("file", {})
        url = file.get("url")
        if not url and file.get("oss_name") and block.get("parent"):
            url = self.markdown_download_url(block)
        if not url:
            # Discover the public contract, never guess private routes or unsigned CDN links.
            if self._download_spec is None:
                self._download_spec, _ = self.writer.request("GET", "/openapi.json")
            endpoint = self._download_spec.get("paths", {}).get("/v2/files/download-url", {})
            if "get" not in endpoint:
                raise DownloadUnavailable("Attachment metadata and page export returned no exact file URL, "
                                          "and no direct download operation is declared; migration remains blocked")
            oss = file.get("oss_name")
            if not oss or not block.get("id"):
                raise GateError("Attachment is missing its block ID or storage key")
            from urllib.parse import urlencode
            response, _ = self.writer.request("GET", "/files/download-url?" + urlencode({
                "block_id": block["id"], "oss_name": oss}))
            url = response.get("file", {}).get("url")
            if not url:
                raise DownloadUnavailable("Authenticated attachment response has no download URL")
        return url

    def markdown_download_url(self, block):
        from urllib.parse import quote, unquote, urlsplit
        parent = block.get("parent", {})
        visited = set()
        for _ in range(32):
            if parent.get("type") == "page_id":
                page_id = parent.get("page_id")
                break
            ancestor = parent.get("block_id") if parent.get("type") == "block_id" else None
            if not ancestor or ancestor in visited:
                return None
            visited.add(ancestor)
            data, _ = self.writer.request("GET", "/blocks/" + quote(ancestor, safe=""))
            parent = data.get("parent", {})
        else:
            raise GateError("Attachment parent chain is too deep")
        if not page_id:
            return None
        export, _ = self.writer.request("GET", "/pages/" + quote(page_id, safe="") + "/content/markdown")
        markdown = export.get("markdown", "")
        oss = block["file"]["file"]["oss_name"].lstrip("/")
        # Use only actual links emitted by the official export; never synthesize a CDN URL.
        matches = []
        for raw in re.findall(r"https://[^\s<>\"\\]+", markdown):
            candidate = html.unescape(raw[:-1] if raw.endswith(")") else raw)
            parsed = urlsplit(candidate)
            if unquote(parsed.path).lstrip("/") != oss:
                continue
            check_file_url(candidate)
            if candidate not in matches:
                matches.append(candidate)
        if len(matches) > 1:
            raise GateError("Page export returned ambiguous links for one storage object")
        return matches[0] if matches else None

    def download_block(self, block):
        url = self.download_url(block)
        try:
            return self.writer.transfer("GET", url)
        except APIError as error:
            if error.status not in (401, 403) or not block.get("id"):
                raise
        # At most one refresh. A rejected URL never causes another upload or a guessed URL.
        from urllib.parse import quote
        refreshed, _ = self.writer.request("GET", "/blocks/" + quote(block["id"], safe=""))
        before = block.get("file", {}).get("file", {}).get("oss_name")
        after = refreshed.get("file", {}).get("file", {}).get("oss_name")
        if refreshed.get("id") != block["id"] or before != after:
            raise Conflict("Attachment changed while refreshing its download URL")
        return self.writer.transfer("GET", self.download_url(refreshed))
