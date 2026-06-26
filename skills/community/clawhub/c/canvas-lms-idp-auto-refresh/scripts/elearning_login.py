from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

from auth_session import (
    AppConfig,
    DEFAULT_ENTITY_ID,
    DEFAULT_ENTRY_URL,
    DEFAULT_IDP_BASE,
    DEFAULT_SETTINGS_REFERER,
    DEFAULT_TIMEOUT,
    DEFAULT_TOKEN_API,
    ElearningAuthClient,
    FlowError,
    LoginPreparationResult,
    mask,
)
from token_ops import CanvasTokenManager

LOGGER = logging.getLogger("elearning_login")


def dump_debug_artifacts(base_dir: Path, filename: str, content: str) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    target = base_dir / filename
    target.write_text(content, encoding="utf-8")
    LOGGER.debug("已写入调试文件：%s", target)


def dump_cookies(base_dir: Path, session: requests.Session) -> None:
    lines = [f"{cookie.domain}\t{cookie.name}\t{mask(cookie.value or '')}" for cookie in session.cookies]
    dump_debug_artifacts(base_dir, "cookies.txt", "\n".join(lines))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Elearning 新版 IDP 登录并创建 Canvas Token")
    parser.add_argument("--debug", action="store_true", help="开启调试日志")
    parser.add_argument("--dry-run", action="store_true", help="只跑到公钥获取，不做登录提交")
    parser.add_argument("--skip-token", action="store_true", help="登录后跳过 Token 创建")
    parser.add_argument(
        "--cleanup-old-tokens",
        action="store_true",
        default=os.getenv("ELEARNING_CLEANUP_OLD_TOKENS", "0").strip().lower() in {"1", "true", "yes", "on"},
        help="创建新 token 后，按 purpose 删除旧 token（保留新建 token）",
    )
    parser.add_argument(
        "--cleanup-purpose",
        default=os.getenv("ELEARNING_CLEANUP_PURPOSE", "").strip(),
        help="清理匹配的 purpose（默认使用当前创建 token 的 purpose）",
    )
    parser.add_argument(
        "--cleanup-dry-run",
        action="store_true",
        help="只输出将被删除的 token，不实际删除",
    )
    parser.add_argument("--dump-dir", default="debug_output", help="调试文件输出目录")
    return parser.parse_args(argv)


def load_config_from_env(*, allow_missing_credentials: bool = False) -> AppConfig:
    load_dotenv()

    username = os.getenv("ELEARNING_USERNAME", "").strip()
    password = os.getenv("ELEARNING_PASSWORD", "").strip()

    if (not username or not password) and not allow_missing_credentials:
        raise FlowError("缺少环境变量 ELEARNING_USERNAME / ELEARNING_PASSWORD")

    timeout_str = os.getenv("ELEARNING_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT)).strip()
    timeout_seconds = int(timeout_str) if timeout_str.isdigit() else DEFAULT_TIMEOUT

    return AppConfig(
        username=username,
        password=password,
        entry_url=os.getenv("ELEARNING_ENTRY_URL", DEFAULT_ENTRY_URL),
        entity_id=os.getenv("ELEARNING_ENTITY_ID", DEFAULT_ENTITY_ID),
        idp_base_url=os.getenv("ELEARNING_IDP_BASE_URL", DEFAULT_IDP_BASE),
        timeout_seconds=timeout_seconds,
        token_api_url=os.getenv("ELEARNING_TOKEN_API_URL", DEFAULT_TOKEN_API),
        token_purpose=os.getenv("ELEARNING_TOKEN_PURPOSE", "OpenClaw Auto Refresh Token"),
        settings_referer=os.getenv("ELEARNING_SETTINGS_REFERER", DEFAULT_SETTINGS_REFERER),
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    try:
        config = load_config_from_env(allow_missing_credentials=args.dry_run)
        auth_client = ElearningAuthClient(config)
        token_manager = CanvasTokenManager(session=auth_client.session, config=config)
        debug_dir = Path(args.dump_dir)

        login_result: LoginPreparationResult = auth_client.login_and_prepare_session(dry_run=args.dry_run)

        dump_debug_artifacts(debug_dir, "entry_response.html", login_result.entry_response.text)
        dump_debug_artifacts(
            debug_dir,
            "query_auth_methods.json",
            json.dumps(login_result.auth_methods_body, ensure_ascii=False, indent=2),
        )
        dump_debug_artifacts(
            debug_dir,
            "get_js_public_key.json",
            json.dumps(login_result.public_key_body, ensure_ascii=False, indent=2),
        )

        if args.dry_run:
            LOGGER.info("dry-run 完成：已拿到 lck/authChainCode/publicKey")
            dump_cookies(debug_dir, auth_client.session)
            return 0

        LOGGER.info("RSA 加密完成。cipher_len=%s", len(login_result.encrypted_password or ""))

        auth_body = login_result.auth_body or {}
        dump_debug_artifacts(
            debug_dir,
            "auth_execute.json",
            json.dumps(auth_body, ensure_ascii=False, indent=2),
        )

        LOGGER.info("已提取 loginToken（masked）=%s", mask(login_result.login_token or ""))

        if login_result.authn_engine_response is not None:
            dump_debug_artifacts(debug_dir, "authn_engine_response.html", login_result.authn_engine_response.text)

        dump_cookies(debug_dir, auth_client.session)

        if args.skip_token:
            LOGGER.info("已按参数跳过 Token 创建。")
            return 0

        csrf_token = auth_client.extract_csrf()
        token_body = token_manager.create_canvas_token(csrf_token)
        dump_debug_artifacts(
            debug_dir,
            "create_token.json",
            json.dumps(token_body, ensure_ascii=False, indent=2),
        )

        if args.cleanup_old_tokens:
            cleanup_purpose = args.cleanup_purpose.strip() or str(
                token_body.get("purpose") or config.token_purpose
            )
            keep_token_id = str(token_body.get("id")) if token_body.get("id") is not None else None
            cleanup_summary = token_manager.cleanup_old_tokens_by_purpose(
                csrf_token=csrf_token,
                purpose=cleanup_purpose,
                keep_token_id=keep_token_id,
                dry_run=args.cleanup_dry_run,
            )
            dump_debug_artifacts(
                debug_dir,
                "cleanup_summary.json",
                json.dumps(cleanup_summary, ensure_ascii=False, indent=2),
            )

        visible_token = token_body.get("visible_token")
        if visible_token:
            print(f"NEW_TOKEN={visible_token}")
        else:
            print("Token 创建成功，但响应中无 visible_token 字段，请检查 create_token.json")
        return 0

    except FlowError as exc:
        LOGGER.error("流程失败：%s", exc)
        return 2
    except requests.RequestException as exc:
        LOGGER.error("网络请求失败：%s", exc)
        return 3
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception("未预期异常：%s", exc)
        return 9


if __name__ == "__main__":
    raise SystemExit(main())
