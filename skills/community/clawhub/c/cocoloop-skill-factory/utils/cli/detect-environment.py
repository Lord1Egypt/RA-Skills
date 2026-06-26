#!/usr/bin/env python3
"""Detect local execution environment and emit a conservative JSON snapshot."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))

from _common import command_version, default_platform_snapshot, env_flag, json_print, utc_now


def detect_shell() -> dict[str, Any]:
    shell = os.environ.get("SHELL") or os.environ.get("COMSPEC") or ""
    resolved = Path(shell).name if shell else ""
    return {
        "raw": shell,
        "name": resolved or None,
    }


def detect_agent_environment_hints(workspace: Path) -> dict[str, Any]:
    home = Path.home()
    shared_roots = [
        workspace / ".agents" / "skills",
        home / ".agents" / "skills",
    ]
    platform_markers = {
        "codex": [
            workspace / ".codex" / "skills",
            home / ".codex" / "skills",
        ],
        "claude code": [
            workspace / ".claude" / "skills",
            home / ".claude" / "skills",
        ],
        "openclaw": [
            workspace / ".openclaw",
            home / ".openclaw",
        ],
        "copaw": [
            workspace / ".copaw",
            home / ".copaw",
        ],
        "molili": [
            workspace / ".molili",
            home / ".molili",
        ],
        "hermes agent": [
            workspace / ".hermes",
            home / ".hermes",
        ],
    }

    shared_matches = [str(path.resolve()) for path in shared_roots if path.exists()]
    platform_hints: list[dict[str, Any]] = []
    for platform_name, candidates in platform_markers.items():
        matches = [str(path.resolve()) for path in candidates if path.exists()]
        if matches:
            platform_hints.append({"platform": platform_name, "matched_paths": matches})

    return {
        "shared_skill_roots": shared_matches,
        "platform_hints": platform_hints,
    }


def detect_browser() -> dict[str, Any] | None:
    candidates = [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "brave-browser",
        "microsoft-edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Safari.app/Contents/MacOS/Safari",
    ]

    for candidate in candidates:
        if candidate.endswith(".app/Contents/MacOS/Safari"):
            result = command_version(candidate, version_args=("--version", "-version", "--product-version"))
        else:
            result = command_version(candidate)
        if result["available"]:
            return {
                "name": Path(candidate).name if "/" in candidate else candidate,
                "path": result["path"],
                "version": result["version"],
            }

    return None


def build_snapshot() -> dict[str, Any]:
    workspace = Path.cwd()
    commands = [
        "python3",
        "python",
        "node",
        "npm",
        "uv",
        "git",
        "cocoloop",
        "clawhub",
    ]

    command_states = []
    for command in commands:
        if command == "clawhub":
            info = command_version(command, version_args=("--cli-version", "-V", "--version"))
        else:
            info = command_version(command)
        command_states.append(
            {
                "name": command,
                "available": info["available"],
                "path": info["path"],
                "version": info["version"],
            }
        )

    browser = detect_browser()
    shell = detect_shell()
    environment_hints = detect_agent_environment_hints(workspace)

    return {
        "tool": "detect-environment",
        "status": "ok",
        "detected_at": utc_now(),
        "platform": default_platform_snapshot(),
        "environment_flags": {
            "inside_ci": env_flag("CI"),
            "inside_container": env_flag("CI") or env_flag("DOCKER_CONTAINER"),
        },
        "workspace": str(workspace.resolve()),
        "shell": shell,
        "commands": command_states,
        "browser": browser,
        "agent_environment_hints": environment_hints,
        "warnings": [
            "browser_not_found" if browser is None else "",
            "agent_environment_unknown" if not environment_hints["shared_skill_roots"] and not environment_hints["platform_hints"] else "",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect local environment and emit JSON.")
    parser.parse_args()
    payload = build_snapshot()
    payload["warnings"] = [item for item in payload["warnings"] if item]
    return json_print(payload)


if __name__ == "__main__":
    raise SystemExit(main())
