"""统一入口脚本 — 路由命令到对应脚本执行。

用法:
    python3 run.py <command> [args...]
"""

import json
import os
import subprocess
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_COMMANDS = [
    "upload", "search_keyword", "create_flow", "sign_url",
    "query_flow", "list_flows", "revoke_flow", "download_docs",
    "verify", "save_flow", "file_status", "extract_text", "format",
]


def _resolve_command(cmd, args):
    """将统一命令路由到对应脚本和参数。"""
    if cmd == "extract_text":
        return ["extract_text.py"] + list(args)
    elif cmd == "format":
        return ["format_contract.py"] + list(args)
    else:
        return ["esign_api.py", cmd] + list(args)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 run.py <command> [args...]", "commands": _COMMANDS}))
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    script_args = _resolve_command(cmd, args)
    script_path = os.path.join(_SCRIPT_DIR, script_args[0])

    python = sys.executable
    full_cmd = [python, script_path] + script_args[1:]

    result = subprocess.run(full_cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
