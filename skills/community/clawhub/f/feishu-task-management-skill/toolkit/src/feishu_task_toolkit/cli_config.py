from __future__ import annotations

import argparse
import getpass
import json
import secrets
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from .config import AppConfig, AppConfigError, ToolkitPaths, expires_at_from_now, load_json, write_json
from .http import ApiError, FeishuHttpClient
from .members import sync_members

DEFAULT_REDIRECT_URI = "https://example.com/feishu/oauth/callback"


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="feishu_config")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("guide")
    subparsers.add_parser("show")
    subparsers.add_parser("validate")

    set_parser = subparsers.add_parser("set")
    set_parser.add_argument("--app-id", required=True)
    set_parser.add_argument("--app-secret", required=True)
    set_parser.add_argument("--user-access-token", default=None)
    set_parser.add_argument("--refresh-token", default=None)
    set_parser.add_argument("--user-token-expires-at", default=None)
    set_parser.add_argument("--user-scope", default=None)
    set_parser.add_argument("--base-url", default="https://open.feishu.cn/open-apis")
    set_parser.add_argument("--timezone", default="Asia/Shanghai")
    set_parser.add_argument("--default-member-open-id", default=None)

    clear_parser = subparsers.add_parser("clear")
    clear_parser.add_argument("--yes", action="store_true")
    return parser


def _is_yes(value: str, default: bool = False) -> bool:
    normalized = value.strip().lower()
    if not normalized:
        return default
    return normalized in {"y", "yes"}


def _run_member_sync(paths: ToolkitPaths) -> dict[str, Any]:
    client = FeishuHttpClient(AppConfig.load(paths))
    result = sync_members(client, paths)
    return result["sync_meta"]


def build_authorize_url(client_id: str, redirect_uri: str, scope: str, state: str) -> str:
    query = urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
    )
    return f"https://accounts.feishu.cn/open-apis/authen/v1/authorize?{query}"


def parse_oauth_callback_input(raw: str, expected_state: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if "://" not in value:
        raise ValueError("OAuth callback input must be the full callback URL")
    parsed = urlparse(value)
    query = parse_qs(parsed.query)
    code = (query.get("code") or [""])[0]
    state = (query.get("state") or [""])[0]
    if expected_state and state and state != expected_state:
        raise ValueError("OAuth callback state mismatch")
    if not code:
        raise ValueError("OAuth callback does not contain code")
    return code


def _default_state() -> str:
    return secrets.token_urlsafe(16)


def _exchange_authorization_code(
    app_id: str,
    app_secret: str,
    code: str,
    redirect_uri: str,
    code_verifier: str,
) -> dict[str, Any]:
    client = FeishuHttpClient(AppConfig(app_id=app_id, app_secret=app_secret))
    payload = client.exchange_authorization_code(
        code=code,
        redirect_uri=redirect_uri or None,
        code_verifier=code_verifier or None,
    )
    result = {
        "access_token": payload.get("access_token", ""),
        "refresh_token": payload.get("refresh_token", ""),
        "expires_in": payload.get("expires_in", 0),
        "refresh_token_expires_in": payload.get("refresh_token_expires_in", 0),
        "scope": payload.get("scope", ""),
    }
    if result["expires_in"]:
        result["user_token_expires_at"] = expires_at_from_now(int(result["expires_in"]))
    else:
        result["user_token_expires_at"] = ""
    return result


def run_guide(
    paths: ToolkitPaths,
    input_fn=input,
    secret_input_fn=getpass.getpass,
    print_fn=print,
    exchange_code_fn=_exchange_authorization_code,
    state_fn=_default_state,
    sync_fn=_run_member_sync,
) -> int:
    paths.ensure()
    try:
        print_fn("飞书任务工具配置向导")
        print_fn("")

        if paths.runtime_config_file.exists():
            overwrite = input_fn(f"检测到现有配置文件 {paths.runtime_config_file}，将被覆盖，是否继续? [y/N]: ")
            if not _is_yes(overwrite, default=False):
                print_fn("已取消写入。")
                return 1
            print_fn("")

        app_id = ""
        app_secret = ""
        while not app_id:
            app_id = input_fn("请输入 App ID: ").strip()
        while not app_secret:
            app_secret = secret_input_fn("请输入 App Secret: ").strip()
        enable_user_oauth = input_fn("是否继续配置用户 OAuth 授权? [Y/n]: ")
        redirect_uri = DEFAULT_REDIRECT_URI
        user_access_token = ""
        refresh_token = ""
        user_token_expires_at = ""
        user_scope = ""
        if _is_yes(enable_user_oauth, default=True):
            scope = (
                input_fn(
                    "请输入 scope（直接回车使用默认值 task:task:read task:task:write）: "
                ).strip()
                or "task:task:read task:task:write"
            )
            state = state_fn()
            authorize_url = build_authorize_url(
                client_id=app_id,
                redirect_uri=redirect_uri,
                scope=scope,
                state=state,
            )
            print_fn(f"默认 redirect_uri: {redirect_uri}")
            print_fn("请先在飞书开发者后台把这个 redirect_uri 配置到应用安全设置中。")
            print_fn("请在浏览器中打开下面的授权链接，完成授权后把完整回调 URL 粘贴回来。")
            print_fn(f"授权链接: {authorize_url}")
            callback_input = input_fn("请输入完整回调 URL（直接回车跳过）: ").strip()
            authorization_code = parse_oauth_callback_input(callback_input, expected_state=state) if callback_input else ""
        else:
            authorization_code = ""
            scope = ""
            state = ""
        if authorization_code:
            token_payload = exchange_code_fn(app_id, app_secret, authorization_code, redirect_uri, "")
            user_access_token = token_payload.get("access_token", "")
            refresh_token = token_payload.get("refresh_token", "")
            user_token_expires_at = token_payload.get("user_token_expires_at", "")
            if not user_token_expires_at and token_payload.get("expires_in"):
                user_token_expires_at = expires_at_from_now(int(token_payload["expires_in"]))
            user_scope = token_payload.get("scope", "") or scope
        default_member_open_id = input_fn("请输入默认加入任务的用户 Open ID（直接回车跳过）: ").strip()

        payload = {
            "app_id": app_id,
            "app_secret": app_secret,
            "user_access_token": user_access_token,
            "refresh_token": refresh_token,
            "user_token_expires_at": user_token_expires_at,
            "user_scope": user_scope,
            "base_url": "https://open.feishu.cn/open-apis",
            "timezone": "Asia/Shanghai",
            "default_member_open_id": default_member_open_id,
        }

        print_fn("")
        print_fn(f"将写入: {paths.runtime_config_file}")
        print_fn("配置预览:")
        print_fn(f"- app_id: {payload['app_id']}")
        print_fn(f"- app_secret: {AppConfig(**payload).to_public_dict()['app_secret']}")
        print_fn(f"- user_access_token: {AppConfig(**payload).to_public_dict()['user_access_token']}")
        print_fn(f"- refresh_token: {AppConfig(**payload).to_public_dict()['refresh_token']}")
        print_fn(f"- user_token_expires_at: {payload['user_token_expires_at'] or '(未设置)'}")
        print_fn(f"- user_scope: {payload['user_scope'] or '(未设置)'}")
        print_fn(f"- base_url: {payload['base_url']}")
        print_fn(f"- timezone: {payload['timezone']}")
        print_fn(f"- default_member_open_id: {payload['default_member_open_id'] or '(未设置)'}")
        confirm = input_fn("确认写入? [y/N]: ")
        if not _is_yes(confirm, default=False):
            print_fn("已取消写入。")
            return 1

        write_json(paths.runtime_config_file, payload)
        print_fn("")
        print_fn("配置已保存。")

        sync_now = input_fn("下一步是否立即同步成员映射? [Y/n]: ")
        if _is_yes(sync_now, default=True):
            print_fn("开始同步授权范围内成员...")
            try:
                sync_meta = sync_fn(paths)
                print_fn(f"成员同步完成。成员数: {sync_meta.get('member_count', 0)}")
                for warning in sync_meta.get("warnings", []):
                    print_fn(f"提示: {warning.get('message', '')}")
            except Exception as exc:  # pragma: no cover - exercised through CLI behavior rather than narrow exception matching
                print_fn(f"成员同步失败: {exc}")
                print_fn("配置已保存，可稍后手动执行成员同步。")
        else:
            print_fn("已跳过成员同步，可稍后手动执行。")

        aliases = load_json(paths.alias_file, {})
        if aliases == {}:
            print_fn("提示: 如有重名成员，建议补充 feishu-task-management/toolkit/data/member_aliases.json。")
        print_fn("建议下一步执行:")
        print_fn("- python3 feishu-task-management/toolkit/scripts/feishu_config.py validate")
        print_fn("- python3 feishu-task-management/toolkit/scripts/feishu_members.py sync")
        return 0
    except KeyboardInterrupt:
        print_fn("")
        print_fn("已取消配置向导。")
        return 130


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = ToolkitPaths.discover()
    paths.ensure()
    try:
        if args.command == "guide":
            return run_guide(paths)
        if args.command == "set":
            existing = AppConfig.load(paths) if paths.runtime_config_file.exists() else None
            payload = {
                "app_id": args.app_id,
                "app_secret": args.app_secret,
                "user_access_token": (
                    args.user_access_token if args.user_access_token is not None else (existing.user_access_token if existing else "")
                ),
                "refresh_token": (
                    args.refresh_token if args.refresh_token is not None else (existing.refresh_token if existing else "")
                ),
                "user_token_expires_at": (
                    args.user_token_expires_at
                    if args.user_token_expires_at is not None
                    else (existing.user_token_expires_at if existing else "")
                ),
                "user_scope": args.user_scope if args.user_scope is not None else (existing.user_scope if existing else ""),
                "base_url": args.base_url,
                "timezone": args.timezone,
                "default_member_open_id": (
                    args.default_member_open_id
                    if args.default_member_open_id is not None
                    else (existing.default_member_open_id if existing else "")
                ),
            }
            write_json(paths.runtime_config_file, payload)
            _print({"status": "configured", "config_file": str(paths.runtime_config_file)})
            return 0
        if args.command == "show":
            runtime = load_json(paths.runtime_config_file, {})
            payload = {
                "runtime_config_file": str(paths.runtime_config_file),
                "runtime_config_present": paths.runtime_config_file.exists(),
                "runtime_config": {
                    "app_id": runtime.get("app_id", ""),
                    "app_secret": "*" * len(runtime.get("app_secret", "")) if runtime.get("app_secret") else "",
                    "user_access_token": "*" * len(runtime.get("user_access_token", ""))
                    if runtime.get("user_access_token")
                    else "",
                    "refresh_token": "*" * len(runtime.get("refresh_token", "")) if runtime.get("refresh_token") else "",
                    "user_token_expires_at": runtime.get("user_token_expires_at", ""),
                    "user_scope": runtime.get("user_scope", ""),
                    "base_url": runtime.get("base_url", ""),
                    "timezone": runtime.get("timezone", ""),
                    "default_member_open_id": runtime.get("default_member_open_id", ""),
                },
            }
            try:
                payload["effective_config"] = AppConfig.load(paths).to_public_dict()
            except AppConfigError as exc:
                payload["effective_config_error"] = str(exc)
            _print(payload)
            return 0
        if args.command == "validate":
            _print({"status": "ok", "config": AppConfig.load(paths).to_public_dict()})
            return 0
        if args.command == "clear":
            if not args.yes:
                raise AppConfigError("clear requires --yes")
            if paths.runtime_config_file.exists():
                paths.runtime_config_file.unlink()
            _print({"status": "cleared", "config_file": str(paths.runtime_config_file)})
            return 0
    except (AppConfigError, ApiError) as exc:
        payload = {"error": type(exc).__name__, "message": str(exc)}
        if isinstance(exc, ApiError):
            payload["code"] = exc.code
            payload["status"] = exc.status
            payload["payload"] = exc.payload
        _print(payload)
        return 1
    parser.error(f"unsupported command: {args.command}")
    return 2
