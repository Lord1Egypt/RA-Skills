#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path

from runtime_config import load_runtime_env, require_em_api_key


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_DIR = Path.home() / ".uwillberich" / "news-iterator"
DEFAULT_LABEL = "com.tingchi.uwillberich-news-iterator"
DEFAULT_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{DEFAULT_LABEL}.plist"


load_runtime_env()
require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")


def run_command(args: list[str], check: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def build_plist(interval_seconds: int, state_dir: Path, python_bin: str) -> dict:
    state_dir.mkdir(parents=True, exist_ok=True)
    load_runtime_env()
    plist = {
        "Label": DEFAULT_LABEL,
        "ProgramArguments": [
            python_bin,
            str(ROOT / "scripts" / "news_iterator.py"),
            "--state-dir",
            str(state_dir),
            "poll",
        ],
        "RunAtLoad": True,
        "StartInterval": interval_seconds,
        "WorkingDirectory": str(ROOT),
        "StandardOutPath": str(state_dir / "launchd.out.log"),
        "StandardErrorPath": str(state_dir / "launchd.err.log"),
    }
    env_vars = {}
    runtime_env_path = os.environ.get("UWILLBERICH_RUNTIME_ENV") or os.environ.get("A_SHARE_RUNTIME_ENV")
    if runtime_env_path:
        env_vars["UWILLBERICH_RUNTIME_ENV"] = runtime_env_path
    if env_vars:
        plist["EnvironmentVariables"] = env_vars
    return plist


def unload_if_present(plist_path: Path) -> None:
    domain = f"gui/{os.getuid()}"
    run_command(["launchctl", "bootout", domain, str(plist_path)], check=False)


def install(args: argparse.Namespace) -> int:
    plist_path = Path(args.plist_path)
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    state_dir = Path(args.state_dir)
    plist = build_plist(args.interval_seconds, state_dir, args.python_bin)
    with plist_path.open("wb") as handle:
        plistlib.dump(plist, handle)

    unload_if_present(plist_path)
    domain = f"gui/{os.getuid()}"
    run_command(["launchctl", "bootstrap", domain, str(plist_path)], check=True)
    run_command(["launchctl", "kickstart", "-k", f"{domain}/{DEFAULT_LABEL}"], check=False)
    print(f"installed: {plist_path}")
    print(f"state_dir: {state_dir}")
    print(f"interval_seconds: {args.interval_seconds}")
    return 0


def uninstall(args: argparse.Namespace) -> int:
    plist_path = Path(args.plist_path)
    if plist_path.exists():
        unload_if_present(plist_path)
        plist_path.unlink()
        print(f"removed: {plist_path}")
    else:
        print(f"not found: {plist_path}")
    return 0


def status(args: argparse.Namespace) -> int:
    plist_path = Path(args.plist_path)
    print(f"plist: {plist_path}")
    print(f"exists: {plist_path.exists()}")
    if not plist_path.exists():
        return 0

    result = run_command(["launchctl", "print", f"gui/{os.getuid()}/{DEFAULT_LABEL}"], check=False)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(result.stderr.strip() or result.stdout.strip())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install the news iterator as a launchd agent on macOS.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install and load the launchd job.")
    install_parser.add_argument("--interval-seconds", type=int, default=300, help="Polling interval.")
    install_parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="State directory.")
    install_parser.add_argument("--plist-path", default=str(DEFAULT_PLIST), help="LaunchAgent plist path.")
    install_parser.add_argument("--python-bin", default=sys.executable, help="Python interpreter path.")
    install_parser.set_defaults(func=install)

    uninstall_parser = subparsers.add_parser("uninstall", help="Unload and remove the launchd job.")
    uninstall_parser.add_argument("--plist-path", default=str(DEFAULT_PLIST), help="LaunchAgent plist path.")
    uninstall_parser.set_defaults(func=uninstall)

    status_parser = subparsers.add_parser("status", help="Show launchd job status.")
    status_parser.add_argument("--plist-path", default=str(DEFAULT_PLIST), help="LaunchAgent plist path.")
    status_parser.set_defaults(func=status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
