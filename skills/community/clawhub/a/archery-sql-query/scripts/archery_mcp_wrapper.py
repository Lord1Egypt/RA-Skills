#!/usr/bin/env python3
"""
MCP Wrapper - 启动 Archery MCP 服务器
"""
import json
import os
import sys
from pathlib import Path


def main() -> int:
    # 默认使用全局配置文件
    secrets_path = Path(
        os.getenv("ARCHERY_SECRETS_FILE", "~/.archery/config.json")
    ).expanduser()

    if not secrets_path.exists():
        print(
            f"请先配置凭证文件: {secrets_path}\n"
            f"或设置环境变量 ARCHERY_SECRETS_FILE",
            file=sys.stderr,
        )
        return 1

    secrets = json.loads(secrets_path.read_text())
    username = secrets.get("archery_username")
    password = secrets.get("archery_password")

    if not username or not password:
        print(
            "配置文件必须包含 archery_username 和 archery_password",
            file=sys.stderr,
        )
        return 1

    os.environ["ARCHERY_USERNAME"] = username
    os.environ["ARCHERY_PASSWORD"] = password

    server_path = Path(__file__).with_name("archery_mcp_server.py")
    os.execvp("python3", ["python3", str(server_path)])


if __name__ == "__main__":
    sys.exit(main())
