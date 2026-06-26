#!/usr/bin/env python3
"""
蝉镜凭证配置脚本。
- APP_ID / SECRET_KEY 写入项目路径 .env（默认 skills/chanjing-content-creation-skill/.env）。
用法: chanjing_config --app-id <app_id> --sk <secret_key> | --status | --help
"""
import argparse
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = Path(os.environ.get("CHANJING_ENV_FILE", str(SKILL_DIR / ".env")))
LOGIN_URL = "https://www.chanjing.cc/openapi/login"
DOC_URL = "https://doc.chanjing.cc"


def _read_env_file():
    if not ENV_FILE.exists():
        return {}
    result = {}
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and (
            (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")
        ):
            value = value[1:-1]
        result[key] = value
    return result


def _write_env_file(values):
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={values[key]}" for key in sorted(values.keys())]
    ENV_FILE.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    try:
        os.chmod(ENV_FILE, 0o600)
    except OSError:
        pass


def show_status():
    env_data = _read_env_file()
    app_id = env_data.get("CHANJING_APP_ID") or ""
    secret_key = env_data.get("CHANJING_SECRET_KEY") or ""
    has_user_id = bool(app_id)
    has_sk = bool(secret_key)

    print("ENV 路径:", ENV_FILE)
    print("APP_ID:", "已配置" if has_user_id else "未配置")
    print("secret_key:", "已配置" if has_sk else "未配置")

    if not has_user_id or not has_sk:
        print()
        print("请完成 APP_ID/SECRET_KEY 配置：")
        print("  chanjing_config --app-id <你的app_id> --sk <你的secret_key>")
        print()
        print("获取秘钥:", LOGIN_URL)
        return 1

    print("Token: 不落盘缓存（按需请求，进程内复用）")
    return 0


def set_credentials(app_id, sk):
    env_data = _read_env_file()
    env_data["CHANJING_APP_ID"] = app_id
    env_data["CHANJING_SECRET_KEY"] = sk
    env_data.pop("CHANJING_USER_ID", None)
    env_data.pop("USER_ID", None)
    env_data.pop("APP_ID", None)
    _write_env_file(env_data)
    print("凭证已保存到", ENV_FILE)
    print()
    print("验证配置: chanjing_config --status")


def main():
    parser = argparse.ArgumentParser(
        description="蝉镜凭证配置工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="存储位置: %s\n获取秘钥: %s\n文档: %s" % (ENV_FILE, LOGIN_URL, DOC_URL),
    )
    parser.add_argument("--app-id", "--user-id", "--ak", dest="app_id", help="App ID (兼容旧参数 --user-id/--ak)")
    parser.add_argument("--sk", help="Secret Key (secret_key)")
    parser.add_argument("--status", "-s", action="store_true", help="查看配置状态")

    args = parser.parse_args()

    if args.status:
        sys.exit(show_status())

    if args.app_id and args.sk:
        set_credentials(args.app_id, args.sk)
        return

    if args.app_id or args.sk:
        print("错误: 必须同时提供 --app-id（或 --user-id/--ak）和 --sk", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # 默认显示状态
    sys.exit(show_status())


if __name__ == "__main__":
    main()
