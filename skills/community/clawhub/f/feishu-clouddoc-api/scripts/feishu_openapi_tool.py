#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


DOC_BLOCK_TYPE_TEXT = 2
TEXT_COLOR_RED = 4
TOKEN_EXPIRED_CODES = {99991668, 99991677}
FEISHU_HOST = "open.feishu.cn"
FEISHU_DNS_FALLBACK_IPV4 = (
    "101.89.125.72",
    "117.24.169.93",
    "106.227.20.100",
)


class FeishuError(RuntimeError):
    pass


def install_feishu_dns_fallback() -> None:
    if getattr(socket, "_openclaw_feishu_dns_fallback", False):
        return

    original_getaddrinfo = socket.getaddrinfo

    def patched_getaddrinfo(
        host: str | bytes | None,
        port: str | int | None,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> list[Any]:
        hostname = host.decode("utf-8", errors="ignore") if isinstance(host, bytes) else host
        if str(hostname or "").lower() != FEISHU_HOST:
            return original_getaddrinfo(host, port, family, type, proto, flags)

        try:
            return original_getaddrinfo(host, port, family, type, proto, flags)
        except socket.gaierror:
            pass

        if family == socket.AF_INET6:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known")

        results: list[Any] = []
        for ip in FEISHU_DNS_FALLBACK_IPV4:
            results.extend(original_getaddrinfo(ip, port, socket.AF_INET, type, proto, flags))
        return results

    socket.getaddrinfo = patched_getaddrinfo
    socket._openclaw_feishu_dns_fallback = True


install_feishu_dns_fallback()


def read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def write_env_values(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    remaining = dict(values)
    out: list[str] = []
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            out.append(line)
            continue
        key = line.split("=", 1)[0].strip()
        if key in remaining:
            out.append(f"{key}={remaining.pop(key)}")
        else:
            out.append(line)
    for key, value in remaining.items():
        out.append(f"{key}={value}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def shared_user_token_file(env: dict[str, str]) -> Path | None:
    app_id = env.get("FEISHU_APP_ID", "").strip()
    if not app_id:
        return None
    custom = env.get("FEISHU_USER_TOKEN_FILE", "").strip()
    if custom:
        return Path(custom).expanduser()
    slot = hashlib.sha256(app_id.encode("utf-8")).hexdigest()[:16]
    return Path.home() / ".openclaw" / "feishu-user-tokens" / f"{slot}.env"


def load_or_seed_shared_user_tokens(env: dict[str, str], env_path: Path | None) -> None:
    token_path = shared_user_token_file(env)
    if not token_path:
        return
    if token_path.exists():
        token_env = read_env_file(token_path)
        for key, value in token_env.items():
            if key.startswith("FEISHU_USER_"):
                env[key] = value
        env["FEISHU_USER_TOKEN_FILE"] = str(token_path)
        return
    if not env_path or not env_path.exists():
        return
    current = read_env_file(env_path)
    wanted = {
        key: current.get(key, "")
        for key in [
            "FEISHU_USER_ACCESS_TOKEN",
            "FEISHU_USER_REFRESH_TOKEN",
            "FEISHU_USER_OPEN_ID",
            "FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT",
            "FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT",
        ]
        if current.get(key, "")
    }
    if wanted.get("FEISHU_USER_ACCESS_TOKEN") or wanted.get("FEISHU_USER_REFRESH_TOKEN"):
        write_env_values(token_path, wanted)
        env["FEISHU_USER_TOKEN_FILE"] = str(token_path)


def load_env(path: str | None) -> dict[str, str]:
    env = dict(os.environ)
    if not path:
        load_or_seed_shared_user_tokens(env, None)
        return env
    env_path = Path(path)
    if not env_path.exists():
        load_or_seed_shared_user_tokens(env, env_path)
        return env
    for key, value in read_env_file(env_path).items():
        if key and key not in env:
            env[key] = value
    load_or_seed_shared_user_tokens(env, env_path)
    return env


def redact_status(env: dict[str, str]) -> dict[str, Any]:
    keys = [
        "FEISHU_APP_ID",
        "FEISHU_APP_SECRET",
        "FEISHU_BASE_URL",
        "FEISHU_USER_ACCESS_TOKEN",
        "FEISHU_USER_REFRESH_TOKEN",
        "FEISHU_USER_OPEN_ID",
        "FEISHU_DEFAULT_FOLDER_TOKEN",
    ]
    return {key: bool(env.get(key, "").strip()) for key in keys}


def base_url(env: dict[str, str]) -> str:
    return env.get("FEISHU_BASE_URL", "https://open.feishu.cn").rstrip("/")


def require_env(env: dict[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise FeishuError(f"Missing {name}")
    return value


def token_from_input(value: str) -> str:
    value = value.strip()
    if not value:
        raise FeishuError("Missing Feishu URL or token")
    patterns = [
        r"/docx/([A-Za-z0-9_-]+)",
        r"/doc/([A-Za-z0-9_-]+)",
        r"/wiki/([A-Za-z0-9_-]+)",
        r"/sheets/([A-Za-z0-9_-]+)",
        r"/base/([A-Za-z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return value.split("?")[0].rstrip("/").split("/")[-1]


def http_json(
    env: dict[str, str],
    method: str,
    path: str,
    *,
    bearer: str | None = None,
    body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    retry_user_token: bool = True,
) -> dict[str, Any]:
    query = ""
    if params:
        clean_params = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean_params:
            query = "?" + urllib.parse.urlencode(clean_params)
    url = base_url(env) + path + query
    data = None
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise FeishuError(f"HTTP {exc.code} {method} {path}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise FeishuError(f"Network error for {method} {path}: {exc}") from exc

    try:
        payload = json.loads(text) if text else {}
    except json.JSONDecodeError as exc:
        raise FeishuError(f"Invalid JSON response from {method} {path}: {text[:200]}") from exc

    code = payload.get("code", 0)
    if code not in (0, None):
        if (
            retry_user_token
            and code in TOKEN_EXPIRED_CODES
            and bearer
            and bearer == env.get("FEISHU_USER_ACCESS_TOKEN", "").strip()
            and env.get("FEISHU_USER_REFRESH_TOKEN", "").strip()
        ):
            return http_json(
                env,
                method,
                path,
                bearer=refresh_user_access_token(env),
                body=body,
                params=params,
                retry_user_token=False,
            )
        msg = payload.get("msg") or payload.get("message") or "Feishu API error"
        raise FeishuError(f"{method} {path} failed: code={code} msg={msg}")
    return payload


def tenant_access_token(env: dict[str, str]) -> str:
    payload = http_json(
        env,
        "POST",
        "/open-apis/auth/v3/tenant_access_token/internal",
        body={
            "app_id": require_env(env, "FEISHU_APP_ID"),
            "app_secret": require_env(env, "FEISHU_APP_SECRET"),
        },
    )
    token = payload.get("tenant_access_token", "")
    if not token:
        raise FeishuError("Feishu did not return tenant_access_token")
    return token


def refresh_user_access_token(env: dict[str, str]) -> str:
    refresh_token = require_env(env, "FEISHU_USER_REFRESH_TOKEN")
    try:
        data = refresh_user_access_token_with_sdk(env, refresh_token)
    except ImportError:
        tenant_token = tenant_access_token(env)
        payload = http_json(
            env,
            "POST",
            "/open-apis/authen/v1/oidc/refresh_access_token",
            bearer=tenant_token,
            body={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            retry_user_token=False,
        )
        data = payload.get("data") or {}
    access_token = data.get("access_token", "")
    next_refresh_token = data.get("refresh_token", "")
    if not access_token or not next_refresh_token:
        raise FeishuError("Feishu refresh response did not include user tokens")

    now = int(time.time())
    wanted = {
        "FEISHU_USER_ACCESS_TOKEN": access_token,
        "FEISHU_USER_REFRESH_TOKEN": next_refresh_token,
        "FEISHU_USER_OPEN_ID": env.get("FEISHU_USER_OPEN_ID", ""),
        "FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT": str(now + int(data.get("expires_in") or 0)),
        "FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT": str(
            now + int(data.get("refresh_token_expires_in") or data.get("refresh_expires_in") or 0)
        ),
    }
    token_path = shared_user_token_file(env)
    if token_path:
        write_env_values(token_path, wanted)
        env["FEISHU_USER_TOKEN_FILE"] = str(token_path)
    env.update(wanted)
    return access_token


def refresh_user_access_token_with_sdk(env: dict[str, str], refresh_token: str) -> dict[str, Any]:
    import lark_oapi as lark
    from lark_oapi.api.authen.v1 import (
        CreateRefreshAccessTokenRequest,
        CreateRefreshAccessTokenRequestBody,
    )

    builder = (
        lark.Client.builder()
        .app_id(require_env(env, "FEISHU_APP_ID"))
        .app_secret(require_env(env, "FEISHU_APP_SECRET"))
    )
    if base_url(env) != "https://open.feishu.cn":
        builder = builder.domain(base_url(env))
    client = builder.build()
    request = CreateRefreshAccessTokenRequest.builder().request_body(
        CreateRefreshAccessTokenRequestBody.builder()
        .grant_type("refresh_token")
        .refresh_token(refresh_token)
        .build()
    ).build()
    response = client.authen.v1.refresh_access_token.create(request)
    if not getattr(response, "success", lambda: False)():
        raise FeishuError(
            f"refresh_user_access_token failed: code={getattr(response, 'code', None)} msg={getattr(response, 'msg', None)}"
        )
    data = response.data
    return {
        "access_token": getattr(data, "access_token", "") or "",
        "refresh_token": getattr(data, "refresh_token", "") or "",
        "expires_in": getattr(data, "expires_in", 0) or 0,
        "refresh_token_expires_in": (
            getattr(data, "refresh_token_expires_in", 0)
            or getattr(data, "refresh_expires_in", 0)
            or 0
        ),
        "open_id": getattr(data, "open_id", "") or "",
    }


def needs_preemptive_refresh(env: dict[str, str], *, skew_seconds: int = 300) -> bool:
    expires = env.get("FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT", "").strip()
    if not expires:
        return False
    try:
        return int(expires) <= int(time.time()) + skew_seconds
    except ValueError:
        return False


def bearer_token(env: dict[str, str], *, prefer_user: bool = False) -> tuple[str, str]:
    user_token = env.get("FEISHU_USER_ACCESS_TOKEN", "").strip()
    if prefer_user:
        if env.get("FEISHU_USER_REFRESH_TOKEN", "").strip() and (
            not user_token or needs_preemptive_refresh(env)
        ):
            user_token = refresh_user_access_token(env)
        if not user_token:
            raise FeishuError("Missing FEISHU_USER_ACCESS_TOKEN for user-token operation")
        return user_token, "user"
    return tenant_access_token(env), "tenant"


def text_block(text: str, *, red: bool = False) -> dict[str, Any]:
    text_run: dict[str, Any] = {"content": text}
    if red:
        text_run["text_element_style"] = {"text_color": TEXT_COLOR_RED}
    return {
        "block_type": DOC_BLOCK_TYPE_TEXT,
        "text": {
            "elements": [
                {
                    "text_run": text_run,
                }
            ]
        },
    }


def extract_text_from_block(block: dict[str, Any]) -> str:
    text_fields = [
        "page",
        "text",
        "heading1",
        "heading2",
        "heading3",
        "heading4",
        "heading5",
        "heading6",
        "heading7",
        "heading8",
        "heading9",
        "bullet",
        "ordered",
        "code",
        "quote",
        "equation",
        "todo",
    ]
    for field in text_fields:
        data = block.get(field)
        if not isinstance(data, dict):
            continue
        parts: list[str] = []
        for element in data.get("elements") or []:
            run = (element or {}).get("text_run") or {}
            content = run.get("content")
            if content:
                parts.append(str(content))
        if parts:
            return "".join(parts)
    return ""


def summarize_block(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "block_id": block.get("block_id"),
        "parent_id": block.get("parent_id"),
        "block_type": block.get("block_type"),
        "text": extract_text_from_block(block),
        "children": block.get("children") or [],
    }


def list_blocks(env: dict[str, str], document_id: str, *, token: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    page_token = ""
    while True:
        params: dict[str, Any] = {"page_size": 200}
        if page_token:
            params["page_token"] = page_token
        payload = http_json(
            env,
            "GET",
            f"/open-apis/docx/v1/documents/{document_id}/blocks",
            bearer=token,
            params=params,
        )
        data = payload.get("data") or {}
        blocks.extend(data.get("items") or [])
        if not data.get("has_more"):
            break
        page_token = data.get("page_token", "")
        if not page_token:
            break
    return blocks


def command_env_check(args: argparse.Namespace) -> dict[str, Any]:
    env = load_env(args.env_file)
    status = redact_status(env)
    return {
        "ok": bool(status["FEISHU_APP_ID"] and status["FEISHU_APP_SECRET"]),
        "env_file": args.env_file,
        "present": status,
        "note": "Secret values are intentionally not printed.",
    }


def command_resolve(args: argparse.Namespace) -> dict[str, Any]:
    return {"input": args.input, "token": token_from_input(args.input)}


def command_read_doc(args: argparse.Namespace) -> dict[str, Any]:
    env = load_env(args.env_file)
    document_id = token_from_input(args.doc)
    token, mode = bearer_token(env, prefer_user=args.user_token)
    meta = http_json(env, "GET", f"/open-apis/docx/v1/documents/{document_id}", bearer=token)
    raw = http_json(env, "GET", f"/open-apis/docx/v1/documents/{document_id}/raw_content", bearer=token)
    blocks = list_blocks(env, document_id, token=token) if args.blocks else []
    return {
        "auth_mode": mode,
        "document_id": document_id,
        "document": (meta.get("data") or {}).get("document") or meta.get("data"),
        "raw_content": (raw.get("data") or {}).get("content"),
        "blocks": [summarize_block(block) for block in blocks],
        "block_count": len(blocks),
    }


def command_list_blocks(args: argparse.Namespace) -> dict[str, Any]:
    env = load_env(args.env_file)
    document_id = token_from_input(args.doc)
    token, mode = bearer_token(env, prefer_user=args.user_token)
    blocks = list_blocks(env, document_id, token=token)
    return {
        "auth_mode": mode,
        "document_id": document_id,
        "blocks": [summarize_block(block) for block in blocks],
        "block_count": len(blocks),
    }


def command_create_doc(args: argparse.Namespace) -> dict[str, Any]:
    env = load_env(args.env_file)
    prefer_user = not args.allow_app_owned
    token, mode = bearer_token(env, prefer_user=prefer_user)
    folder_token = args.folder_token or env.get("FEISHU_DEFAULT_FOLDER_TOKEN", "")
    body = {"title": args.title}
    if folder_token:
        body["folder_token"] = folder_token
    payload = http_json(env, "POST", "/open-apis/docx/v1/documents", bearer=token, body=body)
    document = (payload.get("data") or {}).get("document") or payload.get("data") or {}
    document_id = document.get("document_id")
    if args.append_text and document_id:
        append_args = argparse.Namespace(
            env_file=args.env_file,
            doc=document_id,
            text=args.append_text,
            red=False,
            user_token=(mode == "user"),
            parent_block_id="",
            index=None,
        )
        appended = command_append_text(append_args)
    else:
        appended = None
    return {
        "auth_mode": mode,
        "ownership_note": "user token used" if mode == "user" else "app-owned creation explicitly allowed",
        "document": document,
        "url": f"https://feishu.cn/docx/{document_id}" if document_id else None,
        "append_result": appended,
    }


def command_append_text(args: argparse.Namespace) -> dict[str, Any]:
    env = load_env(args.env_file)
    document_id = token_from_input(args.doc)
    token, mode = bearer_token(env, prefer_user=args.user_token)
    parent_block_id = args.parent_block_id or document_id
    params = {
        "document_revision_id": -1,
        "client_token": str(uuid.uuid4()),
    }
    body: dict[str, Any] = {"children": [text_block(args.text, red=args.red)]}
    if args.index is not None:
        body["index"] = args.index
    payload = http_json(
        env,
        "POST",
        f"/open-apis/docx/v1/documents/{document_id}/blocks/{parent_block_id}/children",
        bearer=token,
        body=body,
        params=params,
    )
    children = ((payload.get("data") or {}).get("children")) or []
    return {
        "auth_mode": mode,
        "document_id": document_id,
        "parent_block_id": parent_block_id,
        "block_ids": [child.get("block_id") for child in children if child.get("block_id")],
        "raw_data": payload.get("data"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portable Feishu OpenAPI helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_env(p: argparse.ArgumentParser) -> None:
        p.add_argument("--env-file", default=".env", help="Path to .env file")

    p = subparsers.add_parser("env-check", help="Validate environment without printing secrets")
    add_env(p)
    p.set_defaults(func=command_env_check)

    p = subparsers.add_parser("resolve", help="Extract token from a Feishu URL or raw token")
    p.add_argument("--input", required=True)
    p.set_defaults(func=command_resolve)

    p = subparsers.add_parser("read-doc", help="Read a Feishu Docx document")
    add_env(p)
    p.add_argument("--doc", required=True, help="Docx URL or document_id")
    p.add_argument("--blocks", action="store_true", help="Include block summaries")
    p.add_argument("--user-token", action="store_true", help="Use FEISHU_USER_ACCESS_TOKEN")
    p.set_defaults(func=command_read_doc)

    p = subparsers.add_parser("list-blocks", help="List document block summaries")
    add_env(p)
    p.add_argument("--doc", required=True, help="Docx URL or document_id")
    p.add_argument("--user-token", action="store_true", help="Use FEISHU_USER_ACCESS_TOKEN")
    p.set_defaults(func=command_list_blocks)

    p = subparsers.add_parser("create-doc", help="Create a Feishu Docx document")
    add_env(p)
    p.add_argument("--title", required=True)
    p.add_argument("--folder-token", default="", help="Target folder token")
    p.add_argument("--append-text", default="", help="Optional initial text")
    p.add_argument("--allow-app-owned", action="store_true", help="Allow tenant/app-token creation")
    p.set_defaults(func=command_create_doc)

    p = subparsers.add_parser("append-text", help="Append text to a Feishu Docx document")
    add_env(p)
    p.add_argument("--doc", required=True, help="Docx URL or document_id")
    p.add_argument("--text", required=True)
    p.add_argument("--red", action="store_true")
    p.add_argument("--user-token", action="store_true", help="Use FEISHU_USER_ACCESS_TOKEN")
    p.add_argument("--parent-block-id", default="", help="Defaults to root document block")
    p.add_argument("--index", type=int, default=None)
    p.set_defaults(func=command_append_text)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except FeishuError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
