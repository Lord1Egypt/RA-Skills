#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parents[1]
WORKSPACE_DIR = SCRIPT_PATH.parents[3]
CONFIG_PATH = WORKSPACE_DIR / "config" / "mcporter.json"
SERVER_NAME = "codex-cli"


def fail(message: str, code: int = 1) -> "NoReturn":
    print(message, file=sys.stderr)
    raise SystemExit(code)


try:
    from typing import NoReturn
except ImportError:  # pragma: no cover
    NoReturn = None  # type: ignore


def run(cmd: list[str], *, timeout_ms: int | None = None) -> subprocess.CompletedProcess[str]:
    timeout = None if timeout_ms is None else max(1, timeout_ms / 1000)
    return subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        fail(f"Missing required binary: {name}")
    return path


def mcporter_base() -> list[str]:
    return [require_binary("mcporter"), "--config", str(CONFIG_PATH)]


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.stdin_prompt:
        return sys.stdin.read()
    fail("Provide one of: --prompt, --prompt-file, or --stdin-prompt")


def cmd_doctor(_: argparse.Namespace) -> int:
    result = {
        "workspace": str(WORKSPACE_DIR),
        "skillDir": str(SKILL_DIR),
        "config": {"path": str(CONFIG_PATH), "exists": CONFIG_PATH.exists()},
        "binaries": {
            "mcporter": shutil.which("mcporter"),
            "codex": shutil.which("codex"),
            "codex-mcp": shutil.which("codex-mcp"),
        },
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not CONFIG_PATH.exists():
        fail("mcporter config is missing")

    schema = run(mcporter_base() + ["list", SERVER_NAME, "--schema", "--timeout", "20000"])
    if schema.returncode != 0:
        sys.stderr.write(schema.stderr or schema.stdout)
        fail("mcporter schema probe failed", schema.returncode)

    print("\nMCP schema probe: OK")
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    res = run(mcporter_base() + ["call", f"{SERVER_NAME}.version", "--output", "text", "--timeout", "30000"])
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
    return res.returncode


def cmd_ping(args: argparse.Namespace) -> int:
    res = run(
        mcporter_base()
        + [
            "call",
            f"{SERVER_NAME}.ping",
            f"prompt={args.message}",
            "--output",
            "text",
            "--timeout",
            "30000",
        ]
    )
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
    return res.returncode


def cmd_ask(args: argparse.Namespace) -> int:
    prompt = read_prompt(args).strip()
    if not prompt:
        fail("Prompt is empty")

    payload: dict[str, Any] = {
        "prompt": prompt,
        "timeout": args.timeout_ms,
        "includeThinking": args.include_thinking,
        "includeMetadata": not args.hide_metadata,
    }

    if args.cwd:
        payload["workingDir"] = str(Path(args.cwd).expanduser().resolve())
    if args.model:
        payload["model"] = args.model
    if args.profile:
        payload["profile"] = args.profile
    if args.full_auto:
        payload["fullAuto"] = True
    if args.approval_policy:
        payload["approvalPolicy"] = args.approval_policy
    if args.sandbox_mode:
        payload["sandboxMode"] = args.sandbox_mode
    if args.search:
        payload["search"] = True
    if args.oss:
        payload["oss"] = True
    if args.yolo:
        payload["yolo"] = True

    overall_timeout_ms = max(args.timeout_ms + 60000, 120000)
    res = run(
        mcporter_base()
        + [
            "call",
            f"{SERVER_NAME}.ask-codex",
            "--args",
            json.dumps(payload, ensure_ascii=False),
            "--output",
            "text",
            "--timeout",
            str(overall_timeout_ms),
        ],
        timeout_ms=overall_timeout_ms + 5000,
    )
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
    return res.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convenience wrapper for the local Codex MCP server via mcporter."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check binaries, config, and schema discovery")
    doctor.set_defaults(func=cmd_doctor)

    version = sub.add_parser("version", help="Show Codex + MCP version info")
    version.set_defaults(func=cmd_version)

    ping = sub.add_parser("ping", help="Echo a message through the MCP server")
    ping.add_argument("message", nargs="?", default="ping")
    ping.set_defaults(func=cmd_ping)

    ask = sub.add_parser("ask", help="Send a coding task to the local Codex MCP server")
    prompt_group = ask.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text")
    prompt_group.add_argument("--prompt-file", help="Read prompt text from a file")
    prompt_group.add_argument(
        "--stdin-prompt", action="store_true", help="Read prompt text from stdin"
    )
    ask.add_argument("--cwd", help="Working directory for Codex")
    ask.add_argument("--model", help="Override Codex model")
    ask.add_argument("--profile", help="Use a named Codex profile")
    ask.add_argument(
        "--timeout-ms",
        type=int,
        default=300000,
        help="Task timeout forwarded to the MCP tool (default: 300000)",
    )
    ask.add_argument(
        "--full-auto",
        action="store_true",
        help="Enable normal implementation mode (workspace-write + on-failure approval)",
    )
    ask.add_argument(
        "--approval-policy",
        choices=["never", "on-request", "on-failure", "untrusted"],
        help="Explicit Codex approval policy",
    )
    ask.add_argument(
        "--sandbox-mode",
        choices=["read-only", "workspace-write", "danger-full-access"],
        help="Explicit Codex sandbox mode",
    )
    ask.add_argument("--search", action="store_true", help="Enable Codex web search")
    ask.add_argument("--oss", action="store_true", help="Use local Ollama mode")
    ask.add_argument("--yolo", action="store_true", help="Allow aggressive Codex execution")
    ask.add_argument(
        "--include-thinking",
        action="store_true",
        help="Include Codex reasoning in the returned text",
    )
    ask.add_argument(
        "--hide-metadata",
        action="store_true",
        help="Hide tool metadata in the returned text",
    )
    ask.set_defaults(func=cmd_ask)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
