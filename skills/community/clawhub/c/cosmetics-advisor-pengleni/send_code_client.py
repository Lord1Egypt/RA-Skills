#!/usr/bin/env python3
"""Send SMS verification code."""

import argparse
from typing import Any, Dict

from client_common import has_error, load_env_file, post_json, print_json, require_env


def send_code(phone: str) -> Dict[str, Any]:
    """Send SMS verification code.

    功能:
        调用站点级验证码接口发送短信验证码。

    输入:
        phone: 手机号字符串，预期为 11 位数字。

    输出:
        接口响应字典；失败时通常包含 error 字段。
    """
    site_base_url = require_env("SITE_BASE_URL").rstrip("/")
    url = f"{site_base_url}/chainlit/send-verification-code"
    return post_json(url, {"phone": phone})


def main() -> None:
    """CLI entrypoint for sending verification code.

    功能:
        解析命令行参数，加载环境变量，发送验证码并打印结果。

    输入:
        来自命令行参数的 env 文件路径与手机号。

    输出:
        无显式返回值；打印 JSON 到标准输出，失败时退出码为 1。
    """
    parser = argparse.ArgumentParser(description="Send verification code")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--phone", required=True, help="Phone number, e.g. 13800138000")
    args = parser.parse_args()

    load_env_file(args.env)
    result = send_code(args.phone)
    print_json(result)
    if has_error(result):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
