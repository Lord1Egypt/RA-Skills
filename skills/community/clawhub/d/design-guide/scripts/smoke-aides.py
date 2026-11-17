#!/usr/bin/env python3
"""Opt-in provider-backed navigation smoke tests for supported AIDEs."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


PROMPT = (
    "使用已安装的 design-guide。只进入导航模式，不修改任何文件。读取 design-guide.json 后，"
    "第一行严格输出 F_DESIGN_SMOKE version=<版本号>，随后只列出三项可选前端任务。"
)


def release_version(root: pathlib.Path) -> str:
    manifest = json.loads((root / "design-guide.json").read_text(encoding="utf-8"))
    manifest_version = manifest.get("version") if isinstance(manifest, dict) else None
    version_file = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not isinstance(manifest_version, str) or not version_file or manifest_version != version_file:
        raise ValueError("VERSION and design-guide.json version must match before provider smoke tests")
    return manifest_version


def commands(workspace: pathlib.Path) -> dict[str, list[str]]:
    return {
        "codex": [
            "codex", "exec", "--skip-git-repo-check", "--ephemeral", "--sandbox", "read-only",
            "--color", "never", PROMPT,
        ],
        "claude": [
            "claude", "-p", "--permission-mode", "plan", "--no-session-persistence",
            "/design-guide " + PROMPT,
        ],
        "qwen": [
            "qwen", "--approval-mode", "plan", "--chat-recording", "false", "--output-format", "text", PROMPT,
        ],
        "cursor": [
            "cursor", "agent", "-p", "--mode", "ask", "--workspace", str(workspace), PROMPT,
        ],
    }


def run_smoke(aide: str, command: list[str], workspace: pathlib.Path, version: str, timeout: int) -> dict:
    executable = shutil.which(command[0])
    if executable is None:
        return {"aide": aide, "status": "not-installed", "command": command, "output": "CLI not found"}
    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + (exc.stderr or "")).strip()
        return {"aide": aide, "status": "blocked", "command": command, "output": output or "timed out"}
    marker = f"F_DESIGN_SMOKE version={version}"
    status = "invoked" if result.returncode == 0 and marker in output else "blocked"
    return {
        "aide": aide,
        "status": status,
        "exitCode": result.returncode,
        "command": command,
        "output": output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=t("Run explicit provider-backed design-guide invocation tests. May consume model quota.")
    )
    add_locale_argument(parser)
    parser.add_argument("--aide", action="append", choices=("codex", "claude", "qwen", "cursor"), required=True)
    parser.add_argument("--workspace", default="/tmp")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--json-out")
    parser.add_argument("--yes-consume-provider-quota", action="store_true")
    args = parser.parse_args()
    if not args.yes_consume_provider_quota:
        print(t("Refusing provider calls without --yes-consume-provider-quota", args.locale), file=sys.stderr)
        return 2
    root = pathlib.Path(__file__).resolve().parents[1]
    try:
        version = release_version(root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(t("Release version check failed: {error}", args.locale, error=exc), file=sys.stderr)
        return 2
    workspace = pathlib.Path(args.workspace).resolve()
    available = commands(workspace)
    results = [run_smoke(aide, available[aide], workspace, version, args.timeout) for aide in args.aide]
    payload = {"version": version, "results": results}
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if all(item["status"] == "invoked" for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
