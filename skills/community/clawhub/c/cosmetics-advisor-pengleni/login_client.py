#!/usr/bin/env python3
"""Login with phone and verification code."""

import argparse
from typing import Any, Dict

from client_common import has_error, load_env_file, post_json, print_json, require_env, save_session


def login(phone: str, verify_code: str, session_id: str = "") -> Dict[str, Any]:
    """Login with phone verification code and create/reuse a session.

    功能:
        调用登录接口，基于手机号和验证码获取 user_id/session_id。

    输入:
        phone: 手机号字符串。
        verify_code: 短信验证码。
        session_id: 可选会话 ID，用于尝试延续已有会话。

    输出:
        登录接口响应字典；失败时通常包含 error 字段。
    """
    api_base_url = require_env("API_BASE_URL").rstrip("/")
    token = require_env("CLAWHUB_SKILL_TOKEN")

    payload: Dict[str, Any] = {
        "phone": phone,
        "verify_code": verify_code,
    }
    if session_id:
        payload["session_id"] = session_id

    url = f"{api_base_url}/session/login"
    return post_json(url, payload, token=token)


def main() -> None:
    """CLI entrypoint for login flow.

    功能:
        解析命令行参数，执行登录，并在成功后写入会话文件。

    输入:
        命令行参数中的 env 路径、phone、verify_code、session_id、session_file。

    输出:
        无显式返回值；打印 JSON 到标准输出，失败时抛出 SystemExit。
    """
    parser = argparse.ArgumentParser(description="Login and create/reuse session")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--phone", required=True, help="Phone number")
    parser.add_argument("--verify-code", required=True, help="Verification code")
    parser.add_argument("--session-id", default="", help="Optional existing session id")
    parser.add_argument(
        "--session-file",
        default=".session.json",
        help="Where to persist user_id/session_id, default: .session.json",
    )
    args = parser.parse_args()

    load_env_file(args.env)
    result = login(args.phone, args.verify_code, args.session_id)

    if has_error(result):
        print_json(result)
        raise SystemExit(1)

    if result.get("user_id") and result.get("session_id"):
        save_session(
            {
                "user_id": result["user_id"],
                "session_id": result["session_id"],
            },
            path=args.session_file,
        )
    else:
        print_json(result)
        raise SystemExit("[ERROR] login response missing user_id/session_id")

    print_json(result)


if __name__ == "__main__":
    main()
