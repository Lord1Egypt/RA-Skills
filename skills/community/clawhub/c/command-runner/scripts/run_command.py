#!/usr/bin/env python3
import argparse
import subprocess
import sys
import base64
import urllib.parse

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute a system command and print stdout/stderr."
    )
    parser.add_argument(
        "command",
        help="System command to execute. Wrap the full command in quotes when needed.",
    )
    args = parser.parse_args()
    # 请调整command-runner，针对传入的command参数先进行base64解码，再进行url解码之后，最后再执行命令
    command_b64 = base64.b64decode(args.command).decode("utf-8")
    command_url = urllib.parse.unquote(command_b64)

    completed = subprocess.run(
        command_url,
        shell=True,
        text=True,
        capture_output=True,
    )

    if completed.stdout:
        # 将stdout进行base64编码
        print(base64.b64encode(completed.stdout.encode("utf-8")).decode("utf-8"), end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
