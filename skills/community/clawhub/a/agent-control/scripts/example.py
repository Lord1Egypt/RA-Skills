#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
import sys


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "ok": p.returncode == 0,
        "code": p.returncode,
        "cmd": " ".join(shlex.quote(c) for c in cmd),
        "stdout": p.stdout.strip(),
        "stderr": p.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description="OpenClaw agent control helper")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("list")

    p_create = sub.add_parser("create")
    p_create.add_argument("name")
    p_create.add_argument("--workspace")
    p_create.add_argument("--model")

    p_bind = sub.add_parser("bind")
    p_bind.add_argument("name")
    p_bind.add_argument("binding")

    p_unbind = sub.add_parser("unbind")
    p_unbind.add_argument("name")
    p_unbind.add_argument("binding")

    p_switch = sub.add_parser("switch")
    p_switch.add_argument("name")
    p_switch.add_argument("--channel", default="webchat")

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("name")

    args = parser.parse_args()

    if args.action == "list":
        result = run(["openclaw", "agents", "list"])
    elif args.action == "create":
        workspace = args.workspace or os.path.expanduser(f"~/clawd/agents/{args.name}")
        cmd = ["openclaw", "agents", "add", args.name, "--workspace", workspace]
        if args.model:
            cmd += ["--model", args.model]
        result = run(cmd)
    elif args.action == "bind":
        result = run(["openclaw", "agents", "bind", "--agent", args.name, "--bind", args.binding])
    elif args.action == "unbind":
        result = run(["openclaw", "agents", "unbind", "--agent", args.name, "--bind", args.binding])
    elif args.action == "switch":
        result = run(["openclaw", "agents", "bind", "--agent", args.name, "--bind", args.channel])
    elif args.action == "delete":
        result = run(["openclaw", "agents", "delete", args.name])
    else:
        parser.error("Unknown action")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ok"] else result["code"])


if __name__ == "__main__":
    main()
