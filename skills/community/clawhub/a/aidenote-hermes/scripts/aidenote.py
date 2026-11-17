#!/usr/bin/env python3
"""Deterministic, secret-safe AideNote API client for Hermes skills."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys
from dataclasses import dataclass
from typing import Any
from urllib import error, parse, request


DEFAULT_API_BASE = "https://api.aidenote.cn"
TOKEN_PATH = "/api/UserapikeyMstr/GetToken/{api_key}"
TIMEOUT_SECONDS = 30


class AideNoteError(Exception):
    def __init__(self, code: str, message: str, *, operation: str = "") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.operation = operation


def emit(value: Any, *, stream: Any = sys.stdout) -> None:
    json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
    stream.write("\n")


def first_nonempty(*values: Any) -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def find_token(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("accessToken", "token", "bridgeToken", "tunnelToken"):
            token = value.get(key)
            if isinstance(token, str) and token.strip():
                return token.strip()
        for key in ("result", "data", "token"):
            if key in value:
                token = find_token(value[key])
                if token:
                    return token
    if isinstance(value, list):
        for item in value:
            token = find_token(item)
            if token:
                return token
    return ""


def result_value(value: Any) -> Any:
    return value.get("result") if isinstance(value, dict) else None


def result_items(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("items", "records", "list", "data"):
            items = value.get(key)
            if isinstance(items, list):
                return items
    return []


def first_value(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = row.get(key)
        if value is not None and str(value).strip():
            return value
    return None


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value or "").strip().lower() in {"true", "1", "yes"}


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def validate_api_base(raw: str) -> str:
    value = raw.strip().rstrip("/")
    parsed = parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise AideNoteError("invalid_config", "AIDENOTE_API_BASE must be an HTTP(S) URL")
    if parsed.username or parsed.password:
        raise AideNoteError("invalid_config", "AIDENOTE_API_BASE must not contain credentials")
    return value


def safe_api_message(value: Any) -> str:
    text = " ".join(str(value or "").split())
    lowered = text.lower()
    internal_markers = (
        "sqlstate",
        "null value in column",
        "relation \"",
        "constraint",
        "connection string",
        "stack trace",
        "exception at",
    )
    if not text or len(text) > 240 or any(marker in lowered for marker in internal_markers):
        return "AideNote could not complete the requested operation"
    return text


def decode_response(response: Any, *, operation: str) -> Any:
    raw = response.read()
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AideNoteError(
            "invalid_response",
            f"AideNote returned invalid JSON for {operation}",
            operation=operation,
        ) from exc


@dataclass
class Client:
    api_base: str
    api_key: str
    token: str = ""

    @classmethod
    def from_credentials(cls) -> "Client":
        hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))).expanduser()
        credentials_path = hermes_home / "aidenote-credentials.json"
        if not credentials_path.is_file():
            raise AideNoteError(
                "missing_credentials",
                "AideNote credentials are not configured. Run the Skill's scripts/configure.py locally.",
            )
        if os.name != "nt" and stat.S_IMODE(credentials_path.stat().st_mode) & 0o077:
            raise AideNoteError(
                "insecure_credentials",
                "AideNote credentials must be readable only by the current user. Rerun scripts/configure.py.",
            )
        try:
            credentials = json.loads(credentials_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AideNoteError(
                "invalid_credentials",
                "AideNote credentials could not be read. Rerun scripts/configure.py.",
            ) from exc
        if not isinstance(credentials, dict):
            raise AideNoteError("invalid_credentials", "AideNote credentials have an invalid format")
        api_key = first_nonempty(credentials.get("apiKey"))
        if not api_key:
            raise AideNoteError("invalid_credentials", "AideNote credentials do not contain an API Key")
        api_base = validate_api_base(first_nonempty(credentials.get("apiBase"), DEFAULT_API_BASE))
        return cls(api_base=api_base, api_key=api_key)

    def exchange_token(self) -> str:
        if self.token:
            return self.token
        endpoint = self.api_base + TOKEN_PATH.format(api_key=parse.quote(self.api_key, safe=""))
        payload = json.dumps({"apiKey": self.api_key}).encode("utf-8")
        req = request.Request(
            endpoint,
            data=payload,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            },
        )
        decoded = self._open(req, operation="token exchange", authentication=True)
        token = find_token(decoded)
        if not token:
            raise AideNoteError(
                "authentication_failed",
                "AideNote authentication response did not contain an access token",
                operation="token exchange",
            )
        self.token = token
        return token

    def post(self, path: str, body: dict[str, Any] | None, *, operation: str) -> Any:
        payload = None if body is None else json.dumps(body).encode("utf-8")
        for attempt in range(2):
            token = self.exchange_token()
            req = request.Request(
                self.api_base + path,
                data=payload,
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            try:
                decoded = self._open(req, operation=operation)
            except AideNoteError as exc:
                if attempt == 0 and exc.code == "authentication_failed":
                    self.token = ""
                    continue
                raise
            if isinstance(decoded, dict) and "code" in decoded:
                code = str(decoded.get("code"))
                if attempt == 0 and code in {"401", "403"}:
                    self.token = ""
                    continue
                if code != "200":
                    message = safe_api_message(decoded.get("message"))
                    raise AideNoteError("api_error", message, operation=operation)
            return decoded
        raise AideNoteError(
            "authentication_failed",
            "AideNote authentication retry failed",
            operation=operation,
        )

    def _open(self, req: request.Request, *, operation: str, authentication: bool = False) -> Any:
        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                return decode_response(response, operation=operation)
        except error.HTTPError as exc:
            if authentication or exc.code in {401, 403}:
                raise AideNoteError(
                    "authentication_failed",
                    f"AideNote authentication failed (HTTP {exc.code})",
                    operation=operation,
                ) from exc
            raise AideNoteError(
                "api_error",
                f"AideNote request failed (HTTP {exc.code})",
                operation=operation,
            ) from exc
        except (error.URLError, TimeoutError, OSError) as exc:
            raise AideNoteError(
                "network_error",
                f"Could not reach AideNote during {operation}",
                operation=operation,
            ) from exc


def list_recordings(
    client: Client,
    args: argparse.Namespace,
    *,
    shared_with_me: bool = False,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "page": clamp(args.page, 1, 1_000_000),
        "pageSize": clamp(args.page_size, 1, 50),
        "orderField": "createTime",
        "order": "descending",
    }
    if shared_with_me:
        body["screeningType"] = "2"
    if args.keyword:
        body["selectValue"] = args.keyword
    response = client.post(
        "/api/audiofileMstr/audiofileseleUserAllList",
        body,
        operation="list shared recordings" if shared_with_me else "list recordings",
    )
    result = result_value(response)
    items = result_items(result)
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "fileId": first_value(item, "audiofileFileid", "fileId", "id"),
                "title": first_value(item, "audiofileTitle", "audiofileFileName", "title"),
                "createTime": first_value(item, "createTime"),
                "durationMs": first_value(item, "audiofileTimeLength", "duration"),
                "transcriptStatus": first_value(item, "transcriptStatus"),
                "summaryStatus": first_value(item, "summaryStatus"),
                "type": first_value(item, "audiofileType", "type"),
            }
        )
    total = result.get("total") if isinstance(result, dict) else len(normalized)
    return {
        "ok": True,
        "operation": "shared-recordings" if shared_with_me else "recordings",
        "total": total,
        "page": body["page"],
        "pageSize": body["pageSize"],
        "items": normalized,
    }


def recordings(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    return list_recordings(client, args)


def shared_recordings(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    return list_recordings(client, args, shared_with_me=True)


def recording_detail(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    response = client.post(
        "/api/audiofileMstr/audiofileToText",
        {"audiototextFileid": args.file_id},
        operation="get recording detail",
    )
    return {
        "ok": True,
        "operation": "recording-detail",
        "fileId": args.file_id,
        "result": result_value(response),
    }


def todos(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    scan_count = clamp(args.recording_page_size, 1, 50)
    response = client.post(
        "/api/audiofileMstr/audiofileseleUserAllList",
        {
            "page": 1,
            "pageSize": scan_count,
            "orderField": "createTime",
            "order": "descending",
        },
        operation="list recordings for todos",
    )
    recent = result_items(result_value(response))
    found: list[dict[str, Any]] = []
    for recording in recent:
        if not isinstance(recording, dict):
            continue
        file_id = first_nonempty(first_value(recording, "audiofileFileid", "fileId", "id"))
        if not file_id:
            continue
        todo_response = client.post(
            "/api/audiofileTodo/listByFile",
            {
                "audiofileTodoFileid": file_id,
                "includeDeleted": args.include_deleted,
            },
            operation="list recording todos",
        )
        for todo in result_items(result_value(todo_response)):
            if not isinstance(todo, dict):
                continue
            done = as_bool(first_value(todo, "audiofileTodoIsDone", "isDone"))
            if done and not args.include_done:
                continue
            found.append(
                {
                    "id": first_value(todo, "id"),
                    "content": first_value(todo, "audiofileTodoContent", "content"),
                    "isDone": done,
                    "source": first_value(todo, "audiofileTodoSource", "source"),
                    "createTime": first_value(todo, "createTime"),
                    "doneTime": first_value(todo, "audiofileTodoDoneTime", "doneTime"),
                    "recordingId": file_id,
                    "recording": {
                        "title": first_value(recording, "audiofileTitle", "audiofileFileName", "title"),
                        "createTime": first_value(recording, "createTime"),
                    },
                }
            )
    page = clamp(args.page, 1, 1_000_000)
    page_size = clamp(args.page_size, 1, 100)
    start = min((page - 1) * page_size, len(found))
    end = min(start + page_size, len(found))
    return {
        "ok": True,
        "operation": "todos",
        "total": len(found),
        "page": page,
        "pageSize": page_size,
        "includeDone": args.include_done,
        "recordingsScanned": len(recent),
        "items": found[start:end],
    }


def health(client: Client, _args: argparse.Namespace) -> dict[str, Any]:
    response = client.post(
        "/api/audiofileMstr/audiofileseleUserAllList",
        {"page": 1, "pageSize": 1, "orderField": "createTime", "order": "descending"},
        operation="health check",
    )
    result = result_value(response)
    return {
        "ok": True,
        "operation": "health",
        "apiBase": client.api_base,
        "authenticated": True,
        "recordingsAccessible": isinstance(result, (dict, list)),
        "recordingTotal": result.get("total") if isinstance(result, dict) else None,
    }


def user_info(client: Client, _args: argparse.Namespace) -> dict[str, Any]:
    response = client.post(
        "/api/audiofileMstr/getUserInfo",
        None,
        operation="get user info",
    )
    result = result_value(response)
    if result is not None:
        return {"ok": True, "operation": "user-info", "result": result}
    fallback = health(client, _args)
    return {
        "ok": True,
        "operation": "user-info",
        "result": {
            "authenticated": True,
            "userInfoAvailable": False,
            "recordingsAccessible": fallback["recordingsAccessible"],
            "recordingTotal": fallback["recordingTotal"],
        },
    }


def knowledge_bases(client: Client, _args: argparse.Namespace) -> dict[str, Any]:
    response = client.post(
        "/api/userfolderMstr/AllList",
        {},
        operation="list knowledge bases",
    )
    return {
        "ok": True,
        "operation": "knowledge-bases",
        "result": result_value(response),
    }


def knowledge_files(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": args.knowledge_base_id,
        "name": args.keyword or "",
        "type": "kb",
        "fileld": "",
        "fileType": "",
        "filePath": "",
        "permission": True,
    }
    if args.folder_id:
        body["folderId"] = args.folder_id
    response = client.post(
        "/api/userfolderMstr/FolderList",
        body,
        operation="list knowledge files",
    )
    return {
        "ok": True,
        "operation": "knowledge-files",
        "knowledgeBaseId": args.knowledge_base_id,
        "result": result_value(response),
    }


def knowledge_recordings(client: Client, args: argparse.Namespace) -> dict[str, Any]:
    queue = [0]
    visited: set[int] = set()
    recordings_found: list[dict[str, Any]] = []

    while queue:
        folder_id = queue.pop(0)
        if folder_id in visited:
            continue
        visited.add(folder_id)
        body: dict[str, Any] = {
            "id": args.knowledge_base_id,
            "name": "",
            "type": "kb" if folder_id == 0 else "folder",
            "fileld": "",
            "fileType": "",
            "filePath": "",
            "permission": True,
        }
        if folder_id:
            body["folderId"] = folder_id
        response = client.post(
            "/api/userfolderMstr/FolderList",
            body,
            operation="list knowledge recordings",
        )
        for item in result_items(result_value(response)):
            if not isinstance(item, dict):
                continue
            item_type = first_nonempty(first_value(item, "type", "Type")).lower()
            if item_type == "folder":
                child_id = first_value(item, "folderId", "FolderId")
                try:
                    parsed_id = int(child_id)
                except (TypeError, ValueError):
                    continue
                if parsed_id and parsed_id not in visited:
                    queue.append(parsed_id)
                continue
            if item_type != "file" or str(first_value(item, "fileAttribute", "FileAttribute")) != "3":
                continue
            title = first_value(
                item,
                "name",
                "Name",
                "kbfileTitle",
                "KbfileTitle",
                "fileName",
                "FileName",
            )
            if args.keyword and args.keyword.lower() not in str(title or "").lower():
                continue
            recordings_found.append(
                {
                    "fileId": first_value(item, "fileId", "FileId"),
                    "title": title,
                    "fileName": first_value(item, "fileName", "FileName"),
                    "folderId": first_value(item, "folderId", "FolderId"),
                    "knowledgeBaseId": args.knowledge_base_id,
                    "contentType": first_value(item, "contentType", "ContentType"),
                    "uploadTime": first_value(item, "uploadTime", "UploadTime"),
                    "updateTime": first_value(item, "updatetime", "Updatetime"),
                }
            )

    return {
        "ok": True,
        "operation": "knowledge-recordings",
        "knowledgeBaseId": args.knowledge_base_id,
        "total": len(recordings_found),
        "items": recordings_found,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query AideNote from Hermes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Verify authentication and data access")
    subparsers.add_parser("user-info", help="Read current account information")

    recordings_parser = subparsers.add_parser("recordings", help="List recent recordings")
    recordings_parser.add_argument("--page", type=int, default=1)
    recordings_parser.add_argument("--page-size", type=int, default=10)
    recordings_parser.add_argument("--keyword", default="")

    shared_parser = subparsers.add_parser(
        "shared-recordings", help="List recordings shared with the current account"
    )
    shared_parser.add_argument("--page", type=int, default=1)
    shared_parser.add_argument("--page-size", type=int, default=10)
    shared_parser.add_argument("--keyword", default="")

    detail_parser = subparsers.add_parser("recording-detail", help="Read one recording detail")
    detail_parser.add_argument("--file-id", required=True)

    todos_parser = subparsers.add_parser("todos", help="List todos extracted from recordings")
    todos_parser.add_argument("--recording-page-size", type=int, default=20)
    todos_parser.add_argument("--page", type=int, default=1)
    todos_parser.add_argument("--page-size", type=int, default=50)
    todos_parser.add_argument("--include-done", action="store_true")
    todos_parser.add_argument("--include-deleted", action="store_true")

    subparsers.add_parser("knowledge-bases", help="List knowledge bases")
    knowledge_parser = subparsers.add_parser("knowledge-files", help="List knowledge files")
    knowledge_parser.add_argument("--knowledge-base-id", type=int, required=True)
    knowledge_parser.add_argument("--folder-id", type=int)
    knowledge_parser.add_argument("--keyword", default="")
    knowledge_recordings_parser = subparsers.add_parser(
        "knowledge-recordings", help="Recursively list recordings in a knowledge base"
    )
    knowledge_recordings_parser.add_argument("--knowledge-base-id", type=int, required=True)
    knowledge_recordings_parser.add_argument("--keyword", default="")
    return parser


HANDLERS = {
    "health": health,
    "user-info": user_info,
    "recordings": recordings,
    "shared-recordings": shared_recordings,
    "recording-detail": recording_detail,
    "todos": todos,
    "knowledge-bases": knowledge_bases,
    "knowledge-files": knowledge_files,
    "knowledge-recordings": knowledge_recordings,
}


def main() -> int:
    args = build_parser().parse_args()
    try:
        client = Client.from_credentials()
        emit(HANDLERS[args.command](client, args))
        return 0
    except AideNoteError as exc:
        emit(
            {
                "ok": False,
                "error": exc.code,
                "operation": exc.operation or args.command,
                "message": exc.message,
            },
            stream=sys.stderr,
        )
        return 2
    except Exception:
        emit(
            {
                "ok": False,
                "error": "unexpected_error",
                "operation": args.command,
                "message": "Unexpected AideNote client failure",
            },
            stream=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
