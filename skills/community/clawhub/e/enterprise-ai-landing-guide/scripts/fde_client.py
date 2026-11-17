#!/usr/bin/env python3
"""Zero-dependency client for the Enterprise AI Landing Guide public API."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class ApiError(RuntimeError):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(f"HTTP {status} {code}: {message}")
        self.status = status
        self.code = code
        self.message = message


class LandingGuideClient:
    def __init__(self, base_url: str, timeout: float = 35.0):
        self.base_url = base_url.rstrip("/")
        self.prefix = "/api/public/clawhive/v1"
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | bytes | None = None,
        token: str | None = None,
        idempotency_key: str | None = None,
        content_type: str = "application/json",
    ) -> dict[str, Any]:
        url = f"{self.base_url}{self.prefix}{path}"
        headers = {"Accept": "application/json", "User-Agent": "enterprise-ai-landing-guide-skill/1.2.0"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data: bytes | None = None
        if isinstance(body, bytes):
            data = body
            headers["Content-Type"] = content_type
        elif body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return self._json(response.read())
        except urllib.error.HTTPError as error:
            payload = self._json(error.read(), allow_empty=True)
            raise ApiError(error.code, str(payload.get("code", "EXT-HTTP")), str(payload.get("message", "请求失败"))) from None
        except urllib.error.URLError as error:
            raise ApiError(0, "EXT-NETWORK", f"服务不可达: {error.reason}") from None

    @staticmethod
    def _json(raw: bytes, allow_empty: bool = False) -> dict[str, Any]:
        if not raw and allow_empty:
            return {}
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            if allow_empty:
                return {}
            raise ApiError(0, "EXT-INVALID-RESPONSE", "服务返回了无法解析的响应") from None
        if not isinstance(value, dict):
            raise ApiError(0, "EXT-INVALID-RESPONSE", "服务响应不是JSON对象")
        return value

    def health(self) -> dict[str, Any]:
        return self.request("GET", "/health")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/sessions", body=payload)

    def message(self, session_id: str, token: str, text: str, mode: str | None, key: str) -> dict[str, Any]:
        payload: dict[str, Any] = {"message": text}
        if mode:
            payload["mode"] = mode
        return self.request("POST", f"/sessions/{session_id}/messages", body=payload, token=token, idempotency_key=key)

    def upload(self, session_id: str, token: str, filename: str, key: str) -> dict[str, Any]:
        path = Path(filename)
        content = path.read_bytes()
        if len(content) > 10 * 1024 * 1024:
            raise ApiError(0, "EXT-FILE-SIZE", "文件超过10MB客户端上限")
        boundary = f"----elag-{secrets.token_hex(16)}"
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        safe_name = path.name.replace('"', "")
        parts = [
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'.encode(),
            f"Content-Type: {mime}\r\n\r\n".encode(),
            content,
            f"\r\n--{boundary}--\r\n".encode(),
        ]
        return self.request(
            "POST",
            f"/sessions/{session_id}/attachments",
            body=b"".join(parts),
            token=token,
            idempotency_key=key,
            content_type=f"multipart/form-data; boundary={boundary}",
        )

    def generate(self, session_id: str, token: str, key: str) -> dict[str, Any]:
        return self.request("POST", f"/sessions/{session_id}/generate-map", body={}, token=token, idempotency_key=key)

    def get_map(self, session_id: str, token: str) -> dict[str, Any]:
        return self.request("GET", f"/sessions/{session_id}/map", token=token)

    def consent(self, session_id: str, token: str, payload: dict[str, Any], key: str) -> dict[str, Any]:
        return self.request("POST", f"/sessions/{session_id}/consent", body=payload, token=token, idempotency_key=key)

    def convert(self, session_id: str, token: str, key: str) -> dict[str, Any]:
        return self.request("POST", f"/sessions/{session_id}/convert", body={}, token=token, idempotency_key=key)

    def delete(self, session_id: str, token: str) -> dict[str, Any]:
        return self.request("DELETE", f"/sessions/{session_id}", token=token)


def token_from_environment() -> str:
    token = os.environ.get("ENTERPRISE_AI_LANDING_SESSION_TOKEN", "").strip()
    if not token:
        raise ApiError(0, "EXT-TOKEN-MISSING", "请在当前进程上下文设置ENTERPRISE_AI_LANDING_SESSION_TOKEN")
    return token


def idempotency(value: str | None) -> str:
    return value or f"skill-{secrets.token_hex(16)}"


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Enterprise AI Landing Guide API client")
    root.add_argument("--base-url", default=os.environ.get("ENTERPRISE_AI_LANDING_API_BASE", "https://fde.lantuzhigou.com"))
    root.add_argument("--timeout", type=float, default=35.0)
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("health")

    create = commands.add_parser("create")
    create.add_argument("--platform", required=True)
    create.add_argument("--version", default="1.2.0")
    create.add_argument("--external-session-id", required=True)
    create.add_argument("--mode", choices=["KNOWN_PROBLEM", "OPPORTUNITY_SCAN"])
    create.add_argument("--campaign")
    create.add_argument("--referrer")
    create.add_argument("--entry-url")

    for name in ("message", "upload", "generate", "map", "consent", "convert", "delete"):
        command = commands.add_parser(name)
        command.add_argument("--session-id", required=True)
        if name in {"message", "upload", "generate", "consent", "convert"}:
            command.add_argument("--idempotency-key")
        if name == "message":
            command.add_argument("--text", required=True)
            command.add_argument("--mode", choices=["KNOWN_PROBLEM", "OPPORTUNITY_SCAN"])
        elif name == "upload":
            command.add_argument("--file", required=True)
        elif name == "consent":
            command.add_argument("--store", action="store_true")
            command.add_argument("--contact", action="store_true")
            command.add_argument("--company")
            command.add_argument("--contact-name")
            command.add_argument("--mobile")
            command.add_argument("--email")
    return root


def run(args: argparse.Namespace) -> dict[str, Any]:
    client = LandingGuideClient(args.base_url, args.timeout)
    if args.command == "health":
        return client.health()
    if args.command == "create":
        payload = {
            "sourcePlatform": args.platform,
            "sourceVersion": args.version,
            "externalSessionId": args.external_session_id,
        }
        for key, value in (("mode", args.mode), ("campaignCode", args.campaign), ("referrer", args.referrer), ("entryUrl", args.entry_url)):
            if value:
                payload[key] = value
        return client.create(payload)

    token = token_from_environment()
    if args.command == "message":
        return client.message(args.session_id, token, args.text, args.mode, idempotency(args.idempotency_key))
    if args.command == "upload":
        return client.upload(args.session_id, token, args.file, idempotency(args.idempotency_key))
    if args.command == "generate":
        return client.generate(args.session_id, token, idempotency(args.idempotency_key))
    if args.command == "map":
        return client.get_map(args.session_id, token)
    if args.command == "consent":
        payload = {
            "consentToStore": args.store,
            "consentToContact": args.contact,
            "companyName": args.company or "",
            "contactName": args.contact_name or "",
            "mobile": args.mobile or "",
            "email": args.email or "",
        }
        return client.consent(args.session_id, token, payload, idempotency(args.idempotency_key))
    if args.command == "convert":
        return client.convert(args.session_id, token, idempotency(args.idempotency_key))
    if args.command == "delete":
        return client.delete(args.session_id, token)
    raise ApiError(0, "EXT-CLI", "未支持的命令")


def main() -> int:
    try:
        result = run(parser().parse_args())
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (ApiError, OSError) as error:
        sys.stderr.write(f"{error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
