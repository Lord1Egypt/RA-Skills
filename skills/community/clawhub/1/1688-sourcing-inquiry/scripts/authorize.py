"""
OAuth 2.1 授权入口脚本（作为子进程运行）

用法：
    python3 scripts/authorize.py --scope "read:order" [--client-id xxx] [--timeout 300]
    python3 scripts/authorize.py --mode AK [--timeout 300]
"""
from __future__ import annotations

import argparse
import json
import logging
import secrets
import sys
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

# 确保 scripts/ 目录在 sys.path 中
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from _const import (
    CLIENT_ID,
    AUTHORIZE_ENDPOINT,
    AUTHORIZATION_TIMEOUT,
    CALLBACK_HOST,
    ENV_FILE,
    ENV_CLIENT_ID,
    AUTH_MODE_OAUTH,
    AUTH_MODE_AK,
)
from pkce import generate_pair
from callback_server import CallbackServer
from token_manager import load_token, has_scope
from secure_store import load_metadata

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def output_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False), flush=True)


def _run_ak_mode(timeout: int) -> int:
    try:
        state = secrets.token_urlsafe(32)
        server = CallbackServer(
            client_id="", redirect_uri="", code_verifier="",
            state=state, mode=AUTH_MODE_AK,
        )
        server.start()

        redirect_uri = f"http://{CALLBACK_HOST}:{server.port}/callback"
        server.redirect_uri = redirect_uri

        params = {"mode": AUTH_MODE_AK, "state": state, "redirect_uri": redirect_uri}
        authorize_url = f"{AUTHORIZE_ENDPOINT}?{urlencode(params)}"

        logger.info("正在打开浏览器获取 AK...")
        opened = webbrowser.open(authorize_url)
        if not opened:
            logger.info("\n请手动在浏览器中打开以下链接：\n  %s\n", authorize_url)
        else:
            logger.info("浏览器已打开，请在页面中完成 AK 获取。")
        logger.info("等待 AK 获取完成（超时 %d 秒）...", timeout)

        try:
            completed = server.wait(timeout=timeout)
        except KeyboardInterrupt:
            output_json({"success": False, "error_code": "USER_CANCELLED",
                         "markdown": "用户取消了操作。"})
            return 1
        finally:
            server.stop()

        if completed and server.success:
            ak = server.result.get("ak", "")
            output_json({"success": True, "markdown": "AK 设置成功", "data": {"ak": ak}})
            return 0

        if not completed:
            output_json({"success": False, "error_code": "AUTHORIZATION_TIMEOUT",
                         "markdown": f"用户未在 {timeout} 秒内完成操作，请重新发起。"})
            return 1

        result = server.result
        output_json({"success": False, "error_code": result.get("error", "UNKNOWN"),
                     "markdown": result.get("error_description", "AK 获取失败")})
        return 1
    except Exception as e:
        logger.exception("AK 模式执行异常: %s", e)
        output_json({"success": False, "error_code": "AK_MODE_ERROR",
                     "markdown": f"获取 AK 失败：{e}"})
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="1688 OAuth 2.1 授权")
    parser.add_argument("--scope", default=None)
    parser.add_argument("--client-id", default=None)
    parser.add_argument("--mode", default=AUTH_MODE_OAUTH,
                        choices=[AUTH_MODE_OAUTH, AUTH_MODE_AK])
    parser.add_argument("--timeout", type=int, default=AUTHORIZATION_TIMEOUT)
    parser.add_argument("--env-file", type=Path, default=ENV_FILE)
    args = parser.parse_args()

    env_file: Path = args.env_file
    timeout: int = args.timeout
    mode: str = args.mode

    if mode == AUTH_MODE_AK:
        return _run_ak_mode(timeout)

    requested_scope: str | None = args.scope
    if not requested_scope or not requested_scope.strip():
        output_json({"success": False, "error": "MISSING_SCOPE",
                     "message": "必须指定 --scope 参数"})
        return 1

    requested_scope = requested_scope.strip()
    client_id = args.client_id or load_metadata(ENV_CLIENT_ID, env_file) or CLIENT_ID

    # 检查已有有效 Token
    token = load_token(env_file)
    if token and not token["expired"] and has_scope(token["scope"], requested_scope):
        output_json({"success": True, "scope": token["scope"],
                     "expires_in": token["expires_in"],
                     "message": "已有有效授权，无需重新授权"})
        return 0

    # 增量授权：合并已有 scope
    if token and token["scope"]:
        existing = set(token["scope"].split())
        requested = set(requested_scope.split())
        merged_scope = " ".join(sorted(existing | requested))
    else:
        merged_scope = requested_scope

    code_verifier, code_challenge = generate_pair()
    state = secrets.token_urlsafe(32)

    server = CallbackServer(
        client_id=client_id, redirect_uri="",
        code_verifier=code_verifier, state=state, env_file=env_file,
    )
    server.start()

    redirect_uri = f"http://{CALLBACK_HOST}:{server.port}/callback"
    server.redirect_uri = redirect_uri

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": merged_scope,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    authorize_url = f"{AUTHORIZE_ENDPOINT}?{urlencode(params)}"

    logger.info("正在打开浏览器进行授权...")
    opened = webbrowser.open(authorize_url)
    if not opened:
        logger.info("\n请手动在浏览器中打开以下链接：\n  %s\n", authorize_url)
    else:
        logger.info("浏览器已打开，请在页面中完成登录和授权确认。")
    logger.info("等待授权完成（超时 %d 秒）...", timeout)

    try:
        completed = server.wait(timeout=timeout)
    except KeyboardInterrupt:
        output_json({"success": False, "error_code": "USER_CANCELLED",
                     "markdown": "用户取消了授权。"})
        return 1
    finally:
        server.stop()

    if completed and server.success:
        result = server.result
        output_json({"success": True, "markdown": "授权成功。",
                     "data": {"scope": result.get("scope", ""),
                              "expires_in": result.get("expires_in", 0)}})
        return 0

    if not completed:
        output_json({"success": False, "error_code": "AUTHORIZATION_TIMEOUT",
                     "markdown": f"用户未在 {timeout} 秒内完成授权，请重新发起。"})
        return 1

    result = server.result
    output_json({"success": False, "error_code": result.get("error", "UNKNOWN"),
                 "markdown": result.get("error_description", "授权失败")})
    return 1


if __name__ == "__main__":
    sys.exit(main())
